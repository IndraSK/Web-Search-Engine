import math
import pickle
import os
import copy
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter

N = 7001

stop_words = stopwords.words("english")

st = PorterStemmer()

# folder to store pickle files
pickle_folder = "./PickleFiles/"
os.makedirs(pickle_folder, exist_ok=True)

idf_webpages = {}
max_freq = {}
webpages_tf_idf = {}

# Loading all the pickle files
with open(pickle_folder + "inverted_index.pickle", "rb") as f:
    inverted_index = pickle.load(f)

with open(pickle_folder + "webpages_tokens.pickle", "rb") as f:
    webpages_tokens = pickle.load(f)

with open(pickle_folder + "Retrieved_pages_crawled.pickle", "rb") as f:
    urls = pickle.load(f)


# Calculate IDF
def calculate_idf(inverted_index):
    idf = {}
    for key in inverted_index.keys():
        df = len(inverted_index[key].keys())
        # calculating IDF for a token
        idf[key] = math.log2(N / df)
    return idf


# Calculate Tf-Idf
def calculate_tfidf(inverted_index):
    tf_idf = copy.deepcopy(inverted_index)
    for token in tf_idf:
        for page in tf_idf[token]:
            tf = tf_idf[token][page] / max_freq[page]
            tf_idf[token][page] = tf * idf_webpages[token]
    return tf_idf


# Calculate Document length
def calculate_doc_length(doc, doc_tokens):
    doc_len = 0
    for token in set(doc_tokens):
        # adding square of weight of token to document vector length
        doc_len = doc_len+webpages_tf_idf[token][doc] ** 2
    doc_len = math.sqrt(doc_len)
    return doc_len


# Calculate Document Vector Length
def doc_len_pages(list_of_tokens):
    doc_lens = {}
    for page in list_of_tokens:
        doc_lens[page] = calculate_doc_length(page, list_of_tokens[page])
    return doc_lens


# Calculate cosine similarity
def calculate_cos_sim_scores(query, doc_lens):
    similarity_scores = {}
    query_length = 0
    query_weights = {}
    # create count dictionary of the query
    query_dict = Counter(query)

    for token in query_dict.keys():
        # calculate query token TF
        token_tf = query_dict[token] / query_dict.most_common(1)[0][1]
        # calculate query token TF-IDF of token
        query_weights[token] = token_tf * idf_webpages.get(token, 0)
        # add square of token weight to query vector length
        query_length += query_weights[token] ** 2

    query_length = math.sqrt(query_length)

    for token in query:
        token_weight = query_weights.get(token)

        if token_weight:
            # calculating inner product between query and webpages
            for page in webpages_tf_idf[token].keys():
                similarity_scores[page] = similarity_scores.get(page, 0) + (
                    webpages_tf_idf[token][page] * token_weight
                )

    # dividing inner product by product of doc lens of query and webpage
    for page in similarity_scores:
        similarity_scores[page] = similarity_scores[page] / (doc_lens[page] * query_length)

    return similarity_scores


# function to tokenize query text
def tokenize_query(query_text):
    text = query_text.lower()
    text = re.sub("[^a-z]+", " ", text)
    tokens = text.split()
    clean_stem_tokens = [
        st.stem(token)
        for token in tokens
        if (token not in stop_words and st.stem(token) not in stop_words)
        and len(st.stem(token)) > 2
    ]
    return clean_stem_tokens


def show_relevant_pages(count, webpages):
    for i in range(count, count + 10):
        try:
            url_no = int(webpages[i][0])

        # executed when their are no more relevant pages to display
        except Exception as e:
            print("\nNo more results found !!")
            break

        if urls.get(url_no, None):
            print(i + 1, urls.get(url_no))


# calculating IDF 
idf_webpages = calculate_idf(inverted_index)

# finding the frequency of most frequent token in each webpage
for page in webpages_tokens:
    max_freq[page] = Counter(webpages_tokens[page]).most_common(1)[0][1]

# calculating TF-IDF 
webpages_tf_idf = calculate_tfidf(inverted_index)

# calculating document vector length 
webpages_lens = doc_len_pages(webpages_tokens)


print("\n ***  UIC Web Search Engine  *** \n")
query = str(input("Enter search query: "))
print("\n")
query_tokens = tokenize_query(query)

# calculate cosine similarity scores
query_sim_pages = calculate_cos_sim_scores(query_tokens, webpages_lens)

# sort cosine similarities in descending order
most_relevant_pages = sorted(query_sim_pages.items(), key=lambda x: x[1], reverse=True)

yes = {"y", "yes"}
first_pass = True
count = 0

while first_pass or choice.lower() in yes:
    first_pass = False
    show_relevant_pages(count, most_relevant_pages)
    choice = str(input("\nDo you want to more web page results? "))
    count += 20
