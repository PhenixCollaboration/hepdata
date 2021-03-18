# HEPData helper scripts

A folder to keep various scripts facilitating submissions to the HEPData site

makethumbnails.pl is a perl script which will copy every png in a directory to thumb_FILENAME.png.  Thumbnail images must begin with "thumb_" so this script helps just copy existing files to what HEPData looks for.

formatter.py is a python script that reads HEPfiles and formats their numbers according to the PDG guidelines.

The HEPfiles seem to come in docx form, but txt is the expected format. The first thing to do is run (making sure you have libreoffice installed)

`libreoffice --headless --convert-to "txt:Text (encoded):UTF8" *.docx`

in the folder containing the files.

You should also format all headers so that there is NO WHITESPACE in individual header names:

Prime offenders:

y value -> y-value

x low -> x-low

x high -> x-high

sys, uncor -> sys,uncor

sys, cor -> sys,cor

sys, stat -> sys,stat

The sufficiently equipped user can try to do a replace all over many files, but do not be surprised if you find other cases of whitespace that are not here.
