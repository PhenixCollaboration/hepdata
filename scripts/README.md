# HEPData helper scripts

A folder to keep various scripts facilitating submissions to the HEPData site

makethumbnails.pl is a perl script which will copy every png in a directory to thumb_FILENAME.png.  Thumbnail images must begin with "thumb_" so this script helps just copy existing files to what HEPData looks for.

Use this command while in the same directory as your .png files that you would like this to affect:
`perl makethumbnails.pl`

## formatter.py
is a python script that reads HEPfiles and formats their numbers according to the PDG guidelines. https://pdg.lbl.gov/2011/reviews/rpp2011-rev-rpp-intro.pdf (5.3 on page 13)

### Preparation


<details>
<summary>Outdated instructions. They are preserved in this dropdown in case anybody would like to see them</summary>
<br>
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

</details>
<br />

See the examples files, example.txt and examples_bins.txt to see how to prepare your text files before running the script on them. Some operating systems might have an encoding that messes with how the .txt files are read. The outdated instructions in the dropdown above might help.

One important note is that the header (first line) is **required**. Make sure that the column titles are separated by whitespace, but make sure there is no whitespace in the column title.

For example: y value -> y_value

### Instructions
See the preparation section before running the script.

For help in the terminal run: `python3 formatter.py -h`


<details>
<summary>View output from python3 formatter.py -h</summary>
<br>

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

</details>
<br />

To format a file run either: `python3 formatter.py hasXbins NumErrors inFileName outFileName`
or: `python3 formatter.py -a inFileName outFileName` 


### Running the example files
We have two .txt files in this repository for you to try as example. 
Notice:
- Our titles in the header in the first line are whitespace delimited. 
- example_bins.txt has bins while example.txt does not. We can use -a **only** when our data has bins

To run:
##### example.txt
`python3 formatter.py 0 4 example.txt formatted_example.txt`
##### example_bins.txt
`python3 formatter.py -a example_bins.txt formatted_example_bins.txt`


