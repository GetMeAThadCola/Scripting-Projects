# Hash Guard


This Bash script, attributed to Hunter Carbone, serves as a file comparison tool. 
When executed, it checks whether two provided files, indicated as arguments (likely file paths), are identical or have differences. 
The code begins by displaying a message, asserting ownership of the code, and indicating that a check is in progress. 
It proceeds to calculate MD5 checksums for the provided files and compares them. 
If the MD5 checksums match, the script reports that the files are identical. 
If there's a discrepancy in the checksums, it states that there are differences between the files. 
This script is useful for quickly verifying the integrity of files or identifying any variations between two files.