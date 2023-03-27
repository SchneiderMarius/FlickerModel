def InitModel(fname):
    folder = '/mnt/hpc/home/schneiderm/Projects/12B_Neuron/'
    import shutil
    import os
    from allensdk.model.biophys_sim.config import Config
    from allensdk.model.biophysical.utils import Utils
    #from allensdk.core.dat_utilities import DatUtilities
    from allensdk.api.queries.biophysical_api import BiophysicalApi
        
    folderhoc = os.path.join(folder,"hoc_functions/fixnseg.hoc")   
    ModelFolder = os.path.join(folder,'CellModels',str(fname))
#    ModelFolder = os.path.join(folder,'CellModels')
    
    # if ~os.path.isdir(ModelFolder):
    #     print(ModelFolder)
    #     os.makedirs(ModelFolder)
    #     # copy file into new dir
    #     SDir = os.path.join(folder,'functions')
    #     file_names = os.listdir(SDir)
    #     for file_name in file_names:
    #         shutil.move(os.path.join(SDir, file_name), ModelFolder)    

    # if not os.path.isdir(ModelFolder):
    #     bp = BiophysicalApi('http://api.brain-map.org')
    #     bp.cache_stimulus = False  # don't want to download the large stimulus NWB file
    #     bp.cache_data(fname, working_directory=ModelFolder)
    #     SDir = os.path.join(folder, 'functions')
    #     file_names = os.listdir(SDir)
    #     for file_name in file_names:
    #         # original
    #         #shutil.copy(os.path.join(SDir, file_name), ModelFolder)
    #         # changed for VecStim
    #         ModelFolderMod = os.path.join(ModelFolder,'modfiles')
    #         #shutil.copy(os.path.join(SDir, file_name), ModelFolder)
    #         shutil.copy(os.path.join(SDir, file_name), ModelFolderMod)
            
    #     os.chdir(ModelFolder)
    #     os.system('nrnivmodl modfiles')
    # else:
    os.chdir(ModelFolder)
        
        
    import os
    if 'DISPLAY' in os.environ:
        del os.environ['DISPLAY']            

#    description = Config().load('manifest_'+str(fname)+'.json')
    description = Config().load('manifest.json')
    utils = Utils(description)
    h = utils.h

    # configure model
    manifest = description.manifest
    morphology_path = description.manifest.get_path('MORPHOLOGY')
    utils.generate_morphology(morphology_path.encode('ascii', 'ignore'))
    utils.load_cell_parameters()

    h.xopen(folderhoc)
    h.geom_nseg()   


    return h, manifest, utils, description

