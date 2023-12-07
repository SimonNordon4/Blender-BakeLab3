import os
import bpy
import sys
import typing
import inspect
import pkgutil
import importlib
from pathlib import Path

class AutoLoader():
    blender_version = bpy.app.version

    modules = None
    ordered_classes = None

    @staticmethod
    def init():
        AutoLoader.modules = AutoLoader.get_all_submodules(Path(__file__).parent)
        AutoLoader.ordered_classes = AutoLoader.get_ordered_classes_to_register(AutoLoader.modules)

    @staticmethod
    def register():
        print("Registering")
        for cls in AutoLoader.ordered_classes:
            print("Registering", cls)
            bpy.utils.register_class(cls)

        for module in AutoLoader.modules:
            if module.__name__ == __name__:
                continue
            if hasattr(module, "register"):
                module.register()

    @staticmethod
    def unregister():
        if AutoLoader.ordered_classes is None:
            return
        for cls in reversed(AutoLoader.ordered_classes):
            print("Unregistering", cls)
            bpy.utils.unregister_class(cls)

        for module in AutoLoader.modules:
            if module.__name__ == __name__:
                continue
            if hasattr(module, "unregister"):
                module.unregister()


    # Import modules
    #################################################
    @staticmethod
    def get_all_submodules(directory):
        return list(AutoLoader.iter_submodules(directory, directory.name))
    @staticmethod
    def iter_submodules(path, package_name):
        for name in sorted(AutoLoader.iter_submodule_names(path)):
            module = importlib.import_module("." + name, package_name)
            try:
                importlib.reload(module)
            except:
                pass
            yield module
    @staticmethod
    def iter_submodule_names(path, root=""):
        for _, module_name, is_package in pkgutil.iter_modules([str(path)]):
            if is_package:
                sub_path = path / module_name
                sub_root = root + module_name + "."
                yield from AutoLoader.iter_submodule_names(sub_path, sub_root)
            else:
                yield root + module_name


    # Find classes to register
    #################################################
    @staticmethod
    def get_ordered_classes_to_register(modules):
        return AutoLoader.toposort(AutoLoader.get_register_deps_dict(modules))
    
    @staticmethod
    def get_register_deps_dict(modules):
        my_classes = set(AutoLoader.iter_my_classes(modules))
        my_classes_by_idname = {cls.bl_idname : cls for cls in my_classes if hasattr(cls, "bl_idname")}

        deps_dict = {}
        for cls in my_classes:
            deps_dict[cls] = set(AutoLoader.iter_my_register_deps(cls, my_classes, my_classes_by_idname))
        return deps_dict
    
    @staticmethod
    def iter_my_register_deps(cls, my_classes, my_classes_by_idname):
        yield from AutoLoader.iter_my_deps_from_annotations(cls, my_classes)
        yield from AutoLoader.iter_my_deps_from_parent_id(cls, my_classes_by_idname)

    @staticmethod
    def iter_my_deps_from_annotations(cls, my_classes):
        for value in typing.get_type_hints(cls, {}, {}).values():
            dependency = AutoLoader.get_dependency_from_annotation(value)
            if dependency is not None:
                if dependency in my_classes:
                    yield dependency

    @staticmethod
    def get_dependency_from_annotation(value):
        if AutoLoader.blender_version >= (2, 93):
            if isinstance(value, bpy.props._PropertyDeferred):
                return value.keywords.get("type")
        else:
            if isinstance(value, tuple) and len(value) == 2:
                if value[0] in (bpy.props.PointerProperty, bpy.props.CollectionProperty):
                    return value[1]["type"]
        return None
    
    @staticmethod
    def iter_my_deps_from_parent_id(cls, my_classes_by_idname):
        if bpy.types.Panel in cls.__bases__:
            parent_idname = getattr(cls, "bl_parent_id", None)
            if parent_idname is not None:
                parent_cls = my_classes_by_idname.get(parent_idname)
                if parent_cls is not None:
                    yield parent_cls

    @staticmethod
    def iter_my_classes(modules):
        base_types = AutoLoader.get_register_base_types()
        for cls in AutoLoader.get_classes_in_modules(modules):
            if any(base in base_types for base in cls.__bases__):
                if not getattr(cls, "is_registered", False):
                    yield cls
                else:
                    #if class is registered, unregister it
                    bpy.utils.unregister_class(cls)
                    yield cls

    @staticmethod
    def get_classes_in_modules(modules):
        classes = set()
        for module in modules:
            for cls in AutoLoader.iter_classes_in_module(module):
                classes.add(cls)
        return classes
    
    @staticmethod
    def iter_classes_in_module(module):
        for value in module.__dict__.values():
            if inspect.isclass(value):
                yield value

    @staticmethod
    def get_register_base_types():
        return set(getattr(bpy.types, name) for name in [
            "Panel", "Operator", "PropertyGroup",
            "AddonPreferences", "Header", "Menu",
            "Node", "NodeSocket", "NodeTree",
            "UIList", "RenderEngine",
            "Gizmo", "GizmoGroup",
        ])


    # Find order to register to solve dependencies
    #################################################
    @staticmethod
    def toposort(deps_dict):
        sorted_list = []
        sorted_values = set()
        while len(deps_dict) > 0:
            unsorted = []
            for value, deps in deps_dict.items():
                if len(deps) == 0:
                    sorted_list.append(value)
                    sorted_values.add(value)
                else:
                    unsorted.append(value)
            deps_dict = {value : deps_dict[value] - sorted_values for value in unsorted}
        return sorted_list
