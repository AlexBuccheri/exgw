import numpy as np

from src.parse.parsers import parse_species_xml, parse_lorecommendations

from src.basis.optimised_basis import construct_optimised_basis, maximum_pqn_per_valence_orbital, \
    filter_lowest_lo_recommendations, filter_highest_lo_recommendations, max_nodes_per_valence_orbital, \
    max_nodes_per_conduction_orbital, max_nodes_per_orbital_channel, n_radial_nodes


def test_maximum_valence_per_orbital():
    # Output expected from a parsed species file for atomicStates
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

    # l_max can be any size
    pqn = maximum_pqn_per_valence_orbital(atomic_states)
    assert (pqn == [4, 3, 3]).all(), "Expect 4s, 3p, 3d"


def test_max_nodes_per_valence_orbital():
    # Output expected from a parsed species file for atomicStates
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
    l_max = 2

    nodes = max_nodes_per_valence_orbital(atomic_states)
    l_channels = {0, 1, 2}
    assert set(nodes) == l_channels
    assert nodes == {0: 3, 1: 1, 2: 0}, "Nodes 3, 1, 0"

    pqn = maximum_pqn_per_valence_orbital(atomic_states)
    assert nodes == {l: n_radial_nodes(pqn[l], l) for l in range(0, l_max + 1)}, \
        "Max number of nodes should equal (pqn - l - 1)"


def test_max_nodes_per_conduction_orbital():
    """ Construct an optimised basis for Ti (from TiO2).
    """
    lo_basis_ti = [
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [-4.3784852599536, -4.3784852599536],
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

    max_nodes = max_nodes_per_conduction_orbital(lo_basis_ti)

    l_channels = {2, 3, 4, 5}
    assert set(max_nodes) == l_channels

    # max nodes per pure conduction channel
    assert max_nodes[2] == 0, "Functions 3d and 4d with 0 and 1 nodes, respectively"
    assert max_nodes[3] == 0, "Functions 4f and 5f with 0 and 1 nodes, respectively"
    assert max_nodes[4] == 0, "Functions 5g and 6g with 0 and 1 nodes, respectively"
    assert max_nodes[5] == 0, "Functions 7h and 8h with 0 and 1 nodes, respectively"


def test_max_nodes_per_orbital_channel():
    ground_state_basis_ti = parse_species_xml(species_str)
    max_nodes = max_nodes_per_orbital_channel(ground_state_basis_ti)

    assert max_nodes == {0: 3, 1: 1, 2: 0, 3: 0, 4: 0, 5: 0}


def test_filter_lowest_lo_recommendations():
    # From (n_nodes + l + 1), LOs present in basis = 4s 3p 3d 4f 5g 6h
    max_nodes = {0: 3,
                 1: 1,
                 2: 0,
                 3: 0,
                 4: 0,
                 5: 0}

    message = """
    As the valence/conduction is (4s, 3p, 3d) (4f 5g 6h), I expect to get recommendations starting from
    (5s, 4p, 4d) (5f 6g 7h) -> nodes/indices = (4, 2, 1, 1, 1, 1)
    """
    # Essentially, this routine is now trivial.
    indices = filter_lowest_lo_recommendations(max_nodes)
    assert (indices == [4, 2, 1, 1, 1, 1]).all(), message


def test_application_to_lo_recommendations(tmpdir):
    indices = np.array([4, 2, 1, 1, 1, 1])

    lorec_file = tmpdir / "lorecommendations.txt"
    lorec_file.write(lo_recommendations)
    recommendations_ti = parse_lorecommendations(str(lorec_file), ['ti', 'o'], l_max=7, node_max=20)['ti']
    assert recommendations_ti.shape == (8, 21), 'l_max+1, n_nodes+1'

    lowest_energies = []
    for l in range(0, len(indices)):
        i = indices[l]
        lowest_energies.append(recommendations_ti[l, i])

    assert lowest_energies == [12.9176469892837, 4.05064453003636, 4.58295441473611,
                               10.014835866122, 14.8600135756357, 19.7520553049321]


def test_filter_highest_lo_recommendations(tmpdir):
    # Would be better to retrieve this from the file
    l_max = 7
    node_max = 20

    lorec_file = tmpdir / "lorecommendations.txt"
    lorec_file.write(lo_recommendations)
    recommendations_ti = parse_lorecommendations(str(lorec_file), ['ti', 'o'], l_max=7, node_max=20)['ti']
    assert recommendations_ti.shape == (l_max + 1, node_max + 1)

    energy_cutoff = {0: 150}

    indices = filter_highest_lo_recommendations(energy_cutoff, recommendations_ti)
    assert len(indices) == l_max + 1
    assert (indices == [11, 0, 0, 0, 0, 0, 0, 0]).all(), "Only cut off the l=0 channel"

    # Returns index or i+1 th value, such that recommendations_ti[l][:indices[l]] returns
    # up to and including the cut-off
    l_value = 0
    refined_recommendations = recommendations_ti[l_value][:indices[l_value]]
    assert refined_recommendations[-1] <= energy_cutoff[l_value], "Demonstrating HOW to use the indices"
    assert recommendations_ti[l_value][indices[l_value]] > energy_cutoff[
        l_value], "Demonstrating how NOT to use the indices"

    l_value = 1
    refined_recommendations = recommendations_ti[l_value][:indices[l_value]]
    assert not refined_recommendations.any(), "If an l-channel cutoff is not defined, 0 is returned" \
                                              "so do not use the index"


def test_construct_optimised_basis(tmpdir):
    """ Construct an optimised basis for Ti (from TiO2).
    """
    # Ground state basis
    default_basis_ti = parse_species_xml(species_str)

    # LO recommendations for Ti
    lorec_file = tmpdir / "lorecommendations.txt"
    lorec_file.write(lo_recommendations)
    l_max = 7
    node_max = 20
    recommendations = parse_lorecommendations(str(lorec_file), ['ti', 'o'], l_max=l_max, node_max=node_max)
    recommendations_ti = recommendations['ti']

    # LO cut-off, for l-channels 0, 1 and 2
    energy_cutoff_ti = {0: 150, 1: 120, 2: 80}

    optimised_basis: dict = construct_optimised_basis(default_basis_ti, recommendations_ti, l_max, energy_cutoff_ti)

    reference = [
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [-4.37848525995355, -4.37848525995355],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [1.35670550183736, 1.35670550183736],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [0, 0], 'trialEnergy': [1.35670550183736, -4.37848525995355],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [1, 2], 'trialEnergy': [1.35670550183736, 1.35670550183736],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [12.9176469892837, 12.9176469892837],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [1, 2], 'trialEnergy': [12.9176469892837, 12.9176469892837],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [26.1778761935082, 26.1778761935082],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [1, 2], 'trialEnergy': [26.1778761935082, 26.1778761935082],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [42.947252809507, 42.947252809507], 'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [1, 2], 'trialEnergy': [42.947252809507, 42.947252809507], 'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [63.096841739398, 63.096841739398], 'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [1, 2], 'trialEnergy': [63.096841739398, 63.096841739398], 'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [86.5450984374082, 86.5450984374082],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [1, 2], 'trialEnergy': [86.5450984374082, 86.5450984374082],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [113.228758144247, 113.228758144247],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [1, 2], 'trialEnergy': [113.228758144247, 113.228758144247],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [0, 1], 'trialEnergy': [143.109614979104, 143.109614979104],
         'searchE': [False, False]},
        {'l': 0, 'matchingOrder': [1, 2], 'trialEnergy': [143.109614979104, 143.109614979104],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [0, 1], 'trialEnergy': [-2.69952312512447, -2.69952312512447],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [1, 2], 'trialEnergy': [-2.69952312512447, -2.69952312512447],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [0, 1], 'trialEnergy': [4.05064453003636, 4.05064453003636],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [1, 2], 'trialEnergy': [4.05064453003636, 4.05064453003636],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [0, 1], 'trialEnergy': [13.0713956122497, 13.0713956122497],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [1, 2], 'trialEnergy': [13.0713956122497, 13.0713956122497],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [0, 1], 'trialEnergy': [25.6716499475157, 25.6716499475157],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [1, 2], 'trialEnergy': [25.6716499475157, 25.6716499475157],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [0, 1], 'trialEnergy': [41.6170180964515, 41.6170180964515],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [1, 2], 'trialEnergy': [41.6170180964515, 41.6170180964515],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [0, 1], 'trialEnergy': [60.8160619242497, 60.8160619242497],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [1, 2], 'trialEnergy': [60.8160619242497, 60.8160619242497],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [0, 1], 'trialEnergy': [83.2059799685343, 83.2059799685343],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [1, 2], 'trialEnergy': [83.2059799685343, 83.2059799685343],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [0, 1], 'trialEnergy': [108.745073489527, 108.745073489527],
         'searchE': [False, False]},
        {'l': 1, 'matchingOrder': [1, 2], 'trialEnergy': [108.745073489527, 108.745073489527],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [0.0, 0.0], 'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [4.58295441473611, 4.58295441473611],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [4.58295441473611, 4.58295441473611],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [12.4039296587687, 12.4039296587687],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [12.4039296587687, 12.4039296587687],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [23.6106241836797, 23.6106241836797],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [23.6106241836797, 23.6106241836797],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [38.1112945017348, 38.1112945017348],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [38.1112945017348, 38.1112945017348],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [55.8297495749646, 55.8297495749646],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [55.8297495749646, 55.8297495749646],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [0, 1], 'trialEnergy': [76.7132045452432, 76.7132045452432],
         'searchE': [False, False]},
        {'l': 2, 'matchingOrder': [1, 2], 'trialEnergy': [76.7132045452432, 76.7132045452432],
         'searchE': [False, False]},
        {'l': 3, 'matchingOrder': [0, 1], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
        {'l': 3, 'matchingOrder': [1, 2], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
        {'l': 4, 'matchingOrder': [0, 1], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
        {'l': 4, 'matchingOrder': [1, 2], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
        {'l': 5, 'matchingOrder': [0, 1], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]},
        {'l': 5, 'matchingOrder': [1, 2], 'trialEnergy': [1.0, 1.0], 'searchE': [False, False]}]

    assert optimised_basis['basis']['lo'] == reference


# Mocked inputs

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

# For TiO2 computed with rgkmax = 8.0, ngridk="4 4 4" and RMT (Ti, O) = (1.80, 1.50)
lo_recommendations = """ Energy parameters
 ------------
 species           1
 l=           0
 n=           0  -259.369188082763     
 n=           1  -19.3034231232313     
 n=           2  -1.82516041130036     
 n=           3   3.49036592294616     
 n=           4   12.9176469892837     
 n=           5   26.1778761935082     
 n=           6   42.9472528095070     
 n=           7   63.0968417393980     
 n=           8   86.5450984374082     
 n=           9   113.228758144247     
 n=          10   143.109614979104     
 n=          11   176.165025006327     
 n=          12   212.371637815201     
 n=          13   251.708976162372     
 n=          14   294.165047633081     
 n=          15   339.730301333293     
 n=          16   388.394593224781     
 n=          17   440.150370786348     
 n=          18   494.992403716618     
 n=          19   552.915577327171     
 n=          20   613.915369774928     
 
 l=           1
 n=           0  -15.9036026797939     
 n=           1 -0.916594422041659     
 n=           2   4.05064453003636     
 n=           3   13.0713956122497     
 n=           4   25.6716499475157     
 n=           5   41.6170180964515     
 n=           6   60.8160619242497     
 n=           7   83.2059799685343     
 n=           8   108.745073489527     
 n=           9   137.418378471044     
 n=          10   169.214173057501     
 n=          11   204.115782614501     
 n=          12   242.114135788504     
 n=          13   283.205380937343     
 n=          14   327.382797301318     
 n=          15   374.640297242177     
 n=          16   424.974879064549     
 n=          17   478.383337710301     
 n=          18   534.862055554789     
 n=          19   594.408560312595     
 n=          20   657.020794765786     
 
 l=           2
 n=           0  0.503036444916332     
 n=           1   4.58295441473611     
 n=           2   12.4039296587687     
 n=           3   23.6106241836797     
 n=           4   38.1112945017348     
 n=           5   55.8297495749646     
 n=           6   76.7132045452432     
 n=           7   100.746323777240     
 n=           8   127.917770423832     
 n=           9   158.205335887679     
 n=          10   191.596864321575     
 n=          11   228.088577312084     
 n=          12   267.671847836793     
 n=          13   310.338729992569     
 n=          14   356.086278883842     
 n=          15   404.911058498023     
 n=          16   456.808740116681     
 n=          17   511.776805758468     
 n=          18   569.813298034584     
 n=          19   630.915841336001     
 n=          20   695.082556015792     
 
 l=           3
 n=           0   3.62239944277359     
 n=           1   10.0148358661220     
 n=           2   19.7679227638865     
 n=           3   32.7749704857271     
 n=           4   48.9795005294507     
 n=           5   68.3672361013944     
 n=           6   90.9104504725290     
 n=           7   116.575874130065     
 n=           8   145.353675720780     
 n=           9   177.241232724529     
 n=          10   212.226132813998     
 n=          11   250.299578163230     
 n=          12   291.459518761812     
 n=          13   335.701095551504     
 n=          14   383.018503665349     
 n=          15   433.409118053102     
 n=          16   486.870556523134     
 n=          17   543.399661471325     
 n=          18   602.994273288022     
 n=          19   665.652805860171     
 n=          20   731.373487195129     
 
 l=           4
 n=           0   6.31739245209088     
 n=           1   14.8600135756357     
 n=           2   26.4849482058817     
 n=           3   41.2788452338538     
 n=           4   59.2074468430280     
 n=           5   80.2608665274760     
 n=           6   104.443414687192     
 n=           7   131.742382030324     
 n=           8   162.137244542013     
 n=           9   195.623026175066     
 n=          10   232.199294647865     
 n=          11   271.858354584544     
 n=          12   314.594538999903     
 n=          13   360.406815182199     
 n=          14   409.292313604271     
 n=          15   461.247201312456     
 n=          16   516.269572586634     
 n=          17   574.357747868165     
 n=          18   635.509497908624     
 n=          19   699.723150838476     
 n=          20   766.997415944937     
 
 l=           5
 n=           0   9.20446124429451     
 n=           1   19.7520553049321     
 n=           2   33.1720095758415     
 n=           3   49.6929498889539     
 n=           4   69.3171738083830     
 n=           5   92.0318503739110     
 n=           6   117.840278508168     
 n=           7   146.750243005582     
 n=           8   178.753137678429     
 n=           9   213.836002740462     
 n=          10   251.997089627681     
 n=          11   293.236304503786     
 n=          12   337.548316983287     
 n=          13   384.929545599425     
 n=          14   435.379430265364     
 n=          15   488.896076029643     
 n=          16   545.476976587385     
 n=          17   605.120838096024     
 n=          18   667.826466940541     
 n=          19   733.592314310617     
 n=          20   802.417170704447     
 
 l=           6
 n=           0   12.3770850953162     
 n=           1   24.8730696981051     
 n=           2   40.0477889015186     
 n=           3   58.2584368201336     
 n=           4   79.5454525306208     
 n=           5   103.906223444436     
 n=           6   131.336929449987     
 n=           7   161.846200669672     
 n=           8   195.440607558900     
 n=           9   232.112942291757     
 n=          10   271.855304080245     
 n=          11   314.667774771156     
 n=          12   360.550069840482     
 n=          13   409.498315311272     
 n=          14   461.510295417779     
 n=          15   516.585639707090     
 n=          16   574.722962732585     
 n=          17   635.920600568705     
 n=          18   700.177671111939     
 n=          19   767.493296109274     
 n=          20   837.866390218539     
 
 l=           7
 n=           0   15.8641422436787     
 n=           1   30.2902093404854     
 n=           2   47.2007036798467     
 n=           3   67.0826308545680     
 n=           4   90.0109786527877     
 n=           5   115.999858477713     
 n=           6   145.046716459017     
 n=           7   177.153451309478     
 n=           8   212.330238361273     
 n=           9   250.581060750811     
 n=          10   291.899809317721     
 n=          11   336.282140792353     
 n=          12   383.728964173645     
 n=          13   434.239726980987     
 n=          14   487.811619727578     
 n=          15   544.443323602092     
 n=          16   604.134530526312     
 n=          17   666.884172870597     
 n=          18   732.691129128751     
 n=          19   801.554779200506     
 n=          20   873.474453489839     
 
 species           2
 l=           0
 n=           0  -18.2591047939371     
 n=           1 -5.534299085382377E-002
 n=           2   6.76993107010801     
 n=           3   19.3008058710191     
 n=           4   36.7095261886706     
 n=           5   58.7646459628864     
 n=           6   85.3738258731782     
 n=           7   116.480467640519     
 n=           8   152.049558727031     
 n=           9   192.065572776831     
 n=          10   236.518429856541     
 n=          11   285.397340561776     
 n=          12   338.694502266150     
 n=          13   396.405479099324     
 n=          14   458.526461055309     
 n=          15   525.053814113973     
 n=          16   595.984767400710     
 n=          17   671.317185235181     
 n=          18   751.049177053000     
 n=          19   835.179105636313     
 n=          20   923.705603066417     
 
 l=           1
 n=           0  0.500499737249399     
 n=           1   6.00417947392677     
 n=           2   16.6244902325676     
 n=           3   31.9390492371309     
 n=           4   51.8487657000116     
 n=           5   76.2802837022488     
 n=           6   105.188456670102     
 n=           7   138.557350300250     
 n=           8   176.375329301630     
 n=           9   218.627309041331     
 n=          10   265.303650448348     
 n=          11   316.399828323890     
 n=          12   371.911054284842     
 n=          13   431.832469784859     
 n=          14   496.160762878792     
 n=          15   564.893465013808     
 n=          16   638.028239236460     
 n=          17   715.563073574882     
 n=          18   797.496348336346     
 n=          19   883.826661649663     
 n=          20   974.552773294797     
 
 l=           2
 n=           0   3.83945446883056     
 n=           1   12.1939562032803     
 n=           2   25.2842194468834     
 n=           3   42.9575431122334     
 n=           4   65.1545264514181     
 n=           5   91.8523535842225     
 n=           6   123.021685608380     
 n=           7   158.636452273438     
 n=           8   198.686443684450     
 n=           9   243.166259939108     
 n=          10   292.067590042401     
 n=          11   345.383667205643     
 n=          12   403.110997321794     
 n=          13   465.246610797274     
 n=          14   531.787367941305     
 n=          15   602.730809647179     
 n=          16   678.075070812743     
 n=          17   757.818471441704     
 n=          18   841.959522373783     
 n=          19   930.496970122767     
 n=          20   1023.42972546073     
 
 l=           3
 n=           0   6.98848256944531     
 n=           1   18.0747793354204     
 n=           2   33.6102477594338     
 n=           3   53.6519090661656     
 n=           4   78.1624370648352     
 n=           5   107.130413072972     
 n=           6   140.552426428783     
 n=           7   178.414973888309     
 n=           8   220.703412296845     
 n=           9   267.411709904519     
 n=          10   318.536956197423     
 n=          11   374.074380951663     
 n=          12   434.019572346479     
 n=          13   498.369939668691     
 n=          14   567.123429770478     
 n=          15   640.277951917003     
 n=          16   717.831747806278     
 n=          17   799.783420074093     
 n=          18   886.131731213631     
 n=          19   976.875577059800     
 n=          20   1072.01400141206     
 
 l=           4
 n=           0   10.5079862441597     
 n=           1   24.2341071131867     
 n=           2   42.1715722650949     
 n=           3   64.5499641069724     
 n=           4   91.3664953582778     
 n=           5   122.610336954317     
 n=           6   158.282514342210     
 n=           7   198.384268179873     
 n=           8   242.908248735095     
 n=           9   291.845949222348     
 n=          10   345.193857389491     
 n=          11   402.950233914381     
 n=          12   465.112186519857     
 n=          13   531.676864094118     
 n=          14   602.642394321105     
 n=          15   678.007287409829     
 n=          16   757.770085311167     
 n=          17   841.929519215749     
 n=          18   930.484536347643     
 n=          19   1023.43420413396     
 n=          20   1120.77768735372     
 
 l=           5
 n=           0   14.4830431697300     
 n=           1   30.8291872130391     
 n=           2   51.1527964656132     
 n=           3   75.8495711892589     
 n=           4   104.957254611350     
 n=           5   138.474612296734     
 n=           6   176.400302745340     
 n=           7   218.739126356488     
 n=           8   265.493126135740     
 n=           9   316.657900876879     
 n=          10   372.228449696562     
 n=          11   432.202751558381     
 n=          12   496.579707867895     
 n=          13   565.357499556312     
 n=          14   638.534278705924     
 n=          15   716.108715054758     
 n=          16   798.079713269793     
 n=          17   884.446226110917     
 n=          18   975.207325043735     
 n=          19   1070.36221245948     
 n=          20   1169.91017394726     
 
 l=           6
 n=           0   18.9374137083283     
 n=           1   37.9141871976703     
 n=           2   60.6239509995307     
 n=           3   87.6345520101954     
 n=           4   119.024600128231     
 n=           5   154.809339138549     
 n=           6   194.989656229806     
 n=           7   239.568461031240     
 n=           8   288.551302945596     
 n=           9   341.940035198566     
 n=          10   399.731966748238     
 n=          11   461.924208191579     
 n=          12   528.515636005759     
 n=          13   599.505551895389     
 n=          14   674.892798857927     
 n=          15   754.676181560091     
 n=          16   838.854769160395     
 n=          17   927.427760867938     
 n=          18   1020.39439649781     
 n=          19   1117.75399124681     
 n=          20   1219.50593969916     
 
 l=           7
 n=           0   23.8789253115928     
 n=           1   45.5109632964848     
 n=           2   70.6152727873199     
 n=           3   99.9431021745479     
 n=           4   133.614036585287     
 n=           5   171.661955073127     
 n=           6   214.095310941263     
 n=           7   260.916739097525     
 n=           8   312.131003894453     
 n=           9   367.743266887814     
 n=          10   427.755046970866     
 n=          11   492.164779170177     
 n=          12   560.970886524390     
 n=          13   634.172798234004     
 n=          14   711.770093818222     
 n=          15   793.762052479818     
 n=          16   880.147913049594     
 n=          17   970.927038634742     
 n=          18   1066.09885419154     
 n=          19   1165.66281049308     
 n=          20   1269.61840446143  
 
 """
