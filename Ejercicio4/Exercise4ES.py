from elasticsearch import Elasticsearch

def main():
    es = Elasticsearch()

    subredditsQuery = es.search( index="reddit-mentalhealth-stopwords-stemming-ngrams",
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
            "size": 10
          }
        }
      }
    })



    selectedSubreddits = list()

    for i in range(10):
        selectedSubreddits.append(subredditsQuery['aggregations']['Subreddits relevantes']['buckets'][i]['key'])

    for i in selectedSubreddits:
        print(i)

        
if __name__ == '__main__':
    main()
