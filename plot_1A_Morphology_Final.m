clear all

cd /mnt/hpc/home/schneiderm/Projects/12C_Neuron

addpath(genpath('/mnt/hpc/home/schneiderm/Tools/treestoolbox-master'));

Folder = fullfile(cd,'CellModels/');

ModelName = {'Pyr','PV'} 
ModelID = [472451419,471085845] 

rcolor = [0 0 0];
col = [[0 0 0];[1 0 0];[0, 0.4470, 0.7410];[0.8500, 0.3250, 0.0980];[0 0.6 0.3]	];

fonts   = 8;
lwidth  = 0.8;
tickl   = 0.025;
alph    = 0.2;
foi     = [6 80];  
    figure
hold on;
for cnt1 = 1 : length(ModelID)

    dat     = dir(fullfile(fullfile(Folder,num2str(ModelID(cnt1))),'*swc'));
    tree    = load_tree(fullfile(dat(1).folder,dat(1).name));

    if iscell(tree)
        tree=tree{1};
    end
    if cnt1 ==1
        tree.X = tree.X-500;
        tree = rot_tree(tree, [0 0 180]);
        tree.Y = tree.Y+600;
    end
    
%    figure
    hp               = plot_tree   (tree, rcolor, [], [], [], '-b1');
    plot([100 200],[0 0 ],'-k')
    set              (hp,'edgecolor',rcolor,'linewidth',0.25);
    axis             image off
    set              (gca,'ActivePositionProperty','position','position',[0.2 0.2 0.75 0.75]);
    set(gcf, 'Units', 'centimeters', 'Position', [2,2,5.2,5], 'Renderer', 'painters');

end
print(gcf,fullfile(cd,'Figures','Fig1A_morphology.pdf'),'-dpdf') % then print it
close all    
