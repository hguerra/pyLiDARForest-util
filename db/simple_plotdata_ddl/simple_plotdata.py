# -*- coding: utf-8 -*-
import codecs
import csv
import logging
import os.path as ospath
import pprint
import traceback
from multiprocessing import cpu_count, current_process, Process

import pytaxize
import re
import unidecode

from stuff.dbutils import dbutils


def new_filename(filename, prefix="", sulfix="", extension=None):
    path = ospath.dirname(filename)
    filename = ospath.basename(filename)
    filename, ext = ospath.splitext(filename)
    ext = extension or ext
    multi_bat = "{}{}{}{}".format(prefix, filename, sulfix, ext)
    return ospath.join(path, multi_bat)


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
    return data, reader.fieldnames


def dict_to_csv(path, data, fields=None, sep=";", _id="_id"):
    if isinstance(data, dict):
        elements = []
        iteritems = sorted(data.keys())
        for k in iteritems:
            items = data[k]
            items[_id] = k
            elements.append(items)
            if not fields:
                fields = sorted(items.keys())
        data = elements

    assert isinstance(data, list)
    assert isinstance(fields, list)

    try:
        with open(path, 'w') as f:
            writer = csv.DictWriter(f, delimiter=sep, lineterminator="\n", fieldnames=fields)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except IOError:
        logging.error("I/O error: {}".format(path))
    return


def get_connection(dbname="simple_plotdata", host="localhost", user="eba", password="ebaeba18", template="pg_default"):
    return dbutils(host, user, password, dbname, template)


def insert_db(tablename, fields, data, nullvalue):
    assert isinstance(tablename, str)
    assert isinstance(fields, list) or isinstance(fields, tuple)
    assert isinstance(data, list)

    assert len(fields) > 0
    assert len(data) > 0
    assert isinstance(data[0], dict)

    success = True
    db = get_connection()
    try:
        db.execute("BEGIN;")
        db.initsqlvalidfieldnames(fields)
        added = db.addrecs(tablename, fields, data, nullvalue=nullvalue)
        db.execute("COMMIT;")
        logging.info("Records added: {}".format(added))
    except:
        logging.error("Error to insert {} to table {}: {}\n".format(str(len(data)), tablename, traceback.format_exc()))
        success = False
        db.execute("ROLLBACK;")
    finally:
        db.close()
    return success


def get_data_id(table, key="name", value="id"):
    db = get_connection()
    res = db.selectMappedTable(table, geom=False)

    data = {}
    for r in res:
        data[r[key]] = r[value]
    db.close()
    return data


def get_data(table, key=None, where=None, limit=None):
    db = get_connection()
    res = db.selectMappedTable(table, where=where, limit=limit, geom=False)
    db.close()

    if key:
        data = {}
        for r in res:
            data[r[key]] = r
        res = data
    return res


def get_last_value_from_sequence(seq):
    db = get_connection()
    last_value = db.getdata("SELECT last_value FROM {};".format(seq))[0][0]
    db.close()
    return last_value


def levenshtein(str1, str2):
    if str1 != str2:
        m = len(str1)
        n = len(str2)
        d = []
        for i in range(m + 1):
            d.append([i])
        del d[0][0]
        for j in range(n + 1):
            d[0].append(j)
        for j in range(1, n + 1):
            for i in range(1, m + 1):
                if str1[i - 1] == str2[j - 1]:
                    d[i].insert(j, d[i - 1][j - 1])
                else:
                    minimum = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + 2)
                    d[i].insert(j, minimum)
        return d[-1][-1]
    return 0


def suggestion(value, options):
    options.sort()

    word_default = ""
    substr = []
    distance = len(value)
    word = word_default
    for op in options:
        if op.find(value) > 0:
            substr.append(op)

        d = levenshtein(value, op)
        if d < distance:
            distance = d
            word = op
    if float(distance) < len(value) * 0.6:
        return word

    if len(substr) == 1:
        return substr[0]
    return word_default


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def thread(elements, __sof__, cpus=cpu_count()):
    n = len(elements) / cpus
    logging.info("Running '{}' using {} cpus and {} elements by cpu...".format(__sof__.func_name, cpus, n))
    procs = []
    for el in chunks(elements, n):
        proc = Process(target=__sof__, args=(el,))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()


def pretty_printer(elements, width=40, keys=("common_name", "family", "genus", "species")):
    header = "|{}"
    empty_space = " "
    empty_str = ""
    end_concat = " |"
    sep_concat = "-"
    line_template = "| {} | {} | {} | {} |"
    cols = []
    for k in keys:
        k = empty_space + k.center(width, empty_space) + end_concat
        cols.append(k)

    print(header.format(empty_str.join(cols)))
    print(line_template.format(empty_str.center(width, sep_concat), empty_str.center(width, sep_concat),
                               empty_str.center(width, sep_concat), empty_str.center(width, sep_concat)))

    iteritems = sorted(elements.keys())
    for c in iteritems:
        p = elements[c]
        print(line_template.format(p[keys[0]].center(width, empty_space), p[keys[1]].center(width, empty_space),
                                   p[keys[2]].center(width, empty_space), p[keys[3]].center(width, empty_space)))


def normalize(s, encoding="latin-1", replace_hyphen=False, replace_multiple_space=False, remove_prepositions=False, join=False):
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


def split_alphanumeric(s):
    pattern_alphanumeric = r"([0-9]+)(.*)"
    p = re.compile(pattern_alphanumeric)
    return p.findall(s)


def is_list_empty(in_list):
    if isinstance(in_list, list):
        return all(map(is_list_empty, in_list))
    return False


def global_names_resolver(names, gbif=False):
    """
    Retrieve data sources used in Global Names Index or GBIF’s parser API, see
    http://gni.globalnames.org/ for information.
    :param names: List of taxonomic names
    :return: List with results or pandas DataFrame
    """
    if gbif:
        res = pytaxize.gbif_parse(scientificname=names)
    else:
        try:
            res = pytaxize.gnr_resolve(names, best_match_only=True)
        except SystemExit as err:
            logging.error(err)
            res = [[]]
    return res


def spell_check(words, s, error_column="error_colon_name"):
    if words and s not in words:
        for key, values in words.iteritems():
            if s in values[error_column]:
                logging.info("Changing '{}' to '{}'".format(s, key))
                return key
        logging.warning("Error to find '{}'".format(s))
    return s


def get_dictionary(path, key="common_name", error_column="error_common_name", sep=";"):
    base = {}
    raw_base, _ = csv_as_list(path)
    for row in raw_base:
        row[error_column] = row[error_column].split(sep)
        mkey = row[key]
        del row[key]
        base[mkey] = row
    return base


def get_key(nullvalue, *args):
    for arg in args:
        if arg == nullvalue:
            return
    return ";".join(args)


def each_taxonomy(elements, __sof__):
    for raw in elements:
        raw_id = normalize(raw["Numero"])
        family = normalize(raw["Familia"])
        genus = normalize(raw["Genero"])
        species = normalize(raw["Especie"])
        density = normalize(raw["Densidade da madeira"]).replace(",", ".")
        region = normalize(raw["Regiao"])
        article_reference = normalize(raw["N_referencia"])
        __sof__(raw_id, family, genus, species, density, region, article_reference)


def addrecs(table, dataset, field="name", nullvalue="na"):
    db = get_connection()
    fields = [field]
    db.initsqlvalidfieldnames(fields)

    data = []
    for rec in dataset:
        data.append({field: rec})
    count = db.addrecs(table, fields, data, nullvalue=nullvalue)
    db.close()
    return count


def insert_family_genus_species(elements, __sof__):
    logging.info("Inserting in db family, genus and species...")
    raw_family = set()
    raw_genus = set()
    raw_species = set()

    def populate(raw_id, family, genus, species, density, region, article_reference):
        raw_family.add(family)
        raw_genus.add(genus)
        raw_species.add(species)

    __sof__(elements, populate)

    added = addrecs("family", raw_family)
    logging.info("Records added: {}".format(added))

    added = addrecs("genus", raw_genus)
    logging.info("Records added: {}".format(added))

    added = addrecs("species", raw_species)
    logging.info("Records added: {}".format(added))


def insert_taxonomy(elements, nullvalue="na"):
    logging.info("Inserting in db taxonomy...")
    data_family = get_data_id("family")
    data_genus = get_data_id("genus")
    data_species = get_data_id("species")

    data = []
    tablename = "taxonomy"
    fields = ["family_id", "genus_id", "species_id", "density", "region", "article_reference"]

    def populate(raw_id, family, genus, species, density, region, article_reference):
        try:
            rec = {
                fields[0]: int(data_family[family]),
                fields[1]: int(data_genus[genus]),
                fields[2]: int(data_species[species]),
                fields[3]: float(density),
                fields[4]: region,
                fields[5]: int(article_reference)
            }
            data.append(rec)
        except:
            logging.error("Error to process taxonomy with id {}: {}\n".format(raw_id, traceback.format_exc()))

    each_taxonomy(elements, populate)
    insert_db(tablename, fields, data, nullvalue)


def each_measurements(elements, __sof__):
    nodata = "na"
    col_family = "Familia"
    col_genus = "Genero"
    col_species = "Especie"
    col_tree_id = "N"
    for raw in elements:
        raw_id = raw["_id"]
        plot = normalize(raw["Parcela"])
        year = normalize(raw["Ano"])
        dap = normalize(raw["DAP"]).replace(",", ".")
        height = normalize(raw["Altura"]).replace(",", ".")
        raw_information_plot = normalize(raw["Obs_parcela"])
        raw_information_height = normalize(raw["Altura_medida_estimada"])
        raw_information_dead = normalize(raw["Morta"])
        raw_information_type = normalize(raw["Tipo"])
        common_name = normalize(raw["Nome_comum"], replace_hyphen=True, replace_multiple_space=True, remove_prepositions=True)

        family = nodata
        genus = nodata
        species = nodata
        tree_id = nodata
        raw_information_tree_id = nodata
        if col_family in raw:
            family = normalize(raw[col_family])
        if col_genus in raw:
            genus = normalize(raw[col_genus])
        if col_species in raw:
            species = normalize(raw[col_species])
        if col_tree_id in raw:
            tree_id = normalize(raw[col_tree_id], replace_hyphen=True, replace_multiple_space=True, join=True)
            if tree_id.isalpha():
                raw_information_tree_id = tree_id
                tree_id = nodata
            elif not tree_id.isdigit():
                match = split_alphanumeric(tree_id)[0]
                tree_id = match[0]
                raw_information_tree_id = match[1]

        __sof__(raw_id, plot, tree_id, year, dap, height, raw_information_plot, raw_information_tree_id,
                raw_information_height, raw_information_dead, raw_information_type, family, genus, species, common_name)


def check_common_name(elements, words=None, nullvalue="na"):
    logging.info("Check Common names...")

    exists = {}
    incomplete = {}
    compound_names = []
    options = []
    errors = {}
    error_stats = {
        'diff': 0,
        'total': 0,
        'warn_add_error': "It is the correct name '{}' ({}, {}, {})? Do you mean '{}'?",
        'warn_add_incomplete': "Incomplete row, got only common name '{}'.",
        'info': "Total of common names: {}. Total of possible errors: {}."
    }

    def add_name(key, family, genus, species, common_name, compound_name=None):
        exists[key] = {"family": family, "genus": genus, "species": species, "common_name": common_name}
        options.append(common_name)
        if compound_name:
            compound_names.extend(compound_name)

    def add_incomplete_name(key, family, genus, species, common_name, _id):
        logging.warning(error_stats["warn_add_incomplete"].format(common_name))
        incomplete[key] = {"_id": _id, "family": family, "genus": genus, "species": species, "common_name": common_name}

    def add_error(key, family, genus, species, common_name, sug):
        logging.warning(error_stats["warn_add_error"].format(common_name, family, genus, species, sug))
        errors[key] = {"family": family, "genus": genus, "species": species, "common_name": common_name}
        error_stats["diff"] = error_stats["diff"] + 1

    def increment_stats():
        error_stats["total"] = error_stats["total"] + 1

    def populate(raw_id, plot, tree_id, year, dap, height, raw_information_plot,
                 raw_information_height, raw_information_dead, raw_information_type,
                 family, genus, species, common_name):
        common_name = spell_check(words, common_name)
        key = get_key(nullvalue, family, genus, species, common_name)
        if not key:
            return add_incomplete_name(key, family, genus, species, common_name, raw_id)

        if key not in exists:
            sug = suggestion(common_name, options)
            endswithalpha = common_name[-1:].isalpha()

            if sug and sug != common_name and endswithalpha:
                common_compound_name = common_name.split()
                sug_compound_name = sug.split()
                has_same_size = len(common_compound_name) == len(sug_compound_name)
                is_compound = len(common_compound_name) > 1 and len(sug_compound_name) > 1

                if not has_same_size or is_compound and not suggestion(common_compound_name[1], compound_names):
                    add_name(key, family, genus, species, common_name, compound_name=common_compound_name[1:])
                else:
                    add_error(key, family, genus, species, common_name, sug)
            else:
                add_name(key, family, genus, species, common_name)
            increment_stats()

    each_measurements(elements, populate)
    logging.info(error_stats["info"].format(error_stats["total"], error_stats["diff"]))
    return exists, errors, incomplete


def check_common_name_db(elements, path, nullvalue="na"):
    logging.info("Inserting in db common_names...")
    data_family = get_data_id("family")
    data_genus = get_data_id("genus")
    data_species = get_data_id("species")
    data_taxonomy = get_data("taxonomy", key="species_id")

    options_species = data_species.keys()
    options_species_cache = {}

    save = {}
    for row in elements:
        family = row["family"]
        genus = row["genus"]
        species = row["species"]
        common_name = row["common_name"]
        if species in data_species:
            sp_id = data_species[species]
            taxonomy = data_taxonomy[sp_id]
            if family not in data_family:
                fm_id = taxonomy["family_id"]
                logging.warning("Family is different of taxonomy table ({}), got '{}'.".format(fm_id, family))
            if genus not in data_genus:
                gn_id = taxonomy["genus_id"]
                logging.warning("Genus is different of taxonomy table ({}), got '{}'.".format(gn_id, genus))
        else:
            if species in options_species_cache:
                sug = options_species_cache[species]
            else:
                sug = suggestion(species, options_species)

            msg = ""
            if sug:
                msg = " Do you mean '{}'?".format(sug)
            logging.error("Species '{}' (family: '{}', genus: '{}', common name: '{}') not found in taxonomy table."
                          .format(species, family, genus, common_name) + msg)
            key = get_key(nullvalue, species, family, genus, common_name)
            if key not in save:
                save[key] = {
                    "family": family,
                    "genus": genus,
                    "species": species,
                    "common_name": common_name,
                    "suggestion": sug
                }

    dict_to_csv(path.format(current_process().name), save)


def check_species(elements, errors, path, replace=False):
    logging.info("Check species using global resolver...")

    col_common_name = "common_name"
    col_family = "family"
    col_genus = "genus"
    col_species = "species"
    col_id = "_id"
    col_match = "canonical_form"
    msg_error = "Species '{}' not found in global names. Rows: {}."
    msg_warning_sp = "Updating species '{}' to '{}' based on global names. Rows: {}."
    msg_warning_fam = "Updating family '{}' to '{}' based on global names. Rows: {}."
    msg_warning_gen = "Updating genus '{}' to '{}' based on global names. Rows: {}."

    def reduce_species(array):
        species_id = {}
        new_elements = {}
        for el in array:
            el_id = el[col_id]
            sp = el[col_species]
            if sp not in species_id:
                species_id[sp] = []
            species_id[sp].append(el_id)
            del el[col_id]
            new_elements[el_id] = el
        return new_elements, species_id

    def classify(request):
        ranks = request["classification_path_ranks"].split("|")
        classification_path = request["classification_path"].split("|")
        family_idx = ranks.index(col_family) if col_family in ranks else None
        genus_idx = ranks.index(col_genus) if col_genus in ranks else None

        res_family = classification_path[family_idx].lower() if family_idx else family_idx
        res_genus = classification_path[genus_idx].lower() if genus_idx else genus_idx
        return res_family, res_genus, request[col_match].lower()

    elements, names_species = reduce_species(elements)
    names = names_species.keys()
    resolver = global_names_resolver(names)
    for idx, res in enumerate(resolver):
        species = names[idx]
        rows_id = names_species[species]
        srows_id = str(rows_id)
        if is_list_empty(res):
            logging.error(msg_error.format(species, srows_id))
            errors.add(species)
        else:
            family, genus, canonical = classify(res[0])
            for _id in rows_id:
                el = elements[_id]
                el_fam = el[col_family]
                el_gen = el[col_genus]
                if canonical != species:
                    logging.warning(msg_warning_sp.format(species, canonical, srows_id))
                    if replace:
                        el[col_species] = canonical
                if family and family != el_fam:
                    logging.warning(msg_warning_fam.format(el_fam, family, srows_id))
                    if replace:
                        el[col_family] = family
                if genus and genus != el_gen:
                    logging.warning(msg_warning_gen.format(el_gen, genus, srows_id))
                    if replace:
                        el[col_genus] = genus

    save = {}
    for species in errors:
        if species not in names_species:
            continue
        rows_id = names_species[species]
        for _id in rows_id:
            row = elements[_id]
            common_name = row[col_common_name]
            family = row[col_family]
            genus = row[col_genus]
            save[_id] = {
                col_family: family,
                col_genus: genus,
                col_species: species,
                col_common_name: common_name
            }

    dict_to_csv(path, save)


def insert_common_name(elements, words=None, nullvalue="", error_columm="error", add=False):
    logging.info("Inserting in db common_names...")
    data_family = get_data_id("family")
    data_genus = get_data_id("genus")
    data_species = get_data_id("species")

    def each(__sof__):
        for row in elements:
            __sof__(row["family"], row["genus"], spell_check(words, row["species"], error_column=error_columm),
                    row["common_name"])

    if add:
        raw_family = set()
        raw_genus = set()
        raw_species = set()

        def populate_insert_family_genus_species(family, genus, species, common_name):
            if family not in data_family:
                raw_family.add(family)
            if genus not in data_genus:
                raw_genus.add(genus)
            if species not in data_species:
                raw_species.add(species)

        each(populate_insert_family_genus_species)

        added = addrecs("family", raw_family, nullvalue=nullvalue)
        logging.info("Records added: {}".format(added))

        added = addrecs("genus", raw_genus, nullvalue=nullvalue)
        logging.info("Records added: {}".format(added))

        added = addrecs("species", raw_species, nullvalue=nullvalue)
        logging.info("Records added: {}".format(added))

        data_family = get_data_id("family")
        data_genus = get_data_id("genus")
        data_species = get_data_id("species")

    data = []
    tablename = "common_name"
    fields = ("name", "family_id", "genus_id", "species_id")

    def populate_insert_common_name(family, genus, species, common_name):
        count = 0
        rec = {fields[0]: common_name}
        if family in data_family:
            rec[fields[1]] = data_family[family]
            count += 1
        else:
            logging.warning("Family '{}' not found in 'family' table.".format(family))
            rec[fields[1]] = nullvalue
        if genus in data_genus:
            rec[fields[2]] = data_genus[genus]
            count += 1
        else:
            logging.warning("Genus '{}' not found in 'genus' table.".format(genus))
            rec[fields[2]] = nullvalue
        if species in data_species:
            rec[fields[3]] = data_species[species]
            count += 1
        else:
            logging.warning("Species '{}' not found in 'species' table.".format(species))
            rec[fields[3]] = nullvalue
        if count > 0:
            data.append(rec)
        else:
            logging.error("Common name '{}' does not have other attributes.".format(common_name))

    each(populate_insert_common_name)
    insert_db(tablename, fields, data, nullvalue)


def insert_measurements(elements, nullvalue="", nodata="na", height_measured="med", insert_information=True, last_information_id=None):
    logging.info("Load family, genus and species from DB...")
    data_family = get_data_id("family")
    data_genus = get_data_id("genus")
    data_species = get_data_id("species")
    data_common_name = get_data_id("common_name")
    data_common_name_all = get_data("common_name", key="id")
    last_information_id = last_information_id or get_last_value_from_sequence("information_id_seq")

    if insert_information:
        data_information = []
        tablename_information = "information"
        fields_information = ("plot", "height", "dead", "type")
        estimated = "ESTIMATED"
        measured = "MEASURED"

        def populate_insert_information(raw_id, plot, tree_id, year, dap, height, raw_information_plot, raw_information_tree_id,
                raw_information_height, raw_information_dead, raw_information_type, family, genus, species, common_name):
            information_plot = nullvalue
            if raw_information_plot != nodata:
                information_plot = raw_information_plot

            information_height = estimated
            if raw_information_height == height_measured:
                information_height = measured

            information_type = nullvalue
            if raw_information_type != nodata:
                information_type = raw_information_type

            rec = {
                fields_information[0]: information_plot,
                fields_information[1]: information_height,
                fields_information[2]: raw_information_dead != nodata,
                fields_information[3]: information_type
            }

            data_information.append(rec)

        each_measurements(elements, populate_insert_information)

        logging.info("Inserting information...")
        insert_db(tablename_information, fields_information, data_information, nullvalue)

    data_measurements = []
    tablename_measurements = "measurements"
    fields_measurements = ("common_name_id", "family_id", "genus_id", "species_id", "information_id", "tree_id", "plot",
                           "year", "dap", "height")

    data_information = get_data("information", key="id", where="id > {}".format(last_information_id))

    def populate_insert_measurements(raw_id, plot, tree_id, year, dap, height, raw_information_plot, raw_information_tree_id,
                raw_information_height, raw_information_dead, raw_information_type, family, genus, species, common_name):

        information_id = data_information[last_information_id + raw_id]["id"]

        family_id = None
        if family in data_family:
            family_id = data_family[family]

        genus_id = None
        if genus in data_genus:
            genus_id = data_genus[genus]

        species_id = None
        if species in data_species:
            species_id = data_species[species]

        common_name_id = None
        for _id, row in data_common_name_all.iteritems():
            if family_id == row["family_id"] and genus_id == row["genus_id"] and species_id == row["species_id"]:
                common_name_id = _id
                break

        if not common_name_id and common_name in data_common_name:
            common_name_id = data_common_name[common_name]

        if tree_id == nodata:
            tree_id = nullvalue

        if year == nodata:
            year = nullvalue

        if dap == nodata:
            dap = nullvalue

        if height == nodata:
            height = nullvalue

        rec = {
            fields_measurements[0]: common_name_id or nullvalue,
            fields_measurements[1]: family_id or nullvalue,
            fields_measurements[2]: genus_id or nullvalue,
            fields_measurements[3]: species_id or nullvalue,
            fields_measurements[4]: information_id,
            fields_measurements[5]: tree_id,
            fields_measurements[6]: plot,
            fields_measurements[7]: year,
            fields_measurements[8]: dap,
            fields_measurements[9]: height,
        }

        data_measurements.append(rec)

    each_measurements(elements, populate_insert_measurements)

    logging.info("Inserting measurements")
    insert_db(tablename_measurements, fields_measurements, data_measurements, nullvalue)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Running script to populate 'simple_plotdata'")
    pp = pprint.PrettyPrinter(indent=4).pprint

    ## taxonomy
    # path_taxonomy = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\fam_gen_esp_densidade.csv"
    # raw_taxonomy, _ = csv_as_list(path_taxonomy)

    ## insert family, genus and species
    # insert_family_genus_species(raw_taxonomy, each_taxonomy)

    ## inserted taxonomy
    # insert_taxonomy(raw_taxonomy)

    ## common name
    # path_base = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\base_jaraua.csv"
    # spell_base = get_dictionary(path_base)
    #
    # path_measurements = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\JARAUA_2017_RESUMO.csv"
    # check_log = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\base.csv"
    # raw_measurements, _ = csv_as_list(path_measurements)
    #
    # ch_exists, ch_errors, _ = check_common_name(raw_measurements, spell_base)
    # dict_to_csv(check_log, reduce(lambda x, y: dict(x, **y), (ch_exists, ch_errors)))
    #

    # path_common_names = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\Banco_nomes_INPA.csv"
    # path_common_names_export = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\inpa\inpa_{}.csv"
    # raw_common_names, _ = csv_as_list(path_common_names, is_normalize=False)
    #
    # def check(elements):
    #     check_common_name_db(elements, path_common_names_export)
    #
    # thread(raw_common_names, check, cpus=6)

    # path_common_names = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\base_jaraua2.csv"
    # raw_common_names, _ = csv_as_list(path_common_names, is_normalize=False)
    # insert_common_name(raw_common_names)

    # base_path = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data"
    # errors = set()
    # for i in xrange(1, 8):
    #     name = "inpa_Process-{}.csv".format(i)
    #     elements_path = ospath.join(base_path, "inpa", name)
    #     raw_common_names, _ = csv_as_list(elements_path, is_normalize=True)
    #
    #     output_path = ospath.join(base_path, "global", name)
    #     check_species(raw_common_names, errors, output_path)
    #
    # for err in sorted(errors):
    #     print(err)

    # path_base = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\Errors.csv"
    # spell_base = get_dictionary(path_base, key="species", error_column="error")
    #
    # path_measurements = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\Banco_nomes_INPA.csv"
    # raw_common_names, _ = csv_as_list(path_measurements, is_normalize=False)
    # insert_common_name(raw_common_names, words=spell_base, add=True)

    # path_measurements = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\simple_plotdata_ddl\data\TLO_2015_RESUMO.csv"
    # raw_measurements, _ = csv_as_list(path_measurements)
    # insert_measurements(raw_measurements)
    # insert_measurements(raw_measurements, insert_information=False, last_information_id=6538)

    # last_information_id = 6538
    # def populate(raw_id, plot, tree_id, year, dap, height, raw_information_plot,
    #                                  raw_information_tree_id,
    #                                  raw_information_height, raw_information_dead, raw_information_type, family, genus,
    #                                  species, common_name):
    #
    #     info_id = last_information_id + raw_id
    #     info_tree_id = "'{}'".format(raw_information_tree_id)
    #     if info_tree_id == "'na'":
    #         info_tree_id = "NULL"
    #
    #     sql = "UPDATE information SET tree_id = {} WHERE id = {};".format(info_tree_id, info_id)
    #     print(sql)
    # each_measurements(raw_measurements, populate)

    logging.info("done.")
