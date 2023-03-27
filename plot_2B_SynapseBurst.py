###
import os
#import xopen
import numpy as np
import matplotlib.pyplot as plt
import pickle

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

font = {'family':'Arial',
        'weight': 'regular',
        'size': 8}
plt.rc('font',**font)

ResultFolder = os.path.join(os.getcwd(),'results/Fig2/')
PlotFolder = os.path.join(ResultFolder,'Figures/')


ModelName = ['Pyr','PV'] 
ModelID = [472451419,471085845] 

col = [(0.1059,0.6196,0.4667),(0.851, 0.3725, 0.0078),(0, 0.4470, 0.7410),(0.6350, 0.0780, 0.1840)]

roi = 'dend'
dist = 150

Freq    = list(range(5,105,5))
PlotFreq    = [20, 40, 80]
YLim        = [[-88,-75],[-95,-82],[-100, -87]]

TI = [[] for x in range(len(ModelName))]


mosaic = """
        ABCGGHHH
        DEFGGHHH
        """
fig,axs = plt.subplot_mosaic(mosaic, dpi=100,constrained_layout=True)
cnt = 0

from matplotlib.gridspec import GridSpec
cm = 1/2.54
fig = plt.figure(figsize=(17*cm,5*cm),dpi=100,constrained_layout=True)
gs = GridSpec(nrows=2,ncols=5,figure=fig)
fig.tight_layout()
axs[0,0] = fig.add_subplot(gs[0,0])
axs[0,1] = fig.add_subplot(gs[0,1])
axs[0,2] = fig.add_subplot(gs[0,2])
axs[1,0] = fig.add_subplot(gs[1,0])
axs[1,1] = fig.add_subplot(gs[1,1])
axs[1,2] = fig.add_subplot(gs[1,2])

axs[0,3] = fig.add_subplot(gs[:,3])
axs[1,3] = fig.add_subplot(gs[:,4])


for i1, ID in enumerate(ModelID):

    Sname = ResultFolder + str(ID) + '.p'
    data = pickle.load(open(Sname, 'rb'))

    for i2,freq_temp in enumerate(Freq):
        
        TI[i1].append(data[(data['distance']==dist) & (data['roi']==roi) & (data['freq']==freq_temp)].transfer_impedance_freq.values[0])
        
        if i1==0 and freq_temp in PlotFreq:
            y = data[(data['distance']==dist) & (data['roi']==roi) & (data['freq']==freq_temp)].synapse_current.values[0]
            x = data[(data['distance']==dist) & (data['roi']==roi) & (data['freq']==freq_temp)].time.values[0]
    
            axs[0,cnt].plot(x, -y,color=col[0])
            axs[0,cnt].set(xlim=(0,600))
            axs[0,cnt].set(ylim=(0,0.2))        
            axs[0,cnt].spines['right'].set_visible(False)
            axs[0,cnt].spines['top'].set_visible(False)        
            axs[0,cnt].axis('off')
                
            y = data[(data['distance']==dist) & (data['roi']==roi) & (data['freq']==freq_temp)].soma_potential.values[0]
                
            axs[1,cnt].plot(x, y,color=col[1])
            axs[1,cnt].set(xlim=(0,600))
            axs[1,cnt].set(ylim=(-100,-84))                    
            axs[1,cnt].spines['right'].set_visible(False)
            axs[1,cnt].spines['top'].set_visible(False)   
            axs[1,cnt].axis('off')    
            if cnt==2:
                axs[1,cnt].plot([400,400, 500],[-90, -94, -94],'k')
                axs[1,cnt].text(420,-98,'100 ms')
                axs[1,cnt].text(420,-93,'4 mV')
                axs[1,cnt].text(420,-88,'50 pA')
    
            cnt +=1
            
           
    axs[0,3].plot(Freq, TI[i1], color=col[i1+2])    
    axs[0,3].set_box_aspect(1)
    axs[0,3].spines['right'].set_visible(False)
    axs[0,3].spines['top'].set_visible(False)   
    axs[0,3].set(xlabel='Stimulation Frequency [Hz]',ylabel='Transfer Impedance [M$\Omega$]')
    axs[0,3].legend(ModelName, title="Cell-type", fontsize="small", fancybox=True) 
    axs[0,3].set_yticks(np.arange(0, 100000, step=50000))
    axs[0,3].set_xticks(np.arange(0, 150, step=50))
    axs[0,3].set(xlim=(min(Freq), max(Freq)))

    
    
axs[1,3].plot(Freq, np.asarray(TI[0])/np.asarray(TI[1]), color='k')    
axs[1,3].set_box_aspect(1)
axs[1,3].spines['right'].set_visible(False)
axs[1,3].spines['top'].set_visible(False)   
axs[1,3].set(xlabel='Stimulation Frequency [Hz]',ylabel='Transfer Impedance (normalized)')
axs[1,3].set_yticks(np.arange(0, 1.5, step=0.5))
axs[1,3].set_xticks(np.arange(0, 150, step=50))
axs[1,3].set(xlim=(min(Freq), max(Freq)))   
    
PlotName = PlotFolder + 'Fig2_TransferImpedance_Burst'
fig.savefig(PlotName + '.svg', format='svg', dpi=200,bbox_inches='tight') 
fig.savefig(PlotName + '.png', format='png', dpi=200,bbox_inches='tight') 


    

