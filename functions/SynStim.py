def SynStim(ResultFolder,Sname,i_trial):
    import pickle
    import DistributeSynapse2 as DN
    from scipy.signal import find_peaks
    import numpy as np        
    import InitModel as IM
    
    par = pickle.load(open(ResultFolder +'Par_' +Sname+'.p', "rb"))  # save it into a file named save.p
    
    ID           = par[0]
    roi          = par[1]
    Strength     = par[2]
    ExpType      = par[3]
    Freq         = par[4]
    InputNum     = par[5]
    SynPN        = par[6]
    
    hInit, manifest, utils, description = IM.InitModel(ID)
   
    h_out,stim,syn,ncstim,parameters = [None]*len(roi),[None]*len(roi),[None]*len(roi),[None]*len(roi),[None]*len(roi)
    
    for i in range(len(roi)):
        if i==0:
            h_out[i], stim[i], syn[i], ncstim[i], parameters[i] = DN.DistributeSynapse2(
                hInit, ResultFolder, roi[i],Strength[i],i_trial,ExpType[i],Freq[i], InputNumber=InputNum[i], SynPerNeuron=SynPN[i])                
        else:
            h_out[i], stim[i], syn[i], ncstim[i], parameters[i] = DN.DistributeSynapse2(
                h_out[i-1], ResultFolder, roi[i],Strength[i],i_trial,ExpType[i],Freq[i], InputNumber=InputNum[i], SynPerNeuron=SynPN[i])                
       
    dur = parameters[len(roi)-1].duration.values[0]*1000
    
    v_soma = h_out[len(roi)-1].Vector()                    # set up recording vector
    v_soma.record(h_out[len(roi)-1].soma[0](0.5)._ref_v)    # location of recording
    
    timeVec = h_out[len(roi)-1].Vector()
    timeVec.record(h_out[len(roi)-1]._ref_t)                # record time
    
    apc = h_out[len(roi)-1].APCount(h_out[len(roi)-1].soma[0](0.5))
    
    h_out[len(roi)-1].tstop = dur
    h_out[len(roi)-1].run()
    
    ##  outputs
    FR = apc.n/dur*1000
    timeVec = np.array(timeVec)
    voltVec = np.array(v_soma)
    
    peak_idx, _ = find_peaks(voltVec, height=-20)
    SPtimes = timeVec[peak_idx]
    
#    SenderSpikes   = parameters[len(roi)-1].SpikeTimes.values[0][i_trial][0]
#    SenderAcitivty = parameters[len(roi)-1].PopulationActivty_filter.values[0][i_trial]
#    ReceiverSpikes = SPtimes/1000
 
    
    Sname = ResultFolder + Sname +'/' + Sname +'_trial'+str(i_trial) + '.p'
    
#    pickle.dump([SPtimes,SenderSpikes,SenderAcitivty,ReceiverSpikes,parameters[len(roi)-1]], open(Sname, "wb"))  # save it into a file named save.p
    pickle.dump([FR,SPtimes], open(Sname, "wb"))  # save it into a file named save.p