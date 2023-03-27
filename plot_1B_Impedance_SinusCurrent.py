import os
import numpy as np
import matplotlib.pyplot as plt
import pickle

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

ResultFolder = os.path.join(os.getcwd(),'results/Fig1/')
PlotFolder = os.path.join(ResultFolder,'Figures/')

ModelName = ['Pyr','PV'] 
ModelID = [472451419,471085845] 

col = ['tab:blue','tab:orange','tab:green','tab:purple']


col = [(0.1059,0.6196,0.4667),(0.851, 0.3725, 0.0078),(0, 0.4470, 0.7410),(0.6350, 0.0780, 0.1840)]

roi = 'dend'
distance = 150
freq = np.append(np.linspace(2,10,5), np.linspace(15,105,19))


fig, axs = plt.subplots(1, 3, dpi=100,constrained_layout=True)#, constrained_layout=True)  

TI = np.empty((2,len(freq)))

for i1, ID in enumerate(ModelID):

    Sname = ResultFolder + str(ID) + '.p'
    data = pickle.load(open(Sname, 'rb'))
    for i2,freq_temp in enumerate(freq):
        TI[i1,i2] = data[(data['distance']==distance) & (data['roi']==roi) & (data['freq']==freq_temp)].ImpAmpSoma.values[0]
   
        if (freq_temp==10) and (i1==0):
           x = data[(data['distance']==distance) & (data['roi']==roi) & (data['freq']==freq_temp)].time.values[0]
           y1 = data[(data['distance']==distance) & (data['roi']==roi) & (data['freq']==freq_temp)].InjectedCurrent.values[0]
           y2 = data[(data['distance']==distance) & (data['roi']==roi) & (data['freq']==freq_temp)].VoltageSoma.values[0]
           
           axs[0].plot(x,y1,color=col[0])
           axs[0].set(xlim=(600, 800))#,ylim=(0.06, 0.12))
           axs[0].spines['right'].set_visible(False) 
           axs[0].spines['top'].set_visible(False)   
           axs[0].set_ylabel('Injected Current [nA]', color=col[0])
           axs[0].set_xlabel('Time [ms]')
           axs[0].tick_params(axis='y', labelcolor=col[0])
           axs[0].set(ylim=(-0.01, 0.11))
           
           axs[0].set_yticks(np.arange(-0, 0.15, step=0.1))
           axs[0].set_box_aspect(1)
          
           
           ax2 = axs[0].twinx()  # instantiate a second axes that shares the same x-axis
           ax2.plot(x,y2,color=col[1])
           ax2.set(ylim=(-92, -78))
           ax2.set_yticks(np.arange(-90, -70, step=10))
           ax2.set_xticks(np.arange(600, 900, step=100))

           ax2.set_ylabel('Somatic Potential [mV]', color=col[1])
           ax2.tick_params(axis='y', labelcolor=col[1])
           ax2.spines['top'].set_visible(False)      
           ax2.set_box_aspect(1)   
   
    axs[1].plot(freq, TI[i1,:],color=col[i1+2],linestyle='-')  
    
axs[1].set(xlim=(2, 100))
axs[1].spines['right'].set_visible(False)
axs[1].spines['top'].set_visible(False)   
axs[1].set(xlabel='Stimulation Frequency [Hz]',ylabel='Transfer Impedance [M$\Omega$]')
axs[1].set_box_aspect(1)
axs[1].set_yticks(np.arange(0, 300, step=100))

#for i1, ID in enumerate(ModelID):
axs[2].plot(freq, TI[0,:]/TI[1,:],color='k',linestyle='-')    
axs[2].set(xlim=(2, 100))
axs[2].set(ylim=(0, 1.3))
axs[2].spines['right'].set_visible(False)
axs[2].spines['top'].set_visible(False)   
axs[2].set(xlabel='Stimulation Frequency [Hz]',ylabel='Transfer Impedance (normalized)')    
axs[2].set_box_aspect(1)
axs[2].set_yticks(np.arange(0, 1.5, step=0.5))

PlotName = PlotFolder + 'Fig1_TransferImpedance_SinusCurrent'
fig.savefig(PlotName + '.svg', format='svg', dpi=200,bbox_inches='tight') 
fig.savefig(PlotName + '.png', format='png', dpi=200,bbox_inches='tight') 



