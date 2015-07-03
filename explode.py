import bpy

from bpy import context
from math import sin, cos, radians, pi
from .rustext1111 import convert_to_mesh

def explode_tex(x,y,z, stic, xx, yy, zz):
    bpy.ops.object.quick_explode(frame_start=x, frame_end=y)
    bpy.context.object.collision.permeability = (z)
    bpy.context.object.collision.stickiness = (stic)
    bpy.context.object.active_material.diffuse_color = (xx, yy, zz)

class MyExplodeText(bpy.types.Operator):
    bl_idname = "object.explode_text"
    bl_label = "explode text"
    bl_description = "Set the Text to be exploted"
    bl_context = "objectmode"
    bl_options = {'REGISTER', 'UNDO'}
    
    bpy.types.Object.x = bpy.props.IntProperty(name='Start Frame', default = 1)
    bpy.types.Object.y = bpy.props.IntProperty(name='End Frame', default = 50)
    bpy.types.Object.z = bpy.props.IntProperty(name='Count Of Particles', default = 0)
    bpy.types.Object.stic = bpy.props.IntProperty(name='Stickiness', default = 0)
    bpy.types.Object.r = bpy.props.FloatProperty(name='R Color', default = 0.428644)
    bpy.types.Object.g = bpy.props.FloatProperty(name='G Color', default = 0.347955)
    bpy.types.Object.b = bpy.props.FloatProperty(name='B Color', default = 0.8)
 
    def execute(self, context):
        obj = context.active_object
        if bpy.context.object.type != 'MESH':
            convert_to_mesh()
        
        if len(bpy.context.object.particle_systems.keys()) != 0:
            bpy.ops.object.particle_system_remove()
        
        explode_tex(obj.x, obj.y, obj.z, obj.stic, obj.r, obj.g, obj.b)
        
        
        
        return{'FINISHED'} 




class RusTextExplodePanel(bpy.types.Panel):
    """A RusTextExplode Panel in the Viewport Toolbar"""
    bl_label = "Explode Text Tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_context = 'objectmode'
    
    @classmethod    
    def poll(self, context ):
        if context.object:
            return True
            

    def draw(self, context): #Функция отображающая содержимое нашего меню
        layout = self.layout #Переменной layout присваивается выражение self.layout
        layout.label(text="Explode Text")	#С помощью label выводится любой текст
        obj = bpy.context.object

        row = layout.row()
        
        split = layout.split()
        
        col = split.column(align=True)

        col.operator("object.explode_text", text="push to explode text!!!")
        if obj.x:
            row = layout.row()
            row.prop(obj, "x")
            #row.operator()
            
            row = layout.row()
            row.prop(obj, "y")
            
            row = layout.row()
            row.prop(obj, "z")
            
            row = layout.row()
            row.prop(obj, "stic")
            
            row = layout.row()
            row.prop(obj, "r")
            
            row = layout.row()
            row.prop(obj, "g")
            
            row = layout.row()
            row.prop(obj, "b")
            



def register():
    bpy.utils.register_class(MyExplode)
    
    
def unregister():
    bpy.utils.unregister_class(MyExplode)
    
if __name__ == "__main__":
    register()
    
