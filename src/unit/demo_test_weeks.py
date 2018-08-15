import datetime
import tf_idf

print('first', tf_idf.weeks_since_01(datetime.date(2018, 8, 1)))
tf_idf.TESTING_DATE = datetime.date(2018, 8, 30)
print('second', tf_idf.weeks_since_01(datetime.date(2018, 8, 1)))

#--------------------

from tf_idf import weeks_since_02
print('first', weeks_since_02(datetime.date(2018, 8, 1)))
weeks_since_02.testing_date = datetime.date(2018, 8, 30)
print('second', weeks_since_02(datetime.date(2018, 8, 1)))
