import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Prompt Enhancer", layout="centered")
st.title("🔧 Prompt Enhancer for AI")

st.markdown(
    """
    Enter **Role**, **Context**, and **Task** – I'll turn it into a powerful AI prompt.
    - No OpenAI API key is stored: it is only used for your session.
    """
)

# User input for API key
api_key = st.text_input("🔑 OpenAI API Key", type="password")

# User prompt details
role = st.text_input("🧑‍💼 Role of the AI Assistant", placeholder="e.g., Career Coach")
context = st.text_area("📄 Context", placeholder="e.g., A college student seeking career advice.")
task = st.text_area("🎯 Task", placeholder="e.g., Suggest three career options with rationale.")

# Enhanced prompt variable for output
enhanced_prompt = ""

if st.button("Generate Enhanced Prompt"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not role or not context or not task:
        st.warning("Please complete all fields.")
    else:
        client = OpenAI(api_key=api_key)

        base_input = f"""You are an AI prompt engineer. Convert the following into a powerful GPT-style prompt.

ROLE:
{role}

CONTEXT:
{context}

TASK:
{task}

Instructions:
- Specify the assistant's role clearly.
- Ask the model to clarify assumptions before responding.
- Include a preferred answer format (e.g., bullets, table, step-by-step).

Return only the enhanced prompt. Do NOT add explanation.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": base_input}
                ],
                temperature=0.7,
                max_tokens=500
            )
            enhanced_prompt = response.choices[0].message.content

            st.subheader("📝 Enhanced Prompt")
            st.text_area(
                "Your Enhanced Prompt",
                value=enhanced_prompt,
                height=350,  # You can increase this value if you want a bigger box
                key="enhanced_prompt_output"
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Optional: Simple tip for copying
if enhanced_prompt:
    st.info("Tip: Click into the box above, press Ctrl+A to select all, then Ctrl+C to copy!")

