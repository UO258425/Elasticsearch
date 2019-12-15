from elasticsearch import Elasticsearch

def main():
    es = Elasticsearch(["http://elastic.carlosmanrique.dev:9200"])

    subredditsQuery = es.search( index="reddit-mentalhealth-stopwords-stemming",
                            body ={
      "size": 0,
      "query": {
        "multi_match": {
          "fields": [
            "selftext",
            "subreddit",
            "title"
          ],
          "type": "phrase",
          "query": "problem with alcohol"
        }
      },
      "aggs": {
        "Subreddits relevantes": {
          "terms": {
            "field": "subreddit.keyword",
            "size": 20 
          }
        }
      }
    })



    selectedSubreddits = list()
    queryParam = ""

    for i in range(10):
        selectedSubreddits.append(subredditsQuery['aggregations']['Subreddits relevantes']['buckets'][i]['key'])

    queryParam = selectedSubreddits[0]
    for i in selectedSubreddits[2:]:
        queryParam += ", "+i
    
    comorbiditiesQuery = es.search(
        index="reddit-mentalhealth-stopwords-stemming",
        body={
            "size":0,
            "query":{
                "match":{
                    "subreddit":{
                        "query": queryParam,
                        "operator":"or"
                        }
                    }
                },
            "aggs":{
                "Most significant terms":{
                    "significant_terms":{
                        "field": "selftext",
                        "size":40000,
                        "gnd":{}
                    }
                }
            }
        })


    popOutput = [line.rstrip("\n") for line in open("popOutput.txt")]
    result = list()
    for i in comorbiditiesQuery["aggregations"]["Most significant terms"]["buckets"]:
        if i["key"].lower() in popOutput:
            result.append(i["key"])
            print(i["key"])

    resultFile = open("result.txt","wt")
    resultFile.write("\n".join(result))
        
if __name__ == '__main__':
    main()
