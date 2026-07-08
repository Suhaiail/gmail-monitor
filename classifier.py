from google import genai
from google.genai import types
from pydantic import BaseModel
from config import GEMINI_API_KEY
 
client = genai.Client(api_key=GEMINI_API_KEY)


class Classification(BaseModel):
    category: str
    confidence: float
    notify: bool
    company: str
    summary: str
    action_required: str


PROMPT = """
You are my personal Gmail assistant.

Notify me ONLY if the email is about:

1. Interview invitation, confirmation or reschedule.
2. Placement drive.
3. Internship opportunity.
4. Online assessment / Coding test.
5. College deadlines.
6. Exams.
7. Assignment / DA submission.
8. FFCS / Registration / Fee payment.
9. Faculty study materials (PDF, PPT, Notes, Lab Manual, Question Bank, Previous Year Questions, Lecture Recording, Google Drive Links).
10. Useful hackathons with placement/resume value.

Ignore:

- Promotions
- Marketing
- Shopping
- Receipts
- Club events
- Cultural events
- Generic newsletters
- Generic webinars
- Spam

If unsure return:

uncertain_maybe_important

Categories:

interview
college_deadline
placement_company
exam
assignment_da
hackathon_useful
form_deadline
faculty_study_material
uncertain_maybe_important
unimportant_event
spam_or_promo
personal_other
"""


def classify(email):

    prompt = f"""
{PROMPT}

Subject:
{email['subject']}

From:
{email['from']}

Snippet:
{email['snippet']}

Body:
{email['body'][:3000]}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Classification,
        ),
    )

    return response.parsed
