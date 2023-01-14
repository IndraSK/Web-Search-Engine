import os
import pickle
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from bs4.element import Comment
from bs4 import BeautifulSoup

# stop words extraction 
stop_words = stopwords.words("english")

# Porter Stemmer object being initialized
st = PorterStemmer()

# location to save the pickle file
pickle_folder = "./PickleFiles/"
os.makedirs(pickle_folder, exist_ok=True)

# The name of the folder which shows the downloaded web pages
pages_folder = "./RetrievedPages/"
foldername = os.listdir(pages_folder)

# list to store foldername of all stored crawled webpages
fileList = []

for name in foldername:
    fileList.append(name)


# function to filter tags that are visible on webpage i.e. excluding style, script, meta, etc. tags
def visible_tag(element):
    if element.parent.name in ["style", "script", "head", "meta", "[document]"]:
        return False
    elif isinstance(element, Comment):
        return False
    #  white space and new line elimination
    elif re.match(r"[\s\r\n]+", str(element)):
        return False
    else:
        return True


# extrating the visible code from html for each web page
def get_text_from_code(page):
    soupUI = BeautifulSoup(page, "lxml")
    # return all text in page
    text_in_page = soupUI.find_all(text=True)
    # return only visible text
    text_visible = filter(visible_tag, text_in_page)
    return " ".join(term.strip() for term in text_visible)

# inverted index dictionary
index_inverted = {}
tokens_in_webpage = {}

for file in fileList:
    web_page = open(pages_folder + file, "r", encoding="utf-8")
    code = web_page.read()
    # get all text actually visible on web page
    text = get_text_from_code(code)
    text = text.lower()
    # remove all punctuations and digits
    text = re.sub("[^a-z]+", " ", text)
    tokens = text.split()
    # removing stop words and stemming each token while only accepting stemmed tokens with length greater than 2
    clean_stem_tokens = [
        st.stem(token)
        for token in tokens
        if (token not in stop_words and st.stem(token) not in stop_words)
        and len(st.stem(token)) > 2
    ]

    # add tokens in web page to dict
    tokens_in_webpage[file] = clean_stem_tokens

    for token in clean_stem_tokens:
        # retrieving the frequency of token and setting the value as 0 if token in not present in the dictionary
        freq = index_inverted.setdefault(token, {}).get(file, 0)

        # 1 was added to frequency of token in current webpage
        index_inverted.setdefault(token, {})[file] = freq + 1


# inverted index and webpage tokens are pickeled
with open(pickle_folder + "index_inverted.pickle", "wb") as f:
    pickle.dump(index_inverted, f)

with open(pickle_folder + "webpages_tokens.pickle", "wb") as f:
    pickle.dump(tokens_in_webpage, f)
