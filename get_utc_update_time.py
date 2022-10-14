import datetime
import pytz

def get_utc_update_string() -> str:
    utc_tz = pytz.UTC
    current_time_utc = datetime.datetime.now(tz=utc_tz)
    result_string = f"{current_time_utc.year}.{current_time_utc.month}.{current_time_utc.day}.{current_time_utc.hour}"
    return result_string

if __name__ == '__main__':
    print(get_utc_update_string())
