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
                    "items": {"type": "string"},
                },
            },
            "required": [
                "job_title",
                "company_name",
                "location",
                "contract_type",
                "required_skills",
            ],
            "additionalProperties": False,
        },
    },
}


def parse_job_offer(offer_text: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Estrai le informazioni dall'offerta di lavoro seguendo lo schema fornito.",
            },
            {"role": "user", "content": offer_text},
        ],
        response_format=JOB_OFFER_SCHEMA,
    )
    return json.loads(response.choices[0].message.content)



if __name__ == "__main__":

    offerta_esempio = """
    Offerta di lavoro - Backend Developer

    Azienda: TechCorp Srl
    Sede: Milano, con possibilità di smart working parziale
    Contratto: Tempo indeterminato

    Cerchiamo un Backend Developer con esperienza in:
    - Python (FastAPI o Django)
    - PostgreSQL e Redis
    - Docker e Kubernetes
    - Architetture REST e microservizi
    - Conoscenza di Git e CI/CD

    Costituisce titolo preferenziale esperienza con AWS o GCP.
    Offriamo RAL competitiva, ticket restaurant e formazione continua.
    """

    print("Parsing offerta di lavoro in corso...\n")
    risultato = parse_job_offer(offerta_esempio)

    print(f"Titolo:          {risultato['job_title']}")
    print(f"Azienda:         {risultato['company_name']}")
    print(f"Sede:            {risultato['location']}")
    print(f"Contratto:       {risultato['contract_type']}")
    print(f"\nCompetenze richieste ({len(risultato['required_skills'])}):")
    for skill in risultato["required_skills"]:
        print(f"  - {skill}")

    print("\n--- JSON grezzo restituito dall'LLM ---")
    print(json.dumps(risultato, indent=2, ensure_ascii=False))