%global pypi_name vitrageclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        1.0.1
Release:        1%{?dist}
Summary:        Python client for Virage REST API

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        http://pypi.python.org/packages/source/v/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Python client for Vitrage REST API. Includes python library for Vitrage API
and Command Line Interface (CLI) library.


%package -n     python2-%{pypi_name}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

Requires:       python2-babel >= 2.3.4
Requires:       python2-cliff >= 1.15.0
Requires:       python2-keystoneauth1 >= 2.10.0
Requires:       python-pbr
Requires:       python2-oslo-utils >= 3.16.0

Summary:        Python client for Vitrage REST API
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Python client for Vitrage REST API. Includes python library for Vitrage API
and Command Line Interface (CLI) library.


# Python3 package
%package -n     python3-%{pypi_name}
Summary:        Python client for Vitrage REST API
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6

Requires:       python3-babel >= 2.3.4
Requires:       python3-cliff >= 1.15.0
Requires:       python3-keystoneauth1 >= 2.10.0
Requires:       python3-pbr
Requires:       python3-oslo-utils >= 3.16.0

%description -n python3-%{pypi_name}
Python client for Vitrage REST API. Includes python library for Vitrage API
and Command Line Interface (CLI) library.


# Documentation package
%package -n python-%{pypi_name}-doc
Summary:       Documentation for python client for Vitrage REST API

BuildRequires: python-sphinx
BuildRequires: python2-oslo-sphinx >= 2.3.0

%description -n python-%{pypi_name}-doc
Documentation for python client for Vitrage REST API. Includes python library
for Vitrage API and Command Line Interface (CLI) library.


%prep
%autosetup -n %{name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt


%build
%py2_build
%py3_build

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%py2_install
%py3_install


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info 
%{_bindir}/vitrage*
/usr/share/vitrage*

# Files for python3
%files -n python3-%{pypi_name} 
%license LICENSE
%doc README.rst
%{_bindir}/vitrage*
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-%{version}-py?.?.egg-info

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE


%changelog
* Tue Sep 27 2016 Marcos Fermin Lobo <lobo@lukos.org> 1.0.1
- First RPM

