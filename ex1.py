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
            {
                "role": "system",
                "content": "Estrai le informazioni dalla ricetta seguendo lo schema fornito.",
            },
            {"role": "user", "content": recipe_text},
        ],
        response_format=RecipeAnalysis,
    )
    return completion.choices[0].message.parsed


if __name__ == "__main__":

    ricetta_esempio = """
    Pasta alla Carbonara

    Difficoltà: Media
    Tempo di preparazione: 25 minuti
    Porzioni: 4

    Ingredienti:
    - 400g di spaghetti
    - 200g di guanciale
    - 4 uova intere
    - 100g di pecorino romano grattugiato
    - Pepe nero q.b.
    - Sale q.b.

    Procedimento:
    Cuocere la pasta in acqua salata. Nel frattempo rosolare il guanciale a cubetti
    in padella senza aggiungere grassi. In una ciotola sbattere le uova con il pecorino
    e abbondante pepe. Scolare la pasta al dente, mantecare fuori dal fuoco con il
    guanciale e il composto di uova. Servire subito.
    """

    print("Analisi ricetta in corso...\n")
    risultato = analyze_recipe(ricetta_esempio)

    print(f"Piatto:          {risultato.dish_name}")
    print(f"Difficoltà:      {risultato.difficulty}")
    print(f"Tempo prep:      {risultato.prep_time_minutes} minuti")
    print(f"Porzioni:        {risultato.servings}")
    print(f"\nIngredienti ({len(risultato.ingredients)}):")
    for ing in risultato.ingredients:
        print(f"  - {ing.name}: {ing.quantity}")