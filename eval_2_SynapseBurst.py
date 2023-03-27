import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
import pickle
import pandas as pd

from InitModel import InitModel
from functions.getSection import getSection
from functions.SynImpedance import SynImpedance

ResultFolder = os.path.join(os.getcwd(),'results/Fig2/')
PlotFolder = os.path.join(ResultFolder,'plots/')


if not os.path.exists(PlotFolder):
    os.makedirs(PlotFolder)

ModelName = ['Pyr','PV'] 
ModelID = [472451419,471085845] 

dist    = [50,100,150]
roi     = ['dend','dend','dend']
Freq    = list(range(5,105,5))
plt.rcParams['font.size'] = '6'

Plt_Freq = [20, 40, 80]

for i1, ID in enumerate(ModelID):
    h, manifest, utils, description = InitModel(ID)
    
    df      = pd.DataFrame()
    sName   = ResultFolder + str(ID)
    
    site, dist_temp, roi_temp = getSection(h,roi,dist)

    for i2, site_temp in enumerate(site):
        fig, axs = plt.subplots(4, len(Plt_Freq))#, constrained_layout=True)
        fig.tight_layout()
        
        count = 0
        for i3,freq_temp in enumerate(Freq):

            stim = h.NetStim()                      # Make a new stimulator
            stim.number = 9                       # number of spike events in NetStin
            stim.interval = 1/freq_temp*1000        # Timing of first spike [ms]
            stim.start = 9                          # Timing of first spike [ms]
            
            syn = h.Exp2Syn(site_temp)              # attach synapse to a segment in the cell
            syn.tau1 = 1
            syn.tau2 = 3            
            
            ncstim = h.NetCon(stim, syn)            # connect netstim with synapes
            ncstim.delay = 1                        # delay of synaptic event
            ncstim.weight[0] = 0.004                # NetCon weight is a vector.
            
            v_stim  = h.Vector()                    # set up recording vector
            v_stim.record(site_temp._ref_v)         # location of recording
            
            v_soma  = h.Vector()                    # set up recording vector
            v_soma.record(h.soma[0](0.5)._ref_v)    # location of recording
            
            timeVec     = h.Vector()
            timeVec.record(h._ref_t)                # record time
            
            i_syn     = h.Vector()                  
            i_syn.record(syn._ref_i)                # record synaptic current    
            
            h.tstop = 1000
            h.run()
            
            TI, TI_freq, faxis, v_soma_S, v_syn_S, i_syn_S = SynImpedance(v_soma, i_syn, v_stim, timeVec, freq_temp)
            
            
            R_temp = {'distance':dist_temp[i2],'roi':roi_temp[i2],'freq':freq_temp,'synapse_current':[np.array(i_syn)],
                      'soma_potential':[np.array(v_soma)],'syn_potential':[np.array(v_stim)],'time':[np.array(timeVec)],'model_id':ModelID[i1],
                      'model_name':ModelName[i1],'transfer_impedance':[TI],'transfer_impedance_freq':
                          [TI_freq],'impedance_freq':[faxis],'soma_potential_fft':[v_soma_S],'syn_potential_fft':[v_syn_S],'synapse_current_fft':[i_syn_S]
                          }
            df_temp = pd.DataFrame(data=R_temp)
            df = df.append(df_temp)

            if freq_temp in Plt_Freq:
                axs[0, count].plot(timeVec, -i_syn)
                axs[0, count].set(xlabel='time [ms]', ylabel='current [pA]')
                axs[0, count].spines['right'].set_visible(False)
                axs[0, count].spines['top'].set_visible(False)
                axs[0, count].set_title(str(freq_temp)+'Hz burst at '+str(dist_temp[i2])+'ym')            
                axs[0, count].set_xlim([0, 600])
                
                
                axs[1, count].plot(timeVec, v_soma)
                axs[1, count].set(xlabel='time [ms]', ylabel='voltage [mV]')
                axs[1, count].spines['right'].set_visible(False)
                axs[1, count].spines['top'].set_visible(False)
                if i3==round(len(Plt_Freq)/2):
                    axs[1, count].set_title('voltage output at soma')            
                axs[1, count].set_xlim([0, 600])
                
                axs[2, count].plot(faxis, i_syn_S)
                axs[2, count].set(xlabel='Frequency [Hz]', ylabel='power [pA**2]')
                axs[2,count].spines['right'].set_visible(False)
                axs[2,count].spines['top'].set_visible(False)                 
                axs[2,count].set(xlim=(2,100))
                if i3==round(len(Plt_Freq)/2):
                    axs[2, i3].set_title('input at '+str(dist_temp[i2])+'ym')
                
                axs[3,count].plot(faxis, v_soma_S)
                axs[3,count].set(xlabel='Frequency [Hz]', ylabel='power [mV**2]')
                axs[3,count].set(xlim=(2,100))
                if i3==round(len(Plt_Freq)/2):
                    axs[1, i3].set_title('voltage output at soma')     
                
                axs[3,count].spines['right'].set_visible(False)
                axs[3,count].spines['top'].set_visible(False)
                count +=1
                
        PlotName = PlotFolder+ str(ID)+'_'+ roi_temp[i2] +'_'+ str(dist_temp[i2])
            
        plt.tight_layout()
        plt.show()
        fig.savefig(PlotName, dpi=200)
        fig.savefig(PlotName, format='pdf', dpi=200)  


    Sname = ResultFolder +  str(ID) + '.p'
    pickle.dump(df, open(Sname, "wb"))  # save it into a file named save.p

