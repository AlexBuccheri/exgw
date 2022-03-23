""" Generate inputs with several LO channels, and multiple LOs per channel
"""
# External libs
import os.path
from pathlib import Path
import shutil
from typing import List

# This package
from exgw.src.inputs.gw import GWInput
from exgw.src.parse.parsers import parse_lorecommendations, parse_species_xml
from exgw.src.write.species import write_species_file_from_dict

# TiO2 specific
from exgw.tio2.lo_spread.ground_state_xml import converged_input_xml
from exgw.tio2.lo_spread.calculations import *


def set_input() -> str:
    """ Compose converged ground state and GW input settings.

    GW Fixed input
    Ground state input read from python

    :return: Input xml string.
    """
    # Converged ground state
    input_xml = converged_input_xml.replace('do="skip"', 'do="fromfile"')

    # GW
    gw = {'taskname': 'G0W0', 'nempty': 100, 'ngridq': [2, 2, 2], 'skipgnd': "false"}
    mixbasis = {'lmaxmb': 4, 'epsmb': 0.001, 'gmb': 1.0}
    freqgrid = {'nomeg': 16, 'freqmax': 1.0}
    barecoul = {'pwm': 2.0, 'stctol': 1e-16, 'barcevtol': 0.1}
    selfenergy = {'actype': 'pade', 'singularity': 'mpb'}
    gw_input = GWInput(gw=gw, mixbasis=mixbasis, freqgrid=freqgrid, barecoul=barecoul, selfenergy=selfenergy)

    # Inject GW settings into input
    input_xml = input_xml.format(GW_INPUT=gw_input.to_xml_str())

    return input_xml


def main(root: str, ground_state_path: str, input_xml: str, calculations: List[Calculation]):
    """ Main for running TiO2

    Idea is to define the root, ground_state_path, input.xml and a list of calculation settings, then inject
    into this routine. It's more code to define each calculation, but it's clean and robust.

    Need some way of producing directory paths so I can easily load when I want to do post-processing?
    - Should just be `full_directory` from above. All settings in calculations
    """
    osjp = os.path.join

    for calculation in calculations:
        # Create run directory
        full_directory = osjp(root, calculation.directory)
        Path(full_directory).mkdir(parents=True, exist_ok=True)

        # Copy STATE.OUT from the ground state
        shutil.copyfile(osjp(ground_state_path, "STATE.OUT"), osjp(full_directory, "STATE.OUT"))

        # Input xml
        with open(osjp(full_directory, "input.xml"), "w") as fid:
            fid.write(input_xml)

        # Species files
        for x in ['ti', 'o']:
            file_name = osjp(full_directory, x.capitalize() + '.xml')
            write_species_file_from_dict(calculation.basis[x], file_name=file_name)

        # Run script
        with open(osjp(full_directory, "run.sh"), "w") as fid:
            fid.write(calculation.run_script)


if __name__ == "__main__":
    root = "/users/sol/abuccheri/wp2/tio2/gw/losweep"

    ground_state_path = "/users/sol/abuccheri/wp2/tio2/ground_state"
    default_basis = {}
    default_basis['ti'] = parse_species_xml(os.path.join(ground_state_path, "Ti.xml"))
    default_basis['o'] = parse_species_xml(os.path.join(ground_state_path, "O.xml"))
    lo_recommendations = parse_lorecommendations(os.path.join(ground_state_path, "lorecommendations.dat"), ['ti', 'o'], l_max=7, node_max=20)

    input_xml = set_input()
    calculations = [calc_lmax43_locut20(default_basis, lo_recommendations),
                    calc_lmax43_locut30(default_basis, lo_recommendations),
                    calc_lmax43_locut40(default_basis, lo_recommendations),
                    calc_lmax43_locut50(default_basis, lo_recommendations),
                    calc_lmax43_locut60(default_basis, lo_recommendations),
                    calc_lmax43_locut70(default_basis, lo_recommendations),
                    calc_lmax43_locut80(default_basis, lo_recommendations),
                    calc_lmax43_locut90(default_basis, lo_recommendations),
                    calc_lmax43_locut100(default_basis, lo_recommendations)]

    main(root, ground_state_path, input_xml, calculations)
