import concurrent.futures
import os
import tempfile
import threading
import wave
from io import StringIO

import pyttsx3
from pydub import AudioSegment
from gtts import gTTS

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


# def save_to_mp3(t, file):
#     tts = gTTS(t, lang='en')
#     tts.save(file)
#
#
# def extract_text_from_pdf(pdf_path):
#     resource_manager = PDFResourceManager()
#     fake_file_handle = StringIO()
#     converter = TextConverter(resource_manager, fake_file_handle)
#     page_interpreter = PDFPageInterpreter(resource_manager, converter)
#
#     # t = ""
#     with open(f"{pdf_path}.pdf", 'rb') as fh:
#         for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
#             page_interpreter.process_page(page)
#
#         t = fake_file_handle.getvalue()
#
#     converter.close()
#     fake_file_handle.close()
#
#     if t:
#         return t
#
#
# def text_converting(pdf_in):
#     pdf_path = f"{pdf_in}.pdf"
#     t = extract_text_from_pdf(pdf_path)
#     speaker = pyttsx3.init()
#     speaker.setProperty('rate', 120)
#     speaker.say(t)
#     speaker.runAndWait()
#     speaker.stop()


# if __name__ == '__main__':
#     pdf_document = input(str("Enter the name of the PDF document you want to process: "))
#     # text_converting(pdf_document)
#     text = extract_text_from_pdf(pdf_document)
#     mp3_file = input(str("Enter the name of the mp3 file you want to save: "))
#     save_to_mp3(text, mp3_file)


# def text_converting(pdf_in, mp3_out):
#     pdf_reader = PdfFileReader(pdf_in)
#     engine = pyttsx3.init()
#
#     # Set the speed of the speech
#     rate = engine.getProperty('rate')
#     engine.setProperty('rate', rate - 30)
#
#     clean_text = ""
#     for page_number in range(len(pdf_reader.pages)):
#         text = pdf_reader.pages[page_number].extract_text()
#         # Clean up the text and remove page numbers, headings, etc.
#         clean_text += text.strip().replace('\n', ' ')
#
#     # Save the speech to a MP3 file
#     engine.save_to_file(clean_text, mp3_out)
#     engine.runAndWait()
#     engine.stop()
#
#
# if __name__ == '__main__':
#     pdf_file = input("Enter the name of the PDF file: ")
#     pdf_path = input("Enter the path to the PDF file: ")
#     pdf_file_path = pdf_path + "/" + pdf_file
#
#     mp3_file = input("Enter the name for the MP3 file: ")
#     mp3_path = input("Enter the path to save the MP3 file: ")
#     mp3_file_path = mp3_path + "/" + mp3_file + ".mp3"
#
#     text_converting(pdf_file_path, mp3_file_path)
#     print(f"File saved to {mp3_file_path}.")


def extract_text_from_pdf(path):
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    laparams = LAParams()
    laparams.all_texts = True
    laparams.detect_vertical = True
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    converter = TextConverter(resource_manager, fake_file_handle, laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        t = fake_file_handle.getvalue()

    unwanted_parts = ("These materials are © 2018 John Wiley & Sons, Inc. Any dissemination, distribution or " +
                      "unauthorized use is strictly prohibited.")
    for part in unwanted_parts:
        t = t.replace(part, '')

    converter.close()
    fake_file_handle.close()
    return t


def text_converting(pdf_in):
    path = pdf_in
    t = extract_text_from_pdf(path)
    speaker = pyttsx3.init()
    speaker.setProperty('rate', 200)
    speaker.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    speaker.say(t)
    speaker.runAndWait()
    return t


# def save_to_mp3(t, file_path):
#     with tempfile.NamedTemporaryFile(delete=False) as temp_wav_file:
#         temp_wav_file_path = temp_wav_file.name
#         try:
#             engine = pyttsx3.init()
#             engine.setProperty('rate', 200)
#             engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN' +
#                                         r'-US_ZIRA_11.0')
#             engine.save_to_file(t, temp_wav_file_path)
#             engine.runAndWait()
#             os.system(f'ffmpeg -i "{temp_wav_file_path}" "{file_path}"')
#         except Exception as e:
#             print(e)
#             return False
#     return True


def save_to_mp3(t, path):
    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav_file:
        # Convert text to audio
        speaker = pyttsx3.init()
        speaker.setProperty('rate', 200)
        speaker.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN' +
                                     r'-US_ZIRA_11.0')
        speaker.save_to_file(t, temp_wav_file.name)
        speaker.runAndWait()

    # Convert the WAV file to an MP3 file
        with wave.open(temp_wav_file.name, 'rb') as wave_file:
            audio_data = wave_file.readframes(wave_file.getnframes())
            audio_segment = AudioSegment(
                data=audio_data,
                sample_width=wave_file.getsampwidth(),
                frame_rate=wave_file.getframerate(),
                channels=wave_file.getnchannels()
            )
            audio_segment.export(path, format='mp3')
    # Remove the temporary WAV file
    os.remove(temp_wav_file.name)


if __name__ == '__main__':
    pdf_file = input("Enter the name of the PDF file: ")
    pdf_path = input("Enter the path to the PDF file: ")
    pdf_file_path = pdf_path + "/" + pdf_file
    if ".pdf" not in pdf_file_path:
        pdf_file_path += ".pdf"

    mp3_file = input("Enter the name for the MP3 file: ")
    mp3_path = input("Enter the path to save the MP3 file: ")
    mp3_file_path = mp3_path + "/" + mp3_file
    if ".mp3" not in mp3_file_path:
        mp3_file_path += ".mp3"

    text = extract_text_from_pdf(pdf_file_path)
    print(text)
    save_to_mp3(text, mp3_file_path)
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future = executor.submit(extract_text_from_pdf, pdf_file_path)
    #     text = future.result()
    #     # text_to_speech_thread = threading.Thread(target=text_converting(), args=(text,))
    #     # text_to_speech_thread.start()
    #     save_to_mp3_thread = threading.Thread(target=save_to_mp3, args=(text, mp3_file_path))
    #     save_to_mp3_thread.start()
    #     # text_to_speech_thread.join()
    #     save_to_mp3_thread.join()
    print(f"File saved to {mp3_path}.")
