import pickle
import DistributeSynapse as DN
from scipy.signal import find_peaks
import numpy as np        
import InitModel as IM
import os

def PoissonSyn(ResultFolder,Name,ModelID,freq1,freq2,InNum1,InNum2,strength,i_trial):

    Roi = [['dend'],['dend','apic']]   

    Strength     = [strength,strength]
    Freq         = [freq1,freq2]
    InputNum     = [InNum1,InNum2]

    h_init, manifest, utils, description = IM.InitModel(ModelID)
       
    h, stim, syn, ncstim, parameters = DN.DistributeSynapse(
            h_init, ResultFolder, Roi,Strength,i_trial,Freq, InputNumber=InputNum,SynPerNeuron=70)       
    
    dur = parameters.duration.values[0]*1000
    
    v_soma = h.Vector()                    # set up recording vector
    v_soma.record(h.soma[0](0.5)._ref_v)    # location of recording
    
    timeVec = h.Vector()
    timeVec.record(h._ref_t)                # record time
    
    apc = h.APCount(h.soma[0](0.5))
    
    h.tstop = dur
    h.run()
    
    FR = apc.n/dur*1000
    timeVec = np.array(timeVec)
    voltVec = np.array(v_soma)
    
    peak_idx, _ = find_peaks(voltVec, height=-30)
    SPtimes = timeVec[peak_idx]
        
    Sname = ResultFolder + Name +'/' + Name +'_trial'+str(i_trial) + '.p'
    if i_trial<10:
        pickle.dump([FR,SPtimes,i_trial,timeVec,voltVec], open(Sname, "wb"))
    else:
        pickle.dump([FR,SPtimes,i_trial], open(Sname, "wb"))    

if __name__ == "__main__":
    import sys
    
    
    x1 = sys.argv[1]    
    x2 = sys.argv[2]
    x3 = int(sys.argv[3])
    x4 = int(sys.argv[4])
    x5 = int(sys.argv[5])
    x6 = int(sys.argv[6])
    x7 = int(sys.argv[7])
    x8 = float(sys.argv[8])
    x9 = int(sys.argv[9])

    PoissonSyn(x1,x2,x3,x4,x5,x6,x7,x8,x9)
    
