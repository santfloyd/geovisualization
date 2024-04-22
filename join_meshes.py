import bpy
import re

#patron para agrupar ppr año 
pattern = r"A(\d{4})_"      

#creacion de listas de codigos de provincia a partir de las mallas existentes en la escena
codes = []
for obj in bpy.context.scene.objects:
    code = re.findall(pattern, obj.name)        
    if obj.type == "MESH" and code not in codes:
        codes.append(code)

#re.findall devuelve una lista, es necesario convertir la lista de listas en lista de strings
codes=[' '.join(code) for code in codes]
print(codes)

#creacion de listas de objetos por codigo de provincia presente en el nombre de cada objeto
meshes_to_join = []
for code in codes:
    mesh_by_code = []
    for obj in bpy.context.scene.objects:
        
        if obj.type == "MESH" and f"A{code}_" in obj.name:
            mesh_by_code.append(obj)
    print('numero de mallas por codigo', code, ': ', len(mesh_by_code))
    meshes_to_join.append(mesh_by_code)
    
print(len(meshes_to_join))
print(meshes_to_join)
    

#merge de las mallas 
for submeshes in meshes_to_join:
    #se vuelve a extraer el codigo del nombre de la primera malla de cada sublista para mas adelante 
    #componer el nombre de la malla fucionada
    code = re.findall(pattern, submeshes[0].name)        
    code_ = code[0]
    print("año: ",code_)

    location = submeshes[0].location
    # select each mesh and join it to the new object
    for mesh in submeshes:
        mesh.hide_viewport = False    
        mesh.select_set(True)
        bpy.context.view_layer.objects.active = mesh
        print("capa a unir: ",mesh.name)
        bpy.ops.object.join()
    

    # create a new object from the active object after joining
    joined_mesh = bpy.context.view_layer.objects.active
    joined_mesh.name = f"A{code_}_joined"
    print(joined_mesh.name)    
    
    # set the location of the joined mesh to the first mesh in the list
    joined_mesh.location = location
    
    # deselect all objects and select the joined mesh
    bpy.ops.object.select_all(action='DESELECT')
    joined_mesh.select_set(True)
    
    # set the active object to the joined mesh and apply any transformations
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = joined_mesh
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)