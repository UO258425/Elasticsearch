# Para poder usar la función print e imprimir sin saltos de línea
from __future__ import print_function

import json # Para poder trabajar con objetos JSON
import pprint # Para poder hacer uso de PrettyPrinter
import sys # Para poder usar exit

from elasticsearch import Elasticsearch
import requests
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
                        "query": " \"prescribed me\" prescr* antidepressant*",
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

                        "exclude":["prescribes", "prescribed", "prescribe","prescription","prescribing","prescriber", "medicine",
                                   "meds", "drugs", "dose", "doctor", "pharmacy" , "diagnosed" ,"diagnostic",
                                   "medications","medication","dose","dosage","pill","pills","psychiatrist","mg","tak*","effect","effects","symptoms","gp"
                                   ,"antidepressants","drugs","lower","treatment","pharmacist","drug","doctors","height","infection","duration","lbs"
                            ,"prescriptions","oral","nausea","fever","blood","intolerance","intolerances","appointment","appointments",
                                   "addicted","addictive","addiction","tested","doses","adhd","doc","referred","allergy","allergic","tests"
                            ,"specialist","reuptake","inflammation","grossly","recreational","recreationally","advised","advises","switched","experience",
                                   "experienced","experiencing","side","effects","pain","pains","taking","took","taken","addictiveness","antidepressant"
                                   ,"podiatrist","complaint","medical","emergency","urgent","attacks","smoker","result","results","recommended","recomendation",
                                   "consultation","physician","physchaitrist","capsules","tablets","nuerologist","ssri","stimulant","stimulants","adverse","test"
                                   ,"deficiency","decrease","decreased","caucasian","x","testing","fatigue","symptoms","dermatologist"]



                    }
                }

            }
        }
        )

    # pp.pprint(results)
    print(str(results["hits"]["total"]) + " resultados para una query \"rehab\"")

    medications =[]
    f = open("medications.txt", "wb")
    # Iteramos sobre los resultados, no es preciso preocuparse de las
    # conexiones consecutivas que hay que hacer con el servidor ES
    for hit in results["aggregations"]["Terminos mas significativos"]["buckets"]:
        # get created date for a repo and fallback to authored_date for a commit
        print(str(hit["key"]))
        entityQuery = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+ hit["key"] +"&language=en&format=json"
        r = requests.get(entityQuery).json()
        if len(r["search"])>0:
          for res in r["search"]:
           #print(str(res['id']))
           code = str(res['id']);
           queryByCode = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+code+"&languages=en&format=json"
           rCode = requests.get(queryByCode).json();
           if "P31" in rCode["entities"][code]["claims"]:
            for code in rCode["entities"][code]["claims"]["P31"]:
               instanceCode = str(code["mainsnak"]["datavalue"]["value"]["id"]);
               print(str(code["mainsnak"]["datavalue"]["value"]["id"]));
               if instanceCode=="Q28885102" or instanceCode=="Q12140":
                    print("Es un medicamento:" +str(hit["key"]))
                    f.write(hit["key"].encode("UTF-8"))
                    f.write("\n".encode("UTF-8"))



    f.close()





if __name__ == '__main__':
    main()
