#!/usr/bin/env python
# coding: utf-8

"""
EXPLAIN_WHAT_THIS_IS_ALL_ABOUT_PLEASE

first row is like so: '﻿HEADER'
"""
# Created: 18.12.20

import csv
from pathlib import Path


def get_csv(path: Path) -> list:

    def map_line(line: list, fields: dict) -> dict:
        d = {}
        for k in fields:
            d[fields[k]] = line[k]
        return d

    with open(path) as fp:
        reader = csv.reader(fp, delimiter=';', quotechar='"')
        header = next(reader)
        assert header[0].endswith("HEADER")
        fields = {}
        for i in range(1, len(header)):
            if header[i]:
                fields[i] = header[i]
        data = []
        for row in reader:
            if row[0].endswith("COMMENT"):
                continue
            data.append(map_line(row, fields))
        return data


if __name__ == "__main__":
    path = Path(".") / "Dr-Shiva.csv"
    data = get_csv(path)
