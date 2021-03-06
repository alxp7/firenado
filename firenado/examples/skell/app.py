#!/usr/bin/env python
#
# Copyright 2015-2016 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import skell.handlers
import firenado.tornadoweb
from skell import uimodules


class SkellComponent(firenado.tornadoweb.TornadoComponent):

    def get_handlers(self):
        return [
            (r'/', skell.handlers.IndexHandler),
            (r'/session', skell.handlers.SessionHandler),
            (r'/login', skell.handlers.LoginHandler),
        ]

    def get_ui_modules(self):
        return uimodules

    def install(self):
        """ Component installation functional test.
        This is only printing some output but it could be something more.
        """
        print("Skell app doesn't need to be installed.")
