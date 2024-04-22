# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 16:07:15 2023

@author: Santiago 
"""

import pandas as pd
import os
import numpy as np

def read_clean_dataset(directory):
    
    path_files = []
    
    for root, dirs, files in os.walk(directory):
               
        for name_file in files:
            if name_file.endswith('.csv'):
                path_files.append(os.path.join(root, name_file))
    # print(path_files)
    print('numero de archivos: ',len(path_files))
    
    lst_dfs = []
    
    for df in path_files:
        # print(df)
        df = pd.read_csv(df,header=0,encoding='latin1', sep='\t')
        
        column_names = df.columns
        # print(column_names)
        df['Total'] = pd.to_numeric(df['Total'].str.replace(',','.'), errors='coerce')
        
        if 'Comunidad autónoma' in column_names:
            index_drop_row = df[df['Comunidad autónoma']=='Total'].index
        
            df.drop(index_drop_row, inplace=True)
            df=df[['Comunidad autónoma', 'Periodo', 'Total']]
            #si es necesario, reemplazar los nombres para que coincidan
            df.loc[df['Comunidad autónoma'] == 'Asturias (Principado de)','Comunidad autónoma']='Asturias, Principado de'
            df.loc[df['Comunidad autónoma'] == 'Balears (Illes)','Comunidad autónoma']='Balears, Illes'
            df.loc[df['Comunidad autónoma'] == 'Comunidad Valenciana','Comunidad autónoma']='Comunitat Valenciana'
            df.loc[df['Comunidad autónoma'] == 'Madrid (Comunidad de)','Comunidad autónoma']='Madrid, Comunidad de'
            df.loc[df['Comunidad autónoma'] == 'Murcia (Región de)','Comunidad autónoma']='Murcia, Región de'
            df.loc[df['Comunidad autónoma'] == 'Navarra (Comunidad Foral de)','Comunidad autónoma']='Navarra, Comunidad Foral de'
            
            lst_dfs.append(df)
        else:
            df=df[['Comunidades y Ciudades Autónomas', 'Periodo', 'Total']]
            df.rename(columns={"Comunidades y Ciudades Autónomas": "Comunidad autónoma"}, inplace=True)
            
            # print(df.head(21))
            lst_dfs.append(df)
          
    
    df_concat = pd.concat(lst_dfs)   
    
    #remueve ultimos caracteres de cada periodo para solo dejar el año T seguido por cualquier caracter
    df_concat['Periodo'] = df_concat["Periodo"].str.replace('(T.*)', '', regex =  True)
    #añade "A" al inicio de cada año
    df_concat['Periodo'] = "A" + df_concat['Periodo']
    
    #ya no es neesario
    # df_concat['codigo'] = df_concat["Comunidad autónoma"].str.extract('(\d{2})')
    df_concat['Comunidad autónoma'] = df_concat["Comunidad autónoma"].str.replace('(\d{2} )', '', regex =  True)
    # print(df_concat)
    
    #ya no es neesario
    #dataframe solo con los codigos y las comunidades para hacer un mapeo posterior
    #selecciona solo las filas no nulas y luego selecciona la primera y cuarta columna
    # df_codigo = df_concat[df_concat['codigo'].notnull()].iloc[:,[0,3]] 
    #bota duplicados, establece index basado en una columna y saca a diccionario {index: value}
    #pandas devuelve una lista para los valores, es necesario devolver solo el valor del codigo
    #fuera de la lista
    # dict_cod= df_codigo.drop_duplicates(subset='Comunidad autónoma').set_index('Comunidad autónoma').T.to_dict('list')
    # for k, v in dict_cod.items():
    #     dict_cod[k] = v[0]    
    # #print(dict_cod)
     
    #pivot para que por comunidad las columnas sean los años y sus valores sean la tasa de paro
    df_concat = pd.pivot_table(df_concat, values='Total', index='Comunidad autónoma', columns='Periodo', aggfunc=np.sum, margins=True)
    # print(df_concat)
    
    # mapeo de los codigos
    dict_cod= {'Andalucía':'61', 'Aragón':'62','Asturias, Principado de':'63','Balears, Illes':'64','Cantabria':'66',
               'Castilla - La Mancha':'68','Castilla y León':'67','Cataluña':'69','Ceuta':'78','Ceuta y Melilla':'78','Comunitat Valenciana':'77',
               'Extremadura':'70','Galicia':'71','Madrid, Comunidad de':'72','Melilla':'78','Murcia, Región de':'73','Navarra, Comunidad Foral de':'74',
               'País Vasco':'75','Rioja, La':'76'}
    
    #sumar ceuta y melilla y rebautizar a ceuta y melilla
    
    df_concat['codigo'] = df_concat.index.map(dict_cod) 
       
    df_concat = df_concat.groupby(['codigo']).sum()
    
    #para insertar de nuevo los nombres de las comunidades despues de group by que bota esa columna
    #a menos de que quede un subindice por simplicidad agrupar y mapear un dic inverso
    reversed_dict = {}  
    for k, v in dict_cod.items():
        reversed_dict[v] = k
    #mapeado
    df_concat['comunidad autonoma'] = df_concat.index.map(reversed_dict)
    #reemplazar el nombre de la comunidad
    df_concat.loc[df_concat['comunidad autonoma'] == 'Melilla', 'comunidad autonoma']='Ceuta y Melilla'
    
        
    return df_concat, dict_cod


df_total, prov_cod = read_clean_dataset(r'E:\C\Master_geomatica\geovisualizacion_3D\unidad1\Unidad 3\datos')

print(df_total.shape)
print(df_total.head(21))


df_total.to_csv(r'E:\C\Master_geomatica\geovisualizacion_3D\unidad1\Unidad 3\datos\comunidad_periodo.csv')







