""" Test writing serialised species data to XML
"""
from exgw.src.parse.parsers import parse_species_xml

from exgw.src.write.species import species_xml_str_from_dict


def test_write_species_file_from_dict():
    """ Uncomment the print statement to confirm printing.
    Note, string comparison unit tests are not robust, hence why no assert.
    :return:
    """
    species_dict = parse_species_xml(species_str)
    species_string = species_xml_str_from_dict(species_dict)
    print(species_string)


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
