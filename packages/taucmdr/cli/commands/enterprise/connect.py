# -*- coding: utf-8 -*-
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
#
"""``project select`` subcommand."""

import getpass
from taucmdr import EXIT_SUCCESS
from taucmdr.cli import arguments
from taucmdr.model.project import Project
from taucmdr.cli.command import AbstractCommand


class EnterpriseConnectCommand(AbstractCommand):
    """``enterprise connect`` subcommand."""

    def _construct_parser(self):
        usage = "%s <username> [arguments]" % self.command
        parser = arguments.get_parser(prog=self.command, usage=usage, description=self.summary)
        parser.add_argument('username', help="TAU Enterprise username", metavar='<username>')
        parser.add_argument('--key',
                            help="A pre-existing API key to use in place of the password.",
                            metavar='<key>',
                            default=None)
        parser.add_argument('--db',
                            help="The name of the remote database to use",
                            metavar='<db>',
                            default=None)
        return parser

    def main(self, argv):
        args = self._parse_args(argv)
        proj_ctrl = Project.controller()
        if args.key is not None:
            proj_ctrl.connect(args.key, db_name=args.db)
        else:
            username = args.username
            password = getpass.getpass()
            proj_ctrl.connect_with_password(username, password, db_name=args.db)
        return EXIT_SUCCESS


COMMAND = EnterpriseConnectCommand(__name__, summary_fmt=("Connect the current project to TAU Enterprise storage."))
