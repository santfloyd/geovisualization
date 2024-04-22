import shapefile
import bpy

# Tiempo: Inicio - Fin
bpy.context.scene.frame_current = 0
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 644

# Tiempo: Inicio - Fin
t = int(645//45)

#Hacer todo no visible excepto los elementos adicionales del mapa y la primer capa 
for ob in bpy.data.objects:
    if ob.name != "A1976_joined" and ob.name != "Escala_11" and ob.name != "Cone" and ob.name != "Leyenda" and ob.name != "Years" and ob.name != "Camera":
        ob.hide_viewport = True
        ob.hide_render = True
        
#añadir keyframes tomando en cuenta la cantidad de objetos a mostrar
#en la linea de tiempo        
for i in range(0,len(bpy.data.objects)-1):

    ob = bpy.data.objects[i]

    ob1 = bpy.data.objects[i+1]

    # keyframes
    ob.keyframe_insert(data_path="hide_viewport",frame=i*t)
    ob.keyframe_insert(data_path="hide_render",frame=i*t)
    ob1.keyframe_insert(data_path="hide_viewport",frame=i*t)
    ob1.keyframe_insert(data_path="hide_render",frame=i*t)
    # accion
    ob.hide_viewport = True
    ob.hide_render = True
    ob1.hide_viewport = False
    ob1.hide_render = False
