import os
from dotenv import load_dotenv

load_dotenv()

# ===========================
# API KEYS
# ===========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GREEN_API_URL = os.getenv("GREEN_API_URL")
GREEN_API_ID = os.getenv("GREEN_API_ID_INSTANCE")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN_INSTANCE")

# ===========================
# USER SETTINGS
# ===========================

PHONE_NUMBER = "919573338048"

# Gmail query
# Ignore Promotions & Social
# Only unread emails from last 2 days

GMAIL_QUERY = "is:unread"

MAX_RESULTS = 2

# ===========================
# GOOGLE SCOPES
# ===========================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

# ===========================
# IMPORTANT CATEGORIES
# ===========================

IMPORTANT_CATEGORIES = {
    "interview",
    "college_deadline",
    "placement_company",
    "exam",
    "assignment_da",
    "hackathon_useful",
    "form_deadline",
    "faculty_study_material",
    "uncertain_maybe_important",
}

# ===========================
# STATE SETTINGS
# ===========================

STATE_FILE = "work/gmail-alert-state.json"

STATE_RETENTION_DAYS = 30

# ===========================
# WHATSAPP RETRY
# ===========================

MAX_RETRIES = 3

RETRY_DELAYS = [5, 10, 20]