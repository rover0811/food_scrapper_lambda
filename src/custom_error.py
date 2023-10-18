class HolidayError(Exception):
    def __init__(self,date):
        super().__init__(f'The restaurant is closed on this date {date}')

class NetworkError(Exception):
    def __init__(self):
        super().__init__('While sending requests to ChatGPT, All retrial are failed.')
