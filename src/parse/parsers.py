"""Tools for parsing local orbitals
"""
import numpy as np


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


def parse_species_xml():
    pass
