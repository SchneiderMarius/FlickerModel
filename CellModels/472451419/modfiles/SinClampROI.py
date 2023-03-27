def SinClampROI(h,roi,dist):
    import numpy as np
    import random as rd
    import os
    
    folder = '/mnt/hpx/home/schneiderm/Projects/12_Neuron/'
    folderhoc = os.path.join(folder,"hoc_functions/SinClamp.hoc")   
    #h.xopen(folderhoc) 
    if 'soma' in roi:
        v_stim  = h.Vector()
        stim = h.SinClamp(h.soma[0](0.5))
        v_stim.record(h.soma[0](0.5)._ref_v)        
    else:
        v_stim  = h.Vector()
        D = np.empty((100,2))
        D[:] = np.NaN
        for count,sec in enumerate(h.allsec()):
            D[count,1] = h.distance(sec(1),h.soma[0](0.5))
            D[count,0] = h.distance(sec(0),h.soma[0](0.5))
            if roi not in str(sec):
                D[count,0:2] = np.NaN   
        D = D[0:count+1, :]
    
        idDist = np.where(((D[:,0]<dist) & (D[:,1]>dist)))
        sel     = rd.randrange(len(idDist[0]))
        
        for count,sec in enumerate(h.allsec()):
            if count == idDist[0][sel]:
               #segPart = (dist - D[count, 0])/(D[count, 1]-D[count, 0])
               segPart = (dist - D[count, 0])/sec.L
               #rsec = h.sec(segPart)          
               stim = h.SinClamp(sec(segPart))
               v_stim.record(sec(segPart)._ref_v)

    return stim, v_stim     
