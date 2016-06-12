#!/usr/bin/env python
"""Simple Hello World example for using pbcommand.

This example does NOT emit or consume tool contracts, it's for building common
commandline interfaces with (hopefully) minimal boiler plate machinery.

See the hello_world_quick.py for an example of interfacing with the "Quick"
commandline interface.

Author: Michael Kocher
"""
import sys
import logging

from pbcommand.utils import setup_log
from pbcommand.cli import get_default_argparser, pacbio_args_runner
import pbcommand.common_options as C
from pbcommand.validators import validate_file


log = logging.getLogger(__name__)

__version__ = "0.1.1"


def run_main(fasta_in, fasta_out, min_sequence_length):
    """This should be imported from your library code"""
    _d = dict(i=fasta_in, o=fasta_out, s=min_sequence_length)
    log.info("MOCK filtering (<{s}) fasta {i} to {o}".format(**_d))
    with open(fasta_out, 'w') as f:
        f.write(">record_1\nACGT")
    # Every main should return an positive integer return code
    return 0


def get_parser():
    p = get_default_argparser(__version__, __doc__)
    C.add_base_options(p)
    p.add_argument("fasta_in", type=validate_file, help="Fasta Input")
    p.add_argument("fasta_out", type=str, help="Output Filtered Fasta file")
    p.add_argument("--min-length", type=int, default=50, help="Min Sequence length")
    return p


def _args_runner(args):
    return run_main(args.fasta_in, args.fasta_out, args.min_length)


def main(argv=sys.argv):
    return pacbio_args_runner(argv[1:], get_parser(), _args_runner, log, setup_log)


if __name__ == '__main__':
    sys.exit(main())