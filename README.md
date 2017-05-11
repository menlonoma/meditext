# Meditext
An SMS-based differential diagnosis and medical information service.
Built using Infermedica and Twilio APIs.
Created for COMP150 - Computing for Developing Regions at Tufts University

### Interacting with Meditext via SMS (not yet available)

Send Meditext a message to start the service, such as 'hello'. Meditext will reply
with instructions to enter a disease name for more information or the user's age for a
differential diagnosis. Answer accordingly, and follow the instructions provided by
Meditext. If an age is sent to start a differential diagnosis, the user will be prompted
for their sex, followed by their symptoms, and then will be asked a series of yes or no
questions. If the user is asked more than 10 yes or no questions and a conclusive diagnosis
(confidence of at least 90%), Meditext will begin sending the user the top three diagnoses
along with the next yes or no question. Users can text 'more info' at this point for more
information about the diagnoses, and then can send an answer to the next question to continue
or text 'q' to quit.

### Interacting with Meditext via Browser

Meditext uses Twilio to send and receive text messages. Testing was completed on a
designated trial account, but we have not paid for a number accessible by any phone.
To interact with Meditext via a web browser, one can use the following URL format:

http://meditextcdr.herokuapp.com/?From=%2B16466237048&Body=MESSAGEHERE

In the URL above, 16466237048 represents a phone number, which Meditext expects to
receive from Twilio, along with a message body, encoded in place of MESSAGEHERE.

To begin an interaction with Meditext, a user must send a text to Meditext. This can
be simulated with the following URL:

http://meditextcdr.herokuapp.com/?From=%2B16466237048&Body=hello

Meditext then prompts the user for their age if they wish to obtain a diagnosis,
or the name of a disease if they are looking for treatment information. Replace
the MESSAGEHERE field in the testing URL with the appropriate input and then press enter.

Search example: http://meditextcdr.herokuapp.com/?From=%2B16466237048&Body=burn

This will lead Meditext to return information about caring for a burn.

Diagnosis example: http://meditextcdr.herokuapp.com/?From=%2B16466237048&Body=20

By sending 20, Meditext will begin a process of attempting to diagnose a 20 year-old person,
and will prompt the user for their sex. Change the MESSAGEHERE field to M or F and press enter.
To enter symptoms, change the MESSAGEHERE field to include symptoms separated by '+'.
Meditext then begins asking yes or no questions, which can be answered with yes, no, Y, and N,
regardless of capitalization. Continue answering questions until Meditext returns a diagnosis.