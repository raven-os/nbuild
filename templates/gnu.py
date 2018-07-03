#!/usr/bin/env python3

from templates.autotools import AutotoolsTemplate
from templates.fetchtarball import FetchTarballTemplate


class GnuTemplate(FetchTarballTemplate, AutotoolsTemplate):
    def __init__(self, fetch={}, autotools={}):
        FetchTarballTemplate.__init__(
            self,
            **fetch
        )
        AutotoolsTemplate.__init__(
            self,
            **autotools
        )
