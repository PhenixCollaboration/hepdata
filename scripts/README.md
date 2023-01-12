# HEPData helper scripts

A folder to keep various scripts facilitating submissions to the HEPData site

makethumbnails.pl is a perl script which will copy every png in a directory to thumb_FILENAME.png.  Thumbnail images must begin with "thumb_" so this script helps just copy existing files to what HEPData looks for.

## formatter.py 
is a python script that reads HEPfiles and formats their numbers according to the PDG guidelines.

### Preparation

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

### Intstructions
See the preparation section before running the script.

For help in the terminal run: `python3 formatter.py -h`

Which will print:

    HepMC Formatter!
        
    Thanks for using it!
    Your HepMC file should be in a standard format
    [leftBin, rightBin, Observable, errors...]
    [centralValues, Observable, errors...]
    The header should not be commented out! The program uses it to fill in the header for the output file.
        
    syntax: 
    python3 formatter.py hasXbins NumErrors inFileName outFileName

    bool hasXbins: Set to 1 if there are two X columns corresponding to left and right bins and 0 if there is one column of central values
    int NumErrors: After the observable, the number of error columns
    string inFileName: The name of the file to be formatted
    string outFileName: The name of the output file    
    
    syntax: 
    python3 formatter.py -a inFileName outFileName

    -a: Will try to infer number of x columns and errors
    string inFileName: The name of the file to be formatted
    string outFileName: The name of the output file        
    Once in the program it will read your file and attempt to read the header.
    If it is obviously mismatched with the data, we will let you know and ask if you want to abort the formatting to go edit the file.  
    If you choose to go forward with formatting, then we will ask if you know the observable name.
    This is all assuming that the files will always have x_low and x_high by default(as opposed to just x, or x_central). 

To format a file run either: `python3 formatter.py hasXbins NumErrors inFileName outFileName`

or: `python3 formatter.py -a inFileName outFileName` 

as described above. I recommend using the automatic mode `-a`


