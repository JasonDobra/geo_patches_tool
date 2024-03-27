import maya.cmds as mc 

import random

def setup_mesh_patches(face_selection, patch_name):
    
    result = promptNameWindow()
    
    if result == 'OK':
        
        patch_name = mc.promptDialog(query=True, text=True)
        create_mesh_patch(patch_name, face_selection)
       
def create_mesh_patch(patch_name, face_selection):
    
    stored_face_selection=[]
    face_selection_list=[]
    
    stored_face_selection.append(face_selection)
    #face_source_sets = mc.sets(stored_face_selection[0], n=patch_name + '_target_set', t=patch_name + '_target_set')
        
    skin_transform = mc.listRelatives(face_selection, allParents=True)
    
    skin_duplicate = mc.duplicate(skin_transform, n=patch_name)
    mc.parent(skin_duplicate, world=True)
    
    skin_duplicate_shape = mc.listRelatives(type='shape')
    
    for i in range(len(face_selection)):
        split_str=face_selection[i].split('.')
        face_selection_list.append(split_str[1])
      
    mc.select(cl=True)
    
    mc.select(skin_duplicate[0]+'.f[*]')
    
    for i in range(len(face_selection)):
        mc.select(skin_duplicate[0]+'.'+face_selection_list[i],deselect=True)
        
    mc.delete()
    mc.select(cl=True)
    
    duplicate_face_list_number = mc.polyEvaluate(skin_duplicate[0], f=True)
    duplicate_face_list = mc.filterExpand(skin_duplicate[0] + '.f[{}:{}]'.format(0, duplicate_face_list_number), sm=34)
    
    face_source_sets = mc.sets(stored_face_selection[0], n=patch_name + '_target_set', t=patch_name + '_target_set')
    face_source_sets = mc.sets(duplicate_face_list, n=patch_name + '_source_set', t=patch_name + '_source_set')
    
    random_colours(skin_duplicate)

def random_colours(obj):
    
    for i in obj:
        shader = mc.shadingNode('lambert', asShader=True, n='{}{}'.format(i, '_MAT'))
        
        r = [random.random() for i in range(3)]
        
        shading_group = mc.sets(renderable=1, noSurfaceShader=1, empty=1, name='{}{}'.format(i, 'SG'))
        mc.setAttr((shader + '.color'), r[0], r[1], r[2], type='double3')
        mc.connectAttr((shader+'.outColor'),(shading_group+'.surfaceShader'),f=1)
        mc.sets(i, e=1, forceElement=shading_group)

def promptNameWindow():
    
    window = mc.promptDialog(
                title='Patch Name',
                message='Enter Name:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')
    return window

       
if __name__ == '__main__':
    setup_mesh_patches(mc.ls(sl=True), patch_name='L_eye_patch_geo')
