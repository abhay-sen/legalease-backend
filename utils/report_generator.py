from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def generate_legal_report(text: str):
    prompt = f"""
You're an AI legal assistant. Given the following legal document text, extract and summarize:

1. Summary of document  
2. Key parties involved  
3. Important dates  
4. Type of document  
5. Major clauses  
6. Signatories  

Only return a JSON object structured like:  
{{
  "summary": "...",
  "parties": [...],
  "important_dates": [...],
  "document_type": "...",
  "clauses": [{{"title": "...", "text": "..."}}],
  "signatories": [...]
}}

Document:
{text}
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Or "gpt-3.5-turbo" to save cost
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return completion.choices[0].message.content
