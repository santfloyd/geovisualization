import bpy
import re
import bmesh
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
meshes_to_merge = []
for code in codes:
    mesh_by_code = []
    for obj in bpy.context.scene.objects:
        
        if obj.type == "MESH" and f"A{code}_" in obj.name:
            mesh_by_code.append(obj)
    print('numero de mallas por codigo', code, ': ', len(mesh_by_code))
    meshes_to_merge.append(mesh_by_code)
    
print(len(meshes_to_merge))
print(meshes_to_merge)

#merge de las mallas 
for submeshes in meshes_to_merge:
    #se vuelve a extraer el codigo del nombre de la primera malla de cada sublista para mas adelante 
    #componer el nombre de la malla fucionada
    code = re.findall(pattern, submeshes[0].name)        
    code_ = code[0]
    print(code_)

    # crea un nuevo objeto mesh
    bm = bmesh.new()

    # itera en cada sublista para añadir cada malla al objeto bmesh 
    for mesh in submeshes:
        bm.from_mesh(mesh.data)

    # Merge the bmesh
    #remove_doubles remueve vertices duplicados que hubieran podido ser creados durante el proceso
    #dist especifica la distancia maxima en la que se considera un vertice duplicado
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

    # crea una nueva malla a partir del objeto bmesh merged
    merged_mesh = bpy.data.meshes.new(name=f'A{code_}')
    bm.to_mesh(merged_mesh)
    bm.free()

    # Create a new object from the merged mesh and link it to the scene
    merged_obj = bpy.data.objects.new(f'A{code_}', merged_mesh)
    bpy.context.collection.objects.link(merged_obj)
