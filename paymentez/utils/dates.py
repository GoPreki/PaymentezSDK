from datetime import datetime

def isoformat_to_timestamp(isoformat_date, date_format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(isoformat_date, date_format).timestamp()