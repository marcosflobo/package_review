%global pypi_name PuLP


%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

%if 0%{?fedora}
%global with_python3 1
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

%define _binaries_in_noarch_packages_terminate_build 0

# Avoid exit error due to debug files
%define _unpackaged_files_terminate_build 0

Name:		python-%{pypi_name}
Version:	1.6.1
Release:	1%{?dist}
Summary:	LP modeler written in python.

License:	ASL 2.0
URL:		https://pypi.python.org/pypi/PuLP
Source0:	https://pypi.io/packages/source/P/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:	noarch

%description
PuLP is an LP modeler written in python. PuLP can generate MPS or LP files
and call GLPK[1], COIN CLP/CBC[2], CPLEX[3], and GUROBI[4] to solve linear
problems.



%package -n	python2-%{pypi_name}

BuildRequires:	python2-devel
BuildRequires:	python-setuptools
BuildRequires:	python-pbr

Requires:	python-pyparsing >= 2.0.0

Summary:	LP modeler written in python.
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
PuLP is an LP modeler written in python. PuLP can generate MPS or LP files
and call GLPK[1], COIN CLP/CBC[2], CPLEX[3], and GUROBI[4] to solve linear
problems.



# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        LP modeler written in python.
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6

Requires:       python3-pyparsing >= 2.0.0

%description -n python3-%{pypi_name}
PuLP is an LP modeler written in python. PuLP can generate MPS or LP files
and call GLPK[1], COIN CLP/CBC[2], CPLEX[3], and GUROBI[4] to solve linear
problems.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf src/%{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt


%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%py2_build

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif

%install
%py2_install

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

# rename binaries, make compat symlinks
install -m 755 -d %{buildroot}/%{_bindir}
pushd %{buildroot}%{_bindir}
ln -s %{pypi_name} %{pypi_name}
for i in %{pypi_name}-{2,%{?python2_shortver}}; do
    ln -s %{pypi_name} $i
done
%if 0%{?with_python3}
for i in %{pypi_name}-{3,%{?python3_shortver}}; do
    ln -s  python3-%{pypi_name} $i
done
%endif
popd

%files -n python2-%{pypi_name}
%license LICENSE
%{_bindir}/pulp*
%{_bindir}/%{pypi_name}*
%{python2_sitelib}/pulp*
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

# Files for python3
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%{_bindir}/pulp*
%{python3_sitelib}/pulp*
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif


%changelog
* Tue Sep 6 2016 Marcos Fermin Lobo <lobo@lukos.org> - 1.6.1-1
- First RPM

