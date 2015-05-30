#!/usr/bin/env python
#
# Copyright 2015 Flavio Garcia
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
#
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

from __future__ import (absolute_import, division,
                        print_function, with_statement)

import firenado.conf
from firenado.util.argparse_util import ArgumentParserException
from firenado.util.argparse_util import FirenadoArgumentParser
import os
import sys
from tornado import template

# Commands will be registered here. This is done by ManagementCommand
#
command_categories = dict()


def run_from_command_line():
    """ Run Firenado's management commands from a command line
    """
    for key, module in firenado.conf.scaffolding['commands'].iteritems():
        exec('import %s' % module)
    command_index = 1
    for arg in sys.argv[1:]:
        command_index += 1
        if arg[0] != "-":
            break
    parser = FirenadoArgumentParser(prog=os.path.split(sys.argv[0])[1])
    parser.add_argument("command", help="Command to executed")
    try:
        namespace = parser.parse_args(sys.argv[1:command_index])
        if not command_exists(namespace.command):
            show_command_line_usage(parser)
        else:
            run_command(namespace.command, sys.argv[command_index-1:])
    except ArgumentParserException:
        show_command_line_usage(parser, True)


def get_command_header(parser, usage=False):
    """ Return the command line header
    """
    loader = template.Loader(os.path.join(
                firenado.conf.ROOT, 'core','scaffolding', 'templates', 'help'))
    return loader.load("header.txt").generate(parser=parser, usage=usage)


def show_command_line_usage(parser, usage=False):
    """ Show the command line help
    """
    help_header_message = get_command_header(parser, usage)
    loader = template.Loader(os.path.join(
        firenado.conf.ROOT, 'core', 'management', 'templates', 'help'))
    command_template = "  {0.name:15}{0.description:40}"
    help_message = loader.load("main_command_help.txt").generate(
        command_categories=command_categories,
        command_template=command_template
    )
    # TODO: This print has to go. Use proper stream instead(stdout or stderr)
    print(''.join([help_header_message, help_message]))
    print("\n    --name=value    whatever")
    print("    --help          display help")


def command_exists(command):
    """ Check if the given command was registered. In another words if it
    exists.
    """
    for category, commands in command_categories.iteritems():
        for existing_command in commands:
            if command == existing_command.name:
                return True
    return False


def run_command(command, args):
    """ Run all tasks registered in a command.
    """
    for category, commands in command_categories.iteritems():
        for existing_command in commands:
            if command == existing_command.name:
                existing_command.run_tasks(args)

