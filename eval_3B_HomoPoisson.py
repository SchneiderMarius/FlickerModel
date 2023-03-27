##Create Poisson Spike Train and calc PPC
## Parameters
import os
import numpy as np
from functions.PoissonTimes import PoissonTimes
from scipy import signal
import pickle
import pandas as pd
  

ResultFolder1 = os.path.join(os.getcwd(),'results/Fig3/')
ResultFolder2 = os.path.join(os.getcwd(),'results/FigS1/')
ResultFolder3 = os.path.join(os.getcwd(),'results/FigS2/')

fsample     = 1000
duration    = 10
rate        = 8
NumNeurons  = 1000
NumTrials   = 600

sos         = signal.butter(1, 100, 'low', fs=1000, output='sos')

time        = np.arange(1/fsample,duration+1/fsample,1/fsample)
modFunction = (lambda x: rate+x-x)

##############################################################################

sp          = [[[None] for i in range(NumNeurons)] for j in range(NumTrials)]
lfp         = [[[None] for i in range(NumNeurons)] for j in range(NumTrials)]
lfpNoise    = [[[None] for i in range(NumNeurons)] for j in range(NumTrials)]
PopActivity = [None]*NumTrials
PopActivityFilter = [None]*NumTrials

frate = np.array([])
d = np.array([])
for i in range(NumTrials):
    for n in range(NumNeurons):
        sp[i][n] = PoissonTimes(modFunction,time)
        
        
par         = {'fsample':[fsample],'duration':[duration],'rate':[rate],'SpikeTimes': [sp],'time':[time]}
parameters  = pd.DataFrame(data=par)
Sname = '1_InputSpikes_HomogeneousPP' + '.p'
pickle.dump(parameters, open(ResultFolder1 + Sname, "wb"))    
pickle.dump(parameters, open(ResultFolder3 + Sname, "wb"))    
pickle.dump(parameters, open(ResultFolder3 + Sname, "wb"))    
