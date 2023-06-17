from datetime import datetime
import re
import string
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

AVG_TYPING_SPEED = 45
COPY_PASTE_THRESHOLD = 50

def get_current_datetime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')

def auto_fill_id(latest_row_id):
    return latest_row_id+1

#check if copy pasted with respect to typing speed
#Catch: This logic holds true if we know the exact start-time of user when he/she starts to edit
def is_copy_pasted_wrt_wpm(new_content,duration):
    if len(new_content)==0 or duration==0:
        return 0
    number_of_words = len(new_content.split())
    duration = int(duration/60) #Convert seconds to minutes
    typing_speed = int(number_of_words/duration)
    if typing_speed > AVG_TYPING_SPEED:
        #Likely to have been copied
        return 1
    #Possibly not copy pasted
    return 0

def preprocess_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Convert to lowercase
    text = text.lower()
    return text

#check if copy pasted from external sources
#Catch: This logic holds true if we can guess the external sources
def is_copy_pasted_external_source(new_content):

    # Divide the content into sentences
    sentences = re.split(r'(?<=[.!?])\s+', new_content)

    #Add external sources which can be used to copy paste
    external_sources = [
        "https://www.google.com/",
        "https://www.lipsum.com/",
        "https://randomwordgenerator.com/paragraph.php",
        "https://www.chegg.com/"
    ]

    # Vectorize the sentences using TF-IDF
    vectorizer = TfidfVectorizer()
    sentence_vectors = vectorizer.fit_transform(sentences)

    copied_sentences = []

    # Compare each sentence with the external sources
    for source in external_sources:
        response = requests.get(source)
        if response.status_code == 200:
            source_content = preprocess_text(response.text)
            source_vectors = vectorizer.transform([source_content])
            similarities = cosine_similarity(sentences, source_vectors)

            for i in enumerate(similarities):
                copied_sentences.append(sentences[i])
    
    if copied_sentences:
        percentage_copied = (len(copied_sentences) / len(sentences)) * 100
        #If text copied from external source is more than threshold (here, 50%), 
        #consider it copy-pasted
        if percentage_copied > COPY_PASTE_THRESHOLD:
            return 1
    
    return 0