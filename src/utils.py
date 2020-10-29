import datetime
import pycronofy
import uuid


### Useful helper functions and dicts
def save_html(html, path):
    with open(path, 'w') as f:
        f.write(html)

def open_html(path):
    with open(path, 'r') as f:
        return f.read()

data = {
    "monday": {
        "time": "",
        "module_title": "",
        "room": ""
    }
}

day_of_week = {
    "On Demand": 0,
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4
}

time = {
    9: "09:00",
    10: "10:00",
    11: "11:00",
    12: "12:00",
    13: "13:00",
    14: "14:00",
    15: "15:00",
    16: "16:00",
    17: "17:00",
    18: "18:00"
}

def constructDateTime(day):
    x = datetime.datetime.now()
    delta = day_of_week[day]
    date_of_day = x + datetime.timedelta(days=-x.weekday() + delta)
    return(date_of_day.strftime("%Y-%m-%d"))

def getCalendar():
    cronofy = pycronofy.Client(access_token="yamXobHAPtZLSjJJ8rhlprzn-9ZVSoBF")
    #events = cronofy.read_events()
    calendars = cronofy.list_calendars()
    print(calendars)

def createEvent(module_name, start_time, day, length, location, id):

    cronofy = pycronofy.Client(access_token="yamXobHAPtZLSjJJ8rhlprzn-9ZVSoBF")
    calendar_id = 'cal_X5fQV5pTLgCb1jIo_mhSbXatWLLPOjwgmAoWWZA'

    event = {
        'event_id': str(id),
        'summary': module_name,
        'description': "Lecture",
        'start': f"{constructDateTime(day)}T{time[start_time]}:00Z",
        'end': f"{constructDateTime(day)}T{time[start_time + length]}:00Z",
        'location': {
            'description': location
        }
    }
    cronofy.upsert_event(calendar_id=calendar_id, event=event)