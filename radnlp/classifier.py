"""
This module implements a generic document classification based on
pyConTextNLP markup
"""

from . import utils
from . import schema


"""
def modify_categories(document, category_rules):
    for cr in category_rules:
        utils.anatomy_recategorize(g,t,cr)
"""


def classify_result(doc_rslts, _schema):
        """
        given results in doc_rslts compare to classification_schema and
        return score.
        Takes a three-tuple of boolean values for
            * Disease State Positive
            * Disease State Certain
            * Disease State Acute
        """
        return schema.assign_schema(doc_rslts, _schema)


def classify_document_targets(doc,
                              classification_rules,
                              category_rules,
                              severity_rules,
                              _schema,
                              neg_filters=["definite_negated_existence",
                                           "probable_negated_existence"],
                              exclusion_categories=["QUALITY_FEATURE",
                                                    "ARTIFACT"]):
    """
    Look at the targets and their modifiers to get an overall
    classification for the document_markup
    """
    rslts = {}

    qualityInducedUncertainty = False
    g = doc.getDocumentGraph()
    targets = [n[0] for n in g.nodes(data=True)
               if n[1].get("category", "") == 'target']

    if targets:
        for t in targets:
            severity_values = []
            current_rslts = {}
            current_category = t.getCategory()
            if not t.isA(exclusion_categories):
                # iterate across all the classification_rules
                current_rslts = \
                    {rk:utils.generic_classifier(g,
                                                 t,
                                                 classification_rules[rk])
                     for rk in classification_rules}

                for cr in category_rules:
                    utils.anatomy_recategorize(g, t, cr)
                for sv in severity_rules:
                    severity = utils.get_severity(g, t, sv)
                    severity_values.extend(severity)
                current_category = t.categoryString()
                # now need to compare current_rslts to rslts
                # to select most Positive
                docr = classify_result(current_rslts, _schema)
                trslts = rslts.get(current_category, [-1, '', []])
                if trslts[0] < docr:
                    trslts = [docr, t.getXML(), severity_values]
                rslts[current_category] = trslts
            else:
                if t.isA('QUALITY_FEATURE'):
                    qualityInducedUncertainty = True
                else:
                    # if non-negated artifacts call uncertain
                    if not utils.modifies(g, t, neg_filters):
                        qualityInducedUncertainty = True
    return rslts
