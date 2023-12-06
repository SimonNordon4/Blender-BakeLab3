import importlib
import inspect
from pathlib import Path
import bpy
import os
import sys
from pathlib import Path

# Add the directory containing your module to sys.path
addon_directory = Path(__file__).parent
if str(addon_directory) not in sys.path:
    sys.path.append(str(addon_directory))

class AutoLoader:
    bakelab_classes = []

    @staticmethod
    def init():
        folder_path = Path(__file__).parent
        modules = AutoLoader.get_modules(folder_path)

        for module_name in modules:
            AutoLoader.handle_module(module_name)
        AutoLoader.bakelab_classes = AutoLoader.get_blender_classes()

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
        print(f"Trying to import: {module_name}")
        try:
            if module_name not in sys.modules:
                importlib.import_module(module_name)
                print(f"Imported module {module_name}")
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
                print(f"Reloaded module {module_name}")
        except ImportError as e:
            print(f"Failed to import module {module_name}: {e}")


    @staticmethod
    def get_blender_classes():
        blender_types = (bpy.types.Operator, bpy.types.Panel, bpy.types.PropertyGroup)
        return [cls for module_name, module in sys.modules.items() 
                if module_name.startswith('your_addon_name')
                for _, cls in inspect.getmembers(module, inspect.isclass) 
                if issubclass(cls, blender_types)]

    @staticmethod
    def register():
        print(f"Registering classes: {AutoLoader.bakelab_classes}")
        for cls in AutoLoader.bakelab_classes:
            try:
                print(f"Registering class {cls}")
                bpy.utils.register_class(cls)
            except ValueError as e:
                print(f"Failed to register class {cls}: {e}")

    @staticmethod
    def unregister():
        for cls in AutoLoader.bakelab_classes:
            bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    print(f"Module name: {__name__}, Package: {__package__}")
    AutoLoader.init()
    AutoLoader.register()
