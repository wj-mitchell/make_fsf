import nibabel as nib
import os

# ----- check_directory_exists
def check_directory_exists(file_path):
    if not os.path.isdir(file_path):
        raise FileNotFoundError(f"The directory or file {file_path} does not exist.")

# ----- vols_from_nifti -----
def vols_from_nifti(input_file):
    """
    Reads the number of volumes from a NIfTI file.

    Parameters:
    input_file (str): The path to the .nii.gz file.

    Returns:
    float: The number of volumes within the .nii.gz file, or None if not found.
    """
    check_directory_exists(input_file)
    
    try:
        nifti = nib.load(input_file)
        data = nifti.get_fdata()
        num_volumes = data.shape[-1]  # Assuming last dimension represents time points
        return num_volumes
    
    except Exception as e:
        print(f"Error loading or processing {input_file}: {e}")
        return None

# ----- tr_from_nifti -----
def tr_from_nifti(input_file):
    """
    Reads the repetition time (TR) from a NIfTI file.

    Parameters:
    input_file (str): The path to the .nii.gz file.

    Returns:
    float: The repetition time (TR) in seconds, or None if not found.
    """   
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"The input file {input_file} does not exist.")
  
    try:
        # Load the NIfTI file
        img = nib.load(input_file)
        
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
    
# ----- voxels_from_nifti -----
def voxels_from_nifti(input_file):
    """
    Reads the number of voxels contained within a NIfTI file.

    Parameters:
    input_file (str): The path to the .nii.gz file.

    Returns:
    float: The number of voxels contained, or None if not found.
    """   
    try:
        nifti = nib.load(input_file)
        data = nifti.get_fdata()
        num_voxels = data.size  # Total number of elements in the data array
        return num_voxels
    except Exception as e:
        print(f"Error loading or processing {input_file}: {e}")
        return None
