import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def fact_check_crew(news_headline_or_topic):
    """
    Simplified fact-checking function that works without crewai.
    Uses direct API calls to Google Gemini and Serper for web search.
    """
    start_time = time.time()
    
    # Get API keys from environment
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    serper_api_key = os.getenv('SERPER_API_KEY')
    
    if not gemini_api_key or gemini_api_key == 'your_gemini_api_key_here':
        return {
            "final_verdict": "Configuration Error",
            "reasoning": "Gemini API key not configured. Please set your GEMINI_API_KEY in the .env file.",
            "supporting_articles": [],
            "sources_verified": 0,
            "execution_time": time.time() - start_time
        }
    
    if not serper_api_key or serper_api_key == 'your_serper_api_key_here':
        return {
            "final_verdict": "Configuration Error",
            "reasoning": "Serper API key not configured. Please set your SERPER_API_KEY in the .env file.",
            "supporting_articles": [],
            "sources_verified": 0,
            "execution_time": time.time() - start_time
        }
    
    try:
        # Step 1: Search for relevant articles
        search_results = search_web(news_headline_or_topic, serper_api_key)
        
        # Step 2: Analyze with Gemini
        analysis = analyze_with_gemini(news_headline_or_topic, search_results, gemini_api_key)
        
        execution_time = time.time() - start_time
        
        return {
            "final_verdict": analysis.get("verdict", "Unable to determine"),
            "reasoning": analysis.get("reasoning", "Analysis could not be completed"),
            "supporting_articles": search_results[:3],  # Top 3 articles
            "sources_verified": len(search_results),
            "execution_time": execution_time
        }
        
    except Exception as e:
        return {
            "final_verdict": "Error",
            "reasoning": f"An error occurred during fact-checking: {str(e)}",
            "supporting_articles": [],
            "sources_verified": 0,
            "execution_time": time.time() - start_time
        }

def search_web(query, api_key):
    """
    Search the web using Serper API
    """
    url = "https://google.serper.dev/search"
    
    payload = json.dumps({
        "q": f"fact check {query}",
        "num": 5
    })
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if 'organic' in data:
            for item in data['organic'][:5]:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return results
        
    except Exception as e:
        print(f"Search error: {e}")
        return []

def analyze_with_gemini(topic, search_results, api_key):
    """
    Analyze the topic and search results using Google Gemini API
    """
    # Prepare context from search results
    context = "\n".join([
        f"Title: {result['title']}\nSnippet: {result['snippet']}\n"
        for result in search_results
    ])
    
    prompt = f"""
    You are a professional fact-checker. Analyze the following claim and the search results provided.
    
    Claim to fact-check: "{topic}"
    
    Search Results:
    {context}
    
    Based on the search results, provide a fact-check analysis in the following JSON format:
    {{
        "verdict": "True" | "False" | "Partially True" | "Misleading" | "Unverified",
        "reasoning": "Detailed explanation of your analysis and conclusion"
    }}
    
    Be thorough in your analysis and provide clear reasoning for your verdict.
    """
    
    try:
        # Using Gemini REST API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'candidates' in data and len(data['candidates']) > 0:
            text = data['candidates'][0]['content']['parts'][0]['text']
            
            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                import re
                json_match = re.search(r'\{[^}]+\}', text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    # Fallback if no JSON found
                    return {
                        "verdict": "Unverified",
                        "reasoning": text
                    }
            except json.JSONDecodeError:
                return {
                    "verdict": "Unverified",
                    "reasoning": text
                }
        else:
            return {
                "verdict": "Error",
                "reasoning": "No response from Gemini API"
            }
            
    except Exception as e:
        return {
            "verdict": "Error",
            "reasoning": f"API error: {str(e)}"
        }