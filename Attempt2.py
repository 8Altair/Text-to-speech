import os
import re
import tempfile

import pyttsx3
import PyPDF2
from pydub import AudioSegment


def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        text = ""
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
        return text


def save_to_mp3(pdf_file_path, mp3_file_path):
    # Validate file paths
    if not re.match(r'^\w+\.pdf$', os.path.basename(pdf_file_path)):
        raise ValueError("Invalid PDF file name")
    if not re.match(r'^\w+\.mp3$', os.path.basename(mp3_file_path)):
        raise ValueError("Invalid MP3 file name")

    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav_file:
        # Convert text to audio
        speaker = pyttsx3.init()
        speaker.setProperty('rate', 200)
        speaker.setProperty('voice',
                            r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
        speaker.save_to_file(extract_text_from_pdf(pdf_file_path), temp_wav_file.name)
        speaker.runAndWait()

        # Convert the WAV file to an MP3 file
        with open(temp_wav_file.name, 'rb') as wave_file:
            audio_data = wave_file.read()
            audio_segment = AudioSegment(
                data=audio_data,
                sample_width=2,
                frame_rate=44100,
                channels=1
            )
            audio_segment.export(mp3_file_path, format='mp3')

    # Remove the temporary WAV file
    os.remove(temp_wav_file.name)


if __name__ == "__main__":
    pdf_file_name = input("Enter the PDF file name: ")
    pdf_file_path = input("Enter the PDF file path: ")
    pdf_file_path += pdf_file_path + "\\" + pdf_file_name
    if ".pdf" not in pdf_file_path:
        pdf_file_path += ".pdf"
    print(pdf_file_path)
    mp3_file_name = input("Enter the MP3 file name: ")
    mp3_file_path = input("Enter the MP3 file path: ")
    mp3_file_path += mp3_file_path + "\\" + mp3_file_name
    if ".mp3" not in mp3_file_path:
        mp3_file_path += ".mp3"
        print(mp3_file_path)
    save_to_mp3(pdf_file_path, mp3_file_path)
    print(f"\nFile saved to {mp3_file_path}.")
