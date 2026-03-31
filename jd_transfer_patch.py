from maya import cmds
import sys

def transfer_patch_skinning(selection):
    
    print(len(selection))
    
    if len(selection) < 2:
        
        sys.stdout.write('Error: Please select one source and target object to proceed')    
        
    else:
        selection_name = selection[0]
        
        source = selection_name + '_source_set'
        target = selection_name + '_target_set'
        
        cmds.select(source, r=1)
        cmds.select(target, add=1)

transfer_patch_skinning(cmds.ls(sl=True))
