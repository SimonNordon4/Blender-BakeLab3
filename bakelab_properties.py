import bpy

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
from os.path import expanduser

def updateAdaptiveImageMinSize(self, context):
    self.image_min_size = min(self.image_min_size, self.image_max_size)

def updateAdaptiveImageMaxSize(self, context):
    self.image_max_size = max(self.image_min_size, self.image_max_size)

def updateSavePath(self, context):
    if bpy.data.is_saved:
        self.save_path = bpy.path.abspath(self.save_path)

class BakeLabProperties(PropertyGroup):
    bake_state: EnumProperty(
            items = (
                ("NONE",   "None",   ""),
                ("BAKING", "Baking", ""),
                ("BAKED",  "Baked",  "")
            ),
            default = "NONE"
        )
    bake_mode: EnumProperty(
            name = "Mode",
            description = 'Baking mode',
            items = (
                ("INDIVIDUAL", "Individual Objects", "", "PIVOT_INDIVIDUAL", 1),
                ("ALL_TO_ONE", "All To One Image",   "", "PROP_ON", 2),
                ("TO_ACTIVE",  "Selected to active", "", "PIVOT_ACTIVE", 3)
            ),
            default = "INDIVIDUAL"
        )
    cage_extrusion : FloatProperty(
            name = 'Cage Extrusion', default = 0.05,
            min = 0, soft_max = 1
        )
    pre_join_mesh : BoolProperty(
            name = 'Pre-Join Meshes', default = False,
            description = 'Create one merged mesh and bake to it using ray-tracing',
        )
    image_size : EnumProperty(
            name = 'Image Size',
            items = (
                ('FIXED',    'Fixed',    "Fixed image size"),
                ('ADAPTIVE', 'Adaptive', "Image size by object's surface area")
            ),
            default = 'FIXED'
        )
    adaptive_image_Settings : BoolProperty(
            name = '',
            default = True
        )
    texel_per_unit : FloatProperty(
            name = 'Texels Per Unit',
            default = 100,
            min = 0
        )
    image_min_size    : IntProperty(
            name = 'Min Size',
            default = 32,
            min = 1,
            update=updateAdaptiveImageMaxSize
        )
    image_max_size    : IntProperty(
            name = 'Max Size',
            default = 2048,
            min = 1,
            update=updateAdaptiveImageMinSize
        )
    round_adaptive_image : BoolProperty(
        name = 'Round to power of two', 
        default = True
    )
    anti_alias : IntProperty(
            name = 'Anti-aliasing', default = 1,
            description = 'Anti-aliasing (1 = No Anti-aliasing)',
            min = 1, soft_max = 8
        )
    bake_margin    : IntProperty(
            name = 'Bake Margin',
            description = 'Extends the baked result as a post process filter',
            default = 4,
            min = 0,
            soft_max = 64
        )
    global_image_name  : StringProperty(
            name = 'Image Name',
            description = 'Names of baked images',
            default = "Atlas",
        )
    compute_device : EnumProperty(
            name = 'Device',
            description = 'Compute Device',
            items =  (
                ('GPU','GPU Compute',''),
                ('CPU','CPU','')
            )
        )
    save_or_pack : EnumProperty(
                name  = 'Output',
                items =  (
                    ('PACK','Pack',''),
                    ('SAVE','Save','')
                ),
                default = 'PACK'
            )
    create_folder : BoolProperty(
        name="Create folder",
        description="Automatically creates a folder named after the object(s)",
        default = True
        ) 
    folder_name  : StringProperty(
            name = 'Folder name',
            description = 'Name of the folder',
            default = "Selection",
        )
    save_path : StringProperty(
                default=expanduser("~"),
                name="Folder",
                subtype="DIR_PATH",
                update=updateSavePath
            )
    show_bake_settings : BoolProperty(name = '', default = False)
    show_map_settings  : BoolProperty(name = '', default = False)
    show_file_settings : BoolProperty(name = '', default = False)
    
    apply_only_selected : BoolProperty(
        name = 'Apply only to Selected',
        description = 'Apply only to selected objects',
        default = True
    )
    make_single_user : BoolProperty(
        name = 'Make single user',
        description = 'Make data single user',
        default = True
    )
    # Display
    baking_obj_count : IntProperty(
            name = 'Baking object count',
            default = 0
        )
    baking_obj_index : IntProperty(
            name = 'Current baking object',
            default = 0
        )
    baking_obj_name : StringProperty(
            name = 'Current baking object',
            default = ""
        )
    baking_map_count : IntProperty(
            name = 'Baking map count',
            default = 0
        )
    baking_map_index : IntProperty(
            name = 'Current baking map',
            default = 0
        )
    baking_map_type : StringProperty(
            name = 'Current baking map type',
            default = ""
        )
    baking_map_name : StringProperty(
            name = 'Current baking image',
            default = ""
        )
    baking_map_size : StringProperty(
            name = 'Current baking size',
            default = ""
        )