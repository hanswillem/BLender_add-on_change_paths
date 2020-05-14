bl_info = {
    'name' : 'Change Paths',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (2, 83, 0  ),
    'location' : 'Properties Panel > Output > Change Paths',
    'description' : 'Changes output paths',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'rendering'
    }

#imports
import bpy
import os.path
import subprocess

def main_check_mismatch():
    if os.path.exists(r'C:\Users\hansw') and r'C:\Users\polpot' in bpy.context.scene.render.filepath:
        return True
    if os.path.exists(r'C:\Users\polpot') and r'C:\Users\hansw' in bpy.context.scene.render.filepath:
        return True
    else:
        return False

def main_check_node_mismatch():
    if not bpy.context.scene.use_nodes:
        return False
    else:
        for i in bpy.context.scene.node_tree.nodes:
            if i.type == 'OUTPUT_FILE':
                if i.base_path != os.path.dirname(bpy.context.scene.render.filepath):
                    return True
                    break
                else:
                    return False

def main_get_pc():
    if os.path.exists(r'C:\Users\hansw'):
        return 'Home'
    if os.path.exists(r'C:\Users\polpot'):
        return 'Redrum'

def main_change_paths():
    if os.path.exists(r'C:\Users\hansw'):
        s1 = r'C:\Users\polpot'
        s2 = r'C:\Users\hansw'
    if os.path.exists(r'C:\Users\polpot'):
        s1 = r'C:\Users\hansw'
        s2 = r'C:\Users\polpot'   

    bpy.context.scene.render.filepath = bpy.context.scene.render.filepath.replace(s1, s2)
    # file output nodes
    for i in bpy.context.scene.node_tree.nodes:
        if i.type == 'OUTPUT_FILE':
            i.base_path = i.base_path.replace(s1, s2)

#update the file output node paths bases on the render path
def main_update_file_output_nodes():
    for i in bpy.context.scene.node_tree.nodes:
        if i.type == 'OUTPUT_FILE':
            i.base_path = os.path.dirname(bpy.context.scene.render.filepath)

def main_open_folder():
    subprocess.Popen('explorer ' + os.path.dirname(bpy.context.scene.render.filepath))


#operator class
class SCRIPT_OT_update_paths(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Update File Paths'
    bl_idname = 'script.update_paths'

    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return 2 > 1
    
    #execute
    def execute(self, context):
        main_change_paths()
        return {'FINISHED'}

#operator class
class SCRIPT_OT_update_nodes(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Update File Output Nodes'
    bl_idname = 'script.update_nodes'

    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return 2 > 1
    
    #execute
    def execute(self, context):
        main_update_file_output_nodes()
        return {'FINISHED'}

#operator class
class SCRIPT_OT_open_folder(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Open Folder'
    bl_idname = 'script.open_folder'

    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return 2 > 1
    
    #execute
    def execute(self, context):
        main_open_folder()
        return {'FINISHED'}

#panel class
class VIEW_3D_PT_change_paths(bpy.types.Panel):
    #panel attributes
    """Tooltip"""
    bl_label = 'Change Paths'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_category = 'Change Paths'
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        layout.label(text = f'PC: {main_get_pc()}')
        col = layout.column(align = True)

        if main_check_mismatch():
            btn_text = 'Switch PC'
            col.operator('script.update_paths', text=btn_text, icon='ERROR')
  
        if main_check_node_mismatch():
            col.operator('script.update_nodes', text='Update Nodes', icon='ERROR')

        col.operator('script.open_folder', text='Open Render Folder', icon='FILE_FOLDER')

   
#registration
classes = (
    VIEW_3D_PT_change_paths,
    SCRIPT_OT_update_paths,
    SCRIPT_OT_update_nodes,
    SCRIPT_OT_open_folder,
    )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


#enable to test the addon by running this script
if __name__ == '__main__':
    register()
