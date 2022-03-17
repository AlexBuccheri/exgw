""" Write to file
"""

def write_species_file_from_dict(species: dict) -> str:
    """
    Expect dict with top-level keys {'species', 'muffin_tin', 'atomic_states', 'basis'}

    <?xml version="1.0" encoding="UTF-8"?>
<spdb xsi:noNamespaceSchemaLocation="../../xml/species.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <sp chemicalSymbol="Ti" name="titanium" z="-22.0000" mass="87256.20311">
    <muffinTin rmin="0.100000E-05" radius="2.0000" rinf="25.7965" radialmeshPoints="600"/>
    <atomicState n="1" l="0" kappa="1" occ="2.00000" core="true"/>
    <atomicState n="2" l="0" kappa="1" occ="2.00000" core="true"/>
    <atomicState n="2" l="1" kappa="1" occ="2.00000" core="true"/>
    <atomicState n="2" l="1" kappa="2" occ="4.00000" core="true"/>
    <atomicState n="3" l="0" kappa="1" occ="2.00000" core="false"/>
    <atomicState n="3" l="1" kappa="1" occ="2.00000" core="false"/>
    <atomicState n="3" l="1" kappa="2" occ="4.00000" core="false"/>
    <atomicState n="3" l="2" kappa="2" occ="2.00000" core="false"/>
    <atomicState n="4" l="0" kappa="1" occ="2.00000" core="false"/>
    <basis>
      <default type="lapw" trialEnergy="0.1500" searchE="false"/>

      <custom l="0" type="lapw" trialEnergy="-1.83220324630948" searchE="false"/>
      <lo l="0">
        <wf matchingOrder="0" trialEnergy="-1.83220324630948" searchE="false"/>
        <wf matchingOrder="1" trialEnergy="-1.83220324630948" searchE="false"/>
      </lo>
      <lo l="0">
        <wf matchingOrder="1" trialEnergy="-1.83220324630948" searchE="false"/>
        <wf matchingOrder="2" trialEnergy="-1.83220324630948" searchE="false"/>
      </lo>
      <lo l="0">
        <wf matchingOrder="0" trialEnergy="-1.83220324630948" searchE="false"/>
        <wf matchingOrder="0" trialEnergy="3.48339510536654" searchE="false"/>
      </lo>
      <lo l="0">
        <wf matchingOrder="0" trialEnergy="3.48339510536654" searchE="false"/>
        <wf matchingOrder="1" trialEnergy="3.48339510536654" searchE="false"/>
      </lo>
        </basis>
  </sp>
</spdb>

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


    # Presort apws into l-channels

    # Presort LOs into l-channels

    # "<basis>\n "
    # species_str += function_string(species['default'])
    # for l in range(0, l_max +1):
    #     species_str += function_string(species['custom'][l])
    #     species_str += local_orbitals_string(species['custom'][l])

    species_str += """  </basis>
  </sp>
</spdb>"""

    return species_str


def local_orbitals_string():
    """
    Expect
    {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},
           {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},
    :return:
    """
    pass


def local_orbital_string():
    """

    :return:
    """
    pass


def function_string(function: dict):
    """

    :param function:
    :return:
    """
    type = str(function['type'][0])
    trial_energy = str(function['trialEnergy'][0])
    search_e = str(function['searchE'][0]).lower()
    string = f'<default type="{type}" trialEnergy="{trial_energy}" searchE="{search_e}"/> \n'
    return string


def atomic_states_string(atomic_states: dict) -> str:
    """
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
