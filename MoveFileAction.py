from FileAction import FileAction
from pathlib import Path
import os


class MoveFileAction(FileAction):

    def __init__(self, path):
        self.path = path

    def execute(self, file: Path):
        """Move the file at the given path
        to the path stored in this object"""
        os.rename(file, self.path)
        pass
