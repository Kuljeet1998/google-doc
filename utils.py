from datetime import datetime

AVG_TYPING_SPEED = 45

def get_current_datetime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')

def auto_fill_id(latest_row_id):
    return latest_row_id+1

def is_copy_pasted(new_content,duration):
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