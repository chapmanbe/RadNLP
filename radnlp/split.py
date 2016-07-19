"""
Tools for splitting report and recognizing sections
"""
import re
from textblob import TextBlob

r_headings = re.compile(r"""(?P<heading>([A-Z ]+\s)?[A-Z()]+:)""")
r_digits = re.compile(r"""\d\.""")
r_enumerate = re.compile(r"""((\d(.|:|\))\s)(.+)(?=\n))""")

canned_phrases = ("if you have any question about this report, contact me at:",
                  "i have personally reviewed the images and agree",
                  "i have personally reviewed the images for this examination",
                  "please utilize the following guidance for the management of these patients",
                  "please utilize the following guidance for management",
                  "i have reviewed the images and approve this final report",
                 "the imaging exam has been reviewed and the report has been issued by a radiologist physician",
                 )
def terminate_lists(txt):
    """
    Replace enumerated lists that don't end with a period/question mark
    """
    lists = r_enumerate.findall(txt)
    for l in lists:
        txt = txt.replace(l[0],"%s."%l[0])
    return txt


def get_headings(txt):
    """
    """
    global r_headings
    return [r.group("heading").strip() for r in r_headings.finditer(txt)]
def find_terminating_sentences(txt,phrases=None):
    """

    """
    try:
        if not phrases:
            phrases = ()
        indices = [i for i in [txt.lower().find(p) for p in phrases] if i != -1]
        return min(indices)
    except:
        return None


def get_report(txt,terminating_phrases= None):
    """
    get report text up to any terminating_phrases
    """
    if not terminating_phrases:
        terminating_phrases = canned_phrases
    ti = find_terminating_sentences(txt,terminating_phrases)
    global r_digits
    if ti != -1:
        return r_digits.sub("",txt[:ti])
    else:
        return r_digits.sub("",txt)


def preprocess_report(txt,
                      fix_enumerated_lists=True,
                      drop_boiler_plate=True,
                      canned_phrases=None):
    """
    from a string (txt) containing a report, return the relevant
    portions

    fix_enumerated_lists: boolean.
        If true, use regular expressions to transform enumerated lists into more sentence like structures.
    drop_boiler_plate: boolean.
        If true, only return text preceding canned_phrases
    canned_phrases: None or list.
        List of canned phrases to exlcude as boilerplate
    """
    if fix_enumerated_lists:
        txt = terminate_lists(txt)
    if drop_boiler_plate:
        txt = get_report(txt,terminating_phrases=canned_phrases)
    return txt

def grab_impression(txt):
    """
    grab impression from text via looking for IMPRESSION:
    """
    try:
        return txt[txt.index("IMPRESSION:"):].split("IMPRESSION:")[1]
    except Exception as error:
        print(error)
        return ""


def  get_sections(txt, headings):
    h = headings.pop()


def get_section(txt,heading):
    try:
        loc = txt.index(heading)
        return txt[:loc], txt[loc:].split(heading)[1].strip()
    except Exception as error:
        #print(error, heading, txt)
        return txt, ""


def get_sections_by_headings(txt, sections, headings):
    if not headings:
        return txt, sections
    else:
        h = headings.pop()
        txt, sections[h] = get_section(txt, h)
        return get_sections_by_headings(txt, sections, headings)


def reverse_sections(secs):
    _secs = OrderedDict()
    while secs:
        sec,txt = secs.popitem()
        _secs[sec] = txt
    return _secs


def split_report(txt):
    headings = get_headings(txt)
    txt, secs = get_sections_by_headings(txt, OrderedDict(), headings)
    return reverse_sections(secs)

def get_sentences(report):
    """
    Wrapper around TextBlob
    generates a TextBlob instance from report and
    returns the sentences
    """
    return [s.raw for s in TextBlob(report).sentences]
