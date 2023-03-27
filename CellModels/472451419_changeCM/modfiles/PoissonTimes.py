import numpy as np

def PoissonTimes(modFunction,t):
    dt          = t[1]-t[0]
    avgRate     = (modFunction(t) + modFunction(t+dt))/2
    avgProp     = 1 - np.exp(-avgRate*dt)
    randNum     = np.random.uniform(size=t.shape[0])
    
    return t[avgProp>=randNum].tolist()

    
    
