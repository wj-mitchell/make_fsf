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
               dof, # Respecify a value for this
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
# 1 : Pre-processing
# 2 : Statistics
set fmri(analysis) 7

# Use relative filenames
set fmri(relative_yn) 0

# Cleanup first-level standard-space images
set fmri(sscleanup_yn) 0

# First-level analysis output directory
set fmri(outputdir) "{output_dir}"

# TR(s)
set fmri(tr) {tr}

# Total volumes
set fmri(npts) {total_volumes}

# Delete volumes
set fmri(ndelete) {delete_volumes}

# Perfusion tag/control order
set fmri(tagfirst) 1

# Number of first-level analyses
set fmri(multiple) 1

# Higher-level input type
# 1 : Inputs are lower-level FEAT directories
# 2 : Inputs are cope images from FEAT directories
set fmri(inputtype) 2

# Carry out pre-stats processing?
set fmri(filtering_yn) 1

# Brain/background threshold, %
set fmri(brain_thresh) 10

# Critical z for design efficiency calculation
set fmri(critical_z) 5.3

# Noise level
set fmri(noise) 0.66

# Noise AR(1)
set fmri(noisear) 0.34

# Motion correction
# 0 : None
# 1 : MCFLIRT
set fmri(mc) {1 if motion_correction != "None" else 0}

# Spin-history (currently obsolete)
set fmri(sh_yn) 0

# B0 fieldmap unwarping?
set fmri(regunwarp_yn) {1 if b0_unwarping else 0}

# GDC Test
set fmri(gdc) ""

# EPI dwell time (ms)
set fmri(dwell) 0.0

# EPI TE (ms)
set fmri(te) 0.0

# % Signal loss threshold
set fmri(signallossthresh) 10

# Unwarp direction
set fmri(unwarp_dir) y-

# Slice timing correction
# 0 : None
# 1 : Regular up (0, 1, 2, 3, ...)
# 2 : Regular down
# 3 : Use slice order file
# 4 : Use slice timings file
# 5 : Interleaved (0, 2, 4 ... 1, 3, 5 ... )
set fmri(st) {1 if slice_timing_correction != "None" else 0}

# Slice timings file
set fmri(st_file) ""

# BET brain extraction
set fmri(bet_yn) {1 if brain_extraction else 0}

# Spatial smoothing FWHM (mm)
set fmri(smooth) {spatial_smoothing}

# Intensity normalization
set fmri(norm_yn) {1 if intensity_normalization else 0}

# Perfusion subtraction
set fmri(perfsub_yn) {1 if perfusion_subtraction else 0}

# Highpass temporal filtering
set fmri(temphp_yn) {1 if highpass else 0}

# Lowpass temporal filtering
set fmri(templp_yn) 0

# MELODIC ICA data exploration
set fmri(melodic_yn) {1 if melodica_ICA else 0}

# Carry out main stats?
set fmri(stats_yn) 1

# Carry out prewhitening?
set fmri(prewhiten_yn) {1 if film_prewhitening else 0}

# Add motion parameters to model
# 0 : No
# 1 : Yes
set fmri(motionevs) 0
set fmri(motionevsbeta) ""
set fmri(scriptevsbeta) ""

# Robust outlier detection in FLAME?
set fmri(robust_yn) 0

# Higher-level modelling
# 3 : Fixed effects
# 0 : Mixed Effects: Simple OLS
# 2 : Mixed Effects: FLAME 1
# 1 : Mixed Effects: FLAME 1+2
set fmri(mixed_yn) 2

# Higher-level permutations
set fmri(randomisePermutations) 5000

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

# Add constant column to design matrix? (obsolete)
set fmri(constcol) 0

# Carry out post-stats steps?
set fmri(poststats_yn) 1

# Pre-threshold masking?
set fmri(threshmask) ""

# Thresholding
# 0 : None
# 1 : Uncorrected
# 2 : Voxel
# 3 : Cluster
set fmri(thresh) {thresholding}

# P threshold
set fmri(prob_thresh) {cluster_p}

# Z threshold
set fmri(z_thresh) {cluster_z}

# Z min/max for colour rendering
# 0 : Use actual Z min/max
# 1 : Use preset Z min/max
set fmri(zdisplay) 0

# Z min in colour rendering
set fmri(zmin) 2

# Z max in colour rendering
set fmri(zmax) 8

# Colour rendering type
# 0 : Solid blobs
# 1 : Transparent blobs
set fmri(rendertype) 1

# Background image for higher-level stats overlays
# 1 : Mean highres
# 2 : First highres
# 3 : Mean functional
# 4 : First functional
# 5 : Standard space template
set fmri(bgimage) 1

# Create time series plots
set fmri(tsplot_yn) 0

# Registration to initial structural
set fmri(reginitial_highres_yn) 0

# Search space for registration to initial structural
# 0   : No search
# 90  : Normal search
# 180 : Full search
set fmri(reginitial_highres_search) 90

# Degrees of Freedom for registration to initial structural
set fmri(reginitial_highres_dof) 3

# Registration to main structural
set fmri(reghighres_yn) 0

# Search space for registration to main structural
# 0   : No search
# 90  : Normal search
# 180 : Full search
set fmri(reghighres_search) 90

# Degrees of Freedom for registration to main structural
set fmri(reghighres_dof) BBR

# Registration to standard image?
set fmri(regstandard_yn) 1

# Use alternate reference images?
set fmri(alternateReference_yn) 0

# Standard image
set fmri(regstandard) "/usr/local/fsl/data/standard/MNI152_T1_2mm_brain"

# Search space for registration to standard space
# 0   : No search
# 90  : Normal search
# 180 : Full search
set fmri(regstandard_search) 180

# Degrees of Freedom for registration to standard space
set fmri(regstandard_dof) 12

# Do nonlinear registration from structural to standard space?
set fmri(regstandard_nonlinear_yn) 0

# Control nonlinear warp field resolution
set fmri(regstandard_nonlinear_warpres) 10

# High pass filter cutoff
set fmri(paradigm_hp) {high_pass_filter}

# Total voxels
set fmri(totalVoxels) {utilities.voxels_from_nifti}

# Number of lower-level copes feeding into higher-level analysis
set fmri(ncopeinputs) 0

# 4D AVW data or FEAT directory (1)
set feat_files(1) "{input_file}"

# Add confound EVs text file
set fmri(confoundevs) 1

# Confound EVs text file for analysis 1
set confoundev_files(1) "{confound_file}"

    """

    # Adding EVs
    for i, (ev_file, ev_name) in enumerate(zip(ev_files, ev_names), start=1):
        fsf_content += f"""
# EV {i} title
set fmri(evtitle{i}) "{ev_name}"

# Basic waveform shape (EV {i})
# 0 : Square
# 1 : Sinusoid
# 2 : Custom (1 entry per volume)
# 3 : Custom (3 column format)
# 4 : Interaction
# 10 : Empty (all zeros)
set fmri(shape{i}) 3

# Convolution (EV {i})
# 0 : None
# 1 : Gaussian
# 2 : Gamma
# 3 : Double-Gamma HRF
# 4 : Gamma basis functions
# 5 : Sine basis functions
# 6 : FIR basis functions
# 8 : Alternate Double-Gamma
set fmri(convolve{i}) 3

# Convolve phase (EV {i})
set fmri(convolve_phase{i}) 0

# Apply temporal filtering (EV {i})
set fmri(tempfilt_yn{i}) 1

# Add temporal derivative (EV {i})
set fmri(deriv_yn{i}) 1

# Custom EV file (EV {i})
set fmri(custom{i}) "{ev_file}"
        """

###################################################
# NOTE: FIND A WAY TO ADD ORTHOGONALIZATION HERE
# # Orthogonalise EV {i} wrt EV {x}
# set fmri(ortho{i}.{x}) 0
##################################################
    
    # Adding contrasts
    fsf_content += f"""
# Contrast & F-tests mode
# real : control real EVs
# orig : control original EVs
set fmri(con_mode_old) orig
set fmri(con_mode) orig

        """
    
    for j, (contrast_name, contrast_values) in enumerate(contrasts.items(), start=1):
        fsf_content += f"""
# Display images for contrast_real {j}
set fmri(conpic_real.{j}) 1

# Title for contrast_real {j}
set fmri(conname_real.{j}) "{contrast_name}"
        """

        for k, value in enumerate(contrast_values, start=1):
            fsf_content += f"set fmri(con_real{j}.{k}) {value}\n"

    fsf_content += f"""
##########################################################
# Now options that don't appear in the GUI

# Alternative (to BETting) mask image
set fmri(alternative_mask) ""

# Initial structural space registration initialisation transform
set fmri(init_initial_highres) ""

# Structural space registration initialisation transform
set fmri(init_highres) ""

# Standard space registration initialisation transform
set fmri(init_standard) ""

# For full FEAT analysis: overwrite existing .feat output dir?
set fmri(overwrite_yn) 0
        """

    with open(fsf_dir + "/design.fsf", "w") as file:
        file.write(fsf_content)
    
    # Print if successfully completed
    print("FSF file generated successfully.")