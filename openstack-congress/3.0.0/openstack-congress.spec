%global pypi_name congress

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

Requires: python-%{pypi_name} = %{version}-%{release}
Requires: python-%{pypi_name}-doc = %{version}-%{release}

%description
Support of Congress for OpenStack.

%package -n     python2-%{pypi_name}
Summary:        OpenStack Congress Service
%{?python_provide:%python_provide python2-%{pypi_name}}

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

%description -n python2-%{pypi_name}
OpenStack Congress Service is an open policy framework for OpenStack

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

%build
%py2_build

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip heat's entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/congress-config-generator.conf --output-file=./etc/congress.conf

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install

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

%post
%systemd_post openstack-congress-server.service

%preun
%systemd_preun openstack-congress-server.service

%postun
%systemd_postun_with_restart openstack-congress-server.service

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



%files -n python-%{pypi_name}-doc
%doc html


%changelog
* Fri Sep 2 2016 Marcos Fermin Lobo <lobo@lukos.org> - 3.0.0-1
- First RPM


