# Blender2MSFS2
Collaborative adoption of Blender2MSFS which apparently has been left in limbo by its author

Version 0.42.12 and beyonfd are for Blender 3.3+ - In that there is a breaking change. Blender 3.3 due to shader node naming changes SHADERNODERGB has been changed to SHADERNODECOLOR

You must redo all you MSFS Materials if you open your existing pre 3.3 into this version.

Ron Haertel - 0.42.x author (experimantal - good for production use)
Ver 0.42.x - Updated to the latest Khronos version of the blender gltf exporter with the MSFS 2020 specific
ASOBO gltf extensions
New - Pearlescnet - operationl
New - added more UV export data - texture tiling - not operational yet.
New - FBW - importer - not operational
New - Windshield Rain drop scale and wiper 1,2

Fixed Windshield - alpha panel information not appearing.

Fixed Soptlight error in updated code.

3DS naming of texture slots like 3DS version for windshield and geodecalfrosted

The releases of the upstream Blender2MSFS are archived at
https://www.fsdeveloper.com/forum/resources/blender2msfs-toolkit.256/history
. As can be seen, there has been no public releases since
September 2020. That is hardly ideal.

The intent of this repository is to enable people to co-operate on
further work on this exporter.

I (Tor Lillqvist) am not personally adopting this code, and/or volunteering to
maintain it, as I don't have the skills needed. I am not a Python
expert at all. I don't know Blender's data structures (as accessible
from Python). I don't really know glTF at all. And finally, I have
been using Blender for only two months.

My role is just to set up this repository and import the Blender2MSFS
releases into it. I will gladly give away maintainership of this repo
(however that would be done) if some interested and eager volunteer
appears.

If the original author re-appears and starts releasing newer versions,
this repository might well become obsolete.

The original README is MSFSToolkit/readme.md

There are also other efforts on export from Blender to MSFS, and even import of MSFS 3D assets to Blender.

The most promising is perhaps
https://github.com/flybywiresim/msfs2blender2msfs , which is forked
from the official Khronos glTF 2.0 importer and exporter. Sadly, that
too apparently has stagnated somewhat.

For import from MSFS to Blender, there is
https://github.com/bestdani/msfs2blend

# How to install
Download this repo as a .zip file. Start blender go to the settings / addons / install from file. Choos the downloaded .zip file and hit ok.

# Original Readme from Vitus

Blender2MSFS
============

This Blender addon allows you to create 3D assets for Microsoft Flight Simulator (2020). The addon is designed for Blender 2.83, and above.

MSFS is using the Khronos' glTF 2.0 file format with multiple custom extensions and extras for special material functions. While Blender 2.8x already ships with a glTF exporter, some changes had to be made to the exporter to facilitate some of the used extensions. These changes come fully integrated into this addon, in the form of modified call functions. These functions will make use of the existing Khronos glTF 2.0 exporter, while inserting some of the custom extensions for MSFS.

In order to export all the available materials, select the "extended glTF 2.0 for MSFS" in the Export menu and make sure that the "Asobo Extensions" are enabled in the export options, under "Extensions".


Incompatibility with Blender2P3D/FSX
------------------------------------

It is important to point out that the Blender2MSFS toolkit is incompatible with the Blender2P3D/FSX toolset. While there is no problem having both of them installed in Blender, you cannot use both of them at the same time for any particular blender scene. Instead, you have to keep separate Blender files both for MSFS and P3D/FSX.
The reason for this incompatibility is the fact that both addons customize the shader node tree to match the material counterpart of the sim. When changing a model’s material to a MSFS material, you will lose the material parameters for P3D/FSX, and vice-versa.

However, since exporting to MSFS has some other very specific requirements in contradiction to a P3D/FSX model, it is encouraged to keep those two models separate anyway.


Materials
---------

The Blender2MSFS addon features all 15 of the Microsoft Flight Simulator materials. To assign one of those flight simulator specific materials to an object, open the material option for a selected object and find the section “MSFS Material Params”.
Use the drop-down list to switch between the different material modes. After a material mode is selected, the addon will automatically rebuild the shader node tree in a way that is specific to the selected material type. Some materials contain special parameters which are revealed when those materials are selected.

The shader node tree is also handled dynamically by the Blender2MSFS addon. This means that some of the nodes are not linked to the BSDF principled shader when the material is set up. Instead, those links are being generated only when textures are being assigned to the various texture slots in the MSFS material parameters.

Because these links are generated by interacting with the MSFS material parameters, make sure to only use this custom interface to assign textures! Do not assign textures directly in the shader node tree, as that will not synchronize and update the shader accordingly.

While we try to adjust the shader node tree in a way that it is representative of the shader of Flight Simulator, this is not always possible. While some of the more common materials, like “MSFS Standard” or “MSFS glass” look very similar in Blender and the sim, this is not always the case, due to the limitations of Blender and the BSDF principled node. That being said, we will try to improve the shader node tree for the various custom materials as we develop the next versions of this addon.

Also note that not all of the materials have been undergoing some thorough testing. It is possible that some of the parameters currently don’t create the desired effect. If you find such a mis-match, please let me know in the Blender2MSFS support thread. 

Most of the materials and parameters are well documented in the MSFS SDK. You can find the information under “Asset creation->glTF Materials”.


Export
------

The Blender2MSFS addon appends the Export options of Blender by an additional entry “extended glTF 2.0 for MSFS”, which, as the name suggests, can be used to produce MSFS compatible addons. When selecting    this option, you’re presented with the exporter dialog containing the following options:

glTF formats
    glTF files can have three different forms: glTF binaries (.glb), glTF Embedded (.glTF) or glTF separate (.gltf + .bin + texture). For MSFS it is recommended to use the last of the three options.

Textures
    Note that when using the glTF separate option, the exporter will automatically copy/convert your textures into the PNG format. If you don’t specify a directory in the “Textures” input, those textures will be generated in the same folder as your glTF model. Note that the textures folder utilises relative paths from the model file. This means you can use “../textures” as an input, which will automatically copy the textures to a MSFS conform location.
    That said, be aware that the relative path is NOT copied to the URI of the textures. This is a rigid requirement of the sim, but it leads to your model not being able to properly render in other glTF render engines. 

Copyright
    You can specify a copyright notice in the text input, this notice will be copied into the glTF file upon export.

MSFS specific parameters
    The MSFS parameters contain options to auto-generate the model behavior file, a GUID or perform an LOD batch-export. Those options are described in detail further below.

Other glTF specific parameters
    There’s many other parameters to further customize your glTF model. Those options are the same as the default glTF export options, therefore please refer to the Blender manual for more information.

Extensions
    As discussed above, glTF files can include “extensions” and “extras”, which are custom render-engine sets of parameters. The Flight Simulator is using those extensions extensively. Therefore, make sure that you have the “Asobo Extensions” enabled under “Extensions”.


LOD batch-export
----------------

It is possible to use the extended glTF2 exporter to generate multiple models of different level-of-detail (LOD) in one go. For this, you need to organize your Blender scene in the following manner:

Each LOD model needs to be contained in a separate collection. Tha name of the collection needs to follow the pattern of x##, where ## is the identifying number of the LOD - e.g. x00, x01, x02, etc.

When opening the exporter, expand the section labeled "MSFS" and enable the option "Batch export LODs". The exporter will now automatically scan your Blender scene and export each of the x## collections in a separate object, called <modelname>_LOD##.gltf.

Model behavior file
-------------------

The export options allow you to automatically generate the model-behavior file for your model. To activate this option, open the "MSFS" panel in the export dialog and check the box for "Generate/Append XML file". This will allow you to specify a filename for the XML file. Note that the filename will append the .xml file extension, if you don't add it. If a file by the specified filename already exists, the exporter will try to append it with new model information.

When the "Generate GUID" option is selected, the exporter will first check if there is already an existing GUID generated for the model and create a new one if not. The GUID is then inserted into the file.

If you're running a batch-export for multiple LODs, the model information for the different LODs are automatically added to the behavior file. Note however that the values for the "minSize" might need some manual adjustment afterwards.

At the moment, the model behavior file will not include any animations, mouse rects or other model behaviors, due to the lack of documentation in the SDK. This feature will be developed at a later date as more information becomes available.


Credits
-------

The Blender2MSFS toolkit was coded by Otmar Nitsche, aka Vitus of Wing42 (www.wing42.com) and is provided, free of charge, to the flight simulator community under the Apache 2.0 licensing agreement. 

The Blender2MSFS toolkit was made possible by the generous donations and the support of a group of outstanding flight simulator developers.

I want to thank everyone who took part in this process!

Special thanks go to Dean Crawford (DC Designs) for getting the ball rolling! And many thanks to Selmar Kok, Lionel Fuentes and Luca Pierabella of Asobo Studios, who took time off their busy schedule to answer so many of our questions.

Members of the team:
Otmar Nitsche (Wing42)
Dean Crawford (DC Design)
Bill Womack (iBlueYonder)
Raz Goeta (Gaya Simulations)
Finn Hansen (Orbx)
Alex Vletsas (SimWorks Studios)
Tony Wroblewski (W2XP)
Daniel Chircop (MS Design)
Mitsushi Yutaka (FS Painter)
Scott Armstrong (Aurora Simulations)


License
-------

Copyright © 2020 Otmar Nitsche

The license of the software can be simplified as follows:
Do whatever you want with it.

Use it personally, internally or commercially. Change it, redistribute it, sell it. You can credit the original authors. Or don’t, and collect all the glory for yourself.

Here’s the legal bit:

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this addon except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.