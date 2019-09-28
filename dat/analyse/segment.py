import math
import urllib.request, urllib.error, urllib.parse
import os
from dat.analyse.util import temp_directory

class OneGramDist(dict):

   URL="https://gist.githubusercontent.com/mrturkmen06/d9d5f8bc35be8efd81c447f70ca99fbf/raw/cfa317d7bce53ba55ca8f9bf27aa3170038f99cf/one-grams.txt"
   FILEPATH=temp_directory.name+"one-grams.txt"
   @classmethod
   def fetch_one_grams(cls, url=None):
      url = url
      print('Fetching one gram file from gist ..')
      lines = urllib.request.urlopen(cls.URL).readlines()
      f = open(cls.FILEPATH, 'wb')
      f.writelines(lines)
      f.close()

   def __init__(self, filename):
      self.gramCount = 0

      for line in open(filename):
         (word, count) = line[:-1].split('\t')
         self[word] = int(count)
         self.gramCount += self[word]

   def __call__(self, key):
      if key in self:
         return float(self[key]) / self.gramCount
      else:
         return 1.0 / (self.gramCount * 10**(len(key)-2))


if os.path.exists(temp_directory.name+"one-grams.txt"):
   singleWordProb = OneGramDist(temp_directory.name+"one-grams.txt")
else:
   singleWordProb = OneGramDist.fetch_one_grams()



singleWordProb = OneGramDist(temp_directory.name+"one-grams.txt")
def word_seq_fitness(words):
   return sum(math.log10(singleWordProb(w)) for w in words)

def memoize(f):
   cache = {}

   def memoizedFunction(*args):
      if args not in cache:
         cache[args] = f(*args)
      return cache[args]

   memoizedFunction.cache = cache
   return memoizedFunction

@memoize
def segment(word):
   if not word: return []
   word = word.lower() # change to lower case
   allSegmentations = [[first] + segment(rest) for (first,rest) in splitPairs(word)]
   return max(allSegmentations, key = word_seq_fitness)

def splitPairs(word, maxLen=20):
   return [(word[:i+1], word[i+1:]) for i in range(max(len(word), maxLen))]

@memoize
def segment_with_prob(word):
   segmented = segment(word)
   return (word_seq_fitness(segmented), segmented)
