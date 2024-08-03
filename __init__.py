bl_info = {
    "name": "render multi-cams",
    "description": "Would you like to render multiple images from various cameras without changing the active camera each time? This add-on is here to help!",
    "author": " [ ModdedProp ] ",
    "version": (1, 2),
    "blender": (4, 0, 0),
    "location": "View3D > render multi-cams",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "https://github.com/ModdedLight/Multi-Cam-Rendering-Add-on",
    "category": "Render",
}

import bpy
import os

class RenderMultipleCamerasProperties(bpy.types.PropertyGroup):
    output_path: bpy.props.StringProperty(
        name="Output Path",
        description="Directory to save rendered images",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )

class RENDER_OT_multiple_cameras(bpy.types.Operator):
    bl_idname = "render.render_multiple_cameras"
    bl_label = "Render Multiple Cameras"
    bl_description = "Render all cameras in the scene and save each render as a PNG file named after the camera"

    def execute(self, context):
        scene = context.scene
        output_dir = scene.render_multiple_cameras_properties.output_path
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for obj in scene.objects:
            if obj.type == 'CAMERA':
                scene.camera = obj
                camera_name = obj.name
                filepath = os.path.join(output_dir, f"{camera_name}.png")
                bpy.context.scene.render.filepath = filepath
                bpy.ops.render.render(write_still=True)
        
        self.report({'INFO'}, f"Rendered {len([obj for obj in scene.objects if obj.type == 'CAMERA'])} cameras")
        return {'FINISHED'}

class RENDER_PT_multiple_cameras_panel(bpy.types.Panel):
    bl_label = "Render Multiple Cameras"
    bl_idname = "RENDER_PT_multiple_cameras_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        properties = scene.render_multiple_cameras_properties

        layout.prop(properties, "output_path")
        layout.operator(RENDER_OT_multiple_cameras.bl_idname)

def register():
    bpy.utils.register_class(RenderMultipleCamerasProperties)
    bpy.utils.register_class(RENDER_OT_multiple_cameras)
    bpy.utils.register_class(RENDER_PT_multiple_cameras_panel)
    bpy.types.Scene.render_multiple_cameras_properties = bpy.props.PointerProperty(type=RenderMultipleCamerasProperties)

def unregister():
    bpy.utils.unregister_class(RenderMultipleCamerasProperties)
    bpy.utils.unregister_class(RENDER_OT_multiple_cameras)
    bpy.utils.unregister_class(RENDER_PT_multiple_cameras_panel)
    del bpy.types.Scene.render_multiple_cameras_properties

if __name__ == "__main__":
    register()
