import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from ai_handler import get_ai_response

def fetch_real_news(query):
    """
    Fetches real-time news headlines and links from Google News RSS.
    """
    try:
        # Use Google News RSS for real-time medical updates
        rss_url = f"https://news.google.com/rss/search?q={query}+medical+news&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(rss_url, timeout=10)
        root = ET.fromstring(response.content)
        
        news_items = []
        for item in root.findall('.//item')[:5]: # Take top 5 news items
            news_items.append({
                "title": item.find('title').text,
                "link": item.find('link').text,
                "pubDate": item.find('pubDate').text,
                "source": item.find('source').text if item.find('source') is not None else "Google News"
            })
        return news_items
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

def get_medical_news(query="latest medical research"):
    """
    Fetches real news items and uses AI to summarize them.
    STRICT RULE: If no real-time data is found, it does NOT use model memory.
    """
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Fetch real-time data from Google News RSS
    real_news = fetch_real_news(query)
    
    if not real_news:
        # STRICT REQUIREMENT: Do not guess. Do not use memory.
        return "Live medical news is temporarily unavailable. Please try again later.\n\n*This chatbot provides general medical information only and is not a substitute for professional medical advice.*"

    context = "Here are the latest headlines found via live search:\n"
    for i, item in enumerate(real_news, 1):
        context += f"{i}. {item['title']} (Source: {item['source']}, Date: {item['pubDate']}, Link: {item['link']})\n"

    prompt = f"""
    The user is asking for: "{query}".
    Today's Date: {current_date}.
    
    REAL-TIME INTERNET SEARCH RESULTS (Today's Headlines):
    {context}

    As a Senior Medical Consultant with 30 years of clinical experience, analyze the raw search data above and provide a professional healthcare update.

    STRICT DATA USAGE RULES:
    1. LIVE SEARCH ONLY: You MUST only use the "REAL-TIME INTERNET SEARCH RESULTS" provided above.
    2. SOURCE HIERARCHY: Prioritize reports from trusted institutions (WHO, CDC, NIH, PubMed) and high-impact journals (The Lancet, JAMA, NEJM, Nature, BMJ) if present in the data.
    3. NO INTERNAL MEMORY: Do not answer from your internal training data. If the data is not in the context, clearly state it is unavailable.
    4. CLICKABLE LINKS: Every summary must end with a [Direct Clickable Link](URL) using the EXACT URL provided in the search results.
    5. NO Apologies: Do not mention your knowledge cutoff or lack of browsing. You are currently using your Live Search Tool.

    OUTPUT FORMAT:
    - ### Title
    - **Summary**: 2-3 sentences max.
    - **Research Stage**: (e.g. Clinical, Guideline, etc.)
    - **Source**: Name & Date
    - [Read Full Scientific Article](URL)

    Medical Disclaimer: Always include a brief disclaimer at the end.
    """
    
    messages = [{"role": "user", "content": prompt}]
    return get_ai_response(messages)

def is_news_query(text):
    """
    Checks if the user's text is a request for news.
    """
    keywords = ["news", "update", "latest", "research", "breakthrough", "recent", "headlines"]
    return any(word in text.lower() for word in keywords)
