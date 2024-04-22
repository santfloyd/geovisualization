import shapefile
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


#es muy importante hacer un deselect para que el procesamiento sea rápido
bpy.ops.object.select_all(action='DESELECT')
# Extruir objetos
#procesar por chunks para evitar overhead de la memoria de la maquina
# lista de todos los objetos de la escena
objects = bpy.data.objects
#extencion de la lista
num_objects = len(objects)
#extension del chunk deseado
chunk_size = 10

#iterar con la funcion range para eficiencia en memoria
for i in range(0, num_objects, chunk_size): #start, stop, step
    #slice de la lista desde el primer y ultimo indice por cada step
    #por slice, cada objeto ej: de 100 cada 10: 0-10, 10-20 etc
    for obj in objects[i:i+chunk_size]:
#        print("chunk start",i)
        obj.select_set(True)
        # extraccion del dato a partir del nombre de la capa
        if "_" in obj.name and obj.name.split("_")[2] != "None":
            print(obj.name)
            part = float(obj.name.split("_")[2])
            if part > 0:
                part = part/25
            else: 
                part = 0
            print(part)
            
        else:
            print("no cumple la condicion:" ,obj.name)
            part = 0
            
        bpy.context.view_layer.objects.active = obj
        # modo edicion        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0,0,part)})

        #asigna un material a la extrusion
        obj.data.materials.clear()
        color_mat = color(part*30)
        print(color_mat)
        if color_mat is not None:    
            material = bpy.data.materials.new(obj.name)
            obj.data.materials.append(material)        
            material.use_nodes = True
            # nodos
            nodetree = material.node_tree
            nodes = nodetree.nodes
            links = nodetree.links
            
            #remover el nodo por defecto 
            if nodes.get('Diffuse BSDF') is not None:
                nodes.remove(nodes.get('Diffuse BSDF'))
            
            #create 'Principled BSDF'
            principle_node = nodes.new('ShaderNodeBsdfPrincipled')
            principle_node.location = (0, 0)
            
            #Set the color of the Principled BSDF node based on the color gradient function
            principle_node.inputs[0].default_value = color_mat



            # Link the Principled BSDF node to the Material Output node
            output_node = nodes.get('Material Output')
            links.new(principle_node.outputs[0], output_node.inputs[0])
                
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.hide_viewport = True
        obj.data.update()
        





        
    
    