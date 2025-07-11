from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import shutil
import os

from utils.pdfutils import extract_text_from_pdf
from utils.report_generator import generate_legal_report
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use exact origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class PDFLinkRequest(BaseModel):
    url: str

@app.post("/process-pdf-url/")
async def process_pdf_url(req: PDFLinkRequest):
    temp_path = "temp_supabase_download.pdf"

    try:
        # Download the file from Supabase URL
        with requests.get(req.url, stream=True) as r:
            if r.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to download file from URL")
            with open(temp_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        
        # Extract text
        text = extract_text_from_pdf(temp_path)
        os.remove(temp_path)

        

        report = generate_legal_report(text)

        return {
            "report": report
        }

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))
