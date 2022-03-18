""" Write data to species file.
"""
from typing import List, Optional


def write_species_file_from_dict(species_dict: dict, file_name: Optional[str] = None):
    """ Write species data serialised a dict, to file.

    :param species_dict: Serialised species data.
    :param file_name: Optional file name.
    """
    species_str = species_xml_str_from_dict(species_dict)
    if file_name is None:
        file_name = species_dict['species']['name'].capitalize() + '.xml'
    with open(file_name, "w") as fid:
        fid.write(species_str)


def species_xml_str_from_dict(species: dict) -> str:
    """ Given species data in dict form (as returned by parse_species_xml), return
    an XML-formatted string.

    :param species: Serialised species data.
    :return species_str: XML-formatted species file string.
    """
    # Header
    species_str = """<?xml version="1.0" encoding="UTF-8"?>
<spdb xsi:noNamespaceSchemaLocation="../../xml/species.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    """

    # Species
    chemicalSymbol = species['species']['chemicalSymbol']
    name = species['species']['name']
    z = species['species']['z']
    mass = species['species']['mass']
    species_str += f'<sp chemicalSymbol="{chemicalSymbol}" name="{name}" z="{z}" mass="{mass}">\n'

    # Muffin tin
    rmin = species['muffin_tin']['rmin']
    radius = species['muffin_tin']['radius']
    rinf = species['muffin_tin']['rinf']
    radialmeshPoints = species['muffin_tin']['radialmeshPoints']
    species_str += f'    <muffinTin rmin="{rmin}" radius="{radius}" rinf="{rinf}" radialmeshPoints="{radialmeshPoints}"/>\n'

    # Atomic states
    species_str += atomic_states_string(species['atomic_states'])

    l_values = [lapw['l'] for lapw in species['basis']['custom']]
    l_max = max(l_values)

    # Presort LOs into l-channels
    all_los = species['basis']['lo']
    los_by_lvalue = [[] for _ in range(0, l_max + 1)]
    for lo in all_los:
        l = lo['l']
        los_by_lvalue[l].append(lo)

    species_str += "    <basis>\n "

    # Default l(apw) line
    type = species['basis']['default'][0]['type']
    trial_energy = species['basis']['default'][0]['trialEnergy']
    search_e = species['basis']['default'][0]['searchE']
    species_str += f'      <default type="{type}" trialEnergy="{trial_energy}" searchE="{search_e}"/> \n\n'

    # lapw and any explicit local orbitals, per l-channel
    # Note, there should only be one l(apw) per l-channel
    print(species['basis']['custom'])
    for l in range(0, l_max + 1):
        species_str += function_string(species['basis']['custom'][l])
        species_str += local_orbitals_string(los_by_lvalue[l])

    species_str += """    </basis>
  </sp>
</spdb>"""

    return species_str


def local_orbitals_string(los_l: List[dict]) -> str:
    """ Convert serialised local orbital data to string.

    NOTE, these operations are perhaps too trivial to be a function.
    For example:
    los_l = [lo1, lo2], with
    lo1 =  {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},
    lo2 =  {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},

    Returns a string of the form:
    <lo l="2">
      <wf matchingOrder="0" trialEnergy="0.00" searchE="false"/>
      <wf matchingOrder="1" trialEnergy="0.00" searchE="false"/>
    </lo>
     <lo l="2">
      <wf matchingOrder="1" trialEnergy="0.00" searchE="false"/>
      <wf matchingOrder="2" trialEnergy="0.00" searchE="false"/>
    </lo>

    :param los_l: List of LO functions, stored as dicts.
    :return string: XML-formatted LO string.
    """
    string = ''
    for lo in los_l:
        string += local_orbital_string(lo)
    return string + '\n'


def local_orbital_string(lo: dict) -> str:
    """ Convert serialised local orbital data to string.

    For example:
    lo =  {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},

    Returns a string of the form:
    <lo l="2">
      <wf matchingOrder="0" trialEnergy="0.00" searchE="false"/>
      <wf matchingOrder="1" trialEnergy="0.00" searchE="false"/>
    </lo>

    :return: XML-formatted local orbital string.
    """
    l = lo['l']
    string = f'      <lo l="{l}">\n'
    n_radial_functions = len(lo['matchingOrder'])
    for ir in range(0, n_radial_functions):
        matchingOrder = lo['matchingOrder'][ir]
        trialEnergy = lo['trialEnergy'][ir]
        searchE = str(lo['searchE'][ir]).lower()
        string += f'       <wf matchingOrder="{matchingOrder}" trialEnergy="{trialEnergy}" searchE="{searchE}"/>\n'
    string += '      </lo>\n'
    return string


def function_string(function: dict):
    """ Convert lapw serialised data into an XML string.

    Given:
    function = {'l': 0, 'type': 'lapw', 'trialEnergy': -1.83220324630948, 'searchE': False}

    return:
    <custom l="0" type="lapw" trialEnergy="-1.83220324630948" searchE="false"/>

    :param function: Dict of (l)apw data.
    :return: XML-formatted string for an (l)apw function in exciting's species file.
    """
    l = function['l']
    type = function['type']
    trial_energy = str(function['trialEnergy'])
    search_e = str(function['searchE']).lower()
    string = f'      <custom l="{l}" type="{type}" trialEnergy="{trial_energy}" searchE="{search_e}"/> \n\n'
    return string


def atomic_states_string(atomic_states: List[dict]) -> str:
    """ Convert serialised atomic states data to an XML string.

    Given atomic_states = [{'n': 1, 'l': 0, 'kappa': 1, 'occ': 2.00000, 'core': True},
                           {'n': 2, 'l': 0, 'kappa': 1, 'occ': 2.00000, 'core': True}, ...]
    return:
    '      <atomicState n="1" l="0" kappa="1" occ="2.00000" core="True"/>'
    '      <atomicState n="2" l="0" kappa="1" occ="2.00000" core="True"/>'

    :param atomic_states: List of atomic states. Each atomic state is held in a dictionary.
    :return: XML-formatted string for the atomicState lines in exciting's species file.
    """
    string = ''
    for state in atomic_states:
        n = state['n']
        l = state['l']
        kappa = state['kappa']
        occ = state['occ']
        core = str(state['core']).lower()
        string += f'      <atomicState n="{n}" l="{l}" kappa="{kappa}" occ="{occ}" core="{core}"/>\n'
    return string
