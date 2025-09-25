from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import random
import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ssl

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Cashifygcmart API",
    description="Gift Card Exchange Platform API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
db_client = None
db = None

# Pydantic models
class GiftCard(BaseModel):
    brand: str
    value: str
    condition: str
    hasReceipt: str
    cardType: str
    digitalCode: Optional[str] = ""
    digitalPin: Optional[str] = ""
    frontImage: Optional[dict] = None
    backImage: Optional[dict] = None
    receiptImage: Optional[dict] = None

class GiftCardSubmission(BaseModel):
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    cards: List[GiftCard]
    paymentMethod: str
    paypalAddress: Optional[str] = ""
    zelleDetails: Optional[str] = ""
    cashAppTag: Optional[str] = ""
    btcAddress: Optional[str] = ""
    chimeDetails: Optional[str] = 
  ""# Email Template Functions
def generate_confirmation_email_html(customer_name, reference_number):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You for Your Submission</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333333;
            background-color: #f5f7fa;
            padding: 20px 0;
        }}
        .email-container {{
            max-width: 650px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
            color: white;
            padding: 35px 30px;
            text-align: center;
        }}
        .logo {{
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 8px;
        }}
        .tagline {{
            font-size: 12px;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 20px;
        }}
        .header-title {{
            font-size: 24px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="logo">Cashifygcmart</div>
            <div class="tagline">Instant Offers, Same-Day Payments</div>
            <div class="header-title">Thank You for Your Submission</div>
        </div>
        
        <div class="content">
            <div class="greeting">Thank You for Your Submission, {customer_name}</div>
            <div class="reference">Reference Number: {reference_number}</div>
            
            <div class="intro-text">
                Thank you for submitting your gift card details to Cashifygcmart. Below is an update on the current status of your submission.
            </div>
        </div>
    </div>
</body>
</html>
    """
  # API Router
api_router = APIRouter(prefix="/api")

@api_router.get("/")
async def root():
    return {"message": "Cashifygcmart API is running"}

@api_router.post("/submit-gift-card")
async def submit_gift_card(submission: GiftCardSubmission):
    try:
        # Generate reference number
        timestamp = datetime.now().strftime("%H%M%S")
        random_num = random.randint(10, 99)
        reference_number = f"GC-{timestamp}-{random_num}"
        
        return {
            "success": True,
            "reference_number": reference_number,
            "message": "Gift card submission received successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Submission failed: {str(e)}"
        }

# Include API router
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
  
