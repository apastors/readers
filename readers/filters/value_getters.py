"""
Defines and facilitate access to a set of callables that will receive a row as input and will return a value
"""
import pyjq

from .operations import Operation, identity

class ValueGetter(object):
    def __init__(self, getter_string, transform=None):
        """
        Use jq-syntax to compile a query that will fetch the required value
        """
        try:
            self.string = getter_string
            self.getter = pyjq.compile(getter_string)
        except (AttributeError, ValueError) as err:
            raise ValueError(f'{getter_string} does not compile. {err}')
        self.transform = Operation(transform) if transform is not None else identity

    def __str__(self):
        string = self.string
        if self.transform is not identity:
            string = string + " (transform: {transform})".format(transform=self.transform)
        return string

    def __repr__(self):
        return self.__str__()


    def __call__(self, js):
        value = self.getter.apply(js)
        if len(value) == 1:
            value = value.pop()
        return self.transform(value)