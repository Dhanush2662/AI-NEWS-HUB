import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Any

# Import our simplified fact-checking function
from trigger_crew_simple import fact_check_crew

# Configure page settings
st.set_page_config(
    page_title="FactBot AI - Simplified",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Theme Configuration
DARK_THEME = {
    "primary-color": "#4CAF50",
    "secondary-color": "#2196F3",
    "accent-color": "#FFD54F",
    "success-color": "#8BC34A",
    "warning-color": "#FFD54F",
    "danger-color": "#E57373",
    "dark-bg": "#1E1E1E",
    "light-bg": "#262730",
    "main-bg": "#121212",
    "text-color": "#E0E0E0",
    "secondary-text-color": "#A0A0A0",
    "card-bg-gradient-light": "#2A2A2A",
    "card-bg-gradient-dark": "#333333",
}

# Initialize processing state
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

def apply_dark_theme():
    """Applies the dark theme's CSS variables."""
    theme_colors = DARK_THEME
    
    fake_result_bg = f"linear-gradient(135deg, {theme_colors['danger-color']}20, {theme_colors['card-bg-gradient-dark']})"
    true_result_bg = f"linear-gradient(135deg, {theme_colors['success-color']}20, {theme_colors['card-bg-gradient-dark']})"
    mixed_result_bg = f"linear-gradient(135deg, {theme_colors['warning-color']}20, {theme_colors['card-bg-gradient-dark']})"
    
    st.markdown(f"""
    <style>
    .stApp {{
        background: {theme_colors['main-bg']};
        color: {theme_colors['text-color']};
    }}
    
    .main-header {{
        background: linear-gradient(90deg, {theme_colors['primary-color']}, {theme_colors['secondary-color']});
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }}
    
    .result-card {{
        background: {theme_colors['dark-bg']};
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid {theme_colors['primary-color']};
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }}
    
    .verdict-true {{
        background: {true_result_bg};
        border-left-color: {theme_colors['success-color']};
    }}
    
    .verdict-false {{
        background: {fake_result_bg};
        border-left-color: {theme_colors['danger-color']};
    }}
    
    .verdict-mixed {{
        background: {mixed_result_bg};
        border-left-color: {theme_colors['warning-color']};
    }}
    
    .metric-card {{
        background: {theme_colors['dark-bg']};
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid {theme_colors['card-bg-gradient-light']};
    }}
    
    .source-card {{
        background: {theme_colors['light-bg']};
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid {theme_colors['accent-color']};
    }}
    
    .stTextInput > div > div > input {{
        background-color: {theme_colors['dark-bg']};
        color: {theme_colors['text-color']};
        border: 1px solid {theme_colors['card-bg-gradient-light']};
    }}
    
    .stTextArea > div > div > textarea {{
        background-color: {theme_colors['dark-bg']};
        color: {theme_colors['text-color']};
        border: 1px solid {theme_colors['card-bg-gradient-light']};
    }}
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """Display the main header with branding."""
    st.markdown("""
    <div class="main-header">
        <h1>🔍 FactBot AI - Simplified Version</h1>
        <p>Your Intelligent Fact-Checking Assistant</p>
        <p><em>Simplified version without full CrewAI dependencies</em></p>
    </div>
    """, unsafe_allow_html=True)

def display_result_card(result: Dict[str, Any]):
    """Display the fact-checking result in a styled card."""
    verdict = result.get('final_verdict', 'Unknown')
    reasoning = result.get('reasoning', 'No reasoning provided')
    sources_verified = result.get('sources_verified', 0)
    execution_time = result.get('execution_time', 0)
    supporting_articles = result.get('supporting_articles', [])
    
    # Determine card style based on verdict
    if verdict.lower() in ['true', 'verified']:
        card_class = "result-card verdict-true"
        verdict_emoji = "✅"
    elif verdict.lower() in ['false', 'fake', 'misleading']:
        card_class = "result-card verdict-false"
        verdict_emoji = "❌"
    else:
        card_class = "result-card verdict-mixed"
        verdict_emoji = "⚠️"
    
    st.markdown(f"""
    <div class="{card_class}">
        <h2>{verdict_emoji} Final Verdict: {verdict}</h2>
        <h3>📝 Detailed Reasoning:</h3>
        <p>{reasoning}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Sources Verified</h3>
            <h2>{sources_verified}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⏱️ Execution Time</h3>
            <h2>{execution_time:.2f}s</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Display supporting articles
    if supporting_articles:
        st.markdown("### 📚 Supporting Articles")
        for i, article in enumerate(supporting_articles, 1):
            st.markdown(f"""
            <div class="source-card">
                <h4>📄 Source {i}: {article.get('title', 'No title')}</h4>
                <p>{article.get('snippet', 'No description available')}</p>
                <a href="{article.get('link', '#')}" target="_blank">🔗 Read Full Article</a>
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main application function."""
    apply_dark_theme()
    display_header()
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        st.markdown("""
        **Setup Instructions:**
        1. Get your [Gemini API Key](https://makersuite.google.com/app/apikey)
        2. Get your [Serper API Key](https://serper.dev)
        3. Add them to the `.env` file in this directory
        
        **Current Status:**
        """)
        
        # Check if API keys are configured
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        gemini_key = os.getenv('GEMINI_API_KEY')
        serper_key = os.getenv('SERPER_API_KEY')
        
        if gemini_key and gemini_key != 'your_gemini_api_key_here':
            st.success("✅ Gemini API Key: Configured")
        else:
            st.error("❌ Gemini API Key: Not configured")
            
        if serper_key and serper_key != 'your_serper_api_key_here':
            st.success("✅ Serper API Key: Configured")
        else:
            st.error("❌ Serper API Key: Not configured")
    
    # Main input area
    st.markdown("### 📝 Enter News Article or Topic to Fact-Check")
    
    input_text = st.text_area(
        "Paste your news article, headline, or topic here:",
        height=150,
        placeholder="Enter the news article, headline, or topic you want to fact-check..."
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔍 Start Fact-Checking", type="primary", use_container_width=True):
            if input_text.strip():
                if not st.session_state.is_processing:
                    st.session_state.is_processing = True
                    
                    with st.spinner("🔄 Analyzing and fact-checking..."):
                        try:
                            result = fact_check_crew(input_text.strip())
                            st.session_state.is_processing = False
                            
                            if result:
                                display_result_card(result)
                            else:
                                st.error("❌ Failed to get fact-checking results. Please try again.")
                                
                        except Exception as e:
                            st.session_state.is_processing = False
                            st.error(f"❌ An error occurred: {str(e)}")
                else:
                    st.warning("⏳ Fact-checking is already in progress. Please wait...")
            else:
                st.warning("⚠️ Please enter some text to fact-check.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #A0A0A0; padding: 1rem;">
        <p>🔍 FactBot AI - Simplified Version | Powered by Google Gemini & Serper API</p>
        <p><em>This is a simplified version that works without the full CrewAI framework</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()