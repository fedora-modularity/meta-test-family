from __future__ import print_function
import yaml
import os
import sys
import glob
from urllib import urlretrieve
from avocado.utils import process
from urlparse import urlparse
from warnings import warn


"""
Basic classes for metatadata handling, it contains classes derived from general metadata parser
for example for MTF testcases

for usage and deeper understand see  examples unittests in selftest.py file 
"""

MFILENAME = "metadata.yaml"
DESC = "description"
SOURCE = "source"
TESTE = "tests"
TESTC = "tests_coverage"
DOCUMENT = "document"
DOCUMENT_TYPES = ["metadata", "test-metadata", "tmet"]
SUBTYPE = "subtype"
SUBTYPE_G = "general"
SUBTYPE_T = "test"
BACKEND = "backend"
TAGS = "tags"
RELEVANCY = "relevancy"
DEPENDENCIES = "deps"
COVPATH = "coverage_path"
MODULELINT = "enable_lint"
IMPORT_TESTS = "import_tests"
TAG_FILETERS = "tag_filters"
URL_DOWNLOAD = "download_urls"
GIT_DOWNLOAD = "clone_gits"


def print_debug(*args):
    """
    Own implementation of print_debug, to not be dependent on MTF anyhow inside metadata
    """
    if os.environ.get("DEBUG"):
        for arg in args:
            print(arg, file=sys.stderr)


def logic_formula(statement, filters, op_negation="-", op_and=",", op_or=None):
    """
    disjunctive normla form statement parser https://en.wikipedia.org/wiki/Disjunctive_normal_form

    :param statement:
    :param filters:
    :param op_negation:
    :param op_and:
    :param op_or:
    :return:
    """
    def logic_simple(simple):
        key = simple
        value = True
        if key.startswith(op_negation):
            key = key[len(op_negation):]
            value = False
        return key, value

    def logic_and(normalform):
        dictset = {}
        for one in normalform.split(op_and):
            k, v = logic_simple(one)
            dictset[k] = v
        return dictset

    def logic_filter(actual_tag_list, tag_filter):
        # TODO: try to replace this part with http://www.sympy.org
        statement_or = False
        # if no tags in test then add this test to set (same behaviour as avocado --tag...empty)
        # print actual_tag_list, tag_filter
        if not actual_tag_list:
            statement_or = True
        actualinput = logic_and(actual_tag_list)
        for onefilter in tag_filter:
            filterinput = logic_and(onefilter)
            statement_and = True
            for key in filterinput:
                if filterinput.get(key) != bool(actualinput.get(key)):
                    statement_and = False
                    break
            if statement_and:
                statement_or = True
                break
        return statement_or

    if op_or:
        filters = filters.split(op_or)
    elif isinstance(filters,str):
        filters = [filters]
    return logic_filter(statement, filters)


class MetadataLoader(object):
    """
    General class for parsing test metadata from metadata.yaml files
    """
    base_element = {}
    backends = ["generic", "general"]
    # in filter there will be items like: {"relevancy": None, "tags": None}
    filter_list = [None]

    def __init__(self, location=".", linters=False, **kwargs):
        self.location = os.path.abspath(location)
        self._load_recursive()
        if URL_DOWNLOAD in self.base_element:
            self._url_download_files(self.base_element[URL_DOWNLOAD])
        if GIT_DOWNLOAD in self.base_element:
            self._git_clone_files(self.base_element[GIT_DOWNLOAD])
        # VERY IMPORTANT
        # Do it once more time, because coverage may changed after downloading urls and gits
        self._load_recursive()

        if IMPORT_TESTS in self.base_element:
            for testglob in self.base_element.get(IMPORT_TESTS):
                self._import_tests(os.path.join(self.location, testglob))
        if TAG_FILETERS in self.base_element:
            self.add_filter(tags=self.base_element.get(TAG_FILETERS))
        if linters or self.base_element.get(MODULELINT):
            self._import_linters()

    def _git_clone_files(self,gitdict):
        print_debug("Cloning resources via GIT (you have to have git installed)")
        for test in gitdict:
            if os.path.exists(test):
                print_debug("Directory %s already exist" % test)
            else:
                print_debug("Cloning git %s to directory %s" % (gitdict[test], test))
                process.run("git clone %s %s" % (gitdict[test], test))


    def _url_download_files(self,testdict):
        print_debug("Downloading resources via URL")
        for test in testdict:
            if os.path.exists(test):
                print_debug("File %s already exist locally" % test)
            else:
                print_debug("Storing %s as file %s" % (testdict[test], test))
                urlretrieve(testdict[test],filename=test)

    def _import_tests(self, testglob, pathlenght=0):
        """
        import tests based on file path glob like "*.py"

        :param testglob: string
        :param pathlenght: lenght of path for coverage usage (by default full path from glob is used)
        :return:
        """
        pathglob = testglob if testglob.startswith(os.pathsep) else os.path.join(self.location, testglob)
        print_debug("Import tests: %s" % pathglob)
        for testfile in glob.glob(pathglob):
            test = {SOURCE: testfile, DESC: "Imported tests by path: %s" % pathglob}
            self._insert_to_test_tree(testfile.strip(os.sep).split(os.sep)[pathlenght:],
                                      test)

    def _import_linters(self):
        """
        Import linters if any for backend type

        :return:
        """
        raise NotImplementedError

    def get_metadata(self):
        """
        get whole metadata loaded object
        :return: dict
        """
        return self.base_element

    def load_yaml(self, location):
        """
        internal method for loading data from yaml file

        :param location:
        :return:
        """
        print_debug("Loading metadata from file: %s" % location)
        with open(location, 'r') as ymlfile:
            xcfg = yaml.load(ymlfile.read())
        if xcfg.get(DOCUMENT) not in DOCUMENT_TYPES:
            raise BaseException("bad yaml file: item (%s)", xcfg.get(DOCUMENT))
        else:
            return xcfg

    def _insert_to_coverage(self, path_list, test):
        """
        translate test with path to coverage mapping TESTC

        :param path_list: how to store coverage
        :param test: dict object representing test
        :return:
        """
        coverage_key = "/".join(path_list)
        print_debug("insert to coverage %s to %s" % (test, coverage_key))
        # add test coverage key
        # add backend key if does not exist
        self.base_element[TESTC][coverage_key] = test
        self.base_element[TESTC][coverage_key][COVPATH] = coverage_key
        if BACKEND not in self.base_element[TESTC][coverage_key]:
            self.base_element[TESTC][coverage_key][BACKEND] = self.backends[0]

    def _parse_base_coverage(self, base=None, path=[]):
        """
        RECURSIVE internal method for parsing coverage in GENERAL metadata yaml tests: key in file

        :param base:
        :param path:
        :return:
        """
        base = base or self.base_element.get(TESTE, {})
        if DESC in base:
            if path:
                self._insert_to_coverage(path, base)
        elif isinstance(base, dict):
            for key, value in base.iteritems():
                self._parse_base_coverage(base=value, path=path + [key])
        else:
            print_debug("Try to parse element what is not parsable, check your structure: %s" % base)

    def _insert_to_test_tree(self, path_list, test):
        """
        Internal method to insert test to tests: dict object, used by simple metadata files

        :param path_list: where to store item (based on FS path)
        :param test: test object
        :return:
        """
        actualelem = self.base_element[TESTE]
        # sanitize testpath with test for these tests what are not fully qualified files
        # append directory locaiton to source
        if SOURCE in test \
                and not urlparse(test.get(SOURCE)).scheme \
                and not test.get(SOURCE).startswith(os.pathsep):
            test[SOURCE] = os.path.join(*(path_list + [test[SOURCE]]))
            print_debug("source testpath extended %s" % test[SOURCE])
        previous_item = None
        link_previous = None
        # Next code create full dictionary path to test if does not exist.
        # like ['a','b','c'] creates {'a':{'b':{'c':{}}}}
        for item in path_list:
            if actualelem.get(item) is None:
                actualelem[item] = dict()
            link_previous = actualelem
            previous_item = item
            actualelem = actualelem[item]
        link_previous[previous_item] = test
        self._insert_to_coverage(path_list, test)
        return self.base_element

    def _load_recursive(self):
        """
        Internal method to parse all metadata files
        It uses os.walk to find all files recursively

        :return:
        """
        allfiles = []
        location = self.location
        for root, sub_folders, files in os.walk(location):
            if MFILENAME in files:
                allfiles.append(os.path.join(root, MFILENAME))
        elem_element = {}
        if allfiles:
            elem_element = self.load_yaml(allfiles[0])
        if elem_element.get(SUBTYPE) == SUBTYPE_G:
            # this code cannont cause traceback because default value is {} or it loads yaml
            allfiles = allfiles[1:]
            self.base_element = elem_element
        else:
            self.base_element = {}
        if TESTC not in self.base_element:
            self.base_element[TESTC] = dict()
        if TESTE not in self.base_element:
            self.base_element[TESTE] = dict()
        self._parse_base_coverage()
        for item in allfiles:
            self._insert_to_test_tree(os.path.dirname(item)[len(location):].split("/")[1:],
                                      self.load_yaml(item))

    def get_coverage(self):
        """
        return coverage elemetn
        :return: dict
        """
        return self.base_element.get(TESTC)

    def get_backends(self):
        """
        List of all backends mentioned in metadata file
        :return: list
        """
        return set([x.get(BACKEND) for x in self.get_coverage().values()])

    def filter_relevancy(self, tests, envrion_description):
        """
        apply relevancy filtering, actually just a stub, returns everything
        Not implemented

        :param tests: list of tests
        :param envrion_description:  enviroment description
        :return:
        """
        return tests

    def filter_tags(self, tests, tag_list):
        """
        filter tags based on tags in metadata files for test

        :param tests:
        :param tag_list:
        :return:
        """
        output = []
        for test in tests:
            test_tags = test.get(TAGS, "")
            if logic_formula(test_tags, tag_list):
                output.append(test)
        return output

    def add_filter(self, tags=[], relevancy={}):
        """
        You can define multiple filters and apply them,
        :param tags:
        :param relevancy:
        :return:
        """
        addedfilter = {RELEVANCY: relevancy, TAGS: tags}
        if self.filter_list[-1] is None:
            self.filter_list = self.filter_list[:-1]
        self.filter_list.append(addedfilter)

    def apply_filters(self):
        output = self.backend_tests()
        for infilter in self.filter_list:
            if infilter:
                if infilter.get(TAGS):
                    output = self.filter_tags(output, infilter.get(TAGS))
                if infilter.get(RELEVANCY):
                    output = self.filter_relevancy(output, infilter.get(RELEVANCY))
        return output

    def backend_tests(self):
        cov = self.get_coverage()
        return [cov[x] for x in cov if cov[x].get(BACKEND) in self.backends and SOURCE in cov[x]]

    def backend_passtrought_args(self):
        return self.get_filters()

    def get_filters(self):
        return self.filter_list


class MetadataLoaderMTF(MetadataLoader):
    """
    metadata specific class for MTF (avocado) tests
    """
    try:
        import moduleframework.tests
        MTF_LINTER_PATH = os.path.dirname(moduleframework.tests.__file__)
    except:
        warn("MTF library not installed, linters are ignored")
        MTF_LINTER_PATH = None
    listcmd = "avocado list"
    backends = ["mtf", "avocado"]
    VALID_TEST_TYPES = ["EXTERNAL", "INSTRUMENTED", "SIMPLE", "PYUNITTEST"]

    def _import_tests(self, testglob, pathlenght=0):
        pathglob = testglob if testglob.startswith(os.pathsep) else os.path.join(self.location, testglob)
        print_debug("Import by pathglob: %s" % pathglob)
        tests_cmd = process.run("%s %s" % (self.listcmd, pathglob), shell=True, verbose=False, ignore_status=True)
        tests = tests_cmd.stdout.splitlines()
        if tests_cmd.exit_status != 0:
            raise BaseException("unbale to import tests (avocado list) via location: %s" % pathglob)
        for testurl in tests:
            if testurl and len(testurl) > 1:
                testlinesplitted = testurl.split(" ")
                testfile = " ".join(testlinesplitted[1:])
                testtype = testlinesplitted[0]
                print_debug("\t%s" % testfile)
                test = {SOURCE: testfile,
                        DESC: "Imported (%s) tests by path: %s" % (testtype, pathglob),
                        "avocado_test_type": testtype
                        }
                self._insert_to_test_tree(testfile.strip(os.sep).split(os.sep)[pathlenght:],
                                          test)

    def _import_linters(self):
        if self.MTF_LINTER_PATH:
            self._import_tests(os.path.join(self.MTF_LINTER_PATH, "generic", "*.py"), pathlenght=-3)
            self._import_tests(os.path.join(self.MTF_LINTER_PATH, "static", "*.py"), pathlenght=-3)

    def __avcado_tag_args(self, tag_list, defaultparam="--filter-by-tags-include-empty"):
        output = []
        for tag in tag_list:
            output.append("--filter-by-tags=%s" % tag)
        if output:
            output.append(defaultparam)
        return " ".join(output)

    def filter_tags(self, tests, tag_list):
        output = []
        test_sources = [x[SOURCE] for x in tests]
        cmd = process.run("%s %s %s" % (self.listcmd, self.__avcado_tag_args(tag_list), " ".join(test_sources)))
        testlist = []
        for line in cmd.stdout.splitlines():
            splittedline = line.split(" ", 1)
            if splittedline[0].strip() in self.VALID_TEST_TYPES:
                testlist.append(splittedline[1].strip())
            else:
                warn("NOT A TEST (may cause error when schedule): %s" % splittedline)
        for test in tests:
            if test[SOURCE] in testlist:
                output.append(test)
        return output


def get_backend_class(backend):
    if backend == "mtf":
        out = MetadataLoaderMTF
    else:
        out = MetadataLoader
    print_debug("Backend is: %s" % out)
    return out
