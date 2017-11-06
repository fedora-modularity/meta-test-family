import yaml
import os
import glob

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

def logic_formula(actual_tags, filter_list):
    def tag_logic_simple(simple):
        key = simple
        value = True
        if key.startswith("-"):
            key = key[1:]
            value = False
        return key, value

    def tag_logic_formula(normalform):
        dictset = {}
        for one in normalform.split(","):
            k, v = tag_logic_simple(one)
            dictset[k] = v
        return dictset

    def tag_logic_filter(actual_tag_list, tag_filter):
        statement_or = False
        # if no tags in test then add this test to set (same behaviour as avocado --tag...empty)
        print actual_tag_list, tag_filter
        if not actual_tag_list:
            statement_or = True
        actualinput = tag_logic_formula(actual_tag_list)
        for onefilter in tag_filter:
            filterinput = tag_logic_formula(onefilter)
            statement_and = True
            for key in filterinput:
                if filterinput.get(key) != bool(actualinput.get(key)):
                    statement_and = False
                    break
            if statement_and:
                statement_or = True
                break
        return statement_or
    return tag_logic_filter(actual_tags, filter_list)

class MetadataLoader(object):
    base_element = {}
    parent_backend = BACKEND_DEFAULT
    # in filter there will be items like: {"relevancy": None, "tags": None}
    filter_list = [None]
    def __init__(self, localtion=".", linters=False, backend=BACKEND_DEFAULT):
        self.location = localtion
        self.backend = backend
        self.__load_recursive()
        self.parent_backend = self.base_element.get(BACKEND) or BACKEND_DEFAULT
        if linters:
            self._import_linters()

    def _import_tests(self,testglob, pathlenght=0):
        for testfile in glob.glob(testglob):
            self.__insert_to_test_tree(os.path.dirname(testglob.strip(os.sep).split(os.sep))[pathlenght:],
                                       testfile)

    def _import_linters(self):
        raise NotImplementedError

    def get_metadata(self):
        return self.base_element

    def load_yaml(self, location):
        with open(location, 'r') as ymlfile:
            xcfg = yaml.load(ymlfile.read())
        if xcfg.get(DOCUMENT[0]) not in DOCUMENT[1]:
            raise BaseException("bad yaml file: item (%s)", xcfg.get(DOCUMENT[0]))
        else:
            return xcfg

    def __insert_to_coverage(self, path_list, test):
        if not self.base_element.get(TESTC):
            self.base_element[TESTC] = dict()
        coverage_key = "/".join(path_list)
        # add test coverage key
        # add backend key if does not exist
        if not self.base_element[TESTC].get(BACKEND):
            self.base_element[TESTC][BACKEND] = self.parent_backend

    def __parse_base_coverage(self,base=None, path=[]):
        base = base or self.base_element.get(TESTE,{})
        if base.get(DESC):
            if path:
                self.__insert_to_coverage(path,base)
        else:
            for key, value in base.iteritems():
                self.__parse_base_coverage(base=value, path=path+[key])

    def __insert_to_test_tree(self, path_list, test):
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
        link_previous[previous_item] = test
        self.__insert_to_coverage(path_list, test)
        return self.base_element

    def __load_recursive(self):
        allfiles = []
        location = self.location
        for root, sub_folders, files in os.walk(location):
            if MFILENAME in files:
                allfiles.append(os.path.join(root,MFILENAME))
        base_element = self.load_yaml(allfiles[0])
        if base_element.get(SUBTYPE) == SUBTYPE_G:
            allfiles=allfiles[1:]
        else:
            base_element={}
        self.base_element = base_element
        self.__parse_base_coverage()
        for item in allfiles:
            self.__insert_to_test_tree(os.path.dirname(item)[len(location):].split("/")[1:],
                                       self.load_yaml(item))

    def get_coverage(self):
        return self.base_element.get(TESTC)

    def get_backends(self):
        return set([x.get(BACKEND) for x in self.get_coverage()])

    def filter_relevancy(self, tests, envrion_description):
        pass

    def filter_tags(self, tests, tag_list):
        output = []
        for test in tests:
            test_tags = test.get("tags", "")
            if logic_formula(test_tags, tag_list):
                output.append(test)
        return output

    def add_filter(self, relevancy={}, tags=[]):
        addedfilter = {'relevancy':relevancy, 'tags':tags}
        if self.filter_list[-1] == None:
            self.filter_list[-1] = addedfilter
        self.filter_list.append(addedfilter)

    def apply_filters(self):
        output = self.backend_test_set()
        for infilter in self.filter_list:
            if infilter:
                output = self.filter_tags(output, infilter.get("tags"))
                output = self.filter_relevancy(output, infilter.get("relevancy"))
        return output

    def backend_test_set(self):
        return set([x.get(SOURCE) for x in self.get_coverage() if x.get(BACKEND)==self.backend and x.get(SOURCE)])

    def backend_passtrought_args(self):
        return self.get_filters()[-1]

    def get_filters(self):
        return self.filter_list

class MetadataLoaderMTF(MetadataLoader):
    import moduleframework.tools
    MTF_LINTER_PATH = os.path.dirname(moduleframework.tools.__file__)

    def __init__(self, *args, **kwargs):
        super(MetadataLoader, self).__init__(*args,**kwargs)

    def _import_linters(self):
        self._import_tests(os.path.join(self.MTF_LINTER_PATH,"*.py"), pathlenght=-2)


def test_loader():
    mt = MetadataLoader(localtion="example-component/tests")
    #print yaml.dump(mt.get_metadata())

#test_loader()