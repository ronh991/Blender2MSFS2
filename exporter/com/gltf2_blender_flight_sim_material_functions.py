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
import numpy as np
from bpy.types import Material
from ..com.gltf2_blender_material_helpers import get_gltf_node_name
from . import gltf2_blender_flight_sim_material_utilities as utilities
from ..com import gltf2_io_debug

### Material Creation
def create_material(self, context):
    if not self.is_import:
        self.use_nodes = True
        while self.node_tree.nodes:  # clear all nodes
            self.node_tree.nodes.remove(self.node_tree.nodes[0])

        bsdf_node = self.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        bsdf_node.location = 10, 300

        make_output_nodes(
            self,
            location=(250, 260),
            shader_socket=bsdf_node.outputs[0],
            make_emission_socket=False,
            make_alpha_socket=False,
        )


# => [Add Emission] => [Mix Alpha] => [Material Output]
def make_output_nodes(
    mat,
    location,
    shader_socket,
    make_emission_socket,
    make_alpha_socket,):
    """
    Creates the Material Output node and connects shader_socket to it.
    If requested, it can also create places to hookup the emission/alpha
    in between shader_socket and the Output node too.

    :return: a pair containing the sockets you should put emission and alpha
    in (None if not requested).
    """
    x, y = location
    emission_socket = None
    alpha_socket = None

    # Create an Emission node and add it to the shader.
    if make_emission_socket:
        # Emission
        node = mat.node_tree.nodes.new("ShaderNodeEmission")
        node.location = x + 50, y + 250
        # Inputs
        emission_socket = node.inputs[0]
        # Outputs
        emission_output = node.outputs[0]

        # Add
        node = mat.node_tree.nodes.new("ShaderNodeAddShader")
        node.location = x + 250, y + 160
        # Inputs
        mat.node_tree.links.new(node.inputs[0], emission_output)
        mat.node_tree.links.new(node.inputs[1], shader_socket)
        # Outputs
        shader_socket = node.outputs[0]

        if make_alpha_socket:
            x += 200
            y += 175
        else:
            x += 380
            y += 125

    # Mix with a Transparent BSDF. Mixing factor is the alpha value.
    if make_alpha_socket:
        # Transparent BSDF
        node = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
        node.location = x + 100, y - 350
        # Outputs
        transparent_out = node.outputs[0]

        # Mix
        node = mat.node_tree.nodes.new("ShaderNodeMixShader")
        node.location = x + 340, y - 180
        # Inputs
        alpha_socket = node.inputs[0]
        mat.node_tree.links.new(node.inputs[1], transparent_out)
        mat.node_tree.links.new(node.inputs[2], shader_socket)
        # Outputs
        shader_socket = node.outputs[0]

        x += 480
        y -= 210

    # Material output
    node = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    node.location = x + 70, y + 10
    # Outputs
    mat.node_tree.links.new(node.inputs[0], shader_socket)

    return emission_socket, alpha_socket


### Texture Functions
def texture(
    mat,
    texture,
    location,  # Upper-right corner of the TexImage node
    label,  # Label for the TexImg node
    color_socket=None,
    alpha_socket=None,
    is_data=False,):
    """Creates nodes for a TextureInfo and hooks up the color/alpha outputs."""
    x, y = location

    # Image Texture
    tex_img = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex_img.location = x - 240, y
    tex_img.label = label
    tex_img.image = texture

    # Set colorspace for data images
    if is_data:
        if tex_img.image:
            tex_img.image.colorspace_settings.is_data = True

    # Outputs
    if color_socket is not None:
        mat.node_tree.links.new(color_socket, tex_img.outputs["Color"])
    if alpha_socket is not None:
        mat.node_tree.links.new(alpha_socket, tex_img.outputs["Alpha"])

    return tex_img


#      [Texture] => [Mix Colors] => [Color Factor] =>
# [Vertex Color] => [Mix Alphas] => [Alpha Factor] =>
def base_color(
    mat,
    location,
    color_socket,
    alpha_socket=None,):
    """Handle base color (= baseColorTexture * vertexColor * baseColorFactor)."""
    x, y = location
    base_color_factor = list(mat.msfs_base_color_factor)
    base_color_texture = mat.msfs_base_color_texture
    detail_color_texture = mat.msfs_detail_color_texture

    if base_color_factor is None:
        base_color_factor = [1, 1, 1, 1]

    if base_color_texture is None and detail_color_texture is None:
        color_socket.default_value = base_color_factor[:3] + [1]
        if alpha_socket is not None:
            alpha_socket.default_value = base_color_factor[3]
        return

    # Mix in base color factor
    needs_color_factor = base_color_factor[:3] != [1, 1, 1]
    needs_alpha_factor = base_color_factor[3] != 1.0 and alpha_socket is not None
    if needs_color_factor or needs_alpha_factor:
        if needs_color_factor:
            node = mat.node_tree.nodes.new("ShaderNodeMixRGB")
            node.label = "Color Factor"
            node.location = x - 140, y
            node.blend_type = "MULTIPLY"
            # Outputs
            mat.node_tree.links.new(color_socket, node.outputs[0])
            # Inputs
            node.inputs["Fac"].default_value = 1.0
            color_socket = node.inputs["Color1"]
            node.inputs["Color2"].default_value = base_color_factor[:3] + [1]

        if needs_alpha_factor:
            node = mat.node_tree.nodes.new("ShaderNodeMath")
            node.label = "Alpha Factor"
            node.location = x - 140, y - 200
            # Outputs
            mat.node_tree.links.new(alpha_socket, node.outputs[0])
            # Inputs
            node.operation = "MULTIPLY"
            alpha_socket = node.inputs[0]
            node.inputs[1].default_value = base_color_factor[3]

        x -= 200

    # Mix detail map
    detail_color_socket = None
    base_alpha_socket = None  # We need this in case there is an alpha mix, because we still want to keep the reference to the alpha socket on the BSDF node
    detail_alpha_socket = None
    if base_color_texture is not None and detail_color_texture is not None:
        if color_socket is not None:
            node = mat.node_tree.nodes.new("ShaderNodeMixRGB")
            node.label = "Detail Color Mix"
            node.location = (x - 140, y) if alpha_socket is None else (x - 140, y + 100)
            node.blend_type = "MULTIPLY"
            # Outputs
            mat.node_tree.links.new(color_socket, node.outputs[0])
            # Inputs
            node.inputs["Fac"].default_value = 1.0
            color_socket = node.inputs["Color1"]
            detail_color_socket = node.inputs["Color2"]
            node.inputs["Color2"].default_value = [1, 1, 1, 1]

        if alpha_socket is not None:
            node = mat.node_tree.nodes.new("ShaderNodeMixRGB")
            node.label = "Detail Alpha Mix"
            node.location = (x - 140, y) if alpha_socket is None else (x - 140, y - 100)
            node.blend_type = "MULTIPLY"
            # Outputs
            mat.node_tree.links.new(alpha_socket, node.outputs[0])
            # Inputs
            node.inputs["Fac"].default_value = 1.0
            base_alpha_socket = node.inputs["Color1"]
            detail_alpha_socket = node.inputs["Color2"]
            node.inputs["Color2"].default_value = [1, 1, 1, 1]

        x -= 200

    if base_alpha_socket is None:
        base_alpha_socket = alpha_socket

    # Texture
    if base_color_texture is not None:
        texture(
            mat,
            texture=base_color_texture,
            label="BASE COLOR",
            location=(x, y) if detail_color_texture is None else (x, y + 150),
            color_socket=color_socket,
            alpha_socket=base_alpha_socket,
        )

    if detail_color_texture is not None:
        texture(
            mat,
            texture=detail_color_texture,
            label="DETAIL COLOR",
            location=(x, y) if base_color_texture is None else (x, y - 150),
            color_socket=detail_color_socket
            if base_color_texture is not None
            else color_socket,
            alpha_socket=detail_alpha_socket
            if base_color_texture is not None
            else base_alpha_socket,
        )


# [Texture] => [Separate GB] => [Metal/Rough Factor] =>
def metallic_roughness(mat, location, metallic_socket, roughness_socket):
    x, y = location

    comp_texture = mat.msfs_comp_texture
    detail_comp_texture = mat.msfs_detail_comp_texture
    metal_factor = mat.msfs_metallic_factor
    rough_factor = mat.msfs_roughness_factor

    if metal_factor is None:
        metal_factor = 1.0
    if rough_factor is None:
        rough_factor = 1.0

    if comp_texture is None and detail_comp_texture is None:
        metallic_socket.default_value = metal_factor
        roughness_socket.default_value = rough_factor
        return

    if metal_factor != 1.0 or rough_factor != 1.0:
        # Mix metal factor
        if metal_factor != 1.0:
            node = mat.node_tree.nodes.new("ShaderNodeMath")
            node.label = "Metallic Factor"
            node.location = x - 140, y
            node.operation = "MULTIPLY"
            # Outputs
            mat.node_tree.links.new(metallic_socket, node.outputs[0])
            # Inputs
            metallic_socket = node.inputs[0]
            node.inputs[1].default_value = metal_factor

        # Mix rough factor
        if rough_factor != 1.0:
            node = mat.node_tree.nodes.new("ShaderNodeMath")
            node.label = "Roughness Factor"
            node.location = x - 140, y - 200
            node.operation = "MULTIPLY"
            # Outputs
            mat.node_tree.links.new(roughness_socket, node.outputs[0])
            # Inputs
            roughness_socket = node.inputs[0]
            node.inputs[1].default_value = rough_factor

        x -= 200

    # Separate RGB
    node = mat.node_tree.nodes.new("ShaderNodeSeparateRGB")
    node.location = x - 150, y - 75
    # Outputs
    mat.node_tree.links.new(metallic_socket, node.outputs["B"])
    mat.node_tree.links.new(roughness_socket, node.outputs["G"])
    # Inputs
    color_socket = node.inputs[0]

    x -= 200

    # Mix detail map
    detail_color_socket = None
    if comp_texture is not None and detail_comp_texture is not None:
        node = mat.node_tree.nodes.new("ShaderNodeMixRGB")
        node.label = "Detail Comp Mix"
        node.location = x - 140, y
        node.blend_type = "MULTIPLY"
        # Outputs
        mat.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs["Fac"].default_value = 1.0
        color_socket = node.inputs["Color1"]
        detail_color_socket = node.inputs["Color2"]
        node.inputs["Color2"].default_value = [1, 1, 1, 1]

        x -= 200

    if comp_texture is not None:
        texture(
            mat,
            texture=comp_texture,
            label="METALLIC ROUGHNESS",
            location=(x, y) if detail_comp_texture is None else (x, y + 150),
            is_data=True,
            color_socket=color_socket,
        )

    if detail_comp_texture is not None:
        texture(
            mat,
            texture=detail_comp_texture,
            label="DETAIL METALLIC ROUGHNESS",
            location=(x, y) if comp_texture is None else (x, y - 150),
            is_data=True,
            color_socket=detail_color_socket
            if comp_texture is not None
            else color_socket,
        )


# [Texture] => [Separate R] => [Mix Strength] =>
def occlusion(mat, location, occlusion_socket):
    x, y = location

    comp_texture = mat.msfs_comp_texture
    detail_comp_texture = mat.msfs_detail_comp_texture
    if comp_texture is None:
        return

    # We don't need to add strength as the Max exporter always has it at 1.0

    # Separate RGB
    node = mat.node_tree.nodes.new("ShaderNodeSeparateRGB")
    node.location = x - 150, y - 75
    # Outputs
    mat.node_tree.links.new(occlusion_socket, node.outputs["R"])
    # Inputs
    color_socket = node.inputs[0]

    x -= 200

    # Mix detail map
    detail_color_socket = None
    if comp_texture is not None and detail_comp_texture is not None:
        node = mat.node_tree.nodes.new("ShaderNodeMixRGB")
        node.label = "Detail Occlusion Mix"
        node.location = x - 140, y
        node.blend_type = "MULTIPLY"
        # Outputs
        mat.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs["Fac"].default_value = 1.0
        color_socket = node.inputs["Color1"]
        detail_color_socket = node.inputs["Color2"]
        node.inputs["Color2"].default_value = [1, 1, 1, 1]

        x -= 200

    if comp_texture is not None:
        texture(
            mat,
            texture=comp_texture,
            label="OCCLUSION",
            location=(x, y) if detail_comp_texture is None else (x, y + 150),
            is_data=True,
            color_socket=color_socket,
        )

    if detail_comp_texture is not None:
        texture(
            mat,
            texture=detail_comp_texture,
            label="DETAIL OCCLUSION",
            location=(x, y) if comp_texture is None else (x, y - 150),
            is_data=True,
            color_socket=detail_color_socket
            if comp_texture is not None
            else color_socket,
        )


# [Texture] => [Normal Map] =>
def normal(mat, location, normal_socket):
    x, y = location
    normal_texture = mat.msfs_normal_texture
    detail_normal_texture = mat.msfs_detail_normal_texture

    if normal_texture is None and detail_normal_texture is None:
        return

    # Normal map
    node = mat.node_tree.nodes.new("ShaderNodeNormalMap")
    node.location = x - 150, y - 40
    # Set UVMap
    node.uv_map = "UVMap"
    # Outputs
    mat.node_tree.links.new(normal_socket, node.outputs["Normal"])
    # Inputs
    color_socket = node.inputs["Color"]

    x -= 200

    # Mix detail map
    detail_color_socket = None
    if normal_texture is not None and detail_normal_texture is not None:
        node = mat.node_tree.nodes.new("ShaderNodeMixRGB")
        node.label = "Detail Normal Mix"
        node.location = x - 140, y
        node.blend_type = "MULTIPLY"
        # Outputs
        mat.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs["Fac"].default_value = 1.0
        color_socket = node.inputs["Color1"]
        detail_color_socket = node.inputs["Color2"]
        node.inputs["Color2"].default_value = [1, 1, 1, 1]

        x -= 200

    if normal_texture is not None:
        texture(
            mat,
            texture=normal_texture,
            label="NORMALMAP",
            location=(x, y) if detail_normal_texture is None else (x, y + 150),
            is_data=True,
            color_socket=color_socket,
        )

    if detail_normal_texture is not None:
        texture(
            mat,
            texture=detail_normal_texture,
            label="DETAIL NORMALMAP",
            location=(x, y) if normal_texture is None else (x, y - 150),
            is_data=True,
            color_socket=detail_color_socket
            if normal_texture is not None
            else color_socket,
        )


# [Texture] => [Emissive Factor] =>
def emission(
    mat,
    location,
    color_socket,):
    
    x, y = location
    emissive_texture = mat.msfs_emissive_texture
    emissive_factor = list(mat.msfs_emissive_factor)

    if color_socket is None:
        return

    if emissive_texture is None:
        color_socket.default_value = emissive_factor + [1]
        return

    if emissive_factor != [1, 1, 1]:
        node = mat.node_tree.nodes.new("ShaderNodeMixRGB")
        node.label = "Emissive Factor"
        node.location = x - 140, y
        node.blend_type = "MULTIPLY"
        # Outputs
        mat.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs["Fac"].default_value = 1.0
        color_socket = node.inputs["Color1"]
        node.inputs["Color2"].default_value = emissive_factor + [1]

        x -= 200

    texture(
        mat,
        texture=emissive_texture,
        label="EMISSIVE",
        location=(x, y),
        color_socket=color_socket,
    )


# [Texture] => [Detail Texture Factor] =>
def blend_mask(mat, location):
    x, y = location
    blend_mask_texture = mat.msfs_blend_mask_texture

    if blend_mask_texture is None:
        return

    (
        base_color_socket,
        comp_socket,
        occlusion_socket,
        normal_socket,
    ) = utilities.get_detail_factor_sockets(mat)

    if (
        base_color_socket is None
        and comp_socket is None
        and occlusion_socket is None
        and normal_socket is None
    ):
        return

    blend_mask = texture(
        mat,
        texture=blend_mask_texture,
        label="BLEND MASK",
        location=(x, y),
    )

    if (
        blend_mask_texture.channels > 3
    ):  # if there is more than 3 channels, we know that an alpha channel is present
        # if the entire alpha layer is all white we treat it as no alpha channel, and use the color channels as the blend mask
        width = blend_mask_texture.size[0]
        height = blend_mask_texture.size[1]
        pixels = np.empty(width * height * 4, dtype=np.float32)
        blend_mask_texture.pixels.foreach_get(pixels)
        pixels = pixels.reshape((-1, 4))
        alpha_pixels = pixels[:, -1]
        if not all(alpha_pixels == 1.0):  # 1.0 is a white pixel
            if base_color_socket is not None:
                mat.node_tree.links.new(base_color_socket, blend_mask.outputs["Alpha"])
            if comp_socket is not None:
                mat.node_tree.links.new(comp_socket, blend_mask.outputs["Alpha"])
            if occlusion_socket is not None:
                mat.node_tree.links.new(occlusion_socket, blend_mask.outputs["Alpha"])
            if normal_socket is not None:
                mat.node_tree.links.new(normal_socket, blend_mask.outputs["Alpha"])
            return

    # use color output for blend mask
    if base_color_socket is not None:
        mat.node_tree.links.new(base_color_socket, blend_mask.outputs["Color"])
    if comp_socket is not None:
        mat.node_tree.links.new(comp_socket, blend_mask.outputs["Color"])
    if occlusion_socket is not None:
        mat.node_tree.links.new(occlusion_socket, blend_mask.outputs["Color"])
    if normal_socket is not None:
        mat.node_tree.links.new(normal_socket, blend_mask.outputs["Color"])


# [Texture] => [Wetness AO] =>
def wetness_ao(
    mat,
    location,
    wetness_ao_socket,):
    x, y = location
    wetness_ao_texture = mat.msfs_wetness_ao_texture

    if wetness_ao_texture is not None:
        texture(
            mat,
            texture=wetness_ao_texture,
            label="WETNESS AO",
            location=(x, y),
            color_socket=wetness_ao_socket,
        )


def dirt(
    mat,
    location,
    clearcoat_socket,
    roughness_socket,):
    x, y = location
    dirt_texture = mat.msfs_dirt_texture

    if (
        roughness_socket is None
    ):  # some versions of Blender don't seem to have a clearcoat roughness socket
        return

    if dirt_texture is None:
        return

    # Separate RGB (amount is in R, roughness is in G)
    node = mat.node_tree.nodes.new("ShaderNodeSeparateRGB")
    node.location = x - 150, y - 75
    # Outputs
    mat.node_tree.links.new(clearcoat_socket, node.outputs["R"])
    mat.node_tree.links.new(roughness_socket, node.outputs["G"])
    # Inputs
    color_socket = node.inputs[0]

    x -= 200

    texture(
        mat,
        texture=dirt_texture,
        label="DIRT",
        location=(x, y),
        is_data=True,
        color_socket=color_socket,
    )


### Texture Update Functions - newer function not used for MSFSToolkit Legacy version
def update_base_color_texture(self, context):
    if not self.is_import:
        bsdf_node = utilities.get_bsdf_node(self)  # Try finding the BSDF node

        if bsdf_node is not None:  # maybe recreate the material in this case?
            # Clear Base Color
            utilities.clear_socket(self, bsdf_node.inputs["Base Color"])
            utilities.clear_socket(self, bsdf_node.inputs["Alpha"])

            locs = utilities.calc_locations(self)

            base_color(
                self,
                location=locs["base_color"],
                color_socket=bsdf_node.inputs["Base Color"],
                alpha_socket=bsdf_node.inputs["Alpha"]
                if not utilities.is_opaque(self)
                else None,
            )

            # update the blend mask
            update_blend_mask_texture(self, context)


def update_comp_texture(self, context):
    if not self.is_import:
        nodes = self.node_tree.nodes
        bsdf_node = utilities.get_bsdf_node(self)  # Try finding the BSDF node

        if bsdf_node is not None:
            # The comp texture has 3 parts - Occlusion (R), Roughness (G), Metalness (B). We do Roughness and Metalness first.
            # Clear Roughness and Metalness
            utilities.clear_socket(self, bsdf_node.inputs["Roughness"])
            utilities.clear_socket(self, bsdf_node.inputs["Metallic"])

            locs = utilities.calc_locations(self)

            metallic_roughness(
                self,
                location=locs["metallic_roughness"],
                metallic_socket=bsdf_node.inputs["Metallic"],
                roughness_socket=bsdf_node.inputs["Roughness"],
            )

            # Do Occlusion
            occlusion_socket = utilities.get_socket_old(self, "Occlusion")
            if occlusion_socket is not None:
                utilities.clear_socket(self, occlusion_socket)
                # check if it's safe to remove the gltf settings node
                if not utilities.is_node_linked(occlusion_socket.node):
                    nodes.remove(occlusion_socket.node)
                    occlusion_socket = None

            if (
                self.msfs_comp_texture is not None
                or self.msfs_detail_comp_texture is not None
            ):
                if (
                    occlusion_socket is None
                ):  # Create a settings node if one doesn't already exist
                    settings_node = utilities.make_settings_node(self)
                    settings_node.location = 40, -370
                    settings_node.width = 180
                    occlusion_socket = settings_node.inputs["Occlusion"]
                occlusion(
                    self,
                    location=locs["occlusion"],
                    occlusion_socket=occlusion_socket,
                )

            # update the blend mask
            update_blend_mask_texture(self, context)


def update_normal_texture(self, context):
    if not self.is_import:
        bsdf_node = utilities.get_bsdf_node(self)  # Try finding the BSDF node

        if bsdf_node is not None:  # maybe recreate the material in this case?
            # Clear Normal
            utilities.clear_socket(self, bsdf_node.inputs["Normal"])

            locs = utilities.calc_locations(self)

            normal(
                self,
                location=locs["normal"],
                normal_socket=bsdf_node.inputs["Normal"],
            )

            # update the blend mask
            update_blend_mask_texture(self, context)


def update_emissive_texture(self, context):
    if not self.is_import:
        bsdf_node = utilities.get_bsdf_node(self)  # Try finding the BSDF node

        if bsdf_node is not None:  # maybe recreate the material in this case?
            # Clear Emission
            utilities.clear_socket(self, bsdf_node.inputs["Emission"])

            locs = utilities.calc_locations(self)

            emission(
                self,
                location=locs["emission"],
                color_socket=bsdf_node.inputs["Emission"],
            )


def update_blend_mask_texture(self, context):
    if not self.is_import:
        nodes = self.node_tree.nodes

        (
            detail_base_color_factor_socket,
            detail_comp_factor_socket,
            detail_occlusion_factor_socket,
            detail_normal_factor_socket,
        ) = utilities.get_detail_factor_sockets(self)

        # Remove blend masks

        # Base color blend mask
        if detail_base_color_factor_socket is not None:
            base_color_blend_mask = utilities.previous_node(
                detail_base_color_factor_socket
            )
            if base_color_blend_mask is not None:
                nodes.remove(base_color_blend_mask)

        # Comp blend mask
        if detail_comp_factor_socket is not None:
            comp_blend_mask = utilities.previous_node(detail_comp_factor_socket)
            if comp_blend_mask is not None:
                nodes.remove(comp_blend_mask)

        # Occlusion blend mask
        if detail_occlusion_factor_socket is not None:
            occlusion_blend_mask = utilities.previous_node(
                detail_occlusion_factor_socket
            )
            if occlusion_blend_mask is not None:
                nodes.remove(occlusion_blend_mask)

        # Normal blend mask
        if detail_normal_factor_socket is not None:
            normal_blend_mask = utilities.previous_node(detail_normal_factor_socket)
            if normal_blend_mask is not None:
                nodes.remove(normal_blend_mask)

        locs = utilities.calc_locations(self)

        blend_mask(
            self,
            location=locs["blend_mask"],
        )


def update_wetness_ao_texture(self, context):
    if not self.is_import:
        nodes = self.node_tree.nodes
        bsdf_node = utilities.get_bsdf_node(self)  # Try finding the BSDF node

        if bsdf_node is not None:
            # We put the wetness ao in the settings node as Blender can't render this
            wetness_ao_socket = utilities.get_socket_old(self, "Wetness AO")
            if wetness_ao_socket is not None:
                utilities.clear_socket(self, wetness_ao_socket)
                # check if it's safe to remove the gltf settings node
                if not utilities.is_node_linked(wetness_ao_socket.node):
                    nodes.remove(wetness_ao_socket.node)
                    wetness_ao_socket = None

            if self.msfs_wetness_ao_texture is not None:
                if (
                    wetness_ao_socket is None
                ):  # Create a settings node if one doesn't already exist
                    settings_node = utilities.make_settings_node(self)
                    settings_node.location = 40, -370
                    settings_node.width = 180
                    wetness_ao_socket = settings_node.inputs["Wetness AO"]

                locs = utilities.calc_locations(self)

                wetness_ao(
                    self,
                    location=locs["wetness_ao"],
                    wetness_ao_socket=wetness_ao_socket,
                )


def update_dirt_texture(self, context):
    if not self.is_import:
        bsdf_node = utilities.get_bsdf_node(self)  # Try finding the BSDF node

        if bsdf_node is not None:  # maybe recreate the material in this case?
            # Clear Clearcoat and Clearcoat Roughness
            utilities.clear_socket(self, bsdf_node.inputs["Clearcoat"])
            utilities.clear_socket(self, bsdf_node.inputs["Clearcoat Roughness"])

            locs = utilities.calc_locations(self)

            dirt(
                self,
                location=locs["clearcoat"],
                clearcoat_socket=bsdf_node.inputs["Clearcoat"],
                roughness_socket=bsdf_node.inputs["Clearcoat Roughness"],
            )


### Other Update Functions- newer function not used for MSFSToolkit Legacy version

def update_base_color_factor(self, context):
    gltf2_io_debug.print_console("WARNING","in base")

    if not self.is_import:
        gltf2_io_debug.print_console("WARNING","in past is_import")

        # Locate base color factor socket and change it
        base_color_socket = utilities.get_socket(self, "Base Color")
        if base_color_socket is None:
            base_color_socket = utilities.get_socket(self, "BaseColor")
        if base_color_socket is None:
            base_color_socket = utilities.get_socket_old(self, "BaseColorFactor")
        if isinstance(
            base_color_socket, bpy.types.NodeSocket
        ):  # Make sure this is a node socket
            gltf2_io_debug.print_console("WARNING","socket is {0}".format(base_color_socket))
            base_color_factor = list(self.msfs_base_color_factor)
            if base_color_socket.is_linked:  # We have a node going into the socket
                base_color_socket = utilities.get_rgb_socket(base_color_socket)

                if (
                    base_color_socket is None
                ):  # If the socket is none, we trigger an update to the base color texture as that handles color factor creation, and it's easier to do that than redoing that here.
                    update_base_color_texture(self, context)
                else:
                    base_color_socket.default_value = base_color_factor
            else:  # We just update the socket itself
                base_color_socket.default_value = base_color_factor
        gltf2_io_debug.print_console("WARNING","base color socket default is at end {0} {1} {2} {3}".format(self.name, base_color_socket.default_value[0],base_color_socket.default_value[1],base_color_socket.default_value[2]))


def update_emissive_factor(self, context):
    if not self.is_import:
        # Locate emissive factor socket and change it
        emissive_socket = utilities.get_socket(self, "Emissive")
        if emissive_socket is None:
            emissive_socket = utilities.get_socket_old(self, "EmissiveFactor")
        if isinstance(
            emissive_socket, bpy.types.NodeSocket
        ):  # Make sure this is a node socket
            emissive_factor = list(self.msfs_emissive_factor) + [
                1
            ]  # msfs_emissive_factor is an array of 3 items, but the socket takes an array of 4 items, so we add one
            if emissive_socket.is_linked:  # We have a node going into the socket
                emissive_socket = utilities.get_rgb_socket(emissive_socket)

                if (
                    emissive_socket is None
                ):  # If the socket is none, we trigger an update to the emissive texture as that handles emissive factor creation, and it's easier to do that than redoing that here.
                    update_base_color_texture(self, context)
                else:
                    emissive_socket.default_value = emissive_factor
            else:  # We just update the socket itself
                emissive_socket.default_value = emissive_factor

# MSFSToolkit Legacy
class MaterialError(Exception):
    def __init__(self, msg, objs=None):
        self.msg = msg
        self.objs= objs

#class MaterialUtil():
def MakeOpaque(Material):
    #remove the alpha link:
    bsdf_node = Material.node_tree.nodes.get("bsdf")
    if bsdf_node != None:
        l = bsdf_node.inputs["Alpha"].links[0]
        Material.node_tree.links.remove(l)    

    Material.blend_method = 'OPAQUE'

def MakeMasked(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    #create the alpha link:
    bsdf_node = nodes.get("bsdf")
    alpha_multiply = nodes.get("alpha_multiply")
    if (bsdf_node != None and alpha_multiply != None):
        links.net(alpha_multiply.outputs["Value"],bsdf_node.inputs["Alpha"])

    Material.blend_method = 'CLIP'

def MakeTranslucent(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    #create the alpha link:
    bsdf_node = nodes.get("bsdf")
    alpha_multiply = nodes.get("alpha_multiply")
    if (bsdf_node != None and alpha_multiply != None):
        links.new(alpha_multiply.outputs["Value"],bsdf_node.inputs["Alpha"])

    Material.blend_method = 'BLEND'

def MakeDither(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    #Since Eevee doesn't provide a dither mode, we'll just use alpha-blend instead.
    #It sucks, but what else is there to do?
    #create the alpha link:
    bsdf_node = nodes.get("bsdf")
    alpha_multiply = nodes.get("alpha_multiply")
    if (bsdf_node != None and alpha_multiply != None):
        links.new(alpha_multiply.outputs["Value"],bsdf_node.inputs["Alpha"])

    Material.blend_method = 'BLEND'

# This function removes all nodes from the shader node tree
def RemoveShaderNodes(Material,keep_output=True):
    nodes = Material.node_tree.nodes
    output_node = None

    for idx,node in enumerate(nodes):
        if ((node.type != 'OUTPUT_MATERIAL') or (keep_output == False)):
            #removing node:
            print("Deleting: %s | %s"%(node.name,node.type))
            nodes.remove(node)
        else:
            output_node = node
    
    return output_node

# Find a node of a specific type
def FindNodeByType(Material, node_type):
    nodes = Material.node_tree.nodes
    for idx,node in enumerate(nodes):
        if node.type == node_type:
            return node
    return None
# Find a node of a specific name
def FindNodeByName(Material, node_name):
    nodes = Material.node_tree.nodes
    for idx,node in enumerate(nodes):
        if node.name == node_name:
            return node
    return None

# Create a new node of a specific type
def CreateNewNode(Material,node_type,label=None,location=(.0,.0)):
    new_node = None
    try:
        new_node = Material.node_tree.nodes.new(node_type)
        if label != None:
            new_node.name = label
            new_node.label = label
        new_node.location = location
    finally:
        print("New node '%s' of type '%s' created for material '%s'."%(new_node.name,node_type,Material.name))

    if new_node == None:
        msg = format("MATERIAL ERROR! A new output shader node could not be created for the material '%s'."%Material.name)
        raise MaterialError(msg)
    return new_node

def CreatePBRBranch(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

    # Base color
    base_color_node = CreateNewNode(Material,'ShaderNodeTexImage',"albedo",location=(offset[0],offset[1]))

    # color mixer
    base_color_tint = CreateNewNode(Material,'ShaderNodeRGB',"albedo_tint",location=(offset[0]+100,offset[1]+50))
    base_color_tint.hide = True
    base_color_tint.outputs[0].default_value[0]=Material.msfs_color_albedo_mix[0]
    base_color_tint.outputs[0].default_value[1]=Material.msfs_color_albedo_mix[1]
    base_color_tint.outputs[0].default_value[2]=Material.msfs_color_albedo_mix[2]
    base_color_tint.outputs[0].default_value[3]=Material.msfs_color_alpha_mix
    base_color_tint_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"albedo_tint_mix",location=(offset[0]+350,offset[1]+20))
    base_color_tint_mix.hide = True
    base_color_tint_mix.blend_type = 'MULTIPLY'
    base_color_tint_mix.inputs[0].default_value = 1.0
    base_color_tint_mix.inputs[1].default_value[0] = 1.0
    base_color_tint_mix.inputs[1].default_value[1] = 1.0
    base_color_tint_mix.inputs[1].default_value[2] = 1.0
    base_color_detail_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"albedo_detail_mix",location=(offset[0]+550,offset[1]+20))
    base_color_detail_mix.hide = True
    base_color_detail_mix.blend_type = 'MULTIPLY'
    base_color_detail_mix.inputs[0].default_value = Material.msfs_color_base_mix
    base_color_detail_mix.inputs[2].default_value[0] = Material.msfs_color_albedo_mix[0]
    base_color_detail_mix.inputs[2].default_value[1] = Material.msfs_color_albedo_mix[1]
    base_color_detail_mix.inputs[2].default_value[2] = Material.msfs_color_albedo_mix[2]
    base_color_detail_mix.inputs[2].default_value[3] = Material.msfs_color_base_mix
    # base_color_detail_mix.inputs["Color2"].default_value = (1.0,1.0,1.0,1.0)

    # Assign texture, if already saved in msfs data:
    if Material.msfs_albedo_texture != None:
        if Material.msfs_albedo_texture.name != "":
            base_color_node.image = Material.msfs_albedo_texture
            links.new(base_color_node.outputs["Color"], base_color_tint_mix.inputs["Color2"])
            links.new(base_color_detail_mix.outputs["Color"], bsdf_node.inputs["Base Color"])

    #Create the Alpha path:
    alpha_multiply = CreateNewNode(Material,'ShaderNodeMath',"alpha_multiply",location=(offset[0]+550,offset[1]-350))
    alpha_multiply.hide = True
    alpha_multiply.operation = 'MULTIPLY'
    alpha_multiply.inputs[1].default_value = Material.msfs_color_alpha_mix
    alpha_multiply.inputs[0].default_value = 1.0

    #Link the UV:
    links.new(uv_node.outputs["UV"], base_color_node.inputs["Vector"])
    #Create albedo links:
    #links.new(base_color_tint.outputs["Color"], base_color_detail_mix.inputs["Color2"])
    #links.new(base_color_tint.outputs["Color"], base_color_tint_mix.inputs["Color1"])
    links.new(base_color_tint_mix.outputs["Color"], base_color_detail_mix.inputs["Color1"])

    #Link the Alpha:
    links.new(base_color_node.outputs["Alpha"], alpha_multiply.inputs[0])


    # Metallic
    texture_metallic_node = CreateNewNode(Material,'ShaderNodeTexImage',"metallic",location=(offset[0],offset[1]-280))
    if Material.msfs_metallic_texture != None:
        if Material.msfs_metallic_texture.name != "":
            texture_metallic_node.image = Material.msfs_metallic_texture
    metallic_detail_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"metallic_detail_mix",location=(offset[0]+350,offset[1]-305))
    metallic_detail_mix.hide = True
    metallic_detail_mix.blend_type = 'MIX'
    metallic_detail_mix.inputs[0].default_value = 0.0
    metallic_separate = CreateNewNode(Material,'ShaderNodeSeparateRGB',"metallic_sep",location=(offset[0]+550,offset[1]-305))
    metallic_separate.hide = True

    # Create a node group for the occlusion map
    #Let's see if the node tree already exists, if not create one.
    occlusion_node_tree = bpy.data.node_groups.get("glTF Settings")
    if occlusion_node_tree == None:
        #create a new node tree with one input for the occlusion:
        occlusion_node_tree = bpy.data.node_groups.new('glTF Settings', 'ShaderNodeTree')
        occlusion_node_tree.nodes.new('NodeGroupInput')
        occlusion_node_tree.inputs.new('NodeSocketFloat','Occlusion')
        occlusion_node_tree.inputs[0].default_value = (1.000)
    #2. place a new node group in the current node tree:
    occlusion_group = CreateNewNode(Material,'ShaderNodeGroup',location=(offset[0]+1000,offset[1]+50))
    occlusion_group.node_tree = occlusion_node_tree
    occlusion_group.width = 200.0

    #Link the UV:
    links.new(uv_node.outputs["UV"], texture_metallic_node.inputs["Vector"])
    #Create metallic links:
    links.new(texture_metallic_node.outputs["Color"], metallic_detail_mix.inputs["Color1"])
    links.new(metallic_detail_mix.outputs["Color"], metallic_separate.inputs["Image"])
    links.new(metallic_separate.outputs[0], occlusion_group.inputs["Occlusion"])
    if Material.msfs_metallic_texture != None:
        if Material.msfs_metallic_texture.name != "":
            #link to bsdf
            if (bsdf_node != None and metallic_separate != None):
                links.new(metallic_separate.outputs[1], bsdf_node.inputs["Roughness"])
                links.new(metallic_separate.outputs[2], bsdf_node.inputs["Metallic"])


    # Normal map
    normal_node = CreateNewNode(Material,'ShaderNodeTexImage',"normal",location=(offset[0],offset[1]-900))
    normal_map_node = CreateNewNode(Material,'ShaderNodeNormalMap',"normal_map_node",location=(offset[0]+550,offset[1]-930))
    if Material.msfs_normal_texture != None:
        if Material.msfs_normal_texture.name != "":
            normal_node.image = Material.msfs_normal_texture
            links.new(normal_map_node.outputs["Normal"], bsdf_node.inputs["Normal"])
    normal_map_node.inputs["Strength"].default_value = Material.msfs_normal_scale
    normal_map_node.hide = True
    normal_detail_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"normal_detail_mix",location=(offset[0]+350,offset[1]-926))
    normal_detail_mix.hide = True
    normal_detail_mix.blend_type = 'MIX'
    normal_detail_mix.use_clamp = True
    normal_detail_mix.inputs[0].default_value = 0.0

    #Link the UV:
    links.new(uv_node.outputs["UV"], normal_node.inputs["Vector"])
    #Create normal links:
    links.new(normal_node.outputs["Color"], normal_detail_mix.inputs["Color1"])
    links.new(normal_detail_mix.outputs["Color"], normal_map_node.inputs["Color"])
    #link to bsdf
    #links.new(normal_map_node.outputs["Normal"], bsdf_node.inputs["Normal"])


def CreateEmissiveBranch(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

   # Emissive
    emissive_node = CreateNewNode(Material,'ShaderNodeTexImage',"emissive",location=(offset[0],offset[1]))
    if Material.msfs_emissive_texture != None:
        if Material.msfs_emissive_texture.name != "":
            emissive_node.image = Material.msfs_emissive_texture
    # color mixer
    emissive_tint = CreateNewNode(Material,'ShaderNodeRGB',"emissive_tint",location=(offset[0]+100,offset[1]+50))
    emissive_tint.hide = True
    emissive_tint.outputs[0].default_value[0]=Material.msfs_color_emissive_mix[0]
    emissive_tint.outputs[0].default_value[1]=Material.msfs_color_emissive_mix[1]
    emissive_tint.outputs[0].default_value[2]=Material.msfs_color_emissive_mix[1]
    emissive_tint_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"emissive_tint_mix",location=(offset[0]+350,offset[1]+20))
    emissive_tint_mix.hide = True
    emissive_tint_mix.blend_type = 'MULTIPLY'
    emissive_tint_mix.inputs[0].default_value = 1.0

    #Link UV:
    links.new(uv_node.outputs["UV"], emissive_node.inputs["Vector"])
    #Create metallic links:
    links.new(emissive_tint.outputs["Color"], emissive_tint_mix.inputs["Color1"])
    links.new(emissive_node.outputs["Color"], emissive_tint_mix.inputs["Color2"])


def CreateDetailBranch(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

    # Detail texture nodes:
    detail_albedo_node = CreateNewNode(Material,'ShaderNodeTexImage',"detail_albedo",location=(offset[0],offset[1]))
    if Material.msfs_detail_albedo_texture != None:
        if Material.msfs_detail_albedo_texture.name != "":
            detail_albedo_node.image = Material.msfs_detail_albedo_texture
    detail_metallic_node = CreateNewNode(Material,'ShaderNodeTexImage',"detail_metallic",location=(offset[0],offset[1]-280))
    if Material.msfs_detail_metallic_texture != None:
        if Material.msfs_detail_metallic_texture.name != "":
            detail_metallic_node.image = Material.msfs_detail_metallic_texture
    detail_normal_node = CreateNewNode(Material,'ShaderNodeTexImage',"detail_normal",location=(offset[0],offset[1]-560))
    if Material.msfs_detail_normal_texture != None:
        if Material.msfs_detail_normal_texture.name != "":
            detail_normal_node.image = Material.msfs_detail_normal_texture

    # Create the scaling transform
    detail_uv_scale_node = CreateNewNode(Material, 'ShaderNodeMapping', 'detail_uv_scale', location=(offset[0]-200,offset[1]-195))
    detail_uv_scale_node.hide = True

    # Find the main pbr nodes:
    albedo_node_mix = nodes.get("albedo_detail_mix")
    metallic_node_mix = nodes.get("metallic_detail_mix")
    normal_node_mix = nodes.get("normal_detail_mix")

    #create the links, if possible and texture name is already set:
    if albedo_node_mix != None:
        if Material.msfs_detail_albedo_texture != None:
            if Material.msfs_detail_albedo_texture.name != "":
                links.new(detail_albedo_node.outputs["Color"],albedo_node_mix.inputs["Color2"])
    if metallic_node_mix != None:
        if Material.msfs_detail_metallic_texture != None:
            if Material.msfs_detail_metallic_texture.name != "":
                links.new(detail_metallic_node.outputs["Color"],metallic_node_mix.inputs["Color2"])
    if normal_node_mix != None:
        if Material.msfs_detail_normal_texture != None:
            if Material.msfs_detail_normal_texture.name != "":
                links.new(detail_normal_node.outputs["Color"],normal_node_mix.inputs["Color2"])

    links.new(uv_node.outputs["UV"],detail_uv_scale_node.inputs["Vector"])
    links.new(detail_uv_scale_node.outputs["Vector"],detail_albedo_node.inputs["Vector"])
    links.new(detail_uv_scale_node.outputs["Vector"],detail_metallic_node.inputs["Vector"])
    links.new(detail_uv_scale_node.outputs["Vector"],detail_normal_node.inputs["Vector"])

    detail_uv_scale_node.inputs["Scale"].default_value[0] = Material.msfs_detail_uv_scale
    detail_uv_scale_node.inputs["Scale"].default_value[1] = Material.msfs_detail_uv_scale
    detail_uv_scale_node.inputs["Scale"].default_value[2] = Material.msfs_detail_uv_scale

def CreateBlendMask(Material, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

   # Blend Mask
    blend_mask = CreateNewNode(Material,'ShaderNodeTexImage',"blend_mask",location=(offset[0],offset[1]))
    if Material.msfs_blend_mask_texture != None:
        if Material.msfs_blend_mask_texture.name != "":
            blend_mask.image = Material.msfs_blend_mask_texture

    #Link UV:
    links.new(uv_node.outputs["UV"], blend_mask.inputs["Vector"])   #this might need to come from the detail uv transform instead.

    if Material.msfs_blend_mask_texture != None:
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

def CreateAnisotropicDirection(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

   # Blend Mask
    anisotropic_direction = CreateNewNode(Material,'ShaderNodeTexImage',"anisotropic_direction",location=(offset[0],offset[1]))
    if Material.msfs_anisotropic_direction_texture != None:
        if Material.msfs_anisotropic_direction_texture.name != "":
            anisotropic_direction.image = Material.msfs_anisotropic_direction_texture

    #Link UV:
    links.new(uv_node.outputs["UV"], anisotropic_direction.inputs["Vector"])   #this might need to come from the detail uv transform instead.

def CreateClearcoat(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

    clearcoat = CreateNewNode(Material,'ShaderNodeTexImage',"clearcoat",location=(offset[0],offset[1]))
    clearcoat_sep = CreateNewNode(Material,'ShaderNodeSeparateRGB',"clearcoat_sep",location=(offset[0]+350,offset[1]))
    clearcoat_sep.hide = True
    links.new(clearcoat.outputs["Color"],clearcoat_sep.inputs["Image"])

    if Material.msfs_clearcoat_texture != None:
        if Material.msfs_clearcoat_texture.name != "":
            clearcoat.image = Material.msfs_clearcoat_texture
            #Create links:
            links.new(clearcoat_sep.outputs["R"],bsdf_node.inputs["Clearcoat"])
            links.new(clearcoat_sep.outputs["G"],bsdf_node.inputs["Clearcoat Roughness"])

    #Link UV:
    links.new(uv_node.outputs["UV"], clearcoat.inputs["Vector"])   #this might need to come from the detail uv transform instead.

def CreateWiperMask(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

    wiper_mask = CreateNewNode(Material,'ShaderNodeTexImage',"wiper_mask",location=(offset[0],offset[1]))

    #Link UV:
    links.new(uv_node.outputs["UV"], wiper_mask.inputs["Vector"])

# The following functions create Blender shaders to represent the MSFS material presets
def CreateMSFSStandardShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

def CreateMSFSAnisotropicShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateAnisotropicDirection(Material,bsdf_node,(-1000,-700))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1250))
    CreateBlendMask(Material,(-1000,-900))

def CreateMSFSSSSShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))
    bsdf_node.inputs["Subsurface Color"].default_value = Material.msfs_color_sss

    bsdf_node.inputs["Subsurface"].default_value = 0.1

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    
def CreateMSFSGlassShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))
    
    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSDecalShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

    #enable transparency:
    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSClearcoatShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateClearcoat(Material, bsdf_node,(-1000,-700))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1350))
    CreateBlendMask(Material,(-1000,-1000))

def CreateMSFSFakeTerrainShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

def CreateMSFSFresnelShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))

    #enable transparency:
    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSWindshieldShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))
    #CreateWiperMask(Material,(-1000,-950))

    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSPortholeShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

def CreateMSFSParallaxShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))

    #For the behind-glass magic, we'll need some uv controls:
    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(-3000,500))
    behind_glass_uv_scale_node = CreateNewNode(Material, 'ShaderNodeMapping', 'behind_glass_uv_scale', location=(-1200,-795))
    behind_glass_uv_scale_node.hide = True

    # Add the behind-glass-albedo-emissive
    behind_glass_node = CreateNewNode(Material,'ShaderNodeTexImage',"behind_glass",location=(-1000,-750))
    if Material.msfs_behind_glass_texture != None:
        if Material.msfs_behind_glass_texture.name != "":
            behind_glass_node.image = Material.msfs_behind_glass_texture
            if nodes.get("albedo_detail_mix") != None:
                links.new(behind_glass_node.outputs["Color"], nodes.get("albedo_detail_mix").inputs["Color2"])
    # Grab the Emissive texture:
    emissive_node = FindNodeByName(Material,"emissive")
    links.new(uv_node.outputs["UV"],behind_glass_uv_scale_node.inputs["Vector"])
    links.new(behind_glass_uv_scale_node.outputs["Vector"],behind_glass_node.inputs["Vector"])

    if emissive_node != None:
        links.new(behind_glass_uv_scale_node.outputs["Vector"],emissive_node.inputs["Vector"])

def CreateMSFSGeoDecalShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-500))

    #enable transparency:
    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSHairShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.2    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateAnisotropicDirection(Material, bsdf_node,(-1000,-400))

    Material.msfs_blend_mode = 'DITHER'

def CreateMSFSInvisibleShader(Material):

    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)
    
    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')
    
    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled',location=(0,400))
    bsdf_node.inputs["Alpha"].default_value = 0.1
    bsdf_node.inputs["Base Color"].default_value = (0.8,0.0,0.0,1.0)
    bsdf_node.inputs["Emission"].default_value = (0.8,0.0,0.0,1.0)

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #connect the nodes:
    links.new(output_node.inputs["Surface"], bsdf_node.outputs["BSDF"])

    #enable transparency:
    MakeTranslucent(Material)

def CreateMSFSEnvOccluderShader(Material):

    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)
    
    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')
    
    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled',location=(0,400))
    bsdf_node.inputs["Alpha"].default_value = 0.3
    bsdf_node.inputs["Base Color"].default_value = (0.0,0.8,0.0,1.0)
    bsdf_node.inputs["Emission"].default_value = (0.0,0.8,0.0,1.0)

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #connect the nodes:
    links.new(output_node.inputs["Surface"], bsdf_node.outputs["BSDF"])

    #enable transparency:
    MakeTranslucent(Material)

