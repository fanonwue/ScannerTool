#!/usr/bin/env python

from pathlib import Path
import re
from SmtpConfig import SmtpConfig
from EmailConfig import EmailConfig
from MailFileAction import MailFileAction
from MoveFileAction import MoveFileAction
from MappingEntry import MappingEntry
import csv
import os
import yaml


# initial setup


config = None
try:
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
except Exception as e:
    print("ERORR: failed to open config.yaml! Aborting...")
    exit(-1)

path_config = config['paths']
smtp_config = SmtpConfig(**config['smtp'])
email_config = EmailConfig(**config['email'])

scan_path = Path(path_config['document_path'])
archive_path = Path(path_config['archive_path'])
mapping_file = Path(path_config['mapping_file'])


mapping_entries = []

# read config file
with open(mapping_file.resolve()) as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    # skip header
    next(reader, None)
    for prefix, target_mail, target_path in reader:
        entry = MappingEntry(prefix)

        if target_mail:
            action = MailFileAction(target_mail, smtp_config, email_config)
            entry.add_action(action)

        if target_path:
            action = MoveFileAction(target_path)
            entry.add_action(action)

        # we only need entries that actually have to do something
        if entry.has_actions():
            mapping_entries.append(entry)


# get all files (excluding directories)
files = filter(Path.is_file, scan_path.iterdir())

regex_config = config['regex']
if regex_config['enabled']:
    # filter according to the provided pattern
    pattern = regex_config['pattern']
    files = map(lambda x: str(x), files)
    files = filter(re.compile(pattern).match, files)
    files = map(lambda x: Path(x), files)


for file in files:
    for mapping_entry in mapping_entries:
        if file.name.upper().startswith(mapping_entry.prefix.upper()):
            mapping_entry.execute_actions(file)

            # if file hasn't been moved by an action
            if file.exists():
                os.rename(file, archive_path.joinpath(file.name))
