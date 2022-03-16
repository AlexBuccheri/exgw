""" Generate inputs with several LO channels, and multiple LOs per channel

Workflow Description:
* Need to run a converged ground state, with lo recommendations as true.
* Generate an input file for GW
* With the existing basis, LO recommendations, and LO channel settings, build a new basis file.
* Generate an appropriate submission script
* Generate a directory name
* Package this into a calculation type

 TODOs
# Separate results processing from input generation
# Functions:
# Generate run directory name
# Specify N LOs or cut-offs per channel
# Get LOs in for the optimised basis (that are not already present in the default basis)
"""
# External libs
import os.path
from pathlib import Path
from typing import List, Optional, Tuple

# This package
import numpy as np

from src.inputs.gw import GWInput
from src.parse.parsers import parse_lorecommendations, parse_species_xml

# TiO2 specific
from tio2.lo_spread.ground_state_xml import converged_input_xml



#  Variable (thing that varies between calculations) and directory.
class VarDir:
    def __init__(self, variable: any, directory: str):
        self.variable = variable
        self.directory = directory


def set_input() -> str:
    """ Compose converged ground state and GW input settings.
    :return: Input xml string.
    """
    # Converged ground state
    input_xml = converged_input_xml.replace('do="skip"', 'do="fromfile"')

    # GW
    gw = {'taskname': 'G0W0', 'nempty': 800, 'ngridq': [4, 4, 4], 'skipgnd': "false"}
    mixbasis = {'lmaxmb': 4, 'epsmb': 0.001, 'gmb': 1.0}
    freqgrid = {'nomeg': 32, 'freqmax': 1.0}
    barecoul = {'pwm': 2.0, 'stctol': 1e-16, 'barcevtol': 0.1}
    selfenergy = {'actype': 'pade', 'singularity': 'mpb'}
    gw_input = GWInput(gw=gw, mixbasis=mixbasis, freqgrid=freqgrid, barecoul=barecoul, selfenergy=selfenergy)

    # Inject GW settings into input
    input_xml = input_xml.format(GW_INPUT=gw_input.to_xml_str())

    return input_xml


def calc_lmax55_locut100() -> VarDir:
    """ Define a calculation

    Same cutoff for each channel.
    :return:
    """
    lo_energy_cutoff = {'ti': {{0: 100, 1: 100, 2: 100, 3: 100, 4: 100, 5: 100}},
                        'o': {{0: 100, 1: 100, 2: 100, 3: 100, 4: 100, 5: 100}},
                        }
    directory = 'lmax55/locut100'
    return VarDir(lo_energy_cutoff, directory)


def calc_lmax55_locut150() -> VarDir:
    """ Define a calculation

    Same cutoff for each channel.
    :return:
    """
    lo_energy_cutoff = {'ti': {{0: 150, 1: 150, 2: 150, 3: 150, 4: 150, 5: 150}},
                        'o': {{0: 150, 1: 150, 2: 150, 3: 150, 4: 150, 5: 150}},
                        }
    directory = 'lmax55/locut150'
    return VarDir(lo_energy_cutoff, directory)


def construct_optimised_basis(default_basis: dict,
                              lo_recommendations: np.ndarray,
                              lo_cutoff= Optional[dict],
                              n_los = Optional[dict]) -> dict:
    """ Build species files

    Do not need to parse LINENERGY
    Can parse species file - See new code. This equals default basis
    Should also get the species currently in the core
    For example, with Ti:
        <atomicState n="3" l="0" kappa="1" occ="2.00000" core="false"/>
        <atomicState n="3" l="1" kappa="1" occ="2.00000" core="false"/>
        <atomicState n="3" l="1" kappa="2" occ="4.00000" core="false"/>
        <atomicState n="3" l="2" kappa="2" occ="2.00000" core="false"/>
        <atomicState n="4" l="0" kappa="1" occ="2.00000" core="false"/>
     3s 3p 3d 4s
    Should also add something to count the number of LOs in the basis => Can apply to the default and to the final basis

    With the lo-recommendations, the easiest thing to do is label them (1s, 2s, 3s, ...), (2p, 3p, 4p, ...)
    Then it should not be a problem to add them in, in a simple pattern, and not accidentally add in LOs that "should"
    already be present

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




def main():
    """ Main for running l_max = (5, 5) for TiO2
    TODOs
    OR number of LOs per l-channel (convert the nunber of LOs to a trial energy)

    Parse existing basis
    Add to it using LO recommendations
    Write the new basis out

    :return:
    """
    root = "/users/sol/abuccheri/wp2/tio2/lo_sweep/"

    input_xml = set_input()

    default_basis = parse_species_xml()
    lo_recommendations = parse_lorecommendations("lorecommendations.dat", ['ti', 'o'], l_max=7, node_max=20)


    lo_energy_cutoff = {'ti': {0: 150, 1: 150, 2: 150, 3: 150, 4: 150, 5: 150},
                        'o': {0: 150, 1: 150, 2: 150, 3: 150, 4: 150, 5: 150},
                        }
    gw_basis_ti: dict = construct_optimised_basis(default_basis['ti'], lo_recommendations['ti'], lo_energy_cutoff['ti'])
    gw_basis_o: dict = construct_optimised_basis(default_basis['ti'], lo_recommendations['ti'])


    # Idea is to define the root, input.xml and a list of calculation settings, then inject
    # to this routine. It's more code to define each calculation, but it's way cleaner and
    # more robust.
    calculations = [calc_lmax55_locut100(), calc_lmax55_locut150()]

    for calculation in calculations:
        # Create the directories
        full_directory = os.path.join(root, calculation.directory)
        Path(full_directory).mkdir(parents=True, exist_ok=True)

        # Input xml
        with open(os.path.join(full_directory, "input.xml"), "w") as fid:
            fid.write(input_xml)

        # Species file/s

        # Run script



main()
