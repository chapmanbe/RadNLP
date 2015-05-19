import pyConTextNLP.pyConTextGraph as pyConText

def modifies(g,n,modifiers):
    """Tests whether any of the modifiers of node n are in any of the categories listed in 'modifiers'"""
    pred = g.predecessors(n)
    if not pred:
        return False
    pcats = []
    for p in pred:
        pcats.extend(p.getCategory())
    return bool(set(pcats).intersection([m.lower() for m in modifiers]))
def matchedModifiers(g,n,modifiers):
    """returns the set of predecessors of node 'n' that are of a category contained in 'modifiers'"""
    pred = g.predecessors(n)
    if not pred:
        return False
    pcats = []
    for p in pred:
        pcats.extend(p.getCategory())

    return set(pcats).intersection([m.lower() for m in modifiers])

def returnMatchedModifiers(g,n,modifiers):
    pred = g.predecessors(n)
    if not pred:
        return []
    mods = [m.lower() for m in modifiers]
    mmods = [p for p in pred if p.isA(mods)]
    return mmods
def markup_sentence(s, modifiers, targets):
    markup = pyConText.ConTextMarkup()
    markup.setRawText(s)
    markup.cleanText()
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")

    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    # apply modifiers to any targets within the modifiers scope
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    markup.dropInactiveModifiers()
    return markup_sentence

def genericClassifier(g,t,rule):
    """based on the modifiers of the target 't' and the provide rule in 'rule' classify the target node"""
    mods = g.predecessors(t)
    if not mods:
        return rule["DEFAULT"]
    for r in rule["RULES"]:
        if( modifies(g,t,r[1]) ):
            return r[0]
    return rule["DEFAULT"]

