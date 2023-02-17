from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import whisper
import openai
from googletrans import Translator
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import traceback
import os

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize(ARTICLE, output_language):
    translator = Translator()
    ARTICLE = translator.translate(ARTICLE, dest='en').text

    ARTICLE = ARTICLE.replace('.', '.<eos>')
    ARTICLE = ARTICLE.replace('?', '?<eos>')
    ARTICLE = ARTICLE.replace('!', '!<eos>')

    sentences = ARTICLE.split('<eos>')
    current_chunk = 0
    max_chunk = 500
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1:
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])

    res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
    text = ' '.join([summ['summary_text'] for summ in res])

    translated_summary = translator.translate(text, dest=output_language).text
    return translated_summary


summary = summarize("""

Hi, I'm Grecia, from Mexico. I live in the state of Colima, in Villa de Álvarez. 
In my state you can see two volcanoes. One is fire and the other is snow. 
My cities are aseismic because the fire volcano is an active volcano and it shakes often. 
However, I really like being from there because it is a beautiful and peaceful place. 
The weather is warm most of the year, but there are times when you can see snow on the volcano. 
Volcanoes also serve to orient people because they indicate where the north is.

""",  "Spanish")


summarize
