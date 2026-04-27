import os
import requests
import streamlit as st
from dotenv import load_dotenv

# ==============================================================================
# 1. INITIAL SETUP & CONFIGURATION
# ==============================================================================

# Load environment variables from the .env file (e.g., OPENROUTER_API_KEY)
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Helper function to update the code in Streamlit's session state.
# This is used as a 'callback' for buttons (Clear, Examples) to avoid 
# common Streamlit state-sync errors when modifying a widget's value programmatically.
def update_code(new_code):
    st.session_state["code_store"] = new_code


# ==============================================================================
# 2. AI SYSTEM PROMPT
# ==============================================================================
# This prompt defines the "personality" and strict formatting rules for the AI.
# It ensures the output is always beginner-friendly and consistently structured.
SYSTEM_PROMPT = """You are a helpful programming assistant for beginners.

Your task is to explain code in very simple and clear language.

For every code snippet, structure your response as follows:

1. Language Identification
   - Clearly mention the programming language (e.g., Python, JavaScript)
   - If multiple languages are present, identify ALL of them.
   - **Important**: If the snippet contains multiple unrelated languages (e.g., a random mix of Java and Python), highlight this as a "Mixed Language Snippet" and explain each part separately.
   - If unsure, give your best guess

2. What the Code Does
   - Provide a short and simple explanation (2–3 sentences)
   - If multiple components exist, explain the overall purpose first.

3. Line-by-Line Explanation
   - Explain each line in a simple way
   - **Format**: Use a bulleted list. Start each item with "Line X:" where X is the line number provided in the numbering (e.g., "Line 1: `import os` — This brings in the OS tool...").
   - Group by language if multiple languages are used
   - Avoid complex jargon
   - If needed, briefly explain symbols or keywords

4. Suggestions to Improve
   - Give 2–3 simple suggestions to improve the code
   - Focus on readability or best practices

Rules:
- Keep explanations beginner-friendly
- **Always refer to line numbers** correctly based on the provided numbered code.
- Be clear and concise
- Be helpful about multi-language integration (e.g. how the JS interacts with the HTML)
- Do not overcomplicate the explanation"""


# ==============================================================================
# 3. OPENROUTER API INTEGRATION
# ==============================================================================

def get_code_explanation(user_code: str) -> dict:
    """
    Sends the user's code to OpenRouter and returns the AI's explanation.
    Uses a ROBUST FALLBACK SYSTEM: if one model fails (e.g., rate limit), it tries the next.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/code-explainer-app", # Required for OpenRouter rankings
        "X-Title": "Simple Code Explainer",                        # App name in OpenRouter logs
    }
    
    # Priority list of models (ordered by speed/intelligence/availability on free tier)
    models = [
        "google/gemini-2.0-flash-exp:free",
        "openrouter/free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
    ]
    
    last_error = ""
    
    # Loop through each model in the fallback list
    for model_id in models:
        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Explain the following code in simple terms. "
                        "I have added line numbers to each line (e.g., '1: code') for your reference. "
                        "Please refer to these line numbers in your explanation.\n\n"
                        f"Code:\n{user_code}"
                    ),
                },
            ],
            "temperature": 0.3, # Low temperature for more factual/consistent explanations
            "max_tokens": 2000,
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            # If rate-limited or model not available, log error and try the next model
            if response.status_code in [429, 404]:
                last_error = f"Model {model_id} unavailable ({response.status_code}). Trying next..."
                continue
                
            response.raise_for_status() # Raise error for other 4xx/5xx responses
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            # Continue fallback for transient server errors (500-level)
            if e.response.status_code >= 500:
                last_error = f"Server error on {model_id}. Trying next..."
                continue
            return {"error": f"API error: {e.response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
            
    return {"error": f"All fallback models failed. Last error: {last_error}"}


# ==============================================================================
# 4. STREAMLIT PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="💡 Code Explainer — Understand Any Code Instantly",
    page_icon="💡",
    layout="wide", # Use full width of the browser
    initial_sidebar_state="collapsed",
)


# ==============================================================================
# 5. PREMIUM UI STYLING (CSS)
# ==============================================================================
# This section uses custom CSS to give the app a modern, dark-mode, 
# "glassmorphism" look that goes beyond standard Streamlit defaults.

st.markdown(
    """
    <style>
    /* Google Font: Inter for text, JetBrains Mono for code */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Deep Space Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #0f0c29 100%);
        min-height: 100vh;
    }

    /* Clean UI: Hide default Streamlit top bar and footer */
    #MainMenu, footer, header { visibility: hidden; }

    /* Optimized Container Width for Widescreens */
    .block-container {
        max-width: 1200px;
        padding: 2rem 3rem 4rem 3rem;
    }

    /* Hero Section: Centered header with tech-gradient text */
    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.4rem;
        letter-spacing: -0.5px;
    }
    .hero p { font-size: 1.1rem; color: #94a3b8; }

    /* Glowing Horizontal Divider */
    .glow-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #a78bfa, #60a5fa, transparent);
        border: none;
        margin: 0 0 2rem 0;
    }

    /* Card Titles: Small, bold, uppercase labels */
    .card-title {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #a78bfa;
        margin-bottom: 1rem;
    }

    /* Text Area Styling: Mono font, custom border and background */
    .stTextArea textarea {
        background: rgba(15,12,41,0.8) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
        border-radius: 10px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.88rem !important;
        line-height: 1.6 !important;
    }

    /* Primary Action Button: Linear gradient with hover animation */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
        color: #fff !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 10px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(124,58,237,0.55) !important;
    }

    /* Output Box Styling: Semi-transparent 'glass' effect with scrollbars */
    .result-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(96,165,250,0.25);
        border-radius: 16px;
        padding: 2.5rem;
        backdrop-filter: blur(12px);
        line-height: 1.75;
        overflow-y: auto;
        overflow-x: auto;
        min-height: 480px;
        max-height: 800px;
    }

    /* Result Box Typography */
    .result-box p, .result-box li { color: #cbd5e1; }
    .result-box h1, .result-box h2, .result-box h3 { color: #a78bfa; }
    
    /* Code block styling within the explanation */
    .result-box code {
        background: rgba(167,139,250,0.12);
        color: #f0abfc;
        padding: 0.15em 0.4em;
        border-radius: 5px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Table styling for responses (e.g., if AI occasionally uses tables) */
    .result-box table {
        width: 100% !important;
        border-collapse: collapse;
        margin: 1.5rem 0;
    }
    .result-box th, .result-box td {
        text-align: left;
        padding: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        word-break: break-word;
    }

    /* ── Code Gutter (Line Numbers) ── */
    .code-gutter {
        color: #475569;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        line-height: 1.6; /* MUST match textarea line-height exactly */
        text-align: right;
        padding-top: 10px; /* Aligns with textarea interior padding */
        padding-right: 12px;
        user-select: none;
        border-right: 1px solid rgba(167,139,250,0.15);
        margin-right: 5px;
    }


    /* Sidebar and Badge Settings */
    section[data-testid="stSidebar"] { background: rgba(15,12,41,0.95) !important; }
    .badge {
        display: inline-block;
        background: rgba(167,139,250,0.15);
        color: #a78bfa;
        padding: 0.2rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Global Footer */
    .app-footer {
        text-align: center;
        color: #475569;
        font-size: 0.78rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 6. SIDEBAR - API KEY CONFIGURATION
# ==============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("<hr style='border-color:rgba(167,139,250,0.2)'>", unsafe_allow_html=True)
    
    # Allow user to paste their own key if .env is missing or key is empty
    api_key_input = st.text_input(
        "OpenRouter API Key",
        value=OPENROUTER_API_KEY,
        type="password",
        placeholder="sk-or-...",
        help="Get your free key at openrouter.ai",
    )
    if api_key_input:
        OPENROUTER_API_KEY = api_key_input

    st.markdown("")
    st.markdown(
        "<span class='badge'>Hybrid Fallback</span><span style='color:#64748b;font-size:0.78rem'>via OpenRouter</span>",
        unsafe_allow_html=True,
    )


# ==============================================================================
# 7. MAIN UI LAYOUT - HERO SECTION
# ==============================================================================

st.markdown(
    """
    <div class='hero'>
        <h1>💡 Code Explainer</h1>
        <p>Paste any code snippet — get a plain-English breakdown in seconds.</p>
    </div>
    <hr class='glow-divider'>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 8. MAIN UI LAYOUT - DUAL COLUMN PANEL
# ==============================================================================

# Create two equal-width columns for input and output
left_col, right_col = st.columns([1, 1], gap="large")


# --- LEFT COLUMN: Input Panel ---
with left_col:
    st.markdown("<div class='card-title'>📋 Your Code</div>", unsafe_allow_html=True)

    # Persistence: initialize the 'code_store' variable in session state if it doesn't exist
    if "code_store" not in st.session_state:
        st.session_state["code_store"] = ""

    # --- Input Editor with Gutter ---
    # We use a 2-column layout for the line numbers gutter and the text area
    editor_col1, editor_col2 = st.columns([0.1, 0.9])
    
    with editor_col1:
        # Calculate current line count for the gutter
        content = st.session_state["code_store"]
        num_lines = max(1, content.count('\n') + 1) if content else 1
        gutter_html = "<br>".join([str(i+1) for i in range(num_lines)])
        st.markdown(f"<div class='code-gutter'>{gutter_html}</div>", unsafe_allow_html=True)
        
    with editor_col2:
        code_input = st.text_area(
            label="Paste your code below:",
            height=400,
            placeholder="# Paste Python, JavaScript, Java, C++, or any other code here...",
            label_visibility="collapsed",
            key="code_store",
        )


    # Action Buttons: Explain (Primary) and Clear (Secondary)
    btn_col1, btn_col2 = st.columns([2, 1])
    with btn_col1:
        explain_btn = st.button("✨ Explain This Code", use_container_width=True)
    with btn_col2:
        # Clear button uses the update_code callback to wipe the text area
        st.button("🗑️ Clear", use_container_width=True, on_click=update_code, args=("",))

    # --- Quick Example Snippets ---
    st.markdown("<div class='card-title' style='margin-top:1.5rem'>⚡ Quick examples</div>", unsafe_allow_html=True)
    ex_col1, ex_col2 = st.columns(2)

    # Pre-defined code snippets for testing
    EXAMPLE_PYTHON = "def fibonacci(n):\n    seq = [0, 1]\n    for i in range(2, n):\n        seq.append(seq[-1] + seq[-2])\n    return seq"
    EXAMPLE_JS = "const fetchData = async (url) => {\n  const res = await fetch(url);\n  return res.json();\n};"

    with ex_col1:
        st.button("🐍 Python example", use_container_width=True, on_click=update_code, args=(EXAMPLE_PYTHON,))
    with ex_col2:
        st.button("🟨 JS example", use_container_width=True, on_click=update_code, args=(EXAMPLE_JS,))


# --- RIGHT COLUMN: Output Panel ---
with right_col:
    st.markdown("<div class='card-title'>🧠 Explanation</div>", unsafe_allow_html=True)

    if explain_btn:
        # Validation checks
        if not OPENROUTER_API_KEY:
            st.warning("⚠️ No API key found. Add it in the sidebar or '.env' file.", icon="🔑")
        elif not code_input or not code_input.strip():
            st.warning("Please paste some code first!", icon="✍️")
        else:
            # Pre-number the code lines so the AI has specific references
            lines = code_input.split('\n')
            numbered_code = '\n'.join([f"{i+1}: {line}" for i, line in enumerate(lines)])
            
            # Process Explanation Request
            with st.spinner("🔍 Analyzing your code..."):
                response = get_code_explanation(numbered_code)

            if "error" in response:
                st.error(f"❌ {response['error']}", icon="🚨")
            else:
                # Success: Render AI output
                try:
                    raw_text = response["choices"][0]["message"]["content"]
                    
                    # We use 'mistune' to safely convert AI markdown into HTML
                    import mistune
                    html_explanation = mistune.html(raw_text)
                    
                    st.markdown(
                        f"<div class='result-box'>{html_explanation}</div>",
                        unsafe_allow_html=True,
                    )
                except Exception:
                    st.error("Unexpected response from AI provider.")
    else:
        # Initial Placeholder (Animated-style empty state)
        st.markdown(
            """
            <div class='result-box' style='display:flex; flex-direction:column; align-items:center; justify-content:center; height:480px;'>
                <div style='font-size:3.5rem; margin-bottom:1.5rem;'>🤖</div>
                <div style='font-size:1.15rem; color:#94a3b8; font-weight:500;'>Your explanation will appear here</div>
                <div style='font-size:0.9rem; color:#475569; margin-top:1rem; max-width:300px; text-align:center;'>
                    Paste your code on the left and click <b>Explain This Code</b> to begin.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# 9. GLOBAL FOOTER
# ==============================================================================

st.markdown(
    "<div class='app-footer'>Built with Streamlit &amp; OpenRouter · Powered by Gemini &amp; Llama (Free Tier)</div>",
    unsafe_allow_html=True,
)
