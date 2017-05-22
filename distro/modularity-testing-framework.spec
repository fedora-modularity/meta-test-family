%global framework_name moduleframework

Name:           modularity-testing-framework
Version:        0.4.29
Release:        1%{?dist}
Summary:        Framework for writing tests for modules and containers

License:        GPLv2+
URL:            https://pagure.io/modularity-testing-framework
Source0:        http://releases.pagure.org/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires:       python2-avocado
Requires:       python2-avocado-plugins-output-html
Requires:       python-netifaces
Requires:       docker

%description
%{summary}.

%prep
%autosetup
# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%py2_build

%install
%py2_install
install -d -p -m 755 %{buildroot}%{_datadir}/%{framework_name}
chmod a+x %{buildroot}%{python_sitelib}/%{framework_name}/{module_framework,generator,bashhelper,setup}.py

%files
%license LICENSE
%doc CHANGELOG
%{_bindir}/moduleframework-cmd
%{_bindir}/modulelint
%{_bindir}/generator
%{python2_sitelib}/moduleframework/
%{python2_sitelib}/modularity_testing_framework-*.egg-info/
%{_datadir}/moduleframework/

%changelog
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

