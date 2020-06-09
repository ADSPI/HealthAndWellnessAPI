from datetime import datetime


class DateController:

    @staticmethod
    def format_date_to_iso(date_str: str):
        date_formatted = datetime.strptime(date_str, '%d/%m/%Y').date()

        return date_formatted

    @staticmethod
    def format_date_to_local(date_str):
        date_formatted = datetime.strptime(date_str, '%Y-%m-%d').date().strftime('%d/%m/%Y')

        return date_formatted
