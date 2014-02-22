Vinyl
===========================

Mutable record type for dealing with flat files like CSV or pipe delimited data.

Dealing with flat files is painful. Instead, use vinyl to declaratively describe and validate
common flat file formats. Vinyl gives you the convenience of attribute-style access
like a namedtuple, but in a mutable data type suitable for easily transforming data.

.. code:: python

    import os
    import csv
    from vinyl.record import Record
    from vinyl.fields import VarCharField, FixedCharField

    # declare the data format
    class TestRecord(Record):
        customer_name = VarCharField(max_length=50)
        customer_number = FixedCharField(field_length=10, pad_with='0', justify='right' )
        start_time = FixedCharField(value='00:00:00', field_length=8)

    # create an instance
    record = TestRecord()

    # read data from a file
    with open(os.path.join(os.path.dirname(__file__), 'example.txt')) as f:
        reader = csv.reader(f)
        # copy a row of CSV data to the recordinstance
        record._load(*reader.next())

        # check the name was read correctly
        assert record.customer_name == 'a customer name with max length=50'

        # set a different customer number
        record.customer_number = '3'

        # number is reformatted according to the field settings
        assert record.customer_number == '0000000003'

        # a static field
        assert record.start_time == '00:00:00'

        print repr(record)
        # >>> TestRecord(customer_name=u'a customer name with max length=50',
        #                customer_number=u'0000000003', start_time=u'00:00:00')

Support
-------

For issues and source control, use github:

https://github.com/mrj0/vinyl/
