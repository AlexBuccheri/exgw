"""

"""
from typing import Optional, List
import numpy as np


def maximum_valence_per_orbital(atomic_states: List[dict], l_max: int) -> np.ndarray:
    """ Find the maximum orbital shell per l-channel

    :return: Largest principal quantum number per l-channel
    """
    valence_states = [state for state in atomic_states if not state['core']]
    pqn = np.zeros(shape=(l_max + 1), dtype=np.int)
    for state in valence_states:
        pqn[state['l']] = max(pqn[state['l']], state['n'])
    return pqn


def n_radial_nodes(pqn: int, l: int):
    return pqn - l - 1


def filter_lowest_lo_recommendations(max_valence_states: np.ndarray) -> np.ndarray:
    """ Return recommendation energies for LOs that are not already in the basis.

    Expect recommendations.shape = (l_max + 1, node_max + 1) contains all LO recommendations for the species.

    Filter according to radial nodes, rather than energies.

    Each recommendations[l, :] will start at 0 nodes.
    Map the principal quantum number of the high valence orbital (per l) to number of nodes
    and take i+1 to be the first LO recommendation energy for that l-channel.
    recommendations[0, :] = 0, 1, 2, 3 ... == 1s, 2s, 3s, 4s ...
    recommendations[1, :] = 0, 1, 2, 3 ... == 2p, 3p, 4p, 5p ...
    recommendations[2, :] = 0, 1, 2, 3 ... == 3d, 4d, 5d, 6d ...

    :param max_valence_states:
    :return:
    """
    indices = np.empty(shape=len(max_valence_states))

    for l in range(0, len(max_valence_states)):
        pqn = max_valence_states[l]
        i_min = n_radial_nodes(pqn, l) + 1
        if pqn == 0:
            i_min = 0
        indices[l] = i_min

    return indices


def filter_highest_lo_recommendations(lo_cutoff: dict, recommendations: np.ndarray) -> np.ndarray:
    """

    :param lo_cutoff:
    :param recommendations:
    :return:
    """
    l_max_plus_one, nodes_max_plus_one = recommendations.shape
    indices = np.empty(shape=l_max_plus_one, dtype=np.int)
    # Initialise with max index + 1 (which is constant for all l)
    indices.fill(nodes_max_plus_one)

    for l, cutoff in lo_cutoff.items():
        stuff = np.argwhere(recommendations[l, :] <= cutoff)
        indices[l] = np.max(np.argwhere(recommendations[l, :] <= cutoff))

    return indices


# TODO(Alex)
#  Should also add something to count the number of LOs in the basis => Can apply to the default and to the final basis


def construct_optimised_basis(default_basis: dict,
                              lo_recommendations: np.ndarray,
                              lo_cutoff=Optional[dict],
                              n_los=Optional[dict]) -> dict:
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
    LOs are explicitly defined in the species file

    Can then parse LO recommendations and add new LOs into each l-channel
    Write species file back out

    Take either the number of LOs per l-channel OR the energy cutoff per l-channel
    where lo_cutoff = {0: 150, 1: 150, 2: 150, 3: 150, 4: 150, 5: 150}
    and
    n_los = {0: 8, 1: 8, 2: 8, 3: 5, 4: 5, 5: 2}.
    and the the number of LOs per channel includes ALL non-core LOs. Else this shit gets messy.
    Then one can get number of LOs for default and optimised basis sets, to get the extra number of LOs added for GW.
    :return:
    """

    # List local orbitals in the valence
    # Note - no guarantee that the valence specified by atomicStates are actually explicitly present
    # But in a good species file, they should be
    # Furthermore, one only needs to then extract the highest valence orbital per l-channel
    # such that LO recommendations starts filling above it.

    # Need to pass in l_max values
    max_principal_qns = maximum_valence_per_orbital(default_basis['atomic_states'], l_max=7)

    indices = filter_lowest_lo_recommendations(max_principal_qns)
    indices = filter_highest_lo_recommendations(lo_cutoff, lo_recommendations)

    # Apply the indices to filter out the low end of lo_recommendations

    # Apply lo_cutoff to filter out the top end of lo_recommendations

    # Inject new los into the basis, with energies from lo_recommendations

    # Return the new basis dictionary

    # Need to write something to write this dictionary to a species file
