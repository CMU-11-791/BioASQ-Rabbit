from nltk import word_tokenize
from nltk.corpus import stopwords

# URL= os.environ.get("SIMILARITY", "http://localhost:8081/jaccard")
#
# class SimilarityJaccard:
#     def __init__(self):
#         pass
#
#     def calculateSimilarity(self, s1, s2):
#         data = json.dumps([s1,s2])
#         resp = requests.post(URL, data = data, headers=self.header)
#         score_dict = json.loads(resp.text)
#         return score_dict['score']

# from SimilarityMeasure import *


# class SimilarityJaccard(SimilarityMeasure):


class SimilarityJaccard(object):
    def __init__(self):
        self.stopWords = set(stopwords.words('english'))

    def calculateSimilarity(self, s1, s2):
        set1 = set([i.lower() for i in word_tokenize(s1) if i.lower() not in self.stopWords])
        set2 = set([i.lower() for i in word_tokenize(s2) if i.lower() not in self.stopWords])
        return float(len(set1.intersection(set2))) / len(set1.union(set2))


"""
instance = SimilarityJaccard("apple banana cat dog", "apple elephant cat dog")
print instance.calculateSimilarity()
"""
