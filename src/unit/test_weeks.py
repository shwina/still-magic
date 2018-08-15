import datetime
import tf_idf

def test_weeks():
    tf_idf.TESTING_DATE = datetime.date(2018, 1, 10)
    assert weeks_since(datetime.date(2018, 1, 1)) == 2
