# Defining tasks and pipelines for pbsmrtpipe

pbsmrtpipe supports python, R and Scala for via the pacbio Tool Contract interface.


## Setup to run Examples

Requires python (2.7.9)  with virtualenv

Installing the necessary python components:

```
$> virtualenv ve
$> source ve/bin/activate
$> # this will install pbcommand, pbcore and pbsmrtpipe from github repos. 
$> # modify the REQUIREMENTS.txt file to point to other versions
$> pip install -r REQUIREMENTS.txt

```

### Setup ENV

```
$> # set path to TCs so pbsmrtpipe can load them
$> export PB_TOOL_CONTRACT_DIR=$(pwd)/tool-contracts
$> pbsmrtpipe show-tasks # your tasks should show up in the registry
$> # add *.py examples to our path
$> export PATH=$(pwd):$PATH
$> # Sanity check
$> # rebuild Tool Contracts
$> make python-tool-contracts
$> pbsmrtpipe show-tasks # final check to see if your tasks are in the registry
```


### Run Example

```
$> cd py-examples/01-helloworld
$> # pipeline definition
$> cat pipeline.xml
$> # preset defintion 
$> cat preset.xml
$> # test layer
$> cat testkit.cfg
$> # This will call pbsmrtpipe and run a sanity tests
$> pbtestkit-runner testkit.cfg
$> # output will be in job_output
$> cd job_output
```


## Defining Tasks with Python

[pbcommmand](https://github.com/PacificBiosciences/pbcommand) provides a python interface to define tasks that can be consumed in pbsmrtpipe.


QuickStart to Defining a Task (via ToolContract Interface)
```python
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

# More tasks can be registered by calling @registry()

if __name__ == '__main__':
    sys.exit(registry_runner(registry, sys.argv[1:]))

```


## Defining Tasks with R:

Install requires packrat and [pbcommandR](https://github.com/mpkocher/pbcommandR).

```r
> library(devtools)
> install_githhub("mpkocher/pbcommandR")
```

## Setup ENV

Todo


### Run Example

```
$> cd r-examples/01-helloR
$> # pipeline definition
$> cat pipeline.xml
$> # preset defintion 
$> cat preset.xml
$> # test layer
$> cat testkit.cfg
$> # This will call pbsmrtpipe and run a sanity tests
$> pbtestkit-runner testkit.cfg
$> # output will be in job_output
```

## Defining Tasks with R

[QuickStart pbcommandR](https://github.com/mpkocher/pbcommandR#quick-start)



