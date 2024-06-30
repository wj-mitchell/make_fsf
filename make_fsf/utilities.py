import nibabel as nib

# ----- vols_from_nifti -----
def vols_from_nifti(file_path):
    """
    Reads the number of volumes from a NIfTI file.

    Parameters:
    file_path (str): The path to the .nii.gz file.

    Returns:
    float: The number of volumes within the .nii.gz file, or None if not found.
    """
    try:
        nifti = nib.load(file_path)
        data = nifti.get_fdata()
        num_volumes = data.shape[-1]  # Assuming last dimension represents time points
        return num_volumes
    except Exception as e:
        print(f"Error loading or processing {file_path}: {e}")
        return None

# ----- tr_from_nifti -----
def tr_from_nifti(file_path):
    """
    Reads the repetition time (TR) from a NIfTI file.

    Parameters:
    file_path (str): The path to the .nii.gz file.

    Returns:
    float: The repetition time (TR) in seconds, or None if not found.
    """
    try:
        # Load the NIfTI file
        img = nib.load(file_path)
        
        # Get the header information
        header = img.header
        
        # Check if TR information is available in the header
        if 'pixdim' in header:
            # The TR is usually stored in the pixdim[4] element
            tr = header['pixdim'][4]
            
            # Return the TR value if it is greater than zero
            if tr > 0:
                return tr
            else:
                print("TR value is not greater than zero.")
                return None
        else:
            print("TR information not found in the header.")
            return None
    except Exception as e:
        print(f"An error occurred while reading the NIfTI file: {e}")
        return None
