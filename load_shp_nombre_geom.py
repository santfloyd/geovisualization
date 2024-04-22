import shapefile
import bpy


if bpy.ops.mesh.subdivide.poll():
    bpy.ops.object.mode_set(mode='OBJECT')
for ob in bpy.data.objects:
    ob.hide_viewport = False
    ob.hide_render = False
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()


escena = bpy.context.scene
vista = bpy.context.view_layer

shp_path = r'E:\C\Master_geomatica\geovisualizacion_3D\unidad1\Unidad 3\practica\shape_join_monopart.shp'

#escala y traslacion
fE = 10
tx = -10
ty = 400

shp_reader = shapefile.Reader(shp_path)

# nombres de los atributos del shape
attribute_names = [field[0] for field in shp_reader.fields[1:-4]] # skip first deletion field and last inecesary ones
print(attribute_names)

# itera los records del shape
for shp_record in shp_reader.iterShapeRecords():
    shp_attributes = shp_record.record
#   print(shp_attributes)

    #crear una lista con los codigos
    attribute_ccaa = shp_attributes['id_ccaa']    
    print(attribute_ccaa)
    
    #points and vertices of each record
    shp_shape = shp_record.shape
    puntos = shp_shape.points
    vertices = []
    for p in puntos:
#  multiplico por el factor de escala y traslacion en x e y (de lo contrario no se ve por lo pequeño)
        vertices.append([p[0]*fE-tx,p[1]*fE-ty,0])
#    print(vertices)
    # Iterate over the attribute names to match
    for attribute_name in attribute_names:
       print(attribute_name)
#       acceder a los campos para verificar la posicion del primer año y del ultimo
#       en mi caso van de la posicion 2 a la -2 (1976-2022)
#       la posicion 1 en mi shape es el codigo de la comunidad
       print(shp_reader.fields[2:-2]) #devuelve field name, field type, field length, decimal length 
#       for field in shp_reader.fields[2:-2]:
##            print(field)
#           if attribute_name in field:
##              print(True)  
#               attribute_paro = shp_attributes[attribute_name]
##              nombre de la 
#               nombre = "{year}_{codigo}_{paro}".format(year=attribute_name,codigo=attribute_ccaa,paro=attribute_paro)
##               print(nombre)
##              crear una malla nueva por cada nombre
#               malla = bpy.data.meshes.new(name='geom')
#               ob = bpy.data.objects.new(nombre,malla)
#               escena.collection.objects.link(ob)
#               #numero de caras
#               lista = range(0, len(puntos))
#               caras = [tuple(lista)]        
#               #poblar la malla con los datos
#               malla.from_pydata(vertices,[],caras) #vertices, edges y caras
#               ob.select_set(True)
#               vista.objects.active=ob


#presionar la tecla "/" en el teclado numerico para hacer zoom