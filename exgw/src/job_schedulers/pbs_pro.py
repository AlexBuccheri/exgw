"""
Generate PBS Pro Script

Some notes

Specifying

  qsub -koed my_batchjob_script.pbs

option here and redirecting the output to a file (see example above) makes it possible for you to view STDOUT and
STDERR of your job scripts while the job is running.

Process Pinning
https://www.nas.nasa.gov/hecc/support/kb/using-the-omplace-tool-for-pinning_287.html
https://kb.hlrs.de/platforms/index.php/Batch_System_PBSPro_(Hawk)#Format:

"""
from typing import Optional
from collections import OrderedDict
import sys


def pbs_resources_string_to_vars(pbs_directives: OrderedDict) -> tuple:
    """
    Extract nodes, mpi_per_node, omp_per_process from a pbs resources string of the form:

     PBS -l select=2:node_type=rome:mpiprocs=2

    TODO
    The number of lines in PBS_NODEFILE is the sum of the values of mpiprocs for all chunks (nodes)
    requested by the job. So one could equally wc -l ${PBS_NODEFILE} to obtain total_mpi_procs

    :param pbs_directives: Ordered dictionary of slurm directives
    :return tuple nodes, mpi_per_node, omp_per_process: Number of nodes, mpi processes per node and
    OMP threads per process.
    """

    # Note, this won't work if I ask for different MPI resources on different nodes i.e.:
    # PBS -l select=2:node_type=rome:mpiprocs=2+1:node_type=rome:mpiprocs=3
    process_settings = pbs_directives['l'].split(':')
    for string in process_settings:
        if 'mpiprocs' in string:
             mpi_per_node = int(string.split('=')[-1])
        if 'select' in string:
            nodes = int(string.split('=')[-1])
        if 'ompthreads' in string:
            omp_per_process = int(string.split('=')[-1])

    return nodes, mpi_per_node, omp_per_process


def set_pbs_pro(pbs_directives: OrderedDict,
                env_vars: OrderedDict,
                module_envs: Optional[list] = None,
                mpi_options: Optional[list] = []):
    """
    Generate simple PBS Pro submission script, suitable for hybrid MPI+OMP applications.

    :param OrderedDict pbs_directives: Ordered dictionary of slurm directives
    :param OrderedDict env_vars: Ordered dictionary of environment variables to set
    :param Optional[list] module_envs: Optional list of modules to load
    :param Optional[list] mpi_options: Optional list of mpirun options
    :return: slurm script string
    """
    env_keys = [key for key in env_vars.keys()]
    assert 'EXE' in env_keys, "EXE must be specified in env_vars"

    spacing = lambda length: " " if length == 1 else ""

    pbs_prefix = "#PBS -"

    script = "#!/bin/bash \n\n"
    for directive, setting in pbs_directives.items():
        script += pbs_prefix + directive + spacing(len(directive)) + setting + '\n'
    script += '\n'

    if module_envs is not None:
        script += 'module purge \n'
        for module in module_envs:
            script += "module load " + module + '\n'
        script += '\n'

    for key, setting in env_vars.items():
        script += key + '=' + setting + '\n'

    nodes, mpi_per_node, omp = pbs_resources_string_to_vars(pbs_directives)
    total_mpi_procs = mpi_per_node * nodes

    script += "cd $PBS_O_WORKDIR \n" + \
              "export OMP_NUM_THREADS=" + str(omp) + "\n\n"

    # MPI run command
    script += "mpirun -np " + str(total_mpi_procs)
    for option in mpi_options:
        script += " " + option

    script += " $EXE"

    if 'OUT' in env_keys:
        script += ' > $OUT 2>&1'

    return script


def time_to_string(time: list) -> str:
    """
    Time list to string
    :param time: List of length 3
    :return: string with format 00:20:00
    """
    assert len(time) == 3, "expect [hours, mins, secs]"

    time_string = ''
    for t in time:
        t_str = str(t)
        if len(t_str) == 1:
            t_str = '0' + t_str
        time_string += t_str + ':'

    return time_string[:-1]


def check_send_email(send_email: str):
    """
    Check the "send e-mail" options are valid
    :param str send_email: e-mail send options
    """
    if send_email is not None:
        email_options = ['a', 'b', 'e', 'ab', 'ae', 'be', 'abe']
        if not (send_email in email_options):
            print('send_email string not valid:', send_email)
            print('Must be one of:', email_options)
            sys.quit()


def set_processes_string(nodes: int,
                         cores_per_node: int,
                         mpi_ranks_per_node: int,
                         omp_threads_per_process: int,
                         node_type_mem: int,
                         node_type: str) -> str:
    """
    Set processes string of the form:

        select=1:node_type=rome:node_type_mem=256gb:ncpus=8:mpiprocs=4:ompthreads=2

    TODO This doesn't accommodate multi-node jobs.
    For example:

     Multi node type job can also be specified using a +:
     select=1:node_type=hsw:node_type_mem=256gb+3:node_type=hsw:node_type_mem=128gb:node_type_core=20c

     The example above will allocate 1 hsw node (a 20 core ore 24 core type) with 256 GB memory and 3 hsw nodes
     (the 20 cores type) with 128 GB memory.

    :param int nodes: Number of nodes
    :param int cores_per_node: Physical cores per node
    :param int mpi_ranks_per_node: MPI ranks per node
    :param int omp_threads_per_process: openMP threads per node
    :param int node_type_mem: Memory per node (in gb)
    :param str node_type: Name of node
    :return: str string: Resource string
    """
    string = 'select=' + str(nodes) + ':'

    if node_type is not None:
        string += 'node_type=' + node_type + ':'

    if node_type_mem is not None:
        string += 'node_type_mem=' + str(node_type_mem) + 'gb:'

    string += 'ncpus=' + str(cores_per_node) + ':'
    string += 'mpiprocs=' + str(mpi_ranks_per_node) + ':'
    string += 'ompthreads=' + str(omp_threads_per_process)

    return string


def set_pbs_pro_directives(time: Optional[list] = None,
                           queue_name: Optional[str] = None,
                           nodes: Optional[int] = 1,
                           mpi_ranks_per_node: Optional[int] = 1,
                           omp_threads_per_process: Optional[int] = 1,
                           cores_per_node: Optional[int] = None,
                           node_type: Optional[str] = None,
                           node_type_mem: Optional[int] = None,
                           job_name: Optional[str] = 'default_name',
                           email_address: Optional[str] = 'abuccheri@physik.hu-berlin.de',
                           send_email: Optional[str] = None,
                           project_code: Optional[str] = None,
                           merge_output_err_files: Optional[bool] = True) -> OrderedDict:
    """
    Set PBS Pro script directives/options.

    More script options to add:

    -r value                         Mark job as re-runnable
    -W depend = list                 Specify job dependencies
    -W stagein-list stageout=list    Input/output file staging
    -W sandbox=<value>               Staging and execution directory: User's home vs job-specific
    -a date_time                     Defer execution
    -c interval                      Specify job checkpoint interval
    -h                               Hold a job (delay execution)
    -J X-Y[:Z}                       Define job array
    -k keep                          Retain (o)utput and (e)rror files on execution host
    -p                               Set job's priority

    :param list time: Time with format [hours, mins, secs]
    :param int nodes: Number of nodes (chunks). A chunk is the smallest allocation job can have.
     hence a node for most HPC clusters (prevent job splitting).
    :param int mpi_ranks_per_node: MPI ranks per node
    :param int omp_threads_per_process: openMP threads per process
    :param int cores_per_node: Number of physical cores to request per node
    :param str node_type: Name of node/node type
    :param int node_type_mem: Memory reservation (in gb)
    :param str queue_name: Queue name
    :param str job_name: Job name
    :param str email_address: E-mail address
    :param str send_email:
    :param str project_code:
    :param bool merge_output_err_files:
    :return OrderedDict pbs_directives: PBS Pro script options
    """

    time_str = time_to_string(time)
    check_send_email(send_email)
    merge_output_err = {True: 'oe', False: None}

    if cores_per_node is None:
        # Take one MPI rank per core
        cores_per_node = mpi_ranks_per_node

    processes_str = set_processes_string(nodes,
                                         cores_per_node,
                                         mpi_ranks_per_node,
                                         omp_threads_per_process,
                                         node_type_mem,
                                         node_type)

    #assert omp_threads_per_process * mpi_ranks_per_node <= cores_per_node, "MPI * OMP processes exceeds physical cores"

    pbs_directives = OrderedDict([('N', job_name),
                                  ('A', project_code),
                                  ('q', queue_name),
                                  ('l walltime=', time_str),
                                  ('l', processes_str),
                                  ('m', send_email),
                                  ('M', email_address),
                                  ('j', merge_output_err[merge_output_err_files])
                                  ])

    # Remove null options
    final_pbs_directives = OrderedDict()
    for key, value in pbs_directives.items():
        if value is None:
            continue
        final_pbs_directives[key] = value

    return final_pbs_directives
