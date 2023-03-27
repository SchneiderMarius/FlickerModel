from functions.FreqAnalysis import FreqAnalysis
from functions.SynStim import SynStim
import time
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import find_peaks
from subprocess import call
import scipy.io


Folder = os.path.join(os.getcwd(),'results/Fig3')
SaveFolder1 = os.path.join(os.getcwd(),'results/FigS1')
SaveFolder2 = os.path.join(os.getcwd(),'results/FigS2')

LogFolder = os.path.join(os.getcwd(),'LogFiles/slurm-%A_%a.out')


if not os.path.exists(Folder):
    os.makedirs(Folder)

ModelName = ['Pyr','PV'] 
ModelID = [472451419,471085845] 


LGN_ROI = ['dend']
LGN_SynNum = [6,8]
LGN_Freq = [10, 20, 40, 60]
Local_ROI = ['dend', 'apic']
Local_SynNum = [60,43]
Local_Freq = 0
syn_weight = [0.000012, 0.000012]

Trials = 200

for i1, ID in enumerate(ModelID):
    
    FRmean = np.zeros(len(LGN_Freq))
    PPCpeak = np.zeros(len(LGN_Freq))
    PPC = [None] * len(LGN_Freq)

    for i2, Freq in enumerate(LGN_Freq):

        SName = str(ID) + '_' + str(Freq) + 'Hz' + '_LGNsyn_' + str(
            LGN_SynNum[i1]) + '_Localsyn_' + str(Local_SynNum[i1])+'_Synweight_'+str(syn_weight[i1])
    
        if not os.path.isdir(Folder+SName):
            os.mkdir(Folder+SName)
    
        JobsBackground = int(os.popen('squeue --me | wc -l').read())
    
        for i in range(Trials):
            call(['sbatch', '-p', '8GBXS', '-Q', '--output', LogFolder, 'evalbatch.sh',Folder, SName, str(ID),
                 str(Freq), str(0), str(LGN_SynNum[i1]), str(Local_SynNum[i1]), str(syn_weight[i1]), str(i)])
    
        time.sleep(5)
        JobsRunning = int(os.popen('squeue --me | wc -l').read())
        while JobsRunning-JobsBackground > 0:
            time.sleep(5)
            JobsRunning = int(os.popen('squeue --me | wc -l').read())
    
        print('Jobs Done')

        FRmean[i2],PPCpeak[i2],PPCFreq,PPC[i2]= FreqAnalysis(Folder, SName, Freq)
  
    SaveName = ModelName[i1] + '_LGNsyn_' + str(LGN_SynNum[i1]) + '_Localsyn_' + str(Local_SynNum[i1])
    par         = {'FRmean':[FRmean],'PPC':[PPC],'PPCFreq':[PPCFreq],'PPCpeak':[PPCpeak],'StimFreq':[LGN_Freq]}
    parameters  = pd.DataFrame(data=par)
    pickle.dump(parameters, open(Folder + SaveName, "wb"))   
    pickle.dump(parameters, open(SaveFolder1 + SaveName, "wb"))   
    pickle.dump(parameters, open(SaveFolder2 + SaveName, "wb"))   
    