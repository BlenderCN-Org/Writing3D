"""Tools for working with W3D project features

This module contains tools to help store data related to nearly any feature of
a W3D project. Here, feature refers generically to any complex structure that
may appear in such a project. This may be as sophisticated as a "Timeline" or
as simple as a "Placement" for an object (since Placement features define
position, and potentially multiple kinds of rotation).
"""
from .errors import InvalidArgument


class W3DFeature(dict):
    """Base class for all W3D features

    By overriding argument_validators and default_arguments, subclasses can
    easily validate input and provide sensible default arguments.
    """

    argument_validators = {}
    """Dictionary mapping names of valid arguments to callable objects that
    return true if a given value is valid for that argument

    Note that this is really only used to check simple input from an editor or
    when reading in an XML file. It is not intended to do type-checking or
    consistency-checking across features. e.g. Validators might check if
    reasonable values have been passed in to specify an RGB color, but they
    would not be used to confirm that everything in a list of W3DProject
    objects is actually an object. For such higher-level things, we depend on
    duck-typing."""
    default_arguments = {}
    """Dictionary mapping names of arguments to their default values"""
    blender_scaling = 1
    """Scaling factor used to convert back and forth between Blender and legacy
    units"""

    def __init__(self, *args, **kwargs):
        super(W3DFeature, self).__init__()
        self.update(args)
        self.update(kwargs.items())
        try:
            self.ui_order
        except AttributeError:
            self.ui_order = sorted(self.argument_validators.keys())

    def __setitem__(self, key, value):
        if key not in self.argument_validators:
            raise InvalidArgument(
                "{} not a valid option for this W3D feature".format(key))
        if not self.argument_validators[key](value):
            raise InvalidArgument(
                "{} is not a valid value for option {}".format(value, key))
        super(W3DFeature, self).__setitem__(key, value)

    def __missing__(self, key):
        return self.default_arguments[key]

    def update(self, other):
        for key, value in other:
            self.__setitem__(key, value)

    def toXML(self, parent_root):
        """Store data in W3D XML format within parent_root
        :param :py:class:xml.etree.ElementTree.Element parent_root

        Since this differs for every W3D feature, subclasses MUST override
        this function.
        """
        raise NotImplementedError("toXML not defined for this feature")

    @classmethod
    def fromXML(feature_class, xml_root):
        """Create W3DFeature object from xml node for such a feature

        Since this differs for every W3D feature, subclasses MUST override
        this function.
        :param :py:class:xml.etree.ElementTree.Element xml_root: xml node for
        this feature
        """
        raise NotImplementedError("fromXML not defined for this feature")

    def is_default(self, key):
        """Return true if value has not been set for key and default exists,
        false otherwise"""
        return (key not in self and key in self.default_arguments)
