import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from functions.InitModel import InitModel
from functions.SinClampROI import SinClampROI
from functions.ImpedancePhase import ImpedancePhase

ResultFolder = os.path.join(os.getcwd(),'results/Fig1')
PlotFolder = os.path.join(ResultFolder,'plots')

if not os.path.exists(PlotFolder):
    os.makedirs(PlotFolder)

ModelName = ['Pyr','PV'] 
ModelID = [472451419,471085845] 

roi = ['dend','dend','dend']
dist = [50,100,150]
freq = np.append(np.linspace(2,10,5), np.linspace(15,105,19))

ImpPhaseSoma,ImpAmpSoma         = np.empty((len(dist),len(freq))),np.empty((len(dist),len(freq)))
ImpPhaseLocal,ImpAmpLocal       = np.empty((len(dist),len(freq))),np.empty((len(dist),len(freq)))
fout                            = np.empty((len(dist),len(freq)))
ImpPhaseSoma[:],ImpAmpSoma[:]   = np.NaN,np.NaN
ImpPhaseLocal[:],ImpAmpLocal[:] = np.NaN,np.NaN
fout[:]                         = np.NaN

for i1, ID in enumerate(ModelID):
    h, manifest, utils, description = InitModel(ID)
    
    df      = pd.DataFrame()
    Sname   = ResultFolder + str(ID) + '.p'

    for ct1, v1 in enumerate(dist):
        
        h_temp = h
        
        stim, v_stim = SinClampROI(h_temp, roi[ct1], v1)
    
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
    
            R_temp = {'distance':v1,'roi':roi[ct1],'freq':v2,'ImpPhaseSoma':ImpPhaseSoma[ct1,ct2],
                      'ImpAmpSoma':ImpAmpSoma[ct1,ct2],'fout':fout[ct1,ct2],'ImpPhaseLocal':ImpPhaseLocal[ct1,ct2],'ImpAmpLocal':ImpAmpLocal[ct1,ct2],'model_id':ModelID[i1],
                      'model_name':ModelName[i1],'VoltageSoma':[np.array(v_soma)],'InjectedCurrent':[np.array(injCurr)],
                      'time':[np.array(timeVec)]}
            
            df_temp = pd.DataFrame(data=R_temp)
            df = df.append(df_temp)
    pickle.dump(df, open(Sname, "wb"))

    PlotName = os.path.join(PlotFolder,ModelName[i1])
    
    col = [(217/255,95/255,2/255), (27/255,158/255,119/255)]
    leg = ['dend: 50','dend:100','dend: 150']
    
    
    plt.plot(timeVec,v_soma)
            
    plt.plot(freq,ImpAmpSoma[0,:], color=col[1], alpha=1)
    plt.plot(freq,ImpAmpSoma[1,:], color=col[1], alpha=0.6)
    plt.plot(freq,ImpAmpSoma[2,:], color=col[1], alpha=0.2)

    plt.legend(leg, title="Distance to soma [$\mu$m]", fontsize="small", fancybox=True)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Transfer impedance [M$\Omega$]')
    
    plt.savefig(PlotName)
    plt.savefig(PlotName, format='pdf')
    
