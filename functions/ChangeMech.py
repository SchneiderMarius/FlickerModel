import glob, os, json

def ChangeMech(ModelFolder,ID,IDsave,modify,factor):
    filenameLoad = glob.glob(ModelFolder+ID+"/*_fit.json")
    filenameSave = glob.glob(ModelFolder+IDsave+"/*_fit.json")

    with open(filenameLoad[0], 'r') as f:
        data = json.load(f)

    for i in modify[2]:
#        data[modify[0]][0][modify[1]][i] = data[modify[0]][0][modify[1]][i]*factor
        data[modify[0]][0][modify[1]][i][modify[3]] = data[modify[0]][0][modify[1]][i][modify[3]]*factor

 #   os.remove(filenameLoad[0])
    with open(filenameSave[0], 'w') as f:
        json.dump(data, f, indent=4)