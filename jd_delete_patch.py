from maya import cmds 

def delete_patches(patches):
    
    for patch in patches:
        
        cmds.delete(f'{patch}_target_set')
        cmds.delete(f'{patch}_source_set')
        cmds.delete(f'{patch}_MAT')
        cmds.delete(patch)
    
if __name__ == "__main__":
    delete_patches(cmds.ls(sl=True))

  
