## Copy-pasted ?
***
A project to check if the content on google document is copy-pasted by user.
---

### Instructions to Run 
---
1. Clone the repository: `https://github.com/Kuljeet1998/google-doc`
2. Navigate to the project directory: `cd {repository}`
3. Follow the pre-requiste steps below
4. Run command `python.py google_docs.py -d {DOCUMENT_ID}`
   Examplle: `python google_docs.py -d "13Ztp08sngMZ6ScMFu2YZNwXWOguEmVmVdbooLAVd-9k"`
   Alternative: `python.py google_docs.py` which has default deocument-id set as above.
---

### Pre-requisites (After cloning):
---
1. Create a directory `config` in main directory
2. Create a postgres database
3. Add the following files:
    * `credentials.json` : json file containing OAuth 2.0 desktop client secrets
    * `secrets.json` : json containing secrets of your postgres database (host,database,user,password)
    * `service_account_secrets.json` : json containing secrets of the service account
---

### References Used:
---
1. [GoogleDocsAPI](https://developers.google.com/docs/api/reference/rest "Google Doc Rest API")
2. [GoogleDriveAPI](https://developers.google.com/drive/api/guides/about-sdk "Google drive API")
3. [StackOverflow](https://stackoverflow.com/ "Stack overflow forum")
4. [ChatGPT](https://chat.openai.com/ "ChatGPT")
---

### Video URL
---
https://www.loom.com/share/9b10905fb89845aab2472a4135a69915
(Sorry for the audio clarity)
---