from maya import cmds 
from maya import mel

def install_shelf_tool():
    
    exists = False
    
    shelf_name = "Geo_Patches"
    
    shelf_main_layout = mel.eval('$tmpVar=$gShelfTopLevel')
    
    if not cmds.shelfLayout(shelf_name, exists=True):
        # Create the shelf as a child of the main shelf layout
        cmds.shelfLayout(shelf_name, parent=shelf_main_layout)
        print(f"Shelf '{shelf_name}' created.")
        exists = False
    else:
        print(f"Shelf '{shelf_name}' already exists.")
        exists = True
    
    if not exists:
        create_geo_patch_button = cmds.shelfButton(
            label="GeoP", 
            annotation="Creates a patch", 
            image1="create_patch.png", 
            command="import geo_patches.jd_create_geo_patches as geo_patches; geo_patches.setup_patches()",
            sourceType="python"
        )
        
        transfer_patch_button = cmds.shelfButton(
            label="GeoTr", 
            annotation="Transfer patch", 
            image1="transfer_patch.png", 
            command="import geo_patches.jd_transfer_patch as transfer_patches; transfer_patches.transfer_patch_skinning()",
            dcc="import geo_patches.jd_transfer_geo_patch_smooth as geo_patch_smooth; geo_patch_smooth.transfer_patch_skinning()",
            sourceType="python"
        )
        
        delete_patch_button = cmds.shelfButton(
            label="GeoD", 
            annotation="Delete patch", 
            image1="delete_patch.png", 
            command="import geo_patches.jd_delete_patch as delete_patch; delete_patch.delete_patches()",
            sourceType="python"
        )


def onMayaDroppedPythonFile(*args):
    install_shelf_tool()

install_shelf_tool() # Run immediately on drop