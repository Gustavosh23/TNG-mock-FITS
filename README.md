# TNG-mock-FITS
This python program adapts hdf5 snapshots IllustrisTNG galaxies, creating the plot of realistic visualizations that take into account metallicity and age of particles in the simulated subhalo. We've added a snippet to the source code of a function in the pynbody library to save contributions from each band filter in FITS format.
Basically your IllustrisTNG hdf5 file must have 'GFM_Metallicity' and 'GFM_StellarFormationTime' values in the PartType4 group that will be considered in the plotting.

Some explanation of use:

1- This program is an adaptation of the galmock code shared earlier (https://github.com/Gustavosh23/galmock).
2- The param.ini file has some control options like plotting specifications, rotation of the displayed galaxy etc.
3- For the function to be able to create FITS files you'll need to make a small addition to your python source code. See the field, "pynbody code change" below.

# Pynbody source code change
Once you have the library installed on your computer you will need to edit the file named stars.py. The path where this file can be found should look something like this:

/anaconda3/lib/python3.9/site-packages/pynbody/plot/stars.py

The snippet code is very short and is available in the snippet_TNGmockFIT.txt file. It should be placed on line 252 of the stars.py file, respecting the indentation of the original code. 

# Required libraries
* astropy
* numpy (python-numpy)
* h5py
* pynbody
* matplotlib

# Usage
 usage: python3 TNGmockFITS.py [snapshot.hdf5] [param.ini]
