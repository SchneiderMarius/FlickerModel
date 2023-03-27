def DistributeSynapse(h,ResultFolder,roi,Density,Diversity,Strength,trl,stim_type = 'Poisson',*args,**kwargs):
    import pickle
    import numpy as np
    import random

    # create Netstims
    stim = [None]*Diversity

    if stim_type is 'Poisson':
        Sname = ResultFolder + '1_InputSpikes_HomogeneousPP' + '.p'
        [parameters,freq,ppc,sp,PopActivity,time] = pickle.load( open(Sname, "rb" ) )
        for i in range(Diversity):
            stim[i] = h.VecStim()
            temp = [x*1000 for x in sp[i][trl]]
            vec = h.Vector(temp)
            stim[i].play(vec)
    else:
        Sname = ResultFolder + '1_InputSpikes_' + str(stimFreq) + 'Hz' + '.p'
        [parameters,freq,ppc,sp,PopActivity,time] = pickle.load( open(Sname, "rb" ) )
        for i in range(Diversity):
            stim[i] = h.VecStim()
            temp = [x*1000 for x in sp[i][trl]]
            vec = h.Vector(temp)
            stim[i].play(vec)
  
    # Find regions to place dynapses
    L = np.empty(0)
    D = np.empty(0)
    Name = []
    for i,sec in enumerate(h.allsec()):
        print(str(sec))
        if any(ext in str(sec) for ext in roi) and any(char.isdigit() for char in str(sec)):
            D = np.append(D,sec.diam)       
            L = np.append(L,sec.L)
            #dist = np.append(dist,h.distance(sec(0.5),h.soma[0](0.5)))
            Name.append(sec)

    SynNum = int(round(Density*np.sum(L)))


    syn     = [None]*SynNum
    ncstim  = [None]*SynNum
    
    for i in range(SynNum):
        SynSec = random.randrange(len(L))
        SynLoc = random.uniform(0,1)
        SynNet = random.randrange(0,Diversity)
        
        syn[i] = h.Exp2Syn(Name[SynSec](SynLoc))           # attach synapse to a segment in the cell
        syn[i].tau1 = 1
        syn[i].tau2 = 3 

        ncstim[i] = h.NetCon(stim[SynNet], syn[i])            # connect netstim with synapes
        ncstim[i].delay = 4                                # delay of synaptic event
        ncstim[i].weight[0] = Strength                        # NetCon weight is a vector.


    return h,parameters
