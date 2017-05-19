import numpy as np
import fcg

def create_color(seed):
    rng = np.random.RandomState(seed=seed)
    return '#%02x%02x%02x' % (rng.uniform(64,255), rng.uniform(64,255), rng.uniform(64,255))

def as_span(s):
    return '<span style="background-color: %s;">%s</span>' % (create_color(id(s)), s._id)
def as_div(s):
    return '<div style="background-color: %s;">%s</div>' % (create_color(id(s)), s._id)

def html_structures(w):
    html = []

    style = """
.fcg tr, .fcg td, .fcg th {border: 0px solid black;}
table.fcg {display: inline-block;}

    """

    html.append('<style>%s</style>' % style)

    for s in sorted(w.structures, key=lambda x: x._id):
        items = []
        items.append('<tr><th colspan="2"><center>%s</center></th></tr>' % s._id)
        for k, v in s.extract():
            if isinstance(v, fcg.Structure):
                v = as_div(v)
            if isinstance(v, list):
                v = list(v)
                for i, vv in enumerate(v):
                    if isinstance(vv, fcg.Structure):
                        v[i] = as_span(vv)
                v = '[%s]' % ','.join(v)

            items.append('<tr><th>%s</th><td>%s</td></tr>' % (k, v))
        c = create_color(id(s))
        html.append('<table class="fcg" style="background-color: %s;">%s</table>' % (c, ''.join(items)))
    return ''.join(html)
