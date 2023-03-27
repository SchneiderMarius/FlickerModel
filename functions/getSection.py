def getSection(h,roi,dist):
    import numpy as np
    import random as rd    
    
    roi_out     = []
    dist_out    = []
    site_out    = []    
    
    for ct1, roiL in enumerate(roi): 
        
        if 'soma' in roiL:
            site_out.append(h.soma[0](0.5))
            dist_out.append(dist[ct1])
            roi_out.append(roiL)            
        else:        
        
            D = np.empty((100,2))
            D[:] = np.NaN
            for count,sec in enumerate(h.allsec()):
                D[count,1] = h.distance(sec(1),h.soma[0](0.5))
                D[count,0] = h.distance(sec(0),h.soma[0](0.5))
                if roiL not in str(sec):
                    D[count,0:2] = np.NaN   
            D = D[0:count+1, :]
            
            idDist  = np.where(((D[:,0]<dist[ct1]) & (D[:,1]>dist[ct1])))
            
            if len(idDist[0])>0:
                sel     = rd.randrange(len(idDist[0]))
                
                for count,sec in enumerate(h.allsec()):
                    if count == idDist[0][sel]:
                        segPart = (dist[ct1] - D[count, 0])/sec.L
                
                        site_out.append(sec(segPart))
                        dist_out.append(dist[ct1])
                        roi_out.append(roiL)

    return site_out, dist_out, roi_out

