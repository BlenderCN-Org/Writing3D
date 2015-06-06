"""Tools for validating options provided to Cave features"""
# TODO: convert to universal help and help strings


class OptionListValidator(object):
    """Callable object that returns true if value is in given list"""

    def __init__(self, *valid_options):
        self.valid_options = set(valid_options)

    def __call__(self, value):
        return value in self.valid_options

    def help(self):
        return "Value must be one of " + " ,".join(self.valid_options)


class IsNumeric(object):
    """Return true if value can be interpreted as a numeric type"""

    def __init__(self):
        pass

    def __call__(self, value):
        try:
            float(value)
            return True
        except TypeError:
            return False

    def help(self):
        return "Value must be numeric"


class IsNumericIterable(object):
    """Callable object that returns true if value is a numeric iterable

    :ivar required_length: Optionally sets required length for iterable. If
    this attribute is set to None, length is not checked."""

    def __init__(self, required_length=None):
        self.required_length = required_length

    def __call__(self, iterable):
        try:
            for value in iterable:
                if not IsNumeric(value):
                    return False  # Non-numeric
            return (self.required_length is None or len(iterable) ==
                    self.required_length)
        except TypeError:
            return False  # Non-iterable

    def help(self):
        if self.required_length is not None:
            return "Value must be a sequence of {} numeric values".format(
                self.required_length)
        return "Value must be a sequence of numeric values"


class CheckType(object):
    """Check if type of object matches specified type"""

    def __init__(self, correct_type):
        self.correct_type = correct_type

    def __call__(self, value):
        return isinstance(self.correct_type, value)

    def help(self):
        return "Value must be of type {}".format(self.correct_type)


class AlwaysValid(object):
    """Always returns True"""

    def __init__(self,
                 help_string="All Python objects are valid for this option"):
        self.help_string = help_string

    def __call__(self, value):
        return True

    def help(self):
        return self.help_string
