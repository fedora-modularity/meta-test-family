%global framework_name moduleframework

Name:           modularity-testing-framework
Version:        0.3.6
Release:        1%{?dist}
Summary:        Framework for writing tests for modules and containers

License:        GPLv2+
URL:            https://pagure.io/modularity-testing-framework
Source0:        http://releases.pagure.org/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2-avocado
Requires:       python2-avocado-plugins-output-html
Requires:       python-netifaces
Requires:       docker


%description
Framework for writing tests for modules and containers

%prep
%setup -q -n %{name}-%{version}
# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
install -d -m 755 %{buildroot}%{_datadir}/%{framework_name}
chmod a+x %{buildroot}%{python_sitelib}/%{framework_name}/{module_framework,generator,bashhelper,setup}.py

%files
%license LICENSE
%doc CHANGELOG
%{_bindir}/moduleframework-cmd
%{_bindir}/modulelint
%{_bindir}/generator
%{python2_sitelib}/moduleframework
%{python2_sitelib}/modularity_testing_framework-?.?.*-py?.?.egg-info
%{_datadir}/moduleframework


%changelog
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

