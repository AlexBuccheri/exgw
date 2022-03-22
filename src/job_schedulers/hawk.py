class Hawk:
    # https://www.hlrs.de/systems/hpe-apollo-hawk/

    # node_type=Rome
    # CPUs per node = 2
    # cores per CPU = 64
    # cores_per_node = 128 (CPUs per node * cores per CPU )
    # x2 for hyper threading
    # CPU frequency = 2.25 GHz

    # On Rome-based nodes, the core id corresponds to hyperthreads and sockets as follows:
    # core 0 - core 63: hyperthread 0 @ socket 0
    # core 64 - core 127: hyperthread 0 @ socket 1
    # core 128 - core 191: hyperthread 1 @ socket 0
    # core 192 - core 256: hyperthread 1 @ socket 1

    # We recommend to always (in hybrid as well as pure MPI jobs) use omplace to pin processes and threads to C
    # PU cores (cf. below) in order to prevent expensive migration.

    # node_type_mem = 256gb
    # On  queue smp, one can also ask for 2048gb and 4096gb
    def __init__(self, a):
        self.a = a
