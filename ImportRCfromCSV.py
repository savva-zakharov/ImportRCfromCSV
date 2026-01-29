bl_info = {
    "name": "Import RC Cameras",
    "blender": (4, 00, 0),
    "category": "Import",
}

import bpy
import csv
import math
import os
from mathutils import Euler
from bpy.utils import register_class
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import (
        StringProperty,
        BoolProperty,
        EnumProperty,
        IntProperty,
        FloatProperty,
        )

# =========================
# USER SETTINGS
# =========================
filepath_csv = r"F:\PGT\Richie\drive-download-20200911T075638Z-001\Richie.csv" # Update path
SCALE = 1.0

SENSOR_WIDTH  = 36.0
SENSOR_HEIGHT = 24.0



class ImportRCameras(Operator, ImportHelper):
    
    """A script for importing Reality Scan camera positions from CSV"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "rccsv.import_rc_camera"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Import RC camera CSV"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.   
    
    filename_ext = ".csv"
    filter_glob: StringProperty(default="*.csv", options={'HIDDEN'},)
    
    use_camera: BoolProperty(
    name="Import Images as Background", default=True,
    description="Should the images be imported as camera backgrounds? (should be located in the same folder as the CSV file)")
    
    user_image_path: StringProperty(
    name = "Image Folder", description="Path to your image folder",
    maxlen = 256, default = "", subtype='FILE_PATH')
    
    def draw(self, context):        
        layout = self.layout
        row = layout.row()
        row.prop(self, "use_camera")
        row = layout.row()
        row.prop(self, "user_image_path")
    
    def execute(self, context):
        
        
    



        
        import_rc_camera_csv(filepath_csv, self.use_camera, self.user_image_path)

        return {'FINISHED'}     
           
        
def import_rc_camera_csv(filepath_csv, use_camera, user_image_path):
    render_set = False
    collection_name = "RC_Cameras"
    col = bpy.data.collections.get(collection_name)
    
    if not col:
        col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(col)
        
    csv_folder = os.path.dirname(filepath_csv)


    with open(filepath_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            name = row["#name"]

            # POSITION
            x = float(row["x"]) * SCALE
            y = float(row["y"]) * SCALE
            z = float(row["alt"]) * SCALE

            # CAMERA DATA
            cam_data = bpy.data.cameras.new(name)
            
#            FACTOR = 24.5 / 24.0  # adjust as needed
            FACTOR = 1
            cam_data.lens = float(row["f"]) * FACTOR
            cam_data.sensor_width = SENSOR_WIDTH
            cam_data.sensor_height = SENSOR_HEIGHT
            cam_data.sensor_fit = 'HORIZONTAL'

            px = float(row["px"])
            py = float(row["py"])
            cam_data.shift_x = px / SENSOR_WIDTH
            cam_data.shift_y = -py / SENSOR_HEIGHT

            # CAMERA OBJECT
            cam_obj = bpy.data.objects.new(name, cam_data)
            cam_obj.location = (x, y, z)

            # ROTATION: RealityCapture → Blender YXZ
            pitch = math.radians(float(row["pitch"]))
            roll  = math.radians(float(row["roll"]))
            heading = math.radians(float(row["heading"]))

            # RC docs mapping
            cam_obj.rotation_mode = 'YXZ'
            cam_obj.rotation_euler = Euler((pitch, roll, -heading), 'YXZ')

            col.objects.link(cam_obj)

            # IMAGE BACKGROUND
            if use_camera:
                if not user_image_path == "":
                    image_path = os.path.join(user_image_path, name)        
                else:
                    image_path = os.path.join(csv_folder, name)

                    
                if os.path.isfile(image_path):
                    img = bpy.data.images.load(image_path)
                    cam_data.show_background_images = True
                    bg = cam_data.background_images.new()
                    bg.image = img
                    bg.display_depth = 'BACK'
                    bg.frame_method = 'FIT'
                    bg.alpha = 1.0

                    # Set scene render size from first image
                    if not render_set:
                        bpy.context.scene.render.resolution_x = img.size[0]
                        bpy.context.scene.render.resolution_y = img.size[1]
                        bpy.context.scene.render.resolution_percentage = 100
                        render_set = True
                else:
                    print(f"Warning: Image file not found for {name}")

    print("RealityCapture cameras imported with correct YXZ rotation.")
        
def menu_func_import_rc_csv(self, context):
    self.layout.operator(ImportRCameras.bl_idname, text="Import RC camera CSV (.csv)")

def register():
    register_class(ImportRCameras)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_rc_csv)

def unregister():
    unregister_class(ImportRCameras)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_rc_csv)

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()   