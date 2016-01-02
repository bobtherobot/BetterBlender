######################################################################################################
# An simple add-on to auto cut in two and mirror an object                                           #
# Actualy partialy uncommented (see further version)                                                 #
# Author: Lapineige                                                                                  #
# License: CC-By                                                                                     #
######################################################################################################
  
  
############# Add-on description (use by Blender)
  
bl_info = {
    "name": "Auto Mirror",
    "description": "Super fast cutting and mirroring for mesh",
    "author": "Lapineige",
    "version": (1, 0),
    "blender": (2, 7, 1),
    "location": "View 3D > Toolbar > Tools tab > AutoMirror (panel)",
    "warning": "", 
    "wiki_url": "http://www.le-terrier-de-lapineige.over-blog.com",
    "tracker_url": "http://blenderlounge.fr/forum/viewtopic.php?f=18&p=7103#p7103",
    "category": "Mesh"}
############# 

import bpy

bpy.types.Scene.AutoMirror_x = bpy.props.BoolProperty()
bpy.types.Scene.AutoMirror_y = bpy.props.BoolProperty()
bpy.types.Scene.AutoMirror_z = bpy.props.BoolProperty()
bpy.types.Scene.AutoMirror_axis = bpy.props.EnumProperty(items = [("x", "X", "", 1),("y", "Y", "", 2),("z", "Z", "", 3)])
bpy.types.Scene.AutoMirror_orientation = bpy.props.EnumProperty(items = [("positive", "Positive", "", 1),("negative", "Negative", "", 2)])
bpy.types.Scene.AutoMirror_threshold = bpy.props.FloatProperty(default= 0.001, min= 0.001)
bpy.types.Scene.AutoMirror_cut = bpy.props.BoolProperty(default= True)
bpy.types.Scene.AutoMirror_toggle_edit = bpy.props.BoolProperty(default= True)
bpy.types.Scene.AutoMirror_apply_mirror = bpy.props.BoolProperty()


############### Operator

class AlignVertices(bpy.types.Operator):
    """  """
    bl_idname = "object.align_vertices"
    bl_label = "Align Vertices on 1 Axis"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')

        x1,y1,z1 = bpy.context.scene.cursor_location
        bpy.ops.view3d.snap_cursor_to_selected()

        x2,y2,z2 = bpy.context.scene.cursor_location

        bpy.context.scene.cursor_location[0],bpy.context.scene.cursor_location[1],bpy.context.scene.cursor_location[2]  = 0,0,0

        #Vertices coordinate to 0 (local coordinate, so on the origin)
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if bpy.context.scene.AutoMirror_axis == 'x':
                    axis = 0
                elif bpy.context.scene.AutoMirror_axis == 'y':
                    axis = 1
                elif bpy.context.scene.AutoMirror_axis == 'z':
                    axis = 2
                vert.co[axis] = 0
        #
        bpy.context.scene.cursor_location = x2,y2,z2

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        bpy.context.scene.cursor_location = x1,y1,z1

        bpy.ops.object.mode_set(mode = 'EDIT')  
        return {'FINISHED'}

class AutoMirror(bpy.types.Operator):
    """ Automatically cut an object along an axis """
    bl_idname = "object.automirror"
    bl_label = "AutoMirror"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        X,Y,Z = 0,0,0
        if bpy.context.scene.AutoMirror_axis == 'x':
            X = 1
        elif bpy.context.scene.AutoMirror_axis == 'y':
            Y = 1
        elif bpy.context.scene.AutoMirror_axis == 'z':
            Z = 1

        current_mode = bpy.context.object.mode # Save the current mode
        
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT") # Go to edit mode
        bpy.ops.mesh.select_all(action='SELECT') # Select all the vertices
        if bpy.context.scene.AutoMirror_orientation == 'positive':
            orientation = 1
        else:
            orientation = -1

        bpy.ops.mesh.bisect(plane_co= (bpy.context.object.location[0], bpy.context.object.location[1], bpy.context.object.location[2]), plane_no= (X*orientation, Y*orientation, Z*orientation), use_fill= False, clear_inner= bpy.context.scene.AutoMirror_cut, clear_outer= 0, threshold= bpy.context.scene.AutoMirror_threshold) # Cut the mesh
        
        bpy.ops.object.align_vertices() # Use to align the vertices on the origin, needed by the "threshold"  ##### !!! Marche pas avec autre axe !!!
        
        if not bpy.context.scene.AutoMirror_toggle_edit:
            bpy.ops.object.mode_set(mode=current_mode) # Reload previous mode
        
        if bpy.context.scene.AutoMirror_cut:
            bpy.ops.object.modifier_add(type='MIRROR') # Add a mirror modifier
            bpy.context.object.modifiers[-1].use_x = X # Choose the axis to use, based on the cut's axis
            bpy.context.object.modifiers[-1].use_y = Y
            bpy.context.object.modifiers[-1].use_z = Z
            if bpy.context.scene.AutoMirror_apply_mirror:
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.modifier_apply(apply_as= 'DATA', modifier= bpy.context.object.modifiers[-1].name)
                if bpy.context.scene.AutoMirror_toggle_edit:
                    bpy.ops.object.mode_set(mode='EDIT')
                else:
                    bpy.ops.object.mode_set(mode=current_mode)
        
        return {'FINISHED'}

#################### Panel

class BisectMirror(bpy.types.Panel):
    """ The AutoMirror panel on the toolbar tab 'Tools' """
    bl_label = "Auto Mirror"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Addons"

    def draw(self, context):
        layout = self.layout
        if bpy.context.object and bpy.context.object.type == 'MESH':
            layout.operator("object.automirror")
            layout.prop(context.scene, "AutoMirror_axis", text="Mirror axis")
            layout.prop(context.scene, "AutoMirror_orientation", text="Orientation")
            layout.prop(context.scene, "AutoMirror_threshold", text="Threshold")
            layout.prop(context.scene, "AutoMirror_toggle_edit", text="Toggle edit")
            layout.prop(context.scene, "AutoMirror_cut", text="Cut and mirror")
            if bpy.context.scene.AutoMirror_cut:
                layout.prop(context.scene, "AutoMirror_apply_mirror", text="Apply mirror")
        else:
            layout.label(icon="ERROR", text="No mesh selected")


def register():
    bpy.utils.register_class(BisectMirror)
    bpy.utils.register_class(AutoMirror)
    bpy.utils.register_class(AlignVertices)


def unregister():
    bpy.utils.unregister_class(BisectMirror)
    bpy.utils.unregister_class(AutoMirror)
    bpy.utils.unregister_class(AlignVertices)


if __name__ == "__main__":
    register()



