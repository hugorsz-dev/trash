# Este script:
# 1 Iterará (walk) por todos los directorios que contengan un .yaml
# 2 Contemplará 
    # - cada una de sus descripciones, tanto de resumen, de request, y su descripción introductoria
    # - cada enlace
# 3 Clasificará su contenido en base al número de palabras de su descripción, y la validez de los urls respectivamente. 
# 4 Exportará ficheros CSV para su visualización. 

#########
# Variables configurables
##########
# Localización (relativa o absoluta) del directorio a inspeccionar
path="content/api/"
# Host de hugo
host ="http://localhost:1313"

###########################

import subprocess
import os
import csv
import yaml
import json
import os
import re
from urllib.parse import urlparse


"""
Cuenta las palabras de las que está compuesto un string
"""

def count_words(text):
    try:
        n_words = text.split()
        return len(n_words)
    except:
        return 0

"""
Comprueba si una página web está en línea
ATENCIÓN: usa el comando ping de LINUX, no prevee las respuestas para el comando de la consola de Windows
"""

def is_web_online (url): 

    parser = urlparse(url)
    url = parser.netloc.replace('www.', '')

    result = subprocess.run(["ping", "-c", "1", url], capture_output=True, text=True)
    if "PING" in result.stdout:
        return True
    return False 

"""
def join_url (original_url, url_to_convert):
    previus_folders = url_to_convert.count ("../")

    if previus_folders:

        if ("." in original_url.split("/")[-1] ):
            original_url = original_url.split("/")[:-1]
            original_url = ("/".join(original_url))

        origin_path= (original_url.split("/")[:(previus_folders)])
        origin_path = ("/".join(origin_path))
        url_to_convert = url_to_convert.replace ("../","")
        print (url_to_convert)
        output = origin_path + "/" + url_to_convert
        return output
"""

"""
Elimina los saltos (../) de una URL, por ejemplo:
    original_url: hugo/documents/articles/file.txt
    url_to_convert: ../../downloads/game.rar
    return: hugo/downloads/game.rar 
"""
  
def join_url (original_url, url_to_convert):
    combined_path = os.path.join(os.path.dirname(original_url), url_to_convert) # Une las dos rutas
    return os.path.normpath(combined_path) # "Normaliza" la ruta resultante, quitando toda la basura de por medio

"""
Itera en todos los archivos de un directorio y compara su nombre.extension con la introducida por parámetro
"""

def search_file (searched_file,dir):
    for root, dirs, files in os.walk(dir):
        for file in files: 
            if file == searched_file:
                return True
    return False

# Output 

definition_output=[]
responses_output=[]
repetitive_definition_output = []
bad_urls_output = []
info_output = []

recurring_phrases = ["above", "must replace", "using curl", "can request", "correctly formatted"]

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
                        definition_output.append ({
                            "words": count_words(subvalue["description"]),
                            "request": subkey,
                            "tag": subvalue["tags"][0],
                            "url":url,
                            "file_path": file_path,
                            "content": subvalue["description"],
                            "yaml_path": yaml_path 
                        })

                        # Comprobación de frases recurrentes
                        try:
                            if any (phrase in subvalue["description"] for phrase in recurring_phrases):
                                repetitive_definition_output.append ({
                                    "words": count_words(subvalue["description"]),
                                    "request": subkey,
                                    "tag": subvalue["tags"][0],
                                   "url":url,
                                    "file_path": file_path,
                                    "content": subvalue["description"],
                                    "yaml_path": yaml_path 
                                })
                        except:
                            pass
                        
                    # ... y las descripciones de sus respuestas en otro fichero, si las tiene.
                    if "responses" in subvalue:
                        for response, description in subvalue["responses"].items():
                            responses_output.append ({
                                "words": count_words(description["description"]),
                                "request": subkey,
                                "url":url,
                                "file_path": file_path,
                                "content": description["description"],
                                "response":response,
                                "yaml_path": yaml_path,                    
                            })          
                        
                yaml_path="pahts"

            # Detección de enlaces incorrectos.
            # -  Habría que refactorizar el condicional. 

            # Array de URLS que hay por cada file
            file_urls = re.findall(r'\[.*?\]\((.*?)\)',str(yaml_data) )
            
            # Si hay URLS...
            if file_urls:
                for file_url in file_urls:
                    # Comprobar que, si el enlace redirige a internet, la página adjunta está en línea
                    if "://" in file_url:
                        if not is_web_online (file_url):
                            bad_urls_output.append ({"url":url,"file_path": file_path,"file_url":file_url})   
                    # Si el enlace es relativo....
                    elif ".." in file_url:
                        # ... si contiene la referencia a un encabezado ... 
                        if "#" in file_url:
                            # ... unir URL 
                            joined_url = join_url (file.name, os.path.dirname(file_url) )+".md"
                            if ( not os.path.exists (joined_url)): 
                                if "_index.md" not in joined_url: 
                                    if (not search_file(os.path.basename(joined_url), ".")):
                                        bad_urls_output.append ({"url":url,"file_path": file_path,"file_url":file_url})
                                else:
                                    bad_urls_output.append ({"url":url,"file_path": file_path,"file_url":file_url})
                        elif (not search_file(os.path.basename(file_url), ".")): 
                            joined_url = join_url (file.name, file_url)
                            if joined_url[-1]=="/": joined_url= joined_url[:-1]
                            joined_url = joined_url + "/_index.md"
                            if (not os.path.exists(joined_url)):
                                bad_urls_output.append ({"url":url,"file_path": file_path,"file_url":file_url})
                                print (file.name, file_url)
                                joined_url = join_url (file.name, file_url)
                                print (joined_url)
                    else:
                        if "#" in file_url:    
                            joined_url = join_url (file.name, os.path.dirname(file_url) )+".md"
                            if ( not os.path.exists (file_url)): 
                                if "_index.md" not in joined_url: 
                                    if (not search_file(os.path.basename(joined_url), ".")):
                                        bad_urls_output.append ({"url":url,"file_path": file_path,"file_url":file_url})
                                else:
                                    bad_urls_output.append ({"url":url,"file_path": file_path,"file_url":file_url})
                        elif (not search_file(os.path.basename(file_url), ".")):
                            joined_url = os.path.dirname(file.name)+"/"+file_url
                            if joined_url[-1]=="/": joined_url= joined_url[:-1]
                            joined_url = joined_url + "/_index.md"
                            if (not os.path.exists(joined_url)):
                                bad_urls_output.append ({"url":url,"file_path": file_path,"file_url":file_url})
                            

            # Descripciones que encabezan los documentos .yaml
            if "info" in yaml_data:
                if "description" in yaml_data["info"]:
                    info_output.append ({
                        "words":count_words(yaml_data["info"]["description"]),
                        "path": file_path,
                        "url":url,
                        "content": yaml_data["info"]["description"]
                    })
               

# Ordenación de los campos - la función sorted es iterable, por lo que la key variará

responses_output = sorted (responses_output, key= lambda dictionary: dictionary["words"], reverse=True)
definition_output = sorted (definition_output , key= lambda dictionary: dictionary["words"], reverse=True)
repetitive_definition_output = sorted (definition_output , key= lambda dictionary: dictionary["words"], reverse=True)
info_output = sorted (info_output , key= lambda dictionary: dictionary["words"], reverse=True)


field_names = ["words", "request", "url", "file_path", "content", "response", "yaml_path"]

with open('responses.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(responses_output)

field_names = ["words", "request", "tag", "url", "file_path", "content", "yaml_path"]

with open('definitions.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(definition_output)

with open('repetitive_definition_output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(repetitive_definition_output)

field_names = ["url", "file_path", "file_url"]

with open('bad_urls.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(bad_urls_output)

field_names = ["words","path", "url", "content"]

with open('info_output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(info_output)




