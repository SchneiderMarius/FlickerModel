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
from functions.ChangeMech import ChangeMech

Folder = os.path.join(os.getcwd(),'results/FigS3')
LogFolder = os.path.join(os.getcwd(),'LogFiles/slurm-%A_%a.out')
ModelFolder = os.path.join(os.getcwd(),'CellModels')
DataFolder = os.path.join(os.getcwd(),'data/')

FitData = scipy.io.loadmat(DataFolder  + 'LEDPPC.mat')

if not os.path.exists(Folder):
    os.makedirs(Folder)

ModelName = ['Pyr',] 
ModelID = [472451419] 

LGN_ROI = ['dend']
LGN_SynNum = [6,8]
LGN_Freq = [10, 20, 40, 60]
Local_ROI = ['dend', 'apic']
Local_SynNum = [60,43]
Local_Freq = 0
syn_weight = [0.000012, 0.000012]

Trials = 200


modify = ['passive','cm',[2,3],'cm']
factor = np.array([0.2,0.5,1])

for i1, ID_temp in enumerate(ModelID):
    
    FRmean = np.zeros((len(factor),len(LGN_Freq)))
    PPCpeak = np.zeros((len(factor),len(LGN_Freq)))
    PPC = [[None for x in range(len(LGN_Freq))] for y in range(len(factor))] 
    ID = str(ID_temp) + '_changeCM'
    
    for ii,fac in enumerate(factor):
        print(str(ii) + '/' + str(len(factor)))
        ChangeMech(ModelFolder,str(ID_temp),ID,modify,fac)
    
        for i2, Freq in enumerate(LGN_Freq):
    
            SName = str(ID) +'_'+ str(ii)+ '_' + str(Freq) + 'Hz' + '_LGNsyn_' + str(
                LGN_SynNum[i1]) + '_Localsyn_' + str(Local_SynNum[i1])+'_Synweight_'+str(syn_weight[i1])
        
            if not os.path.isdir(Folder+SName):
                os.mkdir(Folder+SName)
        
            JobsBackground = int(os.popen('squeue --me | wc -l').read())
        
            for i in range(Trials):
                call(['sbatch', '-p', '8GBXS', '-Q', '--output', LogFolder, 'evalbatch2.sh',Folder, SName, str(ID),
                     str(Freq), str(0), str(LGN_SynNum[i1]), str(Local_SynNum[i1]), str(syn_weight[i1]), str(i)])
        
            time.sleep(5)
            JobsRunning = int(os.popen('squeue --me | wc -l').read())
            while JobsRunning-JobsBackground > 0:
                time.sleep(5)
                JobsRunning = int(os.popen('squeue --me | wc -l').read())
        
            print('Jobs Done')
    
            FRmean[ii,i2],PPCpeak[ii,i2],PPCFreq,PPC[ii][i2]= FreqAnalysis(Folder, SName, Freq)
      
        SaveName = Folder + ID+'_scan' + '_LGNsyn_' + str(LGN_SynNum[i1]) + '_Localsyn_' + str(Local_SynNum[i1])
    
        par         = {'FRmean':[FRmean],'PPC':[PPC],'PPCFreq':[PPCFreq],'PPCpeak':[PPCpeak],'StimFreq':[LGN_Freq]}
        parameters  = pd.DataFrame(data=par)
    pickle.dump([FRmean,PPCpeak,PPCFreq,PPC,factor,LGN_Freq], open(SaveName, "wb"))   
        
    