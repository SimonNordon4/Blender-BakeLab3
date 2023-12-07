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

def unregister():
    auto_load.AutoLoader.unregister()

if __name__ == "__main__":
    register()