from fastapi import FastAPI
from pydantic import BaseModel
import os
import sqlite3
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from keybert import KeyBERT
from openai import OpenAI

# Load API keys securely
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Initialize AI tools
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
kw_model = KeyBERT()
client = OpenAI(api_key=OPENAI_KEY)

# Initialize FastAPI
app = FastAPI()

# Create SQLite database for search history
conn = sqlite3.connect("search_history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, query TEXT)")
conn.commit()

class SearchRequest(BaseModel):
    keyword: str

def google_search(query, num_results=3):
    """Fetch top search results from Google using SerpAPI."""
    search_url = "https://serpapi.com/search"
    params = {"q": query, "api_key": SERPAPI_KEY, "num": num_results}

    response = requests.get(search_url, params=params)
    results = response.json()
    return [r["link"] for r in results.get("organic_results", [])[:num_results]]

def fetch_and_summarize(url):
    """Scrapes text from the URL and summarizes it."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        text = " ".join([p.get_text() for p in soup.find_all('p')])
        if len(text) < 200:
            return None, "Content too short to summarize."

        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')

        return summary, [kw[0] for kw in keywords]

    except Exception as e:
        return None, f"Error fetching {url}: {e}"

def generate_related_topics(summary):
    """Generates related search suggestions using GPT."""
    prompt = f"Given this summary: '{summary}', suggest 5 related search topics."
    response = client.completions.create(model="gpt-4", prompt=prompt, max_tokens=100)
    return response.choices[0].text.strip().split("\n")

@app.post("/search")
def search_articles(request: SearchRequest):
    """Handles search requests and returns summarized articles."""
    keyword = request.keyword

    cursor.execute("INSERT INTO history (query) VALUES (?)", (keyword,))
    conn.commit()

    top_links = google_search(keyword, num_results=3)
    results = []

    for url in top_links:
        summary, keywords = fetch_and_summarize(url)
        if summary:
            results.append({"url": url, "summary": summary, "keywords": keywords})

    combined_summaries = " ".join([r["summary"] for r in results])
    related_topics = generate_related_topics(combined_summaries)

    return {"results": results, "related_topics": related_topics}

@app.get("/history")
def get_history():
    """Fetches search history."""
    cursor.execute("SELECT query FROM history ORDER BY id DESC")
    history = [row[0] for row in cursor.fetchall()]
    return {"history": history}
