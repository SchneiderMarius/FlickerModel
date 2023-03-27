## Create Poisson Spike Train and evaluate PPC
import os
import numpy as np
from scipy import signal
import pickle
import pandas as pd
import scipy.io
from functions.ppcSpectrum import ppcSpectrum
from functions.PoissonTimes import PoissonTimes
import random

random.seed(1312)

ResultFolder = os.path.join(os.getcwd(),'results/Fig3')
DataFolder = os.path.join(os.getcwd(),'data')



if not os.path.exists(ResultFolder):
    os.makedirs(ResultFolder)
    
FitData = scipy.io.loadmat(DataFolder  + 'LEDPPC.mat')

fsample     = 1000
duration    = 10
rate        = 6
modStr      = 0.2
dmod        = modStr
NumNeurons  = 40
NumTrials   = 200
twin        = 0.35
foilim      = np.array((1, 100))
maxIter     = 20

Frequency    = np.ndarray.tolist(FitData['StimFreq'].ravel())

sos         = signal.butter(1, 100, 'low', fs=1000, output='sos')
time        = np.arange(1/fsample,duration+1/fsample,1/fsample)

PPCfit = [None] * len(Frequency)
PPCfitPeak = [None] * len(Frequency)

for ifreq,stimFreq in enumerate(Frequency):
    modStrUse = modStr
        
    rounds = 0
    PPCpeak  = 1
    PPCErrorHist    = []
    while abs(FitData['PPC_Mean'][0,ifreq]-PPCpeak)>FitData['PPC_SEM'][0,ifreq] and rounds<maxIter:
        modFunction = (lambda x: rate*modStrUse*np.sin(2*np.pi*x*stimFreq)+rate)
        sp          = [[[None] for i in range(NumNeurons)] for j in range(NumTrials)]   
        frate       = np.array([])
        frate       = np.empty([NumTrials, NumNeurons])
        
        
        SenderLFP   = [None]*NumTrials  
        PPC         = np.empty(shape=(NumNeurons,int((2*twin)/(1/foilim[-1])))) 
        for i in range(NumTrials):
            
            for n in range(NumNeurons):
                sp[i][n]    = PoissonTimes(modFunction,time)
                frate[i,n]       = len(sp[i][n])/duration
                
                if n==0:
                    SummedActivity = np.array(sp[i][n])
                else:
                    SummedActivity = np.concatenate((SummedActivity,np.array(sp[i][n])))
    
            [hist,binedges] = np.histogram(SummedActivity, np.append(time-0.5/fsample,time[-1]+0.5/fsample))   
            
            SenderLFP[i] = signal.sosfilt(sos, hist)
            SenderLFP[i] = SenderLFP[i] - np.mean(SenderLFP[i])
    
        for n in range(NumNeurons):
            PPCFreq,PPC[n,:] = ppcSpectrum(sp[n],SenderLFP,time,twin,foilim)
    
        PPC = np.mean(PPC,axis=0)
        idF = np.argmin(abs(PPCFreq-stimFreq))
        PPCpeak  = PPC[idF]
        PPCErrorHist.append(FitData['PPC_Mean'][0,ifreq]-PPCpeak)

        if len(PPCErrorHist)>1 and PPCErrorHist[-2]*PPCErrorHist[-1]<0:
            dmod = dmod/2
            
        if PPCErrorHist[-1]>FitData['PPC_SEM'][0,ifreq]:
            modStrUse = modStrUse + dmod
        elif PPCErrorHist[-1]<-FitData['PPC_SEM'][0,ifreq]:
            modStrUse = modStrUse - dmod
        rounds =+1    
    
    PPCfit[ifreq] = PPC  
    PPCfitPeak[ifreq] = PPCpeak  
    
    
    print('Freq: '+ str(stimFreq) + '   PPC_data: ' + str(round(FitData['PPC_Mean'][0,ifreq]*1000)/1000)+
          '   PPC_model: ' + str(round(PPCpeak*1000)/1000)+ 
          '   Error [SEM]: ' + str(round(PPCErrorHist[-1]/FitData['PPC_SEM'][0,ifreq]*100)/100))
    
    par         = {'fsample':[fsample],'duration':[duration],'stimFreq':[stimFreq],'rate':[np.mean(frate)],'modStr':[modStrUse],
                   'SpikeTimes': [sp],'time':[time],'PPCError':PPCErrorHist[-1],'PPCfit':[PPCfit],'PPCfreq':[PPCFreq],'PPCpeak':[PPCfitPeak]}
    parameters  = pd.DataFrame(data=par)
    Sname = ResultFolder + '1_InputSpikes_' + str(stimFreq) + 'Hz' + '.p'
    pickle.dump(parameters, open(Sname, "wb"))   
