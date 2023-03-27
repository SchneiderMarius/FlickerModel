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

DataFolder = os.path.join(os.getcwd(),'data/')
PlotFolder = os.path.join(os.getcwd(),'Figures/')
Folder = os.path.join(os.getcwd(),'results/Fig3/')

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


col = [(0.1,0.1,0.1),(0.851, 0.3725, 0.0078),(0, 0.4470, 0.7410),(0.6350, 0.0780, 0.1840)]

axs = [None]*4

from matplotlib.gridspec import GridSpec
cm = 1/2.54
fig = plt.figure(figsize=(12*cm,5*cm),dpi=100,constrained_layout=True)
gs = GridSpec(nrows=2,ncols=3,figure=fig)
fig.tight_layout()
axs[0] = fig.add_subplot(gs[0,0])
axs[1] = fig.add_subplot(gs[1,0])
axs[2] = fig.add_subplot(gs[:,1])
axs[3] = fig.add_subplot(gs[:,2])


for ct1, In in enumerate(Input):
    data = pickle.load(open(Folder+In, 'rb'))
    
    SP = [None]*200
    for ct2 in range(200):
        SP[ct2] = data.SpikeTimes.values[0][ct2][0]
        
    axs[ct1].eventplot(SP,color=col[ct1],linelengths=0.4)
    axs[ct1].spines['right'].set_visible(False)        
    axs[ct1].spines['top'].set_visible(False)
    if ct1==1:
        axs[ct1].set(xlabel='Time [s]',ylabel='Trials')
    else:
        axs[ct1].set(ylabel='Trials')

    axs[ct1].set_xticks(np.arange(0, 3, step=1))
    axs[ct1].set_yticks(np.arange(0, 400, step=200))
    axs[ct1].set(xlim=(0,2))    
    axs[ct1].set_xticks(np.arange(0, 3, step=1))


PPCfit  = [None]*len(LGN_SynNum) 
for iModel, Model in enumerate(ModelName):
    SaveName = Folder + Model + '_LGNsyn_' + str(LGN_SynNum[iModel]) + '_Localsyn_' + str(Local_SynNum[iModel])
    
    Result          = pickle.load(open(SaveName, "rb")) 
    StimFreq        = Result['StimFreq'].values[0]
    PPCfit[iModel]  = Result['PPCpeak'].values[0]
                   
    axs[2].plot(Result['StimFreq'].values[0],Result['PPCpeak'].values[0],color=col[iModel+2])
    axs[2].spines['right'].set_visible(False) 
    axs[2].spines['top'].set_visible(False)      
    axs[2].set_box_aspect(1)    
    axs[2].set_yticks(np.arange(0, 0.06, step=0.02))
    axs[2].set_xticks(np.arange(20, 80, step=20))
    axs[2].set(xlim=(10, 60))   
 


axs[3].plot(Result['StimFreq'].values[0],PPCfit[0]/PPCfit[1],color='k')
axs[3].spines['right'].set_visible(False) 
axs[3].spines['top'].set_visible(False)   
axs[3].set_box_aspect(1) 
axs[3].set_yticks(np.arange(0, 1.5, step=0.5))
axs[3].set_xticks(np.arange(20, 80, step=20))
axs[3].set(xlim=(10, 60))   
axs[3].set_ylabel('PPC normalized')
axs[3].set_xlabel('Inhomogeneous Poissson Peak Frequency [Hz]')
  
axs[2].set_ylabel('PPC') 
PlotName = PlotFolder + 'Fig3'
fig.savefig(PlotName + '.svg', format='svg', dpi=200,bbox_inches='tight') 
fig.savefig(PlotName + '.png', format='png', dpi=200,bbox_inches='tight') 

    
    
    
    