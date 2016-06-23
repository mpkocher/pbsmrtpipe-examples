#!/usr/bin/env python

import os
import sys
import logging
import random
import warnings

from pbcommand.models import FileTypes
from pbcommand.pb_io import load_reseq_conditions_from
from pbcommand.models.report import Report, PlotGroup, Plot
from pbcommand.cli import registry_builder, registry_runner
from pbcommand.utils import which
from pbcore.io import openDataSet

log = logging.getLogger(__name__)

# FIXME. Remove this.
PATHS = ('/mnt/usmp-data3/scratch/Labs/Kristofor/python/plotly',
         '/mnt/usmp-data3/scratch/Labs/Kristofor/python/selenium/py')


def raise_if_not_exist(p):
    if not os.path.exists(p):
        raise IOError("Unable to find {p}".format(p=p))
    return p

PH_EXE = which("phantomjs")

if PH_EXE is None:
    PHANTOM_EXE = '/home/knyquist/local/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
else:
    PHANTOM_EXE = os.path.abspath(PH_EXE)

try:
    import plotly
    import selenium
except ImportError as e:
    warnings.warn("Error {e}\n Trying to import from {p}".format(e=e, p=PATHS))
    for path in PATHS:
        sys.path.append(raise_if_not_exist(path))
    import plotly
    import selenium


from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, plot
from selenium import webdriver

import accuracy_plots

__version__ = "0.3.3"

NAMESPACE = "pbsmrtpipe_examples"


registry = registry_builder(NAMESPACE, "mh_toy.py")


class PhantomDriver(object):

    def __init__(self, exe=PHANTOM_EXE):
        self.exe = raise_if_not_exist(exe)
        self.phantomjs_driver = None

    def __enter__(self):
        self.phantomjs_driver = webdriver.PhantomJS(executable_path=self.exe)
        return self.phantomjs_driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        log.info("Shutting down phantomjs")
        if self.phantomjs_driver is not None:
            self.phantomjs_driver.quit()


def _get_dset_paths(file):
    log.info("Attempting to open condition JSON")
    json = load_reseq_conditions_from(file)
    dset_paths = {}
    for condition in json.conditions:
        if condition.cond_id not in dset_paths.keys():
            dset_paths[condition.cond_id] = {'aset': [],
                                             'sset': [],
                                             'rset': []}
        dset_paths[condition.cond_id]['aset'] = condition.alignmentset
        dset_paths[condition.cond_id]['sset'] = condition.subreadset
        dset_paths[condition.cond_id]['rset'] = condition.referenceset

    return dset_paths


def _subsample_alignments(mapped_subreadset, num=1000):
    ss = random.sample(mapped_subreadset, num)
    return ss


def _getKPIs(mapped_sset, subsampled_mapped_sset):
    """
    Retrieve the KPIs for a single mapped sset in a dictionary structure.
    """
    log.info("Retrieving metrics from aligned subread set")
    data = {}
    data['holenumber'] = []
    data['readlength'] = []
    data['templatespan'] = []
    data['insertions'] = []
    data['deletions'] = []
    data['mismatches'] = []
    data['accuracy'] = []
    data['IPD'] = []

    for aln in subsampled_mapped_sset:
        data['holenumber'].append(aln.HoleNumber)
        data['readlength'].append(float(aln.readEnd - aln.readStart))
        data['templatespan'].append(float(aln.referenceEnd - aln.referenceStart))
        data['insertions'].append(float(aln.nIns) / data['templatespan'][-1])
        data['deletions'].append(float(aln.nDel) / data['templatespan'][-1])
        data['mismatches'].append(float(aln.nMM) / data['templatespan'][-1])
        error_rate = (aln.nIns + aln.nDel + aln.nMM) / data['templatespan'][-1]
        data['accuracy'].append(1 - error_rate)
        data['IPD'].append(aln.IPD())

    data['total nreads'] = len(mapped_sset)

    return data


def _example_main(input_file, output_file, **kwargs):
    """
    This func should be imported from your python package.

    This should have *no* dependency on the pbcommand IO, such as the RTC/TC models.
    """

    # This is just for test purposes
    log.info("Running example main with {i} {o} kw:{k}".format(i=input_file,
                                                               o=output_file,
                                                               k=kwargs))

    # Open dset CSV. Store absolute path of each alignment set.
    dset_paths = _get_dset_paths(input_file[0])

    # Open plots CSV. Store names of plots to produce.
    # plots_to_generate = _get_plots_to_generate(input_file[1])

    dsets_kpis = {}
    for f in dset_paths:
        dset = openDataSet(dset_paths[f]['aset'])
        subsampled_dset = _subsample_alignments(dset)
        dsets_kpis[f] = _getKPIs(dset, subsampled_dset)

    figures = []
    # figure tuple has form (plot_group_id, plot_id, figure)
    figures.append(('accuracy', 'accuracy_vs_readlength', accuracy_plots._plot_accuracy_vs_readlength(dsets_kpis)))
    figures.append(('accuracy', 'accuracy', accuracy_plots._plot_accuracy_distribution(dsets_kpis)))
    figures.append(('accuracy', 'accuracy_boxplot', accuracy_plots._plot_accuracy_boxplots(dsets_kpis)))

    all_plots = {} # dictionary of plots. keys are groups

    with PhantomDriver() as driver:
        for plot_group, plot_id, fig in figures:
            if plot_group not in all_plots.keys():
                all_plots[plot_group] = []
            plot(fig, filename='{i}.html'.format(i=plot_id), show_link=False, auto_open=False)
            plot_name = '{i}.png'.format(i=plot_id)

            driver.set_window_size(1920, 1080)
            driver.get('{i}.html'.format(i=plot_id))
            driver.save_screenshot(plot_name)
            driver.get('{i}.html'.format(i=plot_id))
            driver.save_screenshot('{i}_thumb.png'.format(i=plot_id))

            log.info("Saved screen to {}".format(plot_name))

            os.remove('{i}.html'.format(i=plot_id))
            plot_path = '{i}.png'.format(i=plot_id)
            thumb_path = '{i}_thumb.png'.format(i=plot_id)
            all_plots[plot_group].append(Plot(plot_id, plot_path, thumbnail=thumb_path))

    log.info("completed generating {} plots".format(len(all_plots)))

    plot_groups = []
    for plot_group_title in all_plots.keys():
        plot_group = PlotGroup(plot_group_title, plots=all_plots[plot_group_title])
        plot_groups.append(plot_group)

    report = Report('mh_toy', tables=(), plotgroups=plot_groups, attributes=())
    report.write_json(output_file)

    return 0


@registry("dev_mh_toy", __version__, (FileTypes.COND_RESEQ, ), (FileTypes.REPORT, ), nproc=1, is_distributed=True)
def run_rtc(rtc):
    """
    Example Task for grabbing data from multiple mapped ssets.
    Takes a mapped SubreadSet XML file as input and writes a csv file with mock data.
    """
    # The above docstring will be used as the Task/ToolContract Description

    log.info("Got RTC task options {t}".format(t=rtc.task.options))
    log.info("Got nproc {n}".format(n=rtc.task.nproc))

    # The Task options are now accessible via global identifier
    # alpha = rtc.task.options['pbsmrtpipe_examples.task_options.alpha']
    return _example_main(rtc.task.input_files, rtc.task.output_files[0])


if __name__ == '__main__':
    sys.exit(registry_runner(registry, sys.argv[1:]))