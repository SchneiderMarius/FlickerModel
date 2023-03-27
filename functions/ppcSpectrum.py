import numpy as np

def ppcSpectrum(spike,lfp,t,twin,foilim):
    
    #t = np.expand_dims(t,axis=0)
    
    fsample = 1/(t[1]-t[0])
    # Taper
    begpad = int(np.round(-twin*fsample))
    endpad = int(np.round(twin*fsample))
    numsmp = int(endpad-begpad+1)
    
    taper  = np.hanning(numsmp)
    taper  = taper/np.sqrt(sum(taper**2))

            #maybe sparsen matrix to save memory!    
    taper = np.diag(taper)
    
###################################### Fourier ################################
    nTrial      = len(spike)
    spectrum    = [None]*nTrial    
    spiketime   = [None]*nTrial    
    spiketrial  = [None]*nTrial    
    
    freqaxis = np.linspace(0,fsample,numsmp)
    
    foilimUpdate = np.empty_like(foilim)
    fbeg = np.argmin(abs(freqaxis-foilim[0]))
    fend = np.argmin(abs(freqaxis-foilim[1]))
    
    foilimUpdate[0] = freqaxis[fbeg]
    foilimUpdate[1] = freqaxis[fend]
    
    spike_repr  = np.zeros((1,numsmp))
    time        = np.linspace(-twin,twin,numsmp)        
    time        = np.expand_dims(time,axis=0)
    spike_repr[0,begpad] = 1
    
    spike_fft = np.fft.fft(spike_repr,axis=1)
    spike_fft = spike_fft[0,fbeg:fend+1]
    spike_fft = spike_fft/abs(spike_fft)
    
    rephase = np.diag(np.conj(spike_fft))
    spike_fft = np.expand_dims(spike_fft,axis=0)

    for iTrial in range(nTrial):
        timeBins = np.append(t, t[-1]+1/fsample) - 0.5/fsample
        
        
        # new works when spike times dont exactly match time vector
        spikesmp    = np.empty((1,len(spike[iTrial]))) 
#before
#        spikesmp    = np.empty((1,len(spike[iTrial])),dtype=int) 
        
        
        spikesmp[:] = np.NaN
        for i_nsp,nsp in enumerate(spike[iTrial]):
            spikesmp[0,i_nsp] = int(np.argmin(np.abs(t-nsp)))
        
        # old, works only if times of spikes match time vetor
        #spikesmp = np.where(np.in1d(t, spike[iTrial]))[0]
        
        spikesmp = np.delete(spikesmp, np.append(np.where(spikesmp == 0),np.where(spikesmp == len(timeBins))))        
        
        # maybe just use origial times (ts=spike)
        spikesmp = spikesmp.astype(int)        
        ts       = timeBins[spikesmp]
        
        spiketime[iTrial] = ts[:]
        tr = iTrial*np.ones(spikesmp.shape)
        spiketrial[iTrial] = tr
        
        spectrum[iTrial] = np.zeros((len(spikesmp), fend-fbeg+1),dtype = 'complex_')


        for iSpike, vSpike in enumerate(spikesmp):
            begsmp = vSpike + begpad
            endsmp = vSpike + endpad
            
            if begsmp<0 or endsmp+1>len(lfp[iTrial]):
                segment = np.empty((1,numsmp))
                segment[:] = np.NaN
            else:
                segment = lfp[iTrial][begsmp:endsmp+1] # test if it picks the right indices!
                segment = np.expand_dims(segment,axis=0)   
                
            segment = segment - np.mean(segment)
            
            if np.any(np.isnan(segment)):
                segment_fft = np.empty(segment.shape)
                segment_fft[:] = np.NaN
            else:
                segment_fft = np.fft.fft(np.matmul(segment,taper),axis=1)
            
            segment_fft = segment_fft[0,fbeg:fend+1]/np.sqrt(numsmp/2)
            segment_fft = np.matmul(segment_fft,rephase) 

            spectrum[iTrial][iSpike,:] = segment_fft

################################################## PPC ########################

    fourierspctrm = np.concatenate(spectrum,axis=0)
    trial         = np.concatenate(spiketrial,axis=0)
    time          = np.concatenate(spiketime,axis=0)
    freq          = freqaxis[fbeg:fend+1]

    nTrials       = len(np.unique(trial))  
    
    fourierspctrm = fourierspctrm/abs(fourierspctrm)
    
    S       = np.zeros((1,len(freq)),dtype = 'complex_')
    SS      = np.zeros((1,len(freq)),dtype = 'complex_')
    dof     = np.zeros((1,len(freq)))
    dofSS   = np.zeros((1,len(freq)))

    for iTrial in range(nTrials):
        spikesInTrial = np.where(np.in1d(trial,iTrial))[0]
        spc = fourierspctrm[spikesInTrial,:]
        
        n = np.sum(~np.isnan(spc),axis=0)
        m = np.nansum(spc, axis=0)
        hasNum = ~np.isnan(m)    

        S[0,hasNum]     += m[hasNum]
        SS[0,hasNum]    += m[hasNum]*np.conj(m[hasNum])
        dof[0,hasNum]   += n[hasNum]
        dofSS[0,hasNum] += n[hasNum]**2
    
    ppc = np.squeeze(((S*np.conj(S)-SS)/(dof**2-dofSS)).real)


    return freq,ppc