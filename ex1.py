import os
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o"


class Ingredient(BaseModel):
    name: str
    quantity: str

class RecipeAnalysis(BaseModel):
    dish_name: str
    difficulty: str
    prep_time_minutes: int
    servings: int
    ingredients: list[Ingredient]


def analyze_recipe(recipe_text: str) -> RecipeAnalysis:
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Estrai le informazioni dalla ricetta seguendo lo schema fornito."},
            {"role": "user", "content": recipe_text},
        ],
        response_format=RecipeAnalysis,
    )
    return completion.choices[0].message.parsed