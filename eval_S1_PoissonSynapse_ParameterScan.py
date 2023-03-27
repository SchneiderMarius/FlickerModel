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

Folder = os.path.join(os.getcwd(),'results/Fig3/')
SaveFolder = os.path.join(os.getcwd(),'results/FigS1/')
LogFolder = os.path.join(os.getcwd(),'LogFiles/slurm-%A_%a.out')

if not os.path.exists(Folder):
    os.makedirs(Folder)

ModelName = ['Pyr','PV'] 
ModelID = [472451419,471085845] 

LGN_ROI = ['dend']


LGN_SynNum = np.linspace(1,10,10,dtype=int)
LGN_Freq = 10
Local_ROI = ['dend', 'apic']
Local_SynNum = np.linspace(30, 70, 21,dtype=int)
Local_Freq = 0
syn_weight = 0.000012
Trials = 100

# freq = np.append(, np.linspace(15,105,8))
# LGN_SynNum = [6,8]
# LGN_Freq = [10, 20, 40, 60]
# Local_ROI = ['dend', 'apic']
# Local_SynNum = [60,43]
# Local_Freq = 0
# syn_weight = [0.000012, 0.000012]


for i1, ID in enumerate(ModelID):
    
    FRmean = np.zeros((len(LGN_SynNum),len(Local_SynNum)))
    PPCpeak = np.zeros((len(LGN_SynNum),len(Local_SynNum)))
    PPC = [[None for j in range(len(LGN_SynNum))]for i in range(len(Local_SynNum))]


    for i2, LGNSyn in enumerate(LGN_SynNum):
        for i3, LOCALSyn in enumerate(Local_SynNum):

            SName = str(ID) + '_' + str(LGN_Freq) + 'Hz' + '_LGNsyn_' + str(
                LGNSyn) + '_Localsyn_' + str(LOCALSyn)+'_Synweight_'+str(syn_weight)

            if not os.path.isdir(SaveFolder+SName):
                os.mkdir(SaveFolder+SName)
    
                JobsBackground = int(os.popen('squeue --me | wc -l').read())
        
                for i in range(Trials):
                    call(['sbatch', '-p', '8GBXS', '-Q', '--output', LogFolder, 'evalbatch.sh',SaveFolder, SName, str(ID),
                         str(LGN_Freq), str(0), str(LGNSyn), str(LOCALSyn), str(syn_weight), str(i)])
        
                time.sleep(5)
                JobsRunning = int(os.popen('squeue --me | wc -l').read())
                while JobsRunning-JobsBackground > 0:
                    time.sleep(5)
                    JobsRunning = int(os.popen('squeue --me | wc -l').read())
            
                print('Jobs Done')
        
            FRmean[i2,i3], PPCpeak[i2,i3], PPCFreq, PPC[i2][i1] = FreqAnalysis(SaveFolder, SName, LGN_Freq)

    SaveName = SaveFolder + ModelName[i1] +'_'+ str(ID)+'_'+str(LGN_Freq)+'Hz'   
    par         = {'FRmean':[FRmean],'PPC':[PPC],'PPCFreq':[PPCFreq],'PPCpeak':[PPCpeak],'StimFreq':[LGN_Freq]
                   ,'LGNSynNum':[LGN_SynNum],'LocalSynNum':[Local_SynNum],'SynWeight':[syn_weight]}
    parameters  = pd.DataFrame(data=par)
    pickle.dump(parameters, open(SaveName, "wb"))   
    
    
