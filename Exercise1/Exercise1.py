# Para poder usar la función print e imprimir sin saltos de línea
from __future__ import print_function

import datetime
import json # Para poder trabajar con objetos JSON
import pprint # Para poder hacer uso de PrettyPrinter
import sys # Para poder usar exit

from elasticsearch import Elasticsearch
from elasticsearch import helpers

def main():
    # Queremos imprimir bonito
    pp = pprint.PrettyPrinter(indent=2)

    # Nos conectamos por defecto a localhost:9200
    es = Elasticsearch(['http://elastic.carlosmanrique.dev:9200'])
    # En ocasiones las consultas tienen que formalizarse en JSON
    results = es.search(
        index="reddit-mentalhealth-stopwords",
        body = {
            "query": {
                "match": {
                    "selftext": {
                        "query": "rehab rehabilitation",
                        "operator": "or"
                    }
                }
            },
            "aggs":{
                "Terminos mas significativos":{
                    "significant_terms":{
                        "field":"selftext",
                        "size":100,
                        "chi_square":{

                        },


                    }
                }

            }
        }
        )

    # pp.pprint(results)
    print(str(results["hits"]["total"]) + " resultados para una query \"rehab\"")

    significantWords =[]
    words = ""
    # Iteramos sobre los resultados, no es preciso preocuparse de las
    # conexiones consecutivas que hay que hacer con el servidor ES
    for hit in results["aggregations"]["Terminos mas significativos"]["buckets"]:
        # get created date for a repo and fallback to authored_date for a commit
        print(str(hit["key"]))
        significantWords.append(hit["key"])
        words+=" "+str(hit["key"])



    secondQuery = {
         "query":{
             "match":
                 {
                     "selftext": {
                         "query": words ,
                         "operator": "or"
                     }

                 }
         }
     }

    posts = helpers.scan(es,index="reddit-mentalhealth",query=secondQuery)

    f = open("relatedPostsChi.txt", "wb")
    # Iteramos sobre los resultados, no es preciso preocuparse de las
    # conexiones consecutivas que hay que hacer con el servidor ES
    for hit in posts:
        f.write('Author:'.encode("UTF-8"))
        f.write(hit["_source"]["author"].encode("UTF-8"))
        f.write('\n'.encode("UTF-8"))
        postdate = datetime.datetime.utcfromtimestamp(hit["_source"]["created_utc"] )
        f.write('Date:'.encode("UTF-8"))
        f.write(postdate.strftime("%m/%d/%Y, %H:%M:%S").encode("UTF-8"))
        f.write('\n'.encode("UTF-8"))
        f.write('Post:'.encode("UTF-8"))
        f.write(hit["_source"]["selftext"].encode("UTF-8"))
        f.write('\n'.encode("UTF-8"))

    f.close()

    # Preparar consultas con default_operator y docvalue_fields, por ejemplo
    # para obtener los textos únicamente para hacer data mining...
    #
    # ...

if __name__ == '__main__':
    main()
