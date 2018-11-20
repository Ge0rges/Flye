#(c) 2016 by Authors
#This file is a part of ABruijn program.
#Released under the BSD license (see LICENSE file)

"""
Runs repeat/contigger binary
"""

import subprocess
import logging
import os

from flye.utils.utils import which

REPEAT_BIN = "flye-repeat"
CONTIGGER_BIN = "flye-contigger"
logger = logging.getLogger()


class RepeatException(Exception):
    pass


def check_binaries():
    if not which(REPEAT_BIN) or not which(CONTIGGER_BIN):
        raise RepeatException("Repeat/contgger binaries were not found. "
                              "Did you run 'make'?")
    try:
        devnull = open(os.devnull, "w")
        subprocess.check_call([REPEAT_BIN, "-h"], stderr=devnull)
    except subprocess.CalledProcessError as e:
        raise RepeatException(str(e))
    except OSError as e:
        raise RepeatException(str(e))


def analyse_repeats(args, run_params, input_assembly, out_folder,
                    log_file, config_file):
    logger.debug("-----Begin repeat analyser log------")

    cmdline = [REPEAT_BIN, "-l", log_file, "-t", str(args.threads)]
    if args.min_overlap is not None:
        cmdline.extend(["-v", str(args.min_overlap)])
    if args.debug:
        cmdline.append("-d")
    cmdline.extend(["-v", str(run_params["min_overlap"])])
    cmdline.extend(["-k", str(run_params["kmer_size"])])
    cmdline.extend([input_assembly, ",".join(args.reads),
                    out_folder, config_file])

    try:
        logger.debug("Running: " + " ".join(cmdline))
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError as e:
        if e.returncode == -9:
            logger.error("Looks like the system ran out of memory")
        raise RepeatException(str(e))
    except OSError as e:
        raise RepeatException(str(e))


def generate_contigs(args, run_params, input_assembly, out_folder,
                    log_file, config_file, repeat_graph, reads_alignment):
    logger.debug("-----Begin contigger analyser log------")

    cmdline = [CONTIGGER_BIN, "-l", log_file, "-t", str(args.threads)]
    if args.debug:
        cmdline.append("-d")
    cmdline.extend(["-v", str(run_params["min_overlap"])])
    cmdline.extend(["-k", str(run_params["kmer_size"])])
    cmdline.extend([input_assembly, ",".join(args.reads),
                    out_folder, config_file, repeat_graph, reads_alignment])

    try:
        logger.debug("Running: " + " ".join(cmdline))
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError as e:
        if e.returncode == -9:
            logger.error("Looks like the system ran out of memory")
        raise RepeatException(str(e))
    except OSError as e:
        raise RepeatException(str(e))
