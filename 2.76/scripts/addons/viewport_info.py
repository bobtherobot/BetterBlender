'''
Copyright (C) 2015 Pistiwique

Created by Pistiwique

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Viewport info",
    "author": "Pistiwique",
    "version": (0, 0, 8),
    "blender": (2, 74, 0),
    "description": "Display selected infos in viewport",
    "tracker_url": "http://blenderlounge.fr/forum/viewtopic.php?f=26&t=1116",
    "category": "3D View"}
    
import bpy
import blf
import bgl
import bmesh
from math import sqrt

# Thanks to Zeffii on Blender Stack Exchange for his/her help

###################################
####    MATERIALS FONCTIONS    ####
###################################

def Setup_Scene():
    bpy.ops.object.mode_set(mode='OBJECT')
    for slots in bpy.context.active_object.material_slots:
        bpy.ops.object.material_slot_remove() # remove all materials slots   
    bpy.ops.object.mode_set(mode='EDIT')
  

#####################################################################
   
def Create_Mat():

    if bpy.context.space_data.use_matcap:
        bpy.context.space_data.use_matcap = False
                            
    # create new material        
    mat_A = bpy.data.materials.new("Quads")
    mat_A.diffuse_color = (0.323, 0.323, 0.323)

    mat_B = bpy.data.materials.new("Ngons")
    mat_B.diffuse_color = (0.800, 0.146, 0.146)
    
    mat_C = bpy.data.materials.new("Tris")
    mat_C.diffuse_color = (0.800, 0.800, 0.100)
    
    ob = bpy.context.active_object
    me = ob.data
    mat_list = [mat_A, mat_B, mat_C]
    for mat in mat_list:
        me.materials.append(mat) # assign materials

#####################################################################
       
def Restore_Mat():
    Setup_Scene()
    mat_A = bpy.data.materials['Quads']

    mat_B = bpy.data.materials['Ngons']
    
    mat_C = bpy.data.materials['Tris']

    
    ob = bpy.context.active_object
    me = ob.data
    mat_list = [mat_A, mat_B, mat_C]
    for mat in mat_list:
        me.materials.append(mat)
        
###############################
####    MATERIALS CLASS    ####
###############################

class SetupMaterials(bpy.types.Operator):
    bl_idname = "object.setup_materials"
    bl_label = "Setup materials"
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type == 'MESH'
    
    def execute(sefl, context):
        
        st = context.window_manager.show_text
            
        if not bpy.data.materials:

            Create_Mat()
                
            st.Display_T_N = True
            return {'FINISHED'}

        else:
            if bpy.context.object.active_material:
                for mat_slots in bpy.context.active_object.material_slots:
                    st.backup_mat.append(mat_slots.name)
                    st.Save_Mat = True
                        
            ref_list = ['Quads', 'Ngons', 'Tris']            
            mat_list = []
            for mat in bpy.data.materials:
                mat_list.append(mat.name)
            for ref in ref_list:
                if ref in mat_list:                   
                    Restore_Mat()
                    st.Display_T_N  = True
                    return {'FINISHED'}
                else:
                    Setup_Scene() 
                    Create_Mat()
                    if context.space_data.use_matcap:
                        context.space_data.use_matcap = False
                    st.Display_T_N  = True
                    return {'FINISHED'}
                
#####################################################################

class HiddeFaces(bpy.types.Operator):
    bl_idname = "object.hidde_faces"
    bl_label = "Hidde face"
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type == 'MESH'
    
    def execute(self, context):
        st = context.window_manager.show_text
        
        if context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            for slots in bpy.context.active_object.material_slots:
                bpy.ops.object.material_slot_remove()
            if st.Save_Mat:
                ob = bpy.context.active_object
                me = ob.data
                
                for mat in st.backup_mat:
                    mat_list = bpy.data.materials[mat]
                    me.materials.append(mat_list)

                st.Save_Mat = False
                st.backup_mat[:] = [] # clean the list
                
            bpy.ops.object.mode_set(mode='EDIT')
            
        elif context.object.mode == 'OBJECT':
            for slots in bpy.context.active_object.material_slots:
                bpy.ops.object.material_slot_remove()
            if st.Save_Mat:
                ob = bpy.context.active_object
                me = ob.data
                
                for mat in st.backup_mat:
                    mat_list = bpy.data.materials[mat]
                    me.materials.append(mat_list)

                st.Save_Mat = False
                st.backup_mat[:] = []
                
        st.Display_T_N = False
        
        return {'FINISHED'}
    
###############################
####    TEXTS FONCTIONS    ####
###############################

def draw_text_array(context, text, corner, pos_x, pos_y):
    st = context.window_manager.show_text
    height = context.region.height
    width = context.region.width
    font_id = 0
    blf.size(font_id, st.text_font_size, 72) 
    x_offset = 0
    y_offset = 0
    line_height = (blf.dimensions(font_id, "M")[1] * 1.45)
    if corner == '2' or corner == '4':
        text.reverse()
    for command in text:
        if len(command) == 2:
            Text, Color = command
            bgl.glColor3f(*Color)
            text_width, text_height = blf.dimensions(font_id, Text)
            if corner == '1':
                x = pos_x
                y = height - pos_y - st.text_font_size
            elif corner == '2':
                x = width - pos_x - text_width
                y = height - pos_y - st.text_font_size
            elif corner == '3':
                x = pos_x
                y = pos_y + st.text_font_size
            else:
                x = width - pos_x - text_width
                y = pos_y + st.text_font_size             
            blf.position(font_id, (x + x_offset), (y + y_offset), 0)
            blf.draw(font_id, Text)
            if corner == '1' or corner == '3':
                x_offset += text_width
            else:
                x_offset -= text_width
        else:
            x_offset = 0
            if corner == '1' or corner == '2':               
                y_offset -= line_height
            else:               
                y_offset += line_height

#####################################################################

def obj_info_object(context):
    text = []
    obj_list = []
    st = context.window_manager.show_text 
    if context.object.type == 'MESH':
        label_color = st.label_color
        value_color = st.value_color
        name_color = st.name_color
        CR = "Carriage return"
        corner = st.obj_corner
        pos_x = st.obj_pos_x
        pos_y = st.obj_pos_y 
              
        for obj in context.selected_objects: 
            obj_list.extend([obj.name])
            
        if len(obj_list) > 1:
            for obj in context.selected_objects:
                context.scene.objects.active = bpy.data.objects[obj.name]              
                text.extend([CR, (obj.name, name_color)]) 
                
                quads = tris = ngons = 0
                ngons_to_tris = 0 
                    
                ob = bpy.context.object
                me = ob.data
                bm = bmesh.new()
                bm.from_mesh(me)
               
                for f in bm.faces:                
                    v = len(f.verts)
                    if v == 3:
                        tris += 1 
                    elif v == 4:
                        quads += 1
                    elif v > 4:
                        ngons += 1
                        V = len(f.verts) - 2
                        ngons_to_tris += V
                
                if st.Verts_count_Obj:
                    verts = len(bm.verts)
                    text.extend([(" V: ", label_color), (str(verts), value_color)])
                if st.Faces_count_Obj:
                    faces = len(bm.faces)
                    text.extend([(" F: ", label_color), (str(faces), value_color)])
                if st.Tris_count_Obj:
                    text.extend([(" T: ", label_color), (str(tris) + " ( " + str(tris + quads*2 + ngons_to_tris) + " )", value_color)])   
                if st.Ngons_count_Obj:
                    text.extend([(" Ng: ", label_color), (str(ngons), value_color)])
                
                bm.to_mesh(me)
                bm.free()
        
        elif len(obj_list) == 1:             
            quads = tris = ngons = 0
            ngons_to_tris = 0 
                   
            ob = bpy.context.object
            me = ob.data
            bm = bmesh.new()
            bm.from_mesh(me)
           
            for f in bm.faces:                
                v = len(f.verts)
                if v == 3:
                    tris += 1 
                elif v == 4:
                    quads += 1
                elif v > 4:
                    ngons += 1
                    V = len(f.verts) - 2
                    ngons_to_tris += V
            
            if corner == '3' or corner == '2': 
                if st.Ngons_count_Obj:
                    text.extend([CR, ("Ngons: ", label_color), (str(ngons), value_color)]) 
                if st.Tris_count_Obj:
                    text.extend([CR, ("Tris: ", label_color), (str(tris) + " ( " + str(tris + quads*2 + ngons_to_tris) + " )", value_color)])
                if st.Faces_count_Obj:
                    faces = len(bm.faces)
                    text.extend([CR, ("Faces: ", label_color), (str(faces), value_color)]) 
                if st.Verts_count_Obj:
                    verts = len(bm.verts)
                    text.extend([CR, ("Vertex: ", label_color), (str(verts), value_color)]) 
                                    
            else: 
                if st.Verts_count_Obj:
                    verts = len(bm.verts)
                    text.extend([CR, ("Vertex: ", label_color), (str(verts), value_color)])
                if st.Faces_count_Obj:
                    faces = len(bm.faces)
                    text.extend([CR, ("Faces: ", label_color), (str(faces), value_color)]) 
                if st.Tris_count_Obj:
                    text.extend([CR, ("Tris: ", label_color), (str(tris) + " ( " + str(tris + quads*2 + ngons_to_tris) + " )", value_color)]) 
                if st.Ngons_count_Obj:
                    text.extend([CR, ("Ngons: ", label_color), (str(ngons), value_color)])
            
            bm.to_mesh(me)
            bm.free()
                        
        draw_text_array(context, text, corner, pos_x, pos_y)
    
#####################################################################

def obj_info_scene(context):
    
    st = context.window_manager.show_text
    
    text = []
    
    label_color = st.label_color
    value_color = st.value_color
    CR = "Carriage return"
    
    corner = st.scn_corner
    pos_x = st.scn_pos_x
    pos_y = st.scn_pos_y
    
    if corner == '3' or corner == '2':
        if context.active_object.type == 'CAMERA':
            if st.cam_focal:
                focal = context.object.data.lens
                text.extend([CR, ("Cam focal: ", label_color), (str(round(focal, 3)), value_color)])
        if st.current_frame:
            frame = context.scene.frame_current
            text.extend([CR, ("Current frame: ", label_color), (str(frame), value_color)])
        if st.cam_dist:
            obj_list = []  # we store the loacation vector of each object
            for item in bpy.context.selected_objects:
                obj_list.append(item.location)
            if len(obj_list) == 2:
                distance = sqrt( (obj_list[0][0] - obj_list[1][0])**2 + (obj_list[0][1] - obj_list[1][1])**2 + (obj_list[0][2] - obj_list[1][2])**2)
                text.extend([CR, ("Distance: ", label_color), (str(round(distance, 3)), value_color)])
        if st.obj_count:
            obj_count = []
            for obj in bpy.context.selected_objects:
                obj_count.append(obj)
            text.extend([CR, ("Count obj: ", label_color), (str(len(obj_count)), value_color)])
        
        
        
    else:   
        if st.obj_count:
            obj_count = []
            for obj in bpy.context.selected_objects:
                obj_count.append(obj)
            text.extend([CR, ("Count obj: ", label_color), (str(len(obj_count)), value_color)])
        if st.cam_dist:
            obj_list = []  # we store the loacation vector of each object
            for item in bpy.context.selected_objects:
                obj_list.append(item.location)
            if len(obj_list) == 2:
                distance = sqrt( (obj_list[0][0] - obj_list[1][0])**2 + (obj_list[0][1] - obj_list[1][1])**2 + (obj_list[0][2] - obj_list[1][2])**2)
                text.extend([CR, ("Distance: ", label_color), (str(round(distance, 3)), value_color)])
        if st.current_frame:
            frame = context.scene.frame_current
            text.extend([CR, ("Current frame: ", label_color), (str(frame), value_color)])
        if context.active_object.type == 'CAMERA':
            if st.cam_focal:
                focal = context.object.data.lens
                text.extend([CR, ("Cam focal: ", label_color), (str(round(focal, 3)), value_color)])

    draw_text_array(context, text, corner, pos_x, pos_y)

#####################################################################

def render_info(context):
    
    st = context.window_manager.show_text
    
    text = []
    
    label_color = st.label_color
    value_color = st.value_color
    CR = "Carriage return" 
    corner = st.rder_corner
    pos_x = st.rder_pos_x
    pos_y = st.rder_pos_y
    
    if corner == '3' or corner == '2':
        if st.rder_sample:
            r_sample = context.scene.cycles.samples
            r_p_sample = context.scene.cycles.preview_samples 
            text.extend([CR, ("Render samples: ", label_color), (str(r_sample), value_color), CR, ("Preview samples: ", label_color), (str(r_p_sample), value_color)])
        if st.rder_f_rate:
            f_rate = context.scene.render.fps
            text.extend([CR, ("Frame rate: ", label_color), (str(f_rate) + " fps", value_color)])
        if st.rder_f_range:
            f_start = context.scene.frame_start 
            f_end = context.scene.frame_end
            f_step = context.scene.frame_step
            text.extend([CR, ("Frame_start: ", label_color), (str(f_start), value_color), CR, ("Frame end: ", label_color), (str(f_end), value_color), CR, ("Frame step: ", label_color), (str(f_step), value_color)])
        if st.rder_reso:
            reso_x = context.scene.render.resolution_x
            reso_y = context.scene.render.resolution_y
            text.extend([CR, ("Resolution: ", label_color), (str(reso_x) + " x " + str(reso_y), value_color)])
        
        
        
            
    else:
        if st.rder_reso:
            reso_x = context.scene.render.resolution_x
            reso_y = context.scene.render.resolution_y
            text.extend([CR, ("Resolution: ", label_color), (str(reso_x) + " x " + str(reso_y), value_color)])
        if st.rder_f_range:
            f_start = context.scene.frame_start 
            f_end = context.scene.frame_end
            f_step = context.scene.frame_step
            text.extend([CR, ("Frame_start: ", label_color), (str(f_start), value_color), CR, ("Frame end: ", label_color), (str(f_end), value_color), CR, ("Frame step: ", label_color), (str(f_step), value_color)])
        if st.rder_f_rate:
            f_rate = context.scene.render.fps
            text.extend([CR, ("Frame rate: ", label_color), (str(f_rate) + " fps", value_color)])
        if st.rder_sample:
            r_sample = context.scene.cycles.samples
            r_p_sample = context.scene.cycles.preview_samples 
            text.extend([CR, ("Render samples: ", label_color), (str(r_sample), value_color), CR, ("Preview samples: ", label_color), (str(r_p_sample), value_color)])
    
    draw_text_array(context, text, corner, pos_x, pos_y)
    
#####################################################################

def edit_info(context):
    
    st = context.window_manager.show_text
    
    text = []
    
    label_color = st.label_color
    value_color = st.value_color
    CR = "Carriage return" 
    corner = st.edt_corner
    pos_x = st.edt_pos_x
    pos_y = st.edt_pos_y
    
    ob = bpy.context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    
    quads = tris = ngons = 0
    ngons_to_tris = 0            
    verts = len(bm.verts)
    faces = len(bm.faces)
    
    for f in bm.faces:                
        v = len(f.verts)
        if v == 3: # tris
            tris += 1
            if st.Display_T_N:
                f.material_index = 2
        elif v == 4: # quads
            quads += 1
            if st.Display_T_N:
                f.material_index = 0    
        elif v > 4: # ngons
            ngons += 1
            V = len(f.verts) - 2 # nomber of tris in ngons
            ngons_to_tris += V # get total tris of total ngons
            if st.Display_T_N: 
                f.material_index = 1
    
    bmesh.update_edit_mesh(me)
           
    if corner == '3' or corner == '2': 
        if st.Ngons_count_Edt:
            text.extend([CR, ("Ngons: ", label_color), (str(ngons), value_color)]) 
        if st.Tris_count_Edt:
            text.extend([CR, ("Tris: ", label_color), (str(tris) + " ( " + str(tris + quads*2 + ngons_to_tris) + " )", value_color)])
        if st.Faces_count_Edt:
            faces = len(bm.faces)
            text.extend([CR, ("Faces: ", label_color), (str(faces), value_color)]) 
        if st.Verts_count_Edt:
            verts = len(bm.verts)
            text.extend([CR, ("Vertex: ", label_color), (str(verts), value_color)]) 
                            
    else: 
        if st.Verts_count_Edt:
            verts = len(bm.verts)
            text.extend([CR, ("Vertex: ", label_color), (str(verts), value_color)])
        if st.Faces_count_Edt:
            faces = len(bm.faces)
            text.extend([CR, ("Faces: ", label_color), (str(faces), value_color)]) 
        if st.Tris_count_Edt:
            text.extend([CR, ("Tris: ", label_color), (str(tris) + " ( " + str(tris + quads*2 + ngons_to_tris) + " )", value_color)]) 
        if st.Ngons_count_Edt:
            text.extend([CR, ("Ngons: ", label_color), (str(ngons), value_color)]) 
    
    draw_text_array(context, text, corner, pos_x, pos_y)
    
##################################################################### 

def sculpt_info(context):
    
    st = context.window_manager.show_text
    
    text = []
    
    label_color = st.label_color
    value_color = st.value_color
    CR = "Carriage return" 
    corner = st.sculpt_corner
    pos_x = st.sculpt_pos_x
    pos_y = st.sculpt_pos_y
    
    tool_settings = context.scene.tool_settings
    Detail_Size = tool_settings.sculpt.detail_size
    Constant_Detail = tool_settings.sculpt.constant_detail
    if(hasattr(tool_settings.sculpt, 'detail_percent')):
        Detail_Percent = tool_settings.sculpt.detail_percent
    active_brush = context.tool_settings.sculpt.brush.name            
    detail_refine = bpy.context.scene.tool_settings.sculpt.detail_refine_method
    Detail_Type = bpy.context.scene.tool_settings.sculpt.detail_type_method
    if corner == '3' or corner == '2':
        if st.symmetry_use:            
            if tool_settings.sculpt.use_symmetry_x and tool_settings.sculpt.use_symmetry_y and tool_settings.sculpt.use_symmetry_z:
                text.extend([CR, ("Symmetry: ", label_color), ("X, Y, Z", value_color)])
            elif tool_settings.sculpt.use_symmetry_x and tool_settings.sculpt.use_symmetry_y:
                text.extend([CR, ("Symmetry: ", label_color), ("X, Y", value_color)])
            elif tool_settings.sculpt.use_symmetry_x and tool_settings.sculpt.use_symmetry_z:
                text.extend([CR, ("Symmetry: ", label_color), ("X, Z", value_color)])
            elif tool_settings.sculpt.use_symmetry_y and tool_settings.sculpt.use_symmetry_z:
                text.extend([CR, ("Symmetry: ", label_color), ("Y, Z", value_color)])
            elif tool_settings.sculpt.use_symmetry_x:
                text.extend([CR, ("Symmetry: ", label_color), ("X", value_color)])
            elif tool_settings.sculpt.use_symmetry_y:
                text.extend([CR, ("Symmetry: ", label_color), ("Y", value_color)])
            elif tool_settings.sculpt.use_symmetry_z:
                text.extend([CR, ("Symmetry: ", label_color), ("Z", value_color)])
            else:
                text.extend([CR, ("Symmetry: ", label_color), ("OFF", value_color)])
        if st.brush_strength:
            text.extend([CR, ("Strenght: ", label_color), (str(round(bpy.data.brushes[active_brush].strength, 3)), value_color)])
        if st.brush_radius:
            text.extend([CR, ("Radius: ", label_color), (str(tool_settings.unified_paint_settings.size) + " px", value_color)])            
        if context.sculpt_object.use_dynamic_topology_sculpting:
            if st.detail_type:
                text.extend([CR, (Detail_Type.lower(), label_color)])
            if st.refine_method:                                     
                if tool_settings.sculpt.detail_type_method == 'RELATIVE':
                    text.extend([CR, (detail_refine.lower() + ": ", label_color), (str(round(Detail_Size, 2)) + " px", value_color)])
                elif tool_settings.sculpt.detail_type_method == 'CONSTANT':
                    text.extend([CR, (detail_refine.lower() + ": ", label_color), (str(round(Constant_Detail, 2)) + " %", value_color)])
                elif tool_settings.sculpt.detail_type_method == 'BRUSH':
                    text.extend([CR, (detail_refine.lower() + ": ", label_color), (str(round(Detail_Percent, 2)) + " %", value_color)])                   
                
    else:
        if context.sculpt_object.use_dynamic_topology_sculpting:
            if st.refine_method:                                     
                if tool_settings.sculpt.detail_type_method == 'RELATIVE':
                    text.extend([CR, (detail_refine.lower() + ": ", label_color), (str(round(Detail_Size, 2)) + " px", value_color)])
                elif tool_settings.sculpt.detail_type_method == 'CONSTANT':
                    text.extend([CR, (detail_refine.lower() + ": ", label_color), (str(round(Constant_Detail, 2)) + " %", value_color)])
                elif tool_settings.sculpt.detail_type_method == 'BRUSH':
                    text.extend([CR, (detail_refine.lower() + ": ", label_color), (str(round(Detail_Percent, 2)) + " %", value_color)])                   
            if st.detail_type:
                text.extend([CR, (Detail_Type.lower(), label_color)])
                
        if st.brush_radius:
            text.extend([CR, ("Radius: ", label_color), (str(tool_settings.unified_paint_settings.size) + " px", value_color)])
        
        if st.brush_strength:
            text.extend([CR, ("Strenght: ", label_color), (str(round(bpy.data.brushes[active_brush].strength, 3)), value_color)])
        
        if st.symmetry_use:
            
            if tool_settings.sculpt.use_symmetry_x and tool_settings.sculpt.use_symmetry_y and tool_settings.sculpt.use_symmetry_z:
                text.extend([CR, ("Symmetry: ", label_color), ("X, Y, Z", value_color)])
            elif tool_settings.sculpt.use_symmetry_x and tool_settings.sculpt.use_symmetry_y:
                text.extend([CR, ("Symmetry: ", label_color), ("X, Y", value_color)])
            elif tool_settings.sculpt.use_symmetry_x and tool_settings.sculpt.use_symmetry_z:
                text.extend([CR, ("Symmetry: ", label_color), ("X, Z", value_color)])
            elif tool_settings.sculpt.use_symmetry_y and tool_settings.sculpt.use_symmetry_z:
                text.extend([CR, ("Symmetry: ", label_color), ("Y, Z", value_color)])
            elif tool_settings.sculpt.use_symmetry_x:
                text.extend([CR, ("Symmetry: ", label_color), ("X", value_color)])
            elif tool_settings.sculpt.use_symmetry_y:
                text.extend([CR, ("Symmetry: ", label_color), ("Y", value_color)])
            elif tool_settings.sculpt.use_symmetry_z:
                text.extend([CR, ("Symmetry: ", label_color), ("Z", value_color)])
            else:
                text.extend([CR, ("Symmetry: ", label_color), ("OFF", value_color)])
            
    draw_text_array(context, text, corner, pos_x, pos_y)
              
#####################################################################   
                     
def draw_text_callback(self, context):
    
    st = context.window_manager.show_text
    
    if context.active_object and (context.object.type == 'MESH' or context.object.type == 'CAMERA') and context.window_manager.show_text.enabled:
        
        ###  SCULPT MODE  ###
        
        if context.object.mode == 'OBJECT':
            if st.obj_object_enable:
                obj_info_object(context)               
            if st.obj_scn_enable:
                obj_info_scene(context)
            if st.rder_enable:
                render_info(context)
                
        
        elif context.object.mode == 'EDIT':
            if st.edt_object_enable:
                edit_info(context)
        
        elif context.object.mode == 'SCULPT':
            if st.sculpt_enable:
                sculpt_info(context)
            
            


########################
####    OPERATOR    ####
########################

class VIEW3D_OT_ADH_display_text(bpy.types.Operator):
    """Display detail_refine_method active"""
    bl_idname = "view3d.adh_display_text"
    bl_label = "Display Text"
    bl_options = {'REGISTER'}
    
    _handle = None
    
    def modal(self, context, event):
        context.area.tag_redraw()
        if not context.window_manager.show_text.enabled:
            return {'CANCELLED'}
        return {'PASS_THROUGH'}
     
    @staticmethod
    def handle_add(self, context):
        VIEW3D_OT_ADH_display_text._handle = bpy.types.SpaceView3D.draw_handler_add(
               draw_text_callback, 
               (self, context),
               'WINDOW', 'POST_PIXEL')
    
    @staticmethod
    def handle_remove(context):
        _handle = VIEW3D_OT_ADH_display_text._handle
        if _handle != None:
            bpy.types.SpaceView3D.draw_handler_remove(_handle, 'WINDOW')
        VIEW3D_OT_ADH_display_text._handle = None
                        
    def invoke(self, context, event):
        if context.window_manager.show_text.enabled == False:
            context.window_manager.show_text.enabled = True
            context.window_manager.modal_handler_add(self)
            VIEW3D_OT_ADH_display_text.handle_add(self, context)

            return {'RUNNING_MODAL'}
        else:
            context.window_manager.show_text.enabled = False
            VIEW3D_OT_ADH_display_text.handle_remove(context)

            return {'CANCELLED'}

        return {'CANCELLED'}

###################################
####    VIEWPORT INFO PANEL    ####
###################################
   
class VIEW3D_PT_ADH_display_matrix(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Viewport info"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        
        return context.active_object is not None and context.object.type == 'MESH' or context.object.type == 'CAMERA'
    
    def draw(self, context):
        layout = self.layout
        st = context.window_manager.show_text
        mode = context.object.mode
        
        if context.window_manager.show_text.enabled:        
            layout.operator('view3d.adh_display_text', text="Enabled", icon='RESTRICT_VIEW_OFF')
        else:
            layout.operator('view3d.adh_display_text', text="Disabled", icon='RESTRICT_VIEW_ON')
        if mode == 'EDIT':
            if st.Display_T_N:
                layout.operator("object.hidde_faces", text="Hidde faces color", icon="RESTRICT_VIEW_ON")
            elif st.Display_T_N == False:
                layout.operator("object.setup_materials", text="Show faces color", icon="COLOR")
        if mode == 'OBJECT':
            if st.Display_T_N:
                    layout.operator("object.hidde_faces", text="Hidde faces color", icon="RESTRICT_VIEW_ON")
        if st.panel_options:
            layout.prop(st, "panel_options", text="Options", icon="TRIA_UP")
            ### OBJECT MODE ###
            # object infos
            box = layout.box()
            row = box.row()
            box.label(text="### OBJECT MODE ###")
            row = box.row()
            row.prop(st, "obj_object_enable", icon="OBJECT_DATA")
            row = box.row(align=True)        
            row.prop(st, "Verts_count_Obj")
            row.prop(st, "Tris_count_Obj") 
            row = box.row(align=True)         
            row.prop(st, "Faces_count_Obj")
            row.prop(st, "Ngons_count_Obj")
            row = box.row()
            row.prop(st, "obj_corner", expand=True)
            row = box.row()
            row.prop(st, "obj_pos")
            if st.obj_pos:
                row = box.row(align=True)
                row.prop(st, "obj_pos_x")
                row.prop(st, "obj_pos_y")             
            row = box.row()
            row.label(text=" ")
            # scene infos
            row = box.row()            
            row.prop(st, "obj_scn_enable", icon="SCENE_DATA")
            row = box.row(align=True)
            row.prop(st, "obj_count")
            row.prop(st, "cam_dist")
            row = box.row(align=True)
            row.prop(st, "current_frame")
            row.prop(st, "cam_focal")
            row = box.row()
            row.prop(st, "scn_corner", expand=True)
            row = box.row()
            row.prop(st, "scn_pos")
            if st.scn_pos:
                row = box.row(align=True)
                row.prop(st, "scn_pos_x")
                row.prop(st, "scn_pos_y")
            row = box.row()
            row.label(text=" ")
            # render infos
            row = box.row()            
            row.prop(st, "rder_enable", icon="RENDER_STILL")
            row = box.row(align=True)
            row.prop(st, "rder_reso")
            row.prop(st, "rder_f_range")
            row = box.row(align=True)
            row.prop(st, "rder_f_rate")
            row.prop(st, "rder_sample")
            row = box.row()
            row.prop(st, "rder_corner", expand=True)
            row = box.row()
            row.prop(st, "rder_pos")
            if st.rder_pos:
                row = box.row(align=True)
                row.prop(st, "rder_pos_x")
                row.prop(st, "rder_pos_y")
            layout.separator()
                
            ### EDIT MODE ###
            box = layout.box()
            row = box.row()
            box.label(text="### EDIT MODE ###")
            row = box.row()            
            row.prop(st, "edt_object_enable", icon="EDITMODE_HLT")
            row = box.row(align=True)
            row.prop(st, "Verts_count_Edt")
            row.prop(st, "Tris_count_Edt")
            row = box.row(align=True)            
            row.prop(st, "Faces_count_Edt")
            row.prop(st, "Ngons_count_Edt")
            row = box.row()
            row.prop(st, "edt_corner", expand=True)
            row = box.row()
            row.prop(st, "edt_pos")
            if st.edt_pos:
                row = box.row(align=True)
                row.prop(st, "edt_pos_x")
                row.prop(st, "edt_pos_y")
            layout.separator() 
               
            # Sculpt box
            box = layout.box()
            row = box.row()
            box.label(text="### SCULPT MODE ###")
            row = box.row()            
            row.prop(st, "sculpt_enable", icon="SCULPTMODE_HLT")
            row = box.row(align=True)
            row.prop(st, "brush_radius")
            row.prop(st, "brush_strength")
            row = box.row(align=True) 
            row.prop(st, "symmetry_use")
            row = layout.row()
            box.label(text="Enable only with Dyntopo activate:")
            row = box.row(align=True) 
            row.prop(st, "refine_method")
            row.prop(st, "detail_type")
            row = box.row()
            row.prop(st, "sculpt_corner", expand=True)
            row = box.row()
            row.prop(st, "sculpt_pos")
            if st.sculpt_pos:
                row = box.row(align=True)
                row.prop(st, "sculpt_pos_x")
                row.prop(st, "sculpt_pos_y")
                        
            box = layout.box()
            row = box.row()
            row.label(text="### Customization ###")
            row = box.row(align=True)
            row.prop(st, "text_font_size")
            row = box.row(align=True)
            row.prop(st, "label_color")
            row.prop(st, "value_color")
            row.prop(st, "name_color")
        else:
            layout.prop(st, "panel_options", text="Select your options", icon="TRIA_RIGHT")


##########################
####    PROPERTIES    ####
##########################

class ADH_DisplayTextProps(bpy.types.PropertyGroup):
    
    enabled = bpy.props.BoolProperty(default=False)
    panel_options = bpy.props.BoolProperty(default=False)
    ### OBJECT MODE ###
    # object infos
    obj_object_enable = bpy.props.BoolProperty(default=True, name="Object info")
    Ngons_count_Obj = bpy.props.BoolProperty(default=False, name="Ngon count")
    Tris_count_Obj = bpy.props.BoolProperty(default=False, name="Tri count")
    Verts_count_Obj = bpy.props.BoolProperty(default=False, name="Vertex count") 
    Faces_count_Obj = bpy.props.BoolProperty(default=False, name="Face count")
    obj_count = bpy.props.BoolProperty(default=False, name="Object count")
    obj_corner = bpy.props.EnumProperty(items=(('1', "Top L", ""),
                                               ('2', "Top R", ""),
                                               ('3', "Bot L", ""),
                                               ('4', "Bot R", "")),                                         
                                               default='1', name=" ")
    obj_pos = bpy.props.BoolProperty(default=False, name="Advance") 
    obj_pos_x = bpy.props.IntProperty(name="Pos X", default=29, min=0, max=200)                                            
    obj_pos_y = bpy.props.IntProperty(name="Pos Y", default=75, min=0, max=200) 
    # scene info
    obj_scn_enable = bpy.props.BoolProperty(default=True, name="Scene info")
    obj_count = bpy.props.BoolProperty(default=False, name="Object count")
    cam_dist = bpy.props.BoolProperty(default=False, name="Distance between objects")
    current_frame = bpy.props.BoolProperty(default=False, name="Current frame")
    cam_focal = bpy.props.BoolProperty(default=False, name="Focal camera")
    scn_corner = bpy.props.EnumProperty(items=(('1', "Top L", ""),
                                               ('2', "Top R", ""),
                                               ('3', "Bot L", ""),
                                               ('4', "Bot R", "")),                                         
                                               default='4', name=" ")
    scn_pos = bpy.props.BoolProperty(default=False, name="Advance") 
    scn_pos_x = bpy.props.IntProperty(name="Pos X", default=29, min=0, max=200)                                            
    scn_pos_y = bpy.props.IntProperty(name="Pos Y", default=75, min=0, max=200)  
    # render info
    rder_enable = bpy.props.BoolProperty(default=True, name="Render info")
    rder_reso = bpy.props.BoolProperty(default=False, name="Resolution")
    rder_f_range = bpy.props.BoolProperty(default=False, name="Frame range", description="Display Start frame, End frame and Frame step")
    rder_f_rate = bpy.props.BoolProperty(default=False, name="Frame rate")
    rder_sample = bpy.props.BoolProperty(default=False, name="Sampling", description="Display render and preview samples") 
    rder_corner = bpy.props.EnumProperty(items=(('1', "Top L", ""),
                                               ('2', "Top R", ""),
                                               ('3', "Bot L", ""),
                                               ('4', "Bot R", "")),                                         
                                               default='2', name=" ")
    rder_pos = bpy.props.BoolProperty(default=False, name="Advance") 
    rder_pos_x = bpy.props.IntProperty(name="Pos X", default=29, min=0, max=200)                                            
    rder_pos_y = bpy.props.IntProperty(name="Pos Y", default=75, min=0, max=200)
    
                                                 
    # Edit properties
    edt_object_enable = bpy.props.BoolProperty(default=True, name="Object info")
    Ngons_count_Edt = bpy.props.BoolProperty(default=False, name="Ngon count")
    Tris_count_Edt = bpy.props.BoolProperty(default=False, name="Tri count")
    Display_T_N = bpy.props.BoolProperty(default=False)
    Verts_count_Edt = bpy.props.BoolProperty(default=False, name="Vertex count") 
    Faces_count_Edt = bpy.props.BoolProperty(default=False, name="Face count")
    edt_corner = bpy.props.EnumProperty(items=(('1', "Top L", ""),
                                               ('2', "Top R", ""),
                                               ('3', "Bot L", ""),
                                               ('4', "Bot R", "")),                                         
                                               default='1', name=" ")
    edt_pos = bpy.props.BoolProperty(default=False, name="Advance")
    edt_pos_x = bpy.props.IntProperty(name="Pos X", default=29, min=0, max=200)                                            
    edt_pos_y = bpy.props.IntProperty(name="Pos Y", default=75, min=0, max=200)                            
    
    # Sculpt properties
    sculpt_enable = bpy.props.BoolProperty(default=True, name="Sculpt tools info")
    refine_method = bpy.props.BoolProperty(default=False, name="Detail refine method")
    detail_type = bpy.props.BoolProperty(default=False, name="Detail type method")
    brush_radius = bpy.props.BoolProperty(default=False, name="Brush radius")
    brush_strength = bpy.props.BoolProperty(default=False, name="Brush strenght")
    symmetry_use = bpy.props.BoolProperty(default=False, name="Symetry axis")
    sculpt_corner = bpy.props.EnumProperty(items=(('1', "Top L", ""),
                                                  ('2', "Top R", ""),
                                                  ('3', "Bot L", ""),
                                                  ('4', "Bot R", "")),                                         
                                                  default='1', name=" ")
    sculpt_pos = bpy.props.BoolProperty(default=False, name="Advance")
    sculpt_pos_x = bpy.props.IntProperty(name="Pos X", default=29, min=0, max=200)                                            
    sculpt_pos_y = bpy.props.IntProperty(name="Pos Y", default=75, min=0, max=200)
    
    # Customization properties
    text_font_size = bpy.props.IntProperty(name="Font", default=18, min=10, max=50)
    label_color = bpy.props.FloatVectorProperty(name="Label", default=(1.0, 1.0, 1.0), min=0, max=1, subtype='COLOR')
    value_color = bpy.props.FloatVectorProperty(name="Value", default=(1.0, 1.0, 1.0), min=0, max=1, subtype='COLOR')
    name_color = bpy.props.FloatVectorProperty(name="Name", default=(1.0, 1.0, 1.0), min=0, max=1, subtype='COLOR')
    
    # Material properties
    Save_Mat = bpy.props.BoolProperty(default=False)
    backup_mat = []
    

def register():
    bpy.utils.register_module(__name__)
    bpy.types.WindowManager.show_text = bpy.props.PointerProperty(type=ADH_DisplayTextProps)

def unregister():
    bpy.utils.unregister_module(__name__)
    VIEW3D_OT_ADH_display_text.handle_remove(bpy.context)
    del bpy.types.WindowManager.show_text

if __name__ == "__main__":
    register()
