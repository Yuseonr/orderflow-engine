from datetime import datetime, timedelta, timezone
def convert_time(unix_time : int , utc : int=0):
    """
    Convert unix milliseconds to readable date and time format.\n
    :param unix_time: Unix time.
    :param utc: UTC offset in hours (default is 0).
    """
    if unix_time > 1e12:
        unix_time = unix_time / 1000

    dt = datetime.fromtimestamp(unix_time, timezone(timedelta(hours=utc)))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# Test 
if __name__ == "__main__":
    unix_time = 1743729212442
    utc_offset = 0  
    converted_time = convert_time(unix_time, utc_offset)
    print(converted_time)  
   