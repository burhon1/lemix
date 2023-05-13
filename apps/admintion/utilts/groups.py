from datetime import datetime

def diffrent_minut(start_time,end_time):

    start_time = datetime.strptime(str(start_time), "%H:%M:%S")
    end_time = datetime.strptime(end_time+":00", "%H:%M:%S")

    # get difference
    delta = end_time - start_time

    sec = delta.total_seconds()

    min = sec / 60

    return min