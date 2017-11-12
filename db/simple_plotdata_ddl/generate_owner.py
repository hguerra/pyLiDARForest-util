# -*- coding: utf-8 -*-

import codecs
import csv
import logging
import os
import pprint
import re

import unidecode


def extract_number(transect):
    matcher = re.search("T*([0-9]+)", transect)
    if matcher:
        return matcher.group(1).rjust(4, "0")
    return transect


def normalize(s, encoding="latin-1", replace_hyphen=False, replace_multiple_space=False, remove_prepositions=False,
              join=False):
    str_empty = ""
    str_space = " "
    single_quotation_marks = "'"
    if isinstance(s, str):
        s = unicode(s, encoding)
    s = unidecode.unidecode(s)
    s = s.strip().lower()

    s = s.replace(single_quotation_marks, str_empty)
    double_quotation_marks = '"'
    s = s.replace(double_quotation_marks, str_empty)
    prepositions_pt = ("da", "das", "de", "do", "dos")

    if replace_hyphen:
        str_hyphen = "-"
        s = s.replace(str_hyphen, str_space)

    if replace_multiple_space:
        pattern_multiples_space = "\s\s+"
        s = re.sub(pattern_multiples_space, str_space, s)

    if join:
        s = s.replace(str_space, str_empty)

    if remove_prepositions:
        compound_name = s.split()
        if len(compound_name) > 2:
            for i, name in enumerate(compound_name):
                if name in prepositions_pt:
                    del compound_name[i]
            s = str_space.join(compound_name)
    return s


def csv_as_list(path, sep=";", is_normalize=True):
    logging.info("Loading csv from '{}'".format(path))
    data = []
    with codecs.open(path, 'r') as f:
        count = 1
        _id = "_id"
        reader = csv.DictReader(f, delimiter=sep)
        for line in reader:
            if not is_normalize:
                for k, v in line.iteritems():
                    if isinstance(v, str):
                        line[k] = normalize(v,
                                            replace_hyphen=True,
                                            replace_multiple_space=True,
                                            remove_prepositions=True)
            line[_id] = count
            data.append(line)
            count += 1
        fieldnames = [_id] + reader.fieldnames
        fieldnames.sort()
    return data, fieldnames


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Running script to populate 'simple_plotdata'")
    pp = pprint.PrettyPrinter(indent=4).pprint

    spreadsheet_path = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\responsaveis_parcelas.csv"
    pattern_error = "lidar"
    transect_template = "T-{}"

    map_template_init_transects = "Map<String, String> transects = new HashMap<String, String>() {{\n"
    map_template_put_transects = '\tput("{}", "{}");\n'
    map_template_init_owners = "Map<String, String[]> owners = new HashMap<String, String[]>() {{\n"
    map_template_put_owners = '\tput("{}", new String[]{{"{}", "{}"}});\n'
    map_template_end = "}};"

    spreadsheet, fields = csv_as_list(spreadsheet_path, is_normalize=False)
    pp(fields)

    owners = [map_template_init_owners]
    transects = [map_template_init_transects]
    for row in spreadsheet:
        institution = row[fields[1]]
        owner = row[fields[2]]
        plot = row[fields[3]]
        transect_file = row[fields[4]]

        if pattern_error in transect_file.lower():
            logging.warning("Plot '{}' does not have a transect ({}).".format(plot, transect_file))
        else:
            transect_number = extract_number(transect_file)
            transect = transect_template.format(extract_number(transect_file))
            plot = os.path.splitext(plot)[0]

            owners.append(map_template_put_owners.format(plot, owner, institution))
            transects.append(map_template_put_transects.format(plot, transect))

    owners.append(map_template_end)
    transects.append(map_template_end)

    # print("".join(owners))
    print("".join(transects))
