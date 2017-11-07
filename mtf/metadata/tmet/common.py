import yaml
import os
import glob
from mtf.common import print_info, print_debug
from avocado.utils import process

MFILENAME = "metadata.yaml"
DESC = "description"
SOURCE = "source"
TESTE = "tests"
TESTC = "tests_coverage"
DOCUMENT = ["document", "metadata"]
SUBTYPE = "subtype"
SUBTYPE_G = "general"
SUBTYPE_T = "test"
BACKEND = "backend"
BACKEND_DEFAULT = "mtf"
TAGS = "tags"
RELEVANCY = "relevancy"
DEPENDENCIES = "deps"


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

    def tag_logic_filter(actual_tag_list, tag_filter):
        statement_or = False
        # if no tags in test then add this test to set (same behaviour as avocado --tag...empty)
        #print actual_tag_list, tag_filter
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
    return tag_logic_filter(statement, filters)

class MetadataLoader(object):
    base_element = {}
    parent_backend = BACKEND_DEFAULT
    # in filter there will be items like: {"relevancy": None, "tags": None}
    filter_list = [None]
    def __init__(self, location=".", linters=False, backend=BACKEND_DEFAULT, **kwargs):
        self.location = location
        self.backend = backend
        self._load_recursive()
        self.parent_backend = self.base_element.get(BACKEND) or BACKEND_DEFAULT
        if linters:
            self._import_linters()

    def _import_tests(self,testglob, pathlenght=0):
        print_debug("Importing tests: %s" % testglob)
        for testfile in glob.glob(testglob):
            test = {SOURCE: testfile, DESC: "Imported tests by path: %s" % testglob}
            self._insert_to_test_tree(testfile.strip(os.sep).split(os.sep)[pathlenght:],
                                       test)

    def _import_linters(self):
        raise NotImplementedError

    def get_metadata(self):
        return self.base_element

    def load_yaml(self, location):
        print_debug("Loading metadata from file: %s" % location)
        with open(location, 'r') as ymlfile:
            xcfg = yaml.load(ymlfile.read())
        if xcfg.get(DOCUMENT[0]) not in DOCUMENT[1]:
            raise BaseException("bad yaml file: item (%s)", xcfg.get(DOCUMENT[0]))
        else:
            return xcfg

    def _insert_to_coverage(self, path_list, test):
        if not self.base_element.get(TESTC):
            self.base_element[TESTC] = dict()
        coverage_key = "/".join(path_list)
        # add test coverage key
        # add backend key if does not exist
        self.base_element[TESTC][coverage_key] = test
        if not self.base_element[TESTC][coverage_key].get(BACKEND):
            self.base_element[TESTC][coverage_key][BACKEND] = self.parent_backend

    def _parse_base_coverage(self,base=None, path=[]):
        base = base or self.base_element.get(TESTE,{})
        if base.get(DESC):
            if path:
                self._insert_to_coverage(path,base)
        else:
            for key, value in base.iteritems():
                self._parse_base_coverage(base=value, path=path+[key])

    def _insert_to_test_tree(self, path_list, test):
        actualelem = self.base_element
        if not actualelem.get(TESTE):
            actualelem[TESTE] = dict()
        actualelem = actualelem[TESTE]
        previous_item = None
        link_previous = None
        for item in path_list:
            if actualelem.get(item) == None:
                actualelem[item] = dict()
            link_previous = actualelem
            previous_item = item
            actualelem = actualelem[item]
        link_previous[previous_item] = test
        self._insert_to_coverage(path_list, test)
        return self.base_element

    def _load_recursive(self):
        allfiles = []
        location = self.location
        for root, sub_folders, files in os.walk(location):
            if MFILENAME in files:
                allfiles.append(os.path.join(root,MFILENAME))
        elem_element = {}
        if allfiles:
            elem_element = self.load_yaml(allfiles[0])
        if elem_element.get(SUBTYPE) == SUBTYPE_G:
            allfiles=allfiles[1:]
            self.base_element = elem_element
        else:
            self.base_element = {}

        self._parse_base_coverage()
        for item in allfiles:
            self._insert_to_test_tree(os.path.dirname(item)[len(location):].split("/")[1:],
                                       self.load_yaml(item))

    def get_coverage(self):
        return self.base_element.get(TESTC)

    def get_backends(self):
        return set([x.get(BACKEND) for x in self.get_coverage()])

    def filter_relevancy(self, tests, envrion_description):
        return tests

    def filter_tags(self, tests, tag_list):
        output = []
        for test in tests:
            test_tags = test.get(TAGS, "")
            if logic_formula(test_tags, tag_list):
                output.append(test)
        return output

    def add_filter(self, tags=[], relevancy={}):
        addedfilter = {RELEVANCY:relevancy, TAGS:tags}
        if self.filter_list[-1] == None:
            self.filter_list = self.filter_list[:-1]
        self.filter_list.append(addedfilter)

    def apply_filters(self):
        output = self.backend_tests()
        for infilter in self.filter_list:
            if infilter:
                output = self.filter_tags(output, infilter.get(TAGS))
                output = self.filter_relevancy(output, infilter.get(RELEVANCY))
        return output

    def backend_tests(self):
        cov = self.get_coverage()
        return [cov[x] for x in cov if cov[x].get(BACKEND)==self.backend and cov[x].get(SOURCE)]

    def backend_passtrought_args(self):
        return self.get_filters()

    def get_filters(self):
        return self.filter_list

class MetadataLoaderMTF(MetadataLoader):
    import moduleframework.tools
    MTF_LINTER_PATH = os.path.dirname(moduleframework.tools.__file__)

    def _import_tests(self,testglob, pathlenght=0):
        print_debug("Importing tests: %s" % testglob)
        tests = process.run("avocado list %s" % testglob, shell=True).stdout.splitlines()
        for testurl in tests:
            if testurl and len(testurl)>1:
                testlinesplitted = testurl.split(" ")
                testfile = " ".join(testlinesplitted[1:])
                testtype = testlinesplitted[0]
                test = {SOURCE: testfile,
                        DESC: "Imported (%s) tests by path: %s" % (testtype, testglob),
                        "avocado_test_type": testtype
                        }
                self._insert_to_test_tree(testfile.strip(os.sep).split(os.sep)[pathlenght:],
                                       test)

    def __init__(self, *args, **kwargs):
        super(MetadataLoaderMTF, self).__init__(*args, **kwargs)

    def _import_linters(self):
        self._import_tests(os.path.join(self.MTF_LINTER_PATH,"*.py"), pathlenght=-3)

    def filter_tags(self, tests={}, tag_list=[]):
        justtests = tests.values()
        "avocado"

def test_loader():
    mt = MetadataLoader(location="examples/general-component/tests")
    print yaml.dump(mt.get_metadata())

def test_mtf_metadata_linters_only():
    mt = MetadataLoaderMTF(location="examples/mtf-component/tests", linters=True)
    #print yaml.dump(mt.get_metadata())
    print mt.backend_passtrought_args()
    mt.add_filter(tags=["add"])
    print mt.backend_passtrought_args()
    print [v[SOURCE] for v in mt.backend_tests()]
    #mt.apply_filters()

#test_loader()

test_mtf_metadata_linters_only()