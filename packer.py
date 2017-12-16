#! /usr/bin/env python3

import yaml
import datetime
import os

from task import Task


class Packer(object):
    def __init__(self, config_file):
        with open(config_file) as f:
            self.raw_yaml = f.read()
            f.seek(0)
            self.config = yaml.load(f)

    def collect(self, to=None):
        if to == None:
            to = "/tmp/poker-%s" % datetime.datetime.now().isoformat()

        os.makedirs(to, exist_ok=True)
        tasks = self.config["tasks"]
        for task_name in tasks:
            t = Task(task_name, tasks[task_name])
            t.collect(to)

        self.collection_path = to
        with open(os.path.join(to, "tasks.yml"), "w") as f:
            f.write(self.raw_yaml)
        return to

    def compress(self, to_file=None):
        if to_file == None:
            to_file = os.path.basename(self.collection_path) + ".tar.gz"
            to_file = os.path.join("/tmp", to_file)

        os.system("tar cvfz %s %s" % (to_file, self.collection_path))
        return to_file

    def upload(self):
        pass
