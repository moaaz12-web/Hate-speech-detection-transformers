import openai
import re
from googletrans import Translator
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Access the variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI API credentials
openai.api_key = OPENAI_API_KEY


# Define the GPT-3 model to use (e.g. "davinci" for GPT-3's largest model)
model_engine = "text-davinci-002"

# Define the maximum length of the context window
max_window_length = 1800


def answer_question(question, context, output_language):
    translator = Translator()
    question  = translator.translate(question, dest='en').text
    context = translator.translate(context, dest='en').text

    # Split the context into smaller windows of length less than or equal to max_window_length
    context_windows = re.findall(r".{1,%d}" % max_window_length, context, re.DOTALL)

    # Process each context window separately and generate an answer for each window
    answers = []
    for window in context_windows:
        prompt = f"question: {question}\ncontext: {window}\nanswer:"
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=max_window_length,
            n=1,
            stop=None,
            temperature=0.5,
        )
        answer = response.choices[0].text.strip()
        answers.append(answer)

    # Concatenate the answers from each window into a single answer string
    answer = " ".join(answers)

    answer = translator.translate(answer, dest=output_language).text

    return answer


answer = answer_question("Why does she like licving there?", 

"""
Hi, I'm Grecia, from Mexico. I live in the state of Colima, in Villa de Álvarez. In my state you can see two volcanoes. 
One is fire and the other is snow. My cities are aseismic because the fire volcano is an active volcano and it shakes often. 
However, I really like being from there because it is a beautiful and peaceful place. 
The weather is warm most of the year, but there are times when you can see snow on the volcano. 
Volcanoes also serve to orient people because they indicate where the north is.

""",  "Urdu"
)

