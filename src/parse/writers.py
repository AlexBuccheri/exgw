""" Write to file
"""
from typing import List


def write_species_file_from_dict(species: dict) -> str:
    """
    Expect dict with top-level keys {'species', 'muffin_tin', 'atomic_states', 'basis'}
    TODO(Alex) Document
    :param species:
    :return:
    """
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
    search_e  = species['basis']['default'][0]['searchE']
    species_str += f'      <default type="{type}" trialEnergy="{trial_energy}" searchE="{search_e}"/> \n\n'

    # lapw and any explicit local orbitals, per l-channel
    # Note, there should only be one l(apw) per l-channel
    print(species['basis']['custom'])
    for l in range(0, l_max +1):
        species_str += function_string(species['basis']['custom'][l])
        species_str += local_orbitals_string(los_by_lvalue[l])

    species_str += """    </basis>
  </sp>
</spdb>"""

    return species_str


def local_orbitals_string(los_l: List[dict]) -> str:
    """
    TODO(Alex) Document
    Expect
    {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},
           {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},
    :return:
    """
    string = ''
    for lo in los_l:
        string += local_orbital_string(lo)
    return string + '\n'


def local_orbital_string(lo: dict) -> str:
    """
    TODO(Alex) Document
    Generate a string of the form:
    <lo l="2">
	   <wf matchingOrder="0" trialEnergy="0.00" searchE="false"/>
       <wf matchingOrder="1" trialEnergy="0.00" searchE="false"/>
    </lo>

    :return:
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
    """
    TODO(Alex) Document
    :param function:
    :return:
    """
    l = function['l']
    type = function['type']
    trial_energy = str(function['trialEnergy'])
    search_e = str(function['searchE']).lower()
    string = f'      <custom l="{l}" type="{type}" trialEnergy="{trial_energy}" searchE="{search_e}"/> \n\n'
    return string


def atomic_states_string(atomic_states: dict) -> str:
    """
    TODO(Alex) Document
    :param atomic_states:
    :return:
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
