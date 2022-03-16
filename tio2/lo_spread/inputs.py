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
from typing import List


class CalculationInput:
    """ Inputs required for a calculation
    """
    # One can either store all the file strings
    directory: str
    input_xml: str
    species: List[str]
    run_script: str
    # OR one could store the python data (I like the latter more)


Calculations = List[CalculationInput]
