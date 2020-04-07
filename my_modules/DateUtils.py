import time, datetime
import pendulum


class DateUtils:

  def __init__(self):
    print('date util constructor constructor')


  # Creates a pendulum date object with the last day of the current week
  @staticmethod
  def get_high_range_for_week():
    print('high range')


    now = pendulum.now()
    end_of_week = now.end_of('week')
    print(end_of_week)

    return end_of_week

  # Creates a pendulum date object with the first day of the current week
  @staticmethod
  def get_low_range_for_week():
    print('low range')

  
    now = pendulum.now()
    start_of_week = now.start_of('week')
    print(start_of_week)

    return start_of_week


  @staticmethod
  def sort_criteria(message):
    return pendulum.parse(message.val()['time'])
    

  @staticmethod
  def create_date_from_timestamp(timestamp):
    return pendulum.parse(timestamp)

    




  

  





