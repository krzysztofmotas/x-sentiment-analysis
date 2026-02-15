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

# Initialize VADER
sia = SentimentIntensityAnalyzer()

# Calculate overall sentiment score for the given text
def get_vader_sentiment(text):
    return sia.polarity_scores(text)["compound"]

# Classify sentiment score as positive, neutral or negative
def classify_sentiment(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

df["sentiment"] = df["cleaned_text"].apply(get_vader_sentiment)
df["sentiment_label"] = df["sentiment"].apply(classify_sentiment)

# Word cloud
text = " ".join(df["cleaned_text"])
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="Blues").generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud - Real Madrid Transfers")
plt.tight_layout()
plt.show()

# Bar chart – sentiment distribution
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="sentiment_label", hue="sentiment_label", palette="coolwarm", legend=False)
plt.title("Sentiment Distribution in Tweets")
plt.xlabel("Sentiment")
plt.ylabel("Number of Tweets")
plt.tight_layout()
plt.show()

# Line chart – sentiment over time
df_sorted = df.sort_values("created_at")
df_sorted["avg_sentiment"] = df_sorted["sentiment"].rolling(window=3, min_periods=1).mean()

plt.figure(figsize=(10, 5))
plt.plot(df_sorted["created_at"], df_sorted["avg_sentiment"], marker="o")
plt.title("Sentiment Change Over Time")
plt.xlabel("Time")
plt.ylabel("Average Sentiment")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Heat map - average sentiment vs. tweet length
df["word_count"] = df["cleaned_text"].apply(lambda x: len(x.split()))

df["word_count_range"] = pd.cut(
    df["word_count"],
    bins=[0, 5, 10, 20, 40],
    labels=["0-5 words", "6-10 words", "11-20 words", "21-40 words"]
)

avg_sentiment_by_length = df.pivot_table(
    index="word_count_range",
    values="sentiment",
    aggfunc="mean",
    observed=False
)

sns.heatmap(avg_sentiment_by_length, annot=True, cmap="YlGnBu", center=0)
plt.title("Average Sentiment by Tweet Length")
plt.ylabel("Word Count Range")
plt.xlabel("Sentiment")
plt.tight_layout()
plt.show()
