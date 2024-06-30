import utilities

# ----- lowlvl_fsf -----
def lowlvl_fsf(fsf_dir,
               input_file, 
               output_dir,
               confound_file,
               alternative_reference, 
               tr, 
               total_volumes,
               ev_files, 
               ev_names, 
               contrasts,
               delete_volumes = 0,
               high_pass_filter = 100,
               motion_correction = "None",
               b0_unwarping = False,
               slice_timing_correction = "None",
               brain_extraction = False,
               spatial_smoothing = 5,
               intensity_normalization = False,
               perfusion_subtraction = False,
               highpass = False,
               melodica_ICA = False,
               registration_reference = "/usr/local/fsl/data/standard/MNI152_T1_mm_brain",
               linear_search = "Normal",
               dof = "6 DOF",
               film_prewhitening = True,
               thresholding = "None",
               cluster_z = 3.1,
               cluster_p = 0.05,
               timeseries_plot = False):

    """
    Generates a first level .fsf file with specified parameters.

    Parameters:
    input_file (str): The path to the .nii.gz file.
    output_dir (str): The directory where the output should be saved.
    confound_file (str): The path to the confound file.
    alternative_reference (str): The alternative reference for slice timing correction.
    tr (float): Repetition time.
    total_volumes (int): Total number of volumes.
    ev_files (list): List of paths to EV files.
    ev_names (list): List of names for EVs.
    contrasts (dict): Dictionary of contrasts.
    delete_volumes (int): Number of volumes to delete. Default is 0.
    high_pass_filter (float): High-pass filter value. Default is 100.
    motion_correction (str): Motion correction method. Default is "None".
    b0_unwarping (bool): Whether to perform B0 unwarping. Default is False.
    slice_timing_correction (str): Slice timing correction method. Default is "None".
    brain_extraction (bool): Whether to perform brain extraction. Default is False.
    spatial_smoothing (float): Spatial smoothing value in mm. Default is 5.
    intensity_normalization (bool): Whether to perform intensity normalization. Default is False.
    perfusion_subtraction (bool): Whether to perform perfusion subtraction. Default is False.
    highpass (bool): Whether to apply highpass filter. Default is False.
    melodica_ICA (bool): Whether to perform MELODIC ICA analysis. Default is False.
    registration_reference (str): Registration reference file. Default is MNI152_T1_2mm_brain.
    linear_search (str): Linear search method. Default is "Normal".
    dof (str): Degrees of freedom for registration. Default is "6 DOF".
    film_prewhitening (bool): Whether to perform FILM prewhitening. Default is True.
    thresholding (str): Thresholding method. Default is "None".
    cluster_z (float): Z-threshold for clusters. Default is 3.29.
    cluster_p (float): P-threshold for clusters. Default is 0.001.
    timeseries_plot (bool): Whether to generate timeseries plots. Default is False.

    Returns:
    an .fsf file at the specified path

    Example:
    lowlvl_fsf(
        input_file="path/to/your/input_file.nii.gz",
        output_dir="path/to/your/output_directory",
        confound_file="path/to/your/confound_file.txt",
        tr=2.0,
        total_volumes=240,
        ev_files=["path/to/your/ev1.txt", "path/to/your/ev2.txt", "path/to/your/ev3.txt"],
        ev_names=["EV1", "EV2", "EV3"],
        contrasts={
            "Contrast 1": [1, 0, 0],
            "Contrast 2": [0, 1, 0],
            "Contrast 3": [0, 0, 1]
        }
    )    
    """
    # --- QA Checks ---
    # Checking the file paths for inputs and outputs
    for path in [fsf_dir, input_file, output_dir]:
        utilities.check_directory_exists(path)

    # If a confound file was submitted, checking that it exists
    if confound_file is not None:
        utilities.check_directory_exists(confound_file)
    
    # If an alternative reference file was submitted, checking that it exists
    if alternative_reference is not None:
        utilities.check_directory_exists(alternative_reference)

    # Checking the file paths for ev files 
    for ev in ev_files:
        utilities.check_directory_exists(ev)

    # Checking that the number of EV names matches the number of files submitted
    if len(ev_files) != len(ev_names):
        raise ValueError("The number of EV files must be equal to the number of EV names.")

    # --- Defining variables

    # Checking if TR has been manually defined
    if tr is None:
        tr = utilities.tr_from_nifti(input_file)

    # Checking if volumes have been manually defined
    if total_volumes is None:
        total_volumes = utilities.vols_from_nifti(input_file)

    # Defining number of EVs and contrasts
    n_evs = len(ev_files)
    n_contrasts = len(contrasts)
    
    # Creating an object to retain fsf text
    fsf_content = f"""
# FEAT version number
set fmri(version) 6.00

# Are we in MELODIC?
set fmri(inmelodic) {1 if melodica_ICA else 0}

# Analysis level
# 1 : First-level analysis
# 2 : Higher-level analysis
set fmri(level) 1

# Which stages to run
# 0 : No first-level analysis (registration and/or group stats only)
# 7 : Full first-level analysis
set fmri(analysis) 7

# Use relative filenames
set fmri(relative_yn) 0

# TR(s)
set fmri(tr) {tr}

# Total volumes
set fmri(npts) {total_volumes}

# Delete volumes
set fmri(ndelete) {delete_volumes}

# Perfusion tag/control order
set fmri(tagfirst) 1

# Number of first-level designs
set fmri(multilev_yn) 0

# Number of EVs
set fmri(evs_orig) {n_evs}
set fmri(evs_real) {n_evs}
set fmri(evs_vox) 0

# Number of contrasts
set fmri(ncon_orig) {n_contrasts}
set fmri(ncon_real) {n_contrasts}

# Number of F-tests
set fmri(nftests_orig) 0
set fmri(nftests_real) 0

# Number of parametric EVs
set fmri(parevs) 0

# Number of time points
set fmri(npts) {total_volumes}

# Add temporal derivatives
set fmri(temphp_yn) 1

# Highpass temporal filtering
set fmri(paradigm_hp) {high_pass_filter}

# Motion correction
set fmri(realign) {1 if motion_correction != "None" else 0}

# B0 unwarping
set fmri(unwarp_dir) {1 if b0_unwarping else 0}

# Slice timing correction
set fmri(st) {1 if slice_timing_correction != "None" else 0}
set fmri(st_yn) {1 if slice_timing_correction != "None" else 0}
set fmri(st_refslice) {alternative_reference}

# Brain extraction
set fmri(bet_yn) {1 if brain_extraction else 0}

# Spatial smoothing FWHM (mm)
set fmri(smooth) {spatial_smoothing}

# Intensity normalization
set fmri(norm_yn) {1 if intensity_normalization else 0}

# Perfusion subtraction
set fmri(perfsub) {1 if perfusion_subtraction else 0}

# Highpass filter
set fmri(paradigm_hp) {1 if highpass else 0}

# MELODIC ICA
set fmri(melodic) {1 if melodica_ICA else 0}

# Registration reference
set fmri(regstandard) {registration_reference}

# Linear search
set fmri(reghighres_yn) {linear_search}

# Degrees of freedom
set fmri(dof) {dof}

# FILM prewhitening
set fmri(prewhiten) {1 if film_prewhitening else 0}

# Thresholding
set fmri(thresh) {thresholding}

# Cluster Z-threshold
set fmri(thresh_z) {cluster_z}

# Cluster P-threshold
set fmri(thresh_p) {cluster_p}

# Confound EVs text file
set fmri(confoundevs) 1
set confoundev_files(1) "{confound_file}"

# Add motion parameters to model
set fmri(motionevs) 0
set fmri(motionevsbeta) ""

# First-level analysis output directory
set fmri(outputdir) "{output_dir}"

# Input filename
set feat_files(1) "{input_file}"
    """

    # Adding EVs
    for i, (ev_file, ev_name) in enumerate(zip(ev_files, ev_names), start=1):
        fsf_content += f"""
# EV {i} - {ev_name}
set fmri(evtitle{i}) "{ev_name}"
set fmri(shape{i}) 3
set fmri(convolve{i}) 3
set fmri(convolve_phase{i}) 0
set fmri(tempfilt_yn{i}) 1
set fmri(deriv_yn{i}) 1
set fmri(custom{i}) "{ev_file}"
        """

    # Adding contrasts
    fsf_content += "\n# Contrast & F-tests mode\nset fmri(con_mode_old) 0\nset fmri(con_mode) 1\n"
    
    for j, (contrast_name, contrast_values) in enumerate(contrasts.items(), start=1):
        fsf_content += f"""
# Contrast {j} - {contrast_name}
set fmri(conpic_real.{j}) 1
set fmri(conname_real.{j}) "{contrast_name}"
        """
        for k, value in enumerate(contrast_values, start=1):
            fsf_content += f"set fmri(con_real{j}.{k}) {value}\n"

    fsf_content += "\n# Now run FEAT\nset fmri(overwrite_yn) 1\n"
    
    with open(fsf_dir + "/design.fsf", "w") as file:
        file.write(fsf_content)
    
    # Print if successfully completed
    print("FSF file generated successfully.")