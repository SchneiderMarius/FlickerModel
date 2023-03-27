from scipy import signal
from functions.ppcSpectrum import ppcSpectrum
import numpy as np
import pickle
import glob

def FreqAnalysis(Folder,SName,Freq):
    sos     = signal.butter(1, 100, 'low', fs=1000, output='sos')
    twin    = 0.075
    foilim  = np.array((1, 100))
    twin    = 0.15
    
    SNameInput = '1_InputSpikes_' + str(Freq) + 'Hz.p'

    Input = pickle.load(open(Folder+SNameInput, "rb")) 

    fsample = Input.fsample.values[0]
    time    = Input.time.values[0]

    Files = glob.glob(Folder+SName+'/*.p')
    
    Trials      = len(Files)
    Spikes      = [None]*Trials
    SenderLFP   = [None]*Trials
    FR          = np.empty(Trials)
                            
    for i in range(Trials):
        SPout = pickle.load(open(Files[i], "rb"))
        iTrial = SPout[2]

        Spikes[i]  = SPout[1]/1000
        FR[i]      = SPout[0] 
        
        SummedActivity = np.concatenate(Input.SpikeTimes.values[0][iTrial][:])
        [hist,binedges] = np.histogram(SummedActivity, np.append(time-0.5/fsample,time[-1]+0.5/fsample))   
        
        SenderLFP[i] = signal.sosfilt(sos, hist)
        SenderLFP[i] = SenderLFP[i] - np.mean(SenderLFP[i])
    
    #original
    FRmean   = np.mean(FR)       
    # if FRmean==0:
    #     PPCpeak = 0
        
    # else:
    #     freq,ppc = ppcSpectrum(Spikes,SenderLFP,time,twin,foilim)
    #     idx      = np.argmin(abs(freq-Freq))
       
    #     FRmean   = np.mean(FR)       
    #     PPC      = ppc
    #     PPCFreq  = freq
    #     PPCpeak  = ppc[idx]    

    freq,ppc = ppcSpectrum(Spikes,SenderLFP,time,twin,foilim)
    idx      = np.argmin(abs(freq-Freq))
   
    FRmean   = np.mean(FR)       
    PPC      = ppc
    PPCFreq  = freq
    PPCpeak  = ppc[idx]    

    if FRmean==0:
        PPCpeak = 0

    return FRmean,PPCpeak,PPCFreq,PPC
