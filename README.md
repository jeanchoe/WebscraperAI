# AI-Powered Web Search & Summarizer

An **AI-driven search engine** that finds the best articles for a given keyword, **scrapes their content, and generates AI-powered summaries**. Results are displayed in a **ChatGPT-style interface** with search history and AI-generated related topic suggestions. 🚀  

## ***FEATURES***
AI Summarization – Extracts key insights from articles.  
Smart Search – Finds top articles using Google Search API.  
Related Topic Suggestions – Helps users explore further.  
Search History – Keeps track of past searches.  
ChatGPT-Style UI – Clean and interactive experience.  

---

## **Installation Guide**
### **Clone the Repository**
```sh
git clone your-repo-url ai-web-scraper
cd ai-web-scraper

```
***BACKEND SETUP***
cd backend
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate (Mac/Linux)
venv\Scripts\activate  # Activate (Windows)
pip install -r requirements.txt  # Install dependencies

Secure API keys
SERPAPI_KEY=your_new_serpapi_key
OPENAI_KEY=your_new_openai_key

Run FastAPI Server
uvicorn main:app --reload

***FRONT END SETUP***
cd frontend
npm install  # Install dependencies

Set backend URL
REACT_APP_BACKEND_URL=http://127.0.0.1:8000

Start React App
npm start

***API Endpoints***
Method	Endpoint	Description
POST	/search	Searches for a keyword and returns AI-generated summaries.
GET	/history	Fetches the search history.


***DEPLOYMENT***
***Deploy Backend (FastAPI)
Use Railway, Render, AWS, or Heroku.
Example: Deploy using Railway.app.
***Deploy Frontend (React)
Use Vercel, Netlify, or GitHub Pages.
Example: Deploy on Vercel:
sh
Copy code
npm run build
vercel deploy
