import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()
API_KEY = os.getenv("gemini_api_key")

# 2. Configure the AI Model
if API_KEY:
    genai.configure(api_key=API_KEY)
    # Using Gemini 1.5 Flash for fast, high-quality text generation
    model = genai.GenerativeModel('gemini-3.1-flash-lite') 
else:
    st.error("API Key not found. Please check your .env file.")

# 3. Define the Meta-Prompt (The Agentic System Instruction)
def generate_prompt(user_words, style):
    system_instruction = f"""
    You are an expert AI Prompt Engineer. Your job is to take simple keywords provided by the user 
    and expand them into a highly detailed, professional prompt.
    
    CRITICAL RULE - TARGET STYLE: [{style}]
    You MUST strictly adapt the user's keywords to fit this exact Target Style. 
    Do not default to a generic image or story if it does not fit the style. 
    
    Example: If the keywords are "dog in space" and the Target Style is "Professional Business Analyst", 
    you must output a prompt asking for a market analysis of the orbital pet industry, a case study on canine aerospace logistics, or a business plan for zero-gravity dog food.
    
    Ensure the output is ONLY the engineered prompt itself, ready to be copied and pasted. 
    Do not include introductory or concluding phrases like 'Here is your prompt'.
    """
    
    full_query = f"{system_instruction}\n\nUser Keywords: {user_words}"
    
    try:
        response = model.generate_content(full_query)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# 4. Streamlit UI Layout
st.set_page_config(page_title="Prompt Generator", page_icon="🤖", layout="centered")

st.title("🤖 Prompt Generator")
st.markdown("Transform your simple ideas into professional-grade prompts.")

# Sidebar for options
with st.sidebar:
    st.header("Generation Options")
    prompt_style = st.selectbox(
        "Choose the Output type:",
        ["Cinematic Image (Midjourney style)", 
         "Technical Code Instructor", 
         "Creative Storyteller", 
         "Professional Business Analyst"]
    )
    st.markdown("---")
    

# Main interface
user_input = st.text_input("Enter simple words:", placeholder="e.g., 'dog in space' or 'python script for data cleaning'")

# Generate Button
if st.button("Generate Enhanced Prompt", type="primary"):
    if user_input:
        with st.spinner("Engineering your prompt..."):
            # Call the function
            result = generate_prompt(user_input, prompt_style)
            
            # Display results
            st.success("Prompt Engineered Successfully!")
            st.text_area("Copy and paste this into your target AI:", value=result, height=200)
    else:
        st.warning("Please enter some keywords first!")