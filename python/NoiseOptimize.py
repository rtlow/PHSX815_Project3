#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy.optimize as optimize

#setting matplotlib ticksize
matplotlib.rc('xtick', labelsize=14) 
matplotlib.rc('ytick', labelsize=14) 

#set matplotlib global font size
matplotlib.rcParams['font.size']=14

# negative log-likelihood function of just the rate
def negLL(rate, x):

    return -np.sum( x * np.log(rate) - rate )


# main function for our Python code
if __name__ == "__main__":
   
    haveInput = False
    InputFile = None

    outprefix = 'default_prefix_'

    # reading in the cmd args
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            continue

        # seeing if we have input files
        if sys.argv[i] == '--input':
            InputFile = sys.argv[i+1]
            haveInput = True

        # output file prefix
        if sys.argv[i] == '--outprefix':
            outprefix = sys.argv[i+1]
            

    if '-h' in sys.argv or '--help' in sys.argv or not np.all(haveInput):
        print ("Usage: %s [options] --input [input data]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print ("   --outprefix        output file prefixes")
        sys.exit(1)
    
    # reading in data from files
    counts = np.loadtxt(InputFile)

    Nexp = len(counts)

    rate_ests = []
    rate_est_errs = []
    medians = []
    
    # calculate the rate estimates and medians for each experiment
    for e in range(Nexp):
        
        # initial guess is the median
        r0 = np.median(counts[e])
        
        # do the minimization
        result = optimize.minimize(negLL, r0, args=counts[e])
        
        # get the result
        rate_est = result.x[0]
        
        # here's the error estimate
        rate_est_err = np.sqrt(result.hess_inv[0])[0]

        rate_ests.append(rate_est)
        rate_est_errs.append(rate_est_err)
        medians.append(r0)
    
    rate_ests = np.array(rate_ests)
    rate_est_errs = np.array(rate_est_errs)
    medians = np.array(medians)

    # visualize the result
    plt.figure(figsize=[12,7])
    
    # how close the two values match correspond to 
    # how close they land on the line y = x

    x = np.linspace(0, np.amax([rate_ests, medians]))

    plt.plot(x, x, 'k--', label='y=x')

    plt.errorbar(rate_ests, medians, xerr=rate_est_errs, fmt='bo', label='$\\hat{\\lambda_{noise}}$ vs median')
    plt.title('$\\hat{\\lambda_{noise}}$ vs median')
    plt.xlabel('$\\hat{\\lambda_{noise}}$')
    plt.ylabel('median')
    
    plt.legend()

    filename = outprefix + 'scatter_plot.png'
    plt.savefig(filename)
    plt.close()
    
    # equivalently, we can look at how closely the difference is to zero
    
    plt.figure(figsize=[12,7])

    plt.errorbar(rate_ests, rate_ests - medians, xerr=rate_est_errs, fmt='bo', label='$\\hat{\\lambda_{noise}}$ - median')
    plt.title('Residuals of $\\hat{\\lambda_{noise}}$ Estimation by the Median')
    plt.ylabel('$\\hat{\\lambda_{noise}}$ - median')
    plt.xlabel('$\\hat{\\lambda_{noise}}$')
    
    plt.axhline(0, color='k')
    plt.legend()

    filename = outprefix + 'residual_plot.png'
    plt.savefig(filename)
    plt.close()
    
    # output the calculated rate estimates, medians, and errors
    np.savetxt(outprefix + 'rate_est.dat', rate_ests)
    np.savetxt(outprefix + 'rate_est_err.dat', rate_est_errs)
    np.savetxt(outprefix + 'medians.dat', medians)
    
    sys.exit(1)

