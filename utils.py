from datetime import datetime

def get_current_datetime():
    now = datetime.now()
    current_time = now.strftime("%y-%m-%d %H:%M:%S")
    return current_time

def auto_fill_id(latest_row):
    if latest_row == '':
        return 1
    latest_id = latest_row[0]
    latest_id = latest_id + 1
    return latest_id