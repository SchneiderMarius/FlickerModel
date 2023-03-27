import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

font = {'family':'Arial',
        'weight': 'regular',
        'size': 8}
plt.rc('font',**font)


PlotFolder = os.path.join(os.getcwd(),'Figures/')
Folder1 = os.path.join(os.getcwd(),'results/FigS3/')
Folder2 = os.path.join(os.getcwd(),'results/Fig3/')

ModelName = ['Pyr','PV'] 
ModelID = [472451419,471085845] 

LGN_ROI = ['dend']
LGN_SynNum = [6,8]
LGN_Freq = [10, 20, 40, 60]
Local_ROI = ['dend', 'apic']
Local_SynNum = [60,43]
Local_Freq = 0
syn_weight = [0.000012,0.000012]

Input = ['1_InputSpikes_HomogeneousPP.p','1_InputSpikes_10Hz.p']
name = ['Homogeneous Poisson', 'Inhomogeneous Poisson']


col = [(0, 0.4470, 0.7410),(0.6350, 0.0780, 0.1840)]

leg = ['PV','Pyramidal low C_m','Pyramidal mid C_m','Pyramidal']

## Change Only Na

alphaT = np.linspace(0.1,1,5)

fig, axs = plt.subplots(1, 2, dpi=100,constrained_layout=True)#, constrained_layout=True)  


PPCfit  = [None]*len(LGN_SynNum) 
for iModel, ID_temp in enumerate(ModelID):
    ID = str(ID_temp) + '_changeCM_scan'

    if iModel==0:
        
        SaveName = Folder1 + ID + '_LGNsyn_' + str(LGN_SynNum[iModel]) + '_Localsyn_' + str(Local_SynNum[iModel])
        Result          = pickle.load(open(SaveName, "rb")) 
        
        PPCpeak = Result[1]
        factor = Result[4]
    else:
        SaveName = Folder2 + ModelName[iModel] + '_LGNsyn_' + str(LGN_SynNum[iModel]) + '_Localsyn_' + str(Local_SynNum[iModel])
        Result          = pickle.load(open(SaveName, "rb")) 
        StimFreq        = Result['StimFreq'].values[0]
        PPCfit[iModel]  = Result['PPCpeak'].values[0]
        axs[0].plot(Result['StimFreq'].values[0],Result['PPCpeak'].values[0],color=col[iModel])
        axs[0].spines['right'].set_visible(False) 
        axs[0].spines['top'].set_visible(False)      
        axs[0].set_box_aspect(1)    
        axs[0].set_yticks(np.arange(0, 0.06, step=0.02))
        axs[0].set_xticks(np.arange(20, 80, step=20))
        axs[0].set(xlim=(10, 60))   
        axs[0].set_ylabel('PPC')
        
        

for i in range(len(factor)):
        axs[0].plot(Result['StimFreq'].values[0],PPCpeak[i],color=col[0], alpha=alphaT[i])
        axs[1].plot(Result['StimFreq'].values[0],PPCpeak[i]/Result['PPCpeak'].values[0],color='k', alpha=alphaT[i])

axs[0].legend(leg, title="Model", fontsize="small", fancybox=True) 
    
axs[1].spines['right'].set_visible(False) 
axs[1].spines['top'].set_visible(False)   
axs[1].set_box_aspect(1) 
axs[1].set_yticks(np.arange(0, 2, step=0.5))
axs[1].set_xticks(np.arange(20, 80, step=20))
axs[1].set_ylabel('PPC normalized')
axs[1].set_xlabel('Inhomogeneous Poissson Peak Frequency [Hz]')        
axs[1].set(xlim=(10, 60))   
    
PlotName = PlotFolder + 'FigS3_PoissonSynapse_ScanDendCm'
fig.savefig(PlotName + '.svg', format='svg', dpi=200,bbox_inches='tight') 
fig.savefig(PlotName + '.png', format='png', dpi=200,bbox_inches='tight') 

       
        
        