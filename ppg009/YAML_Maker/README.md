# YAML maker

YAML maker is a simple program that takes input from any type of file and outputs to a YAML file that is formatted specifically with particle physics in mind.

## Getting Started

YAML maker can be run in any Linux environment using the C++11 standard. A make file is included for simple compiling.

### Installing

The included makefile can be used on systems with make installed using the command.

```
make
```

## Using the program

The command for YAML maker is 

```
yaml_data debug filename
```
A debug of 1 will print all values and names to the terminal. Filename is the name of the data file to be read.

YAML maker can deal with many file types however each data file must be set up in the following fashion. Please note that each set of y values must end with the string *** including the last set.

```
X axis title:				String
Y count						Integer
Y axis tile #1:				String
....
Y axis title #N:			String
Y qualifiers #1:			String
....
Y qualifiers #N:			String
Is bin:						yes,no
X Stat error:				symmetric, asymmetric, none
X Sys error:				symmetric, asymmetric, none
Y error count				Integer
Y error title #1:			String
Y error type #1:			symmetric, asymmetric
....
Y error title #N:			String
Y error type #N:			symmetric, asymmetric
Data
X2 values /Y1 value / X1 Stat Error / X1 Sys Error / Y1 Error / ... / Y1N Error
***
X2 values /Y2 value / X2 Stat Error / X2 Sys Error / Y2 Error / ... / Y2N Error
***
Xn values /Yn value / Xn Stat Error / Xn Sys Error / YN Error / ... / YNN Error
***
```

Bin examples
No: Single value
Yes: Range e.g. 3-4

### Example of a file set up

```
Delta phi
1
C(Delta phi)
none
none
none
1
sys
symmetric
0.087266  1.794795  0.040905  
0.261799  1.118588  0.033984 
....
```

If all files are set up one command can be run to produce files for many inputs in a directory using the following command. This requires the program to be compiled and in the same directory.

```
find . -exec yaml_data debug {} \;
```

##Video instructions
For an detailed tutorial on how to format data for HEPData including details and examples of using YAML maker check out this video.
https://youtu.be/_hz6EVPeuW4

The channel also has great videos about QGP. Enjoy!

## Authors

* **Tom Krobatsch** - *Initial work* - [tkrobatsch]
(https://github.com/tkrobatsch)

* **Dr. Christine Nattrass** - *Initial work* - [cnattras]
(https://github.com/cnattras)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Dr. Christine Nattrass
christine.nattrass@utk.edu 
* PHYS493 group
* Christal Martin
cbaillar@vols.utk.edu 
