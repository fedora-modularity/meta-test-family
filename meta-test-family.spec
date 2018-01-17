%global framework_name moduleframework

Name:           meta-test-family
Version:        0.7.10
Release:        1%{?dist}
Summary:        Tool to test components of a modular Fedora

License:        GPLv2+
URL:            https://github.com/fedora-modularity/meta-test-family
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
# Exlcude ppc64: there is no docker package on ppc64
# https://bugzilla.redhat.com/show_bug.cgi?id=1465176
ExcludeArch:    ppc64

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires:       python2-avocado
Requires:       python2-avocado-plugins-output-html
Requires:       python-netifaces
Requires:       docker
Requires:       python2-pdc-client
Requires:       python2-modulemd
Requires:       python2-dockerfile-parse
Requires:       python-mistune
Requires:       python2-odcs-client
Provides:       modularity-testing-framework = %{version}-%{release}
Obsoletes:      modularity-testing-framework < 0.5.18-2

%description
Tool to test components of a modular Fedora.

%prep
%autosetup
# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%py2_build

%install
%py2_install
install -d -p -m 755 %{buildroot}%{_datadir}/%{framework_name}

%files
%license LICENSE
%{_mandir}/man1/mtf-env-clean.1*
%{_mandir}/man1/mtf-env-set.1*
%{_mandir}/man1/mtf-generator.1*
%{_bindir}/mtf
%{_bindir}/mtf-cmd
%{_bindir}/mtf-generator
%{_bindir}/mtf-env-set
%{_bindir}/mtf-env-clean
%{_bindir}/mtf-init
%{_bindir}/mtf-pdc-module-info-reader
%{python2_sitelib}/moduleframework/
%{python2_sitelib}/mtf/
%{python2_sitelib}/meta_test_family-*.egg-info/
%{_datadir}/moduleframework/


%changelog
* Wed Jan 17 2018 Petr "Stone" Hracek <phracek@redhat.com> 0.7.10-1
- Couple fixes based on #195 Pull Request (phracek@redhat.com)
- DISABLE CHECK-MTF-METADATA, PDC-MODULE and MTF/METADATA. IT FAILS
  (phracek@redhat.com)
- Using OpenShift 3.6.0 (phracek@redhat.com)
- Include OpenShift into Travis CI and testing (phracek@redhat.com)
- Fix typo in returncode (phracek@redhat.com)
- cath exception from subprocess to know return code (jscotka@redhat.com)
- remove avocado.run and replace it by subprocess to see outputs on the fly
  (jscotka@redhat.com)
- add tee to all integration tests for easier debugging (jscotka@redhat.com)
- speed optimization for avocado based test tag filtering (jscotka@redhat.com)

* Wed Dec 13 2017 Jan Scotka <jscotka@redhat.com> 0.7.9-1
- fix metadata if bug is found (jscotka@redhat.com)
- add tests for tooling if imported tests are included (jscotka@redhat.com)
- add git cloning abilities to metadata (jscotka@redhat.com)
- existing file should not be replaced via metadata (keep local version)
  (jscotka@redhat.com)
- url_downloader option in metadata.yaml allows download tests via URLlib
  (jscotka@redhat.com)
- improve search for helpMD file (jscotka@redhat.com)
- helpmd and docker lint cleanup of loading classes (jscotka@redhat.com)
- Update PR with PEP 8 and use @property also for avocado_test.py
  (phracek@redhat.com)
- Keep backwards compatibility (phracek@redhat.com)
- Couple updates. dependency_list and remove getters (phracek@redhat.com)
- Remove obsolete function which is not used anywhere (phracek@redhat.com)
- Fixes #167 First try for property, setter and getter (phracek@redhat.com)

* Wed Dec 06 2017 Jan Scotka <jscotka@redhat.com> 0.7.8-1
- remove mtf-env-clean from runthem script, it is on not good place and cleanup
  of env is not important to have it ther (jscotka@redhat.com)
- add vagrant file (jscotka@redhat.com)
- add vagrant file for metadata (jscotka@redhat.com)
- support for metadata to mtf tool (jscotka@redhat.com)
- metadata: fix generic test filters (jscotka@redhat.com)
- dependencies for testing in nicer and cleaner format for various distros
  (jscotka@redhat.com)
- remove mtf manpage (jscotka@redhat.com)
- revert generated man pages code (jscotka@redhat.com)
- Revert "remove all manpages" (scottyh@post.cz)
- run also without sudo, to improve pip for avocado (jscotka@redhat.com)
- dependencies in vagrant, travis and for local installation to file
  (jscotka@redhat.com)
- trying to clean man-page-generator (psklenar@redhat.com)
- add test for mtf-pdc-module-info-reader tool and enable it in travis
  (jscotka@redhat.com)
- trying to clean man-page-generator (psklenar@redhat.com)
- trying to clean man-page-generator (psklenar@redhat.com)
- remove regression, pdc_data needs to import BASEPATHDIR (jscotka@redhat.com)
- fix vagrant file, fix odcs format of repo, expected dir not repofile
  (jscotka@redhat.com)
- remove print function, typo (jscotka@redhat.com)
- create clean commit based on PR#172 (jscotka@redhat.com)
- add cool comments (psklenar@redhat.com)
- man page is generated now (psklenar@redhat.com)
- man page is generated now (psklenar@redhat.com)
- man page is generated now (psklenar@redhat.com)
- remove mtf-log-parser from specfile (jscotka@redhat.com)
- add all variables (psklenar@redhat.com)
- fix copr builds (jscotka@redhat.com)
- removed unused imports (psklenar@redhat.com)
- fixing all issues (jscotka@redhat.com)
- add version as its needed for man page generator (psklenar@redhat.com)
- script to run containers in taskotron (jscotka@redhat.com)
- trying travis (psklenar@redhat.com)
- some info about VARIABLES (psklenar@redhat.com)
- empty commit to start tests (psklenar@redhat.com)
- delete file (psklenar@redhat.com)
- not needed (psklenar@redhat.com)
- new line (psklenar@redhat.com)
- needed setup, parser in function (psklenar@redhat.com)
- have parser in function (psklenar@redhat.com)
- man mtf page is generated (psklenar@redhat.com)
- revert back to using python setup.py for package installation
  (jscotka@redhat.com)
- remove avocado html plugin from python dependencies, it is not important for
  mtf anyhow (jscotka@redhat.com)
- test metadata support tool for MTF (jscotka@redhat.com)
- fix profile handling (jscotka@redhat.com)
- add some tags to modulelint tests, to be able to filter them
  (jscotka@redhat.com)
- Updating docstring and adding pod functions (phracek@redhat.com)
- Support run command. (phracek@redhat.com)
- Better check if application exists (phracek@redhat.com)
- Fixes based on the PR comments. (phracek@redhat.com)
- Use command oc get and stdout instead of parsing json. (phracek@redhat.com)
- Add more docu stuff and some fixes. (phracek@redhat.com)
- testing containers in OpenShift (phracek@redhat.com)
- Update setup.py (phracek@redhat.com)
- Fix problem with paramters (phracek@redhat.com)
- Rewrite dnf/yum clean all functions (phracek@redhat.com)
- Check specific file extensions in /var/cache/yum|dnf directories
  (phracek@redhat.com)
- doc test is splitted into two tests. One is for whole image and second one is
  related only for install RPMs by RUN command (phracek@redhat.com)
- Add suport for check nodocs and clean_all (phracek@redhat.com)
- Update docstring (phracek@redhat.com)
- Update RTD. Use sphinx-build-2 (phracek@redhat.com)
- Update name classes (phracek@redhat.com)
- Update setup.py (phracek@redhat.com)
- Bump version to 0.7.7 (phracek@redhat.com)
- Documentation about linters (phracek@redhat.com)
- Split linters into more classes (phracek@redhat.com)
- Couple updates based on PR. (phracek@redhat.com)
- Rename function to assert_to_warn (phracek@redhat.com)
- Package man pages (phracek@redhat.com)
- man page updates based on #151 PR (phracek@redhat.com)
- Implement func mark_as_warn (phracek@redhat.com)
- Fix error in case help_md does not exist (phracek@redhat.com)
- Couple updates. (phracek@redhat.com)
- remove workarounds and add rpm to base package set workaround
  (jscotka@redhat.com)
- typos (psklenar@redhat.com)
- modify how it works images and store rendered output (jscotka@redhat.com)
- docs into RTD (psklenar@redhat.com)
- testsuite for mtf-init (psklenar@redhat.com)
- Bump version to 0.7.6 (phracek@redhat.com)
- Add mtf-generator man page. (phracek@redhat.com)
- Manual page for Meta-Test-Family (phracek@redhat.com)
- Fix error in case help_md does not exist (phracek@redhat.com)
- Fixes #142 Fix tracebacks for COPY and ADD directives (phracek@redhat.com)
- systemd test examples - testing fedora or centos via nspawn
  (jscotka@redhat.com)
- fix multihost regression, caused by code cleanup (jscotka@redhat.com)
- change test for decorators to generic one, and change self.skip to
  self.cancel() (jscotka@redhat.com)
- mistake in os.path.exist (there were makedirs by mistake)
  (jscotka@redhat.com)
- there is sometimes problem to do chmod, so run it via bash
  (jscotka@redhat.com)
- test for exception return in case of failed command, check ret code and
  raised exception (jscotka@redhat.com)
- add function to run script on remote machine (jscotka@redhat.com)
- nspawn operation moved to low level library not depenedent on mtf structure
  (jscotka@redhat.com)
- add argparse, move test.py into templates (psklenar@redhat.com)
- Bump new release (phracek@redhat.com)
- Update documentation and use absolute path (phracek@redhat.com)
- Fix some logging issues and yum checks (phracek@redhat.com)
- raise error in case of compatibility (error has to be raised explicitly)
  (jscotka@redhat.com)
- script which generate easy template (psklenar@redhat.com)
- create snapshot before calling setup from config, because machine does not
  have root directory (jscotka@redhat.com)
- Skip help.md for now if it does not exist (phracek@redhat.com)
- add tests for RUN instructions. One for dnf part and the other one for the
  rest (phracek@redhat.com)
- Use WARNING in case of ENVIRONMENT VARIABLES are not set in help.md
  (phracek@redhat.com)
- Add check for presence help.md (phracek@redhat.com)
- several fixes based on comment from PR. (phracek@redhat.com)
- New help.md fixes (phracek@redhat.com)
- Fix problems found during review (phracek@redhat.com)
- help.md sanity checker (phracek@redhat.com)
- Linter for help.md file (phracek@redhat.com)
- Check for is FROM first (phracek@redhat.com)
- linter: check Red Hat's and Fedora's images (ttomecek@redhat.com)
- add comment and link to bugzilla (jscotka@redhat.com)
- partial change of backward compatibility (jscotka@redhat.com)
- fix issue with bad exit code of mtf command (jscotka@redhat.com)
- Hidden feature for install packages from default module via ENVVAR, for
  further purposes, should not be used now (jscotka@redhat.com)
- pep8 change (jscotka@redhat.com)
- test module uses this config, after fixing composeurl handling, if there is
  bad link, causes error (jscotka@redhat.com)
- back to original timeout library (jscotka@redhat.com)
- spec: fix URL (phracek@redhat.com)
- fix compose handling and fix container issue with using container instead of
  url (jscotka@redhat.com)
- Remove shebang from two python files (phracek@redhat.com)
- Fix shebangs and so (phracek@redhat.com)
- avocado could say 'FAIL' too (psklenar@redhat.com)
- typo (jscotka@redhat.com)
- repair typo in config.yaml and add call of mtf-set-env to makefile
  (jscotka@redhat.com)
- better name of the file (psklenar@redhat.com)
- move main into site package (psklenar@redhat.com)
- new line fix (psklenar@redhat.com)
- function add, not so many spaces (psklenar@redhat.com)
- new line (psklenar@redhat.com)
- new tool avocado_log_json.py (psklenar@redhat.com)
- mtf summary (psklenar@redhat.com)
- add sample output, to see what you can expect (jscotka@redhat.com)
- add internal usage test as class of simpleTest.py (jscotka@redhat.com)
- add usage tests and improve doc (jscotka@redhat.com)
- Revert "add usage tests and improve doc" (jscotka@redhat.com)
- add usage tests and improve doc (jscotka@redhat.com)
- improv base avocado class to not skip modules with proper backend (parent)
  (jscotka@redhat.com)
- repaired submodule for check_modulemd (jscotka@redhat.com)
- revert back submodule (jscotka@redhat.com)
- example how S2I image can be tested with build process (jscotka@redhat.com)
- Update dockerlint a bit according to Container:Guidelines
  (phracek@redhat.com)
- remov baseruntime from Makefile (jscotka@redhat.com)
- remove python docker requirements, cause trouble in taskotron for shell test:
  (jscotka@redhat.com)
- move this important testcase to the end, cause sometimes error
  (jscotka@redhat.com)
- function removed, have to remove from nspawn helper (jscotka@redhat.com)
- taskotron - fix issue with missing base compose repo, when disabled local
  koji cloning (jscotka@redhat.com)

* Tue Oct 31 2017 Petr Hracek <phracek@redhat.com> 0.7.7-1
- new upstream release

* Tue Oct 24 2017 Petr Hracek <phracek@redhat.com> 0.7.6-1
- new upstream release

* Tue Oct 17 2017 Petr Hracek <phracek@redhat.com> 0.7.5-1
- new upstream release

* Wed Oct 04 2017 Petr Hracek <phracek@redhat.com> 0.7.4-2
- fix shebang from two python files

* Wed Oct 04 2017 Petr Hracek <phracek@redhat.com> 0.7.4-1
- fix some packaging stuff

* Tue Sep 26 2017 Jan Scotka <jscotka@redhat.com> 0.7.3-1
- remove old test and update template according to changes (jscotka@redhat.com)
- fix PDC trouble (Bad response code: 502) with Retry (jscotka@redhat.com)
- use mtf command as modulelinter scheduler instead of own solution
  (jscotka@redhat.com)
- base rework, more function to common class, add features to use parent in
  config and use mtf without config.yaml (jscotka@redhat.com)
- adding info about name of the module from loaded config (psklenar@redhat.com)
- add examples for pytest, unittest, nosetest. simple example
  (jscotka@redhat.com)

* Fri Sep 15 2017 Petr "Stone" Hracek <phracek@redhat.com> 0.7.2-1
- better permission info messages (psklenar@redhat.com)
- Improve  executable: (bkabrda@redhat.com)
- fixing No newline at the eof (psklenar@redhat.com)
- typos (psklenar@redhat.com)
- adding more user messages (psklenar@redhat.com)
- added more messages to users whats going on (psklenar@redhat.com)
- Fix missing dependency to python2-dockerfile-parse (phracek@redhat.com)
- Update meta-test-family.spec with mtf binary (phracek@redhat.com)
- Bump release (phracek@redhat.com)
- Fixes #95: Proper handling Dockerfile (phracek@redhat.com)
- Remove BaseRuntime test (jkosciel@redhat.com)
- Fix path for modulelint in run-them.sh (phracek@redhat.com)
- Fixes #79. Provide mtf binary which calls avocado run (phracek@redhat.com)
- Remove behave from requirements (phracek@redhat.com)
- Add requirements.txt for Python packages (phracek@redhat.com)
- Remove __main__ from python files which does not need it.
  (phracek@redhat.com)
- Build version (phracek@redhat.com)
- add fixes mentioned in PR, fix multihost test suite (jscotka@redhat.com)
- parse TARGET env var inside vagrant file (jscotka@redhat.com)
- add setup targets to ceck-pure* targets (jscotka@redhat.com)
- repair mariadb scl example (jscotka@redhat.com)
- changes according to PR review (jscotka@redhat.com)
- load modulemd file for each test (jscotka@redhat.com)
- module type not dependent, able to use them separately. Remove workarounds
  (jscotka@redhat.com)
- Verbose mode is turn off in rpmvalidation.py (phracek@redhat.com)
- Don't log if file is correct by FHS. (phracek@redhat.com)
- Fixing CI tests caused by branch testing_new_dnf_approach
  (phracek@redhat.com)
- example of tests for collections (#48) (scottyh@post.cz)
- Remove obsolete imports (phracek@redhat.com)
- Check /etc/os-release and docs for package (phracek@redhat.com)
- Use check against real packages present in docker image (phracek@redhat.com)
- Let's check only right packages and not whole image (phracek@redhat.com)
- Checking docs over rpm -qad. Remove obsolete fnc (phracek@redhat.com)
- Update checks for nodocs and clean all. Clean all detects metadata in
  /var/cache/<pkg_mgr/*.solv (phracek@redhat.com)
- Tests whether dnf contains --nodocs and clean all (phracek@redhat.com)
- Documentation for env split & some smaller fixes (#54) (scottyh@post.cz)
- better name for nonvalid url and recursive download comment out
  (jscotka@redhat.com)
- remove cleanup of environment not important for automation
  (jscotka@redhat.com)
- repair exception test, add remote repos for all dependencies  * fix issue
  with exception test, by mistake removed --show-job-log, so unable to see
  exception  * added remote repos for every dependency, it will fix issue on
  taskotron (jscotka@redhat.com)
- Update docu with bashhelper (phracek@redhat.com)
- Fix wrong import NspawnAvocadoTest (phracek@redhat.com)
- self.cancel() has to be used otherwise it has traceback (#57)
  (psklenar@gmail.com)
- Fix wrong import ContainerAvocadoTest (phracek@redhat.com)
- Fix wrong import. get_if_do_cleanup (phracek@redhat.com)
- Fix symbolic link to bashhelper.py (phracek@redhat.com)
- Fixes #30 Remove shebags (phracek@redhat.com)

* Wed Sep 13 2017 Petr Hracek <phracek@redhat.com> 0.7.1-2
- Fix missing dependency to dockerfile-parse

* Wed Sep 13 2017 Petr Hracek <phracek@redhat.com> 0.7.1-1
- Fix Proper handling Dockerfile #95
- Fix Remove baseruntime check #73
- Fix packaging issues #22
- Provide mtf binary #79

* Tue Sep 05 2017 Petr Hracek <phracek@redhat.com> 0.7.0-1
- new package built with tito

* Wed Aug 23 2017 Jan Scotka <jscotka@redhat.com> 0.6.1-1
- new package built with tito

* Tue Aug 22 2017 Petr Hracek <phracek@redhat.com> 0.6.0-1
- Introducing mtf-env-set and mtf-env-clean

* Mon Aug 07 2017 Nils Philippsen <nils@redhat.com> 0.5.19-1
- obsolete modularity-testing-framework-0.5.18-1, too

* Fri Aug 04 2017 Petr "Stone" Hracek <phracek@redhat.com> 0.5.19-1
- Add Landscap.io into project (#27) (phracek@redhat.com)
- Update scheduling.rst (phracek@redhat.com)
- Several fixes caused by missing testing. (phracek@redhat.com)
- Draft of refactoring avocado-tests. (phracek@redhat.com)
- replaced get_correct_backed in all internal tests by get_backend
  (jscotka@redhat.com)
- fixed typo caused by function moving to other module (jscotka@redhat.com)
- function names cleanup, removed "correct" "latest" words  fixing command
  sanitizer (jscotka@redhat.com)
- changed return variable to not be same as input param (jscotka@redhat.com)
- improved multihost test handling and created functions for normalizing
  commands before run (escaping) (jscotka@redhat.com)

* Tue Aug 01 2017 Petr Hracek <phracek@redhat.com> - 0.5.18-2
- Renaming package to the new name meta-test-family

* Mon Jul 10 2017 Jan Scotka <jscotka@redhat.com> 0.5.18-1
- improved name handling replacing bad chanracters (jscotka@redhat.com)

* Fri Jul 07 2017 Jan Scotka <jscotka@redhat.com> 0.5.17-1
- Added unitetest to pdc module (jscotka@redhat.com)
- make docker linter faster, not need to invoke parent setup in own setup
  class, because it does offline checking (jscotka@redhat.com)
- minimal config path fix (jscotka@redhat.com)
- changed testing module to minimal config. mksh is not in compose
  (jscotka@redhat.com)
- koji package downloading cleanup, moved to pdc instead of hardcoding in MTF
  main file (jscotka@redhat.com)
- fixed issues with deleting (jscotka@redhat.com)

* Tue Jul 04 2017 Jan Scotka <jscotka@redhat.com> 0.5.16-1
- PDC library install python3 version now by default, so have to ensure that
  python2 is there (jscotka@redhat.com)

* Tue Jul 04 2017 Jan Scotka <jscotka@redhat.com> 0.5.15-1
- 

* Wed Jun 28 2017 Jan Scotka <jscotka@redhat.com> 0.5.14-1
- solved issue with fails caused by dependencies (jscotka@redhat.com)

* Wed Jun 28 2017 Jan Scotka <jscotka@redhat.com> 0.5.13-1
- store repository to /opt instead of actual dir. it should help much with
  persistent data (jscotka@redhat.com)

* Wed Jun 28 2017 Jan Scotka <jscotka@redhat.com> 0.5.12-1
- added show-job-log to proper place for testing module and module linter
  (jscotka@redhat.com)

* Wed Jun 28 2017 Jan Scotka <jscotka@redhat.com> 0.5.11-1
- iproved testing if repo directory contains proper data (jscotka@redhat.com)

* Wed Jun 28 2017 Jan Scotka <jscotka@redhat.com> 0.5.10-1
- enable show job log for avocado, in testing module to have better output in
  taskotron (jscotka@redhat.com)

* Wed Jun 28 2017 Jan Scotka <jscotka@redhat.com> 0.5.9-1
- mistake in function causing traceback (jscotka@redhat.com)
- added doc string to helps to understand why MTF_RECURSIVE_DOWNLOAD
  (jscotka@redhat.com)
- added link to official compose instead of jkaluza's one (jscotka@redhat.com)
- if is bad name prefix, is_ is better (jscotka@redhat.com)
- if is bad name prefix, is_ is better (jscotka@redhat.com)
- added new option to run-them script (jscotka@redhat.com)
- solved issues with multiple directories, create just one repo, and do not
  overwrite it (jscotka@redhat.com)
- initial commit of recursive downloading of all dependent modules to one
  repository (jscotka@redhat.com)
- fixed vagrant issue with removing ssh keys (jscotka@redhat.com)
- Fix for ExcludeArch. BZ #1465176 (phracek@redhat.com)

* Mon Jun 26 2017 Jan Scotka <jscotka@redhat.com> 0.5.8-1
- last generator item in spec (jscotka@redhat.com)

* Mon Jun 26 2017 Jan Scotka <jscotka@redhat.com> 0.5.7-1
- removed generator from specfile (jscotka@redhat.com)

* Mon Jun 26 2017 Jan Scotka <jscotka@redhat.com> 0.5.6-1
- added more comments to receent changes (jscotka@redhat.com)
- fix issue 36 (igulina@redhat.com)
- docs replacing generator with mtf-generator (igulina@redhat.com)
- remove deprecated generator func (igulina@redhat.com)

* Mon Jun 26 2017 Jan Scotka <jscotka@redhat.com> 0.5.5-1
- 

* Mon Jun 26 2017 Jan Scotka <jscotka@redhat.com> 0.5.4-1
- require docker just for intel (jscotka@redhat.com)

* Fri Jun 23 2017 Jan Scotka <jscotka@redhat.com> 0.5.3-1
- docs building up api menu in main menu (igulina@redhat.com)

* Mon Jun 19 2017 Jan Scotka <jscotka@redhat.com> 0.5.2-1
- added deps to runthem script (jscotka@redhat.com)
- added dependency on modulemd for furure usage (jscotka@redhat.com)
- bad version from pip (jscotka@redhat.com)
- added constant instead of variable inside class (jscotka@redhat.com)
- added pdc library dependency, removed own solution, used API
  (jscotka@redhat.com)
- rename get_correct_config (igulina@redhat.com)
- update error handler for get_correct_config (igulina@redhat.com)
- fix var assignment for get_correct_config (igulina@redhat.com)
- update docstring for get_correct_config (igulina@redhat.com)
- removed version string from conf.py (jscotka@redhat.com)
- removed version string from conf.py (jscotka@redhat.com)

* Thu Jun 15 2017 Jan Scotka <jscotka@redhat.com> 0.5.1-1
- added symlink to solve moving minimal config example to user guide
  (jscotka@redhat.com)

* Thu Jun 15 2017 Jan Scotka <jscotka@redhat.com>
- added symlink to solve moving minimal config example to user guide
  (jscotka@redhat.com)

* Thu Jun 15 2017 Jan Scotka <jscotka@redhat.com> 0.5.0-1
- docs removing readme.rst link (igulina@redhat.com)
- docs following PR review remarks (igulina@redhat.com)
- docs typos, errors and whitespaces (igulina@redhat.com)
- docs introducing glossary page (igulina@redhat.com)
- docs list of test methods (igulina@redhat.com)
- docs user guide main steps, conf file,env variables, troubleshooting
  (igulina@redhat.com)
- docs intro page, license, installation (igulina@redhat.com)
- Simple README with what MTF is and a link to docs (igulina@redhat.com)

* Thu Jun 15 2017 Jan Scotka <jscotka@redhat.com> 0.4.64-1
- fixed issue when using repos. mistake caused that it created list in list
  (jscotka@redhat.com)

* Thu Jun 15 2017 Jan Scotka <jscotka@redhat.com> 0.4.63-1
- fixed issue with adding to list what is not list (jscotka@redhat.com)

* Thu Jun 15 2017 Jan Scotka <jscotka@redhat.com> 0.4.62-1
- fixed self test check (jscotka@redhat.com)
- possible to get dependencies with urls via dictionary (jscotka@redhat.com)
- added fixes for stopping nspawn container. in case there is some traceback it
  should remove nspawn machine (jscotka@redhat.com)

* Mon Jun 12 2017 Jan Scotka <jscotka@redhat.com> 0.4.61-1
- Add upstream check_modulemd (phracek@redhat.com)
- added doc strings (jscotka@redhat.com)
- added functions to get architectures (jscotka@redhat.com)

* Fri Jun 09 2017 Jan Scotka <jscotka@redhat.com> 0.4.60-1
- added dockerfile to None in case path does not exist (jscotka@redhat.com)

* Fri Jun 09 2017 Petr "Stone" Hracek <phracek@redhat.com> 0.4.59-1
- Use version directly in setup.py and SPEC file in main dir.
  (phracek@redhat.com)

* Fri Jun 09 2017 Petr "Stone" Hracek <phracek@redhat.com> 0.4.58-1
- fix Dockerlint tests and using AvocadoTest class directly

* Fri Jun 09 2017 Jan Scotka <jscotka@redhat.com> 0.4.57-1
- 

* Wed Jun 07 2017 Jan Scotka <jscotka@redhat.com> 0.4.56-1
- Add dependency into python2-dockerfile-parse (phracek@redhat.com)

* Tue Jun 06 2017 Jan Scotka <jscotka@redhat.com> 0.4.55-1
 - code cleanup
 - added check_modulemd as submodule
 - exceptions improvement

- 

* Mon Jun 05 2017 Jan Scotka <jscotka@redhat.com> 0.4.54-1
- 

* Mon Jun 05 2017 Jan Scotka <jscotka@redhat.com> 0.4.53-1
- 

* Fri Jun 02 2017 Jan Scotka <jscotka@redhat.com> 0.4.52-1
- 

* Thu Jun 01 2017 Jan Scotka <jscotka@redhat.com> 0.4.51-1
- 

* Thu Jun 01 2017 Jan Scotka <jscotka@redhat.com> 0.4.50-1
- 

* Wed May 31 2017 Jan Scotka <jscotka@redhat.com> 0.4.49-1
- 

* Wed May 31 2017 Jan Scotka <jscotka@redhat.com> 0.4.48-1
- 

* Wed May 31 2017 Jan Scotka <jscotka@redhat.com> 0.4.47-1
- 

* Wed May 31 2017 Jan Scotka <jscotka@redhat.com> 0.4.46-1
- 

* Wed May 31 2017 Jan Scotka <jscotka@redhat.com> 0.4.45-1
- 

* Wed May 31 2017 Jan Scotka <jscotka@redhat.com> 0.4.44-1
- 

* Tue May 30 2017 Jan Scotka <jscotka@redhat.com> 0.4.43-1
- 

* Tue May 30 2017 Jan Scotka <jscotka@redhat.com> 0.4.42-1
- 

* Tue May 30 2017 Jan Scotka <jscotka@redhat.com> 0.4.41-1
- 

* Tue May 30 2017 Jan Scotka <jscotka@redhat.com> 0.4.40-1
- 

* Mon May 29 2017 Jan Scotka <jscotka@redhat.com> 0.4.39-1
- adapted to new avocado self.cancel() instead of using internal exception for skipping tests on the fly
- imporved links to composes in testing module. No modules builds in koji.


* Fri May 26 2017 Jan Scotka <jscotka@redhat.com> 0.4.38-1
- 

* Fri May 26 2017 Jan Scotka <jscotka@redhat.com> 0.4.37-1
- 

* Fri May 26 2017 Jan Scotka <jscotka@redhat.com> 0.4.36-1
- removed appearance of change log inside (jscotka@redhat.com)

* Fri May 26 2017 Jan Scotka <jscotka@redhat.com> 0.4.35-1
- 

* Thu May 25 2017 Jan Scotka <jscotka@redhat.com> 0.4.34-1
- removed setup.py symlink (jscotka@redhat.com)

* Wed May 24 2017 Jan Scotka <jscotka@redhat.com> 0.4.33-1
- try this vice versa removed symlinked specfile and added symlink to setup.py
  (jscotka@redhat.com)

* Wed May 24 2017 Jan Scotka <jscotka@redhat.com> 0.4.32-1
- 

* Wed May 24 2017 Jan Scotka <jscotka@redhat.com>
- 

* Wed May 24 2017 Jan Scotka <jscotka@redhat.com> 0.4.30-1
- rename 'generator' script to 'mtf-generator' (nils@redhat.com)

* Mon May 22 2017 Jan Scotka <jscotka@redhat.com> 0.4.29-1
- 

* Fri May 19 2017 Jan Scotka <jscotka@redhat.com> 0.4.28-1
- changes with specfile (jscotka@redhat.com)

* Fri May 19 2017 Jan Scotka <jscotka@redhat.com> 0.4.27-1
- disabled test for package signing (jscotka@redhat.com)
- Moving SPEC to specific distro directory (phracek@redhat.com)

* Thu May 18 2017 Petr Hracek <phracek@redhat.com> - 0.4.26-1
- Calulcate correct path to SPEC file

* Thu May 18 2017 Petr "Stone" Hracek <phracek@redhat.com> 0.4.25-2
- Calculate correct path to SPEC file (phracek@redhat.com)

* Thu May 18 2017 Petr Hracek <phracek@redhat.com> - 0.4.25-2
- Calulcate correct path to SPEC file

* Thu May 18 2017 Jan Scotka <jscotka@redhat.com> 0.4.25-1
- 

* Wed May 17 2017 Jan Scotka <jscotka@redhat.com> 0.4.24-1
- added new version of module lint, it is now directory, so that repaired in
  common tests (jscotka@redhat.com)

* Tue May 16 2017 Jan Scotka <jscotka@redhat.com> 0.4.23-1
- do not remove base packages (jscotka@redhat.com)

* Tue May 16 2017 Jan Scotka <jscotka@redhat.com> 0.4.22-1
- modulelint tests in subdirectory and some improvements (jscotka@redhat.com)
- packaging: trivial fixes (ignatenkobrain@fedoraproject.org)

* Fri May 12 2017 Jan Scotka <jscotka@redhat.com> 0.4.21-1
- fix typo in test dependencies section (nils@redhat.com)

* Fri May 12 2017 Jan Scotka <jscotka@redhat.com> 0.4.20-1
- version read from specfile, test if it will work well (jscotka@redhat.com)

* Fri May 12 2017 Jan Scotka <jscotka@redhat.com> 0.4.19-1
- added longer delay and number of attempts for koji, seems that koji is
  somethimes broken for longer time (jscotka@redhat.com)

* Fri May 12 2017 Jan Scotka <jscotka@redhat.com> 0.4.18-1
- added longer delay and number of attempts for koji, seems that koji is
  somethimes broken for longer time (jscotka@redhat.com)

* Thu May 11 2017 Jan Scotka <jscotka@redhat.com> 0.4.17-1
- improved makefiles and vagrant (jscotka@redhat.com)
- added new lines to doc strings (jscotka@redhat.com)
- added blank line to doc scrings (jscotka@redhat.com)

* Thu May 11 2017 Jan Scotka <jscotka@redhat.com> 0.4.16-1
- repaired one mistake caused by removing avocado from common library
  (jscotka@redhat.com)
- repaired one mistake caused by removing avocado from common library
  (jscotka@redhat.com)
- added link to read the docs documentation (jscotka@redhat.com)

* Thu May 11 2017 Jan Scotka <jscotka@redhat.com> 0.4.15-1
- added link to read the docs documentation (jscotka@redhat.com)
- removed dnf search via dnf command, beter to ask path directly
  (jscotka@redhat.com)
- added dependencies to setup.py file (jscotka@redhat.com)
- try to be more prepared for virt-env (jscotka@redhat.com)
- delete html folder in make clean (phracek@redhat.com)
- Several documentation updates (phracek@redhat.com)
- Remove obsolete documentation (phracek@redhat.com)

* Tue May 09 2017 Jan Scotka <jscotka@redhat.com> 0.4.14-1
- external setup and teardown moved to begin or end of module init/clean
  (jscotka@redhat.com)

* Tue May 09 2017 Jan Scotka <jscotka@redhat.com> 0.4.13-1
- added args and kwargs to init because baseruntime uses that -> it caused
  troubles when inherited with __init__method (jscotka@redhat.com)
- typo introduced inside formatting (jscotka@redhat.com)
- removed retry block and try to use direct wait (jscotka@redhat.com)
- improved multihoste test to use created function instead of calling it
  directly (jscotka@redhat.com)
- improved multihoste test to use created function instead of calling it
  directly (jscotka@redhat.com)

* Tue May 09 2017 Jan Scotka <jscotka@redhat.com> 0.4.12-1
- solved issue with shell tests (jscotka@redhat.com)
- added longer timeout for retry, try to solve issue with shell tests
  (jscotka@redhat.com)
- try to remove outside retry (jscotka@redhat.com)

* Mon May 08 2017 Jan Scotka <jscotka@redhat.com> 0.4.11-1
- bumped version (jscotka@redhat.com)
- disables sh test (jscotka@redhat.com)

* Mon May 08 2017 Jan Scotka <jscotka@redhat.com> 0.4.10-1
- disabled microdnf test to see ci for framework passing (jscotka@redhat.com)

* Mon May 08 2017 Jan Scotka <jscotka@redhat.com> 0.4.9-1
- imporved test module, removed bash test because it needs deeper inspection
  (jscotka@redhat.com)

* Mon May 08 2017 Jan Scotka <jscotka@redhat.com> 0.4.8-1
- bumped version (jscotka@redhat.com)
- cleaner solution to set repos and what to install instead for rewriting class
  values (jscotka@redhat.com)
- solved issues with changing to use init of classes (there is 60s timeout in
  avocado) (jscotka@redhat.com)
- added debug options for shell command, there is some issue with running
  nspawn on background, TODO: needs inspect (jscotka@redhat.com)
- Several updates for documentation stuff. (phracek@redhat.com)

* Fri May 05 2017 Jan Scotka <jscotka@redhat.com> 0.4.7-1
- version increased (jscotka@redhat.com)
- added straight usage of bashhelper python lib it is in same directory
  (jscotka@redhat.com)

* Fri May 05 2017 Jan Scotka <jscotka@redhat.com> 0.4.6-1
- version increased (jscotka@redhat.com)
- allow use more picle file in bash helper to support more machines
  (jscotka@redhat.com)
- removed workaround characters around command to have better output
  (jscotka@redhat.com)
- mistake in bash helper (jscotka@redhat.com)
- imporved makefile for test module to check more possibilities
  (jscotka@redhat.com)
- small typo there (jscotka@redhat.com)
- skip in setup phase should be faster (jscotka@redhat.com)

* Thu May 04 2017 Jan Scotka <jscotka@redhat.com> 0.4.5-1
- added better handling of running machines in nspawn (jscotka@redhat.com)

* Thu May 04 2017 Jan Scotka <jscotka@redhat.com> 0.4.4-1
- repaired problem with dictionary change on the fly (jscotka@redhat.com)

* Thu May 04 2017 Jan Scotka <jscotka@redhat.com> 0.4.3-1
- typo (jscotka@redhat.com)
- version back (jscotka@redhat.com)
- removed unwanted symlink (jscotka@redhat.com)

* Thu May 04 2017 Jan Scotka <jscotka@redhat.com> 0.4.2-1
- bumped version (jscotka@redhat.com)
- added info for chroot path (jscotka@redhat.com)

* Thu May 04 2017 Jan Scotka <jscotka@redhat.com> 0.4.1-1
- small trouble inside multios test caused by using function get correct
  backend (jscotka@redhat.com)
- version increased (jscotka@redhat.com)
- added initsection for base class (jscotka@redhat.com)

* Thu May 04 2017 Jan Scotka <jscotka@redhat.com> 0.3.32-1
- added possibility to add more machines if you want, and play with them
  (jscotka@redhat.com)

* Thu May 04 2017 Jan Scotka <jscotka@redhat.com> 0.3.31-1
- after discussion with jkaluza added more retry (jscotka@redhat.com)

* Thu May 04 2017 Jan Scotka <jscotka@redhat.com> 0.3.30-1
- added better debugging to Retry (allow to output also original exception)
  (jscotka@redhat.com)

* Thu May 04 2017 Jan Scotka <jscotka@redhat.com> 0.3.29-1
- added possibility to retry PDC URL in case of no data (jscotka@redhat.com)

* Wed May 03 2017 Jan Scotka <jscotka@redhat.com> 0.3.28-1
- added better debugging in case container is not running (jscotka@redhat.com)

* Wed May 03 2017 Jan Scotka <jscotka@redhat.com> 0.3.27-1
- bumperd version (jscotka@redhat.com)

* Wed May 03 2017 Jan Scotka <jscotka@redhat.com> 0.3.26-1
- added symlink to docs directory, to enable pydoc (jscotka@redhat.com)
- Add documents for generation RTD (phracek@redhat.com)

* Wed May 03 2017 Jan Scotka <jscotka@redhat.com> 0.3.25-1
- version increased (jscotka@redhat.com)
- removed hardcoded dnf and microdnf commands and added possibility to use null
  moduleMD file (jscotka@redhat.com)

* Wed May 03 2017 Jan Scotka <jscotka@redhat.com> 0.3.24-1
- adde back filter active=true for PDC, it causes strange errors
  (jscotka@redhat.com)

* Tue May 02 2017 Jan Scotka <jscotka@redhat.com> 0.3.23-1
- bumped version (jscotka@redhat.com)
- s (jscotka@redhat.com)

* Tue May 02 2017 Jan Scotka <jscotka@redhat.com> 0.3.22-1
- 

* Tue May 02 2017 Jan Scotka <jscotka@redhat.com> 0.3.21-1
- nspawn used inheride status/start/stop functions, it was bad, because it was
  on host not inside container (jscotka@redhat.com)

* Tue May 02 2017 Jan Scotka <jscotka@redhat.com> 0.3.20-1
- there is missing space (jscotka@redhat.com)

* Tue May 02 2017 Jan Scotka <jscotka@redhat.com> 0.3.19-1
- added more packages to io install based on baseruntime baseimage profile
  (jscotka@redhat.com)

* Tue May 02 2017 Jan Scotka <jscotka@redhat.com> 0.3.18-1
- small typo, it is not cmd but command (jscotka@redhat.com)

* Tue May 02 2017 Jan Scotka <jscotka@redhat.com> 0.3.17-1
- version increased (jscotka@redhat.com)
- added explicit wait after commands in nspawn (jscotka@redhat.com)
- added example how it can be used for multimachine testing in actual way
  (jscotka@redhat.com)
- added better koji handling in case of missing some packages because of issue
  in koji (jscotka@redhat.com)
- removed changing file inside copy test, it causes traceback on docker (bad
  selinux context probably) (jscotka@redhat.com)

* Sat Apr 29 2017 Jan Scotka <jscotka@redhat.com> 0.3.16-1
- removed exceptions and added if expressions (jscotka@redhat.com)

* Sat Apr 29 2017 Jan Scotka <jscotka@redhat.com> 0.3.15-1
- allow in setup cleanup, start stop etc section to let processes at background
  (jscotka@redhat.com)

* Sat Apr 29 2017 Jan Scotka <jscotka@redhat.com> 0.3.14-1
- fixed issue with duplicated shell cmd param (jscotka@redhat.com)

* Sat Apr 29 2017 Jan Scotka <jscotka@redhat.com> 0.3.13-1
- improved copy selftest (jscotka@redhat.com)

* Sat Apr 29 2017 Jan Scotka <jscotka@redhat.com> 0.3.12-1
- removed sleep caused big issue there, because it starts on background
  (jscotka@redhat.com)

* Sat Apr 29 2017 Jan Scotka <jscotka@redhat.com> 0.3.11-1
- added timeout library from cockpit project, improved debug output handling in
  pdc_data lib, changes in documentation, added debug option
  (jscotka@redhat.com)

* Fri Apr 28 2017 Jan Scotka <jscotka@redhat.com> 0.3.10-1
- repaired issue when avocado returns other code that 1 (jscotka@redhat.com)

* Fri Apr 28 2017 Jan Scotka <jscotka@redhat.com> 0.3.9-1
- moved back to version what do copy via machinectl (jscotka@redhat.com)

* Fri Apr 28 2017 Jan Scotka <jscotka@redhat.com> 0.3.8-1
- added dependency solver for modules (jscotka@redhat.com)

* Fri Apr 28 2017 Jan Scotka <jscotka@redhat.com> 0.3.7-1
- switching to proper commit version for test (jscotka@redhat.com)

* Fri Apr 28 2017 Jan Scotka <jscotka@redhat.com> 0.3.6-1
- fixing logic inside (jscotka@redhat.com)
- better logging inside code and divided some variables to common library
  (jscotka@redhat.com)
- list of repos in nspawn, to see how it is set (jscotka@redhat.com)

* Fri Apr 28 2017 Jan Scotka <jscotka@redhat.com> 0.3.5-1
- imporved package section, removed installation of all src pacakges, because
  it fails manytimes with comflict packages (jscotka@redhat.com)

* Thu Apr 27 2017 Jan Scotka <jscotka@redhat.com> 0.3.4-1
- added value to Makefile of testing module (jscotka@redhat.com)

* Thu Apr 27 2017 Jan Scotka <jscotka@redhat.com> 0.3.3-1
- missing brackets for functions. causing bad output (jscotka@redhat.com)

* Thu Apr 27 2017 Jan Scotka <jscotka@redhat.com> 0.3.2-1
- added documentation README, and config files repaired few smalled things
  called autopep8 (jscotka@redhat.com)
- rewritten part of documentation (jscotka@redhat.com)

* Thu Apr 27 2017 Jan Scotka <jscotka@redhat.com> 0.3.1-1
- added verbosity, it will be cleaner if you see output somehow
  (jscotka@redhat.com)

* Thu Apr 27 2017 Jan Scotka <jscotka@redhat.com> 0.2.47-1
- solved issue with stdout and stderr for nspawn (jscotka@redhat.com)

* Wed Apr 26 2017 Jan Scotka <jscotka@redhat.com> 0.2.46-1
- version increasion (jscotka@redhat.com)
- removed active=true it seems that somewthing changed (jscotka@redhat.com)
- remove docker-distribution package (phracek@redhat.com)

* Wed Apr 26 2017 Jan Scotka <jscotka@redhat.com> 0.2.45-1
- copytree needs nonexisting directory (jscotka@redhat.com)

* Wed Apr 26 2017 Jan Scotka <jscotka@redhat.com> 0.2.44-1
- pad source path (jscotka@redhat.com)
- pad source path (jscotka@redhat.com)

* Wed Apr 26 2017 Jan Scotka <jscotka@redhat.com> 0.2.43-1
- another issue with distro creation (jscotka@redhat.com)

* Wed Apr 26 2017 Jan Scotka <jscotka@redhat.com> 0.2.42-1
- dirs are mot created mkdirs function does not exist (jscotka@redhat.com)

* Wed Apr 26 2017 Jan Scotka <jscotka@redhat.com> 0.2.41-1
- small typo in code of installing packages (jscotka@redhat.com)

* Wed Apr 26 2017 Jan Scotka <jscotka@redhat.com> 0.2.40-1
- fixed (jscotka@redhat.com)

* Wed Apr 26 2017 Jan Scotka <jscotka@redhat.com> 0.2.39-1
- repaired more stuff, repaired nspawn repos handling (jscotka@redhat.com)
- add a way to skip SELinux disabling (ttomecek@redhat.com)
- fixing typos and wrong link (rpitonak@redhat.com)

* Tue Apr 25 2017 Jan Scotka <jscotka@redhat.com> 0.2.38-1
- fixed selftest of paths,  this test is bad in case running inside CIs
  (jscotka@redhat.com)

* Tue Apr 25 2017 Jan Scotka <jscotka@redhat.com> 0.2.37-1
- repaired selinux disablig, ignoring status in case you dont have selinux
  enable enabling repos inside module nspawn for dnf command
  (jscotka@redhat.com)

* Tue Apr 25 2017 Jan Scotka <jscotka@redhat.com> 0.2.36-1
- added job output to testing module directly to stdout to see progress
  (jscotka@redhat.com)

* Mon Apr 24 2017 Jan Scotka <jscotka@redhat.com> 0.2.35-1
- bump version (jscotka@redhat.com)
- not in directory where tests are, it is not good when there are another
  resources (jscotka@redhat.com)

* Mon Apr 24 2017 Jan Scotka <jscotka@redhat.com> 0.2.34-1
- small typo (jscotka@redhat.com)

* Mon Apr 24 2017 Jan Scotka <jscotka@redhat.com> 0.2.33-1
- added messages to stderr, to see progress. It causes troubles to taskotron if
  no output there (jscotka@redhat.com)

* Mon Apr 24 2017 Jan Scotka <jscotka@redhat.com> 0.2.32-1
- skip if package not aviable (jscotka@redhat.com)

* Mon Apr 24 2017 Jan Scotka <jscotka@redhat.com> 0.2.31-1
- download just x86_64 arch packages (jscotka@redhat.com)

* Mon Apr 24 2017 Jan Scotka <jscotka@redhat.com> 0.2.30-1
- removed doing repos although it already exists (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.29-1
- 

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.28-1
- I've introduced mistake by this echo (jscotka@redhat.com)
- I've introduced mistake by this echo (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.27-1
- big mistake in generating repos (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.26-1
- all repositories will be generated locally (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.25-1
- added new libe before end, in case there is interactive command it causes no
  new line (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.24-1
- added dependency on python netifaces library (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.23-1
- solved issue with missin ip command, removed and replaced by pythonish style
  (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.22-1
- imporved copying of files to nspawn, using machinectl, added workaround for
  fedpkg https://phab.qa.fedoraproject.org/T944#13630 (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.21-1
- more baseruntime fixes (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.20-1
- version increased (jscotka@redhat.com)
- added resources for baseruntime, it is copy from theitrss project
  (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com>
- 

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.18-1
- restricted it for nspawn for now (jscotka@redhat.com)

* Fri Apr 21 2017 Jan Scotka <jscotka@redhat.com> 0.2.17-1
- simplified run_them script and added better localrepo names, will then work
  with more local repos for various modules (jscotka@redhat.com)
- improved dnf handling inside, microdnf selftest is working well
  (jscotka@redhat.com)

* Thu Apr 20 2017 Jan Scotka <jscotka@redhat.com> 0.2.16-1
- added copying of repositories inside NSPAWN, to have them enabled for using
  by tests (baseruntime) (jscotka@redhat.com)

* Thu Apr 20 2017 Jan Scotka <jscotka@redhat.com> 0.2.15-1
- added copying of repositories inside NSPAWN, to have them enabled for using
  by tests (baseruntime) (jscotka@redhat.com)

* Thu Apr 20 2017 Jan Scotka <jscotka@redhat.com> 0.2.14-1
- improved for taskotron usecase (jscotka@redhat.com)

* Thu Apr 20 2017 Jan Scotka <jscotka@redhat.com> 0.2.13-1
- added changes to support baseruntime exit commands inside code
  (jscotka@redhat.com)

* Thu Apr 20 2017 Jan Scotka <jscotka@redhat.com> 0.2.12-1
- 

* Thu Apr 20 2017 Jan Scotka <jscotka@redhat.com> 0.2.11-1
- version and specfile imporved (jscotka@redhat.com)

* Thu Apr 20 2017 Jan Scotka <jscotka@redhat.com> 0.2.10-1
- new version (jscotka@redhat.com)
- new version (jscotka@redhat.com)

* Thu Apr 20 2017 Jan Scotka <jscotka@redhat.com> 0.2.9-1
- 

* Thu Apr 20 2017 Jan Scotka <jscotka@redhat.com> 0.2.8-1
- prepare for databases, add some common varibles what could be used for
  testing inside code and in configs (jscotka@redhat.com)
- called autopep8 to imporove style of code (jscotka@redhat.com)
- added changes to nspawn  helper, to workaround issues with retun codes and
  bad chars there (jscotka@redhat.com)
- Update documentation (phracek@redhat.com)
- removed upgrading avocado via pip, it cause fail (jscotka@redhat.com)
- small improvements (jscotka@redhat.com)
- after discussing with Bruno, there wwre wound issues in machinectl, so added
  workaround (jscotka@redhat.com)
- reworked part for fetching data.dependencies.requires (jscotka@redhat.com)

* Wed Apr 19 2017 Petr "Stone" Hracek <phracek@redhat.com> 0.2.7-1
- Bump release (phracek@redhat.com)
- typo (jscotka@redhat.com)
- added srippint to rpm commans because it contains bad character
  (jscotka@redhat.com)
- added possibility to use python format variables inside config and then it is
  translated by framework (jscotka@redhat.com)
- iproved docker skip (jscotka@redhat.com)
- removed process object. Unable to pickle, this commit does workaround what
  should be removed in future (jscotka@redhat.com)
- removed memcached specific things from test module (jscotka@redhat.com)
- removed memcached dependencies (jscotka@redhat.com)
- missing nspawn when using local reposiries (jscotka@redhat.com)
- added also enabling selinux in teardown, to return system to previous state
  (jscotka@redhat.com)
- added setenforce 0, because nspawn is failing on F-25 (jscotka@redhat.com)
- changes in testing module example, to actual koji link (jscotka@redhat.com)
- added new link to modulemd file of memcached (jscotka@redhat.com)
- added dependencies on another modules when installing (from PDC)
  (jscotka@redhat.com)
- removed passwd as dependency, not needed (jscotka@redhat.com)
- removed microdnf dep, because it is not installed now in container images or
  not in fedora25 (jscotka@redhat.com)
- added microdnf dependency (jscotka@redhat.com)
- added nspawn helper for rpm based module testing. (jscotka@redhat.com)
- removed localrepository if exist (jscotka@redhat.com)
- improved to properly return good RC for taskotron (jscotka@redhat.com)
- added return stat handling for taskotron (jscotka@redhat.com)
- removed sleep (jscotka@redhat.com)
- more changes (jscotka@redhat.com)
- there were typo in koji downloader (jscotka@redhat.com)
- added possibility to create local repository (jscotka@redhat.com)
- typo (jscotka@redhat.com)
- added possibility to list latest bits from PDC and little bit removed
  duplication of code (jscotka@redhat.com)
- added possibility to list latest bits from PDC and little bit removed
  duplication of code (jscotka@redhat.com)

* Tue Apr 11 2017 Petr "Stone" Hracek <phracek@redhat.com> 0.2.6-1
- Bump version (phracek@redhat.com)
- restructured compose info parser to be able to use them in framework
  (baseruntime RFE) (jscotka@redhat.com)
- restructured compose info parser to be able to use them in framework
  (baseruntime RFE) (jscotka@redhat.com)
- restructured compose info parser to be able to use them in framework
  (baseruntime RFE) (jscotka@redhat.com)
- added distro-sync + install command (jscotka@redhat.com)
- install test dependencies inside setup instead of loadconfig function
  (jscotka@redhat.com)
- moved initialization of name to init of docker class (jscotka@redhat.com)
- moved some part to init method of helper to be able use it also without
  direct using in tests (jscotka@redhat.com)
- typo in fedmsg parser (jscotka@redhat.com)
- added special parameter for taskotron (jscotka@redhat.com)
- imporved taskotron reader to be able use just name-stream-version
  (jscotka@redhat.com)
- bad example fedora message (jscotka@redhat.com)
- moved baseruntime to location to be same as a module name
  (jscotka@redhat.com)
- removed printing of module (jscotka@redhat.com)
- missing module type variable (jscotka@redhat.com)
- imporved run_them script to be able use also compose as input
  (jscotka@redhat.com)
- imporved run_them script to be able use also compose as input
  (jscotka@redhat.com)
- added compose handling library for modules (jscotka@redhat.com)
- added tool for parsing data from final compose (jscotka@redhat.com)
- added timeout before testing (jscotka@redhat.com)
- added timeout before testing (jscotka@redhat.com)
- missing tests subdir (jscotka@redhat.com)
- have to check also if link exists (jscotka@redhat.com)
- if missing profiles, use components:rpms packages to install
  (jscotka@redhat.com)
- improved simple test of testing module (jscotka@redhat.com)
- improved shell test to not fail (jscotka@redhat.com)
- improved shell test to not fail (jscotka@redhat.com)
- adapted PDC changes (jscotka@redhat.com)
- adapted PDC changes (jscotka@redhat.com)
- adapted PDC changes (jscotka@redhat.com)
- added minimal config for module linter in case config does not exist
  (jscotka@redhat.com)
- testing commit (jscotka@redhat.com)
- mistake in fedmsg reader path and removed installing itself
  (jscotka@redhat.com)
- repaired helper tool (jscotka@redhat.com)
- Typo in setup. Missing tools directory (phracek@redhat.com)
- repo repos typos (psklenar@redhat.com)
- removed old code (jscotka@redhat.com)
- removed old code (jscotka@redhat.com)
- Add directory tools (phracek@redhat.com)
- Remove obsolete file (phracek@redhat.com)
- Packaging changes (phracek@redhat.com)
- added another helper tool (jscotka@redhat.com)
- added another helper tool (jscotka@redhat.com)
- added calling avocado service manager instead of starting manually via
  command (jscotka@redhat.com)
- changed to 127.0.0.1 instead of localhost (jscotka@redhat.com)
- changes of haproxy (jscotka@redhat.com)
- more fixes of haproxy to be cleaner (jscotka@redhat.com)
- added some tweaks of haproxy tests (jscotka@redhat.com)
- added some tweaks of haproxy tests (jscotka@redhat.com)
- Bump version with the same as tito (phracek@redhat.com)

* Wed Apr 05 2017 Petr "Stone" Hracek <phracek@redhat.com> 0.2.5-1
- Fix Packaging Guidelines (phracek@redhat.com)
- added memcached to dependencies (jscotka@redhat.com)
- one bug causing that it is not testing proper things (jscotka@redhat.com)
- sed typo (psklenar@redhat.com)
- added small workaround for html plugin (jscotka@redhat.com)
- added symlink to work with testmodule in upstream (jscotka@redhat.com)
- introduced regression for shell tests (jscotka@redhat.com)
- Bump version (phracek@redhat.com)

* Wed Apr 05 2017 Petr Hracek <phracek@redhat.com> 0.2.4-1
- version increased (phracek@redhat.com)

* Fri Mar 31 2017 Jan Scotka <jscotka@redhat.com> 0.2.3-1
- version increased (jscotka@redhat.com)

* Fri Mar 31 2017 Jan Scotka <jscotka@redhat.com> 0.2.2-1
- improved specfile Source0 (jscotka@redhat.com)
- added licenses to files, permissions repaired (jscotka@redhat.com)
- Bum version (phracek@redhat.com)

* Fri Mar 31 2017 Jan Scotka <jscotka@redhat.com> 0.2.1-1
- moved checking ENV variable to functions to allow override them
  (jscotka@redhat.com)
- added possibility to pass file via parameter, not just via stdin, could be
  cleaner solution (jscotka@redhat.com)
- moved skipping of module to specific class (jscotka@redhat.com)
- removed typo in README file (jscotka@redhat.com)
- move xunit log to avocado directory (jscotka@redhat.com)
- typo, redefinig avocado function, it is bad bad bad (jscotka@redhat.com)
- changed to executable (jscotka@redhat.com)
- added scripts to help with taskotron integration (jscotka@redhat.com)
- added scripts to help with taskotron integration (jscotka@redhat.com)
- added scripts to help with taskotron integration (jscotka@redhat.com)
- added simple tests for ngnix (jscotka@redhat.com)
- Typo in version (phracek@redhat.com)
- Bump version (phracek@redhat.com)

* Fri Mar 24 2017 Petr Hracek <phracek@redhat.com> - 0.2.0-1
- New upstream version

* Fri Mar 24 2017 Jan Scotka <jscotka@redhat.com> 0.1.9-1
- 

* Fri Mar 24 2017 Jan Scotka <jscotka@redhat.com> 0.1.8-1
- 

* Fri Mar 24 2017 Jan Scotka <jscotka@redhat.com> 0.1.7-1
- added symlink to testing module to minimal.yaml (jscotka@redhat.com)
- removed source section form minimal config, actually is not anyhow used
  (jscotka@redhat.com)
- imporved docker handling, solved issues with missing labes in config
  (jscotka@redhat.com)
- repaired mistakes caused that MODULE=rpm did not worked (jscotka@redhat.com)
- added setup and cleanup part to config file (before starting module, after
  stopping) - is id done on host (jscotka@redhat.com)
- config improvement, firt commit to be able to disccuss about this
  (jscotka@redhat.com)
- tox file removed to not cause misundertand of project (jscotka@redhat.com)
- improved how it works diagram (jscotka@redhat.com)
- replace try exept with avocado service module (psklenar@masox.brq.redhat.com)
- added setup and test for rpm module for haproxy
  (psklenar@masox.brq.redhat.com)
- added example of simple avocado test (jscotka@redhat.com)
- added :z for selinux (psklenar@masox.brq.redhat.com)
- use port 8077 (psklenar@masox.brq.redhat.com)
- Bump version (phracek@redhat.com)
- repaired behave test (jscotka@redhat.com)

* Mon Mar 20 2017 Jan Scotka <jscotka@redhat.com> 0.1.6-1
- added underline bw words (jscotka@redhat.com)
- added better config handling, and allow use defaultmodule parameter in config
  yaml file (jscotka@redhat.com)
- changed fedora path to public webs (psklenar@masox.brq.redhat.com)
- init of haproxy test (psklenar@masox.brq.redhat.com)
- added explicitly calling start for docker copy functions (jscotka@redhat.com)
- small changes of tox (jscotka@redhat.com)
- added tox file to project for CI (jscotka@redhat.com)
- added tox.ini for CI and improved makefile inside tests for CI
  (jscotka@redhat.com)

* Thu Mar 16 2017 Jan Scotka <jscotka@redhat.com> 0.1.5-1
- added possibility call bash stile in config.yaml (jscotka@redhat.com)
- typo (jscotka@redhat.com)
- added missing egg with ? in spec (jscotka@redhat.com)

* Thu Mar 16 2017 Jan Scotka <jscotka@redhat.com> 0.1.4-1
- removed egg-info (jscotka@redhat.com)
- testing commit (jscotka@redhat.com)

* Wed Mar 15 2017 Jan Scotka <jscotka@redhat.com> 0.1.3-1
- new package built with tito

* Wed Mar 15 2017 Petr Hracek <phracek@redhat.com> - 0.1.2-1
- Release a new version 0.1.2

* Mon Mar 13 2017 Petr Hracek <phracek@redhat.com> - 0.1.1-1
- Release a new version 0.1.1

* Thu Mar 9 2017 Petr Hracek <phracek@redhat.com> - 0.1.0-2
- Renaming package from base to moduleframework
- Wrong dependency to avocado

* Wed Mar 8 2017 Petr Hracek <phracek@redhat.com> - 0.1.0-1
- Initial version

