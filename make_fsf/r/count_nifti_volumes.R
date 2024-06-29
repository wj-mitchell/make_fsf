# Install the oro.nifti package if not already installed
# install.packages("oro.nifti")

library(oro.nifti)

count_nifti_volumes <- function(nifti_file) {
  tryCatch({
    nii <- readNIfTI(nifti_file)
    num_volumes <- dim(nii$data)[4]  # Assuming 4th dimension represents time points
    return(num_volumes)
  }, error = function(e) {
    message(paste("Error loading or processing", nifti_file, ":", e))
    return(NULL)
  })
}

# Example usage:
nifti_file <- "your_nifti_file.nii.gz"
num_volumes <- count_nifti_volumes(nifti_file)
if (!is.null(num_volumes)) {
  cat(paste("Number of volumes in", nifti_file, ":", num_volumes, "\n"))
}