from common import MetadataLoader, MetadataLoaderMTF
from filter import filtertests
import yaml
import glob
import os

__TC_GENERAL_COMPONENT = "examples/general-component/tests"
__TC_MTF_COMPOMENT = "examples/mtf-component/tests"

def test_loader():
    mt = MetadataLoader(location=__TC_GENERAL_COMPONENT)
    print yaml.dump(mt.get_metadata())

def test_mtf_metadata_linters_only():
    mt = MetadataLoaderMTF(location=__TC_MTF_COMPOMENT, linters=True)
    #print yaml.dump(mt.get_metadata())
    #print mt.backend_passtrought_args()
    #print mt.apply_filters()
    case_justlinters_nofilter = len(mt.apply_filters())
    print case_justlinters_nofilter
    mt._import_tests(os.path.join(__TC_MTF_COMPOMENT,"*.py"))
    case_lintersanstests_nofilter = len(mt.apply_filters())
    print case_lintersanstests_nofilter
    mt.add_filter(tags=["add"])
    case_lintersanstests_filter1 = len(mt.apply_filters())
    print case_lintersanstests_filter1
    mt.add_filter(tags=["-add"])
    case_lintersanstests_filter2 = len(mt.apply_filters())
    print case_lintersanstests_filter2

    assert case_justlinters_nofilter > 20
    assert case_lintersanstests_nofilter > case_justlinters_nofilter
    assert case_lintersanstests_filter1 > case_justlinters_nofilter
    assert case_lintersanstests_filter1 < case_lintersanstests_nofilter
    assert case_lintersanstests_filter1 > case_lintersanstests_filter2
    assert case_lintersanstests_filter2 > case_justlinters_nofilter
    #print [v[SOURCE] for v in mt.backend_tests()]
    #mt.apply_filters()

def test_filter_mtf():
    out = len(filtertests(backend="mtf",
                           location=__TC_MTF_COMPOMENT,
                           linters=True,
                           tests=[],
                           tags=[],
                           relevancy=""))
    print out
    assert out > 20
    out = len(filtertests(backend="mtf",
                           location=__TC_MTF_COMPOMENT,
                           linters=False,
                           tests=[],
                           tags=[],
                           relevancy=""))
    print out
    assert out == 0
    out = len(filtertests(backend="mtf",
                           location=__TC_MTF_COMPOMENT,
                           linters=False,
                           tests=glob.glob(os.path.join(__TC_MTF_COMPOMENT,"*.py")),
                           tags=[],
                           relevancy=""))
    print out
    assert out == 11
    out = len(filtertests(backend="mtf",
                          location=__TC_MTF_COMPOMENT,
                          linters=False,
                          tests=glob.glob(os.path.join(__TC_MTF_COMPOMENT, "*.py")),
                          tags=["add"],
                          relevancy=""))
    print out
    assert out == 6
    out = len(filtertests(backend="mtf",
                          location=__TC_MTF_COMPOMENT,
                          linters=False,
                          tests=glob.glob(os.path.join(__TC_MTF_COMPOMENT, "*.py")),
                          tags=["-add"],
                          relevancy=""))
    print out
    assert out == 6
    out = len(filtertests(backend="mtf",
                          location=__TC_MTF_COMPOMENT,
                          linters=False,
                          tests=glob.glob(os.path.join(__TC_MTF_COMPOMENT, "*.py")),
                          tags=["rem"],
                          relevancy=""))
    print out
    assert out == 5

def test_filter_general():
    out = len(filtertests(backend=None,
                          location=__TC_GENERAL_COMPONENT,
                          linters=False,
                          tests=[],
                          tags=[],
                          relevancy=""))
    print out
    assert out == 4

#test_loader()

#test_mtf_metadata_linters_only()

#test_filter_mtf()

#test_filter_general()