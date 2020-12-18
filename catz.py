#!/usr/bin/env python3
import sys
from brologparse import parse_log_file

if len(sys.argv) < 2:
  print("Log parser for Bro/Zeek logfiles")
  print("Usage: catz <logfile>")
  sys.exit(1)

entries = []
for entry in parse_log_file(sys.argv[1]):
  entries.append(entry)

fields = []
with open(sys.argv[1], "r") as f:
    separator = f.readline().rstrip("\n").split(" ")[1].encode('raw_unicode_escape').decode('unicode_escape')
    for i in range(5):
        f.readline()
    fields = [field.replace(".", "_") for field in f.readline().rstrip("\n").lstrip("#").split(separator)[1:]]

formatted_entries = []
field_lengths = {}
for field in fields:
    field_lengths[field] = len(field)
for entry in entries:
    formatted_entry = []
    for field in fields:
        formatted_field = ""
        unformatted_field = getattr(entry, field)
        if unformatted_field is not None:
            formatted_field = "{}".format(unformatted_field)
        formatted_entry.append(formatted_field)
        if len(formatted_field) > field_lengths[field]:
            field_lengths[field] = len(formatted_field)
        formatted_entries.append(formatted_entry)
for i, field in enumerate(fields):
    if field_lengths[field] > 80:
        field_lengths[field] = 80
        for entry in formatted_entries:
            if len(entry[i]) > field_lengths[field]:
                entry[i] = entry[i][:field_lengths[field] - 1] + "…"

row_format = "{:>" + "{}".format(len("{}".format(len(formatted_entries)))) + "} | "
separator_line = []
for field in fields:
    row_format += "{:<" + "{}".format(field_lengths[field]) + "}  "
    separator_line.append("-" * field_lengths[field])
print(row_format.format("", *fields))
print(row_format.format("", *separator_line))
i = 1
for entry in formatted_entries:
    print(row_format.format(i, *entry))
    i += 1
