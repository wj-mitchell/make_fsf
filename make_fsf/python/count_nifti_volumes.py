import nibabel as nib

def count_nifti_volumes(nifti_file):
    try:
        nifti = nib.load(nifti_file)
        data = nifti.get_fdata()
        num_volumes = data.shape[-1]  # Assuming last dimension represents time points
        return num_volumes
    except Exception as e:
        print(f"Error loading or processing {nifti_file}: {e}")
        return None

# Example usage:
nifti_file = 'your_nifti_file.nii.gz'
num_volumes = count_nifti_volumes(nifti_file)
if num_volumes is not None:
    print(f"Number of volumes in {nifti_file}: {num_volumes}")