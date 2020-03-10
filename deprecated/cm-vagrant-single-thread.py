#!/usr/bin/env python
"""Vagrant Manager.

Usage:
    cloud vbox create --count <vm_number> [--debug]
    cloud vbox start [--vms=<vmList>] [--debug]
    cloud vbox stop [--vms=<vmList>] [--debug]
    cloud vbox destroy [--vms=<vmList>] [--debug]
    cloud vbox status [--vms=<vmList>]
    cloud vbox list
    cloud vbox ssh NAME
    cloud vbox run COMMAND  [--vms=<vmList>]

    cloud -h

Options:
  -h --help     Show this screen.
  --vm_list=<list_of_vms>  List of VMs separated by commas ex: node-1,node-2

Description:
   put a description here
   
Example:
   put an example here
"""
# TODO: we have command-run-draft and command.py we should integrate this all in a single command.py


import fileinput
import os
import re
import subprocess

import hostlist
from docopt import docopt
from termcolor import colored


# TODO: workspace should be in ~/.cloudmesh/vbox
# TODO: if the workspace is not ther it needs to be created
# TODO: use captal letters as easier to document in other tools
# TODO: implement ssh
# TODO: implement the run that executes the command on the specified hosts

class Vagrant(object):
    """
    TODO: doc
    """

    def __init__(self, debug=False):
        """
        TODO: doc

        :param debug:
        """
        self.workspace = "~/cloudmesh/vagrant_workspace"
        self.path = os.path.join(self.workspace, "Vagrantfile")
        self.debug = debug

    def execute(self, command):
        """
        TODO: doc

        :param command:
        :return:
        """
        if self.debug:
            print(command.strip())
        else:
            subprocess.run(command.strip(),
                           cwd=self.workspace,
                           check=True,
                           shell=True)

    def status(self, name=None):
        """
        TODO: doc

        :param name:
        :return:
        """
        if name is None:
            # start all
            name = ""
        self.execute("vbox status " + str(name))

    def start(self, name=None):
        """
        TODO: doc

        :param name:
        :return:
        """
        if name is None:
            # start all
            name = ""
        self.execute("vbox up " + str(name))

    def stop(self, name=None):
        """
        TODO: doc

        :param name:
        :return:
        """
        if name is None:
            # start all
            name = ""
        self.execute("vbox halt " + str(name))

    def destroy(self, name=None):
        """
        TODO: doc

        :param name:
        :return:
        """
        if name is None:
            name = ""
        self.execute("vbox destroy " + str(name))

    def generate_vagrantfile(self, number_of_nodes):
        """
        TODO: doc

        :param number_of_nodes:
        :return:
        """
        replacement_string = "NUMBER_OF_NODES = " + str(number_of_nodes)
        for line in fileinput.FileInput(os.path.join(self.path), inplace=True):
            line = re.sub("NUMBER_OF_NODES.*(\d+)$", replacement_string, line.rstrip())
            print(line)

    def list(self):
        """
        TODO: doc

        :return:
        """
        with open(self.path, 'r') as f:
            content = f.read()
        print(content)


def process_arguments(arguments):
    """
    TODO: doc

    :param arguments:
    :return:
    """
    debug = arguments["--debug"]
    if debug:
        try:
            columns, rows = os.get_terminal_size(0)
        except OSError:
            columns, rows = os.get_terminal_size(1)

        print(colored(columns * '=', "red"))
        print(colored("Running in Debug Mode", "red"))
        print(colored(columns * '=', "red"))
        print(arguments)
        print(colored(columns * '-', "red"))

    if arguments.get("vbox"):
        provider = Vagrant(debug=debug)
        if arguments.get("create") & arguments.get("--count"):
            provider.generate_vagrantfile(arguments.get("<vm_number>"))

        elif arguments.get("list"):
            provider.status(list)

        else:
            hosts = None
            action = None

            if arguments.get("--vms"):
                hosts = arguments.get("--vms")
                hosts = hostlist.expand_hostlist(hosts)

            if arguments.get("start"):
                action = provider.start
            elif arguments.get("stop"):
                action = provider.stop
            elif arguments.get("destroy"):
                action = provider.destroy
            elif arguments.get("status"):
                action = provider.status

            # do the action
            if action is not None:
                if hosts:
                    for node_name in hosts:
                        action(node_name)
                else:
                    action()


def main():
    """
    TODO: doc

    :return:
    """
    arguments = docopt(__doc__, version='Vagrant Manager 1.0')
    process_arguments(arguments)


if __name__ == "__main__":
    main()
