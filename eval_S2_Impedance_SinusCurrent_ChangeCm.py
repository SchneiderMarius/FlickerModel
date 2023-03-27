import os
#import xopen
import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from InitModel import *
from functions.SinClampROI import SinClampROI
from functions.ImpedancePhase import ImpedancePhase
from functions.ChangeMech import ChangeMech

ModelFolder = os.path.join(os.getcwd(),'CellModels/')
ResultFolder = os.path.join(os.getcwd(),'results/FigS2/')
PlotFolder = os.path.join(os.getcwd(),'results/Fig1/plots')


if not os.path.exists(PlotFolder):
    os.makedirs(PlotFolder)

ModelName = ['Pyr'] 
ModelID = [472451419] 

roi = 'dend'
dist = 150
freq = np.append(np.linspace(2,10,5), np.linspace(15,105,19))

modify = ['passive','cm',[2,3],'cm']
factor = np.array([0.2,0.5,1])

ImpPhaseSoma,ImpAmpSoma         = np.empty((len(factor),len(freq))),np.empty((len(factor),len(freq)))
ImpPhaseLocal,ImpAmpLocal       = np.empty((len(factor),len(freq))),np.empty((len(factor),len(freq)))
fout                            = np.empty((len(factor),len(freq)))
ImpPhaseSoma[:],ImpAmpSoma[:]   = np.NaN,np.NaN
ImpPhaseLocal[:],ImpAmpLocal[:] = np.NaN,np.NaN
fout[:]                         = np.NaN


## scale dendritic capacity of Pyramidal model

for i1, ID in enumerate(ModelID):
    
    df      = pd.DataFrame()
    Sname   = ResultFolder + str(ID) + '.p'   
    
    for ct1,fac in enumerate(factor):
        
        ChangeMech(ModelFolder,str(ID),str(ID)+'_changeCM',modify,fac)
        
        h, manifest, utils, description = InitModel(str(ID)+'_changeCM')
            
        h_temp = h
        
        stim, v_stim = SinClampROI(h_temp, roi, dist)
    
        for ct2, v2 in enumerate(freq):
            setattr(stim, 'del', 200)
            setattr(stim, 'dur', 1000)
            setattr(stim, 'pkamp', 0.1)
            setattr(stim, 'freq', v2)
            setattr(stim, 'phase', 0)
            setattr(stim, 'bias', 0)
        
            v_soma  = h_temp.Vector()
            injCurr = h_temp.Vector()
            timeVec = h_temp.Vector()
            
            v_soma.record(h_temp.soma[0](0.5)._ref_v)
            injCurr.record(stim._ref_i)
            timeVec.record(h_temp._ref_t)
            
            junction_potential = description.data['fitting'][0]['junction_potential']
            
            h_temp.tstop = 2200
            h_temp.run()

            ImpPhaseSoma[ct1,ct2], ImpAmpSoma[ct1,ct2],fout[ct1,ct2],ImpPhaseLocal[ct1,ct2], ImpAmpLocal[ct1,ct2] \
            = ImpedancePhase(injCurr,v_stim,v_soma,timeVec)
    
            R_temp = {'factor':fac,'distance':dist,'roi':roi,'freq':v2,'ImpPhaseSoma':ImpPhaseSoma[ct1,ct2],
                      'ImpAmpSoma':ImpAmpSoma[ct1,ct2],'fout':fout[ct1,ct2],'ImpPhaseLocal':ImpPhaseLocal[ct1,ct2],'ImpAmpLocal':ImpAmpLocal[ct1,ct2],'model_id':ModelID[i1],
                      'model_name':ModelName[i1],'VoltageSoma':[np.array(v_soma)],'InjectedCurrent':[np.array(injCurr)],
                      'time':[np.array(timeVec)]}
            
            df_temp = pd.DataFrame(data=R_temp)
            df = df.append(df_temp)
            
    pickle.dump(df, open(Sname, "wb"))
    