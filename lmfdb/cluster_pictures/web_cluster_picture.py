# -*- coding: utf-8 -*-
from collections import Counter
import os, yaml

from sage.all import (
    Set, ZZ, euler_phi, CyclotomicField, gap, RealField,
    QQ, NumberField, PolynomialRing, latex, pari, cached_function, Permutation)

from flask import url_for

from lmfdb import db
from lmfdb.utils import (web_latex, coeff_to_poly, pol_to_html,
        display_multiset, factor_base_factor, factor_base_factorization_latex)
from lmfdb.logger import make_logger
wcplog = make_logger("WCP")

@cached_function
def cp_display_knowl(label, name=None, img=None):
    if not name:
        name = "Cluster Picture %s" % label
    if not img:
        img = name
    return '<a title = "%s [clusterpicture.data]" knowl="clusterpicture.data" kwargs="label=%s">%s</a>' % (name, label, img)

def cp_knowl_guts(label):
    out = ''
    wcp = WebClusterPicture(label)
    if wcp.is_null():
        return 'Cannot find cluster picture %s' % label
    out += "<b>Cluster picture %s</b>" % label
    out += '<div>'
    out += '<img src="'
    out += wcp.image()
    out += '" alt="cluster_picture_image"/>'
    out += '<br>Depth: '
    out += str(wcp.depth())
    out += '<br>Size: '
    out += str(wcp.size())
    out += '<br>Potential toric rank: '
    out += str(wcp.potential_toric_rank())
    out += '<br>Potential good reduction curve: '
    out += str(wcp.potential_good_reduction())
    out += '<br>Potential good reduction Jacobian: '
    out += str(wcp.potential_good_jacobian_reduction())
    out += '</div>'
    #out += '<div align="right">'
    #out += '<a href="%s">%s home page</a>' % (str(url_for("number_fields.by_label", label=label)),label)
    #out += '</div>'
    return out

class WebClusterPicture:
    """
     Class for retrieving cluster picture information from the database
    """
    def __init__(self, label, data=None):
        self.label = label
        if data is None:
            self._data = self._get_dbdata()
        else:
            self._data = data

    def _get_dbdata(self):
        return db.cluster_pictures.lookup(self.label)
    
    def is_null(self):
        return self._data is None
    
    def get_label(self):
        return self._data['label']
        
    def image(self):
        return self._data['image']
        
    def thumbnail(self):
        return self._data['thumbnail']
        
    def depth(self):
        return self._data['depth']
        
    def size(self):
        return self._data['size']
        
    def potential_toric_rank(self):
        return self._data['potential_toric_rank']
        
    def potential_good_reduction(self):
        return self._data['potential_good_reduction']
        
    def potential_good_jacobian_reduction(self):
        return self._data['potential_good_jacobian_reduction']
        
    def knowl(self):
        return cp_display_knowl(self.get_label())
