import bpy

# Función con los colores RGBA en rangos
def color(num):
    
    colors = (
        (0.0, 1.0, 0.0, 1.0), # green
        (0.5, 1.0, 0.0, 1.0),
        (1.0, 1.0, 0.0, 1.0),#yellow
        (1.0, 0.8, 0.0, 1.0), 
        (1.0, 0.6, 0.0, 1.0), # Orange
        (1.0, 0.4, 0.0, 1.0),
        (1.0, 0.2, 0.0, 1.0), #Light Red
        (1.0, 0.0, 0.0, 1.0), #Red
        (0.8, 0.0, 0.2, 1.0),
        (0.6, 0.0, 0.4, 1.0), #Dark Red
        (0.4, 0.0, 0.6, 1.0),
        (0.2, 0.0, 0.8, 1.0) #Deep Red
    )
    
    col = [] 
    if num >= 0 and num <= 1:
        col.append(colors[0])
    elif num > 1 and num <= 2:
        col.append(colors[1])
    elif num > 2 and num <= 3:
        col.append(colors[2])
    elif num > 3 and num <= 5:
        col.append(colors[3])
    elif num > 5 and num <= 10:
        col.append(colors[4])
    elif num > 10 and num <= 20:
        col.append(colors[5])
    elif num > 20 and num <= 40:
        col.append(colors[6])
    elif num > 40 and num <= 80:
        col.append(colors[7])
    elif num > 80 and num <= 160:
        col.append(colors[8])
    elif num > 160 and num <= 320:
        col.append(colors[9])
    elif num > 160 and num <= 400:
        col.append(colors[10])
    elif num > 400:
        col.append(colors[11])
        
    return col[0]

def intervals(x):
    if x == 0:
        return 0
    elif 0 < x <= 4:
        return 2**(x-1)
    elif 4 < x <= 6:
        return 5*2**(x-5)
    elif 6 < x <= 8:
        return 10*2**(x-7)
    elif 8 < x <= 10:
        return 20*2**(x-9)
    elif x == 11:
        return 400


# cubes scales
for i in range(0, 12):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(-80, -20, 10+i), scale=(10-i*0.5, 10-i*0.5, i*1.5))
    ob = bpy.data.objects['Cube']
    # name
    ob.name = "Escala_"+str(i)
    # color
    color_mat = color(intervals(i))
    # material
    material = bpy.data.materials.new(ob.name)
    # nodos
    material.use_nodes = True
    nodos = material.node_tree.nodes
    nodo_BSDF = nodos['Principled BSDF']
    nodo_BSDF.inputs[0].default_value = color_mat
    ob.data.materials.append(material)
        # update
    ob.data.update()
        # deselecion
    bpy.ops.object.select_all(action='DESELECT')
        
    
list_escala = []
for i in range(len(bpy.data.objects)-6,len(bpy.data.objects)):
    ob = bpy.data.objects[i]
    # lista nombres
    if "Escala_" in ob.name:
        print(ob.name)
        # Añadir nombres
        list_escala.append(ob)
        ob.select_set(True)
        
ultimo = list_escala[-1]
vista = bpy.context.view_layer
vista.objects.active = ultimo
# join escalas
bpy.ops.object.join()

ultimo.name = "Escala"
# deselecion
bpy.ops.object.select_all(action='DESELECT')

