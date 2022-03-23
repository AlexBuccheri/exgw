""" LO Sweep calculations

For TiO2, want to run l_max = (4,3) (5,4) (6,5) (7,6)
with same cut-off per l_max channel: [20, 30, 40, 50, 60, 70, 80, 90, 100]
Hence 36 calculations.
"""
from typing import Optional
from collections import OrderedDict

from exgw.src.basis.optimised_basis import construct_optimised_basis
from exgw.src.job_schedulers import slurm


class Calculation:
    def __init__(self, directory: str,
                 lo_energy_cutoff: Optional[dict] = None,
                 basis: Optional[dict] = None,
                 run_script: Optional[str] = None):
        self.directory = directory
        self.variable = lo_energy_cutoff
        self.basis = basis
        self.run_script = run_script


# Specify which cluster to generate a run script for
cluster = 'dune'

if cluster is 'dune':
    default_env_vars = OrderedDict([('EXE', '/users/sol/abuccheri/exciting/bin/excitingmpismp'),
                                    ('OUT', 'terminal.out')])
    default_module_envs = ['intel/2019']
    default_directives = slurm.set_slurm_directives(job_name="gw_tio2",
                                                    time=[0, 24, 0, 0],
                                                    partition='all',
                                                    exclusive=True,
                                                    nodes=4,
                                                    ntasks_per_node=2,
                                                    cpus_per_task=18,
                                                    hint='nomultithread')
    set_run_script = slurm.set_slurm_script
elif cluster is 'hawk':
    raise NotImplementedError('Need to specify settings for HAWK environment')
else:
    raise ValueError('Choice of HPC machine is not valid: {}')


def calc_lmax43_locut20(default_basis, lo_recommendations) -> Calculation:
    """ Define a calculation.

    * relative directory (to root)
    * basis settings in dictionary form
    * Note, lo_energy_cutoff assigned to variable is not much good. This could be via **kwargs

    Using same cutoff for each channel.
    :return: Calculation instance
    """
    # Relative run directory
    directory = 'lmax43/locut20'

    # Basis
    l_max = {'ti': 4, 'o': 3}
    lo_energy_cutoff = {'ti': {0: 20, 1: 20, 2: 20, 3: 20, 4: 20},
                        'o': {0: 20, 1: 20, 2: 20, 3: 20}
                        }
    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], l_max[x], lo_energy_cutoff[x])

    # Submission script settings
    run_script = set_run_script(default_directives, default_env_vars, default_module_envs)

    return Calculation(directory, lo_energy_cutoff=lo_energy_cutoff, basis=gw_basis, run_script=run_script)


def calc_lmax43_locut30(default_basis, lo_recommendations) -> Calculation:
    # Relative run directory
    directory = 'lmax43/locut30'

    # Basis
    l_max = {'ti': 4, 'o': 3}
    lo_energy_cutoff = {'ti': {0: 30, 1: 30, 2: 30, 3: 30, 4: 30},
                        'o': {0: 30, 1: 30, 2: 30, 3: 30}
                        }
    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], l_max[x], lo_energy_cutoff[x])

    run_script = set_run_script(default_directives, default_env_vars, default_module_envs)

    return Calculation(directory, lo_energy_cutoff=lo_energy_cutoff, basis=gw_basis, run_script=run_script)


def calc_lmax43_locut40(default_basis, lo_recommendations) -> Calculation:
    # Relative run directory
    directory = 'lmax43/locut40'

    # Basis
    l_max = {'ti': 4, 'o': 3}
    lo_energy_cutoff = {'ti': {0: 40, 1: 40, 2: 40, 3: 40, 4: 40},
                        'o': {0: 40, 1: 40, 2: 40, 3: 40}
                        }
    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], l_max[x], lo_energy_cutoff[x])

    run_script = set_run_script(default_directives, default_env_vars, default_module_envs)

    return Calculation(directory, lo_energy_cutoff=lo_energy_cutoff, basis=gw_basis, run_script=run_script)


def calc_lmax43_locut50(default_basis, lo_recommendations) -> Calculation:
    # Relative run directory
    directory = 'lmax43/locut50'

    # Basis
    l_max = {'ti': 4, 'o': 3}
    lo_energy_cutoff = {'ti': {0: 50, 1: 50, 2: 50, 3: 50, 4: 50},
                        'o': {0: 50, 1: 50, 2: 50, 3: 50}
                        }
    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], l_max[x], lo_energy_cutoff[x])

    run_script = set_run_script(default_directives, default_env_vars, default_module_envs)

    return Calculation(directory, lo_energy_cutoff=lo_energy_cutoff, basis=gw_basis, run_script=run_script)


def calc_lmax43_locut60(default_basis, lo_recommendations) -> Calculation:
    # Relative run directory
    directory = 'lmax43/locut60'

    # Basis
    l_max = {'ti': 4, 'o': 3}
    lo_energy_cutoff = {'ti': {0: 60, 1: 60, 2: 60, 3: 60, 4: 60},
                        'o': {0: 60, 1: 60, 2: 60, 3: 60}
                        }
    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], l_max[x], lo_energy_cutoff[x])

    run_script = set_run_script(default_directives, default_env_vars, default_module_envs)

    return Calculation(directory, lo_energy_cutoff=lo_energy_cutoff, basis=gw_basis, run_script=run_script)


def calc_lmax43_locut70(default_basis, lo_recommendations) -> Calculation:
    # Relative run directory
    directory = 'lmax43/locut70'

    # Basis
    l_max = {'ti': 4, 'o': 3}
    lo_energy_cutoff = {'ti': {0: 70, 1: 70, 2: 70, 3: 70, 4: 70},
                        'o': {0: 70, 1: 70, 2: 70, 3: 70}
                        }
    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], l_max[x], lo_energy_cutoff[x])

    run_script = set_run_script(default_directives, default_env_vars, default_module_envs)

    return Calculation(directory, lo_energy_cutoff=lo_energy_cutoff, basis=gw_basis, run_script=run_script)


def calc_lmax43_locut80(default_basis, lo_recommendations) -> Calculation:
    # Relative run directory
    directory = 'lmax43/locut80'

    # Basis
    l_max = {'ti': 4, 'o': 3}
    lo_energy_cutoff = {'ti': {0: 80, 1: 80, 2: 80, 3: 80, 4: 80},
                        'o': {0: 80, 1: 80, 2: 80, 3: 80}
                        }
    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], l_max[x], lo_energy_cutoff[x])

    run_script = set_run_script(default_directives, default_env_vars, default_module_envs)

    return Calculation(directory, lo_energy_cutoff=lo_energy_cutoff, basis=gw_basis, run_script=run_script)


def calc_lmax43_locut90(default_basis, lo_recommendations) -> Calculation:
    # Relative run directory
    directory = 'lmax43/locut90'

    # Basis
    l_max = {'ti': 4, 'o': 3}
    lo_energy_cutoff = {'ti': {0: 90, 1: 90, 2: 90, 3: 90, 4: 90},
                        'o': {0: 90, 1: 90, 2: 90, 3: 90}
                        }
    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], l_max[x], lo_energy_cutoff[x])

    run_script = set_run_script(default_directives, default_env_vars, default_module_envs)

    return Calculation(directory, lo_energy_cutoff=lo_energy_cutoff, basis=gw_basis, run_script=run_script)


def calc_lmax43_locut100(default_basis, lo_recommendations) -> Calculation:
    # Relative run directory
    directory = 'lmax43/locut100'

    # Basis
    l_max = {'ti': 4, 'o': 3}
    lo_energy_cutoff = {'ti': {0: 100, 1: 100, 2: 100, 3: 100, 4: 100},
                        'o': {0: 100, 1: 100, 2: 100, 3: 100}
                        }
    gw_basis = {}
    for x in ['ti', 'o']:
        gw_basis[x] = construct_optimised_basis(default_basis[x], lo_recommendations[x], l_max[x], lo_energy_cutoff[x])

    run_script = set_run_script(default_directives, default_env_vars, default_module_envs)

    return Calculation(directory, lo_energy_cutoff=lo_energy_cutoff, basis=gw_basis, run_script=run_script)
