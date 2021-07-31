#!/usr/bin/env python

from pathlib import Path
import re
from MailFileAction import MailFileAction
from MoveFileAction import MoveFileAction
from MappingEntry import MappingEntry
import csv
import os


# initial setup


scan_path = Path("M:/Scans")
archive_path = scan_path.joinpath("Archiv")
config_path = scan_path.joinpath("config")
mapping_file = config_path.joinpath("mapping.csv")


mapping_entries = []

# read config file
with open(mapping_file.resolve()) as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    next(reader, None)
    for prefix, target_mail, target_path in reader:
        entry = MappingEntry(prefix)

        if target_mail:
            action = MailFileAction(target_mail)
            entry.add_action(action)

        if target_path:
            action = MoveFileAction(target_path)
            entry.add_action(action)

        # we only need entries that actually have to do something
        if entry.has_actions():
            mapping_entries.append(entry)


pattern = r"\S+_\d+.pdf"
files = map(lambda x: str(x), scan_path.glob("*.pdf"))
files = filter(re.compile(pattern).match, files)
files = map(lambda x: Path(x), files)

for file in files:
    for mapping_entry in mapping_entries:
        if file.name.upper().startswith(mapping_entry.prefix.upper()):
            mapping_entry.execute_actions(file)

            # if file hasn't been moved by an action
            if file.exists():
                os.rename(file, archive_path.joinpath(file.name))
