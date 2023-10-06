# variable "tokens" being a list of words/tokens/characters


# import nltk
# import string
# from nltk import word_tokenize, FreqDist
# from nltk.corpus import stopwords

def preprocess_text(tokens):
    # Convert all characters to lower case
    tokens = [t.lower() for t in tokens]

    # Remove Punctuations (.,)
    tokens = [t for t in tokens if t not in string.punctuation]

    # Remove Stopwords (I, you, our, we)
    stop = stopwords.words('english')
    tokens = [t for t in tokens if t not in stop]

    # Remove Numbers/Numerics
    tokens = [t for t in tokens if not t.isnumeric()]

    # Remove from filtered list, to manually include
    filter_list = ["’", "“", "”", "would", "could", "'s", "left", "right", "a.m.", "p.m."]
    tokens = [t for t in tokens if ':' not in t and t not in filter_list]

    # Choose either Stemming or Lemmatization

#    # Stemming - Reduce words to base form via removal of prefix and suffix
#     porter = nltk.PorterStemmer()
#     tokens=[ porter.stem(t) for t in tokens ]

    # Lemmatization - Reduce words to base form/lemma
    #nltk.download('omw-1.4')
    wnl = nltk.WordNetLemmatizer()
    tokens = [ wnl.lemmatize(t) for t in tokens ] 

    return tokens