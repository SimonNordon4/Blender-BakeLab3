import bpy
import bpy
import importlib
import sys
import os

# Append the directory of this script to sys.path to ensure imports work
script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import bakelab_map

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
class BakeObjData(PropertyGroup):
    obj : PointerProperty(
        type=bpy.types.Object
    )
class BakeMapData(PropertyGroup):
    bake_map : PointerProperty(
        type=bakelab_map.BakeLabMap
    )
    image : PointerProperty(
        type=bpy.types.Image
    )

class BakeLab_BakedData(PropertyGroup):
    obj_list : CollectionProperty(
        type=BakeObjData
    )
    map_list : CollectionProperty(
        type=BakeMapData
    )
    
    def AddObj(self, obj):
        item = self.obj_list.add()
        item.obj = obj

    def AddMap(self, bake_map, image):
        item = self.map_list.add()
        
        item.bake_map.type = bake_map.type
        item.bake_map.pass_name = bake_map.pass_name
        item.bake_map.normal_space = bake_map.normal_space
        
        item.image = image
