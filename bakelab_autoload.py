import importlib
import inspect
from pathlib import Path
import bpy
import os
import sys
from pathlib import Path

from bpy.props import (
            IntProperty,
            EnumProperty,
            BoolProperty,
            FloatProperty,
            StringProperty,
            PointerProperty,
            CollectionProperty
        )

# Add the directory containing your module to sys.path
addon_directory = Path(__file__).parent
if str(addon_directory) not in sys.path:
    sys.path.append(str(addon_directory))

class AutoLoader:
    bakelab_classes = []

    @staticmethod
    def init():
        AutoLoader.bakelab_classes = []
        folder_path = Path(__file__).parent
        modules = AutoLoader.get_modules(folder_path)

        # we need to order certain modules to be registered first.
        if 'bakelab_properties' in modules:
            modules.remove('bakelab_properties')
            modules.insert(0, 'bakelab_properties')

        for module_name in modules:
            AutoLoader.handle_module(module_name)
            AutoLoader.bakelab_classes.extend(AutoLoader.get_blender_classes(module_name))

        AutoLoader.reorder_class_in_list("BakeLabProperties", 0)
        AutoLoader.reorder_class_in_list("BakeLabMap", 1)
        AutoLoader.reorder_class_in_list("BakeObjData", 2)
        AutoLoader.reorder_class_in_list("BakeMapData", 3)
        

    @staticmethod
    def get_modules(folder_path):
        module_names = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".py"):
                module_name = os.path.splitext(file_name)[0]
                # add Blender-BakeLab3. to the front of the module name
                module_name = "Blender-BakeLab3." + module_name
                module_names.append(module_name)
                
        return module_names
    

    @staticmethod
    def handle_module(module_name):
        try:
            if module_name not in sys.modules:
                importlib.import_module(module_name)
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
        except ImportError as e:
            print(f"Failed to import module {module_name}: {e}")


    @staticmethod
    def get_blender_classes(module_name):
        module = sys.modules[module_name]
        blender_types = (bpy.types.Operator, bpy.types.Panel, bpy.types.PropertyGroup)
        module_classes = [cls for name, cls in inspect.getmembers(module, inspect.isclass) 
                          if issubclass(cls, blender_types) and cls not in blender_types]
        return module_classes
    
    @staticmethod
    def reorder_class_in_list(class_name, index):
        target_class = None
        for cls in AutoLoader.bakelab_classes:
            if cls.__name__ == class_name:
                target_class = cls
                break

        if target_class is not None:
            AutoLoader.bakelab_classes.remove(target_class)
            AutoLoader.bakelab_classes.insert(index, target_class)

    @staticmethod
    def register():
        print(f"Registering classes: {AutoLoader.bakelab_classes}")
        for cls in AutoLoader.bakelab_classes:
            try:
                bpy.utils.register_class(cls)
                print("Registered class: " + str(cls))
            except ValueError as e:
                print(f"Failed to register class {cls}: {e}")

        # bpy.types.Scene.BakeLabProps = PointerProperty(type = BakeLabProperties)
        # bpy.types.Scene.BakeLabMaps = CollectionProperty(type = bakelab_map.BakeLabMap)
        # bpy.types.Scene.BakeLab_Data = CollectionProperty(type = bakelab_baked_data.BakeLab_BakedData)
        # bpy.types.Scene.BakeLabMapIndex = IntProperty(name = 'BakeLab Map List Index')

    @staticmethod
    def unregister():
        for cls in AutoLoader.bakelab_classes:
            bpy.utils.unregister_class(cls)

        # del bpy.types.Scene.BakeLabProps
        # del bpy.types.Scene.BakeLabMaps
        # del bpy.types.Scene.BakeLab_Data
        # del bpy.types.Scene.BakeLabMapIndex

if __name__ == "__main__":
    AutoLoader.init()
    AutoLoader.register()

