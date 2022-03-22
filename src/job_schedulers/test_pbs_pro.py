from collections import OrderedDict

from pbs_pro import set_pbs_pro_directives, set_pbs_pro


def test_set_pbs_pro_without_optionals():

    omp = 16
    directives = set_pbs_pro_directives(time=[24,00,0],
                                        queue_name='single',
                                        nodes=1,
                                        mpi_ranks_per_node=8,
                                        omp_threads_per_process=omp,
                                        cores_per_node=128,
                                        node_type='rome',
                                        job_name='GW_gs')

    env_vars = OrderedDict([('EXE', '/zhome/academic/HLRS/pri/ipralbuc/exciting-oxygen_release/bin/exciting_mpismp'),
                            ('OUT', 'terminal.out')
                            ])
    module_envs = ['intel/19.1.0', 'mkl/19.1.0', 'impi/19.1.0']

    mpi_options = ['omplace -nt ' + str(omp)]

    script = set_pbs_pro(directives, env_vars, module_envs, mpi_options)
    print(script)
    # assert script == ref

# TODO Write me
# def test_pbs_pro_with_all_args():
