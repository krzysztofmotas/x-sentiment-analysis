import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
nltk.download("punkt")

with open("tweets_cleaned.json", encoding="utf-8") as f:
    df = pd.read_json(f)

df["created_at"] = pd.to_datetime(df["created_at"])

# Inicjalizacja analizatora sentymentu VADER
sia = SentimentIntensityAnalyzer()

# Oblicza ogólny wynik sentymentu dla podanego tekstu
def get_vader_sentiment(text):
    return sia.polarity_scores(text)["compound"]

# Klasyfikuje wynik sentymentu jako pozytywny, neutralny lub negatywny
def classify_sentiment(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

df["sentiment"] = df["cleaned_text"].apply(get_vader_sentiment)
df["sentiment_label"] = df["sentiment"].apply(classify_sentiment)

# Chmura słów
text = " ".join(df["cleaned_text"])
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="Blues").generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Chmura słów – Transfery Realu Madryt")
plt.tight_layout()
plt.show()

# Wykres słupkowy – rozkład nastrojów
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="sentiment_label", hue="sentiment_label", palette="coolwarm", legend=False)
plt.title("Rozkład nastrojów w tweetach")
plt.xlabel("Nastrój")
plt.ylabel("Liczba tweetów")
plt.tight_layout()
plt.show()

# Wykres liniowy – sentyment w czasie
df_sorted = df.sort_values("created_at")
df_sorted["avg_sentiment"] = df_sorted["sentiment"].rolling(window=3, min_periods=1).mean()

plt.figure(figsize=(10, 5))
plt.plot(df_sorted["created_at"], df_sorted["avg_sentiment"], marker="o")
plt.title("Zmiana nastroju w czasie")
plt.xlabel("Czas")
plt.ylabel("Średni sentyment")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Heat mapa - średni sentyment vs. długość tweeta
df["word_count"] = df["cleaned_text"].apply(lambda x: len(x.split()))

df["word_count_range"] = pd.cut(
    df["word_count"],
    bins=[0, 5, 10, 20, 40],
    labels=["0–5 słów", "6–10 słów", "11–20 słów", "21–40 słów"]
)

avg_sentiment_by_length = df.pivot_table(
    index="word_count_range",
    values="sentiment",
    aggfunc="mean",
    observed=False
)

sns.heatmap(avg_sentiment_by_length, annot=True, cmap="YlGnBu", center=0)
plt.title("Średni sentyment względem długości tweeta")
plt.ylabel("Zakres liczby słów")
plt.xlabel("Sentyment")
plt.tight_layout()
plt.show()
