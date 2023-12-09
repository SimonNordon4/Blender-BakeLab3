# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import os
import sys

# Get the directory of the current file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add it to sys.path
sys.path.insert(0, script_dir)

# Set __package__ to the name of the directory
__package__ = os.path.basename(script_dir)

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

import auto_load
if "auto_load" in locals():
    import importlib
    importlib.reload(auto_load)

bl_info = {
    "name" : "BakeLab",
    "author" : "Simon Nordon",
    "description" : "Bake textures easily",
    "blender" : (2, 81, 0),
    "version" : (2, 0, 1),
    "location" : "View3D > Properties > BakeLab",
    "category" : "Baking"
}

auto_load.AutoLoader.init()

def register():
    auto_load.AutoLoader.register()

def unregister():
    auto_load.AutoLoader.unregister()

if __name__ == "__main__":
    register()
    pass