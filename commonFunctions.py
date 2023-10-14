import nltk
import string
import matplotlib.pyplot as plt
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords

def preprocess_text(tokens):

    # variable "tokens" being a list of words/tokens/characters

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

def detailSummary(df):

    # displayNonNull_statsforNum_groupsforCat_uniqueVars

    print(df.info())
    for x in df.columns.to_list():
        print(f"No. of unique variable '{x}': {df[x].nunique()}")
    print(df.describe())
    for x in df.columns.to_list():
        if df[x].dtype in ['int64', 'float64']:
            continue
        else:
            print(df[x].value_counts())

def hist(df, column_name):
    plt.hist(df[column_name], bins=10, edgecolor='black')
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.title(f'{column_name} Distribution')
    plt.grid(axis='y', alpha=0.75)
    plt.show()