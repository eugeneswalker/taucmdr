#"""
#@file
#@author John C. Linford (jlinford@paratools.com)
#@version 1.0
#
#@brief
#
# This file is part of TAU Commander
#
#@section COPYRIGHT
#
# Copyright (c) 2015, ParaTools, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# (1) Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
# (2) Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
# (3) Neither the name of ParaTools, Inc. nor the names of its contributors may
#     be used to endorse or promote products derived from this software without
#     specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#"""

from tau import logger, arguments, commands, controller
from tau.model.project import Project
from tau.model.target import Target
from tau.model.application import Application
from tau.model.measurement import Measurement


LOGGER = logger.getLogger(__name__)

COMMAND = commands.get_command(__name__)

SHORT_DESCRIPTION = "Create a new project configuration."

USAGE = """
  %(command)s <project_name> [targets] [applications] [measurements] [arguments]
""" % {'command': COMMAND}

HELP = """
'%(command)s' page to be written.
""" % {'command': COMMAND}

PARSER = arguments.getParserFromModel(Project,
                                      prog=COMMAND,
                                      usage=USAGE,
                                      description=SHORT_DESCRIPTION)
PARSER.add_argument('impl_targets',
                    help="Target configurations in this project",
                    metavar='[targets]',
                    nargs='*',
                    default=arguments.SUPPRESS)
PARSER.add_argument('impl_applications',
                    help="Application configurations in this project",
                    metavar='[applications]',
                    nargs='*',
                    default=arguments.SUPPRESS)
PARSER.add_argument('impl_measurements',
                    help="Measurement configurations in this project",
                    metavar='[measurements]',
                    nargs='*',
                    default=arguments.SUPPRESS)
PARSER.add_argument('--targets',
                    help="Target configurations in this project",
                    metavar='t',
                    nargs='+',
                    default=arguments.SUPPRESS)
PARSER.add_argument('--applications',
                    help="Application configurations in this project",
                    metavar='a',
                    nargs='+',
                    default=arguments.SUPPRESS)
PARSER.add_argument('--measurements',
                    help="Measurement configurations in this project",
                    metavar='m',
                    nargs='+',
                    default=arguments.SUPPRESS)


def getUsage():
    return PARSER.format_help()


def getHelp():
    return HELP


def main(argv):
    """
    Program entry point
    """
    args = PARSER.parse_args(args=argv)
    LOGGER.debug('Arguments: %s' % args)

    targets = set()
    applications = set()
    measurements = set()

    for attr, model, dest in [('targets', Target, targets),
                              ('applications', Application, applications),
                              ('measurements', Measurement, measurements)]:
        for name in getattr(args, attr, []):
            found = model.withName(name)
            if not found:
                PARSER.error('There is no %s named %r' %
                             (model.model_name, name))
            dest.add(found.eid)

        for name in getattr(args, 'impl_' + attr, []):
            t = Target.withName(name)
            a = Application.withName(name)
            m = Measurement.withName(name)
            tam = set([t, a, m]) - set([None])
            if len(tam) > 1:
                PARSER.error('%r is ambiguous, please use --targets, --applications,'
                             ' or --measurements to specify configuration type' % name)
            elif len(tam) == 0:
                PARSER.error(
                    '%r is not a target, application, or measurement' % name)
            elif t:
                targets.add(t.eid)
            elif a:
                applications.add(a.eid)
            elif m:
                measurements.add(m.eid)

        try:
            delattr(args, 'impl_' + attr)
        except AttributeError:
            pass

    args.targets = list(targets)
    args.applications = list(applications)
    args.measurements = list(measurements)

    try:
        Project.create(args.__dict__)
    except controller.UniqueAttributeError:
        PARSER.error("A project named '%s' already exists." % args.name)

    LOGGER.info('Created a new project named %r.' % args.name)
    return commands.executeCommand(['project', 'list'], [args.name])
