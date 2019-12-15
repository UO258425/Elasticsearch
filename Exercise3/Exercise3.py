# Para poder usar la función print e imprimir sin saltos de línea
from __future__ import print_function

import json # Para poder trabajar con objetos JSON
import pprint # Para poder hacer uso de PrettyPrinter
import sys # Para poder usar exit

from elasticsearch import Elasticsearch
import requests
from elasticsearch import helpers

def main():


    # Connect to our index
    es = Elasticsearch(['http://elastic.carlosmanrique.dev:9200'])
    # Index without stopwords
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
                "Significant terms":{
                    "significant_terms":{
                        "field":"selftext",
                        "size":100,
                        "gnd":{

                        },

                        "exclude":["prescribes", "prescribed", "prescribe", "prescription", "prescribing", "prescriber",
                                   "medicine",
                                   "meds", "drugs", "dose", "doctor", "pharmacy", "diagnosed", "diagnostic",
                                   "medications", "medication", "dose", "dosage", "pill", "pills", "psychiatrist", "mg",
                                   "tak*", "effect", "effects", "symptoms", "gp"
                            , "antidepressants", "drugs", "lower", "treatment", "pharmacist", "drug", "doctors",
                                   "height", "infection", "duration", "lbs"
                            , "prescriptions", "oral", "nausea", "fever", "blood", "intolerance", "intolerances",
                                   "appointment", "appointments",
                                   "addicted", "addictive", "addiction", "tested", "doses", "adhd", "doc", "referred",
                                   "allergy", "allergic", "tests"
                            , "specialist", "reuptake", "inflammation", "grossly", "recreational", "recreationally",
                                   "advised", "advises", "switched", "experience",
                                   "experienced", "experiencing", "side", "effects", "pain", "pains", "taking", "took",
                                   "taken", "addictiveness", "antidepressant"
                            , "podiatrist", "complaint", "medical", "emergency", "urgent", "attacks", "smoker",
                                   "result", "results", "recommended", "recomendation",
                                   "consultation", "physician", "physchaitrist", "capsules", "tablets", "nuerologist",
                                   "ssri", "stimulant", "stimulants", "adverse", "test"
                            , "deficiency", "decrease", "decreased", "caucasian", "x", "testing", "fatigue", "symptoms",
                                   "dermatologist"]



                    }
                }

            }
        }
        )


    print(str(results["hits"]["total"]) + " potential medication terms")


    f = open("medications.txt", "wb")
    fPosts = open("significantTerms.txt","wb")
    # Iterate through list of potential medications
    for hit in results["aggregations"]["Significant terms"]["buckets"]:
        fPosts.write(hit["key"].encode("UTF-8"))
        fPosts.write("\n".encode("UTF-8"))
        entityQuery = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+ hit["key"] +"&language=en&format=json"
        # Get all of the Wikidata entities whose name matches the term
        r = requests.get(entityQuery).json()
        isMedication = False
        #If it recovers any entity
        if len(r["search"])>0:
          for res in r["search"]:

           code = str(res['id']);
           queryByCode = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+code+"&languages=en&format=json"
           #Get all of the Wikidata information of the entity with such code
           rCode = requests.get(queryByCode).json();
           #If the entity has P31 wich is the "instanceof" property
           #we go through all the all of them
           if "P31" in rCode["entities"][code]["claims"]:
            for code in rCode["entities"][code]["claims"]["P31"]:
                #If this significant term hasn't found a medication match yet
                #Avoids repeated data
               if not isMedication:
                instanceCode = str(code["mainsnak"]["datavalue"]["value"]["id"]);
               #The entity is an instance of pharmaceutical or product or medication
                if instanceCode=="Q28885102" or instanceCode=="Q12140":
                    print("Is a medication:" +str(hit["key"]))
                    f.write(hit["key"].encode("UTF-8"))
                    f.write("\n".encode("UTF-8"))
                    isMedication=True

    f.close()
    fPosts.close()





if __name__ == '__main__':
    main()
