import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Switched from OPENAI_API_KEY to GOOGLE_API_KEY ---
# Ensure your .env file has GOOGLE_API_KEY="your_gemini_api_key"
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def generate_legal_report_with_gemini(text: str):
    """
    Generates a structured legal report from text using the Gemini API.

    Args:
        text: The raw text of the legal document.

    Returns:
        A string containing the structured JSON report.
    """
    # --- Model switched to a Gemini model ---
    # gemini-1.5-flash is a great, fast alternative to gpt-4o-mini
    model = genai.GenerativeModel('gemini-1.5-flash')

    # The prompt is the same, instructing the model on its role and desired output.
    prompt = f"""
You are an AI legal assistant. Based on the legal document text provided below, please extract and summarize the key information.

Your task is to identify:
1.  A concise summary of the document.
2.  All key parties involved.
3.  Any important dates mentioned (e.g., effective date, termination date).
4.  The specific type of the document.
5.  The major clauses and their meanings.
6.  The names of the signatories.

Please format your response as a single, valid JSON object with the following structure:
{{
  "summary": "...",
  "parties": [...],
  "important_dates": [...],
  "document_type": "...",
  "clauses": [
    {{
      "title": "...",
      "text": "..."
    }}
  ],
  "signatories": [...]
}}

Legal Document Text:
---
{text}
---
    """

    # --- Using Gemini's dedicated JSON mode for reliable output ---
    # This is more robust than relying on the prompt alone.
    generation_config = genai.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.3
    )

    # --- API call changed to the Gemini SDK format ---
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    # The response text will be a clean JSON string.
    return response.text

