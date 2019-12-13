from __future__ import print_function

from elasticsearch import Elasticsearch
from elasticsearch import helpers


def main():
    global es
    es = Elasticsearch([{'host': 'elastic.carlosmanrique.dev'}])

    index = "reddit-mentalhealth-stopwords"

    terms_size = 150

    results_mlt = es.search(
        index=index,
        body={
            "size": 12,
            "query": {
                "more_like_this": {
                    "fields": [
                        "selftext"
                    ],
                    "like": ["rehab", "rehabilitation"],
                    "min_term_freq": 1,
                    "max_query_terms": 12
                }
            },
            "aggs": {
                "terms": {
                    "significant_terms": {
                        "field": "selftext",
                        "size": terms_size
                    }
                }
            }
        }
    )

    #print(str(results_mlt["hits"]["total"]) + " resultados para una query \"rehab\" usando mlt")

    terms_mlt = []

    for hit in results_mlt["aggregations"]["terms"]["buckets"]:
        #print(str(hit["key"]))
        terms_mlt.append(hit["key"])

    results_gnd = es.search(
        index=index,
        body={
            "query": {
                "match": {
                    "selftext": {
                        "query": "rehab rehabilitation",
                        "operator": "or"
                    }
                }
            },
            "aggs": {
                "terms": {
                    "significant_terms": {
                        "field": "selftext",
                        "size": terms_size,
                        "gnd": {

                        }
                    }
                }

            }
        }
    )

    #print(str(results_gnd["hits"]["total"]) + " resultados para una query \"rehab\" usando gnd")

    terms_gnd = []

    for hit in results_gnd["aggregations"]["terms"]["buckets"]:
        #print(str(hit["key"]))
        terms_gnd.append(hit["key"])

    terms_gnd.sort()
    terms_mlt.sort()

    matches = 0

    for i in range(len(terms_gnd)):
        for j in range(len(terms_mlt)):
            if(terms_gnd[i] == terms_mlt[j]):
                #print("{0} matches on both".format(terms_mlt[j]))
                matches += 1

    print("MLT:")
    print("\t",terms_mlt)
    print("------------------------")
    print("GND:")
    print("\t",terms_gnd)
    print()
    print("Total matches: {0}, similarity: {1}%".format(matches, matches*100/terms_size))
if __name__ == '__main__':
    main()

