try:
    import urllib2.urlopen as urlopen
except:
    import urllib.request.urlopen as urlopen

try:
    import urllib2.urlparse as urlparse
except:
    import urllib.parse as urlparse


def instantiateSchema(values,rule):
    """evaluates rule by substituting values into rule and evaluating the resulting literal.
    For security the ast.literal_eval() method is used.
    """
    r = rule
    for k in values.keys():
        r = r.replace(k,values[k].__str__())
    #return ast.literal_eval(r)
    return eval(r)

def assignSchema(values,rules):
    for k in rules.keys():
        if( instantiateSchema(values,rules[k][1]) ):
            return k
def readSchema(fname):
    """read the schema and schema classifier functionality"""

    p = urlparse.urlparse(fname)

    if not p.scheme:
        fname = "file://"+fname

    f0 = urlopen(fname)

    schema = {}
    tmp = f0.readlines()
    for t in tmp:
        t = t.strip().split(",")
        if( t[0][0] != "#" ):
            schema[int(t[0])]=(t[1],t[2])
    return schema
