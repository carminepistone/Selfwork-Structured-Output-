import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o"


JOB_OFFER_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "job_offer",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "job_title": {"type": "string"},
                "company_name": {"type": "string"},
                "location": {"type": "string"},
                "contract_type": {"type": "string"},
                "required_skills": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["job_title", "company_name", "location", "contract_type", "required_skills"],
            "additionalProperties": False
        }
    }
}


def parse_job_offer(offer_text: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Estrai le informazioni dall'offerta di lavoro seguendo lo schema fornito."},
            {"role": "user", "content": offer_text},
        ],
        response_format=JOB_OFFER_SCHEMA,
    )
    return json.loads(response.choices[0].message.content)