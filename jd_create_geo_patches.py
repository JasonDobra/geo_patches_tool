
from maya import cmds
import random

def setup_patches(face_selection, patch_name):
    
    stored_face_selection=[]
    face_selection_list=[]
    stored_face_selection.append(face_selection)
    
    promptNameWindow()
    patch_name = cmds.promptDialog(query=True, text=True)
    
   
    skin_transform = cmds.listRelatives(face_selection, allParents=True)
    skin_duplicate = cmds.duplicate(skin_transform, n=patch_name)
    skin_duplicate_shape = cmds.listRelatives(type='shape')
    
    for i in range(len(face_selection)):
        split_str=face_selection[i].split('.')
        face_selection_list.append(split_str[1])
      
    cmds.select(cl=True)
    
    cmds.select(skin_duplicate[0]+'.f[*]')
    
    for i in range(len(face_selection)):
        cmds.select(skin_duplicate[0]+'.'+face_selection_list[i],deselect=True)
        
    cmds.delete()
    cmds.select(cl=True)
    
    duplicate_face_list_number = cmds.polyEvaluate(skin_duplicate[0], f=True)
    duplicate_face_list = cmds.filterExpand(skin_duplicate[0] + '.f[{}:{}]'.format(0, duplicate_face_list_number), sm=34)
    
    face_source_sets = cmds.sets(stored_face_selection[0], n=patch_name + '_target_set', t=patch_name + '_target_set')
    face_source_sets = cmds.sets(duplicate_face_list, n=patch_name + '_source_set', t=patch_name + '_source_set')
    
    random_colours(skin_duplicate)
    


def random_colours(obj):
    
    for i in obj:
        shader = cmds.shadingNode('lambert', asShader=True, n='{}{}'.format(i, '_MAT'))
        
        r = [random.random() for i in range(3)]
        
        shading_group = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name='{}{}'.format(i, 'SG'))
        cmds.setAttr((shader + '.color'), r[0], r[1], r[2], type='double3')
        cmds.connectAttr((shader+'.outColor'),(shading_group+'.surfaceShader'),f=1)
        cmds.sets(i, e=1, forceElement=shading_group)

def promptNameWindow():
    
    cmds.promptDialog(
                title='Group Name',
                message='Enter Name:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')
    return

       
if __name__ == '__main__':
    setup_patches(cmds.ls(sl=True), patch_name=None)
