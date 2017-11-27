from common import MetadataLoader, MetadataLoaderMTF, SOURCE, print_debug
from filter import filtertests
import yaml

__TC_GENERAL_COMPONENT = "examples/general-component/tests"
__TC_MTF_COMPOMENT = "examples/mtf-clean/tests"
__TC_MTF_CONF = "examples/mtf-component/tests"
__TC_GENERAL_CONF = "examples/general-simple"


def test_loader():
    """
    Test general backend loader for complex case
    :return:
    """
    mt = MetadataLoader(location=__TC_GENERAL_COMPONENT)
    print_debug(yaml.dump(mt.get_metadata()))
    print_debug(mt.get_backends())
    assert 'sanity/generaltest.py' in [x[SOURCE] for x in mt.backend_tests()]


def test_mtf_metadata_linters_and_tests_noconfig():
    """
    Test linter only for MTF loader, using no config
    :return:
    """
    mt = MetadataLoaderMTF(location=__TC_MTF_COMPOMENT, linters=True)
    # print yaml.dump(mt.get_metadata())
    # print mt.backend_passtrought_args()
    # print mt.apply_filters()
    case_justlinters_nofilter = len(mt.apply_filters())
    print_debug(case_justlinters_nofilter)
    mt._import_tests("*.py")
    case_lintersanstests_nofilter = len(mt.apply_filters())
    print_debug(case_lintersanstests_nofilter)
    mt.add_filter(tags=["add"])
    case_lintersanstests_filter1 = len(mt.apply_filters())
    print_debug(case_lintersanstests_filter1)
    mt.add_filter(tags=["-add"])
    case_lintersanstests_filter2 = len(mt.apply_filters())
    print_debug(case_lintersanstests_filter2)

    assert case_justlinters_nofilter > 20
    assert case_lintersanstests_nofilter > case_justlinters_nofilter
    assert case_lintersanstests_filter1 > case_justlinters_nofilter
    assert case_lintersanstests_filter1 < case_lintersanstests_nofilter
    assert case_lintersanstests_filter1 > case_lintersanstests_filter2
    assert case_lintersanstests_filter2 < case_justlinters_nofilter
    # print [v[SOURCE] for v in mt.backend_tests()]
    # mt.apply_filters()


def test_filter_mtf_justlintes():
    """
    test load just linter with simple config
    :return:
    """
    out = filtertests(backend="mtf",
                          location=__TC_MTF_COMPOMENT,
                          linters=True,
                          tests=[],
                          tags=[],
                          relevancy="")
    print_debug(out)
    assert len(out) > 20


def test_filter_mtf_nothing():
    """
    use config what loads no tests
    :return:
    """
    out = filtertests(backend="mtf",
                          location=__TC_MTF_COMPOMENT,
                          linters=False,
                          tests=[],
                          tags=[],
                          relevancy="")
    print_debug(out)
    assert len(out) == 0


def test_filter_mtf_justtests():
    """
    tests load configu and just tests there
    """
    out = filtertests(backend="mtf",
                          location=__TC_MTF_COMPOMENT,
                          linters=False,
                          tests=["*.py"],
                          tags=[],
                          relevancy="")
    print_debug(out)
    assert len(out) == 11


def test_filter_mtf_filtered_tests_add():
    """
    tests load config with filters
    :return:
    """
    out = filtertests(backend="mtf",
                          location=__TC_MTF_COMPOMENT,
                          linters=False,
                          tests=["*.py"],
                          tags=["add"],
                          relevancy="")
    print_debug(out)
    assert len(out) == 6


def test_filter_mtf_filtered_notadd():
    """
    tests load config with filters
    :return:
    """
    out = filtertests(backend="mtf",
                          location=__TC_MTF_COMPOMENT,
                          linters=False,
                          tests=["*.py"],
                          tags=["-add"],
                          relevancy="")
    print_debug(out)
    assert len(out) == 6


def test_filter_mtf_filtered_rem():
    """
    tests load config with filters

    :return:
    """
    out = filtertests(backend="mtf",
                          location=__TC_MTF_COMPOMENT,
                          linters=False,
                          tests=["*.py"],
                          tags=["rem"],
                          relevancy="")
    print_debug(out)
    assert len(out) == 5


def test_filter_general():
    """
    tests load config with filters, for general module
    :return:
    """
    out = filtertests(backend=None,
                          location=__TC_GENERAL_COMPONENT,
                          linters=False,
                          tests=[],
                          tags=[],
                          relevancy="")
    print_debug(out)
    assert len(out) == 5


def test_mtf_config():
    """
    test real life example and check if proper tests were filtered based on config file
    :return:
    """
    out = filtertests(backend="mtf",
                       location=__TC_MTF_CONF,
                       linters=False,
                       tests=[],
                       tags=[],
                       relevancy="")
    tests = [x[SOURCE] for x in out]
    print_debug(tests)
    assert len(tests) == 6
    assert "Rem" not in " ".join(tests)
    assert "Add" in " ".join(tests)
    assert "DockerFileLint" in " ".join(tests)


def test_general_config():
    """
    test loading general config and check number of tests, linters disabled
    :return:
    """
    out = (filtertests(backend=None,
                       location=__TC_GENERAL_CONF,
                       linters=False,
                       tests=[],
                       tags=[],
                       relevancy=""))
    print_debug(out)
    assert len(out) == 2


# test_loader()
# test_mtf_metadata_linters_only()
# test_filter_mtf()
# test_filter_general()
# test_mtf_config()
# test_general_config()
