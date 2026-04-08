from maya import cmds 
import sys
import maya.mel as mel


def transfer_patch_skinning():
    
    selection = cmds.ls(sl=True)
    skin_transfer_patch = True
    smooth_border = True
    smtAmt = 2
    
    if len(selection) < 2:
        
        sys.stdout.write('Error: Please select one source and target object to proceed')    
        
    else:
        selection_name = selection[0]
        target_name = selection[1]
        
        source = selection_name + '_source_set'
        target = selection_name + '_target_set'
        
        cmds.select(source, r=1)
        cmds.select(target, add=1)
        
        source_mesh = selection_name
        
        if skin_transfer_patch:
            smooth_skin_patch(selection_name, target_name, target, source)
        
        cmds.select(cl=True)    
        if smooth_border:
            smooth_edge_border(selection_name, source, target, smtAmt)
    
        
        sys.stdout.write('Result:   skin transfer was successful')
        
def smooth_skin_patch(source_mesh, target_mesh, target, source):
    
    sourceSkin = mel.eval('findRelatedSkinCluster ' + source_mesh)
    targetSkin = mel.eval('findRelatedSkinCluster ' + target_mesh)
    
    source_influences = cmds.skinCluster(sourceSkin,query=True,inf=True)
    target_influences = cmds.skinCluster(targetSkin,query=True,inf=True)
    
    for influence in source_influences:
        if influence not in target_influences:
        
            cmds.skinCluster(targetSkin, edit=True, ai=influence, lw=True, ibp=True)
            
        else:
            pass
    
    cmds.select(source, r=1)
    cmds.select(target, add=1)
    
    cmds.copySkinWeights(noMirror = True, surfaceAssociation = 'closestPoint', influenceAssociation = 'closestJoint' )
    
    
def smooth_edge_border(selection, source, target, smoothAmt=None):

    target_skin = mel.eval('findRelatedSkinCluster ' + selection)
    target_influences = cmds.skinCluster(target_skin, query=True, inf=True)
    
    cmds.select(target, add=True)

    
    cmds.SelectPolygonSelectionBoundary()
    
    smoothAmt = range(smoothAmt)
    
    for amt in smoothAmt:
        border = cmds.GrowPolygonSelectionRegion()

    if len(smoothAmt) > 0:
        mel.eval('doSmoothSkinWeightsArgList 3 { "0", "5", "0", "0"   };', ue=True)
        
        
    
transfer_patch_skinning()
