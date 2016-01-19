Name:		nagios-b2handle-probes
Version:	0.2
Release:	1%{?dist}
Summary:	Nagios B2HANDLE probes
License:	GPLv3+
Packager:	Kyriakos Gkinis <kyrginis@admin.grnet.gr>

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

Requires:	python
Requires:	python-argparse
Requires:	python-lxml
Requires:	python-simplejson
Requires:	perl
Requires:	perl-JSON

Requires:	python-defusedxml
Requires:	python-httplib2

%description
Nagios probes to check functionality of Handle service and EPIC API

%prep
%setup -q

%install

install -d %{buildroot}/%{_libexecdir}/argo-monitoring/probes/%{name}
install -m 755 check_handle_resolution.pl %{buildroot}/%{_libexecdir}/argo-monitoring/probes/%{name}/check_handle_resolution.pl
install -m 755 check_epic_api.py %{buildroot}/%{_libexecdir}/argo-monitoring/probes/%{name}/check_epic_api.py
install -m 644 epicclient.py %{buildroot}%{_libexecdir}/argo-monitoring/probes/%{name}/epicclient.py

%files
%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/check_handle_resolution.pl
%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/check_epic_api.py
%attr(0644,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/check_epic_api.pyc
%attr(0644,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/check_epic_api.pyo
%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/epicclient.py
%attr(0644,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/epicclient.pyc
%attr(0644,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/epicclient.pyo

%changelog
* Fri Jan 15 2016 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.1-1
- Initial version of the package
