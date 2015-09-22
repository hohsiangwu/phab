import datetime

def datetime_from_timestamp(timestamp):
  return datetime.datetime.utcfromtimestamp(int(timestamp))
