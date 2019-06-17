import os
import os.path as path
import sys
import datetime
import sonosco.common.path_utils as path_utils

from time import time
from sonosco.common.utils import copy_code


class Experiment:
    """
    Generates a folder where all experiments will be stored an then a named experiment with current
    timestamp and provided name. Automatically starts logging the console output and creates a copy
    of the currently executed code in the experiment folder. The experiment's subfolder paths are provided
    to the outside as member variables. It also allows adding of more subfolders conveniently.
    Args:
        experiment_name (string): name of the exerpiment to be created
        experiments_path (string): location where all experiments will be stored, default is './experiments'
    Example:
        >>> experiment = Experiment('mnist_classification')
        >>> print(experiment.plots) # path to experiment plots
    """

    def __init__(self,
                 experiment_name,
                 experiments_path=None,
                 sub_directories=("plots", "logs", "code"),
                 exclude_dirs=('__pycache__', '.git', 'experiments'),
                 exclude_files=('.pyc',)):

        self.experiments_path = self._set_experiments_dir(experiments_path)
        self.name = self._set_experiment_name(experiment_name)
        self.path = path.join(self.experiments_path, self.name)     # path to current experiment
        self.logs = path.join(self.experiments_path, "logs")
        self.code = path.join(self.experiments_path, "code")
        self._sub_directories = sub_directories

        self._exclude_dirs = exclude_dirs
        self._exclude_dirs.extend(exclude_dirs)
        self._exclude_files = exclude_files
        self._exclude_files.extend(exclude_files)

        self._init_directories()
        self._copy_sourcecode()

    @staticmethod
    def _set_experiments_dir(experiments_path):
        if experiments_path is not None:
            return experiments_path

        local_path = os.path.dirname(sys.argv[0])
        local_path = local_path if local_path != '' else './'
        return path.join(local_path, "experiments")

    @staticmethod
    def _set_experiment_name(experiment_name):
        date_time = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d_%H:%M:%S')
        return f"{date_time}_{experiment_name}"

    def _init_directories(self):
        """ Create all basic directories. """
        path_utils.try_create_directory(self.experiments_path)
        path_utils.try_create_directory(path.join(self.experiments_path, self.name))
        for sub_dir_name in self._sub_directories:
            self.add_directory(sub_dir_name)

    def _add_member(self, key, value):
        """ Add a member variable named 'key' with value 'value' to the experiment instance. """
        self.__dict__[key] = value

    def _copy_sourcecode(self):
        """ Copy code from execution directory in experiment code directory. """
        sources_path = os.path.dirname(sys.argv[0])
        sources_path = sources_path if sources_path != '' else './'
        copy_code(sources_path, self.code,
                  exclude_dirs=self._exclude_dirs,
                  exclude_files=self._exclude_files)

    def add_directory(self, dir_name):
        """
        Add a sub-directory to the experiment. The directory will be automatically
        created and provided to the outside as a member variable.
        """
        # store in sub-dir list
        if dir_name not in self._sub_directories:
            self._sub_directories.append(dir_name)
        # add as member
        dir_path = path.join(self.experiments_path, self.name, dir_name)
        self._add_member(dir_name, dir_path)
        # create directory
        path_utils.try_create_directory(dir_path)

    @staticmethod
    def add_file(folder_path, filename, content):
        """ Adds a file with provided content to folder. Convenience function. """
        with open(path.join(folder_path, filename), 'w') as text_file:
            text_file.write(content)
