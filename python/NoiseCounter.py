#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import numpy as np
import scipy.special as special

# global variables
kB = 8.617333e-5 # [ev/k]

Ef = 1.12 / 2 # band gap of Si divided by 2 [eV]

Nelectrons = 1000 # no. free electrons per pixel

# returns the probability of finding an electron
# at energy E [eV] and temperature T [K]
def FermiDirac(E, T):
    return 1/( 1 + np.exp( (E - Ef)/ (kB * T) ) )


# number of noise electrons we measure
# are the number of electrons above the
# Fermi level, so we can do numerical
# integration
def sampleFermiDirac(Nsample, T, n=100):
    
    samples = []
    
    # do the integration here
    
    # lower bound is Ef
    a = Ef

    # upper bound is 1

    b = 1

    V = b - a

    int_samples = []

    xi = np.random.uniform(a, b, size=n)

    int_samples.append( FermiDirac(xi, T) )
    
    # this is the probability of being detected
    integral = (V/n) * np.sum(int_samples)
    
    for i in range(Nsample):

        # generate Nelectrons uniformly random numbers
        nums = np.random.uniform(size=Nelectrons)

        # number of noise electrons
        rate = np.sum( nums <= integral )
        
        samp = np.random.poisson(rate)
        
        samples.append(samp)

    return samples


# main function for experiment code
if __name__ == "__main__":
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [options]" % sys.argv[0] )
        print('Options:')
        print('-T [number]          temperature in Kelvin')
        print('-Nfree [number]      no. free electrons in pixel')
        print('-Nmeas [number]      no. measurements per experiment')
        print('-Nexp [number]       no. experiments')
        print('-output [string]     output file name')

        print
        sys.exit(1)



    # default number of exposures (letting light collect for fixed time) - per experiment
    Nmeas = 1

    # default number of experiments
    Nexp = 1

    # default temperature
    T = 300

    # output file defaults
    doOutputFile = False



    if '-T' in sys.argv:
        p = sys.argv.index('-T')
        ptemp = float(sys.argv[p+1])
        if ptemp > 0:
            T = ptemp
    if '-Nmeas' in sys.argv:
        p = sys.argv.index('-Nmeas')
        Nt = int(sys.argv[p+1])
        if Nt > 0:
            Nmeas = Nt
    if '-Nexp' in sys.argv:
        p = sys.argv.index('-Nexp')
        Ne = int(sys.argv[p+1])
        if Ne > 0:
            Nexp = Ne
    if '-Nfree' in sys.argv:
        p = sys.argv.index('-Nfree')
        Ne = int(sys.argv[p+1])
        if Ne > 0:
            Nelectrons = Ne
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        doOutputFile = True



    experiments = []
    
    for n in range(Nexp):
            
        measurements = sampleFermiDirac(Nmeas, T)
        experiments.append(measurements)

    if doOutputFile:

        np.savetxt(OutputFileName, experiments)


    else:

        print( experiments )
