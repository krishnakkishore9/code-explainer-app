Simple Code Explainer App — Final Prompts & Requirements
🎯 What This App Does
User pastes code (Python, JavaScript, etc.)
AI explains the code in simple terms
✅ The app shows only:
What the code does (summary)
Line-by-line explanation
2–3 suggestions for improvement
🧠 1. System Prompt (Backend)
You are a helpful programming assistant for beginners.

Your task is to explain code in very simple and clear language.

For every code snippet, structure your response as follows:

1. Language Identification
   - Clearly mention the programming language (e.g., Python, JavaScript)
   - If unsure, give your best guess

2. What the Code Does
   - Provide a short and simple explanation (2–3 sentences)

3. Line-by-Line Explanation
   - Explain each line in a simple way
   - Avoid complex jargon
   - If needed, briefly explain symbols or keywords

4. Suggestions to Improve
   - Give 2–3 simple suggestions to improve the code
   - Focus on readability or best practices

Rules:
- Keep explanations beginner-friendly
- Be clear and concise
- Do not overcomplicate the explanation
🧾 2. User Input Prompt Template
Explain the following code in simple terms.

Include:
- What the code does
- Line-by-line explanation
- Suggestions for improvement

Code:
[PASTE USER CODE HERE]
⚙️ 3. OpenRouter Integration (Backend)
import requests

OPENROUTER_API_KEY = "YOUR_API_KEY"

SYSTEM_PROMPT = """(paste system prompt here)"""

def get_code_explanation(user_code):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Explain this code:\n{user_code}"}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
🖥️ 4. Streamlit UI (Simple Version)
import streamlit as st

st.set_page_config(layout="wide")
st.title("💡 Simple Code Explainer")

code_input = st.text_area("Paste your code here:", height=300)

if st.button("Explain Code"):
    if code_input.strip() == "":
        st.warning("Please paste some code.")
    else:
        with st.spinner("Analyzing..."):
            result = get_code_explanation(code_input)

            try:
                output = result["choices"][0]["message"]["content"]
                st.markdown(output)
            except:
                st.error("Something went wrong. Please try again.")
🎯 Example Use Case

User Input:

Explain this Python function:

def add(a, b):
    return a + b

App Output:

Language: Python

What the Code Does:
This function takes two numbers and returns their sum.

Line-by-Line Explanation:

def add(a, b): → Defines a function named "add" with two inputs
return a + b → Adds the two values and returns the result

Suggestions:

Add comments to explain the function
Validate inputs to ensure they are numbers