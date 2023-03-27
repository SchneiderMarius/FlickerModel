def SynImpedance(v_soma, i_syn, v_stim, timeVec, freq_temp):
    from scipy.fft import rfft
    import numpy as np

    dt = (timeVec[1]-timeVec[0])/1000
    N  = len(timeVec)    
    T  = N*dt
    
    v_soma_f    = rfft(v_soma - v_soma.mean())      # Compute the Fourier transform of x,
    v_syn_f     = rfft(v_stim - v_stim.mean())        # Compute the Fourier transform of x,
    i_syn_f     = rfft(-i_syn + i_syn.mean())       # Compute the Fourier transform of x,
    
    v_soma_S    = np.real(2 * dt ** 2 / T * (v_soma_f * np.conj(v_soma_f))) # ... and the spectrum.
    v_syn_S     = np.real(2 * dt ** 2 / T * (v_syn_f * np.conj(v_syn_f)))   # ... and the spectrum.
    i_syn_S     = np.real(2 * dt ** 2 / T * (i_syn_f * np.conj(i_syn_f)))   # ... and the spectrum.
    
    df      = 1 / T                                     # Define the frequency resolution.
    #fNQ     = 1 / dt / 2                               # Define the Nyquist frequency.
    faxis   = np.arange(len(i_syn_S)) * df                 # Construct the frequency axis.
    
    TI      = v_soma_S/i_syn_S
    i       = np.argmin(abs(faxis-freq_temp))
    TI_freq = TI[i]
        
    return TI, TI_freq, faxis, v_soma_S, v_syn_S, i_syn_S