# coding: utf-8
from datetime import datetime
from nose.tools import (
    assert_equal, assert_is_not_none, assert_is_none,
    assert_raises, assert_true, assert_not_equal)
import pytz
from vinyl.fields import RecordField, VarCharField, FixedCharField,\
    IntegerField, DateField, TimeField, ValidationError
from vinyl.record import Record


class LeadFormat(Record):
    error_code = VarCharField(value='error')
    comment_txt = VarCharField()

class TestFormat(Record):
    one = RecordField(value='w00t')
    two = RecordField(max_length=10)
    three = RecordField(zfill=5)
    four_date = DateField()
    four_hour = TimeField()
    five = IntegerField(min_value=0, max_value=99)
    six = VarCharField(max_length=10)
    seven = FixedCharField(field_length=10, pad_with='0', justify='right')
    eight = FixedCharField(field_length=4, justify='right')
    nine = FixedCharField(field_length=30)
    ten = VarCharField(required=True)

    stripped = RecordField(strip=True)

def test_record():
    record = TestFormat()
    assert_equal(record.one, 'w00t')
    record.two = 'asdflknasdlfknasdfl'
    assert_equal(len(record.two), 10)
    record[1] = 'asdflknasdlfknasdfl'
    assert_equal(len(record.two), 10)

    record.three = 1
    assert_equal(record.three, '00001')

    record.four_date = datetime.fromtimestamp(1340336022L, tz=pytz.utc)
    assert_equal(record.four_date, u'2012-06-22')

    record.four_hour = datetime.fromtimestamp(1340336022L, tz=pytz.utc)
    assert_equal(record.four_hour, u'03:33:42')

    record.five = 5
    assert_equal(record.five, '5')
    assert_raises(ValidationError, setattr, record, 'five', 100)
    assert_raises(ValidationError, setattr, record, 'five', -1)
    record.five = ''
    assert_is_none(record.five, "for reading from files, IntegerRecord should allow '' as None")

    assert_raises(ValidationError, setattr, record, 'six', '01234567890ads')

    record.seven = '12345'
    assert_equal(record.seven, '0000012345')

    record.eight = 'Y'
    assert_equal(record.eight, '   Y')
    record.eight = 'All work and no play makes Derek a dull boy.'
    assert_equal(record.eight, 'All ')

    record.nine = 'Keep Calm and Carry On'
    assert_equal(record.nine, 'Keep Calm and Carry On        ')

    record.stripped = '    a    '
    assert_equal(record.stripped, 'a')

    with assert_raises(ValidationError):
        record.ten = ''
        record._validate()
    with assert_raises(ValidationError):
        record.ten = None
        record._validate()

    assert_equal([f for f in record], list(record), 'should support iteration')

def test_instance():
    a = TestFormat()
    b = TestFormat()
    a.one = 'a'
    b.one = 'b'
    assert_not_equal(a.one, b.one)

def test_lead():
    record = LeadFormat(ERROR_CODE=None)
    assert_is_none(record.ERROR_CODE)
    record[0] = 'e'
    assert_equal(record[0], 'e')
    assert_equal(record.ERROR_CODE, 'e')
    assert_equal(list(record)[0], 'e')
    assert_equal(record._fields['error_code'].field_name, 'error_code')
    assert_equal(LeadFormat(error_code='boom').ERROR_CODE, 'boom')
    assert_raises(AttributeError, LeadFormat, asdf='nicht gut')
    assert_equal(LeadFormat(*(['boom'] * len(record))).ERROR_CODE, 'boom')

    record = LeadFormat(comment_txt=u'\u0161')
    assert_equal(u'\u0161', record.comment_txt)

    assert_equal(record._fields['comment_txt'].to_unicode(123L), '123')
