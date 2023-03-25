import os

import PyPDF2
import pyttsx3


def extract_text_from_pdf(pdf_file_path) -> str:
    """
        Extracts text from a PDF file located at the specified path.

        Args:
            pdf_file_path (str): The path to the PDF file.

        Returns:
            str: The extracted text from the PDF file.

        Raises:
            FileNotFoundError: If the specified PDF file could not be found.
            Exception: If an error occurred while reading the PDF file.
    """

    t = ""
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            number_of_pages = len(pdf_reader.pages)
            for i in range(number_of_pages):
                page = pdf_reader.pages[i]
                page_text = page.extract_text()
                t += page_text
    except FileNotFoundError as e:
        print("The specified PDF file could not be found:", str(e))
    except Exception as e:
        print("An error occurred while reading the PDF file:", str(e))

    return t


# Function to save text to mp3 file
def save_to_mp3(text, mp3_file_path, speed=150, voice_type="male") -> None:
    """
        Converts the given text to mp3 audio file using the specified voice and saves it to the given file path.

        Args: text (str): The text to be converted to audio. mp3_file_path (str): The file path to save the mp3 audio
        file. speed (int, optional): The speed at which the audio is spoken, in words per minute. Defaults to 150.
        voice_type (str, optional): The type of voice to use for the audio. Valid values are "male" (Microsoft David)
        and "female" (Microsoft Zira). Defaults to "male".

        Raises: FileNotFoundError: If the given file path does not exist or is not accessible.
                PermissionError: If the user does not have permission to write to the specified file path.
        Returns:
            None
    """

    try:
        engine = pyttsx3.init()
        possible_voices = engine.getProperty("voices")
        voices = {"male": possible_voices[0], "female": possible_voices[1]}
        engine.setProperty("rate", speed)
        engine.setProperty("voice", voices[voice_type].id)
        engine.save_to_file(text, mp3_file_path)
        engine.runAndWait()
    except FileNotFoundError:
        print(f"Error: The file path '{mp3_file_path}' does not exist or is not accessible.")
    except PermissionError:
        print(f"Error: You do not have permission to write to the file path '{mp3_file_path}'.")


# The following code block will only execute if this script is run directly and not imported as a module
if __name__ == "__main__":
    # Gets user input for the PDF file name and path and combines them into a single string
    pdf_file_name = input("Enter the PDF file name: ")
    pdf_file_path = input("Enter the PDF file path: ")
    pdf_file_path = os.path.join(pdf_file_path, pdf_file_name)
    # Checks if the PDF file path ends with '.pdf', if not, add it to the path string
    if not pdf_file_path.endswith(".pdf"):
        pdf_file_path += ".pdf"

    # Gets user input for the MP3 file name and path and combines them into a single string
    mp3_file_name = input("Enter the MP3 file name: ")
    mp3_file_path = input("Enter the MP3 file path: ")
    mp3_file_path = os.path.join(mp3_file_path, mp3_file_name)
    # Checks if the MP3 file path ends with '.mp3', if not, add it to the path string
    if not mp3_file_path.endswith(".mp3"):
        mp3_file_path += ".mp3"

    # Extracts text from the PDF file specified by the user and stores it in a variable
    text = extract_text_from_pdf(pdf_file_path)
    # Converts the text to an MP3 audio file and saves it to the path specified by the user
    save_to_mp3(text, mp3_file_path, speed=175, voice_type="female")
    print(
        "\nText extracted from pdf file and saved to mp3 file successfully.")  # Print a success message to the console
