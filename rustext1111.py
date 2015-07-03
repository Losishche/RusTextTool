#--------------------------------------------------#
#---- RUSSIAN TEXT INFO ---------------------------#
#--------------------------------------------------#
'''
bl_info = {
    "name": "Russian text tool",
    "description": "Russian text tool Addon",
    "version": (1, 1, 1),
    "category": "User",
    "author": "Stas Gorbachev",
    "warning": ""
}

'''
import bpy

from bpy import context
from math import sin, cos, radians, pi

#--------------------------------------------------#
#---- FUNCTIONS -----------------------------------#
#--------------------------------------------------#

# создать русский текст
def create_rus_text(text):
	bpy.ops.object #.mode_set(mode="OBJECT")
	if bpy.data.fonts.find('Tahoma') == -1:
		bpy.ops.font.open(filepath="/usr/share/blender/scripts/addons/blen_txt/tahoma.ttf")
	bpy.ops.object.text_add(view_align = False, enter_editmode=False, location=(0,1,1))
	bpy.ops.window.managers
	ob = bpy.context.object
	ob.data.font = bpy.data.fonts['Tahoma']
	ob.data.body = text
	ob.data.extrude = 0.05                              

# создать русский текст из файла 
def create_rus_text_from_file(context, filepath):
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    
    print(data)  
    create_rus_text(data)

# анимация текста 
def animate_text(obj, n, l2, l3, l4, l5):
    location = obj.location[1]
    obj.keyframe_insert(data_path="location", frame=n, index=1)  
    
    obj.location[1] = 0.01
    obj.keyframe_insert(data_path="location", frame=l2, index=1)  
    
    obj.location[1] = location
    obj.keyframe_insert(data_path="location", frame=l3, index=1)  
    
    obj.location[1] = 0.01
    obj.keyframe_insert(data_path="location", frame=l4, index=1)  
    
    obj.location[1] = location
    obj.keyframe_insert(data_path="location", frame=l5, index=1)  
    
    bpy.ops.screen.frame_jump()

# разбивка текста по частям
def separate_text_to_chars():
	#bpy.ops.object.convert(target='MESH') 
    bpy.ops.object.mode_set(mode='EDIT')                    # входим в режим редактирования
    bpy.ops.mesh.select_all()                               # выбираем все вершины
    bpy.ops.mesh.remove_doubles()                           # удаляем дубликаты вершин
    bpy.ops.mesh.separate(type='LOOSE')                     # разделяем MESH по несоединенным частям 
    bpy.ops.object.mode_set(mode='OBJECT')                  # выходим из режима редактирования
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS') # устанавливаем центральную точку объекта

# конвертирование типа текст в тип mesh
def convert_to_mesh():
    obj = bpy.ops.object.convert(target='MESH')                   # конвертируем из типа текст в MESH (набор вершин и многоугольников, определяющих форму трёхмерного объекта)
    #bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')      # устанавливаем центральную точку объекта
    return obj

# получаем настройки системы частиц
def particle_get_settings(context):
    if context.particle_system:
        return context.particle_system.settings
    elif isinstance(context.space_data.pin_id, bpy.types.ParticleSettings):
        return context.space_data.pin_id
    return None


# создаём систему частиц
def particc(obj):
	bpy.ops.object.particle_system_add()                    # объект "система частиц"
	#obj.posemode_toggle()
	#context.active_object.randomize_transform(random_seed=5, use_delta=False, use_loc=True, loc=(0.5, 0.5, 0.5), use_rot=True, rot=(0.0, 0.0, 0.0), use_scale=True, scale_even=False, scale=(1.0, 1.0, 1.0))
	bpy.data.particles["ParticleSettings"].use_parent_particles = True 
	bpy.data.particles["ParticleSettings"].render_type = "BILLBOARD" # придаём частицам форму "досок"
	bpy.data.particles["ParticleSettings"].child_type = 'SIMPLE'     # задаём тип распадающихся частиц
	#bpy.ops.particle.connect_hair(all=False)
    #bpy.ops.object.paths_calculate(start_frame=1, end_frame=250)


# создаём систему частиц для анимации звуковых частот из текста
def partic_to_sound_animation():
    bpy.context.object.location[0] = 0 									#меняем координаты положения объекта на 0, 0, 0
    bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = 0
    #bpy.ops.object.editmode_toggle()
    #bpy.context.object.data.extrude = 0
    #bpy.ops.object.editmode_toggle()
    bpy.ops.object.convert(target="MESH") 								# конвертируем в Mesh
    
    obj_n = bpy.context.object 											# запоминаем объект "текст"
    obj_d = bpy.context.object.data.name 								# запоминаем имя объекта "текст"
    #obj_n_grid = bpy.context.object.copy()
    print(obj_d)
    bpy.context.object.show_wire = True 
    bpy.context.object.show_all_edges = True
    bpy.ops.object.modifier_add(type='SOLIDIFY') 						# добавляем модификатор SOLIDIFY
    bpy.context.object.modifiers["Solidify"].thickness = 0
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify") # применяем модификатор 

    bpy.ops.object.modifier_add(type="REMESH")
    bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False  # добавляем модификатор REMESH
    bpy.context.object.modifiers["Remesh"].octree_depth = 7
    bpy.context.object.modifiers["Remesh"].scale = 0.950
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")   # применяем модификатор 


    bpy.ops.object.mode_set(mode='EDIT') 
    turn = bpy.data.meshes[obj_d].vertices[0].co[2]						#запоминаем в переменную координату z первой вершины объекта
    ind = bpy.data.meshes[obj_d].vertices[0].index						#запоминаем индекс первой вершины объекта
    for i in range(0, len(bpy.data.meshes[obj_d].vertices.items())):	# c помощью цикла находим координату и индекс объекта у которого наибольшее значение числа по координате z
        if bpy.data.meshes[obj_d].vertices[i].co[2]>turn:
            turn = bpy.data.meshes[obj_d].vertices[i].co[2]
            ind = bpy.data.meshes[obj_d].vertices[i].index
        
    print(ind)

    #lis_ind_vert = []
    bpy.ops.object.mode_set(mode='OBJECT') 
    for i in range(0, len(bpy.data.meshes[obj_d].vertices.items())):	# с помощью цикла, выделяем все вершины, у которых координата z меньше найденной наибольшей (для последующего удаления)
        if bpy.data.meshes[obj_d].vertices[i].co[2] < turn:
            bpy.data.meshes[obj_d].vertices[i].select = True
            
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.delete(type = 'VERT')

    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.particle_system_add()
    ps = bpy.context.object.particle_systems.active.settings.name
    ps_obj = bpy.context.object.particle_systems.active.settings
    bpy.data.particles[ps].normal_factor = 0
    bpy.data.particles[ps].effector_weights.gravity = 0
    bpy.ops.mesh.primitive_cube_add(radius=1)
    cubus = bpy.context.object
    cubus_name = bpy.context.object.name
    bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, False, False, False, False, False,\
     False, False, False, False, False, False, False, False, False, False,))

    bpy.ops.material.new()
    lm = bpy.data.materials.__len__() - 1
    cust_active_mater = bpy.data.materials[lm].name
    cubus.active_material = bpy.data.materials[lm]
    #bpy.data.meshes['Cube.001'].materials.append(bpy.data.materials['Material.012'])
    bpy.data.materials[bpy.data.materials[lm].name].diffuse_color = (0.8, 0, 0.0293678)
    

    bpy.data.particles[ps].render_type = 'OBJECT'
    bpy.data.particles[ps].dupli_object = bpy.data.objects[cubus_name]

    cubus.scale[2] = 5
    
    bpy.data.particles[ps].particle_size = 0.02

    bpy.context.scene.render.engine = 'CYCLES'
    
    bpy.data.materials[cust_active_mater].use_nodes = True  #включаем режим использования нод
    new_node_ObjectInfo = bpy.data.materials[cust_active_mater].node_tree.nodes.new(type = 'ShaderNodeObjectInfo')  #создаём новую ноду для материала куба, вид ObjectInfo
    ln_node = len(bpy.data.materials[cust_active_mater].node_tree.nodes.keys()) - 1 					 #созраняем индекс последней созданной ноды объекта в переменную
    out = bpy.data.materials[cust_active_mater].node_tree.nodes[ln_node].outputs['Random']  			 #сохраняем объект Random выхода из ноды ObjectInfo в переменную
    inn = bpy.data.materials[cust_active_mater].node_tree.nodes['Diffuse BSDF'].inputs['Color']          #сохраняем объект Random входа в ноду Diffuse BSDF в переменную
    #bpy.data.materials['Material.001'].node_tree.nodes['new_node']										 #cjp
    bpy.data.materials[cust_active_mater].node_tree.links.new(inn, out)									 #создаём линк между этими двумя нодам
    new_node_ShaderHueSaturation = bpy.data.materials[cust_active_mater].node_tree.nodes.new(type="ShaderNodeHueSaturation")
    inn_saturation_hue = bpy.data.materials[cust_active_mater].node_tree.nodes[new_node_ShaderHueSaturation.name].inputs['Hue']
    inn_saturation_value = bpy.data.materials[cust_active_mater].node_tree.nodes[new_node_ShaderHueSaturation.name].inputs['Value']
    out_saturation_color = bpy.data.materials[cust_active_mater].node_tree.nodes[new_node_ShaderHueSaturation.name].outputs['Color']
    bpy.data.materials[cust_active_mater].node_tree.links.new(inn_saturation_hue, out)
    bpy.data.materials[cust_active_mater].node_tree.links.new(inn_saturation_value, out)
    bpy.data.materials[cust_active_mater].node_tree.links.new(inn, out_saturation_color)
    bpy.data.materials[cust_active_mater].node_tree.nodes['Hue Saturation Value'].inputs[4].default_value = (0.8, 0.098, 0.12, 1)
    bpy.data.particles[ps].lifetime = 25
    bpy.data.particles[ps].lifetime_random = 1
    bpy.data.particles[ps].frame_end = 250
    #bpy.context.space_data.viewport_shade = 'SOLID'
    bpy.data.particles[ps].count = 4000
    
    #obj_n.use_disk_cache = True
    #bpy.ops.ptcache.bake(bake=True)
    
    #bpy.data.objects[cubus.name].select = True
    #cubus_two = cubus.copy()
    #cubus_two.location = (2,2,2)
    #print(cubus_two.name, cubus_two.layers[0], cubus_two.layers[1])
    #bpy.context.scene.objects.link(cubus_two) # связываем объект со сценой
    #bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, False, False, False, False, False,\
    #False, False, False, False, False, False, False, False, False, False,))
    #cubus_two.layers[0]  = False
    #cubus_two.layers[1]  = True
    
    bpy.ops.mesh.primitive_cube_add(radius=1)
    cubus_two = bpy.context.object
    cubus_two_name = bpy.context.object.name
    bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, False, False, False, False, False,\
     False, False, False, False, False, False, False, False, False, False,))
    
    
    
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=20, radius=2, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(False, False, True, False, False, False, \
    False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    gridd = bpy.context.object
    #gridd = len(bpy.data.objects) - 1
    bpy.context.object.show_wire = True
    bpy.context.object.show_all_edges = True
    
    bpy.ops.object.particle_system_add()
    
    #bpy.context.object.particle_systems.active.settings = ps_obj
    
    ps_grid_name = bpy.context.object.particle_systems.active.settings.name
    ps_obj_grig = bpy.context.object.particle_systems.active.settings
    bpy.data.particles[ps_grid_name].normal_factor = 0
    bpy.data.particles[ps_grid_name].effector_weights.gravity = 0
    bpy.data.particles[ps_grid_name].frame_end = 1
    bpy.data.particles[ps_grid_name].lifetime = 250
    bpy.data.particles[ps_grid_name].count = 600

    
    bpy.ops.material.new()
    lm_two = bpy.data.materials.__len__() - 1
    cust_active_mater_cubus_two = bpy.data.materials[lm_two].name
    cubus_two.active_material = bpy.data.materials[lm_two]
    #bpy.data.meshes['Cube.001'].materials.append(bpy.data.materials['Material.012'])
    bpy.data.materials[bpy.data.materials[lm_two].name].diffuse_color = (0.8, 0, 0.0293678)
    

    bpy.data.particles[ps_grid_name].render_type = 'OBJECT'
    bpy.data.particles[ps_grid_name].dupli_object = bpy.data.objects[cubus_two.name]

    cubus.scale[2] = 5
    
    bpy.data.particles[ps_grid_name].particle_size = 0.02
    
    bpy.data.materials[cust_active_mater_cubus_two].use_nodes = True  #включаем режим использования нод
    new_node_ParticleInfo = bpy.data.materials[cust_active_mater_cubus_two].node_tree.nodes.new(type = 'ShaderNodeParticleInfo')  #создаём новую ноду для материала ВТОРОГО куба, вид ParticleInfo
    ln_node_cube_two = len(bpy.data.materials[cust_active_mater_cubus_two].node_tree.nodes.keys()) - 1 					 #созраняем индекс последней созданной ноды объекта в переменную
    
    out_two = bpy.data.materials[cust_active_mater_cubus_two].node_tree.nodes[ln_node_cube_two].outputs['Location']  			 #сохраняем объект Location выхода из ноды ParticleInfo в переменную
    inn_two = bpy.data.materials[cust_active_mater_cubus_two].node_tree.nodes['Diffuse BSDF'].inputs['Color']          #сохраняем объект Random входа в ноду Diffuse BSDF в переменную
    #bpy.data.materials['Material.001'].node_tree.nodes['new_node']										 #cjp
    bpy.data.materials[cust_active_mater_cubus_two].node_tree.links.new(inn_two, out_two)									 #создаём линк между этими двумя нодам
    new_node_ShaderHueSaturation_two = bpy.data.materials[cust_active_mater_cubus_two].node_tree.nodes.new(type="ShaderNodeHueSaturation")
    inn_saturation_hue_two = bpy.data.materials[cust_active_mater_cubus_two].node_tree.nodes[new_node_ShaderHueSaturation_two.name].inputs['Hue']
    #inn_saturation_value_two = bpy.data.materials[cust_active_mater_cubus_two].node_tree.nodes[new_node_ShaderHueSaturation_two.name].inputs['Value']
    out_saturation_color_two = bpy.data.materials[cust_active_mater_cubus_two].node_tree.nodes[new_node_ShaderHueSaturation_two.name].outputs['Color']
    bpy.data.materials[cust_active_mater_cubus_two].node_tree.links.new(inn_saturation_hue_two, out_two)
    #bpy.data.materials[cust_active_mater_cubus_two].node_tree.links.new(inn_saturation_value_two, out_two)
    bpy.data.materials[cust_active_mater_cubus_two].node_tree.links.new(inn_two, out_saturation_color_two)
    bpy.data.materials[cust_active_mater_cubus_two].node_tree.nodes[new_node_ShaderHueSaturation_two.name].inputs[4].default_value = (0.8, 0.098, 0.12, 1)
    bpy.data.particles[ps_grid_name].lifetime = 25
    bpy.data.particles[ps_grid_name].lifetime_random = 1
    bpy.data.particles[ps_grid_name].frame_end = 250
    #bpy.context.space_data.viewport_shade = 'SOLID'
    bpy.data.particles[ps_grid_name].count = 4000
    
    #bpy.data.objects[obj_n_grid.name].modifiers.new(type = 'SOLIDIFY', name='newww')
    #bpy.context.object.modifiers['newww'].thickness = 0
    
    bpy.data.objects[gridd.name].modifiers.new(type = 'BOOLEAN', name="neww")
    bpy.context.object.modifiers["neww"].operation = 'DIFFERENCE'
    bpy.context.object.modifiers["neww"].object = bpy.data.objects[obj_n.name]
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    
    bpy.context.scene.objects.active = gridd
    
    bpy.context.scene.render.engine = 'BLENDER_RENDER'
    bpy.ops.texture.new()
    bpy.data.textures["Texture"].type = 'VORONOI'
    bpy.ops.anim.keyframe_insert_button(all=True)
    
    #bpy.context.scene.objects.active = cubus
    #bpy.context.object.name = cubus_name
'''
    # Set band count
    band_count = 1
    
    # Setup pitch settings
    min_pitch = 16  # ~20 Hz
    max_pitch = 135 # ~20 kHz
    pitch_step = (max_pitch - min_pitch) / band_count
    pitch = min_pitch
    
    # Set plane start position
    pos = 0 - band_count
    
    # Go to first frame in frame range
    
    bpy.ops.screen.frame_jump(end=False)
    
    # Reset cursor
    bpy.context.area.type = 'VIEW_3D'
    bpy.ops.view3d.snap_cursor_to_center()
    
    # While loop counter != pos
    
    for i in range(0, band_count):
        bpy.context.scene.objects.active = cubus
        bpy.context.object.name = cubus_name
        print(bpy.context.object)
        #print(bpy.context.active_object.location)
        # Set object origin to bottom of plane
        bpy.context.scene.cursor_location = cubus.location
        bpy.context.scene.cursor_location.z -= 1
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        # Set plane scales
        cubus.scale.x = 0.5
        cubus.scale.y = 15
        cubus.scale.z = 0.5
        bpy.ops.object.transform_apply(scale=True)
        
        # Lock X and Z plane scales
        
        #bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        #cubus.animation_data.action.fcurves[0].lock = True
        #cubus.animation_data.action.fcurves[2].lock = True
        
        # Bake filtered audio to cube
        bpy.context.area.type = 'GRAPH_EDITOR'
        
        band_freq = 55 * 2**( (pitch - 33) / 12 )
        band_low_freq = band_freq - 5
        band_high_freq = band_freq + 5
        
        bpy.ops.graph.sound_bake(filepath = "/home/grishaev/Загрузки/90787290326026.mp3", low = band_low_freq, high = band_high_freq)
        # Lock Y plane scale
        bpy.context.active_object.animation_data.action.fcurves[1].lock = True
        
        # Increment counters
        # 
        pitch = pitch + pitch_step
        pos += 2
        
'''
	#bpy.ops.object.speaker_add(view_align=False, enter_editmode=False, location=(-5.28429, -12.6175, -0.530278), \
    #layers=(False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))


    #bpy.ops.object.modifier_add(type="REMESH")



def my_bezier(x,y,z):
	bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align = False, enter_editmode=True, location=(x,y,z)) #создаём кривую
	bpy.ops.transform.translate(value=(1.5, 7, 3), constraint_axis=(True,False,False), constraint_orientation = 'GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff = 'SMOOTH',proportional_size=1)
	bpy.ops.object.convert(target='CURVE', keep_original=False) #конвертируем в объект типа Curve
	#print(bpy.context.object.name)
	obj = bpy.context.object.name #сохраняем название объекта для последующего использования
	return obj
	#obj.data.path_duration = 90 # редактирование количества кадров движения?
	#obj.data.offset = 0.04000000

#создаём кривую	
def add_curve():
	bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align = False, enter_editmode=False, location=(0,-1,-1)) 
	#print(bpy.context.object.name)
	obj = bpy.context.object.name #сохраняем название объекта для последующего использования
	return obj
	#obj.data.path_duration = 90 # редактирование количества кадров движения?
	#obj.data.offset = 0.04000000

#создаём кривую "круг"
def add_circle(r,x,y,z):
	bpy.ops.curve.primitive_nurbs_circle_add(radius=r, view_align=False, enter_editmode=False, location= (x, y, z))
	obj = bpy.context.object.name #сохраняем название объекта для последующего использования
	return obj

#создаём кривую "парабола"
def add_parabola(x,y,z,zz):
	bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align = False, enter_editmode=True, location=(0,0,0))
	obj = bpy.context.object
	loc = bpy.context.scene.cursor_location
	bpy.context.active_object.data.splines[0].points[2].select = True #.select_control_point = True
	bpy.context.active_object.data.splines[0].points[2].co = (x,y,z,zz)
	bpy.ops.object.editmode_toggle()

#создаём кривую "псевдо кубическая парабола"
def add_cubic_parabola(x,y,z,zz, xx, yy, zzz, zzzz):
	bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align = False, enter_editmode=True, location=(0,0,0))
	obj = bpy.context.object
	loc = bpy.context.scene.cursor_location
	bpy.context.active_object.data.splines[0].points[0].select = True #.select_control_point = True
	bpy.context.active_object.data.splines[0].points[0].co = (x,y,z,zz)
	bpy.context.active_object.data.splines[0].points[4].select = True #.select_control_point = True
	bpy.context.active_object.data.splines[0].points[4].co = (xx,yy,zz,zzzz)
	bpy.ops.object.editmode_toggle()

# создаём винтовую кривую
def add_spiral_curve(r, h, k, a):
    theta = 0
    #h = 12      # x coordinate of circle center
    #k = 10      # y coordinate of circle center
    step = 0.67 # amount to add to theta each time (degrees)
    
    bpy.ops.curve.primitive_nurbs_circle_add(radius=a, view_align = True, enter_editmode=True, location=(h,k,0))
    bpy.ops.curve.cyclic_toggle()
    
    bpy.context.active_object.data.splines[0].points[0].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    theta += step
    
    bpy.context.active_object.data.splines[0].points[1].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    theta += step
    
    bpy.context.active_object.data.splines[0].points[2].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    theta += step
    
    bpy.context.active_object.data.splines[0].points[3].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    theta += step
    
    bpy.context.active_object.data.splines[0].points[4].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    theta += step
    
    bpy.context.active_object.data.splines[0].points[5].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    theta += step
    
    bpy.context.active_object.data.splines[0].points[6].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    theta += step
    
    bpy.context.active_object.data.splines[0].points[7].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    theta += step
    
    bpy.context.active_object.data.splines[0].points.add()
    
    bpy.context.active_object.data.splines[0].points[8].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    theta += step
    
    bpy.context.active_object.data.splines[0].points.add()
    
    bpy.context.active_object.data.splines[0].points[9].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    theta += step
    
    bpy.context.active_object.data.splines[0].points.add()
    
    bpy.context.active_object.data.splines[0].points[10].co = (h + r*cos(theta),k + r*sin(theta),a*theta,a)
    
    bpy.ops.object.editmode_toggle()



#создаём ограничитель для объекта "текст"	
def move_by_curve():
	bpy.ops.object.constraint_add(type='FOLLOW_PATH')
	#obb= bpy.ops.object
	#return obb
	
#привязываем ограничитель к тексту и анимируем по умолчанию
def linking(ob):	
	#ob.constraints["Follow Path"].target = bpy.data.objects[obj] # задаем кривую для ограничения # параметризировать bpy.context.scene.objects.keys()
	ob.constraints["Follow Path"].use_curve_follow = True # устанавливаем опцию "следовать за кривой"
	ob.select = True # выбиваем объекст текст
	bpy.context.scene.objects.active = ob # изменяем контекст на "объект - текст"
	bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT') # применяем анимацию по умолчанию
	bpy.ops.window.managers
def anim_move():
    bpy.ops.anim.keyframe_insert_button(all=True)

def join_curve(ob):
	#bpy.context.scene.objects[ob.name].select = True # выбираем кривую для присоединения
	bpy.ops.object.join()
	bpy.ops.object.mode_set(mode='EDIT') 
	bpy.ops.curve.select_all(action = 'TOGGLE')
	l = len(bpy.context.active_object.data.splines[1].points)
	bpy.context.active_object.data.splines[1].points[l-1].select = True # сделать проверку на количество точек редактирования???
	bpy.context.active_object.data.splines[0].points[0].select = True
	bpy.ops.curve.make_segment()
	bpy.ops.object.mode_set(mode='OBJECT')
	#ob.select = True # выбиваем объекст текст
	#bpy.context.scene.objects.active = ob # изменяем контекст на "объект - текст"
	#bpy.ops.window.managers
    
def join():
	bpy.ops.object.join() #

# разбивка текста по частям
def animate_chars():
    frame_num = 5
    for ob in bpy.context.selected_objects:
        location = ob.location[2]
        ob.keyframe_insert(data_path="location", frame=frame_num+10.0, index=2)
        
        ob.location[2] = 1.0
        ob.keyframe_insert(data_path="location", frame=frame_num+20.0, index=2)
        
        ob.location[2] = location
        ob.keyframe_insert(data_path="location", frame=frame_num+30.0, index=2)
        
        frame_num += 5
    bpy.ops.screen.frame_jump()     

# создать материала
def make_material(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat
 
# установить материал
def set_material(ob, mat):
    me = ob.data
    me.materials.append(mat)

# установить модификатор
def set_modifier(ob):
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    ob.modifiers["SimpleDeform"].deform_method = 'BEND'


#bpy.ops.sound.open('INVOKE_DEFAULT')
#--------------------------------------------------#
#---- CLASSES -------------------------------------#
#--------------------------------------------------#

# загрузка библиотек для классов
from bpy_extras.io_utils import ImportHelper                        
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from bpy.types import Menu, Panel

class View3DPanel():
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'


# добавления текста
class AddRusText(bpy.types.Operator):
    """Add Rus Text"""    
    bl_idname = "object.rustext_add"    
    bl_label = "RusText: Add text"
    
    def execute(self, context):
        create_rus_text("Текст")
        return {'FINISHED'}

# открытие файла
class AddRusTextFromFile(Operator, ImportHelper):
    """Add rus text from file"""
    bl_idname = "object.rustext_add_from_file"
    bl_label = "RusText: Import Text From File"

    filename_ext = ".txt"               # необходимо для ImportHelper

    # установка фильтра для файлового диалога
    filter_glob = StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            )
    
    def execute(self, context):
        create_rus_text_from_file(context, self.filepath)
        return {'FINISHED'}


# анимация текста
class AnimateText(Operator):
    """Animate Selected text"""
    bl_idname = "object.rustext_animate"
    bl_label = "RusText: Animate"
    
    bpy.types.Object.sa = bpy.props.FloatProperty(name='Start Animate', default = 20.0)
    bpy.types.Object.sa2 = bpy.props.FloatProperty(name='Second step Animate', default = 40.0)
    bpy.types.Object.sa3 = bpy.props.FloatProperty(name='Third step Animate', default = 60.0)
    bpy.types.Object.sa4 = bpy.props.FloatProperty(name='Four step Animate', default = 80.0)
    bpy.types.Object.sa5 = bpy.props.FloatProperty(name='Five step Animate', default = 100.0)
    
    def execute(self, context):
        ob = bpy.context.object
        if ob.type == 'FONT': 
            animate_text(ob, ob.sa, ob.sa2, ob.sa3, ob.sa4, ob.sa5)
            x = animate_text(ob, ob.sa, ob.sa2, ob.sa3, ob.sa4, ob.sa5)
            return {'FINISHED'}
        elif ob.type == 'MESH': 
            animate_text(ob, ob.sa, ob.sa2, ob.sa3, ob.sa4, ob.sa5)
            x = animate_text(ob, ob.sa, ob.sa2, ob.sa3, ob.sa4, ob.sa5)             
            return {'FINISHED'}
        else:
            self.report({'INFO'}, 'Selected object is not text.')
            return {'CANCELLED'}

# разбивание текста по частям
class AnimateTextChars(Operator):
	"""Animate Selected text chars"""
	bl_idname = "object.rustext_animate_chars"
	bl_label = "RusText: Animate text to chars"
	def execute(self, context):
		ob = bpy.context.object
		
		if ob.type == 'FONT':
			convert_to_mesh()
			separate_text_to_chars()
			animate_chars()
			return {'FINISHED'}
		elif ob.type == 'MESH':
			separate_text_to_chars()
			animate_chars()
			return {'FINISHED'}
		else:
			self.report({'INFO'}, 'Selected object is not text.')
			return {'CANCELLED'}
 

# установка материала
class SetTextMaterial(Operator):
    """Set Text Material"""
    bl_idname = "object.rustext_set_material"
    bl_label = "RusText: Set random material"
    
    def execute(self, context):
        ob = bpy.context.object
        if ob.type == 'FONT': 
            random_material = make_material('MyMaterial', (random(),random(),random()), (0.5,0.5,0), 0.5)
            set_material(ob, random_material)
            return {'FINISHED'}
        elif ob.type == 'MESH': 
            random_material = make_material('MyMaterial', (random(),random(),random()), (0.5,0.5,0), 0.5)
            set_material(ob, random_material)
            return {'FINISHED'}
        else:
            self.report({'INFO'}, 'Selected object is not text!')
            return {'CANCELLED'}

# установка модификатора

class SetTextModifier(Operator):
	"""Set Text Modifier"""
	bl_idname = "object.rustext_set_modifier"
	bl_label = "RusText: Set modifier"
	def execute(self, context):
		ob = bpy.context.object
		if ob.type == 'FONT':
			set_modifier(ob)
			bpy.context.scene.objects.active = ob
			return {'FINISHED'}
		elif ob.type == 'MESH':
			set_modifier(ob)
			bpy.context.scene.objects.active = ob
			return {'FINISHED'}
		else:
			return {'CANCELLED'}
            
# Класс для получения экремпляров объектов "система частиц"

class Partic(Operator):
    """My Partic""" 
    bl_idname = "object.particle_systems"
    bl_label = "Partic"         # Имя для отображения в пользовательском интерфейсе
    #bl_options = {'REGISTER', 'UNDO'} 
    def execute(self, context):        # execute() вызывается, когда Blender вызывает оператор из пунктов меню, кнопок, скриптов
        ob = bpy.context.object  
        if ob.type == 'FONT':
            convert_to_mesh()
            #bpy.ops.object.modifier_add(type='PARTICLE_SYSTEM')
            #convert_to_text()
            particc(ob)
            #bpy.ops.object.mode_set(mode='PARTICLE_EDIT', toggle=True)
            return {'FINISHED'}
        elif ob.type == 'MESH':
            #bpy.ops.object.modifier_add(type='PARTICLE_SYSTEM')
            #convert_to_text()
            particc(ob)
            #bpy.ops.object.mode_set(mode='PARTICLE_EDIT', toggle=True)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

class MoveButton(Operator):
	"""My Move"""
	bl_idname = "object.move_button"
	bl_label = "move button"         # Имя для отображения в пользовательском интерфейсе
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	
    #bl_options = {'REGISTER', 'UNDO'}
	#bl_options = {'REGISTER', 'UNDO'}
	def execute(self, context):   #вызывается, когда Blender вызывает оператор из пунктов меню, кнопок, скриптов
		if bpy.context.object:
		    ob = bpy.context.object
		    #objec = bpy.context.object.name
		    if ob.type == 'FONT':
			    move_by_curve()
			    #obj = add_curve()
			    linking(ob)
			    return {'FINISHED'}
		    elif ob.type == 'MESH':
			    move_by_curve()
			    #obj = add_curve()
			    linking(ob)
			    return {'FINISHED'}
		    else:
			    return {'CANCELLED'}

# класс для создания визуализаций музыки в форме русского текста 
class SoundVisualizator(Operator):
	"""My Visualizator"""
	bl_idname = "object.visualizator_button"
	bl_label = "visualizator button"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	
	def execute(self, context):
		if bpy.context.object:
			partic_to_sound_animation()
			return {'FINISHED'}
		else:
			return {'CANCELLED'}
			 
'''class MyPropPanel(bpy.types.Panel):
    bl_label = "My properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
 
    def draw(self, context):
        ob = context.object
        if not ob:
            return
        layout = self.layout
        layout.prop(ob, 'myRnaInt')
        try:
            ob["MyIdString"]
            layout.prop(ob, '["MyIdString"]')
        except:
            pass
        if ob.type == 'MESH':
            me = ob.data
            layout.prop(me, 'myRnaFloat')
            try:
                me["MyIdBool"]
                layout.prop(me, '["MyIdBool"]')
            except:
                pass
'''

class NurbsPathAdd(Operator):
	"""My Nurbs"""
	bl_idname = "object.nurbs_button"
	bl_label = "add nurbs"
	bl_context = "objectmode"
	bl_options = {'REGISTER', 'UNDO'}
	def execute(self, context):
		add_curve()
		x = bpy.context.object.name
		print(x)
		return {'FINISHED'}	
		
		
class CircleAdd(Operator):
	"""My Circle"""
	bl_idname = "object.circle_button"
	bl_label = "add circle"
	bl_context = "objectmode"
	bl_options = {'REGISTER', 'UNDO'}
	
	r = bpy.props.IntProperty(name="radius", default=2)
	x = bpy.props.IntProperty(name="coordinate x", default=-1)
	y = bpy.props.IntProperty(name="coordinate y", default=2)
	z = bpy.props.IntProperty(name="coordinate z", default=1)
	def execute(self, contex):
		add_circle(self.r, self.x, self.y, self.z)
		return {'FINISHED'}	
		
class ParabolaAdd(Operator):
	"""My Nurbs"""
	bl_idname = "object.parabola_button"
	bl_label = "add parabola"
	bl_context = "objectmode"
	bl_options = {'REGISTER', 'UNDO'}
	
	#r = bpy.props.IntProperty(name="radius", default=1)
	x = bpy.props.IntProperty(name="coordinate x", default=0)
	y = bpy.props.IntProperty(name="coordinate y", default=0)
	z = bpy.props.IntProperty(name="coordinate z", default=2)
	zz= bpy.props.IntProperty(name="coordinate zz", default=2)
	def execute(self, context):
		add_parabola(self.x,self.y,self.z,self.zz)
		x = bpy.context.object.name
		print(x)
		return {'FINISHED'}	


class CubicParabolaAdd(Operator):
	"""My Nurbs"""
	bl_idname = "object.cubic_parabola_button"
	bl_label = "add cubic_parabola"
	bl_context = "objectmode"
	bl_options = {'REGISTER', 'UNDO'}
	
	#r = bpy.props.IntProperty(name="radius", default=1)
	x = bpy.props.IntProperty(name="coordinate x", default=-2)
	y = bpy.props.IntProperty(name="coordinate y", default=-6)
	z = bpy.props.IntProperty(name="coordinate z", default=0)
	zz= bpy.props.IntProperty(name="coordinate zz", default=2)
	xx = bpy.props.IntProperty(name="coordinate x", default=2)
	yy = bpy.props.IntProperty(name="coordinate yy", default=6)
	zzz = bpy.props.IntProperty(name="coordinate zzz", default=0)
	zzzz= bpy.props.IntProperty(name="coordinate zzzz", default=4)
	def execute(self, context):
		add_cubic_parabola(self.x,self.y,self.z,self.zz,self.xx,self.yy,self.zzz,self.zzzz)
		x = bpy.context.object.name
		print(x)
		return {'FINISHED'}
		
class SpiralCurveaAdd(Operator):
	"""My Nurbs"""
	bl_idname = "object.spiral_curve_add"
	bl_label = "add spiral curve"
	bl_context = "objectmode"
	bl_options = {'REGISTER', 'UNDO'}
	
	r = bpy.props.IntProperty(name="radius", default=1)
	h = bpy.props.IntProperty(name="coordinate x", default=0)
	k = bpy.props.IntProperty(name="coordinate y", default=0)
	a = bpy.props.IntProperty(name="value of spiral", default=2)
	
	def execute(self, context):
		add_spiral_curve(self.r,self.h,self.k,self.a)
		return {'FINISHED'}

class MyJoinCurve(Operator):
    """MyJoinCurve"""
    bl_idname = "object.my_join_curve"
    bl_label = "join curves"
    bl_context = "objectmode"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        ob = bpy.context.object
        if ob.type =='CURVE':
            if len(bpy.context.selected_editable_objects) == 2: # проверяем, что действительно выбрано 2 объета
                join_curve(ob)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
			           
class JoinButton(Operator):
	"""My Join"""
	bl_idname = "object.my_join"
	bl_label = "join objects"         # Имя для отображения в пользовательском интерфейсе
	#bl_options = {'REGISTER', 'UNDO'}
	def execute(self, context):        # execute() вызывается, когда Blender вызывает оператор из пунктов меню, кнопок, скриптов
		ob = bpy.context.object
		if ob.type == 'FONT':
			convert_to_mesh()
			#bpy.ops.object.join() #
			return {'FINISHED'}
		else:
			return {'CANCELLED'}

# ----  ПАНЕЛЬ

class RusTextPanel(bpy.types.Panel):
    """A RusText Panel in the Viewport Toolbar"""
    bl_label = "Russian Text Tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_context = 'objectmode'
    
    def draw(self, context): #Функция отображающая содержимое нашего меню
        layout = self.layout #Переменной layout присваивается выражение self.layout
        layout.label(text="Russian Text")	#С помощью label выводится любой текст

        row = layout.row()
        
        #box = layout.template_constraint(con)

        split = layout.split()
        col = split.column(align=True)

        col.operator("object.rustext_add", text="Add text")
        
        layout.separator()
               
        col.operator("object.rustext_add_from_file", text="Import text from file")
        
        layout.separator()
        
        col.operator("object.rustext_animate", text="Animate")
        
        layout.separator()
        
        col.operator("object.rustext_animate_chars", text="Animate text chars")
        
        layout.separator()
        
        col.operator("object.rustext_set_material", text="Set random material")
        
        layout.separator()
        
        col.operator("object.rustext_set_modifier",  text="Set modifier")
        
        layout.separator()
        
        col.operator("object.particle_systems",  text="Particle System", icon='ZOOMIN')
        
        layout.separator()
        
        col.operator("object.move_button", text="move button")
        
        layout.separator()
        
        col.operator("object.visualizator_button", text="visualizator button")
        
        #layout.operator_menu_enum("object.circle_button", "type")
        ob = context.object
        layout.separator()
        
        if bpy.context.object.sa:
            ob = context.object
            row = layout.row()
            row.prop(ob, "sa")

            row = layout.row()
            row.prop(ob, "sa2")

            row = layout.row()
            row.prop(ob, "sa3")
            
            row = layout.row()
            row.prop(ob, "sa4")
            
            row = layout.row()
            row.prop(ob, "sa5")
                    
        if bpy.context.object.constraints.find('Follow Path') == 0:
            ob = context.object
            if ob.type=="FONT":
                row = layout.row()
                ob_follow = ob.constraints["Follow Path"]
                row.column().prop(ob_follow, "target")
                if ob.constraints["Follow Path"].target.type != 'None':
                    row = layout.row()
                    ob_join = ob.constraints['Follow Path'].type
                    row.column().prop(ob_join , 'type')
                    ob = context.object
            elif ob.type=="MESH":
                row = layout.row()
                ob_follow = ob.constraints["Follow Path"]
                row.column().prop(ob_follow, "target")
                #col.prop(bpy.context.scene, 'objects')

            
			
        #if getattr(ob) имеет атрибут тип?далее вложенный иф
        #if ob.type=="CURVE":
            #row = layout.row()
            #row.column().prop(ob, "radius")
            
        #if ob.type=="CURVE":
            #row = layout.row()
            #row.column().prop(ob, "radius")
            
        bpy.context.scene
        layout.separator()
        col.template_ID(context.scene.objects, "active")

# ----  ПАНЕЛЬ для создания кривых по заданным функциям

class CurvePanel(View3DPanel, bpy.types.Panel): #Создается класс с типом меню Panel
    bl_category = "Tools"
    bl_label = "Curve Panel"	       #Название меню
    bl_space_type = 'VIEW_3D'	       #Окно расположения
    bl_region_type = 'TOOL_PROPS'	       #Панель расположения
 
    def draw(self, context):	#Функция отображающая содержимое нашего меню
        layout = self.layout
        #Переменной layout присваивается выражение self.layout
        layout.label(text="Add custom curves object")	#С помощью label выводится любой текст
 
        split = layout.split()
        #Переменной split присваивается выражение layout.split()
        col = split.column(align=True)
        #Переменной col присваивается выражение split.column(align=True)        
    
        layout.separator()
    
        col.operator("object.nurbs_button",  text="add nurbs")
    
        layout.separator()
    
        col.operator("object.circle_button",  text="add circle")
    
        layout.separator()
    
        col.operator("object.parabola_button",  text="add parabola")
    
        layout.separator()
    
        col.operator("object.cubic_parabola_button",  text="almost cubic parabola")
        
        layout.separator()
        
        ob = context.object
        
        col.operator("object.spiral_curve_add",  text="add spiral curve")
        
        layout.separator()
        
        col.operator("object.my_join_curve",  text="join path of animation")
        
        #if ob.type != 'NurbsPath':
			
            #layout.operator_menu_enum("object.my_join_curve_button", "type")
            #row = layout.row()
            #row.column().template_ID(bpy.context.objects, 'active')
            #row.template_ID(bpy.context.scene.objects, "keys()")
			#ob_join = ob.constraints['Follow Path'].type
			#row.column().prop(ob_join , 'type')
			#ob = context.object
        





if __name__ == "__main__":
    register()       
    
#--------------------------------------------------#
#---- INITIALIZE ----------------------------------#
#--------------------------------------------------#



def register():
    bpy.utils.register_class(MyJoinCurve)
    bpy.utils.register_class(SpiralCurveaAdd)
    bpy.utils.register_class(AddRusText)
    bpy.utils.register_class(AddRusTextFromFile)
    bpy.utils.register_class(AnimateText)
    bpy.utils.register_class(AnimateTextChars)
    bpy.utils.register_class(SetTextMaterial)
    bpy.utils.register_class(SetTextModifier)
    bpy.utils.register_class(RusTextPanel)
    bpy.utils.register_class(Partic)
    bpy.utils.register_class(MoveButton)
    bpy.utils.register_class(ParabolaAdd)
    bpy.utils.register_class(CubicParabolaAdd)
    bpy.utils.register_class(JoinButton)
    bpy.utils.register_class(CurvePanel)
    bpy.utils.register_class(NurbsPathAdd)
    bpy.utils.register_class(CircleAdd)
    bpy.utils.register_class(SoundVisualizator)
    
def unregister():
    bpy.utils.unregister_class(MyJoinCurve)
    bpy.utils.unregister_class(SpiralCurveaAdd)
    bpy.utils.unregister_class(AddRusText)
    bpy.utils.unregister_class(AddRusTextFromFile)
    bpy.utils.unregister_class(AnimateText)
    bpy.utils.unregister_class(AnimateTextChars)
    bpy.utils.unregister_class(SetTextMaterial)
    bpy.utils.unregister_class(SetTextModifier)
    bpy.utils.unregister_class(RusTextPanel)
    bpy.utils.unregister_class(Partic)
    bpy.utils.unregister_class(MoveButton)
    bpy.utils.unregister_class(ParabolaAdd)
    bpy.utils.unregister_class(CubicParabolaAdd)
    bpy.utils.unregister_class(JoinButton)
    bpy.utils.unregister_class(CurvePanel)
    bpy.utils.unregister_class(NurbsPathAdd)
    bpy.utils.unregister_class(SoundVisualizator)
    bpy.utils.unregister_class(CircleAdd)

#if __name__ == "__main__":
#    register()
