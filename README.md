# **Text to speech**
This is a project that aims to convert text from the PDF file to mp3 format.

# Table of Contents
- [Introduction](#introduction)
- [Usage](#usage)
- [Functionalities](#functionalities)
  - [General](##general)
  - [Text extraction](##textextraction)
  - [Saving the extracted text to mp3 format](##savingtheextractedtexttomp3format)
- [License](#license)

## Introduction
This project is designed to extract text from a PDF file and convert it to an mp3 audio file.
It uses PyPDF2 to extract text from the PDF and pyttsx3 to convert the text to speech and save
it as an MP3 file.

## Usage
1. Navigate to the project directory.
2. Run the script (main file).
3. Enter the name and path of the PDF file you want to convert when prompted.
4. Enter the name and path of the MP3 file you want to save when prompted.
5. Wait for the script to extract the text from the PDF file and save it as an MP3 audio file.

## Functionalities
### General
This Python script contains two functions and a conditional code block that allows it to be executed
as a standalone program. The purpose of the script is to extract text from a **PDF** file, convert it to
speech and save it as an **mp3** audio file.

### Text extraction
The *extract_text_from_pdf* function takes in the file path to a **PDF** file as an argument and returns
the extracted text from the file as a string. It first opens the **PDF** file in binary mode using a _with_
statement, reads each page of the file using the **PyPDF2** module and concatenates the extracted text from
all pages into a single string. If an error occurs while opening or reading the file, the function raises an
appropriate exception.

### Saving the extracted text to mp3 format
The *save_to_mp3* function takes in the text to be converted to speech, the file path to save the resulting
**mp3** audio file, the speed at which the audio is spoken and the type of voice to use as arguments.
The function initializes the *pyttsx3* text-to-speech engine, sets the speech rate and voice type based on the
provided arguments, saves the text as an **mp3** audio file at the specified path using the _save_to_file_
method, and processes the resulting audio file using the _runAndWait_ method. If an error occurs while
saving the file, the function raises an appropriate exception.

## License
This project is licensed under the **MIT** License.
