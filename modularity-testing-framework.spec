%global framework_name moduleframework

Name:           modularity-testing-framework
Version:        0.2.5
Release:        1%{?dist}
Summary:        Framework for writing tests for modules and containers

License:        GPLv2+
URL:            https://pagure.io/modularity-testing-framework
Source0:        http://releases.pagure.org/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2-avocado
Requires:       docker
Requires:       docker-distribution

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
%{python2_sitelib}/modularity_testing_framework-?.?.?-py?.?.egg-info
%{_datadir}/moduleframework


%changelog
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

