from datetime import datetime, timedelta
import os
import pickle
from typing import List
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from domain.utils import datetime_to_timezone, numpy_date_to_datetime


class GoogleCalendar():
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    CALENDAR_NAME = 'Entrenamientos Redolat Team'
    TIMEZONE = 'Europe/Madrid'

    service = None

    def __init__(self, credentials) -> None:
        self.start_service(credentials)

    def start_service(self, credentials):
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build("calendar", "v3", credentials=creds)

    def load_events_to_calendar(self, events_training:List[dict], new_calendar_name: str | None):
        print("[START] load_to_calendar")

        try:
            calendar_dict = self.__create_or_get_calendar(new_calendar_name)

            for event_training in events_training:
                self.__insert_event_into_calendar(event_training, calendar_dict)
                print(f"Created event title: {event_training['title']}\n")

                return True

        except HttpError as error:
            print(f"ERROR To load Events")
            raise error

    def __create_or_get_calendar(self, new_calendar_name):
        calendar_name = self.CALENDAR_NAME

        if new_calendar_name is not None:
            calendar_name = new_calendar_name

        calendar_exist = self.__calendar_exists(calendar_name)

        if calendar_exist is not None:
            return calendar_exist

        return self.__create_calendar(calendar_name)

    def __create_calendar(self, calendar_name: str):
        new_calendar_dict = {
            'summary': calendar_name,
            'timeZone': self.TIMEZONE
        }

        try:
            created_calendar = self.service.calendars().insert(body=new_calendar_dict).execute()
            return created_calendar
        except HttpError as error:
            print(f"Error creating Calendar: {calendar_name}")
            raise  error

    def __calendar_exists(self, calendar_name):
        calendars = self.__get_calendars()
        print(calendars)

        for calendar_dict in calendars['items']:
            if calendar_dict['summary'] == calendar_name:
                return calendar_dict

        return None

    def __get_calendars(self):
        try:
            calendar_list = self.service.calendarList().list().execute()
            return calendar_list
        except HttpError as error:
            print(f"ERROR getting calendars")
            raise error

    def __insert_event_into_calendar(self, event_training, calendar_dict):
        try:
            print("event_training: ")
            print(event_training)

            title = event_training[0]
            start_date:datetime = numpy_date_to_datetime(event_training[1])
            start_date = datetime_to_timezone(start_date, self.TIMEZONE)
            print(start_date)

            description = event_training[2]
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_date.isoformat(),
                    'timeZone': self.TIMEZONE,
                },
                'end': {
                    'dateTime': (start_date + timedelta(hours=1)).isoformat(),
                    'timeZone': self.TIMEZONE,
                },
            }

            self.service.events().insert(calendarId=calendar_dict['id'], body=event).execute()
        except HttpError as error:
            print("ERROR Insert Event into Calendar")
            raise error
