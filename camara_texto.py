# importar
import bpy

# Insertar camara
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(80, -180, 65), rotation=(0.607374, 5.34132e-09, -0.111701), scale=(1, 1, 1))
# b) rotar
bpy.ops.transform.resize(value=(10, 10, 10))
bpy.ops.transform.rotate(value=-0.70, orient_axis='Z', orient_type='VIEW', orient_matrix=((0.993768, -0.111469, -7.45058e-09), (0.0915326, 0.816032, 0.570713), (0.0636167, 0.567156, -0.82115)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.rotate(value=-50.65435, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.rotate(value=-0.7, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
#Y UN LIGERO AJUSTE MANUAL

# Años (desde 1976 hasta 2022)
año = ''
for i in range(1976,2023):
    año += str(i)+"    "

# Añadir texto visa de años
bpy.ops.object.text_add(enter_editmode=False, align='VIEW', location=(-15, 46, 20), rotation=(45.5,0,0), scale=(10, 10, 10))
bpy.ops.transform.resize(value=(10, 10, 10))
vista = bpy.context.view_layer
vista.objects.active.name = "Years"

# Activar modo edicion
bpy.ops.object.mode_set(mode='EDIT')

# Insertar texto
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.text_insert(text=año)

# Activar modo objeto
bpy.ops.object.mode_set(mode='OBJECT')

# cono
bpy.ops.mesh.primitive_cone_add(enter_editmode=False, align='VIEW', location=(-4, 45, 10), scale=(3, 3, 3))

# Anadir texto de leyenda
bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(-70, -15, 29), rotation=(1.39626, 0, 0), scale=(10, 10, 10))
vista = bpy.context.view_layer
vista.objects.active.name = "Leyenda"

# Insertar texto
# Modo edicion
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')

# Escalas
bpy.ops.font.text_insert(text=">27.5%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="25%-27.5%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="22.5%-25%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="20%-22.5%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="17.5%-20%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="15%-17.5%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="12.5%-15%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="10%-12.5%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="7.5%-10%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="5%-7.5%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="2.5%-5%")
bpy.ops.font.line_break()
bpy.ops.font.text_insert(text="0%-2.5%")

# Modo objeto
bpy.ops.object.mode_set(mode='OBJECT')

# Visualizacion
bpy.ops.transform.resize(value=(1.6, 1.6, 1.6), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

# Deseleción
bpy.ops.object.select_all(action='DESELECT')

# Activar objetos a los que aplica la animacion
objeto = bpy.data.objects['Years']
vista = bpy.context.view_layer
objeto.select_set(True)
vista.objects.active = objeto


#establecer el inicio y final en frames de la animacion
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 644

# insertar frame de inicio y en la posicion inicial del texto

bpy.context.scene.frame_current = 0
bpy.ops.anim.keyframe_insert_menu(type='Location')

# insertar frame final y en la posicion final del texto
bpy.context.scene.frame_current = 644
bpy.ops.transform.translate(value=(-1430.6, 0, 0))

# keyframes
bpy.ops.anim.keyframe_insert_menu(type='Location')

# modo objeto
if bpy.ops.mesh.subdivide.poll():
    bpy.ops.object.mode_set(mode='OBJECT')
    
# Save objects  
for objeto in bpy.data.objects:
    objeto.hide_viewport = False
    objeto.hide_render = False
bpy.ops.object.select_all(action='SELECT')
bpy.context.area.ui_type = 'FCURVES'
bpy.ops.graph.interpolation_type(type='LINEAR')
bpy.context.area.ui_type = 'TEXT_EDITOR'

# Deselecion
bpy.ops.object.select_all(action='DESELECT')