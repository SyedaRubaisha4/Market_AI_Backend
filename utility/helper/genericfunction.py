from datetime import datetime


class GenericFunctions():

    @staticmethod
    def first_or_default(array):
        return array[0] if array else None

    @staticmethod
    def is_null_or_empty(str_value):
        return str_value == None or str_value == ''

    @staticmethod
    def unix_time_to_datetime(unix_time):
        return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')