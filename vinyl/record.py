from collections import OrderedDict
import logging
from vinyl.fields import BaseField


log = logging.getLogger('vinyl')


class RecordMetaclass(type):
    def __new__(mcs, class_name, bases, dct):
        fields = OrderedDict()
        unordered = [(name.lower(), value) for name, value in dct.items() if isinstance(value, BaseField)]
        map(lambda x: fields.__setitem__(*x), sorted(unordered, key=lambda item: item[1].created_order))

        special = dict((name, value) for name, value in dct.items() if not isinstance(value, BaseField))

        obj = super(RecordMetaclass, mcs).__new__(mcs, class_name, bases, special)
        obj._fields = fields

        # set the field name on each field
        map(lambda x: setattr(x[1], 'field_name', x[0]), fields.items())

        return obj


class Record(object):
    """
    A mutable record type. Write classes describing the data declaratively,
    but have all the ease-of-use that namedtuple provides. Except that the keys
    are case-insensitive, and the type is mutable (useful for converting formats).
    """

    __metaclass__ = RecordMetaclass

    def __init__(self, *args, **kw):
        super(Record, self).__init__()
        self._load(*args, **kw)

    def _load(self, *args, **kw):
        """
        Instantiating this class is expensive. Use this method to load
        new data in to an existing instance.

        Note that it doesn't empty any existing values, so take
        care to set all the fields in this Record to a new value.
        """
        index = 0
        value = None
        try:
            for index, value in enumerate(args):
                self.__setitem__(index, value)
        except IndexError:
            log.error('{0}: IndexError setting index {1} with value: "{2}"'.format(
                self.__class__.__name__, index, value))
            raise

        for k, v in kw.items():
            if k.lower() not in self._fields:
                raise AttributeError('Unknown field {0}'.format(k))
            self.__setattr__(k, v)

    def _validate(self):
        map(lambda x: x.validate(), self._fields.values())

    def __len__(self):
        return len(self._fields)

    def __getitem__(self, index):
        return self._fields.values()[index].value

    def __setitem__(self, index, value):
        name, field = self._fields.items()[index]
        self._fields[name].value = field.to_record(value)

    def __setattr__(self, key, value):
        key = key.lower()
        field = self._fields[key]
        self._fields[key].value = field.to_record(value)

    def __getattr__(self, key):
        return self._fields[key.lower()].value

    def __iter__(self):
        for name, field in self._fields.items():
            yield field.value

    def __repr__(self):
        return '{0}({1})'.format(
            self.__class__.__name__,
            ', '.join(map(lambda x: "{0}={1}".format(x[0], repr(x[1].value)), self._fields.items())),
        )

    def __delattr__(self, name):
        raise NotImplementedError('Cannot delete attributes')
