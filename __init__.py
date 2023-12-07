# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import importlib
import sys
import os

# Append the directory of this script to sys.path to ensure imports work
script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import bakelab_loader
if "bakelab_loader" in sys.modules:
    importlib.reload(bakelab_loader)
else:
    import bakelab_loader

from bakelab_loader import Loader
    
bl_info = {
    "name" : "BakeLab",
    "author" : "Simon Nordon",
    "description" : "Built from Shahzod Boyxonov BakeLab",
    "blender" : (2, 81, 0),
    "version" : (2, 0, 1),
    "location" : "View3D > Properties > BakeLab",
    "category" : "Baking"
}

Loader.init()

def register():
    Loader.register()

def unregister():
    Loader.unregister()

if __name__ == "__main__":
    register()
