from xml.etree import ElementTree as ET

from respite.inflector import singularize, pluralize
from respite.serializers.base import Serializer

class XMLSerializer(Serializer):

    def serialize(self, request):
        data = super(XMLSerializer, self).serialize(request)

        root = ET.Element('response')

        def serialize(key, value):

            def serialize_boolean(boolean):
                element = ET.Element(key)
                element.text = 'true' if boolean else 'false'

                return element

            def serialize_string(string):
                element = ET.Element(key)
                element.text = string

                return element

            def serialize_list(list):
                element = ET.Element(key)

                for item in list:
                    subelement = serialize(singularize(key), item)
                    element.append(subelement)

                return element

            def serialize_dictionary(dictionary):
                element = ET.Element(key)

                for subelement_key, subelement_value in dictionary.items():
                    subelements = serialize(subelement_key, subelement_value)
                    element.append(subelements)

                return element

            def serialize_integer(integer):
                element = ET.Element(key)
                element.text = '%s' % integer

                return element

            def serialize_none(none):
                element = ET.Element(key)
                element.text = ''

                return element

            if isinstance(value, bool):
                return serialize_boolean(value)

            if isinstance(value, basestring):
                return serialize_string(value)

            if isinstance(value, list):
                return serialize_list(value)

            if isinstance(value, dict):
                return serialize_dictionary(value)

            if isinstance(value, int):
                return serialize_integer(value)

            if value is None:
                return serialize_none(value)

            raise TypeError("Respite doesn't know how to serialize %s as XML" % value.__class__.__name__)

        root.append(
            serialize("items", data)
        )

        return '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root)
