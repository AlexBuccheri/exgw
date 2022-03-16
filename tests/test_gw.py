""" Test GW Input Class.
Run from the root directory with  pytest tests or  pytest -s tests to get print statement outputs.
"""
from src.inputs.gw import GWInput


def test_class_gw_with_mandatory_args():
    gw = {'taskname': 'G0W0', 'nempty':800, 'ngridq': [4, 4, 4], 'skipgnd': "false"}
    gw_input = GWInput(gw=gw)
    # print(gw_input.to_xml_str())
    gw_input = GWInput(gw={**gw, 'ibgw': 1, 'nbgw': 20})
    # print(gw_input.to_xml_str())


def test_class_gw_with_all_args():
    gw = {'taskname': 'G0W0', 'nempty':800, 'ngridq': [4, 4, 4], 'skipgnd': "false"}
    mixbasis ={'lmaxmb': 4, 'epsmb': 0.001 , 'gmb': 1.0}
    freqgrid = {'nomeg': 32 ,'freqmax': 1.0}
    barecoul = {'pwm': 2.0, 'stctol': 1e-16, 'barcevtol': 0.1}
    selfenergy = {'actype': 'pade', 'singularity': 'mpb'}
    gw_input = GWInput(gw=gw, mixbasis=mixbasis, freqgrid=freqgrid, barecoul=barecoul, selfenergy=selfenergy)
    # print(gw_input.to_xml_str())
