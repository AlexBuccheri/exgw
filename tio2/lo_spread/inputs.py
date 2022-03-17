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
from src.inputs.gw import GWInput
from src.parse.parsers import parse_lorecommendations, parse_species_xml
from src.basis.optimised_basis import construct_optimised_basis

# TiO2 specific
from tio2.lo_spread.ground_state_xml import converged_input_xml


#  Variable (thing that varies between calculations) and directory.
class Calculation:
    def __init__(self, directory: str, variable: any, basis: Optional[dict] = None):
        self.directory = directory
        self.variable = variable
        self.basis = basis


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


# So the annoying shit is I have to write this out for (4,4), (5,5) (7,7) and lo_energy_cutoff = [20, 40, 60, 80, 100, 120]
# So that is 18 functions that barely differ - BUT this gives me total flexiblity if I want change what quantity I
# vary OR exactly how I want to define the basis
def calc_lmax55_locut150(default_basis, lo_recommendations) -> Calculation:
    """ Define a calculation

    Same cutoff for each channel.
    :return:
    """
    directory = 'lmax55/locut150'

    lo_energy_cutoff = {'ti': {{0: 150, 1: 150, 2: 150, 3: 150, 4: 150, 5: 150}},
                        'o': {{0: 150, 1: 150, 2: 150, 3: 150, 4: 150, 5: 150}},
                        }

    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], lo_cutoff=lo_energy_cutoff[x])

    return Calculation(directory, lo_energy_cutoff, basis=gw_basis)


def main():
    """ Main for running l_max = (5, 5) for TiO2
    TODOs
    OR number of LOs per l-channel (convert the nunber of LOs to a trial energy)

    Parse existing basis
    Add to it using LO recommendations
    Write the new basis out

    Idea is to define the root, input.xml and a list of calculation settings, then inject
    to this routine. It's more code to define each calculation, but it's way cleaner and
    more robust.

    :return:
    """
    root = "/users/sol/abuccheri/wp2/tio2/lo_sweep/"

    input_xml = set_input()
    default_basis = parse_species_xml()
    lo_recommendations = parse_lorecommendations("lorecommendations.dat", ['ti', 'o'], l_max=7, node_max=20)

    calculations = [calc_lmax55_locut150(default_basis, lo_recommendations)]

    for calculation in calculations:
        # Create the directories
        full_directory = os.path.join(root, calculation.directory)
        Path(full_directory).mkdir(parents=True, exist_ok=True)

        # Copy STATE.OUT from the ground state

        # Input xml
        with open(os.path.join(full_directory, "input.xml"), "w") as fid:
            fid.write(input_xml)

        # Species files
        for x in ['ti', 'o']:
            species_fname = f'{x}.xml'.capitalize()
            with open(os.path.join(full_directory, species_fname), "w") as fid:
                fid.write(calculation.basis[x])

        # Run script

        # Need some way of producing directory paths so I can easily load when I want
        # to do post-processing.


main()
