import os
import bpy
import sys
import typing
import inspect
import pkgutil
import importlib
from pathlib import Path

bpy_version = bpy.app.version
modules = None
ordered_classes = None

def init():
    global modules, ordered_classes
    print("Initializing AutoLoader")
    modules = get_all_submodules(Path(__file__).parent)
    print("Found modules:", modules)
    ordered_classes = get_ordered_classes_to_register(modules)
    
def register():
    global modules, ordered_classes
    for cls in ordered_classes:
        print("Registering", cls)
        bpy.utils.register_class(cls)
    for module in modules:
        if module.__name__ == __name__:
            continue
        if hasattr(module, "register"):
            module.register()
    register_scene_properties()
    
def unregister():
    global modules, ordered_classes
    unregister_scene_properties()
    if ordered_classes is None:
        return
    for cls in reversed(ordered_classes):
        print("Unregistering", cls)
        bpy.utils.unregister_class(cls)
    for module in modules:
        if module.__name__ == __name__:
            continue
        if hasattr(module, "unregister"):
            module.unregister()
            
def get_all_submodules(directory):
    return list(iter_submodules(directory, directory.name))

def iter_submodules(path, package_name):
    for name in sorted(iter_submodule_names(path)):
        try:
            module = importlib.import_module("." + name, package_name)
            print("Imported", module)
        except:
            print("Failed to import", name)
            continue
        yield module
        if module.__path__:
            yield from iter_submodules(module.__path__[0], module.__name__)
            
def iter_submodule_names(path):
    for _, name, ispkg in pkgutil.iter_modules([path]):
        if ispkg:
            continue
        yield name
        
def get_ordered_classes_to_register(modules):
    return toposort(get_register_deps_dict(modules))

def get_register_deps_dict(modules):
    my_classes = set(iter_my_classes(modules))
    my_classes_by_idname = {cls.bl_idname : cls for cls in my_classes if hasattr(cls, "bl_idname")}
    deps_dict = {}
    for cls in my_classes:
        deps_dict[cls] = set(iter_my_register_deps(cls, my_classes, my_classes_by_idname))
    return deps_dict

def iter_my_register_deps(cls, my_classes, my_classes_by_idname):
    yield from iter_my_deps_from_annotations(cls, my_classes)
    yield from iter_my_deps_from_parent_id(cls, my_classes_by_idname)
    
    
def iter_my_deps_from_annotations(cls, my_classes):
    for value in typing.get_type_hints(cls, {}, {}).values():
        dependency = get_dependency_from_annotation(value)
        if dependency is not None:
            if dependency in my_classes:
                yield dependency
                
def get_dependency_from_annotation(value):
    if blender_version >= (2, 93):
        if isinstance(value, bpy.props._PropertyDeferred):
            return value.keywords.get("type")
    else:
        if isinstance(value, tuple) and len(value) == 2:
            if value[0] in (bpy.props.PointerProperty, bpy.props.CollectionProperty):
                return value[1]["type"]
    return None

def iter_my_deps_from_parent_id(cls, my_classes_by_idname):
    if bpy.types.Panel in cls.__bases__:
        parent_idname = getattr(cls, "bl_parent_id", None)
        if parent_idname is not None:
            parent_cls = my_classes_by_idname.get(parent_idname)
            if parent_cls is not None:
                yield parent_cls
                
                
def iter_my_classes(modules):
    base_types = get_register_base_types()
    for cls in get_classes_in_modules(modules):
        if any(base in base_types for base in cls.__bases__):
            if not getattr(cls, "is_registered", False):
                yield cls
            else:
                #if class is registered, unregister it
                bpy.utils.unregister_class(cls)
                yield cls
                
                
def get_classes_in_modules(modules):
    classes = set()
    for module in modules:
        for cls in iter_classes_in_module(module):
            classes.add(cls)
    return classes

def iter_classes_in_module(module):
    for value in module.__dict__.values():
        if inspect.isclass(value):
            yield value
            
            
def get_register_base_types():
    return set(getattr(bpy.types, name) for name in [
        "Panel", "Operator", "PropertyGroup",
        "AddonPreferences", "Header", "Menu",
        "Node", "NodeSocket", "NodeTree",
        "UIList", "RenderEngine",
        "Gizmo", "GizmoGroup",
    ])
    
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

def register_scene_properties():
    from bpy.props import (
        PointerProperty,
        CollectionProperty,
        IntProperty,
    )
    from . import bakelab_properties
    from . import bakelab_map
    from . import bakelab_baked_data
    bpy.types.Scene.BakeLabProps = PointerProperty(type = bakelab_properties.BakeLabProperties)
    bpy.types.Scene.BakeLabMaps = CollectionProperty(type = bakelab_map.BakeLabMap)
    bpy.types.Scene.BakeLab_Data = CollectionProperty(type = bakelab_baked_data.BakeLab_BakedData)
    bpy.types.Scene.BakeLabMapIndex = IntProperty(name = 'BakeLab Map List Index')
    
    
def unregister_scene_properties():
    del bpy.types.Scene.BakeLabMapIndex
    del bpy.types.Scene.BakeLab_Data
    del bpy.types.Scene.BakeLabMaps
    del bpy.types.Scene.BakeLabProps
    