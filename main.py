from audio_to_transcript import audio_to_transcript
from question_answering import answer_question
from transcript_to_summary import summarize

def main():
    output_language = input("Enter the output language for audio transcription")
    audio_path = input("Enter the audio path for audio transcription")
    transcript = audio_to_transcript(audio_path, output_language)

    print(transcript)

    output_language_summary = input("Enter the output language for summary:")
    summary = summarize(transcript, output_language_summary)

    print(summary)


    question = input("Enter your question:")
    output_language_for_answering_question = input("Enter the output language for answer:")
    answer =  answer_question(question, transcript, output_language_for_answering_question)

    print(answer)


