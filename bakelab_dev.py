import bpy
import bakelab_loader

from bpy.types import (
        Operator,
        Panel)

class ReloadOperator(bpy.types.Operator):
    bl_idname = "bakelab.reload_operator"
    bl_label = "Reload Auto-Loader"
    
    def execute(self, context):
        bakelab_loader.unregister()
        bakelab_loader.register()
        return {'FINISHED'}

class UninstallOperator(bpy.types.Operator):
    bl_idname = "bakelab.uninstall_operator"
    bl_label = "Uninstall Addon"
    
    def execute(self, context):
        bakelab_loader.unregister()
        return {'FINISHED'}
    
class BakeLabDeveloperPanel(Panel):
    bl_label = "BakeLabDev"
    bl_space_type = 'VIEW_3D'
    bl_idname = "BAKELAB_PT_dev_ui"
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = "BakeLab"
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        layout.operator("bakelab.reload_operator")
        layout.operator("bakelab.uninstall_operator")
