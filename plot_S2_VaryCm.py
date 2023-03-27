###
import os
#import xopen
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
import pickle
import pandas as pd

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

ResultFolder = os.path.join(os.getcwd(),'results/Fig1/')
PlotFolder = os.path.join(os.getcwd(),'Figures/')

ModelName = ['PV'] 
ModelID = [471085845] 

col = ['tab:blue','tab:orange','tab:green','tab:purple']


col = [(0.6350, 0.0780, 0.1840),(0, 0.4470, 0.7410)]

roi = 'dend'
distance = 150
freq = np.append(np.linspace(2,10,5), np.linspace(15,105,19))

fig, axs = plt.subplots(1, 2, dpi=100,constrained_layout=True)#, constrained_layout=True)  

TI_pv = np.empty((1,len(freq)))

for i1, ID in enumerate(ModelID):

    Sname = ResultFolder + str(ID) + '.p'
    data = pickle.load(open(Sname, 'rb'))
    for i2,freq_temp in enumerate(freq):
        TI_pv[i1,i2] = data[(data['distance']==distance) & (data['roi']==roi) & (data['freq']==freq_temp)].ImpAmpSoma.values[0]
   


ResultFolder = os.path.join(os.getcwd(),'results/FigS2/')
ModelID = 472451419
Sname = ResultFolder + str(ModelID) + '.p'
data = pickle.load(open(Sname, 'rb'))

factor = np.linspace(0.1,2,20)
factor = factor[1:10:2]
factor = np.array([0.2,0.5,1])

alphaT = np.linspace(0.1,1,len(factor))

leg = ['Pyramidal low C_m','Pyramidal mid C_m','Pyramidal','PV']

TI = np.empty((len(factor),len(freq)))

for i1,fac in enumerate(factor):
    for i2,freq_temp in enumerate(freq):
        TI[i1,i2] = data[(data['distance']==distance) & (data['roi']==roi) & (data['freq']==freq_temp) & (data['factor']==fac)].ImpAmpSoma.values[0]
   
    axs[0].plot(freq, TI[i1,:],color=col[1], alpha=alphaT[i1],linestyle='-')  

leg[len(factor)] = 'PV'
   
axs[0].plot(freq, TI_pv[0,:],color=col[0],linestyle='-')  
axs[0].set(xlim=(2, 100))
axs[0].spines['right'].set_visible(False)
axs[0].spines['top'].set_visible(False)   
axs[0].set(xlabel='Stimulation Frequency [Hz]',ylabel='Transfer Impedance [M$\Omega$]')
axs[0].set_box_aspect(1)
axs[0].set_yticks(np.arange(0, 400, step=100))    

axs[0].legend(leg, title="Model", fontsize="small", fancybox=True) 

for i1,fac in enumerate(factor):
    axs[1].plot(freq, TI[i1,:]/TI_pv[0,:],color='k', alpha=alphaT[i1],linestyle='-')    
    
axs[1].set(xlim=(2, 100))
axs[1].set(ylim=(0, 3.1))
axs[1].spines['right'].set_visible(False)
axs[1].spines['top'].set_visible(False)   
axs[1].set(xlabel='Stimulation Frequency [Hz]',ylabel='Transfer Impedance (normalized)')    
axs[1].set_box_aspect(1)
axs[1].set_yticks(np.arange(0, 4, step=1))

PlotName = PlotFolder + 'FigS2_TransferImpedance_SinusCurrent_ScanDendCm'
fig.savefig(PlotName + '.svg', format='svg', dpi=200,bbox_inches='tight') 
fig.savefig(PlotName + '.png', format='png', dpi=200,bbox_inches='tight') 
