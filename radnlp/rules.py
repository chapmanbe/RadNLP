"""This module containes functions for reading rules and schema for document
classification based on pyConTextNLP parsing"""
import platform

if platform.python_version_tuple()[0] == '2':
    import urllib2.urlopen as urlopen
    import urllib2.urlparse as urlparse
else:
    from urllib.request import urlopen
    import urllib.parse as urlparse

def read_rules(fname):
    """read the sentence level rules"""

    p = urlparse.urlparse(fname)

    if not p.scheme:
        fname = "file://"+fname

    f0 = urlopen(fname)

    data = f0.readlines()
    class_rules = {}
    category_rules = []
    severity_rules = []
    for d in data:
        if platform.python_version_tuple()[0] == '2':
            tmp = d.strip().split(",")
        else:
            tmp = d.decode('utf-8').strip().split(",")

        if not tmp[0][0] == "#":  # '#' comment character
            if tmp[0] == "@CLASSIFICATION_RULE":
                r = class_rules.get(tmp[1],
                                    {"LABEL":"",
                                     "DEFAULT":"",
                                     "RULES":[]})
                value = int(tmp[3])
                if tmp[2] == 'DEFAULT':
                    r["DEFAULT"] = value
                elif tmp[2] == 'RULE':
                    rcs = []
                    for rc in tmp[4:]:
                        rcs.append(rc)
                    r["RULES"].append((value, rcs))
                class_rules[tmp[1]] = r
            elif tmp[0] == "@CATEGORY_RULE":
                category_rules.append((tmp[1], [r for r in tmp[2:]]))
            elif tmp[0] == "@SEVERITY_RULE":
                severity_rules.append((tmp[1], [r for r in tmp[2:]]))

    return class_rules, category_rules, severity_rules
