%global pypi_name PuLP


Name:		python-%{pypi_name}
Version:	1.6.1
Release:	1%{?dist}
Summary:	LP modeler written in python.

License:	ASL 2.0
URL:		https://pypi.python.org/pypi/PuLP
Source0:	https://pypi.python.org/packages/2f/3d/4316c6145ff84620a5aee571b63f192a9974c1b513269291cc8df5f72124/PuLP-%{version}.tar.gz

BuildArch:	noarch

%define _binaries_in_noarch_packages_terminate_build 0

BuildRequires:	python2-devel
BuildRequires:	python-setuptools
BuildRequires:	python-pbr
BuildRequires:	python-sphinx

Requires:	python-pyparsing >= 2.0.0

%description
PuLP is an LP modeler written in python. PuLP can generate MPS or LP files
and call GLPK[1], COIN CLP/CBC[2], CPLEX[3], and GUROBI[4] to solve linear
problems.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf src/%{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt

%build
%py2_build

%install
%py2_install

%files
%{_bindir}/pulp*
%{python2_sitelib}/pulp*
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
/usr/lib/debug*
%license LICENSE


%changelog
* Tue Sep 6 2016 Marcos Fermin Lobo <lobo@lukos.org> - 1.6.1-1
- First RPM

