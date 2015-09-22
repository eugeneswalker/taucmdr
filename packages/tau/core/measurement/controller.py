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
"""Measurement data model controller."""

from tau.error import ConfigurationError
from tau.core.controller import Controller, ByName


class Measurement(Controller, ByName):
    """Measurement data controller."""      
    
    def on_create(self):
        super(Measurement, self).on_create()
        def get_flag(key):
            return self.attributes[key]['argparse']['flags'][0]  # pylint: disable=no-member

        if not (self['profile'] or self['trace']):
            profile_flag = get_flag('profile')
            trace_flag = get_flag('trace')
            raise ConfigurationError("Profiling, tracing, or both must be enabled",
                                     "Specify %s or %s or both" % (profile_flag, trace_flag))
        
        if self['source_inst'] == 'never' and self['compiler_inst'] == 'never' and not self['sample']:
            source_inst_flag = get_flag('source_inst')
            compiler_inst_flag = get_flag('compiler_inst')
            sample_flag = get_flag('sample')
            raise ConfigurationError("At least one instrumentation method must be used",
                                     "Specify %s, %s, or %s" % (source_inst_flag, compiler_inst_flag, sample_flag))
