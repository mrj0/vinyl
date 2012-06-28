from datetime import datetime


class ValidationError(Exception):
    def __init__(self, field_name, message):
        super(ValidationError, self).__init__(u'{0}: {1}'.format(field_name, message))


class BaseField(object):
    """
    A Field type for a mutable record.

    ``value`` - set the initial value for this field
    ``max_length`` - the maximum length
    ``zfill`` - for value.zfill()
    ``strip`` - remove spaces from value if True
    ``required`` - used with validate (default False)
    """

    # track the order of field creation. This is needed
    # because there is very little other way to determine
    # the order of fields in python.
    creation_counter = -1

    def __init__(self,
                 value=None,
                 max_length=None,
                 zfill=None,
                 strip=False,
                 required=False):
        super(BaseField, self).__init__()
        BaseField.creation_counter += 1
        self.created_order = BaseField.creation_counter
        self.max_length = max_length
        self.zfill = zfill
        self.field_name = None   # filled in by RecordMetaclass
        self.required = required
        self.strip = strip

        self.value = self.to_record(value)

    def to_unicode(self, value):
        if value is None:
            return value
        if isinstance(value, unicode):
            return value
        if isinstance(value, str):
            return unicode(value, 'utf-8', errors='ignore')
        return str(value)

    def to_record(self, value):
        """
        Convert a value to a record value

        This is used when setting values on a Record.
        This method may simply return the input
        (depending on constructor values) but
        subclasses may also do formatting or validation.

        raises ``ValidationException`` on error
        """
        return self.clean_record(value)
    
    
    def raise_invalid(self, message):
        raise ValidationError(self.field_name, message)


    def clean_record(self, value):
        value = self.to_unicode(value)
        if value is not None:
            if self.strip:
                value = value.strip()
            if self.zfill is not None:
                value = value.zfill(self.zfill)
            if self.max_length is not None:
                value = value[:self.max_length]

        return value

    def validate(self):
        if self.required and not self.value:
            self.raise_invalid(u'Field is required')


class RecordField(BaseField):
    pass


class VarCharField(BaseField):
    """
    A validating variable-length character field. Raises an error if
    the length is > max_length (max_length must not be None)
    """

    def clean_record(self, value):
        value = self.to_unicode(value)
        if value is not None:
            if self.max_length is not None and len(value) > self.max_length:
                self.raise_invalid(u'Value too long: {0}'.format(value))

        return super(VarCharField, self).clean_record(value)


class FixedCharField(BaseField):
    """
    A fixed width char field, padded to field_size with pad_with, with a max
    length of field_size.
    """

    def __init__(self, field_length=None, pad_with=' ', justify='left', **kwargs):
        self.field_length = field_length
        self.pad_with = pad_with
        self.justify = justify
        super(FixedCharField, self).__init__(**kwargs)

    def clean_record(self, value):
        value = self.to_unicode(value)
        if value is None:
            value = ''
        if self.field_length is not None:
            if self.justify == 'right':
                value = value.rjust(self.field_length, self.pad_with)
            elif self.justify == 'left':
                value = value.ljust(self.field_length, self.pad_with)
            else:
                self.raise_invalid(u'Unknown value for justify: {0}'.format(self.justify))
        else:
            self.raise_invalid(u'Missing field_length')

        return super(FixedCharField, self).clean_record(value[0:self.field_length])


class IntegerField(BaseField):
    def __init__(self, min_value=None, max_value=None, **kw):
        self.max_value = max_value
        self.min_value = min_value
        super(IntegerField, self).__init__(**kw)

    def clean_record(self, value):
        if value == '':
            value = None

        if value is not None:
            value = int(value)
            if self.min_value is not None:
                if value < self.min_value:
                    self.raise_invalid(u'Value must be at least {0}'.format(self.min_value))
            if self.max_value is not None:
                if value > self.max_value:
                    self.raise_invalid(u'Value must be no greater than {0}'.format(self.max_value))

        return super(IntegerField, self).clean_record(value)


class DateField(BaseField):
    """
    Format datetime as a date string
    """
    def __init__(self, format='%Y-%m-%d', **kwargs):
        """
        ``pattern`` - strftime pattern
        """
        self.format = format
        super(DateField, self).__init__(**kwargs)

    def clean_record(self, value):
        if isinstance(value, datetime):
            value = value.strftime(self.format)

        return super(DateField, self).clean_record(value)


class TimeField(BaseField):
    """
    Format datetime as a time string
    """
    def __init__(self, format='%H:%M:%S', **kwargs):
        """
        ``pattern`` - strftime pattern
        """
        self.format = format
        super(TimeField, self).__init__(**kwargs)

    def clean_record(self, value):
        if isinstance(value, datetime):
            value = value.strftime(self.format)

        return super(TimeField, self).clean_record(value)
