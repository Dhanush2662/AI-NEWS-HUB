import torch
import gradio as gr
from newspaper import Article
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ===================================================
# ✅ MODEL & TOKENIZER LOADING
# ===================================================
model_name = "distilbert-base-uncased"  # Replace with fine-tuned model path if saved locally
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

device = torch.device("cpu")  # Force CPU for compatibility
model.to(device)

# ===================================================
# ✅ LABEL MAP
# ===================================================
reverse_label_map = {
    0: "🟥 Left – Liberal / Progressive",
    1: "⚪ Center – Neutral / Balanced",
    2: "🟦 Right – Conservative"
}

# ===================================================
# ✅ FUNCTIONS
# ===================================================
def classify_bias_text(headline: str) -> str:
    inputs = tokenizer(headline, return_tensors="pt", padding=True, truncation=True, max_length=256).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    prediction = outputs.logits.argmax(dim=1).item()
    return reverse_label_map[prediction]

def classify_bias_from_url(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        headline_or_text = article.title if article.title else article.text[:300]
        if not headline_or_text:
            return "⚠️ Could not extract text from this link."
        return classify_bias_text(headline_or_text)
    except Exception as e:
        return f"⚠️ Error fetching article: {str(e)}"

# ===================================================
# ✅ EXAMPLES
# ===================================================
examples = [
    ["Government announces sweeping climate change policy"],
    ["Opposition criticizes tax cuts for the wealthy"],
    ["Supreme Court delivers verdict on voting rights case"],
    ["Market reacts to President's new economic reforms"]
]

# ===================================================
# ✅ LIQUID GLASS + THEME ADAPTIVE CSS
# ===================================================
custom_css = """
/* 🌗 Theme-aware styling */
@media (prefers-color-scheme: dark) {
  body {
    background: #121212 url('https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0') no-repeat center center fixed;
    background-size: cover;
    color: white;
  }
  h1, h3, p, label { color: white !important; }
}

@media (prefers-color-scheme: light) {
  body {
    background: #f4f4f4 url('https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0') no-repeat center center fixed;
    background-size: cover;
    color: black;
  }
  h1, h3, p, label { color: black !important; }
}

/* ✨ Liquid Glass Panels */
.gr-block.gr-box {
    background: rgba(255, 255, 255, 0.25) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(12px) saturate(180%);
    -webkit-backdrop-filter: blur(12px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    transition: all 0.3s ease-in-out;
}

/* 🖋️ Headings & Paragraphs */
h1 {
    font-size: 48px !important;
    font-weight: bold;
    margin-bottom: 8px;
}
h3 {
    font-size: 22px !important;
    opacity: 0.85;
}
"""

# ===================================================
# ✅ GRADIO UI
# ===================================================
with gr.Blocks(css=custom_css) as demo:
    gr.HTML("""
        <div style="text-align:center; padding: 30px 0;">
            <h1>📰 NewsMind</h1>
            <h3>Political Bias Classifier for News Headlines & Articles</h3>
            <p style="margin-top: 10px;">
                🟥 <b style='color:#ff6b6b;'>Left</b> – Liberal / Progressive |
                ⚪ <b style='color:#f1f1f1;'>Center</b> – Neutral / Balanced |
                🟦 <b style='color:#5dade2;'>Right</b> – Conservative
            </p>
            <p style="font-size: 14px; opacity: 0.8;">
                Type a headline or paste a news article link to see the predicted bias.
            </p>
        </div>
    """)

    with gr.Tab("📝 Headline Input"):
        headline_input = gr.Textbox(label="Enter a News Headline", placeholder="Type or paste a headline here...", lines=2)
        predict_btn_text = gr.Button("🔍 Classify Headline Bias", variant="primary")
        output_text = gr.Label(label="Predicted Political Leaning")
        gr.Examples(examples, inputs=headline_input)
        predict_btn_text.click(classify_bias_text, inputs=headline_input, outputs=output_text)

    with gr.Tab("🌐 URL Input"):
        url_input = gr.Textbox(label="Paste a News Article URL", placeholder="https://example.com/news-article")
        predict_btn_url = gr.Button("🔗 Fetch & Classify Bias", variant="secondary")
        output_url = gr.Label(label="Predicted Political Leaning")
        predict_btn_url.click(classify_bias_from_url, inputs=url_input, outputs=output_url)

# ===================================================
# ✅ LAUNCH APP
# ===================================================
if __name__ == "__main__":
    demo.launch(share=True)
