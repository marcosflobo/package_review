%global pypi_name PuLP

Name:           python-%{pypi_name}
Version:        1.6.1
Release:        1%{?dist}
Summary:        LP modeler written in Python

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/PuLP
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{pypi_name}; echo ${n:0:1})/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%global _description \
PuLP is an LP modeler written in python. PuLP can generate MPS or LP files\
and call GLPK, COIN CLP/CBC, CPLEX, and GUROBI to solve linear problems.

%description %{_description}

%package -n	python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
Requires:       python2-pyparsing

%description -n python2-%{pypi_name} %{_description}

#Python 2 version.

%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
Requires:       python3-pyparsing

%description -n python3-%{pypi_name} %{_description}

#Python 3 version.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf src/%{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%files -n python2-%{pypi_name}
%license LICENSE
%{python2_sitelib}/pulp/
%{python2_sitelib}/%{pypi_name}-*.egg-info/

%files -n python3-%{pypi_name}
%license LICENSE
%{python3_sitelib}/pulp/
%{python3_sitelib}/%{pypi_name}-*.egg-info/

%{_bindir}/pulp

%changelog
* Tue Sep 27 2016 Marcos Fermin Lobo <lobo@lukos.org> - 1.6.1-1
- First RPM

