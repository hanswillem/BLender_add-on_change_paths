bl_info = {
    'name' : 'Change Paths',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (2, 80, 0  ),
    'location' : 'View 3D > Tools > My Addon',
    'description' : 'Changes output paths',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'rendering'
    }


#imports
import bpy
import os.path

#the main functions
def main_change_paths(s1, s2):
    bpy.context.scene.render.filepath = bpy.context.scene.render.filepath.replace(s1, s2)
    # file output nodes
    for i in bpy.context.scene.node_tree.nodes:
        if i.type == 'OUTPUT_FILE':
            i.base_path = i.base_path.replace(s1, s2)

def main_update_file_output_nodes():
    for i in bpy.context.scene.node_tree.nodes:
        if i.type == 'OUTPUT_FILE':
            i.base_path = os.path.dirname(bpy.context.scene.render.filepath)



#operator class
class SCRIPT_OT_change_paths(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Change Paths'
    bl_idname = 'script.change_paths'

    pc_path_01: bpy.props.StringProperty(name = 'pc_path_01')
    pc_path_02: bpy.props.StringProperty(name = 'pc_path_02')
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return 2 > 1
    
    #execute
    def execute(self, context):
        main_change_paths(self.pc_path_01, self.pc_path_02)
        return {'FINISHED'}

#operator class
class SCRIPT_OT_update_file_output_nodes(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Update File Output Nodes'
    bl_idname = 'script.update_file_output_nodes'

    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return 2 > 1
    
    #execute
    def execute(self, context):
        main_update_file_output_nodes()
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
        col = layout.column(align = True)
        row = layout.row(align = True)

        props = row.operator('script.change_paths', text='PC Redrum',)
        props.pc_path_01 = r'C:\Users\hansw'
        props.pc_path_02 = r'C:\Users\polpot'

        props = row.operator('script.change_paths', text='PC Home',)
        props.pc_path_01 = "polpot"
        props.pc_path_02 = "hansw"

        row.operator('script.update_file_output_nodes', text='Update Nodes')

   
#registration
classes = (
    VIEW_3D_PT_change_paths,
    SCRIPT_OT_change_paths,
    SCRIPT_OT_update_file_output_nodes
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
