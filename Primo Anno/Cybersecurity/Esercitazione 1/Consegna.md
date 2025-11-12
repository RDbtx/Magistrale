
Cybersecurity Technologies and Risk Management - Cryptography Assignment

In this assignment, you will have to solve three exercises. All files necessary to complete the assignment can be found inside CryptoAssignment.zip on Microsoft Teams. 
For each exercise, you are required to:

⦁	Provide the code used:
⦁	Write your code in Python
⦁	Make sure that it runs without errors
⦁	Add comments to your code
⦁	Paste your code directly in this document using the following formatting:
⦁	Font: Courier New (or another monospace font)
⦁	Font Size: 10pt
⦁	Use proper indentation for readability.
⦁	This is an example
1.	Explain the code you provided:
⦁	Write a clear, accurate explanation of how the code works, describing each part in sufficient detail.
⦁	Explain any specific cryptographic concepts, algorithms or libraries you used
⦁	Write in correct English language: you can use tools like Grammarly to ensure correctness
1.	Submit this report in PDF format on Microsoft Teams

Tip: Use the code and functions in the CryptoLab.ipynb colab document to solve the exercises



Exercise 1

You are given a PDF file named “exercise1.pdf” which contains an encrypted message. Can you found out how it was encrypted and recover the original message? 
Try analyzing it using the pypdf python library.



Exercise 2

You are given another PDF file, named “exercise2.pdf”, which contains an encrypted message. 
You know that the message was encrypted using AES in ECB mode, and that the key used for encryption is a 16 character 
long binary string (meaning it’s made only of 0 and 1). Can you recover the original message? Again, make sure to use the pypdf python 
library to analyze the document.

Exercise 3

You are given a pdf file which was encrypted using the keys in the “keys” folder.
Once you decrypt the pdf file, you will see that it contains the text “Name Surname Matriculation Number”:
forge a new pdf document named “collision.pdf” that have your name, surname and matriculation number; 
this new document must have the first 4 digits of the sha256 hash equal to the original document, so make sure to add some data to find a collision.



