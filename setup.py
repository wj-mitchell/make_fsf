# setup.py
from setuptools import setup, find_packages

setup(
    name='make_fsf',
    version='0.1.0',
    description="A convenient means of automating the generation of low and high level .fsf files for FSL's FEAT. An alternative to using the FEAT GUI or manually editing a pre-existing document.",
    author='William Mitchell',
    author_email='billy.mitchell@temple.edu',
    url='https://github.com/wj-mitchell/make_fsf',
    packages=find_packages(),
    install_requires=[
        nibabel
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)