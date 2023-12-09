import bpy
import os
import sys
import importlib

from bpy.props import (
            IntProperty, 
            CollectionProperty, 
            PointerProperty
        )

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

import bakelab_bake
import bakelab_baked_data
import bakelab_map
import bakelab_post
import bakelab_properties
import bakelab_tools
import bakelab_ui
import bakelab_uv

if "bpy" in locals():
    importlib.reload(bakelab_bake)
    importlib.reload(bakelab_baked_data)
    importlib.reload(bakelab_map)
    importlib.reload(bakelab_post)
    importlib.reload(bakelab_properties)
    importlib.reload(bakelab_tools)
    importlib.reload(bakelab_ui)
    importlib.reload(bakelab_uv)

classes = (
    bakelab_properties.BakeLabProperties,
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
)

def register():
    print("Registering..")
    for cls in classes:
        print("Registered", cls)
        bpy.utils.register_class(cls)

    bpy.types.Scene.BakeLabProps = PointerProperty(type = bakelab_properties.BakeLabProperties)
    bpy.types.Scene.BakeLabMaps = CollectionProperty(type = bakelab_map.BakeLabMap)
    bpy.types.Scene.BakeLab_Data = CollectionProperty(type = bakelab_baked_data.BakeLab_BakedData)
    bpy.types.Scene.BakeLabMapIndex = IntProperty(name = 'BakeLab Map List Index')


def unregister():
    del bpy.types.Scene.BakeLabMapIndex
    del bpy.types.Scene.BakeLab_Data
    del bpy.types.Scene.BakeLabMaps
    del bpy.types.Scene.BakeLabProps 

    for cls in classes:
        bpy.utils.unregister_class(cls)

register()

