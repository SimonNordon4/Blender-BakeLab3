import bpy
import importlib
import sys
import os

# Append the directory of this script to sys.path to ensure imports work
script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import bakelab_properties   
import bakelab_bake
import bakelab_uv
import bakelab_baked_data
import bakelab_post
import bakelab_map
import bakelab_ui

if "bpy" in locals():
    importlib.reload(bakelab_properties)
    importlib.reload(bakelab_bake)
    importlib.reload(bakelab_uv)
    importlib.reload(bakelab_baked_data)
    importlib.reload(bakelab_post)
    importlib.reload(bakelab_map)
    importlib.reload(bakelab_ui)


from bpy.types import (
            Operator, 
            PropertyGroup, 
            Panel
        )
from bpy.props import (
            IntProperty,
            EnumProperty,
            BoolProperty,
            FloatProperty,
            StringProperty,
            PointerProperty,
            CollectionProperty
        )

classes = [ bakelab_properties.BakeLabProperties,
            bakelab_bake.Baker,
            bakelab_uv.Unwrapper,
            bakelab_uv.ClearUV,
            bakelab_post.BakeLab_GenerateMaterials,
            bakelab_post.BakeLab_ApplyAO,
            bakelab_post.BakeLab_ApplyDisplace,
            bakelab_post.BakeLab_Finish,
            bakelab_map.BakeLabMap,
            bakelab_map.BakeLabAddMapItem,
            bakelab_map.BakeLabRemoveMapItem,
            bakelab_map.BakeLabMapListUI,
            bakelab_baked_data.BakeObjData,
            bakelab_baked_data.BakeMapData,
            bakelab_baked_data.BakeLab_BakedData,
            bakelab_map.BakeLabShowPassPresets,
            bakelab_ui.BakeLabUI
           ]

class Loader:
    @staticmethod
    def register():
        for cls in classes:
            try:
                bpy.utils.register_class(cls)
                print(f"Registered {cls.__name__}")
            except:
                print(f"Failed to register {cls.__name__}")
            
        
    bpy.types.Scene.BakeLabProps = PointerProperty(type = bakelab_properties.BakeLabProperties)
    bpy.types.Scene.BakeLabMaps = CollectionProperty(type = bakelab_map.BakeLabMap)
    bpy.types.Scene.BakeLab_Data = CollectionProperty(type = bakelab_baked_data.BakeLab_BakedData)
    bpy.types.Scene.BakeLabMapIndex = IntProperty(name = 'BakeLab Map List Index')
    
    @staticmethod
    def unregister():
        for cls in classes:
            bpy.utils.unregister_class(cls)
        
        del bpy.types.Scene.BakeLabProps
        del bpy.types.Scene.BakeLabMaps
        del bpy.types.Scene.BakeLab_Data
        del bpy.types.Scene.BakeLabMapIndex
    
if __name__ == "__main__":
    Loader.register()

