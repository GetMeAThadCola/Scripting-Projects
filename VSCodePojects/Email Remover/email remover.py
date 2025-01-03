import imaplib
import time

def print_progress(count, total):
    print(f"Processed {count}/{total} emails...", end='\r')

# Prompt the user to enter their Gmail credentials
EMAIL = input("Enter your Gmail address: ")
PASSWORD = input("Enter your Google APP Password: ")

print("\nConnecting to Gmail...")

# Connect to Gmail via IMAP
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

print("Searching for unread, unstarred emails...")

# Search for unread, unstarred emails
status, data = mail.search(None, '(UNSEEN UNFLAGGED)')

if status == 'OK':
    email_ids = data[0].split()
    total_emails = len(email_ids)
    
    if total_emails == 0:
        print("No emails to process!")
    else:
        print(f"Found {total_emails} emails to process")
        
        # Process emails in batches for better performance
        batch_size = 100
        for i in range(0, total_emails, batch_size):
            batch = email_ids[i:i + batch_size]
            # Convert list of email IDs to comma-separated string
            id_string = b','.join(batch)
            
            # Mark batch for deletion
            mail.store(id_string, '+FLAGS', '\\Deleted')
            print_progress(min(i + batch_size, total_emails), total_emails)
        
        print("\nPermanently removing emails...")
        start_time = time.time()
        mail.expunge()
        
        duration = time.time() - start_time
        print(f"\nSuccess! Removed {total_emails} emails in {duration:.2f} seconds")

# Close the connection
print("Closing connection...")
mail.close()
mail.logout()
print("Done!")