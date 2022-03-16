""" GW XML subtree

The better way would be to follow the pattern of excitingtools and have it build
an XML tree, then finally convert that to a string, however this is faster.
"""
from typing import Optional


class GWInput:
    """ GW XML element in exciting input.xml
    Slightly dirty - goes straight to XML string construction using fstrings.
    """

    _subtrees = ['mixbasis', 'freqgrid', 'barecoul', 'selfenergy']

    def __init__(self,
                 gw: dict,
                 mixbasis: Optional[dict] = None,
                 freqgrid: Optional[dict] = None,
                 barecoul: Optional[dict] = None,
                 selfenergy: Optional[dict] = None
                 ):
        """
        """
        self.gw = gw
        self.mixbasis = mixbasis
        self.freqgrid = freqgrid
        self.barecoul = barecoul
        self.selfenergy = selfenergy

    @staticmethod
    def convert(value):
        """ Convert lists to strings
        :return:
        """
        if not isinstance(value, (list, tuple)):
            return value
        return " ".join(str(x) for x in value).strip()

    def to_xml_str(self) -> str:
        """ Create a GW input XML string from class attributes.
        :return: GW input string.
        """
        # Do the GW attributes separately
        gw_string = "<gw\n"
        for key, value in self.__dict__['gw'].items():
            processed_value = self.convert(value)
            gw_string += f'  {key}="{processed_value}"\n'
        gw_string += "  >\n"

        # All optional subtrees
        for name in self._subtrees:
            subtree = self.__dict__[name]
            if subtree is None:
                continue

            gw_string += f"  <{name}\n"
            for key, value in subtree.items():
                processed_value = self.convert(value)
                gw_string += f'    {key}="{processed_value}"\n'
            gw_string += f"  ></{name}>\n\n"

        gw_string += "</gw\n\n"
        return gw_string
