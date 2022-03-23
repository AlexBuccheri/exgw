from exgw.src.parse.parsers import parse_species_xml


def test_parse_species_xml():
    """ Test parsing of species.xml files.
    """
    assert isinstance(species_str, str), ("Expect species parser to handle strings of XML data, "
                                          "due to use of decorator")

    species_dict = parse_species_xml(species_str)

    print(species_dict)

    assert set(species_dict) == {'species', 'muffin_tin', 'atomic_states', 'basis'}, 'Top level species file keys'
    assert species_dict['species'] == {'chemicalSymbol': 'Zn', 'name': 'zinc', 'z': -30.0, 'mass': 119198.678}
    assert species_dict['muffin_tin'] == {'rmin': 1e-06, 'radius': 2.0, 'rinf': 21.8982, 'radialmeshPoints': 600.0}

    assert isinstance(species_dict['atomic_states'], list), 'Atomic states stored as a list'
    atomic_states = [{'n': 1, 'l': 0, 'kappa': 1, 'occ': 2.00000, 'core': True},
                     {'n': 2, 'l': 0, 'kappa': 1, 'occ': 2.00000, 'core': True},
                     {'n': 2, 'l': 1, 'kappa': 1, 'occ': 2.00000, 'core': True},
                     {'n': 2, 'l': 1, 'kappa': 2, 'occ': 4.00000, 'core': True},
                     {'n': 3, 'l': 0, 'kappa': 1, 'occ': 2.00000, 'core': False},
                     {'n': 3, 'l': 1, 'kappa': 1, 'occ': 2.00000, 'core': False},
                     {'n': 3, 'l': 1, 'kappa': 2, 'occ': 4.00000, 'core': False},
                     {'n': 3, 'l': 2, 'kappa': 2, 'occ': 4.00000, 'core': False},
                     {'n': 3, 'l': 2, 'kappa': 3, 'occ': 6.00000, 'core': False},
                     {'n': 4, 'l': 0, 'kappa': 1, 'occ': 2.00000, 'core': False}]
    assert species_dict['atomic_states'] == atomic_states

    basis = species_dict['basis']
    assert set(basis) == {'default', 'custom', 'lo'}, 'Keys for basis'

    assert basis['default'] == [{'type': 'lapw', 'trialEnergy': 0.1500, 'searchE': True}]

    # Custom apw, lapw or apw+lo
    assert basis['custom'] == [{'l': 0, 'type': 'lapw', 'trialEnergy':  1.35670550183736, 'searchE': False},
                               {'l': 1, 'type': 'lapw', 'trialEnergy': -2.69952312512447, 'searchE': False},
                               {'l': 2, 'type': 'lapw', 'trialEnergy': 0.00,  'searchE': False},
                               {'l': 3, 'type': 'lapw', 'trialEnergy': 1.000, 'searchE': False},
                               {'l': 4, 'type': 'lapw', 'trialEnergy': 1.000, 'searchE': False},
                               {'l': 5, 'type': 'lapw', 'trialEnergy': 1.000, 'searchE': False}]

    # All explicitly specified LOs
    los = [{'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [-4.37848525995355, -4.37848525995355],
            'searchE': [False, False]},
           {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [1.35670550183736, 1.35670550183736],
            'searchE': [False, False]},
           {'l': 0, 'matchingOrder': [0, 0], 'trialEnergy': [1.35670550183736, -4.37848525995355],
            'searchE': [False, False]},
           {'l': 0, 'matchingOrder': [1, 2], 'trialEnergy': [1.35670550183736, 1.35670550183736],
            'searchE': [False, False]},
           {'l': 1, 'matchingOrder': [0, 1], 'trialEnergy': [-2.69952312512447, -2.69952312512447],
            'searchE': [False, False]},
           {'l': 1, 'matchingOrder': [1, 2], 'trialEnergy': [-2.69952312512447, -2.69952312512447],
            'searchE': [False, False]},
           {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},
           {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},
           {'l': 3, 'matchingOrder': [0, 1], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
           {'l': 3, 'matchingOrder': [1, 2], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
           {'l': 4, 'matchingOrder': [0, 1], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
           {'l': 4, 'matchingOrder': [1, 2], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
           {'l': 5, 'matchingOrder': [0, 1], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
           {'l': 5, 'matchingOrder': [1, 2], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]}]

    assert len(basis['lo']) == 14, "Number of explicitly-defined local orbitals"
    assert set(basis['lo'][0]) == {'l', 'matchingOrder', 'trialEnergy', 'searchE'}, \
        "Attributes defining a local orbital"
    assert basis['lo'] == los


species_str = """<?xml version="1.0" encoding="utf-8"?>
<spdb xsi:noNamespaceSchemaLocation="../../xml/species.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <sp chemicalSymbol="Zn" name="zinc" z="-30.0000" mass="119198.6780">
    <muffinTin rmin="0.100000E-05" radius="2.0000" rinf="21.8982" radialmeshPoints="600"/>
    <atomicState n="1" l="0" kappa="1" occ="2.00000" core="true"/>
    <atomicState n="2" l="0" kappa="1" occ="2.00000" core="true"/>
    <atomicState n="2" l="1" kappa="1" occ="2.00000" core="true"/>
    <atomicState n="2" l="1" kappa="2" occ="4.00000" core="true"/>
    <atomicState n="3" l="0" kappa="1" occ="2.00000" core="false"/>
    <atomicState n="3" l="1" kappa="1" occ="2.00000" core="false"/>
    <atomicState n="3" l="1" kappa="2" occ="4.00000" core="false"/>
    <atomicState n="3" l="2" kappa="2" occ="4.00000" core="false"/>
    <atomicState n="3" l="2" kappa="3" occ="6.00000" core="false"/>
    <atomicState n="4" l="0" kappa="1" occ="2.00000" core="false"/>
    <basis>
      <default type="lapw" trialEnergy="0.1500" searchE="true"/>

      <custom l="0" type="lapw" trialEnergy="1.35670550183736" searchE="false"/>
      <lo l="0">
        <wf matchingOrder="0" trialEnergy="-4.37848525995355" searchE="false"/>
	<wf matchingOrder="1" trialEnergy="-4.37848525995355" searchE="false"/>
      </lo>
      <lo l="0">
        <wf matchingOrder="0" trialEnergy="1.35670550183736" searchE="false"/>
        <wf matchingOrder="1" trialEnergy="1.35670550183736" searchE="false"/>
      </lo>
      <lo l="0">
        <wf matchingOrder="0" trialEnergy="1.35670550183736" searchE="false"/>
	<wf matchingOrder="0" trialEnergy="-4.37848525995355" searchE="false"/>
      </lo>
      <lo l="0">
        <wf matchingOrder="1" trialEnergy="1.35670550183736" searchE="false"/>
        <wf matchingOrder="2" trialEnergy="1.35670550183736" searchE="false"/>
      </lo>

      <custom l="1" type="lapw" trialEnergy="-2.69952312512447" searchE="false"/>
      <lo l="1">
        <wf matchingOrder="0" trialEnergy="-2.69952312512447" searchE="false"/>
        <wf matchingOrder="1" trialEnergy="-2.69952312512447" searchE="false"/>
      </lo>
      <lo l="1">
	<wf matchingOrder="1" trialEnergy="-2.69952312512447" searchE="false"/>
	<wf matchingOrder="2" trialEnergy="-2.69952312512447" searchE="false"/>
      </lo>

      <custom l="2" type="lapw" trialEnergy="0.00" searchE="false"/>
      <lo l="2">
	<wf matchingOrder="0" trialEnergy="0.00" searchE="false"/>
        <wf matchingOrder="1" trialEnergy="0.00" searchE="false"/>
      </lo>
      <lo l="2">
	<wf matchingOrder="1" trialEnergy="0.00" searchE="false"/>
        <wf matchingOrder="2" trialEnergy="0.00" searchE="false"/>
      </lo>

      <custom l="3" type="lapw" trialEnergy="1.000" searchE="false"/>
      <lo l="3">
	<wf matchingOrder="0" trialEnergy="1.000" searchE="false"/>
	<wf matchingOrder="1" trialEnergy="1.000" searchE="false"/>
      </lo>
      <lo l="3">
        <wf matchingOrder="1" trialEnergy="1.000" searchE="false"/>
        <wf matchingOrder="2" trialEnergy="1.000" searchE="false"/>
      </lo>

      <custom l="4" type="lapw" trialEnergy="1.000" searchE="false"/>
      <lo l="4">
	<wf matchingOrder="0" trialEnergy="1.000" searchE="false"/>
	<wf matchingOrder="1" trialEnergy="1.000" searchE="false"/>
      </lo>
      <lo l="4">
        <wf matchingOrder="1" trialEnergy="1.000" searchE="false"/>
        <wf matchingOrder="2" trialEnergy="1.000" searchE="false"/>
      </lo>

      <custom l="5" type="lapw" trialEnergy="1.000" searchE="false"/>
      <lo l="5">
	<wf matchingOrder="0" trialEnergy="1.000" searchE="false"/>
	<wf matchingOrder="1" trialEnergy="1.000" searchE="false"/>
      </lo>
      <lo l="5">
        <wf matchingOrder="1" trialEnergy="1.000" searchE="false"/>
        <wf matchingOrder="2" trialEnergy="1.000" searchE="false"/>
      </lo>

    </basis>
  </sp>
</spdb>
"""
