""""
This is a little program to edit .txt files to match the PDG format for error
Version 2.1 (this version includes more exceptions)
Author: Joseph Dominicus Lap
"""



from matplotlib import pyplot as plt
import math
import numpy as np
import sys
from decimal import *

#A script to round correctly. Python default uses IEEE754 standard which rounds to even numbers.
def my_round(n, var,dig):
    #This gives us our precision
    ndigits=var-dig
    part = Decimal(n) * 10 ** ndigits
    delta = part - int(part)
    # always round "away from 0"
    if delta >= 0.5 or -0.5 < delta <= 0:
        part = math.ceil(part)
    else:
        part = math.floor(part)

    output=str(part / (10 ** ndigits))

    #Here we make sure we don't get rid of trailing zeroes
    if(dig>=2 and len(output)!=dig):
        print('This should not occur. Something is wrong')
        sys.exit()

    elif(dig<2 and len(output)!=var-dig+2):
        output+='0'
    return output

#A little script to follow PDG guidelines on error
def ERR_Format(err):
    #How many digits is our error?
    digits=int(np.floor(np.log10(Decimal(err)))+1)


    #What are the first 3 digits of our error?
    #We've removed the annoying edge case of  having a '.' as a digit
    if (digits<3):
        rounding=int((10**(3-digits))*Decimal(err))

    else:
        rounding=int(err[:3])

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


if __name__=="__main__":

    if(sys.argv[1]=="-h"):
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
        ''')
    else:

        N_errs = int(sys.argv[2])
        X_bins = bool(sys.argv[1])

        #If your Nch.txt file is somewhere else
        working_dir=''
        #Put the name of the Nch.txt file here
        file_name=sys.argv[3]
        #We load the file as strings to avoid float arithmetic and loss of 0's 
        try:
            data=np.loadtxt(working_dir+file_name,dtype=str)
            header_ = data[0]
            data = data[1:]
        except:
            print("Something is wrong with the chosen Nch.txt file")


        #This array will be written to a text file
        output_data=[]

        for j in range(len(data)):
            line = []

            if(X_bins):
                line.append(data[j,0]) #Append the left bin
                line.append(data[j,1]) #Append the right bin
            else:
                line.append(data[j,0]) #Append the central value

            errors_fmtd = [np.array(list(map(ERR_Format, data[:, -i])))[:,0][j] for i in range(N_errs,0,-1)] #Get the errors
            var = [np.array(list(map(ERR_Format, data[:, -i])))[:,1][j] for i in range(N_errs,0,-1)] 
            dig = [np.array(list(map(ERR_Format, data[:, -i])))[:,2][j] for i in range(N_errs,0,-1)]
            
            min_index = np.argmin(list(map(float,errors_fmtd))) #find the index of the smallest error
            
            if(X_bins):
                rounded_number=my_round(data[j,2],Decimal(var[min_index]),Decimal(dig[min_index])) 
            else:
                rounded_number=my_round(data[j,1],Decimal(var[min_index]),Decimal(dig[min_index]))
            line.append(rounded_number)

            #Fills the output vectors with the appropriate errors
            for err in errors_fmtd:
                line.append(err)
            output_data.append(line)

        #Just in case something prevents saving
        try:
            np.savetxt(working_dir+sys.argv[4],output_data,fmt='%s',header=" ".join(header_))
        except:
            print('Something is wrong with your permissions or there is not enough storage for the new Nch.txt file')
        

