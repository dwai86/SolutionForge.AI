from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()

#GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# --------------------------------------------------
# Groq - Primary
# --------------------------------------------------
"""
groq_llm = None

if GROQ_API_KEY:
    try:
        groq_llm = LLM(
            model="groq/openai/gpt-oss-120b",
            api_key=GROQ_API_KEY,
            temperature=0.2
        )
    except Exception as e:
        print(f"WARNING: Failed to initialize Groq LLM: {e}")
"""

# --------------------------------------------------
# OpenRouter - Fallback
# --------------------------------------------------

openrouter_llm = None

if OPENROUTER_API_KEY:
    try:
        openrouter_llm = LLM(
            model="openrouter/nvidia/nemotron-3-super-120b-a12b:free",
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.2
        )
    except Exception as e:
        print(f"WARNING: Failed to initialize OpenRouter LLM: {e}")


# --------------------------------------------------
# Select LLM
# --------------------------------------------------
"""
if groq_llm:
    llm = groq_llm
    print("Using Groq as primary LLM")
    """

if openrouter_llm:
    llm = openrouter_llm
    print("Using OpenRouter for LLM")

else:
    raise RuntimeError(
        "No LLM provider is available. "
        "Configure OPENROUTER_API_KEY."
    )