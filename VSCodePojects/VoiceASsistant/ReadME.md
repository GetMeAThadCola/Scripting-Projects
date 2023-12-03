# Voice Assistant
This Python script creates a basic voice assistant using the speech_recognition, gtts (Google Text-to-Speech), and pydub libraries. Here's a short description of the code:

listen Function:

Utilizes the speech_recognition library to capture audio input from the microphone.
Converts the captured audio to text using Google's Speech Recognition service.
Handles exceptions for cases where the speech recognition cannot understand the audio or encounters a request error.
speak Function:

Uses the gTTS (Google Text-to-Speech) library to convert a given text to an MP3 audio file.
Saves the generated audio as "output.mp3."
Utilizes the pydub library to load and play the generated audio file.
__main__ Section:

Enters into an infinite loop to continuously listen for user commands.
Converts the recognized command to lowercase for easier processing.
If the command contains the word "exit," it prints a message and exits the loop, terminating the voice assistant.
If a command is recognized, it prints the command and uses the speak function to respond with a synthesized voice.
This script allows you to interact with the voice assistant by speaking commands, and it responds by converting the text of your command into speech. The assistant can be terminated by saying "exit."
