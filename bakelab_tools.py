import bpy

def SelectObject(obj):
    """
    Deselects all objects and selects the given object.

    Args:
        obj (bpy.types.Object): The object to select.
    """
    bpy.ops.object.select_all(action = 'DESELECT')
    if obj:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def SelectObjects(active_obj, selected_objs):
    """
    Selects a list of objects with one object as the active object.

    Args:
        active_obj (bpy.types.Object): The object to set as the active object.
        selected_objs (list[bpy.types.Object]): The objects to select.
    """
    SelectObject(active_obj)
    for obj in selected_objs:
        if obj:
            obj.select_set(True)

def IsValidMesh(self, obj):
    """
    Checks if the given object is a valid mesh.

    Args:
        obj (bpy.types.Object): The object to check.

    Returns:
        bool: True if the object is a mesh and has faces, False otherwise.
    """
    if obj.type != 'MESH':
        self.report(type = {'WARNING'}, message = 'Object ' + obj.name + ' is not mesh type')
        return False
    if len(obj.data.polygons) == 0:
        self.report(type = {'WARNING'}, message = 'Object ' + obj.name + ' has no faces')
        return False
    return True