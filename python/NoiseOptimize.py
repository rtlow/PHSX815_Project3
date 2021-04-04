#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy.special as special


#setting matplotlib ticksize
matplotlib.rc('xtick', labelsize=14) 
matplotlib.rc('ytick', labelsize=14) 

#set matplotlib global font size
matplotlib.rcParams['font.size']=14


# main function for our CookieAnalysis Python code
if __name__ == "__main__":
   
    haveInput = False
    InputFile = None

    # reading in the cmd args
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            continue

        # seeing if we have input files
        if sys.argv[i] == '--input':
            InputFile[0] = sys.argv[i+1]
            haveInput[0] = True

    
    if '-h' in sys.argv or '--help' in sys.argv or not np.all(haveInput):
        print ("Usage: %s [options] --input [input data]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print ("   -alpha [number]     significance of test")
        print
        sys.exit(1)
    
    # reading in data from files
    counts = np.loadtxt(InputFile)

    LL = []
    Nmeas = 0
    
    #TODO implement calculating LL and optimization
    

    
    sys.exit(1)

