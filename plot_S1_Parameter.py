###
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
import scipy.io

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

font = {'family':'Arial',
        'weight': 'regular',
        'size': 8}
plt.rc('font',**font)

DataFolder = os.path.join(os.getcwd(),'data/')
SaveFolder = os.path.join(os.getcwd(),'results/FigS1/')
PlotFolder = os.path.join(os.getcwd(),'Figures/')


ModelName = ['Pyr','PV'] 
ModelID = [472451419,471085845] 
LGN_Freq = 10

ExpData = scipy.io.loadmat(DataFolder  + 'LEDPPC.mat')
FittedData = pickle.load(open(SaveFolder+'1_InputSpikes_10Hz.p', 'rb'))


fig, axs = plt.subplots(2, 4, dpi=100,constrained_layout=True)#, constrained_layout=True)  
axs[0,0].plot(ExpData['Freq'][0],ExpData['PPCspectraMean'][0,0][0],color = 'k')
axs[0,0].plot(FittedData['PPCfreq'][0],FittedData['PPCfit'][0][0],color = (0.851, 0.3725, 0.0078))
axs[0,0].set_box_aspect(1)
axs[0,0].spines['right'].set_visible(False)
axs[0,0].spines['top'].set_visible(False)   
axs[0,0].set(xlabel='Frequency [Hz]',ylabel='PPC')
axs[0,0].legend(['LGN-LGN','Inhomo. - Inhomo. '], title="Spike - sLFP", fontsize="small", fancybox=True) 
axs[0,0].set_yticks(np.arange(0, 0.15, step=0.1))
axs[0,0].set_xticks(np.arange(0, 150, step=50))
axs[0,0].set(ylim=(-0.001, 0.15))
axs[0,0].set(xlim=(1, 100))

for i1, ID in enumerate(ModelID):
    SaveName = SaveFolder + ModelName[i1] +'_'+ str(ID)+'_'+str(LGN_Freq)+'Hz'   
    data = pickle.load(open(SaveName, 'rb'))

    if i1==1:
        pcm = axs[0,i1+1].pcolormesh(data['LGNSynNum'][0], data['LocalSynNum'][0][5:], data['PPCpeak'][0].transpose()[:][5:], vmin=0, vmax=0.2)
        axs[0,i1+1].set(xlabel='# Inhomogeneous Poisson Inputs')
        axs[0,i1+1].set_title(ModelName[i1])        
        fig.colorbar(pcm, ax=axs[0,i1+1], shrink=0.4, ticks=[0, 0.1, 0.2],label='PPC')
        
        pcm2 = axs[1,i1+1].pcolormesh(data['LGNSynNum'][0], data['LocalSynNum'][0][5:], data['FRmean'][0].transpose()[:][5:], vmin=0, vmax=50)
        axs[1,i1+1].set(xlabel='# Inhomogeneous Poisson Inputs')
        fig.colorbar(pcm2, ax=axs[1,i1+1], shrink=0.4, ticks=[0, 25, 50],label='FR [Hz]')

    else:
        pcm = axs[0,i1+1].pcolormesh(data['LGNSynNum'][0], data['LocalSynNum'][0][10:], data['PPCpeak'][0].transpose()[:][10:], vmin=0, vmax=0.2)
        axs[0,i1+1].set(ylabel='# Homogeneous Poisson Inputs')
        axs[0,i1+1].set_title(ModelName[i1])

        pcm2 = axs[1,i1+1].pcolormesh(data['LGNSynNum'][0], data['LocalSynNum'][0][10:], data['FRmean'][0].transpose()[:][10:], vmin=0, vmax=10)
        axs[1,i1+1].set(ylabel='# Homogeneous Poisson Inputs')
        fig.colorbar(pcm2, ax=axs[1,i1+1], shrink=0.4, ticks=[0, 5, 10],label='FR [Hz]')


    axs[0,i1+1].set_box_aspect(1)
    axs[0,i1+1].spines['right'].set_visible(False)
    axs[0,i1+1].spines['top'].set_visible(False)
    axs[0,i1+1].set_xticks(np.arange(5, 15, step=5))
   
    axs[1,i1+1].set_box_aspect(1)
    axs[1,i1+1].spines['right'].set_visible(False)
    axs[1,i1+1].spines['top'].set_visible(False)
    axs[1,i1+1].set_xticks(np.arange(5, 15, step=5))    
   
    
 
StimFreq = [10,20,40,60,80]
PPCpeak = [None]*len(StimFreq)

for i1,stim in enumerate(StimFreq):
    FittedData = pickle.load(open(SaveFolder+'1_InputSpikes_' +str(stim)+ 'Hz.p', 'rb'))
    idF = np.argmin(abs(FittedData['PPCfreq'][0]-FittedData['stimFreq'][0]))
    PPCpeak[i1] = FittedData['PPCfit'][0][i1][idF]

axs[0,3].plot(ExpData['StimFreq'],ExpData['PPC_Mean'][0,:],color = 'k')
axs[0,3].plot(StimFreq,PPCpeak,color = (0.851, 0.3725, 0.0078))   
axs[0,3].set_box_aspect(1)
axs[0,3].spines['right'].set_visible(False)
axs[0,3].spines['top'].set_visible(False)   
axs[0,3].set(xlabel='Stimulation Frequency [Hz]',ylabel='PPC')
axs[0,3].legend(['LGN-LGN','Inhomo. - Inhomo. '], title="Spike - sLFP", fontsize="small", fancybox=True) 
axs[0,3].set_yticks(np.arange(0, 3, step=0.1))
axs[0,3].set_xticks(np.arange(20, 100, step=20))
axs[0,3].set(ylim=(-0.001, 0.2))
axs[0,3].set(xlim=(10, 80))

PlotName = PlotFolder + 'FigS1_PoissonSynapse_parameters_v2'
fig.savefig(PlotName + '.svg', format='svg', dpi=200,bbox_inches='tight') 
fig.savefig(PlotName + '.png', format='png', dpi=200,bbox_inches='tight')     
   