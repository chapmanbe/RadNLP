"""
define data structures to use in radnlp
"""
from collections import namedtuple

classrslts = namedtuple("classrslts",
                        ["context_document",
                         "exam_type",
                         "report_text",
                         "classification_result"])
def get_brief_classification(crslt):
    """
    crslt: dictionary of classification results
    """
    return {cat: cla[0] for cat, cla in crslt.items()}

def filter_classification_rslts(crslt, select = (7,8)):
    """
    crslt: dictionary of classifications
    select: numeric classification values to keep
    """
    return {cat: cla for cat, cla in crslt.items() if cla[0] in select}

    
def get_classification_result_brief(crslt):
    """
    crslt: an instance of classrslts

    returns a string with each category/classification pair
    """
    return {cat: cla[0] for cat,cla in
                      crslt.classification_result.items()}
