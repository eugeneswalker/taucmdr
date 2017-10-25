# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, ParaTools, Inc.
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
"""Analysis and visualization"""
import importlib
import sys

from taucmdr import util
import taucmdr.analysis.analyses
from taucmdr.analysis import analyses

_ANALYSES = {}


def get_analyses():
    """Get the available analyses.

    Returns:
        dict of str: :obj:`AbstractAnalysis`: Mapping from analysis name to instance of analysis class
    """
    if not _ANALYSES:
        analyses_module = sys.modules[__name__ + '.analyses']
        for importer, name, ispkg in util.walk_packages(analyses_module.__path__, prefix=analyses_module.__name__ + '.'):
            try:
                analysis_module = importlib.import_module(name)
                _ANALYSES[analysis_module.ANALYSIS.name] = analysis_module.ANALYSIS
            except AttributeError:
                pass
    return _ANALYSES


def get_analysis(name):
    """Get an instance of an analysis by name.

    Args:
        name (str): The name of the analysis.

    Returns:
        :obj:`AbstractAnalysis`: An instance of the named analysis

    Raises:
        KeyError: No analysis by that name is registered.
    """
    return get_analyses()[name]