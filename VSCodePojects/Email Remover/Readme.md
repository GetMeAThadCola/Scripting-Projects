# **Script Usage Guide**
Overview
This Python script is designed to access your Gmail account using IMAP and delete unread, unstarred emails from your inbox. Before using the script, ensure you've set up a Google App Password as the script requires it for authentication.

Setting up Google App Password
Go to Google Account Settings:

Access your Google Account settings by clicking on your profile picture in Gmail and selecting "Google Account."
Navigate to Security Settings:

Under the "Security" section, select "App passwords."
Sign in and Generate App Password:

You may be prompted to sign in to your Google Account again for security purposes.
Select "Mail" and the device you intend to use the App Password with.
Click "Generate" to create an App Password.
Copy the App Password:

Once generated, copy the provided App Password. This will be used when running the script.
Using the Script
Clone the Repository:

Clone or download this script repository to your local machine.
Install Dependencies:

Ensure you have Python installed (version X.X or higher) on your system.
Install required dependencies by running:
Copy code
pip install imaplib
Run the Script:

Open a terminal or command prompt.
Navigate to the directory containing the script.
Execute the Script:

Execute the script by running:
Copy code
python script_name.py
The script will prompt you to enter your Gmail address and Google App Password.
Script Execution:

The script will connect to your Gmail account using IMAP and delete any unread, unstarred emails from the inbox
