#!/usr/bin/env python

import sys
import logging

from pbcommand.models import FileTypes, OutputFileType
from pbcommand.cli import registry_builder, registry_runner

log = logging.getLogger(__name__)

# the 'Driver' exe needs to be your your path
registry = registry_builder("pbsmrtpipe_examples", "hello_world_quick.py ")


def _example_main(input_files, output_files, **kwargs):
    # This func should be imported from your python package. 
    # This is just for test purposes
    log.info("Running example main with {i} {o} kw:{k}".format(i=input_files,
                                                               o=output_files, k=kwargs))
    # write mock output files, otherwise the End-to-End test will fail
    xs = output_files if isinstance(output_files, (list, tuple)) else [output_files]
    for x in xs:
        with open(x, 'w') as writer:
            writer.write("Mock data\n")
    return 0


@registry("dev_mk_example_txt", "0.2.1", FileTypes.TXT, FileTypes.TXT, nproc=1, options=dict(alpha=1234))
def run_rtc(rtc):
    return _example_main(rtc.task.input_files[0], rtc.task.output_files[0], nproc=rtc.task.nproc)


if __name__ == '__main__':
    sys.exit(registry_runner(registry, sys.argv[1:]))


