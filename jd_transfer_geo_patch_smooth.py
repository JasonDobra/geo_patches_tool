import maya.cmds as mc
import sys
import maya.mel as mel


def transfer_patch_skinning(selection, skin_transfer_patch, smooth_border, smtAmt=None):
  
    if len(selection) < 2:
        
        sys.stdout.write('Error: Please select one source and target object to proceed')    
        
    else:
        selection_name = selection[0]
        target_name = selection[1]
        
        source = selection_name + '_source_set'
        target = selection_name + '_target_set'
        
        mc.select(source, r=1)
        mc.select(target, add=1)
        
        source_mesh = selection_name
        
        if skin_transfer_patch:
            smooth_skin_patch(selection_name, target_name, target, source)
        
        mc.select(cl=True)    
        if smooth_border:
            smooth_edge_border(selection_name, source, target, smtAmt)
        
        #mc.select(source, r=1)
        #mc.select(target, add=1)
        
        sys.stdout.write('Result:   skin transfer was successful')
        
def smooth_skin_patch(source_mesh, target_mesh, target, source):
    
    sourceSkin = mel.eval('findRelatedSkinCluster ' + source_mesh)
    targetSkin = mel.eval('findRelatedSkinCluster ' + target_mesh)
    
    source_influences = mc.skinCluster(sourceSkin,query=True,inf=True)
    target_influences = mc.skinCluster(targetSkin,query=True,inf=True)
    
    for influence in source_influences:
        if influence not in target_influences:
        
            mc.skinCluster(targetSkin, edit=True, ai=influence, lw=True, ibp=True)
            
        else:
            pass
    
    mc.select(source, r=1)
    mc.select(target, add=1)
    
    mc.copySkinWeights(noMirror = True, surfaceAssociation = 'closestPoint', influenceAssociation = 'closestJoint' )
    
    
def smooth_edge_border(selection, source, target, smoothAmt=None):

    target_skin = mel.eval('findRelatedSkinCluster ' + selection)
    target_influences = mc.skinCluster(target_skin, query=True, inf=True)
    
    mc.select(target, add=True)

    
    mc.SelectPolygonSelectionBoundary()
    
    smoothAmt = range(smoothAmt)
    
    for amt in smoothAmt:
        border = mc.GrowPolygonSelectionRegion()

    if len(smoothAmt) > 0:
        mel.eval('doSmoothSkinWeightsArgList 3 { "0", "5", "0", "0"   };', ue=True)
        
        
    
transfer_patch_skinning(mc.ls(sl=True), True, True, 2)
