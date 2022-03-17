"""Tools for parsing local orbitals
"""
from typing import Callable, Dict
import numpy as np
import xml.etree.ElementTree as ET

from src.utils.utils import str_to_bool, string_to_value


def parse_lorecommendations(file_name: str, species: list, l_max=7, node_max=20) -> dict:
    """Parse lorecommendations.

    Notes:
    ------
    In the output, 'n' is number of nodes, NOT the principal QN.

    The energy parameters are inconsistent with those returned by LINENGY.OUT
    because in one file, the basis is defined as |R|^2, and in the other as |rR|^2.
    Or because they're simply computed differently - need to confirm.

    recommendations = {'species_label1': energies,
                        'species_label2': energies
                      }
    where energies.shape = (l_max + 1, node_max + 1) contains all LO recommendations for the species.

    :param file_name: File name containing lorecommendations.
    :param species:  Lst of species characters, which MUST be consistent with the order they are given in
    exciting's input.
    :param l_max: Maximum l-channel.
    :param node_max: Number of nodes associated with the highest state of an l-channel.
    :return: Dictionary of recommendation energies.
    """
    with open(file=file_name, mode='r') as fid:
        lines = fid.readlines()

    energies = np.empty(shape=(l_max + 1, node_max + 1))

    # Skip header and first species index
    lines = lines[3:]

    i = 0
    recommendations = {}
    for i_species in range(0, len(species)):
        for i_l in range(0, l_max + 1):
            # l_index line
            i += 1
            for i_n in range(0, node_max + 1):
                energies[i_l, i_n] = float(lines[i].split()[2])
                i += 1
            # Single line break
            i += 1
        # skip species index line
        i += 1
        recommendations[species[i_species]] = np.copy(energies)

    return recommendations


def xml_reader(func: Callable):
    """ Decorate XML parsers, enabling the developer to pass
    an XML file name, XML string or ElementTree.Element as input.
    """
    def modified_func(input: str):
        # Element
        if isinstance(input, ET.Element):
            return func(input)

        # File name
        try:
            tree = ET.parse(input)
            root = tree.getroot()
            return func(root)
        except (FileNotFoundError, OSError):
            pass

        # XML string
        try:
            root = ET.fromstring(input)
            return func(root)
        except ET.ParseError:
            raise ValueError(f'Input string neither an XML file, '
                             f'nor valid XML: {input}')

    return modified_func


@xml_reader
def parse_species_xml(root) -> dict:
    """ Parses exciting species files.

    Return a dictionary with elements:
    species = {'chemicalSymbol': chemicalSymbol, 'name': name, 'z': z, 'mass': mass}
    muffin_tin = {'rmin': rmin, 'rinf': rinf, 'radius': radius, 'points':  radialmeshPoints}
    atomic_states = [{'n': 1, 'l': 0, 'kappa': 1, 'occ': 2.0, 'core': True},
                    {'n': 2, 'l': 0, 'kappa': 1, 'occ': 2.0, 'core': True}, ...]    basis = {}
    basis['default'] == [{'type': 'lapw', 'trialEnergy': '0.1500', 'searchE': 'true'}]
    basis['custom'] == [{'l': 0, 'type': 'lapw', 'trialEnergy': 1.35670550183736, 'searchE': False},
                        {'l': 1, 'type': 'lapw', 'trialEnergy': -2.69952312512447, 'searchE': False},
                        {'l': 2, 'type': 'lapw', 'trialEnergy': 0.00,  'searchE': False},
                        {'l': 3, 'type': 'lapw', 'trialEnergy': 1.000, 'searchE': False},
                        {'l': 4, 'type': 'lapw', 'trialEnergy': 1.000, 'searchE': False},
                        {'l': 5, 'type': 'lapw', 'trialEnergy': 1.000, 'searchE': False}]

    :param root: XML file, XML string, or an ET.Element.
    :return : Dictionary of species file data (described above).
    """
    species_tree = root[0]
    species = {key: value for key, value in species_tree.attrib.items()}

    for key in ['z', 'mass']:
        species[key] = float(species[key])

    muffin_tin = {key: float(value) for key, value in species_tree[0].attrib.items()}

    atomic_states = []
    for atomic_state_tree in species_tree[1:-1]:
        assert atomic_state_tree.tag == 'atomicState', "Expect tag to be atomicState"
        atomic_states.append(string_to_value(atomic_state_tree.attrib))

    basis_tree = species_tree[-1]
    basis: Dict[str, list] = {'default': [], 'custom': [], 'lo': []}

    for func in basis_tree:
        function: dict = func.attrib

        if func.tag == 'lo':
            function['l'] = int(function['l'])
            function.update(parse_lo_from_species(func))
        else:
            function = string_to_value(function)

        basis[func.tag].append(function)

    return {'species': species,
            'muffin_tin': muffin_tin,
            'atomic_states': atomic_states,
            'basis': basis}


def parse_lo_from_species(lo_function) -> dict:
    """
    Given some lo_function with:
      wf {'matchingOrder': '0', 'trialEnergy': '-2.0', 'searchE': 'true'}
      wf {'matchingOrder': '1', 'trialEnergy': '-2.0', 'searchE': 'true'}

    return
    {'matchingOrder': [0, 1], 'trialEnergy': [-2.0, -2.0], 'searchE': [True, True]}
    """
    # Use lists to GUARANTEE consistent ordering
    matching_order = []
    trial_energy = []
    search = []
    for radial in lo_function:
        matching_order.append(int(radial.attrib.get('matchingOrder')))
        trial_energy.append(float(radial.attrib.get('trialEnergy')))
        search.append(str_to_bool(radial.attrib.get('searchE')))
    return {'matchingOrder': matching_order, 'trialEnergy': trial_energy, 'searchE': search}
