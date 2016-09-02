%global pypi_name congress

%if 0%{?fedora}
%global with_python3 1
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{pypi_name}
Version:        3.0.0
Release:        1%{?dist}
Summary:        OpenStack Congress Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        openstack-congress-server.service
Source2:        openstack-congress-db-manage.service
Source3:        congress.logrotate

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-oslo-config >= 3.7.0
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-oslo-middleware
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-service
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  systemd

Requires: pulp-rpm >= 1.0.4
Requires: python-alembic >= 0.8.0
Requires: python-babel >= 1.3
Requires: python-dateutil >= 2.4.2
Requires: python-eventlet >= 0.18.2
Requires: python-ceilometerclient >= 2.2.1
Requires: python-cinderclient >= 1.3.1
Requires: python-glanceclient >= 2.0.0
Requires: python-heatclient >= 0.6.0
Requires: python-keystoneclient >= 1.6.0
Requires: python-keystonemiddleware >= 4.0.0
Requires: python-muranoclient >= 0.8.2
Requires: python-neutronclient >= 2.6.0
Requires: python-novaclient >= 2.29.0
Requires: python-oslo-config >= 3.7.0
Requires: python-oslo-context >= 0.2.0
Requires: python-oslo-db >= 4.1.0
Requires: python-oslo-log >= 1.14.0
Requires: python-oslo-messaging >= 4.0.0
Requires: python-oslo-middleware >= 3.0.0
Requires: python-oslo-policy >= 0.5.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-service >= 1.0.0
Requires: python-oslo-utils >= 3.5.0
Requires: python-oslo-vmware >= 1.16.0
Requires: python-paste
Requires: python-paste-deploy >= 1.5.0
Requires: python-pbr >= 1.6
Requires: python-routes >= 1.12.3
Requires: python-six >= 1.9.0
Requires: python-swiftclient >= 2.2.0
Requires: python-webob >= 1.2.3
Requires: %{name}-doc = %{version}-%{release}
 
%description
Support of Congress for OpenStack.

%package -n     python2-%{pypi_name}
Summary:        OpenStack Congress Service
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
OpenStack Congress Service is an open policy framework for OpenStack

# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        OpenStack Congress Service
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-oslo-config >= 3.7.0
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslo-service
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6
BuildRequires:  python-tools

Requires: pulp-rpm >= 1.0.4
Requires: python3-alembic >= 0.8.0
Requires: python3-babel >= 1.3
Requires: python3-dateutil >= 2.4.2
Requires: python3-eventlet >= 0.18.2
Requires: python3-ceilometerclient >= 2.2.1
Requires: python3-cinderclient >= 1.3.1
Requires: python3-glanceclient >= 2.0.0
Requires: python3-heatclient >= 0.6.0
Requires: python3-keystoneclient >= 1.6.0
Requires: python3-keystonemiddleware >= 4.0.0
Requires: python3-muranoclient >= 0.8.2
Requires: python3-neutronclient >= 2.6.0
Requires: python3-novaclient >= 2.29.0
Requires: python3-oslo-config >= 3.7.0
Requires: python3-oslo-context >= 0.2.0
Requires: python3-oslo-db >= 4.1.0
Requires: python3-oslo-log >= 1.14.0
Requires: python3-oslo-messaging >= 4.0.0
Requires: python3-oslo-middleware >= 3.0.0
Requires: python3-oslo-policy >= 0.5.0
Requires: python3-oslo-serialization >= 1.10.0
Requires: python3-oslo-service >= 1.0.0
Requires: python3-oslo-utils >= 3.5.0
Requires: python3-oslo-vmware >= 1.16.0
Requires: python3-paste
Requires: python3-paste-deploy >= 1.5.0
Requires: python3-pbr >= 1.6
Requires: python3-routes >= 1.12.3
Requires: python3-six >= 1.9.0
Requires: python3-swiftclient >= 2.2.0
Requires: python3-webob >= 1.2.3
Requires: %{name}-doc = %{version}-%{release}

%description -n python3-%{pypi_name}
OpenStack Congress Service is an open policy framework for OpenStack
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress service

BuildRequires:  python-sphinx

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Congress service

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif

%build
%{__python2} setup.py build

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip heat's entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/congress-config-generator.conf --output-file=./etc/congress.conf

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/%{pypi_name}-server %{buildroot}%{_bindir}/python3-%{pypi_name}-server
mv %{buildroot}%{_bindir}/%{pypi_name}-db-manage %{buildroot}%{_bindir}/python3-%{pypi_name}-db-manage
popd
%endif

# rename binaries, make compat symlinks
pushd %{buildroot}%{_bindir}
%if 0%{?with_python3}
for i in %{pypi_name}-{3,%{?python3_shortver}}; do
    ln -s  python3-%{pypi_name} $i
done
%endif
popd

# Install data file
install -p -D -m 640 etc/api-paste.ini %{buildroot}%{_sysconfdir}/congress/api-paste.ini
install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/congress/policy.json
install -p -D -m 640 etc/congress.conf %{buildroot}%{_sysconfdir}/congress/congress.conf

# Install services
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-congress-server.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-congress-db-manage.service

# Install log file
install -d -m 755 %{buildroot}%{_localstatedir}/log/congress

# Install logrotate
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-congress


%pre
# 1777:1777 for congress
getent group congress >/dev/null || groupadd -r --gid 1777 congress
getent passwd congress >/dev/null || \
useradd --uid 1777 -r -g congress -d %{_sharedstatedir}/congress -s /sbin/nologin \
-c "OpenStack Congress Daemons" congress
exit 0


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/antlr3runtime*
%{python2_sitelib}/congress*

%files
%{_bindir}/%{pypi_name}*
%dir %attr(0750, root, congress) %{_sysconfdir}/congress
%attr(0644, root, congress) %{_sysconfdir}/congress/api-paste.ini
%attr(0644, root, congress) %{_sysconfdir}/congress/policy.json
%attr(0644, root, congress) %{_sysconfdir}/congress/congress.conf
%{_unitdir}/openstack-congress-server.service
%{_unitdir}/openstack-congress-db-manage.service
%dir %attr(0750, congress, congress) %{_localstatedir}/log/congress
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-congress

# Files for python3
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/python3-%{pypi_name}
%{_bindir}/%{pypi_name}*
%{python3_sitelib}/antlr3runtime*
%{python3_sitelib}/congress*
%endif


%files -n python-%{pypi_name}-doc
%doc html


%changelog
* Fri Apr 15 2016 Marcos Fermin Lobo <marcos.fermin.lobo@cern.ch> - 3.0.0-1
- First RPM


