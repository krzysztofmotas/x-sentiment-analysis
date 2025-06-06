import json
import re
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

def clean_tweet(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def remove_stopwords(text):
    tokens = word_tokenize(text)
    filtered = [word for word in tokens if word not in stop_words and word.isalpha()]
    return " ".join(filtered)

nltk.download('stopwords')
nltk.download('punkt')

with open("tweets.json", encoding="utf-8") as f:
    raw = json.load(f)

tweets_list = raw["data"]
df = pd.DataFrame(tweets_list)

df["cleaned_text"] = df["text"].apply(clean_tweet)
stop_words = set(stopwords.words("english"))
df["cleaned_text"] = df["cleaned_text"].apply(remove_stopwords)

df[["text", "cleaned_text", "created_at"]].to_json(
    "tweets_cleaned.json", orient="records", force_ascii=False, indent=4
)
