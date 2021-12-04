###################################################################################################
#
# Copyright 2020 Otmar Nitsche
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###################################################################################################

bl_info = {
    "name" : "MSFSToolkit v 0.42.x",
    "author" : "Otmar Nitsche, updated by Ron Haertel (FBW import code)",
    "description" : "This toolkit prepares your 3D assets to be used for Microsoft Flight Simulator. Copyright (c) 2020 Otmar Nitsche, 2021 Ron Haertel",
    "blender" : (3, 00, 0),
    "version" : (0, 42, 5),
    "location" : "View3D",
    "warning" : "This version of the addon is work-in-progress. Don't use it in your active development cycle, as it adds variables and objects to the scene that may cause issues further down the line.",
    "category" : "3D View",
    "wiki_url": "https://www.fsdeveloper.com/wiki/index.php?title=Blender2MSFS"
}


from . import auto_load

from . func_behavior import *
from . func_xml import *
from . func_properties import *

from . li_material import *
from . li_properties import *

from . ui_materials import *
#from . ui_properties import *

##################################################################################
# Load custom glTF exporter and activate Asobo extensions:
# io_scene_gltf2 is a modified version of Khronos io_scene_gltf2
from . io_scene_gltf2_msfs import *
from . ext_master import *
##################################################################################

auto_load.init()

## class to add the preference settings
class addSettingsPanel(bpy.types.AddonPreferences):
    bl_idname = __package__
 
    export_texture_dir: bpy.props.StringProperty (
        name = "Default Texture Location",
        description = "Default Texture Location",
        default = ""
    )

    export_copyright: bpy.props.StringProperty (
        name = "Default Copyright Name",
        description = "Default Copyright Name",
        default = ""
    )

    ## draw the panel in the addon preferences
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Optional - You can set here the default values. This will be used in the export window", icon='INFO')

        box = layout.box()
        col = box.column(align = False)

        ## texture default location
        col.prop(self, 'export_texture_dir', expand=False)

        ## default copyright
        col.prop(self, 'export_copyright', expand=False)


def register():
    bpy.utils.register_class(addSettingsPanel)
    auto_load.register()
    try:
        bpy.utils.register_class(ExtAsoboProperties)
    except Exception:
        pass
    bpy.types.Scene.msfs_extAsoboProperties = bpy.props.PointerProperty(type=ExtAsoboProperties)
    from .io_scene_gltf2_msfs import register
    register()


def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(GLTF_PT_AsoboExtensionPanel)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel

def unregister():
    auto_load.unregister()
    bpy.utils.unregister_class(addSettingsPanel)

def unregister_panel():
    try:
        bpy.utils.unregister_class(GLTF_PT_AsoboExtensionPanel)
    except Exception:
        pass
