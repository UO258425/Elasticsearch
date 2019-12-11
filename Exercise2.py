from __future__ import print_function

from elasticsearch import Elasticsearch
from elasticsearch import helpers


def main():
    global es
    es = Elasticsearch([{'host': 'elastic.carlosmanrique.dev'}])

    stopwords = ["a", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "about", "above", "after", "again",
                 "against", "all", "am", "an", "and", "any", "are",
                 "aren't", "as", "at", "be", "because", "been",
                 "before", "being", "below", "between", "both",
                 "but", "by", "can't", "cannot", "could",
                 "couldn't", "did", "didn't", "do", "does",
                 "doesn't", "doing", "don't", "down", "during",
                 "each", "few", "for", "from", "further", "had",
                 "hadn't", "has", "hasn't", "have", "haven't",
                 "having", "he", "he'd", "he'll", "he's", "her",
                 "here", "here's", "hers", "herself", "him",
                 "himself", "his", "how", "how's", "i", "i'd",
                 "i'll", "i'm", "i've", "if", "in", "into", "is",
                 "isn't", "it", "it's", "its", "itself", "let's",
                 "me", "more", "most", "mustn't", "my", "myself",
                 "no", "nor", "not", "of", "off", "on", "once",
                 "only", "or", "other", "ought", "our", "ours",
                 "ourselves", "out", "over", "own", "same",
                 "shan't", "she", "she'd", "she'll", "she's",
                 "should", "shouldn't", "so", "some", "such",
                 "than", "that", "that's", "the", "their",
                 "theirs", "them", "themselves", "then", "there",
                 "there's", "these", "they", "they'd", "they'll",
                 "they're", "they've", "this", "those", "through",
                 "to", "too", "under", "until", "up", "very", "was",
                 "wasn't", "we", "we'd", "we'll", "we're", "we've",
                 "were", "weren't", "what", "what's", "when",
                 "when's", "where", "where's", "which", "while",
                 "who", "who's", "whom", "why", "why's", "with",
                 "won't", "would", "wouldn't", "you", "you'd",
                 "you'll", "you're", "you've", "your", "yours",
                 "yourself", "yourselves", "d", "ll", "m", "re",
                 "s", "t", "ve", "aren", "can", "couldn", "didn",
                 "doesn", "don", "hadn", "hasn", "haven", "he",
                 "here", "how", "i", "isn", "it", "let", "mustn",
                 "shan", "she", "shouldn", "that", "there", "they",
                 "wasn", "we", "weren", "what", "when", "where",
                 "who", "why", "won", "wouldn", "you", "will", "since", "really", "ago"
                                                                                  "just", "today", "one", "two",
                 "three", "four", "five", "six", "seven", "eight",
                 "nine", "zero", "now", "go", "like", "much", "still", "every", "very", "even", "make", "made",
                 "think", "also", "way", "things", "stuff", "such", "as", "lot", "weeks", "days", "another",
                 "other", "well", "long", "short", "ago", "next", "around", "years", "first", "second", "day",
                 "get", "just", "got", "gotten", "getting", "go", "went", "gone", "going"]
                 
    index = "reddit-mentalhealth"

    results = es.search(
        index="reddit-mentalhealth",
        body={
            "size": 12,
            "query": {
                "more_like_this": {
                    "fields": [
                        "selftext",
                        "title"
                    ],
                    "stop_words": stopwords,
                    "like": ["rehab"],
                    "min_term_freq": 1,
                    "max_query_terms": 12
                }
            },
            "aggs": {
                "terms": {
                    "significant_terms": {
                        "field": "selftext",
                        "size": 50,
                        "exclude": stopwords,
                    }
                }
            }
        }
    )

    print(str(results["hits"]["total"]) + " resultados para una query \"rehab\"")

    for hit in results["aggregations"]["terms"]["buckets"]:
        print(str(hit["key"]))


if __name__ == '__main__':
    main()
