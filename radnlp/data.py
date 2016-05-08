"""
define data structures to use in radnlp
"""
from collections import namedtuple

classrslts = namedtuple("classrslts",
                        ["context_document",
                         "exam_type",
                         "report_text",
                         "classification_result"])
def get_classification_result_brief(crslt):
    """
    crslt: an instance of classrslts

    returns a string with each category/classification pair
    """
    return {cat: cla[0] for cat,cla in
                      crslt.classification_result.items()}
