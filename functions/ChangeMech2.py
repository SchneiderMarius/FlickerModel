import glob, os, json

def ChangeMech(ModelFolder,ID,IDsave,modify,par):
    filenameLoad = glob.glob(ModelFolder+ID+"/*_fit.json")
    filenameSave = glob.glob(ModelFolder+IDsave+"/*_fit.json")

    with open(filenameLoad[0], 'r') as f:
        data = json.load(f)

    for ind,i1 in enumerate(modify[0]):
        for i2 in modify[2][ind]:
    #        data[modify[0]][0][modify[1]][i] = data[modify[0]][0][modify[1]][i]*factor
            data[modify[0][ind]][0][modify[1][ind]][i2][modify[3][ind]] = par[ind]

 #   os.remove(filenameLoad[0])
    with open(filenameSave[0], 'w') as f:
        json.dump(data, f, indent=4)