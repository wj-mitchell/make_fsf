generate_fsf <- function(input_file, output_dir, tr, highpass, confound_file, ev_files, ev_names, contrasts) {
  if (length(ev_files) != length(ev_names)) {
    stop("The number of EV files must be equal to the number of EV names.")
  }
  
  n_evs <- length(ev_files)
  n_contrasts <- length(contrasts)
  
  fsf_content <- paste0(
    "# FEAT version number\n",
    "set fmri(version) 6.00\n\n",
    "# Are we in MELODIC?\n",
    "set fmri(inmelodic) 0\n\n",
    "# Analysis level\n",
    "# 1 : First-level analysis\n",
    "# 2 : Higher-level analysis\n",
    "set fmri(level) 1\n\n",
    "# Which stages to run\n",
    "# 0 : No first-level analysis (registration and/or group stats only)\n",
    "# 7 : Full first-level analysis\n",
    "set fmri(analysis) 7\n\n",
    "# Use relative filenames\n",
    "set fmri(relative_yn) 0\n\n",
    "# TR(s)\n",
    "set fmri(tr) ", tr, "\n\n",
    "# Total volumes\n",
    "set fmri(npts) 0\n\n",
    "# Delete volumes\n",
    "set fmri(ndelete) 0\n\n",
    "# Perfusion tag/control order\n",
    "set fmri(tagfirst) 1\n\n",
    "# Number of first-level designs\n",
    "set fmri(multilev_yn) 0\n\n",
    "# Number of EVs\n",
    "set fmri(evs_orig) ", n_evs, "\n",
    "set fmri(evs_real) ", n_evs, "\n",
    "set fmri(evs_vox) 0\n\n",
    "# Number of contrasts\n",
    "set fmri(ncon_orig) ", n_contrasts, "\n",
    "set fmri(ncon_real) ", n_contrasts, "\n\n",
    "# Number of F-tests\n",
    "set fmri(nftests_orig) 0\n",
    "set fmri(nftests_real) 0\n\n",
    "# Number of parametric EVs\n",
    "set fmri(parevs) 0\n\n",
    "# Number of time points\n",
    "set fmri(npts) 0\n\n",
    "# Add temporal derivatives\n",
    "set fmri(temphp_yn) 1\n\n",
    "# Highpass temporal filtering\n",
    "set fmri(paradigm_hp) ", highpass, "\n\n",
    "# Motion correction\n",
    "set fmri(realign) 1\n\n",
    "# BET brain extraction\n",
    "set fmri(bet_yn) 1\n\n",
    "# Spatial smoothing FWHM (mm)\n",
    "set fmri(smooth) 5.0\n\n",
    "# Intensity normalization\n",
    "set fmri(norm_yn) 1\n\n",
    "# Z-transformation\n",
    "set fmri(zg) 0\n\n",
    "# Perfusion subtraction\n",
    "set fmri(perfsub) 0\n\n",
    "# Perfusion subtraction T1\n",
    "set fmri(perfsubthresh) 0\n\n",
    "# Confound EVs text file\n",
    "set fmri(confoundevs) 1\n",
    "set confoundev_files(1) \"", confound_file, "\"\n\n",
    "# Add motion parameters to model\n",
    "set fmri(motionevs) 0\n",
    "set fmri(motionevsbeta) \"\"\n\n",
    "# Slice timing correction\n",
    "set fmri(st) 1\n\n",
    "# Slice timing correction method\n",
    "set fmri(st_yn) 0\n\n",
    "# Alternative reference slice (0 means bottom)\n",
    "set fmri(st_refslice) 0\n\n",
    "# Bias field correction\n",
    "set fmri(bias_yn) 1\n\n",
    "# Thresholding\n",
    "set fmri(thresh) 1000\n\n",
    "# First-level analysis output directory\n",
    "set fmri(outputdir) \"", output_dir, "\"\n\n",
    "# Input filename\n",
    "set feat_files(1) \"", input_file, "\"\n"
  )
  
  # Adding EVs
  for (i in seq_along(ev_files)) {
    fsf_content <- paste0(fsf_content,
      "\n# EV ", i, " - ", ev_names[i], "\n",
      "set fmri(evtitle", i, ") \"", ev_names[i], "\"\n",
      "set fmri(shape", i, ") 3\n",
      "set fmri(convolve", i, ") 3\n",
      "set fmri(convolve_phase", i, ") 0\n",
      "set fmri(tempfilt_yn", i, ") 1\n",
      "set fmri(deriv_yn", i, ") 1\n",
      "set fmri(custom", i, ") \"", ev_files[i], "\"\n"
    )
  }
  
  # Adding contrasts
  fsf_content <- paste0(fsf_content, "\n# Contrast & F-tests mode\nset fmri(con_mode_old) 0\nset fmri(con_mode) 1\n")
  
  j <- 1
  for (contrast_name in names(contrasts)) {
    fsf_content <- paste0(fsf_content,
      "\n# Contrast ", j, " - ", contrast_name, "\n",
      "set fmri(conpic_real.", j, ") 1\n",
      "set fmri(conname_real.", j, ") \"", contrast_name, "\"\n"
    )
    for (k in seq_along(contrasts[[contrast_name]])) {
      fsf_content <- paste0(fsf_content, "set fmri(con_real", j, ".", k, ") ", contrasts[[contrast_name]][k], "\n")
    }
    j <- j + 1
  }
  
  fsf_content <- paste0(fsf_content, "\n# Now run FEAT\nset fmri(overwrite_yn) 1\n")
  
  writeLines(fsf_content, con = file.path(output_dir, "design.fsf"))
  
  message("FSF file generated successfully.")
}

# Example usage
generate_fsf(
  input_file = "path/to/your/input_file.nii.gz",
  output_dir = "path/to/your/output_directory",
  tr = 2.0,
  highpass = 100,
  confound_file = "path/to/your/confound_file.txt",
  ev_files = c("path/to/your/ev1.txt", "path/to/your/ev2.txt", "path/to/your/ev3.txt"),
  ev_names = c("EV1", "EV2", "EV3"),
  contrasts = list(
    "Contrast 1" = c(1, 0, 0),
    "Contrast 2" = c(0, 1, 0),
    "Contrast 3" = c(0, 0, 1)
  )
)
