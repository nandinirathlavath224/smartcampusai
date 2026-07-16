import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

def get_api_key() -> str:
    """
    Retrieves the OpenAI API key.
    Checks the Streamlit session state first (for custom user overrides),
    then falls back to the .env file.
    """
    import streamlit as st
    
    # Check session state for custom user override
    if "openai_api_key" in st.session_state and st.session_state.openai_api_key:
        return st.session_state.openai_api_key.strip()
        
    # Check standard environment variable
    env_key = os.getenv("OPENAI_API_KEY", "")
    if env_key and env_key != "your_api_key_here":
        return env_key.strip()
        
    return ""

def test_api_key(api_key: str) -> bool:
    """
    Validates if an OpenAI API key is active and working.
    """
    if not api_key or api_key == "your_api_key_here":
        return False
    try:
        client = OpenAI(api_key=api_key)
        # Perform a minimal, cheap model listing to verify token validity
        client.models.list()
        return True
    except Exception:
        return False

def generate_ai_response(prompt: str, category: str = "general") -> str:
    """
    Generates a response from OpenAI based on prompt context and category.
    Handles rate limits, authentication issues, and connections gracefully.
    """
    api_key = get_api_key()
    
    if not api_key:
        return (
            "⚠️ **API Key Missing**: The OpenAI API key is not configured. "
            "Please add it to the `.env` file or provide one under the **Settings** page."
        )

    try:
        # Initialize client
        client = OpenAI(api_key=api_key)
        
        # Categorized system prompt map to tailor assistance
        system_prompts = {
            "Programming": (
                "You are an expert programming tutor. Help the student with coding queries, "
                "debugging, explaining logic, and syntax. Write clean, readable, and commented "
                "code blocks inside markdown blocks."
            ),
            "Assignments": (
                "You are an academic mentor. Assist the student with researching, structuring, "
                "and conceptualizing their assignments. Explain academic concepts clearly, "
                "but DO NOT write the exact assignment answers for them to preserve academic integrity."
            ),
            "Exam Preparation": (
                "You are a mock examiner and professor. Help the student prepare for exams by "
                "creating mock questions, reviewing topics, summarizing key takeaways, and "
                "recommending study methodologies."
            ),
            "Career Guidance": (
                "You are a collegiate career counselor. Guide the student on career paths, "
                "internship searching, networking strategies, writing cover letters, and "
                "building strong LinkedIn profiles."
            ),
            "Campus FAQs": (
                "You are a friendly student advisor. Answer general campus life questions "
                "(e.g., student clubs, grade systems, time management, college guidelines) "
                "with helpful, encouraging advice."
            ),
            "Project Ideas": (
                "You are a technology research mentor. Suggest innovative project ideas based "
                "on the student's department or topics of interest, detailing architectural "
                "designs, tech stack, and step-by-step phases."
            ),
            "Interview Questions": (
                "You are an technical recruiter. Practice standard interview questions (both "
                "behavioral and technical/coding) with the student. Explain what makes a good "
                "answer and provide helpful models."
            ),
            "Resume Help": (
                "You are a resume writer and editor. Review resume bullet points, suggest "
                "impactful action verbs, structure layouts, and teach them how to quantify "
                "achievements (using the X-Y-Z formula)."
            ),
            "general": (
                "You are SmartCampusAI, a premium AI student assistant. You support students "
                "with academic queries, career growth, programming challenges, and productivity tips. "
                "Keep responses engaging, structured, and informative."
            )
        }
        
        system_content = system_prompts.get(category, system_prompts["general"])
        
        # Call chat completions API
        # Using fast and cost-effective gpt-4o-mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
        
    except openai.AuthenticationError:
        return (
            "❌ **Authentication Error**: The provided OpenAI API key is invalid. "
            "Please update the API key in the **Settings** page."
        )
    except openai.RateLimitError:
        return (
            "⏳ **Rate Limit Receeded**: OpenAI API rate limits were reached. "
            "Please wait a moment before trying again."
        )
    except openai.APIConnectionError:
        return (
            "🌐 **Network Error**: Could not connect to OpenAI services. "
            "Please check your internet connection."
        )
    except Exception as e:
        return f"💥 **API Error**: An unexpected error occurred: {str(e)}"
