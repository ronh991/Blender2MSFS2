# Copyright 2021 FlyByWire Simulations.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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

import bpy
from bpy.types import Material, Panel, PropertyGroup, Image
from bpy.props import (
    EnumProperty,
    FloatVectorProperty,
    FloatProperty,
    IntProperty,
    BoolProperty,
    PointerProperty,
)
from . import gltf2_blender_flight_sim_material_functions as functions
from ..com import gltf2_io_debug

# - newer function not used for MSFSToolkit Legacy version
def update_material(self, context):

    # Reset material properties
    #self.msfs_base_color_factor = msfs_material_default_values.msfs_base_color_factor
    self.msfs_color_albedo_mix = msfs_material_default_values.msfs_color_albedo_mix
    self.msfs_emissive_factor = msfs_material_default_values.msfs_emissive_factor

    self.msfs_alpha_mode = msfs_material_default_values.msfs_alpha_mode
    self.msfs_draw_order = msfs_material_default_values.msfs_draw_order
    self.msfs_double_sided = msfs_material_default_values.msfs_double_sided
    self.msfs_dont_cast_shadows = msfs_material_default_values.msfs_dont_cast_shadows
    self.msfs_day_night_cycle = msfs_material_default_values.msfs_day_night_cycle

    self.msfs_use_pearl_effect = msfs_material_default_values.msfs_use_pearl_effect
    self.msfs_pearl_shift = msfs_material_default_values.msfs_pearl_shift
    self.msfs_pearl_range = msfs_material_default_values.msfs_pearl_range
    self.msfs_pearl_brightness = msfs_material_default_values.msfs_pearl_brightness

    self.msfs_collision_material = msfs_material_default_values.msfs_collision_material
    self.msfs_road_material = msfs_material_default_values.msfs_road_material

    self.msfs_uv_offset_u = msfs_material_default_values.msfs_uv_offset_u
    self.msfs_uv_offset_v = msfs_material_default_values.msfs_uv_offset_v
    self.msfs_uv_tiling_u = msfs_material_default_values.msfs_uv_tiling_u
    self.msfs_uv_tiling_v = msfs_material_default_values.msfs_uv_tiling_v
    self.msfs_uv_rotation = msfs_material_default_values.msfs_uv_rotation
    self.msfs_uv_clamp_u = msfs_material_default_values.msfs_uv_clamp_u
    self.msfs_uv_clamp_v = msfs_material_default_values.msfs_uv_clamp_v

    self.msfs_roughness_factor = msfs_material_default_values.msfs_roughness_factor
    self.msfs_metallic_factor = msfs_material_default_values.msfs_metallic_factor
    self.msfs_normal_scale = msfs_material_default_values.msfs_normal_scale
    self.msfs_alpha_cutoff = msfs_material_default_values.msfs_alpha_cutoff

    self.msfs_detail_uv_scale = msfs_material_default_values.msfs_detail_uv_scale
    self.msfs_detail_uv_offset_u = msfs_material_default_values.msfs_detail_uv_offset_u
    self.msfs_detail_uv_offset_v = msfs_material_default_values.msfs_detail_uv_offset_v
    self.msfs_detail_normal_scale = (
        msfs_material_default_values.msfs_detail_normal_scale
    )

    self.msfs_blend_threshold = msfs_material_default_values.msfs_blend_threshold
    # Decal / Geo Decal (Frosted)
    self.msfs_decal_color_blend_factor = (
        msfs_material_default_values.msfs_decal_color_blend_factor
    )
    self.msfs_decal_metal_blend_factor = (
        msfs_material_default_values.msfs_decal_metal_blend_factor
    )
    self.msfs_decal_normal_blend_factor = (
        msfs_material_default_values.msfs_decal_normal_blend_factor
    )
    self.msfs_decal_roughness_blend_factor = (
        msfs_material_default_values.msfs_decal_roughness_blend_factor
    )
    self.msfs_decal_occlusion_blend_factor = (
        msfs_material_default_values.msfs_decal_occlusion_blend_factor
    )
    self.msfs_decal_emissive_blend_factor = (
        msfs_material_default_values.msfs_decal_emissive_blend_factor
    )

    # Windshield
    self.msfs_rain_drop_scale = msfs_material_default_values.msfs_rain_drop_scale
    self.msfs_wiper_1_state = msfs_material_default_values.msfs_wiper_1_state
    self.msfs_wiper_2_state = msfs_material_default_values.msfs_wiper_2_state

    # Glass
    self.msfs_glass_reflection_factor = (
        msfs_material_default_values.msfs_glass_reflection_factor
    )
    self.msfs_glass_deformation_factor = (
        msfs_material_default_values.msfs_glass_deformation_factor
    )

    # Parallax
    self.msfs_parallax_scale = msfs_material_default_values.msfs_parallax_scale
    self.msfs_parallax_room_size_x = (
        msfs_material_default_values.msfs_parallax_room_size_x
    )
    self.msfs_parallax_room_size_y = (
        msfs_material_default_values.msfs_parallax_room_size_y
    )
    self.msfs_parallax_room_number = (
        msfs_material_default_values.msfs_parallax_room_number
    )
    self.msfs_parallax_corridor = msfs_material_default_values.msfs_parallax_corridor

    # Hair / SSS
    self.msfs_sss_color = msfs_material_default_values.msfs_sss_color

    # Fresnel
    self.msfs_fresnel_factor = msfs_material_default_values.msfs_fresnel_factor
    self.msfs_fresnel_opacity_bias = (
        msfs_material_default_values.msfs_fresnel_opacity_bias
    )

    # Textures
    self.msfs_base_color_texture = None
    self.msfs_comp_texture = None
    self.msfs_normal_texture = None
    self.msfs_emissive_texture = None
    self.msfs_detail_color_texture = None
    self.msfs_detail_comp_texture = None
    self.msfs_detail_normal_texture = None
    self.msfs_blend_mask_texture = None
    self.msfs_wetness_ao_texture = None
    self.msfs_dirt_texture = None
    self.msfs_height_map_texture = None

    # Next, we decide which properties should be displayed to the user based off the material type
    functions.setup_show(self, context)
    # Finally, we create the material nodes if needed
    
    gltf2_io_debug.print_console("WARNING","update_material - Will be created")
    functions.create_material(self, context)

# MSFSToolkit Legacy

def switch_msfs_material(self,context):
    mat = context.active_object.active_material
    if mat.msfs_material_mode == 'msfs_standard':
        functions.CreateMSFSStandardShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = True
        mat.msfs_show_detail_metallic = True
        mat.msfs_show_detail_normal = True
        mat.msfs_show_blend_mask = True
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = True
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = True

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = True
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = True
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_standard material.")

    elif mat.msfs_material_mode == 'msfs_anisotropic':
        functions.CreateMSFSAnisotropicShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = True
        mat.msfs_show_detail_metallic = True
        mat.msfs_show_detail_normal = True
        mat.msfs_show_blend_mask = True
        mat.msfs_show_anisotropic_direction = True
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = True
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_anisotropic material.")

    elif mat.msfs_material_mode == 'msfs_sss':
        functions.CreateMSFSSSSShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = True

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = False
        mat.msfs_show_detail_metallic = False
        mat.msfs_show_detail_normal = False
        mat.msfs_show_blend_mask = False
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = True
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = False

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_sss material.")

    elif mat.msfs_material_mode == 'msfs_glass':
        functions.CreateMSFSGlassShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = True
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = True
        mat.msfs_show_detail_metallic = True
        mat.msfs_show_detail_normal = True
        mat.msfs_show_blend_mask = True
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = True
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_glass material.")

    elif mat.msfs_material_mode == 'msfs_decal':
        functions.CreateMSFSDecalShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = True
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = True
        mat.msfs_show_detail_metallic = True
        mat.msfs_show_detail_normal = True
        mat.msfs_show_blend_mask = True
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = True
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = True

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_decal material.")

    elif mat.msfs_material_mode == 'msfs_clearcoat':
        functions.CreateMSFSClearcoatShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = True
        mat.msfs_show_detail_metallic = True
        mat.msfs_show_detail_normal = True
        mat.msfs_show_blend_mask = True
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = True
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = True
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_clearcoat material.")

    elif mat.msfs_material_mode == 'msfs_env_occluder':
        functions.CreateMSFSEnvOccluderShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = False
        mat.msfs_show_metallic = False
        mat.msfs_show_normal = False
        mat.msfs_show_emissive = False
        mat.msfs_show_detail_albedo = False
        mat.msfs_show_detail_metallic = False
        mat.msfs_show_detail_normal = False
        mat.msfs_show_blend_mask = False
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = False
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = False
        mat.msfs_show_no_cast_shadow = False
        mat.msfs_show_double_sided = False
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = False
        mat.msfs_show_road_material = False

        mat.msfs_show_ao_use_uv2 = False
        mat.msfs_show_uv_clamp = False

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = False

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_env_occluder material.")

    elif mat.msfs_material_mode == 'msfs_fake_terrain':
        functions.CreateMSFSFakeTerrainShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = True
        mat.msfs_show_detail_metallic = True
        mat.msfs_show_detail_normal = True
        mat.msfs_show_blend_mask = True
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = False
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        mat.msfs_show_pearl = False

        print("Switched to msfs_fake_terrain material.")

    elif mat.msfs_material_mode == 'msfs_fresnel':
        functions.CreateMSFSFresnelShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = True
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = False
        mat.msfs_show_detail_metallic = False
        mat.msfs_show_detail_normal = False
        mat.msfs_show_blend_mask = False
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = True
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_fresnel material.")

    elif mat.msfs_material_mode == 'msfs_windshield':
        functions.CreateMSFSWindshieldShader(mat)
 
        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = True
        mat.msfs_show_detail_metallic = True
        mat.msfs_show_detail_normal = True
        mat.msfs_show_blend_mask = True
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        mat.msfs_show_wiper_mask = False #Unlock this when available

        mat.msfs_show_blend_mode = False
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        #switch_msfs_blendmode()
        if mat.msfs_material_mode == 'msfs_windshield' or mat.msfs_blend_mode == 'BLEND':
            MakeTranslucent(mat)
        elif mat.msfs_blend_mode == 'MASKED':
            MakeMasked(mat)
        elif mat.msfs_blend_mode == 'DITHER':
            MakeDither(mat)
        else:
            MakeOpaque(mat)
        
        print("Switched to msfs_windshield material.")

    elif mat.msfs_material_mode == 'msfs_porthole':
        functions.CreateMSFSPortholeShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = True
        mat.msfs_show_detail_metallic = True
        mat.msfs_show_detail_normal = True
        mat.msfs_show_blend_mask = True
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = False
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_porthole material.")

    elif mat.msfs_material_mode == 'msfs_parallax':
        functions.CreateMSFSParallaxShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = True
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = False
        mat.msfs_show_detail_metallic = False
        mat.msfs_show_detail_normal = False
        mat.msfs_show_blend_mask = False
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = True
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = False
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_parallax material.")

    elif mat.msfs_material_mode == 'msfs_geo_decal':
        functions.CreateMSFSGeoDecalShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = True

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = True
        mat.msfs_show_detail_metallic = True
        mat.msfs_show_detail_normal = True
        mat.msfs_show_blend_mask = False
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = False
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False

        print("Switched to msfs_geo_decal material.")

    elif mat.msfs_material_mode == 'msfs_hair':
        functions.CreateMSFSHairShader(mat)

        mat.msfs_show_tint = True
        mat.msfs_show_sss_color = True

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = True
        mat.msfs_show_metallic = True
        mat.msfs_show_normal = True
        mat.msfs_show_emissive = True
        mat.msfs_show_detail_albedo = False
        mat.msfs_show_detail_metallic = False
        mat.msfs_show_detail_normal = False
        mat.msfs_show_blend_mask = False
        mat.msfs_show_anisotropic_direction = True
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = False
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = True
        mat.msfs_show_no_cast_shadow = True
        mat.msfs_show_double_sided = True
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = True
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = True

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False
        
        print("Switched to msfs_hair material.")

    elif mat.msfs_material_mode == 'msfs_invisible':
        functions.CreateMSFSInvisibleShader(mat)

        mat.msfs_show_tint = False
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = False
        mat.msfs_show_metallic = False
        mat.msfs_show_normal = False
        mat.msfs_show_emissive = False
        mat.msfs_show_detail_albedo = False
        mat.msfs_show_detail_metallic = False
        mat.msfs_show_detail_normal = False
        mat.msfs_show_blend_mask = False
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = False
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = False
        mat.msfs_show_no_cast_shadow = False
        mat.msfs_show_double_sided = False
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = True
        mat.msfs_show_road_material = True

        mat.msfs_show_ao_use_uv2 = False
        mat.msfs_show_uv_clamp = True

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = False

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False
        
        print("Switched to msfs_invisible material.")

    else:
        mat.msfs_show_tint = False
        mat.msfs_show_sss_color = False

        mat.msfs_show_glass_parameters = False
        mat.msfs_show_decal_parameters = False
        mat.msfs_show_fresnel_parameters = False
        mat.msfs_show_parallax_parameters = False
        mat.msfs_show_geo_decal_parameters = False

        mat.msfs_show_albedo = False
        mat.msfs_show_metallic = False
        mat.msfs_show_normal = False
        mat.msfs_show_emissive = False
        mat.msfs_show_detail_albedo = False
        mat.msfs_show_detail_metallic = False
        mat.msfs_show_detail_normal = False
        mat.msfs_show_blend_mask = False
        mat.msfs_show_anisotropic_direction = False
        mat.msfs_show_clearcoat = False
        mat.msfs_show_behind_glass = False
        msfs_show_wiper_mask = False

        mat.msfs_show_blend_mode = False
        mat.use_backface_culling = not mat.msfs_double_sided

        mat.msfs_show_draworder = False
        mat.msfs_show_no_cast_shadow = False
        mat.msfs_show_double_sided = False
        mat.msfs_show_responsive_aa = False
        mat.msfs_show_day_night_cycle = False

        mat.msfs_show_collision_material = False
        mat.msfs_show_road_material = False

        mat.msfs_show_ao_use_uv2 = False
        mat.msfs_show_uv_clamp = False

        mat.msfs_show_alpha_cutoff = False
        mat.msfs_show_blend_threshold = False

        #New
        mat.msfs_show_pearl = False
        mat.msfs_show_windshield_options = False
        
        print("Switched to non-sim material.")

def match_albedo(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf_node = nodes.get("bsdf")
    albedo = nodes.get("albedo")
    albedo_tint_mix = nodes.get("albedo_tint_mix")
    albedo_detail_mix = nodes.get("albedo_detail_mix")

    if albedo != None:
        nodes["albedo"].image = mat.msfs_albedo_texture

        if mat.msfs_albedo_texture != None:
            # Create the link:
            if albedo_tint_mix != None:
                links.new(albedo.outputs["Color"], albedo_tint_mix.inputs["Color2"])
            if albedo_detail_mix != None:
                links.new(albedo_detail_mix.outputs["Color"], bsdf_node.inputs["Base Color"])
        else:
            #unlink the separator:
            if albedo_tint_mix != None:
                l = albedo_tint_mix.inputs["Color2"].links[0]
                links.remove(l)                
            if bsdf_node != None:
                l = bsdf_node.inputs["Base Color"].links[0]
                links.remove(l)                

def match_metallic(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    #Try to generate the links:
    bsdf_node = nodes.get("bsdf")
    metallic = nodes.get("metallic")
    metallic_sep_node = nodes.get("metallic_sep")

    if metallic != None:
        nodes["metallic"].image = mat.msfs_metallic_texture

        if mat.msfs_metallic_texture != None:
            nodes["metallic"].image.colorspace_settings.name = 'Non-Color'

            #link to bsdf
            if (bsdf_node != None and metallic_sep_node != None):
                links.new(metallic_sep_node.outputs[1], bsdf_node.inputs["Roughness"])
                links.new(metallic_sep_node.outputs[2], bsdf_node.inputs["Metallic"])
        else:
            #unlink the separator:
            if (bsdf_node != None and metallic_sep_node != None):
                l = bsdf_node.inputs["Roughness"].links[0]
                links.remove(l)                
                l = bsdf_node.inputs["Metallic"].links[0]
                links.remove(l)                

def match_normal(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf_node = nodes.get("bsdf")
    normal = nodes.get("normal")
    normal_map_node = nodes.get("normal_map_node")

    if normal != None:
        nodes["normal"].image = mat.msfs_normal_texture

        if mat.msfs_normal_texture != None:
            nodes["normal"].image.colorspace_settings.name = 'Non-Color'
            if (bsdf_node != None and normal_map_node != None):
                    links.new(normal_map_node.outputs["Normal"], bsdf_node.inputs["Normal"])
        else:
            if (bsdf_node != None and normal_map_node != None):
                l = bsdf_node.inputs["Normal"].links[0]
                links.remove(l)                

def match_emissive(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    #Try to generate the links:
    bsdf_node = nodes.get("bsdf")
    emissive = nodes.get("emissive")
    emissive_tint_mix = nodes.get("emissive_tint_mix")

    if emissive != None:
        nodes["emissive"].image = mat.msfs_emissive_texture

        if mat.msfs_emissive_texture != "":
            #link to bsdf
            if (bsdf_node != None and emissive_tint_mix != None):
                links.new(emissive_tint_mix.outputs["Color"], bsdf_node.inputs["Emission"])
        else:
            #unlink the separator:
            if (bsdf_node != None and emissive_tint_mix != None):
                l = bsdf_node.inputs["Emission"].links[0]
                links.remove(l)                

def match_detail_albedo(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    albedo_detail_mix = nodes.get("albedo_detail_mix")
    detail_albedo = nodes.get("detail_albedo")

    if detail_albedo != None:
        nodes["detail_albedo"].image = mat.msfs_detail_albedo_texture
        
        if mat.msfs_detail_albedo_texture.name != "":
            # Create the link:
            if (detail_albedo != None and albedo_detail_mix != None):
                links.new(detail_albedo.outputs["Color"], albedo_detail_mix.inputs["Color2"])
                albedo_detail_mix.inputs[0].default_value = 0.5
        else:
            #unlink the separator:
            if (detail_albedo != None and albedo_detail_mix != None):
                l = albedo_detail_mix.inputs["Color2"].links[0]
                links.remove(l)                
                albedo_detail_mix.inputs[0].default_value = 0.0

def match_detail_metallic(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    metallic_detail_mix = nodes.get("metallic_detail_mix")
    detail_metallic = nodes.get("detail_metallic")

    if detail_metallic != None:
        detail_metallic.image = mat.msfs_detail_metallic_texture
        detail_metallic.image.colorspace_settings.name = 'Non-Color'
        if mat.msfs_detail_metallic_texture.name != "":
            # Create the link:
            if (detail_metallic != None and metallic_detail_mix != None):
                links.new(detail_metallic.outputs["Color"], metallic_detail_mix.inputs["Color2"])
                metallic_detail_mix.inputs[0].default_value = 0.5
        else:
            #unlink the separator:
            if (detail_metallic != None and metallic_detail_mix != None):
                l = metallic_detail_mix.inputs["Color2"].links[0]
                links.remove(l)                
                metallic_detail_mix.inputs[0].default_value = 0.0

def match_detail_normal(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    normal_detail_mix = nodes.get("normal_detail_mix")
    detail_normal = nodes.get("detail_normal")

    if detail_normal != None:
        detail_normal.image = mat.msfs_detail_normal_texture
        detail_normal.image.colorspace_settings.name = 'Non-Color'
        if mat.msfs_detail_normal_texture.name != "":
            # Create the link:
            if (detail_normal != None and normal_detail_mix != None):
                links.new(detail_normal.outputs["Color"], normal_detail_mix.inputs["Color2"])
                normal_detail_mix.inputs[0].default_value = 0.5
        else:
            #unlink the separator:
            if (detail_normal != None and normal_detail_mix != None):
                l = normal_detail_mix.inputs["Color2"].links[0]
                links.remove(l)                
                normal_detail_mix.inputs[0].default_value = 0.0

def match_blend_mask(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    if nodes.get("blend_mask", None) != None:
        nodes["blend_mask"].image = mat.msfs_blend_mask_texture
        nodes["blend_mask"].image.colorspace_settings.name = 'Non-Color'

        albedo_detail_mix = nodes.get("albedo_detail_mix")
        metallic_detail_mix = nodes.get("metallic_detail_mix")
        normal_detail_mix = nodes.get("normal_detail_mix")

        #link the node, if a texture is set:
        if mat.msfs_blend_mask_texture.name != "":
            if mat.msfs_blend_mask_texture.channels > 3:
                if albedo_detail_mix != None:
                    links.new(nodes["blend_mask"].outputs["Alpha"],albedo_detail_mix.inputs["Fac"])
                if metallic_detail_mix != None:
                    links.new(nodes["blend_mask"].outputs["Alpha"],metallic_detail_mix.inputs["Fac"])
                if normal_detail_mix != None:
                    links.new(nodes["blend_mask"].outputs["Alpha"],normal_detail_mix.inputs["Fac"])
            else:
                if albedo_detail_mix != None:
                    links.new(nodes["blend_mask"].outputs["Color"],albedo_detail_mix.inputs["Fac"])
                if metallic_detail_mix != None:
                    links.new(nodes["blend_mask"].outputs["Color"],metallic_detail_mix.inputs["Fac"])
                if normal_detail_mix != None:
                    links.new(nodes["blend_mask"].outputs["Color"],normal_detail_mix.inputs["Fac"])
        else:
            if albedo_detail_mix != None:
                l = albedo_detail_mix.inputs["Fac"].links[0]
                links.remove(l)                
            if metallic_detail_mix != None:
                l = metallic_detail_mix.inputs["Fac"].links[0]
                links.remove(l)                
            if normal_detail_mix != None:
                l = normal_detail_mix.inputs["Fac"].links[0]
                links.remove(l)                

def match_anisotropic_direction(self,context):
    mat = context.activate_object.active_material
    if mat.node_tree.nodes.get("anisotropic_direction", None) != None:
        mat.node_tree.nodes["anisotropic_direction"].image = mat.msfs_anisotropic_direction_texture
        mat.node_tree.nodes["anisotropic_direction"].image.colorspace_settings.name = 'Non-Color'

def match_clearcoat(self,context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    clearcoat = nodes.get("clearcoat")
    clearcoat_sep = nodes.get("clearcoat_sep")
    bsdf_node = nodes.get("bsdf")

    if clearcoat != None:
        mat.node_tree.nodes["clearcoat"].image = mat.msfs_clearcoat_texture
        mat.node_tree.nodes["clearcoat"].image.colorspace_settings.name = 'Non-Color'
        if (clearcoat_sep != None and bsdf_node != None):
            if mat.msfs_clearcoat_texture.name != "":
                links.new(clearcoat_sep.outputs["R"],bsdf_node.inputs["Clearcoat"])
                links.new(clearcoat_sep.outputs["G"],bsdf_node.inputs["Clearcoat Roughness"])
            else:
                l = bsdf_node.inputs["Clearcoat"].links[0]
                links.remove(l)                
                l = bsdf_node.inputs["Clearcoat Roughness"].links[0]
                links.remove(l)

def match_behind_glass(self,context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    #Try to generate the links:
    albedo_detail_mix = nodes.get("albedo_detail_mix")
    behind_glass = nodes.get("behind_glass")

    if behind_glass != None:
        mat.node_tree.nodes["behind_glass"].image = mat.msfs_behind_glass_texture
        if mat.msfs_behind_glass_texture.name != "":
            # Create the link:
            if (behind_glass != None and albedo_detail_mix != None):
                links.new(behind_glass.outputs["Color"], albedo_detail_mix.inputs["Color2"])
        else:
            #unlink the separator:
            if (behind_glass != None and albedo_detail_mix != None):
                l = albedo_detail_mix.inputs["Color2"].links[0]
                links.remove(l)                

def match_wiper_mask(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

def switch_msfs_blendmode(self, context):
    mat = context.active_object.active_material
    if mat.msfs_material_mode == 'msfs_windshield' or mat.msfs_blend_mode == 'BLEND':
        MakeTranslucent(mat)
    elif mat.msfs_blend_mode == 'MASKED':
        MakeMasked(mat)
    elif mat.msfs_blend_mode == 'DITHER':
        MakeDither(mat)
    else:
        MakeOpaque(mat)

#Update functions for the "tint" parameters:
def update_color_albedo_mix(self, context):
    mat = context.active_object.active_material
    if mat.node_tree.nodes.get("bsdf", None) != None:
        mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[0] = mat.msfs_color_albedo_mix[0]
        mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[1] = mat.msfs_color_albedo_mix[1]
        mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[2] = mat.msfs_color_albedo_mix[2]
        mat.node_tree.nodes.get("albedo_tint").outputs[0].default_value[0] = mat.msfs_color_albedo_mix[0]
        mat.node_tree.nodes.get("albedo_tint").outputs[0].default_value[1] = mat.msfs_color_albedo_mix[1]
        mat.node_tree.nodes.get("albedo_tint").outputs[0].default_value[2] = mat.msfs_color_albedo_mix[2]
        mat.node_tree.nodes["albedo_detail_mix"].inputs[2].default_value[0] = mat.msfs_color_albedo_mix[0]
        mat.node_tree.nodes["albedo_detail_mix"].inputs[2].default_value[1] = mat.msfs_color_albedo_mix[1]
        mat.node_tree.nodes["albedo_detail_mix"].inputs[2].default_value[2] = mat.msfs_color_albedo_mix[2]

def update_color_alpha_mix(self, context):
    mat = context.active_object.active_material
    if mat.node_tree.nodes.get("bsdf", None) != None:
        mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[3] = mat.msfs_color_alpha_mix
        mat.node_tree.nodes["alpha_multiply"].inputs[1].default_value = mat.msfs_color_alpha_mix
        
def update_color_base_mix(self, context):
    mat = context.active_object.active_material
    #if mat.node_tree.nodes.get("bsdf", None) != None:
        #mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[3] = mat.msfs_color_alpha_mix
    mat.node_tree.nodes.get("albedo_tint").outputs[0].default_value[3] = mat.msfs_color_base_mix
    mat.node_tree.nodes["albedo_detail_mix"].inputs[0].default_value = mat.msfs_color_base_mix
    mat.node_tree.nodes["albedo_detail_mix"].inputs[2].default_value[3] = mat.msfs_color_base_mix

def update_color_emissive_mix(self, context):
    mat = context.active_object.active_material
    nodes = mat.node_tree.nodes

    bsdf = nodes.get("bsdf", None)
    emissive_tint = nodes.get("emissive_tint", None)

    if bsdf != None:
        bsdf.inputs.get('Emission').default_value[0] = mat.msfs_color_emissive_mix[0]
        bsdf.inputs.get('Emission').default_value[1] = mat.msfs_color_emissive_mix[1]
        bsdf.inputs.get('Emission').default_value[2] = mat.msfs_color_emissive_mix[2]
    if emissive_tint != None:
        emissive_tint.outputs[0].default_value[0] = mat.msfs_color_emissive_mix[0]
        emissive_tint.outputs[0].default_value[1] = mat.msfs_color_emissive_mix[1]
        emissive_tint.outputs[0].default_value[2] = mat.msfs_color_emissive_mix[2]

def update_color_sss(self, context):
    mat = context.active_object.active_material
    if mat.node_tree.nodes.get("bsdf", None) != None:
        mat.node_tree.nodes["bsdf"].inputs.get("Subsurface Color").default_value = mat.msfs_color_sss

def update_double_sided(self, context):
    mat = context.active_object.active_material
    mat.use_backface_culling = not mat.msfs_double_sided

def update_alpha_cutoff(self,context):
    mat = context.active_object.active_material
    mat.alpha_threshold = mat.msfs_alpha_cutoff

def update_normal_scale(self,context):
    mat = context.active_object.active_material
    if mat.node_tree.nodes.get("normal_map_node", None) != None:
        mat.node_tree.nodes["normal_map_node"].inputs["Strength"].default_value = mat.msfs_normal_scale

def update_detail_uv_scale(self,context):
    mat = context.active_object.active_material
    if mat.node_tree.nodes.get("detail_uv_scale", None) != None:
        mat.node_tree.nodes["detail_uv_scale"].inputs["Scale"].default_value[0] = mat.msfs_detail_uv_scale
        mat.node_tree.nodes["detail_uv_scale"].inputs["Scale"].default_value[1] = mat.msfs_detail_uv_scale
        mat.node_tree.nodes["detail_uv_scale"].inputs["Scale"].default_value[2] = mat.msfs_detail_uv_scale

def update_detail_uv_offset(self,context):
    mat=context.active_object.active_material
    if mat.node_tree.nodes.get("detail_uv_scale", None) != None:
        mat.node_tree.nodes["detail_uv_scale"].inputs["Location"].default_value[0] = mat.msfs_detail_uv_offset_x
        mat.node_tree.nodes["detail_uv_scale"].inputs["Location"].default_value[1] = mat.msfs_detail_uv_offset_y


class msfs_material_default_values:
    # This class stores the default values for MSFS material properties for ease of access
    # Probably isn't the best way of doing this, but it works and is convenient

    msfs_material_mode = "NONE"

    msfs_base_color_factor = [1.0, 1.0, 1.0, 1.0]
    msfs_color_albedo_mix = [1.0, 1.0, 1.0]
    msfs_emissive_factor = [0.0, 0.0, 0.0]
    msfs_color_alpha_mix = 1.0
    msfs_color_base_mix = 1.0
    
    msfs_alpha_mode = "OPAQUE"
    msfs_draw_order = 0
    msfs_double_sided = False
    msfs_dont_cast_shadows = False
    msfs_day_night_cycle = False

    msfs_use_pearl_effect = False
    msfs_pearl_shift = 0.0
    msfs_pearl_range = 0.0
    msfs_pearl_brightness = 0.0

    msfs_collision_material = False
    msfs_road_material = False

    msfs_uv_offset_u = 0.0
    msfs_uv_offset_v = 0.0
    msfs_uv_tiling_u = 1.0
    msfs_uv_tiling_v = 1.0
    msfs_uv_rotation = 0.0
    msfs_uv_clamp_u = False
    msfs_uv_clamp_v = False

    msfs_roughness_factor = 1.0
    msfs_metallic_factor = 1.0
    msfs_normal_scale = 1.0
    msfs_alpha_cutoff = 0.5

    msfs_detail_uv_scale = (
        1.0  # In 3DS Max the default is 2.0, might want to look more into this later
    )
    msfs_detail_uv_offset_u = 0.0
    msfs_detail_uv_offset_v = 0.0
    msfs_detail_normal_scale = 1.0

    msfs_blend_threshold = 0.1

    # Decal / Geo Decal (Frosted) - new not used
    msfs_decal_color_blend_factor = 1.0
    msfs_decal_metal_blend_factor = 1.0
    msfs_decal_normal_blend_factor = 1.0
    msfs_decal_roughness_blend_factor = 1.0
    msfs_decal_occlusion_blend_factor = 1.0
    msfs_decal_emissive_blend_factor = 1.0

    # Decal / Geo Decal (Frosted) = MSFSToolkit Legacy
    msfs_decal_blend_factor_color = 1.0
    msfs_decal_blend_factor_metal = 1.0
    msfs_decal_blend_factor_normal = 1.0
    msfs_decal_blend_factor_roughness = 1.0
    msfs_decal_blend_factor_occlusion = 1.0
    msfs_decal_blend_factor_emissive = 1.0

    # Windshield
    msfs_rain_drop_scale = 1.0
    msfs_wiper_1_state = 0.0
    msfs_wiper_2_state = 0.0

    # Glass
    msfs_glass_reflection_factor = 1.0
    msfs_glass_deformation_factor = 0.0

    # Parallax
    msfs_parallax_scale = 0.0
    msfs_parallax_room_size_x = 0.5
    msfs_parallax_room_size_y = 0.5
    msfs_parallax_room_number = 1.0
    msfs_parallax_corridor = False

    # Hair / SSS
    msfs_sss_color = [1.0, 1.0, 1.0, 1.0]

    # Fresnel
    msfs_fresnel_factor = 1.0
    msfs_fresnel_opacity_bias = 0.0


class msfs_material_properties(PropertyGroup):
    # Declare all custom material properties here

    Material.msfs_material_mode = EnumProperty(
        items=(
            ("NONE", "Disabled", ""),
            ("msfs_standard", "MSFS Standard", ""),
            ("msfs_anisotropic", "MSFS Anisotropic", ""),
            ("msfs_sss", "MSFS SSS", ""),
            ("msfs_glass", "MSFS Glass", ""),
            ("msfs_decal", "MSFS Decal", ""),
            ("msfs_clearcoat", "MSFS Clearcoat", ""),
            ("msfs_env_occluder", "MSFS Environment Occluder", ""),
            ("msfs_fake_terrain", "MSFS Fake Terrain", ""),
            ("msfs_fresnel", "MSFS Fresnel", ""),
            ("msfs_windshield", "MSFS Windshield", ""),
            ("msfs_porthole", "MSFS Porthole", ""),
            ("msfs_parallax", "MSFS Parallax", ""),
            ("msfs_geo_decal", "MSFS Geo Decal (Frosted)", ""),
            ("msfs_hair", "MSFS Hair", ""),
            ("msfs_invisible", "MSFS Invisible", ""),
        ),
        default=msfs_material_default_values.msfs_material_mode,
        update=switch_msfs_material,
    )

    # Material Parameters
    # Standard
    #Material.msfs_base_color_factor = FloatVectorProperty(
    #    name="Base Color",
    #    subtype="COLOR",
    #    min=0.0,
    #    max=1.0,
    #    size=4,
    #    default=msfs_material_default_values.msfs_base_color_factor,
    #    update=functions.update_base_color_factor,
    #)
    # MSFSToolkit Legacy
    Material.msfs_color_albedo_mix = FloatVectorProperty(
        name="Albedo Color",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=3,
        default=msfs_material_default_values.msfs_color_albedo_mix,
        update=update_color_albedo_mix,
    )
    #Material.msfs_emissive_factor = FloatVectorProperty(
    #    name="Emissive Color",
    #    subtype="COLOR",
    #    min=0.0,
    #    max=1.0,
    #    size=3,
    #    default=msfs_material_default_values.msfs_emissive_factor,
    #    update=functions.update_emissive_factor,
    #)
    # MSFSToolkit Legacy
    Material.msfs_color_emissive_mix = FloatVectorProperty(
        name="Emissive Color",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=3,
        default=msfs_material_default_values.msfs_emissive_factor,
        update=update_color_emissive_mix,
    )
    # MSFSToolkit Legacy
    Material.msfs_color_alpha_mix = FloatProperty(
        name="Alpha multiplier",
        default=msfs_material_default_values.msfs_color_alpha_mix,
        min=-1.0,
        max=1.0,
    )
    # MSFSToolkit Legacy
    Material.msfs_color_base_mix = FloatProperty(
        name="Base(Albedo) Color Mix",
        default=msfs_material_default_values.msfs_color_base_mix,
        min=-1.0,
        max=1.0,
    )

    #Material.msfs_alpha_mode = EnumProperty(
    #    name="Alpha Mode",
    #    items=(
    #        ("OPAQUE", "Opaque", ""),
    #        ("MASK", "Mask", ""),
    #        ("BLEND", "Blend", ""),
    #        ("DITHER", "Dither", ""),
    #    ),
    #    default=msfs_material_default_values.msfs_alpha_mode,
    #)
    # MSFSToolkit Legacy
    Material.msfs_blend_mode = EnumProperty(
        name="Alpha Mode",
        items=(
            ("OPAQUE", "Opaque", ""),
            ("MASK", "Mask", ""),
            ("BLEND", "Blend", ""),
            ("DITHER", "Dither", ""),
        ),
        default=msfs_material_default_values.msfs_alpha_mode,
    )
    Material.msfs_draw_order = IntProperty(
        name="Draw Order",
        default=msfs_material_default_values.msfs_draw_order,
        min=-999,
        max=999,
    )
    Material.msfs_double_sided = BoolProperty(
        name="Double Sided", default=msfs_material_default_values.msfs_double_sided
    )
    #Material.msfs_dont_cast_shadows = BoolProperty(
    #    name="Don't Cast Shadows",
    #    default=msfs_material_default_values.msfs_dont_cast_shadows,
    #)
    # MSFSToolkit Legacy
    Material.msfs_no_cast_shadow = BoolProperty(
        name="Don't Cast Shadows",
        default=msfs_material_default_values.msfs_dont_cast_shadows,
    )
    Material.msfs_day_night_cycle = BoolProperty(
        name="Day Night Cycle",
        default=msfs_material_default_values.msfs_day_night_cycle,
    )

    Material.msfs_use_pearl_effect = BoolProperty(
        name="Use Pearl Effect",
        default=msfs_material_default_values.msfs_use_pearl_effect,
    )
    Material.msfs_pearl_shift = FloatProperty(
        name="Color Shift",
        default=msfs_material_default_values.msfs_pearl_shift,
        min=-999.0,
        max=999.0,
    )
    Material.msfs_pearl_range = FloatProperty(
        name="Color Range",
        default=msfs_material_default_values.msfs_pearl_range,
        min=-999.0,
        max=999.0,
    )
    Material.msfs_pearl_brightness = FloatProperty(
        name="Color Brightness",
        default=msfs_material_default_values.msfs_pearl_brightness,
        min=-1.0,
        max=1.0,
    )

    Material.msfs_collision_material = BoolProperty(
        name="Collision Material",
        default=msfs_material_default_values.msfs_collision_material,
    )
    Material.msfs_road_material = BoolProperty(
        name="Road Material", default=msfs_material_default_values.msfs_road_material
    )

    Material.msfs_uv_offset_u = FloatProperty(
        name="UV Offset U",
        default=msfs_material_default_values.msfs_uv_offset_u,
        min=-10.0,
        max=10.0,
    )
    Material.msfs_uv_offset_v = FloatProperty(
        name="UV Offset V",
        default=msfs_material_default_values.msfs_uv_clamp_v,
        min=-10.0,
        max=10.0,
    )
    Material.msfs_uv_tiling_u = FloatProperty(
        name="UV Tiling U",
        default=msfs_material_default_values.msfs_uv_tiling_u,
        min=-10.0,
        max=10.0,
    )
    Material.msfs_uv_tiling_v = FloatProperty(
        name="UV Tiling V",
        default=msfs_material_default_values.msfs_uv_tiling_v,
        min=-10.0,
        max=10.0,
    )
    Material.msfs_uv_rotation = FloatProperty(
        name="UV Rotation",
        default=msfs_material_default_values.msfs_uv_rotation,
        min=-360.0,
        max=360.0,
    )
    #Material.msfs_uv_clamp_u = BoolProperty(
    #    name=" U", default=msfs_material_default_values.msfs_uv_clamp_u
    #)
    #Material.msfs_uv_clamp_v = BoolProperty(
    #    name=" V", default=msfs_material_default_values.msfs_uv_clamp_v
    #)
    # MSFSToolkit Legacy
    Material.msfs_uv_clamp_x = BoolProperty(
        name=" U", default=msfs_material_default_values.msfs_uv_clamp_u
    )
    Material.msfs_uv_clamp_y = BoolProperty(
        name=" V", default=msfs_material_default_values.msfs_uv_clamp_v
    )

    Material.msfs_roughness_factor = FloatProperty(
        name="Roughness Factor",
        default=msfs_material_default_values.msfs_roughness_factor,
        min=0.0,
        max=1.0,
    )
    #Material.msfs_metallic_factor = FloatProperty(
    #    name="Metallic Factor",
    #    default=msfs_material_default_values.msfs_metallic_factor,
    #    min=0.0,
    #    max=1.0,
    #)
    # MSFSToolkit Legacy
    Material.msfs_roughness_scale = FloatProperty(
        name="Roughness Factor",
        default=msfs_material_default_values.msfs_roughness_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_metallic_scale = FloatProperty(
        name="Metallic Factor",
        default=msfs_material_default_values.msfs_metallic_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_normal_scale = FloatProperty(
        name="Normal Scale",
        default=msfs_material_default_values.msfs_normal_scale,
        min=0.0,
        max=1.0,
    )
    Material.msfs_alpha_cutoff = FloatProperty(
        name="Alpha Cutoff",
        default=msfs_material_default_values.msfs_alpha_cutoff,
        min=0.0,
        max=1.0,
    )  # This is only used with the mask alpha mode

    Material.msfs_detail_uv_scale = FloatProperty(
        name="Detail UV Scale",
        default=msfs_material_default_values.msfs_detail_uv_scale,
        min=0.01,
        max=100.0,
    )
    Material.msfs_detail_uv_offset_u = FloatProperty(
        name=" U",
        default=msfs_material_default_values.msfs_detail_uv_offset_u,
        min=-10.0,
        max=10.0,
    )
    Material.msfs_detail_uv_offset_v = FloatProperty(
        name=" V",
        default=msfs_material_default_values.msfs_detail_uv_offset_v,
        min=-10.0,
        max=10.0,
    )
    # MSFSToolkit Legacy
    Material.msfs_detail_uv_offset_x = FloatProperty(
        name=" U",
        default=msfs_material_default_values.msfs_detail_uv_offset_u,
        min=-10.0,
        max=10.0,
    )
    Material.msfs_detail_uv_offset_y = FloatProperty(
        name=" V",
        default=msfs_material_default_values.msfs_detail_uv_offset_v,
        min=-10.0,
        max=10.0,
    )
    Material.msfs_detail_normal_scale = FloatProperty(
        name="Detail Normal Scale",
        default=msfs_material_default_values.msfs_detail_uv_scale,
        min=0.0,
        max=1.0,
    )

    Material.msfs_blend_threshold = FloatProperty(
        name="Blend Threshold",
        default=msfs_material_default_values.msfs_blend_threshold,
        min=0.001,
        max=1.0,
    )
    #Decal parameters:
    Material.msfs_decal_blend_factor_color = bpy.props.FloatProperty(name="Color", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_metal = bpy.props.FloatProperty(name="Metal", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_normal = bpy.props.FloatProperty(name="Normal", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_roughness = bpy.props.FloatProperty(name="Roughness", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_occlusion = bpy.props.FloatProperty(name="Occlusion", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_emissive = bpy.props.FloatProperty(name="Emissive", min=0.0,max=1.0,default=1.0)

    # Decal / Geo Decal (Frosted) - New not used
    Material.msfs_decal_color_blend_factor = FloatProperty(
        name="Color",
        default=msfs_material_default_values.msfs_decal_color_blend_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_decal_metal_blend_factor = FloatProperty(
        name="Metal",
        default=msfs_material_default_values.msfs_decal_metal_blend_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_decal_normal_blend_factor = FloatProperty(
        name="Normal",
        default=msfs_material_default_values.msfs_decal_normal_blend_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_decal_roughness_blend_factor = FloatProperty(
        name="Roughness",
        default=msfs_material_default_values.msfs_decal_roughness_blend_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_decal_occlusion_blend_factor = FloatProperty(
        name="Occlusion",
        default=msfs_material_default_values.msfs_decal_occlusion_blend_factor,
        min=0.0,
        max=1.0,
    )  # This is Blast Sys on Geo Decals
    Material.msfs_decal_emissive_blend_factor = FloatProperty(
        name="Emissive",
        default=msfs_material_default_values.msfs_decal_emissive_blend_factor,
        min=0.0,
        max=1.0,
    )  # This is Melt Sys on Geo Decals
    # Decal / Geo Decal (Frosted) - MSFSToolkit Legacy
    Material.msfs_geo_decal_blend_factor_color = FloatProperty(
        name="Color",
        default=msfs_material_default_values.msfs_decal_color_blend_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_geo_decal_blend_factor_metal = FloatProperty(
        name="Metal",
        default=msfs_material_default_values.msfs_decal_metal_blend_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_geo_decal_blend_factor_normal = FloatProperty(
        name="Normal",
        default=msfs_material_default_values.msfs_decal_normal_blend_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_geo_decal_blend_factor_roughness = FloatProperty(
        name="Roughness",
        default=msfs_material_default_values.msfs_decal_roughness_blend_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_geo_decal_blend_factor_blast_sys = FloatProperty(
        name="Occlusion (Legacy Blast)",
        default=msfs_material_default_values.msfs_decal_occlusion_blend_factor,
        min=0.0,
        max=1.0,
    )  # This is Blast Sys on Geo Decals
    Material.msfs_geo_decal_blend_factor_melt_sys = FloatProperty(
        name="Emissive (Legacy Melt)",
        default=msfs_material_default_values.msfs_decal_emissive_blend_factor,
        min=0.0,
        max=1.0,
    )  # This is Melt Sys on Geo Decals

    # Windshield
    Material.msfs_rain_drop_scale = FloatProperty(
        name="Rain Drop Scale",
        default=msfs_material_default_values.msfs_rain_drop_scale,
        min=0.0,
        max=100.0,
    )
    Material.msfs_wiper_1_state = FloatProperty(
        name="Wiper 1 State",
        default=msfs_material_default_values.msfs_wiper_1_state,
        min=0.0,
        max=1.0,
    )
    Material.msfs_wiper_2_state = FloatProperty(
        name="Wiper 2 State",
        default=msfs_material_default_values.msfs_wiper_2_state,
        min=0.0,
        max=1.0,
    )  # The 3DS Max plugin has up to 4 states, but the last 2 aren't visible

    # Glass
    #Material.msfs_glass_reflection_factor = FloatProperty(
    #    name="Glass Reflection Mask Factor",
    #    default=msfs_material_default_values.msfs_glass_reflection_factor,
    #    min=0.0,
    #    max=1.0,
    #)
    # MSFSToolkit Legacy
    Material.msfs_glass_reflection_mask_factor = FloatProperty(
        name="Glass Reflection Mask Factor",
        default=msfs_material_default_values.msfs_glass_reflection_factor,
        min=0.0,
        max=1.0,
    )
    Material.msfs_glass_deformation_factor = FloatProperty(
        name="Glass Deformation Factor",
        default=msfs_material_default_values.msfs_glass_deformation_factor,
        min=0.0,
        max=1.0,
    )

    # Parallax
    Material.msfs_parallax_scale = FloatProperty(
        name="Parallax Scale",
        default=msfs_material_default_values.msfs_parallax_scale,
        min=0.0,
        max=1.0,
    )
    Material.msfs_parallax_room_size_x = FloatProperty(
        name="Parallax Room Size X",
        default=msfs_material_default_values.msfs_parallax_room_size_x,
        min=0.01,
        max=10.0,
    )
    Material.msfs_parallax_room_size_y = FloatProperty(
        name="Parallax Room Size Y",
        default=msfs_material_default_values.msfs_parallax_room_size_y,
        min=0.01,
        max=10.0,
    )
    Material.msfs_parallax_room_number = FloatProperty(
        name="Parallax Room Number XY",
        default=msfs_material_default_values.msfs_parallax_room_number,
        min=1.0,
        max=16.0,
    )
    Material.msfs_parallax_corridor = BoolProperty(
        name="Corridor", default=msfs_material_default_values.msfs_parallax_corridor
    )

    # Hair / SSS
    Material.msfs_sss_color = FloatVectorProperty(
        name="SSS Color",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
        default=msfs_material_default_values.msfs_sss_color,
    )  # This is disabled in the 3DS Max plugin

    # Fresnel
    Material.msfs_fresnel_factor = FloatProperty(
        name="Fresnel Factor",
        default=msfs_material_default_values.msfs_fresnel_factor,
        min=0.001,
        max=100.0,
    )
    Material.msfs_fresnel_opacity_bias = FloatProperty(
        name="Fresnel Opacity Bias",
        default=msfs_material_default_values.msfs_fresnel_opacity_bias,
        min=-1.0,
        max=1.0,
    )

    # Textures
    #Material.msfs_base_color_texture = PointerProperty(
    #    type=Image, name="Base Color", update=functions.update_base_color_texture
    #)
    Material.msfs_albedo_texture = PointerProperty(
        type=Image, name="Base Color", update=match_albedo
    )
    #Material.msfs_comp_texture = PointerProperty(
    #    type=Image,
    #    name="Composite (Occlusion (R), Roughness (G), Metalness (B))",
    #    update=functions.update_comp_texture,
    #)
    # MSFSToolkit Legacy
    Material.msfs_metallic_texture = PointerProperty(
        type=Image,
        name="Composite (Occlusion (R), Roughness (G), Metalness (B))",
        update=match_metallic,
    )
    Material.msfs_normal_texture = PointerProperty(
        type=Image, name="Normal", update=match_normal
    )
    Material.msfs_emissive_texture = PointerProperty(
        type=Image, name="Emissive", update=match_emissive
    )
    #Material.msfs_detail_color_texture = PointerProperty(
    #    type=Image, name="Detail Color", update=functions.update_base_color_texture
    #)
    # MSFSToolkit Legacy
    Material.msfs_detail_albedo_texture = PointerProperty(
        type=Image, name="Detail Color", update=match_detail_albedo
    )
    #Material.msfs_detail_comp_texture = PointerProperty(
    #    type=Image,
    #    name="Detail Composite (Occlusion (R), Roughness (G), Metalness (B))",
    #    update=functions.update_comp_texture,
    #)
    # MSFSToolkit Legacy
    Material.msfs_detail_metallic_texture = PointerProperty(
        type=Image,
        name="Detail Composite (Occlusion (R), Roughness (G), Metalness (B))",
        update=match_detail_metallic,
    )
    Material.msfs_detail_normal_texture = PointerProperty(
        type=Image, name="Detail Normal", update=match_detail_metallic
    )
    Material.msfs_blend_mask_texture = PointerProperty(
        type=Image, name="Blend Mask", update=match_blend_mask
    )
    #Material.msfs_wetness_ao_texture = PointerProperty(
    #    type=Image, name="Wetness AO (Aniso Dir)", update=functions.update_wetness_ao_texture
    #)  # this is anisotropic direction but the 3DS Max plugin has the variable name as wetness_ao
    # MSFSToolkit Legacy
    Material.msfs_anisotropic_direction_texture = PointerProperty(
        type=Image, name="Aniso Direction (Wetness AO)", update=match_anisotropic_direction
    )  # this is anisotropic direction but the 3DS Max plugin has the variable name as wetness_ao
    #Material.msfs_dirt_texture = PointerProperty(
    #    type=Image, name="Dirt (Clearcoat)", update=functions.update_dirt_texture
    #)  # similar to wetness ao, this is clearcoat but the 3DS Max plugin has the variable name as dirt
    # MSFSToolkit Legacy
    Material.msfs_clearcoat_texture = PointerProperty(
        type=Image, name="Clearcoat (Dirt)", update=match_clearcoat
    )  # similar to wetness ao, this is clearcoat but the 3DS Max plugin has the variable name as dirt
    Material.msfs_height_map_texture = PointerProperty(
        type=Image, name="Height Map"
    )  # Doesn't seem to be enabled yet in the 3DS Max plugin
    Material.msfs_behind_glass_texture = PointerProperty(type = Image, name = "Behind glass Albedo map", update = match_behind_glass)



    # Option visibility
    # Standard
    #Material.msfs_show_colors = BoolProperty(name="show_colors", default=False)
    #Material.msfs_show_emissive_color = BoolProperty(
    #    name="show_emissive_color", default=False
    #)

    #Material.msfs_show_alpha_mode = BoolProperty(name="show_alpha_mode", default=False)

    #Material.msfs_show_render_options = BoolProperty(
    #    name="show_render_options", default=False
    #)
    #Material.msfs_show_day_night_cycle = BoolProperty(
    #    name="show_day_night_cycle", default=False
    #)

    Material.msfs_show_pearl = BoolProperty(name="show_pearl", default=False)

    #Material.msfs_show_gameplay_options = BoolProperty(
    #    name="show_gameplay_options", default=False
    #)

    #Material.msfs_show_uv_options = BoolProperty(name="show_uv_options", default=False)

    #Material.msfs_show_material_options = BoolProperty(
    #    name="show_material_options", default=False
    #)
    #Material.msfs_show_material_detail_options = BoolProperty(
    #    name="show_material_detail_options", default=False
    #)
    #Material.msfs_show_blend_threshold = BoolProperty(
    #    name="show_blend_threshold", default=False
    #)

    # Decal / Geo Decal (Frosted)
    #Material.msfs_show_decal_blend_factors = BoolProperty(
    #    name="show_decal_blend_factors", default=False
    #)

    # Windshield
    Material.msfs_show_windshield_options = BoolProperty(
        name="show_windshield_options", default=False
    )

    # Glass
    #Material.msfs_show_glass_options = BoolProperty(
    #    name="show_glass_options", default=False
    #)

    # Parallax
    #Material.msfs_show_parallax_options = BoolProperty(
    #    name="show_parallax_options", default=False
    #)

    # Hair / SSS
    #Material.msfs_show_sss_color = BoolProperty(name="show_sss_property", default=False)

    # Fresnel
    #Material.msfs_show_fresnel_options = BoolProperty(
    #    name="show_fresnel_options", default=False
    #)

    # Textures
    #Material.msfs_show_base_color_texture = BoolProperty(
    #    name="show_base_color_texture", default=False
    #)
    #Material.msfs_show_comp_texture = BoolProperty(
    #    name="show_comp_texture", default=False
    #)
    #Material.msfs_show_normal_texture = BoolProperty(
    #    name="show_normal_texture", default=False
    #)
    #Material.msfs_show_emissive_texture = BoolProperty(
    #    name="show_emissive_texture", default=False
    #)
    #Material.msfs_show_detail_color_texture = BoolProperty(
    #    name="show_detail_color_texture", default=False
    #)
    #Material.msfs_show_detail_comp_texture = BoolProperty(
    #    name="show_detail_comp_texture", default=False
    #)
    #Material.msfs_show_detail_normal_texture = BoolProperty(
    #    name="show_detail_normal_texture", default=False
    #)
    #Material.msfs_show_blend_mask_texture = BoolProperty(
    #    name="show_blend_mask_texture", default=False
    #)
    Material.msfs_show_wetness_ao_texture = BoolProperty(
        name="show_wetness_ao_texture", default=False
    )
    Material.msfs_show_dirt_texture = BoolProperty(
        name="show_dirt_texture", default=False
    )
    Material.msfs_show_height_map_texture = BoolProperty(
        name="show_height_map_texture", default=False
    )
    # Legacy MSFSToolkit show params
    # Some flags to control the visibility of all of the paramters in the UI. 
    # Note: they don't control the actualy material parameters, only whether or 
    # not those parameters are being displayed. 
    
    # albedo Base color tint
    Material.msfs_show_tint = bpy.props.BoolProperty(name="show_tint",default=False)
    Material.msfs_show_sss_color = bpy.props.BoolProperty(name="show_sss_color",default=False)

    # parameters
    Material.msfs_show_glass_parameters = bpy.props.BoolProperty(name="show_glass_parameters",default=False)
    Material.msfs_show_decal_parameters = bpy.props.BoolProperty(name="show_decal_parameters",default=False)
    Material.msfs_show_fresnel_parameters = bpy.props.BoolProperty(name="show_fresnel_parameters",default=False)
    Material.msfs_show_parallax_parameters = bpy.props.BoolProperty(name="show_parallax_parameters",default=False)
    Material.msfs_show_geo_decal_parameters = bpy.props.BoolProperty(name="show_geo_decal_parameters",default=False)

    # Textures?
    Material.msfs_show_albedo = bpy.props.BoolProperty(name="show_albedo",default=False)
    Material.msfs_show_metallic = bpy.props.BoolProperty(name="show_metallic",default=False)
    Material.msfs_show_normal = bpy.props.BoolProperty(name="show_normal",default=False)
    Material.msfs_show_emissive = bpy.props.BoolProperty(name="show_emissive",default=False)
    Material.msfs_show_detail_albedo = bpy.props.BoolProperty(name="show_detail_albedo",default=False)
    Material.msfs_show_detail_metallic = bpy.props.BoolProperty(name="show_detail_metallic",default=False)
    Material.msfs_show_detail_normal = bpy.props.BoolProperty(name="show_detail_normal",default=False)
    Material.msfs_show_blend_mask = bpy.props.BoolProperty(name="show_blend_mask",default=False)
    Material.msfs_show_anisotropic_direction = bpy.props.BoolProperty(name="show_anisotropic_direction",default=False)
    Material.msfs_show_clearcoat = bpy.props.BoolProperty(name="show_clearcoat",default=False)
    Material.msfs_show_behind_glass = bpy.props.BoolProperty(name="show_behind_glass",default=False)
    Material.msfs_show_wiper_mask = bpy.props.BoolProperty(name="show_wiper_mask",default=False)

    # Render options
    # blend mode is alpha mode
    Material.msfs_show_blend_mode = bpy.props.BoolProperty(name="show_blend_mode",default=False)
    Material.msfs_show_draworder = bpy.props.BoolProperty(name="show_draworder",default=False)
    Material.msfs_show_no_cast_shadow = bpy.props.BoolProperty(name="show_no_cast_shadow",default=False)
    Material.msfs_show_double_sided = bpy.props.BoolProperty(name="show_double_sided",default=False)
    Material.msfs_show_responsive_aa = bpy.props.BoolProperty(name="show_responsive_aa",default=False)
    Material.msfs_show_day_night_cycle = bpy.props.BoolProperty(name="show_day_night_cycle",default=False)

    # Gameplay
    Material.msfs_show_collision_material = bpy.props.BoolProperty(name="show_collision_material",default=False)
    Material.msfs_show_road_material = bpy.props.BoolProperty(name="show_road_material",default=False)

    # UV options
    Material.msfs_show_ao_use_uv2 = bpy.props.BoolProperty(name="show_ao_use_uv2",default=False)
    Material.msfs_show_uv_clamp = bpy.props.BoolProperty(name="show_uv_clamp",default=False)

    Material.msfs_show_alpha_cutoff = bpy.props.BoolProperty(name="show_alpha_cutoff",default=False)
    Material.msfs_show_blend_threshold = bpy.props.BoolProperty(name="show_blend_threshold",default=False)

    # For importing
    Material.is_import = BoolProperty(name="is_import", default=False)


classes = (msfs_material_properties,)

register, unregister = bpy.utils.register_classes_factory(classes)
