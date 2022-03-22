""" Construct an optimised basis, containing high energy local orbitals
for use in highly-converged GW calculations.
"""
import copy
import warnings
from typing import List
import numpy as np


def maximum_pqn_per_valence_orbital(atomic_states: List[dict]) -> np.ndarray:
    """ Find the maximum orbital per l-channel.

    Index l of pqn[l] corresponds to the l-channel.

    :param atomic_states: Atomic states returned from species parser.
    :param l_max: The maximum l-value to return the principal QN for.
    If an orbital of given l is not in the valence, zero is returned.
    :return: Largest principal quantum number per l-channel
    """
    l_max = max([state['l'] for state in atomic_states])
    valence_states = [state for state in atomic_states if not state['core']]
    pqn = np.zeros(shape=l_max + 1, dtype=np.int)
    for state in valence_states:
        n, l = state['n'], state['l']
        pqn[l] = max(pqn[l], n)
    return pqn


def max_nodes_per_valence_orbital(atomic_states: List[dict]) -> dict:
    """

    :param atomic_states:
    :return:
    """
    pqn = maximum_pqn_per_valence_orbital(atomic_states)
    l_max_plus_one = len(pqn)
    nodes = {}

    for l in range(0, l_max_plus_one):
        nodes[l] = n_radial_nodes(pqn[l], l)

    return nodes


def max_nodes_per_conduction_orbital(lo_block: List[dict]) -> dict:
    """ Get the maximum number of nodes per conduction orbital.

    Conduction states not specified in the atomicState tag, therefore I need to count
    them from the lo block in the parsed basis dictionary.

    They also won't have any principal quantum numbers associated with them,
    so simply count them form 0, and that index will be the number of nodes.

    :param :
    :return
    """
    l_max = max([lo['l'] for lo in lo_block])

    # Sort LOs by l-value
    l_to_index = {l: [] for l in range(0, l_max + 1)}
    for i, lo in enumerate(lo_block):
        l_value = lo['l']
        l_to_index[l_value].append(i)

    # TODO Alex - Ask this question, and for Ti, what it means
    # to have a function in the valence, but its trial energy start at 0.00
    # TODO ALEX NOTE, for conduction states, one can't really assume
    # For valence we ASSUME the species file is constructed properly
    # and just start filling according to the function that SHOULD
    # be in the file
    # For conduction, we can only count. Think I am accidently
    # getting this right due to dict useage
    # Should be judging the number of nodes w.r.t the unique energies
    # not the actually number of LOs (same energy, but different matching numbers)
    # Yes, think this is correct

    # For valence, we ASSUME we have the LOs included to correctly describe
    # the core=false states in atomicState

    # Identify l-channels containing LOs that are ONLY conduction states.
    # For example, 5s might be conduction, but its l-channel contains
    # valence too, hence ignore l=0 here.
    pure_conduction_channel = {}
    for l in range(0, l_max + 1):
        indices = l_to_index[l]
        # For each LO, take the largest trial energy of the matching orders
        energies = [max(lo_block[i]['trialEnergy']) for i in indices]
        # Conduction states start at ~ 0 Ha
        if min(energies) >= -0.01:
            # As functions start at 0 nodes
            # TODO(Alex) Need to verify this
            # Functions with same energies but different matching orders
            # assumed to have the same number of nodes
            n_los = len(set(energies))
            max_nodes = n_los - 1
            pure_conduction_channel[l] = max_nodes

    return pure_conduction_channel


def max_nodes_per_orbital_channel(species: dict):
    """

    :param species:
    :return:
    """
    max_v_nodes = max_nodes_per_valence_orbital(species['atomic_states'])
    max_c_nodes = max_nodes_per_conduction_orbital(species['basis']['lo'])

    # Maybe this won't be an issue in valid species files?
    valence_l = set(max_v_nodes)
    conduction_l = set(max_c_nodes)
    for l in valence_l.intersection(conduction_l):
        if max_v_nodes[l] != max_c_nodes[l]:
            print('Basis details:')
            for lo in species['basis']['lo']:
                if lo['l'] == l:
                    print(lo)
            raise ValueError(f"Cannot distinguish this l={l} channel between valence and conduction")

    return {**max_v_nodes, **max_c_nodes}


def n_radial_nodes(pqn: int, l: int):
    """ Number of nodes in a radial function nl.
    :param pqn: principal QN
    :param l: Orbital angular momentum
    :return: Number of radial nodes
    """
    return pqn - l - 1


def filter_lowest_lo_recommendations(max_nodes: dict) -> np.ndarray:
    """ Return first index of recommendation energies for LOs that are not already in the basis.

    This routine filters according to the number of radial nodes, rather than energies.

    :param max_nodes: Dict of max nodes per l-channel.
    :return: Starting index per l-channel, for LO recommendations.
    """
    l_max = max(list(max_nodes))
    indices = np.empty(shape=(l_max + 1), dtype=np.int)

    for l in range(0, l_max + 1):
        try:
            # LO with most nodes, already in basis = max_nodes[l]
            # so add one.
            i_min = max_nodes[l] + 1
        except KeyError:
            # If l-channel not specified, set to zero
            i_min = 0
        indices[l] = int(i_min)

    return indices


def filter_highest_lo_recommendations(lo_cutoff: dict, recommendations: np.ndarray) -> np.ndarray:
    """ Filter out LO recommendations above a certain LO cutoff

    One is added to the index because array[:n] will return up to element n-1, and we
    want to include element n.

    If the cut-off for the l-channel is not defined, 0 is returned.
    NOTE: Perhaps np.nan would be better.

    :param lo_cutoff:
    :param recommendations:
    :return:
    """
    l_max_plus_one, nodes_max_plus_one = recommendations.shape
    indices = np.empty(shape=l_max_plus_one, dtype=np.int)
    # If an l-channel cut-off is not specified, it implies one does NOT want to add any high-energy orbitals
    # hence initialise to zero.
    indices.fill(0)

    for l, cutoff in lo_cutoff.items():
        indices[l] = np.max(np.argwhere(recommendations[l, :] <= cutoff)) + 1

    return indices


def serialised_local_orbitals(l_value: int, linearisation_energies: np.ndarray) -> List[dict]:
    """ Create serialised local orbital data, following a fixed pattern.

    This pattern is appropriate for high-energy local orbitals.

      <lo l="3">
        <wf matchingOrder="0" trialEnergy="3.6155" searchE="false"/>
        <wf matchingOrder="1" trialEnergy="3.6155" searchE="false"/>
      </lo>
      <lo l="3">
        <wf matchingOrder="1" trialEnergy="3.6155" searchE="false"/>
        <wf matchingOrder="2" trialEnergy="3.6155" searchE="false"/>
      </lo>

    :return:
    """
    local_orbitals = []
    for energy in linearisation_energies:
        local_orbitals.append({'l': l_value, 'matchingOrder': [0, 1], 'trialEnergy': [energy, energy], 'searchE': [False, False]})
        local_orbitals.append({'l': l_value, 'matchingOrder': [1, 2], 'trialEnergy': [energy, energy], 'searchE': [False, False]})
    return local_orbitals


def serialise_optimised_los(default_los: List[dict], conduction_los: List[List[dict]], l_max: int):
    """

    :param default_basis:
    :param conduction_los:
    :param l_max:
    :return:
    """
    # Sort default LOs by l-value
    l_to_index = {l: [] for l in range(0, l_max + 1)}
    for i, lo in enumerate(default_los):
        l_value = lo['l']
        l_to_index[l_value].append(i)

    optimised_los = []
    for l in range(0, l_max + 1):
        # Default LOs
        for i in l_to_index[l]:
            optimised_los.append(default_los[i])
        # Conduction LOs
        for lo in conduction_los[l]:
            optimised_los.append(lo)

    return optimised_los


# TODO(Alex) Check this explanation
def construct_optimised_basis(default_basis: dict,
                              lo_recommendations: np.ndarray,
                              l_max: int,
                              lo_cutoff: dict) -> dict:
    """ Return the local orbitals defined up to the LO cutoff, with trial energies
    set according to LO recommendations.

    Difficult part is filtering LO recommendations such that one doesn't introduce LOs
    into the new basis which are already present. The most straightforward way to do
    this is not be comparing linearisation energies, but by counting nodes.

    Description of How This Routine Works
    -------------------------------------
    For example, with Ti:
        <atomicState n="3" l="0" kappa="1" occ="2.00000" core="false"/>
        <atomicState n="3" l="1" kappa="1" occ="2.00000" core="false"/>
        <atomicState n="3" l="1" kappa="2" occ="4.00000" core="false"/>
        <atomicState n="3" l="2" kappa="2" occ="2.00000" core="false"/>
        <atomicState n="4" l="0" kappa="1" occ="2.00000" core="false"/>

    defines the valence as 3s 3p 3d 4s. This does not guarantee that the corresponding
    LOs are explicitly defined in the species file.

    :param default_basis: Default basis in serialised form.
    :param lo_recommendations: LO energy recommendations, with shape = (l_max+1, n_nodes+1)
    :return: Dictionary of the default_basis, with extra LOs added from l=[0, l_max],
    according to the LO recommendation energies and the lo_cutoff.
    """
    recommendations_l_max, recommendations_node_max = [x - 1 for x in lo_recommendations.shape]

    if recommendations_l_max > l_max:
        raise ValueError(f'LO recommendations go up to l={recommendations_l_max}, however'
                         f'l_max requested is {l_max}')

    for l, cutoff in lo_cutoff.items():
        max_energy = lo_recommendations[l, -1]
        if cutoff > max_energy:
            raise ValueError(f'For l={l}, the LO cutoff exceeds the maximum energy '
                             f'in the LO recommendations.')

    max_nodes = max_nodes_per_orbital_channel(default_basis)

    first_indices = filter_lowest_lo_recommendations(max_nodes)
    # assert first_indices.shape == len(max_nodes), 'l_max for first_indices set by LOs present in the basis'

    # If l_max exceeds that already present in the basis, pad the first_indices
    # with zeros
    if first_indices.shape[0] < (l_max + 1):
        size_diff = (l_max + 1) - first_indices.shape[0]
        padding = np.zeros(shape=size_diff, dtype=np.int)
        first_indices = np.concatenate((first_indices, padding), axis=0)

    last_indices = filter_highest_lo_recommendations(lo_cutoff, lo_recommendations)
    assert last_indices.shape[0] == lo_recommendations.shape[0], 'l_max for last_indices set by lo_recommendations'

    # Create new LOs with the filtered LO recommendations
    # If l-channel has no cut-off, then last_indices[l] = 0, which kills its contribution
    los_by_lvalue = [[] for _ in range(0, l_max + 1)]
    for l in range(0, l_max + 1):
        i1 = first_indices[l]
        i2 = last_indices[l]
        energies = np.copy(lo_recommendations[l, i1:i2])
        los_by_lvalue[l] = serialised_local_orbitals(l, energies)

    # Inject new los into the basis, and return the new basis dictionary
    optimised_basis = copy.deepcopy(default_basis)
    optimised_basis['basis']['lo'] = serialise_optimised_los(default_basis['basis']['lo'], los_by_lvalue, l_max)

    return optimised_basis




# Mapping in lo-recommendations from nodes (used as index) to nl
# nodes (index)
#       0        1s  2p  3d
#       1        2s  3p  4d
#       2        3s  4p  5d
#       3        4s  5p  6d
#       4        5s  6p  7d
#
#     Can then parse LO recommendations and add new LOs into each l-channel
#     Write species file back out
#
#     Take either the number of LOs per l-channel OR the energy cutoff per l-channel
#     where lo_cutoff = {0: 150, 1: 150, 2: 150, 3: 150, 4: 150, 5: 150}
#     and
#     n_los = {0: 8, 1: 8, 2: 8, 3: 5, 4: 5, 5: 2}.
#     and the the number of LOs per channel includes ALL non-core LOs. Else this shit gets messy.
#     Then one can get number of LOs for default and optimised basis sets, to get the extra number of LOs added for GW.



    # TODO(Alex) Move this description
    # Each recommendations[l, :] will start at 0 nodes for all l, therefore we map the principal quantum number
    # of the highest-energy valence orbital in the default basis to number of nodes and take i+1th node to be
    # the first LO recommendation energy for that l-channel.
    #
    # This way, we (hopefully) avoid adding ~ equivalent LOs to the basis, which at least
    # hinders the SCF convergence and at most, leads to linear dependence (and a crash).
    #
    # Example of the mapping:
    # recommendations[0, :] = 0, 1, 2, 3 ... == 1s, 2s, 3s, 4s ...
    # recommendations[1, :] = 0, 1, 2, 3 ... == 2p, 3p, 4p, 5p ...
    # recommendations[2, :] = 0, 1, 2, 3 ... == 3d, 4d, 5d, 6d ...
    # ...
    # recommendations[l_max, :] = 0, 1, 2, 3 ...

    # TODO(Alex)
    #  Should also add something to count the number of LOs in the basis => Can apply to the default and to the final basis

