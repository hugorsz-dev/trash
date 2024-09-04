# Este script:
# 1 Iterará (walk) por todos los directorios que contengan un .yaml
# 2 Contemplará cada una de sus descripciones, tanto de resumen como por cada request. 
# 3 Clasificará su contenido en base al número de palabras de su descripción
# 4 Exportará dos ficheros JSON correspondientes a ambos apartados

#########
# Variables configurables
##########
# Localización (relativa o absoluta) del directorio a inspeccionar
path="content/api/"
# Host de hugo
host ="http://localhost:1313"
# Rango de búsqueda (de 10 en 10, de 20 en 20...)
range=10
#########

import yaml
import jsonz
import os

# Output
definition_output={}
responses_output={}

"""
Devuelve la aproximación por truncación de un número entero,  a partir del rango indicado
P.ej: si el rango es "20"
Al introducir 14 la salida será 20.
Al introducir 22 la salida será 40.  
"""

def round_int(number):
    return (number // 10) * range

"""
Devuelve el número de palabras de un string
"""

def count_words(text):
    n_words = text.split()
    return len(n_words)

"""
Añade un json al output, siendo el atributo que almacena cada uno de los registros el número
de palabras previamente truncado con round_int()
"""

def add_yaml_to_output (input, output):
    try:
        output[str(round_int(input["words"]))].append (input)
    except:
        output[str(round_int(input["words"]))] = []
        output[str(round_int(input["words"]))].append (input)

# Recorre el directorio indicado...

for root, dirs, files in os.walk(path):
    for file in files: 
        file_extension= file.split(".")[-1]
        file_name= file.split(".")[0]
        file_path = os.path.join(root, file)
        url = file_path.replace("content", host)
        url = url[:url.rfind("/")]

        # ... deteniéndose únicamente en los ficheros .yaml...
        if file_extension == "yaml":
            with open(file_path, 'r') as file:
                yaml_data = yaml.safe_load(file)

            # ... a medida que el fichero va recorriéndose, el path del yaml también...
            yaml_path="pahts"

            # ... se recorre el atributo paths del yaml... 
            for key, value in yaml_data["paths"].items():
                yaml_path = yaml_path + key
                for subkey, subvalue in value.items():

                    #... introduciendo su descripción si la tiene
                    if "description" in subvalue:
                        add_yaml_to_output ({
                            "url":url,
                            "file_path": file_path,
                            "yaml_path": yaml_path, 
                            "request": subkey,
                            "words": count_words(subvalue["description"]),
                            "content": subvalue["description"]
                        }, definition_output)
                    
                    # ... y las descripciones de sus respuestas en otro fichero, si las tiene.
                    if "responses" in subvalue:
                        for response, description in subvalue["responses"].items():
                            add_yaml_to_output ({
                                "url":url,
                                "file_path": file_path,
                                "yaml_path": yaml_path, 
                                "request": subkey,
                                "response":response,
                                "words": count_words(description["description"]),
                                "content": description["description"]
                            }, responses_output)

                yaml_path="pahts"            

# En cada ejecución se exportan los JSON
with open('definition_responses.json', 'w') as file_json:
    json.dump(responses_output, file_json, indent=4)
with open('definitions.json', 'w') as file_json:
    json.dump(definition_output, file_json, indent=4)

print ("- definitions.json - creado fichero")
print ("- definition_responses.json - creado fichero")

