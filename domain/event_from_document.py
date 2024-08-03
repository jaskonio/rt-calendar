from datetime import timedelta
from domain.document_docx import DocumentDocx
from domain.utils import convertir_fecha


class EventFromDocument():
    document:DocumentDocx
    start_hour_trainning = 20

    def __init__(self, path_file_name:str) -> None:
        self.document = DocumentDocx(path_file_name)

    def get_events_document(self):
        try:
            name_atleta = self.document.get_name_athlete()
            [start_date_string, end_date_string, year_string ] =  self.document.get_start_end_date()
            start_date = convertir_fecha(start_date_string, year_string)
            start_date = start_date + timedelta(hours=self.start_hour_trainning)
            # end_date = convertir_fecha(end_date_string, year_string)
            content_trainer = self.document.get_training()

            dates = [(start_date + timedelta(days=day)) for day in range(0, 14)]

            events_training = []

            for day, training in zip(dates,content_trainer):
                event = {}
                event['title'] = training[0:14] + '...'
                event['start_date'] = day
                event['training'] = training
                event['type'] = None
                events_training.append(event)

            return events_training
        except Exception as error:
            print(f"ERROR get_events_document")
            print(error)
            return None