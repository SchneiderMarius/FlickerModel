def DistributeSynapse(h,ResultFolder,roi,Strength,trl,stimFreq,InputNumber=1,SynPerNeuron=70):
    import pickle
    import numpy as np
    import random
    import pandas as pd    
    
    # seed to have same synapse termination segments in every run
    random.seed(1312)

    if not isinstance(InputNumber, list):    
        L = np.empty(0)
        D = np.empty(0)
        Name = []
        for i,sec in enumerate(h.allsec()):
            #print(str(sec))
            if any(ext in str(sec) for ext in roi) and any(char.isdigit() for char in str(sec)):
                D = np.append(D,sec.diam)       
                L = np.append(L,sec.L)
                #dist = np.append(dist,h.distance(sec(0.5),h.soma[0](0.5)))
                Name.append(sec)
    
    
        SynapseNumber =int(InputNumber*SynPerNeuron)
        
        # create Netstims
        stim = [None]*InputNumber
    
        if stimFreq==0:
            Sname = ResultFolder + '1_InputSpikes_HomogeneousPP' + '.p'
            parameters = pickle.load( open(Sname, "rb" ) )
            for i in range(InputNumber):
                stim[i] = h.VecStim()
                temp = [x*1000 for x in parameters.SpikeTimes.values[0][trl][i]]
                vec = h.Vector(temp)
                stim[i].play(vec)
        else:
            Sname = ResultFolder + '1_InputSpikes_' + str(stimFreq) + 'Hz' + '.p'
            #[parameters,freq,ppc,sp,PopActivity,PopActivityFilter,time] = pickle.load( open(Sname, "rb" ) )
            parameters = pickle.load( open(Sname, "rb" ) )
            for i in range(InputNumber):
                stim[i] = h.VecStim()
                temp = [x*1000 for x in parameters.SpikeTimes.values[0][trl][i]]
                vec = h.Vector(temp)
                stim[i].play(vec)
      
    
        SynNet = np.asarray([i for i in range(InputNumber) for _ in range(SynPerNeuron)])
        np.random.shuffle(SynNet)
    
        CumSumLength = np.cumsum(L)
    
        syn = [None]*SynapseNumber
        ncstim  = [None]*SynapseNumber
        
        for i in range(SynapseNumber):
            # to DO:
                # right now: every section has same chance of having a synapse
                # chance of synapse should also scale with size of section
            # old
            #SynSec = random.randrange(len(L))
                
            #scale chance of section having a synapse with length of section    
            SynSec = random.uniform(0, sum(L))
            SynSec = np.where(SynSec<CumSumLength)[0][0]
            
            SynLoc = random.uniform(0,1)
    #        SynNet = random.randrange(0,Diversity)
            
            syn[i] = h.Exp2Syn(Name[SynSec](SynLoc))           # attach synapse to a segment in the cell
            syn[i].tau1 = 1
            syn[i].tau2 = 3 
    
            ncstim[i] = h.NetCon(stim[SynNet[i]], syn[i])            # connect netstim with synapes
            ncstim[i].delay = 4                                # delay of synaptic event
            ncstim[i].weight[0] = Strength                        # NetCon weight is a vector.
            
    elif isinstance(InputNumber, list):    
        
        TotalSynapseNumber = int(np.sum(np.array(InputNumber)*SynPerNeuron))
        stim          = [None]*sum(InputNumber)
        
        syn           = [None]*TotalSynapseNumber
        ncstim        = [None]*TotalSynapseNumber       
        
        count_stim = 0
        count_syn  = 0
        
        for count in range(len(InputNumber)):
            SynapseNumber = int(InputNumber[count]*SynPerNeuron)
            
            L = np.empty(0)
            D = np.empty(0)
            Name = []
            for i,sec in enumerate(h.allsec()):
                #print(str(sec))
                if any(ext in str(sec) for ext in roi[count]) and any(char.isdigit() for char in str(sec)):
                    D = np.append(D,sec.diam)       
                    L = np.append(L,sec.L)
                    #dist = np.append(dist,h.distance(sec(0.5),h.soma[0](0.5)))
                    Name.append(sec)           
               
            if stimFreq[count]==0:
                Sname = ResultFolder + '1_InputSpikes_HomogeneousPP' + '.p'
                parameters = pickle.load( open(Sname, "rb" ) )
                for i in range(InputNumber[count]):
                    stim[i+count_stim] = h.VecStim()
                    temp = [x*1000 for x in parameters.SpikeTimes.values[0][trl][i]]
                    vec = h.Vector(temp)
                    stim[i+count_stim].play(vec)
            else:
                Sname = ResultFolder + '1_InputSpikes_' + str(stimFreq[count]) + 'Hz' + '.p'
                #[parameters,freq,ppc,sp,PopActivity,PopActivityFilter,time] = pickle.load( open(Sname, "rb" ) )
                parameters = pickle.load( open(Sname, "rb" ) )
                for i in range(InputNumber[count]):
                    stim[i+count_stim] = h.VecStim()
                    temp = [x*1000 for x in parameters.SpikeTimes.values[0][trl][i]]
                    vec = h.Vector(temp)
                    stim[i+count_stim].play(vec)        
                    
            SynNet = np.asarray([i for i in range(InputNumber[count]) for _ in range(SynPerNeuron)])
            np.random.shuffle(SynNet)
            
            CumSumLength = np.cumsum(L)           
            for i in range(SynapseNumber):
                SynSec = random.uniform(0, sum(L))
                SynSec = np.where(SynSec<CumSumLength)[0][0]
                
                SynLoc = random.uniform(0,1)            
            
                syn[i+count_syn] = h.Exp2Syn(Name[SynSec](SynLoc))           # attach synapse to a segment in the cell
                syn[i+count_syn].tau1 = 1
                syn[i+count_syn].tau2 = 3 
        
                ncstim[i+count_syn] = h.NetCon(stim[SynNet[i]+count_stim], syn[i+count_syn])            # connect netstim with synapes
                ncstim[i+count_syn].delay = 4                                # delay of synaptic event
                ncstim[i+count_syn].weight[0] = Strength[count]                        # NetCon weight is a vector.        

            count_stim =+ InputNumber[count]
            count_syn  =+ SynapseNumber

#    h_out = h

    return h,stim,syn,ncstim,parameters
