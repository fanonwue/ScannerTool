from FileAction import FileAction
from pathlib import Path


class MappingEntry:

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.actions = []


    def add_action(self, action: FileAction):
        self.actions.append(action)


    def execute_actions(self, path: Path):
        if not path.name.upper().startswith(self.prefix.upper()):
            return
        for action in self.actions:
            action.execute(path)

    def has_actions(self):
        return bool(self.actions)
