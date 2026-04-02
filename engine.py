import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def load_prompt():
    with open("prompt.txt", "r") as f:
        return f.read()


def analyze_input(user_input: str):
    system_prompt = load_prompt()

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    test_input = "Should I text her now or wait?"

    result = analyze_input(test_input)
    print(result)