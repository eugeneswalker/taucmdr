# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, ParaTools, Inc.
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
#
"""``trial renumber`` subcommand."""

from taucmdr.cli import arguments
from taucmdr.cli.command import AbstractCommand
from taucmdr.model.trial import Trial
from taucmdr.model.project import Project
from taucmdr.cli.commands.trial.delete import COMMAND as trial_delete_cmd

class TrialRenumberCommand(AbstractCommand):
    """``trial renumber`` subcommand."""

    def _construct_parser(self):
        usage = "%s [trial_number...] --renumber [new_trial_number...]"
        parser = arguments.get_parser(prog=self.command, usage=usage, description=self.summary)
        parser.add_argument('trial_numbers',
                             help="Trials to renumber",
                             metavar='<trial_number>',
                             nargs='+',
                             default=arguments.SUPPRESS)
        parser.add_argument('--to',
                             help="New trial numbers",
                             metavar='<new_trial_number>',
                             nargs='+',
                             default=arguments.SUPPRESS)
        return parser

    def trial_exists(self, trial_id):
        proj_ctrl = Project.controller()
        trial_ctrl = Trial.controller(proj_ctrl.storage)
        records = trial_ctrl.search({'number': trial_id})
        return (records != [])

    def create_new_trial(self, old, new):
        proj_ctrl = Project.controller()
        trial_ctrl = Trial.controller(proj_ctrl.storage)
        records = dict(trial_ctrl.one({'number': old}))
        records['number'] = new
        trial_ctrl.create(records)


    def main(self, argv):
        args = self._parse_args(argv)
        trial_numbers = []
        for num in getattr(args, 'trial_numbers', []):
            try:
                trial_numbers.append(int(num))
            except ValueError:
                self.parser.error("Invalid trial number: %s" %num)
        new_trial_numbers = []
        for num in getattr(args, 'to', []):
            try:
                new_trial_numbers.append(int(num))
            except ValueError:
                self.parser.error("Invalid trial trial number: %s" %num)
        if len(trial_numbers) != len(new_trial_numbers):
            self.parser.error("Invalid number of trials. Number of old trials ids should be equal to number of new trial ids.")

        for trial_pair in range(0,len(trial_numbers)):
            old = trial_numbers[trial_pair]
            new = new_trial_numbers[trial_pair]
            if self.trial_exists(new):
                self.parser.error("Cannot move trial %s to trial %s. Trial %s already exists." %(old, new, new))
            else:
                self.create_new_trial(old, new)
                trial_delete_cmd.main([str(old)])

COMMAND = TrialRenumberCommand(__name__, summary_fmt="Renumber trial numbers.")
