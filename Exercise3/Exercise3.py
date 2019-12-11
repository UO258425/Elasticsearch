# Para poder usar la función print e imprimir sin saltos de línea
from __future__ import print_function

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
        index="reddit-mentalhealth",
        body = {
            "query": {
                "match": {
                    "selftext": {
                        "query": "xanax SSRI SNRI paroxetine fluoxetine  antidepress* prescr* ",
                        "operator": "or"
                    }
                }
            },
            "aggs":{
                "Terminos mas significativos":{
                    "significant_terms":{
                        "field":"selftext",
                        "size":100,
                        "gnd":{

                        },



                    }
                }

            }
        }
        )

    # pp.pprint(results)
    print(str(results["hits"]["total"]) + " resultados para una query \"rehab\"")

    medications =[]

    # Iteramos sobre los resultados, no es preciso preocuparse de las
    # conexiones consecutivas que hay que hacer con el servidor ES
    for hit in results["aggregations"]["Terminos mas significativos"]["buckets"]:
        # get created date for a repo and fallback to authored_date for a commit
        print(str(hit["key"]))
        query = "https: // www.wikidata.org /w/api.php?action=wbsearchentities&search="+ hit["key"] +"&language=en"
        medications.append(hit["key"])





if __name__ == '__main__':
    main()
