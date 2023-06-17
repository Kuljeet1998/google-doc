from datetime import datetime

AVG_TYPING_SPEED = 40

def get_current_datetime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')

def auto_fill_id(latest_row_id):
    return latest_row_id+1
