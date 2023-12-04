import imaplib

# Prompt the user to enter their Gmail credentials
EMAIL = input("Enter your Gmail address: ")
PASSWORD = input("Enter your Google APP Password: ")

# Connect to Gmail via IMAP
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

# Search for unread, unstarred emails
status, data = mail.search(None, '(UNSEEN UNFLAGGED)')

if status == 'OK':
    email_ids = data[0].split()

    for email_id in email_ids:
        mail.store(email_id, '+FLAGS', '\\Deleted')

    # Expunge to permanently delete emails marked as deleted
    mail.expunge()

# Close the connection
mail.close()
mail.logout()