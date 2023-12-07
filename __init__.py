bl_info = {
    "name" : "BakeLab",
    "author" : "Simon Nordon",
    "description" : "Bake textures easily",
    "blender" : (2, 81, 0),
    "version" : (2, 0, 1),
    "location" : "View3D > Properties > BakeLab",
    "category" : "Baking"
}

import importlib
import os
import sys
import bpy

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

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    package_name = os.path.basename(script_dir)
    sys.path.insert(0, script_dir)
    __package__ = package_name





from . import auto_load
if "auto_load" in locals():
    importlib.reload(auto_load)





auto_load.AutoLoader.init()

def register():
    auto_load.AutoLoader.register()

    from . import bakelab_properties
    bpy.types.Scene.BakeLabProps = PointerProperty(type = bakelab_properties.BakeLabProperties)
    # bpy.types.Scene.BakeLabMaps = CollectionProperty(type = bakelab_map.BakeLabMap)
    # bpy.types.Scene.BakeLab_Data = CollectionProperty(type = bakelab_baked_data.BakeLab_BakedData)
    # bpy.types.Scene.BakeLabMapIndex = IntProperty(name = 'BakeLab Map List Index')

def unregister():
    # del bpy.types.Scene.BakeLabMapIndex
    # del bpy.types.Scene.BakeLab_Data
    # del bpy.types.Scene.BakeLabMaps
    # del bpy.types.Scene.BakeLabProps 

    auto_load.AutoLoader.unregister()

if __name__ == "__main__":
    register()