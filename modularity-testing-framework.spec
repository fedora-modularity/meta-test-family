Name:           modularity-testing-framework
<<<<<<< 666ec4aae76e06b97b3d7675f29ff1b180a6a50d
Version:        0.1
Release:        2%{?dist}
||||||| merged common ancestors
Version:        0.1
Release:        1%{?dist}
=======
Version:        0.1.0
Release:        2%{?dist}
>>>>>>>  Rename base to moduleframework
Summary:        Framework for writing tests for modules and containers

License:        GPLv2+
URL:            https://pagure.io/modularity-testing-framework
Source0:        https://pagure.io/modularity-testing-framework/%{name}/%{version}.tar.gz
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
install -d -m 755 %{buildroot}%{_datadir}/moduleframework

%files
%license LICENSE
%doc CHANGELOG
%{_bindir}/moduleframework-cmd
%{python2_sitelib}/moduleframework
%{_bindir}/modulelint
%{_bindir}/generator
%{python2_sitelib}/moduleframework
>>>>>>>  Rename base to moduleframework
%{python2_sitelib}/modularity_testing_framework-%{version}-py?.?.egg-info
%{_datadir}/moduleframework


%changelog
* Wed Mar 9 2017 Petr Hracek <phracek@redhat.com> - 0.1.0-2
- Renaming package from base to moduleframework
- Wrong dependency to avocado

* Wed Mar 8 2017 Petr Hracek <phracek@redhat.com> - 0.1.0-1
- Initial version

