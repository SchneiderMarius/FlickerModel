def ImpedancePhase(StimCurr,StimVolt,SomaVolt,timeVec):
    from scipy.fft import fft, fftfreq
    import numpy as np
    
    N = len(timeVec)
    T = round(timeVec[-1]/len(timeVec)*1000)/1000 / 1000
    xf = fftfreq(N, T)[:N//2]
    
    StimCurrFFT = fft(StimCurr)
    StimVoltFFT = fft(StimVolt)
    SomaVoltFFT = fft(SomaVolt)
    
    StimCurrFFT = StimCurrFFT[0:N//2]
    StimVoltFFT = StimVoltFFT[0:N//2]
    SomaVoltFFT = SomaVoltFFT[0:N//2]
    
    StimCurrFFT = StimCurrFFT[xf>=1]
    StimVoltFFT = StimVoltFFT[xf>=1]
    SomaVoltFFT = SomaVoltFFT[xf>=1]
    xf = xf[xf>=1]
    
    peakID = np.argmax(np.abs(StimCurrFFT))
    
    Zlocal  = StimVoltFFT/StimCurrFFT
    Zsoma   = SomaVoltFFT/StimCurrFFT
    
    ImpPhaseSoma = np.degrees(np.arctan(Zsoma.imag/Zsoma.real))
    ImpAmpSoma = np.sqrt(Zsoma.real**2+Zsoma.imag**2)
    
    ImpPhaseLocal = np.degrees(np.arctan(Zlocal.imag/Zlocal.real))
    ImpAmpLocal = np.sqrt(Zlocal.real**2+Zlocal.imag**2)        
    
    return ImpPhaseSoma[peakID], ImpAmpSoma[peakID],xf[peakID],ImpPhaseLocal[peakID],ImpAmpLocal[peakID]     
