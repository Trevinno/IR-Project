import math

class BM25:
    def __init__(self, recipeNames, k1=1.2, b=0.75, word_weights=None):
        self.k1 = k1
        self.b = b
        self.word_weights = word_weights or {}
        self.name_frequencies = []
        
        #Split recipe names into words (and apply lowercase (this could be done in preprocessing or here))
        self.tokenised_names = [name.lower().split() for name in recipeNames]
        
        #Word weights
        self.weighted_names = self.apply_word_weights(self.tokenised_names)        
        self.name_frequencies = self.count_word_frequencies(self.weighted_names)
        
        #Lengths and IDF
        self.name_lengths = [len(name) for name in self.weighted_names]
        self.avgNameLength = sum(self.name_lengths) / len(self.name_lengths) if self.name_lengths else 0        
        self.idf = self._calculate_idf()
    
    def apply_word_weights(self, tokenised_names):
        weighted_names = []
        for name in tokenised_names:
            weighted_name = []
            for word in name:
                #Add words for word weights
                weight = self.word_weights.get(word, 1)
                weighted_name.extend([word] * weight)
            weighted_names.append(weighted_name)
        return weighted_names
    
    def count_word_frequencies(self, word_lists):
        word_frequencies = []    
        for word_list in word_lists:
            word_freq = {}
            for word in word_list:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
            word_frequencies.append(word_freq)    
        return word_frequencies

    def _calculate_idf(self):
        idf_dict = {}
        nameFreq = {}
        totalRecipeNames = len(self.weighted_names)    

        #How many recipes contain the word
        for name in self.weighted_names:
            for word in set(name):
                if word in nameFreq:
                    nameFreq[word] += 1
                else:
                    nameFreq[word] = 1
    
        #IDF for each word
        for word, freq in nameFreq.items():
            idf_dict[word] = math.log(1 + (totalRecipeNames - freq + 0.5) / (freq + 0.5))
            
        return idf_dict


    def get_scores(self, query):
        query_words = query.lower().split()
    
        #Apply word weights to queries
        weighted_query = []
        for word in query_words:
            weight = self.word_weights.get(word, 1)
            for _ in range(weight):
                weighted_query.append(word)
    
        scores = [0] * len(self.weighted_names)    
        #Calculate score contribution for each query word
        for word in weighted_query:
            if word not in self.idf:
                continue        
            #Check each recipe name for this word
            for recipe_index, term_counts in enumerate(self.name_frequencies):
                if word not in term_counts:
                    continue
            
              #BM25 score for this word in this recipe
                term_freq = term_counts[word]
                recipe_length = self.name_lengths[recipe_index]            
                idf_value = self.idf[word]
                length_normalization = (1 - self.b + self.b * recipe_length / self.avgNameLength)
                term_frequency_factor = (term_freq * (self.k1 + 1)) / (term_freq + self.k1 * length_normalization)

                scores[recipe_index] += idf_value * term_frequency_factor 
    
        return scores

    #Takes in our search query and returns the results
    def search(self, query, recipe_max):
        scores = self.get_scores(query)
        scored_names = [(i, score) for i, score in enumerate(scores)]
        return scored_names[:recipe_max]


# #This is where we add our input
# if __name__ == "__main__":
#     recipeNames = [
#         "Johnny boys big mash and chicken",
#         "Home cooked chicken meal good times",
#         "Yes, its fresh broccoli, good"
#     ]
    
#     #This is where we add our extra weights
#     word_weights = {
#         "meal": 4,    #"meal" is 4 times more important
#         "chicken": 2,
#         "pasta": 15
#     }

#     #We have nothing for punctuation! (this could be done in preprocessing or here)
#     bm25 = BM25(recipeNames, word_weights=word_weights)
#     results = bm25.search("good", 50)
#     for name_id, score in results:
#         print(f"Recipe {name_id} - {score:.3f}")
