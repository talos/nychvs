#!/usr/bin/env python

# By John Krauss
# Copyright 2013

#  This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licences/>

# Convert a dat file to CSV according to a JSON schema.

import json
import os
import sys


def parse_dat(path, schema):
    """
    Yield a parsed line for every line in the dat.
    """
    with open(path, 'r') as dat:
        for line in dat:
            out = {}
            for chars, name, fields in schema:
                # If only one char specified, read one character only.
                if len(chars) == 1:
                    val = line[chars[0]:chars[0] + 1]
                else:
                    val = line[chars[0]:chars[1] + 1]

                # Use the field-specified value if there is one, otherwise
                # leave as-is
                val = fields.get(val, val)

                out[name] = val

            yield out

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write("""
    usage: {0} <path_to_dat> <year> <path_to_schema>

""".format(sys.argv[0]))
        sys.exit(1)

    sep = u'\t'
    nl = u'\n'

    year = sys.argv[2]
    schema = json.load(open(sys.argv[3], 'r'))
    cols = sorted([c[1] for c in schema])

    sys.stdout.write(sep.join([u'file', u'year']) + sep)
    sys.stdout.write(sep.join(cols) + nl)
    for out in parse_dat(sys.argv[1], schema):
        sys.stdout.write(sep.join([os.path.basename(sys.argv[1]), year]) + sep)
        sys.stdout.write(sep.join([out[c] for c in cols]) + nl)

"""
SELECT COUNT(*), Borough, `Sub-borough Area`, AVG(CAST(`Monthly Contract Rent` AS INT))
FROM occ_2011
WHERE CAST(`Monthly Contract Rent` AS INT) > 0
GROUP BY Borough, `Sub-borough Area`
ORDER BY Borough, `Sub-Borough Area`

"""
