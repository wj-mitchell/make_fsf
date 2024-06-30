import utilities

# ----- lowlvl_fsf -----
def lowlvl_fsf(input_file, 
               output_dir, 
               tr, 
               highpass, 
               confound_file, 
               ev_files, 
               ev_names, 
               contrasts):
    


    total_volumes = 0,
                       delete_volumes = 0,
                       TR = 3,
                       high_pass_filter = 100,
                       alternative_reference,
                       motion_correction = c("None", "MCFLIRT"),
                       b0_unwarping = FALSE,
                       slide_timing_correction = c("None", "Regular Up", "Regular Down",
                                                   "Interleaved", "Use Slice Order File",
                                                   "Use Slice Timing File"),
                       brain_extraction = FALSE,
                       spatial_smoothing = 5,
                       intensity_normalization = FALSE,
                       perfusion_subtraction = FALSE,
                       highpass = FALSE,
                       melodica_ICA = FALSE,
                       registration_reference = "/usr/local/fsl/data/standard/MNI152_T1_mm_brain",
                       linear_search = c("None", "Normal", "Full"),
                       dof = c("3 DOF", "6 DOF", "7 DOF",
                               "9 DOF", "12 DOF"),
                       film_prewhitening = TRUE,
                       confound_file,
                       thresholding = c("None", "Cluster"),
                       cluster_z = 3.29,
                       cluster_p = 0.001,
                       timeseries_plot = False
    """
    Generates a first level .fsf file.

    Parameters:
    file_path (str): The path to the .nii.gz file.

    Returns:

    
    Example:
    lowlvl_fsf(
        input_file="path/to/your/input_file.nii.gz",
        output_dir="path/to/your/output_directory",
        tr=2.0,
        highpass=100,
        confound_file="path/to/your/confound_file.txt",
        ev_files=["path/to/your/ev1.txt", "path/to/your/ev2.txt", "path/to/your/ev3.txt"],
        ev_names=["EV1", "EV2", "EV3"],
        contrasts={
            "Contrast 1": [1, 0, 0],
            "Contrast 2": [0, 1, 0],
            "Contrast 3": [0, 0, 1]
        }
    )
    
    """
    if len(ev_files) != len(ev_names):
        raise ValueError("The number of EV files must be equal to the number of EV names.")

    n_evs = len(ev_files)
    n_contrasts = len(contrasts)
    
    if tr is None:
        tr = tr_from_nifti(input_file)
    
    if volumes is None:
        volumes 

    fsf_content = f"""
# FEAT version number
set fmri(version) 6.00

# Are we in MELODIC?
set fmri(inmelodic) 0

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
set fmri(npts) 0

# Delete volumes
set fmri(ndelete) 0

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
set fmri(npts) 0

# Add temporal derivatives
set fmri(temphp_yn) 1

# Highpass temporal filtering
set fmri(paradigm_hp) {highpass}

# Motion correction
set fmri(realign) 1

# BET brain extraction
set fmri(bet_yn) 1

# Spatial smoothing FWHM (mm)
set fmri(smooth) 5.0

# Intensity normalization
set fmri(norm_yn) 1

# Z-transformation
set fmri(zg) 0

# Perfusion subtraction
set fmri(perfsub) 0

# Perfusion subtraction T1
set fmri(perfsubthresh) 0

# Confound EVs text file
set fmri(confoundevs) 1
set confoundev_files(1) "{confound_file}"

# Add motion parameters to model
set fmri(motionevs) 0
set fmri(motionevsbeta) ""

# Slice timing correction
set fmri(st) 1

# Slice timing correction method
set fmri(st_yn) 0

# Alternative reference slice (0 means bottom)
set fmri(st_refslice) 0

# Bias field correction
set fmri(bias_yn) 1

# Thresholding
set fmri(thresh) 1000

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
    
    with open(output_dir + "/design.fsf", "w") as file:
        file.write(fsf_content)
    
    print("FSF file generated successfully.")

