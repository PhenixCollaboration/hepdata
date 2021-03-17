""""
This is a little program to edit .txt files to match the PDG format for error
Version 2.1 (this version includes more exceptions)
Author: Joseph Dominicus Lap
"""


#from matplotlib import pyplot as plt
import math
import numpy as np
import sys
from decimal import *


#If your Nch.txt file is somewhere else
working_dir='.'
#Put the name of the Nch.txt file here
file_name='PbScPi60To80.txt'

#We load the file as strings to avoid float arithmetic and loss of 0's 
try:
    data=np.loadtxt(working_dir+file_name,dtype=str)
except:
    print("Something is wrong with the chosen Nch.txt file")

#Initialization - This array will be written to a text file
output_data=[]

#We check for non-numeric content in any of the rows of the first column
try:
    [int(x[0]) for x in data]
except:
    print("Your headers must be commented out")
    sys.exit()

#Apparently the [int(i) for i in foobar] syntax doesn't work if there's only one row so here's an ugly work around
#This is based on the current formatting
#If formatting changes check the columns
if(isinstance(data[0],np.ndarray)):
    sqrts = [x[0] for x in data]
    sqrts1 = [x[1] for x in data]
    Nch = [x[2] for x in data]
    statE = [x[3] for x in data]
    sysSymErr = [x[4] for x in data]
    sysSymErr1 = [x[5] for x in data]
elif(len(data)==6):
    sqrts=[data[0]]
    sqrts1=[data[1]]
    Nch=[data[2]]
    statE=[data[3]]
    sysSymErr = [data[4]]
    sysSymErr1 = [data[5]]
else:
    print("Something is wrong with your data formatting")
    sys.exit()

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

#Goes line by line formatting the errors
for i in range(len(sqrts)):
    er1,var1,dig1=ERR_Format(statE[i])
    er2,var2,dig2=ERR_Format(sysSymErr[i])
    er3,var3,dig3=ERR_Format(sysSymErr1[i])
    dig=0
    var=0
    line=[]

    #Which of the three is smaller
    if(er1<=er2): # and er1<=er3):
        dig=dig1
        var=var1
    elif(er2<=er1): # and er2<=er3):
        dig=dig2
        var=var2
    elif(er3<=er1): # and er2<=er3):
        dig=dig3
        var=var3
    #Copies over the sqrts as was
    line.append(sqrts[i])
    line.append(sqrts1[i])
    #Rounds the Nch to match the smallest error
    rounded_number=my_round(Nch[i],var,dig)
    line.append(rounded_number)
    #Fills the output vectors with the appropriate errors
    line.append(er1)
    line.append(er2)
    line.append(er3)
    output_data.append(line)
    
#Just in case something prevents saving
try:
    np.savetxt(working_dir+'Nch_formatted.txt',output_data,fmt='%s',header='sqrts   Nch   statE  sysSymErr')
except:
    print('Something is wrong with your permissions or there is not enough storage for the new Nch.txt file')








