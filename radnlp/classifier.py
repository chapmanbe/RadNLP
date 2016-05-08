def modify_categories(document, category_rules):
    for cr in category_rules:
        anatomyRecategorize(g,t,cr)

def classifyDocumentTargets(doc,
                            classification_rules,
                            neg_filter = ["definite_negated_existence",
                                         "probable_negated_existence"],
                            exclusion_categories = ["QUALITY_FEATURE",
                                                    "ARTIFACT"]
                            ):
    """
    Look at the targets and their modifiers to get an overall classification for the document_markup
    """
    rslts = {}

    qualityInducedUncertainty = False
    document_markup = doc.getXML()
    g = doc.getDocumentGraph()
    targets = [n[0] for n in g.nodes(data = True) if n[1].get("category","") == 'target']

    if targets:
        for t in targets:
            severityValues = []
            current_rslts = {}
            currentCategory = t.getCategory()
            if not t.isA(exclusion_categories):
                # iterate across all the classification_rules
                current_rslts = {rk:genericClassifier(g,t,class_rules[rk]) for rk in classification_rules}
                for rk in self.class_rules:
                    current_rslts[rk] = genericClassifier(g,t,self.class_rules[rk])
                for cr in self.category_rules:
                    anatomyRecategorize(g,t,cr)
                for sv in self.severity_rules:
                    severity = getSeverity(g,t,sv)
                    severityValues.extend(severity)
                currentCategory = t.categoryString()
                # now need to compare current_rslts to rslts to select most Positive
                docr = self.classifyResult(current_rslts)
                trslts = rslts.get(currentCategory,[-1,'',[]])
                if trslts[0] < docr:
                    trslts = [docr,t.getXML(),severityValues]
                rslts[currentCategory] = trslts
            else:
                if t.isA('QUALITY_FEATURE'):
                    qualityInducedUncertainty = True
                else:
                    if not modifies(g,t,neg_filters):# non-negated artifacts
                        qualityInducedUncertainty = True

    return rslts,document_markup
