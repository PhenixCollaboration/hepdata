"""
This is a little program to edit .txt files to match the PDG format for error
Version 2.1 (this version includes more exceptions)
Author: Joseph Dominicus Lap

An extended version that is a bit more user-friendly. Includes both manual and auto mode, but it is a very limited auto mode. 
Version 3.1
Author: Patrick John Steffanic

A modified version that fixes issues handling asymmetric errors. Negative values are now allowed in errors. 0 errors are also permitted, but the program displays a message for users to double check their data. Prints the y value associated the 0 error with 4 significant figures. Modifications were made in lines 104-118 and 245-259.
Version 3.2
Author: Joesph Duane Beller

YAMVF (Yet another modified version of formatter.py) that implements handling precision for multiple errors that are not added together in quadrature. This code will find each of the smallest errors per line j, and round all numbers in that line according to the precision of the smallest error.
Version 3.3
Author: Joesph Duane Beller
"""



from matplotlib import pyplot as plt
import math
import numpy as np
import sys
from decimal import *

from numpy.testing._private.utils import KnownFailureTest

from distutils.util import strtobool

#A script to round correctly. Python default uses IEEE754 standard which rounds to even numbers.
def my_round(n, var,dig):
    #This gives us our precision
    ndigits=var-dig
    part = Decimal(n) * Decimal(10 ** ndigits)
    delta = part - int(part)
    # always round "away from 0"
    if delta >= 0.5 or -0.5 < delta <= 0:
        part = math.ceil(part)
    else:
        part = math.floor(part)

    #Here we avoid the scientific notation for now
    if(abs(float(n)) >= 1e-4):
        output=str(part / 10 ** ndigits)
    else:
        output=str('{:f}'.format(Decimal(part) / Decimal(10 ** ndigits)))


    #Here we make sure we don't get rid of trailing zeroes
    if(abs(float(n))<1e+1 and dig>=2 and len(output.replace('-', ""))!=dig):
        print('This should not occur. Something is wrong')
        print(f'Here is the output {output}')
        #sys.exit()

    #Count number of additional digits for output >= 10
    adig = 0
    if(abs(float(output)) >= 1e+1):
        adig = int(np.log10(abs(float(output))))

    while(dig<2 and len(output.replace("-",""))<var-dig+2+adig):
            if('.' in output):
                output+='0'
            else:
                output+='.0'

    #Here we make sure to get rid of unecessary trailing zeroes
    if(dig==1 and var==1):
        output=output.replace('.0','')
    if(dig>=2 and len(output.replace('-', ""))!=dig):
        output=output.replace('.0','')
        #print('This should not occur. Something is wrong')
        #print(f'Here is the output {output}')
        #sys.exit()

    #Here now we consider the scientific notation
    #First : zero value
    if(float(output) == 0.):
        if ((dig-1) >= -3):
            return output
        if(var==1):
            output = '0' + 'e' + str(dig-1)
        elif(var==2):
            output = '0.0' + 'e' + str(dig-1)
        return output

    #Second : non-zero value
    if(dig<2 and abs(float(output)) < 1e-3):
        output='{:10e}'.format(float(output))
        output=output.replace('e-0', 'e-')
        factor=output.split('e')[0]
        exp=output.split('e')[1]

        while(dig<2 and (int(len(factor.replace('-','').replace('.','')))+abs(int(exp))) >= var-dig+2):
            factor=factor[:-1]
            if(factor[-1:]=='.'):
                factor=factor[:-1]

        output_exp = factor + 'e' + exp
        return output_exp

    output=output.replace('E', 'e')
    return output

#A little script to follow PDG guidelines on error
def ERR_Format(err):
    #How many digits is our error?

    ###This first if statement makes sure a 0 value is not entered. This modification was added by Joesph Beller
    
    errcheck = float(err) #Converting our err into a float to verify if it is == 0
    
    if(errcheck != 0):  #Checks if err is zero
        digits=int(np.floor(np.log10(np.abs(Decimal(err))))+1)  ##Definition of digits since version 2.1
    else:
        var, digits = [1,-2] #Avoid an error in the following if statements
        error_is_0 = 1  #Flag to print at end; this is still in development

    ###Modification ended
    
    
    #What are the first 3 digits of our error?
    #We've removed the annoying edge case of  having a '.' as a digit
    if (digits<3):
        rounding=int((10**(3-digits))*Decimal(err))

    else:
        rounding=int(float(err))

    #Here we check the first 3 digits and decide
    if (rounding <355):
        #2 significant figures
        var=2
    elif(rounding<949):
        # 1 significant figure
        var=1
    else:
        # round the error up, but keep 2 sigfig on the value
        var=1
    #Here we round the error to the specified amount
    #%g takes off trailing 0's

    realerr=my_round(err,var,digits)
    
    return realerr,var,digits

def do_formatting(data, X_bins, N_errs):
    output_data=[]

    for j in range(len(data)):  #runs through this code for j# of vertical lines of data
        line = []

        if(X_bins): #if true
            line.append(data[j,0]) #Append the left bin
            line.append(data[j,1]) #Append the right bin
        else:
            line.append(data[j,0]) #Append the central value
            
        
        #Modifications for Version 3.3 begin here:
        # Find the smallest error for each line of j
        min_error = min(map(float,([np.array(list(map(ERR_Format, data[:, -i])))[:,0][j] for i in range(N_errs,0,-1)])))
        # Find the var and dig associated with the min_error
        error_fmtd, var, dig = ERR_Format(min_error)
        
        # The code below was from Version 2.1 ==============================================================================
        #errors_fmtd = [np.array(list(map(ERR_Format, data[:, -i])))[:,0][j] for i in range(N_errs,0,-1)] #Get the errors
        #var = [np.array(list(map(ERR_Format, data[:, -i])))[:,1][j] for i in range(N_errs,0,-1)]
        #dig = [np.array(list(map(ERR_Format, data[:, -i])))[:,2][j] for i in range(N_errs,0,-1)]
        #min_index = np.argmin(list(map(float,errors_fmtd))) #find the index of the smallest error
        # ==================================================================================================================
        
        
        if(X_bins):
            rounded_number=my_round(data[j,2],Decimal(var),Decimal(dig))
        else:
            rounded_number=my_round(data[j,1],Decimal(var),Decimal(dig))
        line.append(rounded_number)

        #Fills the output vectors with the appropriate errors
        for i in range(N_errs,0,-1):
            err = my_round(data[j,-i],Decimal(var),Decimal(dig))
            #Modifications for Version 3.3 end here
            line.append(err)
        output_data.append(line)
    return output_data

def print_help():
    print('''
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
        ''')

def build_header(bad_header, first_line, X_bins, N_errs):
    xaxis = "X"
    errs = " ".join([f"err_{n}" for n in range(N_errs)])
    print(f"The header is not quite right. Go check and make sure that every column name contains no whitespace and that there are the correct number of them. Modify the original file until this works, or use manual mode. Using:\n {xaxis} [OBS] {errs}")
    print(f"Here is the header:  {bad_header}")
    print(f"And the first line: {first_line}")
    ab = input("Do you want to abort this formatting? ( y | n )")
    if ab == 'y':
        exit(0)
    rep_name = input("Would you like to input the observable name? ( y | n )")
    if rep_name=='y':
        obs_name = " "
        while ' ' in obs_name:
            if obs_name != " ":
                print("No spaces allowed!")
            obs_name = input("What is the observable name?")
        header_ = f"{xaxis} {obs_name} {errs}"
    else:
        header_ = f"{xaxis} [OBS] {errs}"
    return header_

if __name__=="__main__":
    
    
    if(sys.argv[1]=="-h"):
        print_help()

    elif sys.argv[1]=='-a':
        file_name=sys.argv[2]
        print(f"Opening file {file_name}")
        try:
            data=np.loadtxt(file_name,dtype=str)
            header_ = " ".join(data[0])
            data = data[1:]
            N_errs = len(data[0])-3
            X_bins = True
        except ValueError as e:
            print(e)
            data=np.loadtxt(file_name,dtype=str, skiprows=1)
            bad_header = np.loadtxt(file_name, dtype=str, max_rows=1)
            first_line = data[0]
            xaxis = "X"
            N_errs = len(data[0])-2
            X_bins = False
            header_ = build_header(bad_header, first_line, X_bins, N_errs)
            data = data[1:]
            
        
        output_data = do_formatting(data, X_bins, N_errs)
        
        
        #Just in case something prevents saving
        try:
            np.savetxt(sys.argv[3],output_data,fmt='%s',header=(header_))
        except Exception as e:
            print(e)
            print('Something is wrong with your permissions or there is not enough storage for the new Nch.txt file')
        
            
    else:
        N_errs = int(sys.argv[2])
        X_bins = strtobool(sys.argv[1])
        #Put the name of the Nch.txt file here
        file_name=sys.argv[3]
        #We load the file as strings to avoid float arithmetic and loss of 0's 
        try:
            data=np.loadtxt(file_name,dtype=str)
            header_ = " ".join(data[0])
            data = data[1:]
        except ValueError:
            data=np.loadtxt(file_name,dtype=str, skiprows=1)
            bad_header = np.loadtxt(file_name, dtype=str, max_rows=1)
            first_line = data[0]
            header_ = build_header(bad_header, first_line, X_bins, N_errs)
            data = data[1:]

        output_data = do_formatting(data, X_bins, N_errs)

        #Just in case something prevents saving
        try:
            np.savetxt(sys.argv[4],output_data,fmt='%s',header=(header_))
        except:
            print('Something is wrong with your permissions or there is not enough storage for the new Nch.txt file')
        

