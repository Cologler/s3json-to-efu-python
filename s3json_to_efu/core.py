# -*- coding: utf-8 -*-
# 
# Copyright (c) 2023~2999 - Cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import collections
import csv
import datetime

from .filetime import from_datetime

EFU_HEADERS = (
    # str, does not endswith with \
    'Filename',

    # int, 0 for directory
    'Size',

    # int
    'Date Modified',

    # int
    'Date Created',

    # int, 32 for file and 16 for directory
    'Attributes'
)

EFU_HEADERS_PYNAME = tuple(x.replace(' ', '_') for x in EFU_HEADERS)

EfuRowItem = collections.namedtuple('EfuRowItem', EFU_HEADERS_PYNAME)

def _replace_keys(d: dict) -> dict:
    return {
        EFU_HEADERS[i]: d[EFU_HEADERS_PYNAME[i]] for i in range(len(EFU_HEADERS))
    }

def write_efu_to(fp, items: list[EfuRowItem]):
    csv_writer = csv.DictWriter(fp, EFU_HEADERS)
    csv_writer.writeheader()
    csv_writer.writerows([
        _replace_keys(x._asdict()) for x in items
    ])

def json_to_efurowitem(json_content: dict, prefix: str) -> EfuRowItem:
    key: str = json_content['Key']
    last_modified = json_content['LastModified']
    size = json_content['Size']

    if key.endswith('/'):
        # folder
        filename = key[:-1]
        attributes = 16
    else:
        # file
        filename = key
        attributes = 32
    date_modified = date_created = from_datetime(
        datetime.datetime.fromisoformat(last_modified)
    )

    if ':' not in prefix:
        prefix += ':'
    filename = f'{prefix}/{filename}'.replace('/', '\\')

    return EfuRowItem(
        filename, size, date_modified, date_created, attributes
    )
