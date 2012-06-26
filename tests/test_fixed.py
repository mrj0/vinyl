from vinyl.fields import VarCharField, FixedCharField
from vinyl.record import Record
from nose.tools import assert_equal


class FixedFormat(Record):
    control_2 = FixedCharField(value='0002', field_length=4)
    customer_nbr = FixedCharField(field_length=26, pad_with='0', justify='right')
    is_business = FixedCharField(field_length=1)
    customer_name = FixedCharField(field_length=40)
    cost_center = FixedCharField(field_length=5, pad_with='0', justify='right')
    user_name = FixedCharField(value='dude', field_length=16)
    item_type = FixedCharField(value='Customer/Prospect', field_length=17)
    item_status = FixedCharField(value=' P', field_length=2)
    subject_code = FixedCharField(field_length=32)
    start_date = FixedCharField(field_length=10)
    start_time = FixedCharField(value='00:00:00', field_length=8)
    assigned_to_user = FixedCharField(field_length=20)
    is_syncable = FixedCharField(value='Y', field_length=1)
    raw_data_string = FixedCharField(field_length=175)
    filler_1 = FixedCharField(value='          {TRM:', field_length=15)
    lead_id = VarCharField(max_length=15)
    filler_2 = FixedCharField(value='}', field_length=1)


def test_fixed():
    record = FixedFormat(customer_nbr='12345', customer_name='Napoleon Bonaparte')
    assert_equal(record.control_2, '0002')
    assert_equal(record.customer_nbr, '00000000000000000000012345')
    assert_equal(record.item_status, ' P') # s/b default pending, space padded
    assert_equal(record.customer_name, 'Napoleon Bonaparte                      ')

