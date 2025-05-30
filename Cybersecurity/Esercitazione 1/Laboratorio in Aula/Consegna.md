####Exercise 1 - RSA####

You manage to intercept an rsa encrypted message: 11700901449779765763508101081

We know that it contains only one word

We also know the public key:

n = 132420683385315910791872800790076560548274292915602211551970038528407686609679552632778004136225026734894405625585255079274407744373849604560084628804772237703552168790280768702939708169783196212168917735971708699471743264252681591112502545288149137877768737422686737460701423105441179752299232063182125115961

e = 2

Can you retrieve the original message?





####Excercise 2: Finding a partial hash collision####

The exam results are out! Unfortunately your grade is 18. 
Now you are required to send an email to accept your grade containing the sentence "I accept my grade of 18". 
An automatic grade-registering platform calculates the md5 of the text of your email, takes the first 6 characters,
and checks if they equal to "e88792". The automatic platform only reads the sentence until the grade,
everything else is discarded. Can you produce a sentence that starts with "I accept my grade of 30" and that has an hash equal to "e88792"?

####Exercise 3 - The ECB Oracle attack####

The oracle has spoken! It appends a secret message to what you send. Can you leak the secret?

We know that the block size and the secret length are 16.

Do not watch what's inside the next cell
Inside this cell there is the definition of the "encrypt" function that the oracle uses to encrypt data.

It takes the message, it appends the secret to it and finally it adds padding if the total length is not a multiple of 16
