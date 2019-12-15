
from __future__ import print_function

import datetime
import json # Para poder trabajar con objetos JSON
import pprint # Para poder hacer uso de PrettyPrinter
import sys # Para poder usar exit

from elasticsearch import Elasticsearch
from elasticsearch import helpers

def main():


    # Connect to our index
    es = Elasticsearch(['http://elastic.carlosmanrique.dev:9200'])
    #Index without stop words
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
                "Significant terms":{
                    "significant_terms":{
                        "field":"selftext",
                        "size":20,
                        "gnd":{

                        },


                    }
                }

            }
        }
        )


    print(str(results["hits"]["total"]) + " results for query about \"rehab\"")

    significant =[]
    words = ""
    f1 = open("significantWordsGND.txt","wb")
    # Iterate results saving them in a variable to use in second query
    for hit in results["aggregations"]["Significant terms"]["buckets"]:
        significant.append(hit["key"])
        f1.write(hit["key"].encode("UTF-8"))
        f1.write("\n".encode("UTF-8"))
        words+=" "+str(hit["key"])
    f1.close()


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

    # Second query upon complete index
    posts = helpers.scan(es,index="reddit-mentalhealth",query=secondQuery)

    f = open("relatedPostsGND.txt", "wb")
    for hit in posts:
        f.write('{ "author" : "'.encode("UTF-8"))
        f.write(hit["_source"]["author"].encode("UTF-8"))
        f.write('",\n'.encode("UTF-8"))
        postdate = datetime.datetime.utcfromtimestamp(hit["_source"]["created_utc"] )
        f.write('"date" : "'.encode("UTF-8"))
        f.write(postdate.strftime("%m/%d/%Y, %H:%M:%S").encode("UTF-8"))
        f.write('",\n'.encode("UTF-8"))
        f.write('"selftext" : "'.encode("UTF-8"))
        f.write(hit["_source"]["selftext"].encode("UTF-8"))
        f.write('"\n}\n'.encode("UTF-8"))

    f.close()



if __name__ == '__main__':
    main()
