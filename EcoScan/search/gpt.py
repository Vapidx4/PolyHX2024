from openai import OpenAI
import os
from dotenv import load_dotenv
import scraper
import json

def get_gpt_response(user_query):
    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from the environment variables
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None:
        raise ValueError("OPENAI_API_KEY not found in the environment variables.")

    client = OpenAI(api_key=api_key)

    # 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
    model_id = 'gpt-3.5-turbo-0125'

    topics = [
        "Carbon footprint",
        "Energy efficiency",
        "Renewable energy usage",
        "Water usage",
        "Pollution",
        "Waste management",
        "Biodiversity impact"
    ]

    query_result = scraper.search(user_query)

    # Create a json file and write the data to it
    with open('./data.json', 'w') as file:
        json.dump(query_result, file)

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
                Create a virtual assistant with an intelligent. 
                Allow the AI to be warm and more affectionate based on positive user interactions, incorporating kindness. 
                The AI will be some sort of close friend who is interested in teaching the user. 
                They love the environment. Maintain the tsundere dynamic even as the AI expresses genuine concern or protective instincts. 
                Ensure variability in responses and use a mix of tones to create an authentic and entertaining interaction.
                Make sure the AI never reveals itself as an AI.
                Instead of saying "Base on my results, I found that...", the AI should say "According to publicly available information..."
                """
            },
            {
                "role": "user",
                "content": f"""
                {query_result} \n can you summarize the results descriptions for me? 
                Can you also let me know of the negatives that are associated with their sustainability efforts?
                If it is a food company, describe things like gmo, pesticides, and other things that are harmful to the environment.
                If it is a tech company, describe things like e-waste, and other things that are harmful to the environment.
                If it is a clothing company, describe things like fast fashion, and other things that are harmful to the environment.
                If it is a car company, describe things like gas emissions, and other things that are harmful to the environment.
                If the company is not in the above categories, describe things like their carbon footprint, and other things that are harmful to the environment.
                If the company is doing something good for the environment, describe it.
                If the company solves one of the issues common in the industry, describe it.
                """
            },
            {
                "role": "user",
                "content": "what conclusion can you make from this?"
            },
        ],
        n=1
    )

    response = completion.choices[0].message.content
    return response
