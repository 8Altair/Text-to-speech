# from PyPDF2 import PdfReader as PPDFR
#
# import pyttsx3
#
#
# def text_converting(pdf_in, pdf_out):
#     pdf_reader = PPDFR(open(f"{pdf_in}.pdf", 'rb'))
#     speaker = pyttsx3.init()
#
#     clean_text = ""
#     for page_number in range(len(pdf_reader.pages)):
#         text = pdf_reader.pages[page_number].extract_text()
#         clean_text = text.strip().replace('\n', ' ')
#         print(clean_text)
#
#     speaker.save_to_file(clean_text, f"{pdf_out}.mp3")
#     speaker.runAndWait()
#
#     speaker.stop()
#
#
# if __name__ == '__main__':
#     pdf_document = input(str("Enter the name of the PDF document you want to process: "))
#     mp3_file = input(str("Enter the name of the mp3 file you want to save: "))
#     text_converting(pdf_document, mp3_file)

from io import StringIO

from gtts import gTTS
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import pyttsx3


def save_to_mp3(t, file):
    tts = gTTS(t, lang='en')
    tts.save(file)


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    t = ""
    with open(f"{pdf_path}.pdf", 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)

        t = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()

    if t:
        return t


def text_converting(pdf_in):
    pdf_path = f"{pdf_in}.pdf"
    t = extract_text_from_pdf(pdf_path)
    speaker = pyttsx3.init()
    speaker.setProperty('rate', 120)
    speaker.say(t)
    speaker.runAndWait()
    speaker.stop()


if __name__ == '__main__':
    pdf_document = input(str("Enter the name of the PDF document you want to process: "))
    # text_converting(pdf_document)
    text = extract_text_from_pdf(pdf_document)
    mp3_file = input(str("Enter the name of the mp3 file you want to save: "))
    save_to_mp3(text, mp3_file)
