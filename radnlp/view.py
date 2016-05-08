"""
Functions and variables for viewing marked up reports
"""
from pyConTextNLP.display.html import mark_document_with_html
from . data import get_classification_result_brief as gcrb
import networkx as nx

clrs = {\
"finding": "blue",
"definite_negated_existence": "red",
"probable_negated_existence": "indianred",
"ambivalent_existence": "orange",
"probable_existence": "forestgreen",
"definite_existence": "green",
"historical": "goldenrod",
"acute": "golden"
}

codingKey = {\
1: "AMBIVALENT",
2: "Negative/Certain/Acute",
3: "Negative/Uncertain/Chronic",
4: "Positive/Uncertain/Chronic",
5: "Positive/Certain/Chronic",
6: "Negative/Uncertain/Acute",
7: "Positive/Uncertain/Acute",
8: "Positive/Certain/Acute"
}

def markup_to_html(markup_rslt, color_map=None):
    """

    """
    if not color_map:
        color_map = clrs

    mt = mark_document_with_html(markup_rslt.context_document,
                                 colors=color_map)
    class_rslts = gcrb(markup_rslt)
    class_str = "; ".join(["%s (%s)"%(k,codingKey.get(v,"NA")) for
                           k, v in class_rslts.items()])
    txt = """
          <table style="width:100">
          <caption>PE Finder Case Review</caption>
          <tr><th>report</th><th>classification</th></tr>
          <tr><td width='500'>%s</td><td width='200'>%s</td></tr>
          </table>""" % (mt,class_str)
    return txt

def get_node_brief(n,id_digits=3):
    return """%s %s(%s)"""%(n.getPhrase(),
                             n.getCategory(),
                             ("%d"%n.getTagID())[-id_digits:])

def documentgraph_to_viewgraph(dg):
    newg = nx.DiGraph()
    edges = dg.edges()
    for e in edges:
        newg.add_edge(get_node_brief(e[0]),
                      get_node_brief(e[1]))
    return newg
def get_pydot_graph(markup_rslt):

    return nx.nx_pydot.to_pydot(
        documentgraph_to_viewgraph(
            markup_rslt.context_document.getDocumentGraph())
        )


def markup_to_pydot(markup_rslt,fname="./tmp.png"):
    ag = get_pydot_graph(markup_rslt)
    ag.write_png(fname)
    return fname
