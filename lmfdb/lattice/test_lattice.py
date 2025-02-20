# -*- coding: utf-8 -*-

from lmfdb.tests import LmfdbTest

class HomePageTest(LmfdbTest):
    # The Lattice page
    def test_lattice(self):
        homepage = self.tc.get("/Lattice/").get_data(as_text=True)
        assert 'random' in homepage
        assert 'Gram' in homepage

    def test_lattice_dim(self):
        L = self.tc.get("/Lattice/9.8.16.1.1").get_data(as_text=True)
        assert '115712' in L #coeff in theta series
        assert '1.58740105196819947475170563927' in L #Hermite number
        assert '11612160' in L #group order

    def test_lattice_classnumber(self):
        L = self.tc.get("/Lattice/?class_number=1").get_data(as_text=True)
        assert '2.13.26.1.2' in L #label (class number 1)

    def test_lattice_classnumber_large(self):
        L = self.tc.get("/Lattice/3.1942.3884.56.13").get_data(as_text=True)
        assert '648' in L #test display genus representatives

    def test_lattice_classnumber_large_download(self):
        L = self.tc.get("/Lattice/3.1942.3884.56.13/download/sage/genus_reps").get_data(as_text=True)
        assert 'Matrix([[2, 0, 0], [0, 14, -3], [0, -3, 70]]),' in L #test download genus representatives

    def test_lattice_search(self):
        L = self.tc.get("/Lattice/?dim=&det=&level=&gram=&minimum=&class_number=1&aut=&count=50").get_data(as_text=True)
        assert '56' in L #search

    def test_lattice_search_next(self):
        L = self.tc.get("/Lattice/?start=50&dim=&det=&level=&gram=&minimum=&class_number=&aut=2&count=50").get_data(as_text=True)
        assert '145' in L #search on the next page

    def test_lattice_searchdim(self):
        L = self.tc.get("/Lattice/?dim=3").get_data(as_text=True)
        assert '3.1.2.1.1' in L #dimension search

    def test_lattice_searchlevel(self):
        L = self.tc.get("/Lattice/?start=&dim=&det=&level=90&gram=&minimum=&class_number=&aut=").get_data(as_text=True)
        assert '16' in L #level search

    def test_lattice_searchminvectlength(self):
        L = self.tc.get("/Lattice/?dim=&det=&level=&gram=&minimum=3&class_number=&aut=").get_data(as_text=True)
        assert '2.42.84.1.3' in L #search minimum vector length

    def test_lattice_searchGM(self):
        L = self.tc.get("/Lattice/?dim=&det=&level=&gram=[17%2C6%2C138]&minimum=&class_number=&aut=").get_data(as_text=True)
        assert '4620' in L #gram matrix search

    def test_lattice_searchGM_2(self):
        L = self.tc.get("/Lattice/?dim=&det=&level=&gram=5%2C3%2C2&minimum=&class_number=&aut=").get_data(as_text=True)
        assert '2.1.2.1.1' in L #gram matrix search through isometries

    def test_latticeZ2(self):
        L = self.tc.get("/Lattice/2.1.2.1.1").get_data(as_text=True)
        assert r'0.785398163397448309615660845820\dots' in L #Z2 lattice

    def test_lattice_thetadisplay(self):
        L = self.tc.get("/Lattice/theta_display/7.576.18.1.1/40").get_data(as_text=True)
        assert '41' in L # theta display
        assert '1848' in L # theta display
        assert '11466' in L # theta display

    def test_lattice_random(self):
        L = self.tc.get("/Lattice/random").get_data(as_text=True)
        assert 'redirected automatically' in L # random lattice
        L = self.tc.get("/Lattice/random", follow_redirects=True)
        assert 'Normalized minimal vectors' in L.get_data(as_text=True) # check redirection

    def test_downloadstring(self):
        L = self.tc.get("/Lattice/5.648.12.1.1").get_data(as_text=True)
        assert 'matrix' in L

    def test_downloadstring2(self):
        L = self.tc.get("/Lattice/2.156.312.1.2").get_data(as_text=True)
        assert 'vector' in L
        assert 'Underlying data' in L and 'data/2.156.312.1.2' in L

    def test_downloadstring_search(self):
        L = self.tc.get("/Lattice/?class_number=8").get_data(as_text=True)
        assert 'Download to' in L

    def test_download_shortest(self):
        L = self.tc.get("/Lattice/13.14.28.8.1/download/magma/shortest_vectors").get_data(as_text=True)
        assert 'data := ' in L

    def test_download_genus(self):
        L = self.tc.get("/Lattice/4.5.5.1.1/download/gp/genus_reps").get_data(as_text=True)
        assert ']~)' in L

    def test_favorite(self):
        for elt in ['A2', 'Z2', 'D3', 'D3*', '3.1942.3884.56.1', 'A5',
                    'E8', 'A14', 'Leech']:
            L = self.tc.get(
                    "/Lattice/?label={}".format(elt),
                    follow_redirects=True)
            assert elt in L.get_data(as_text=True)
            L = self.tc.get(
                    "/Lattice/{}".format(elt),
                    follow_redirects=True)
            assert elt in L.get_data(as_text=True)
