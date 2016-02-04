Name:		nagios-plugins-eudat-b2handle
Version:	0.4
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

%define _unpackaged_files_terminate_build 0 

%install

install -d %{buildroot}/%{_libexecdir}/argo-monitoring/probes/%{name}
install -m 755 check_handle_resolution.pl %{buildroot}/%{_libexecdir}/argo-monitoring/probes/%{name}/check_handle_resolution.pl
install -m 755 check_epic_api.py %{buildroot}/%{_libexecdir}/argo-monitoring/probes/%{name}/check_epic_api.py
install -m 644 epicclient.py %{buildroot}%{_libexecdir}/argo-monitoring/probes/%{name}/epicclient.py

%files
%dir /%{_libexecdir}/argo-monitoring
%dir /%{_libexecdir}/argo-monitoring/probes/
%dir /%{_libexecdir}/argo-monitoring/probes/%{name}

%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/check_handle_resolution.pl
%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/check_epic_api.py
%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/epicclient.py
%attr(0644,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/epicclient.pyc
%attr(0644,root,root) /%{_libexecdir}/argo-monitoring/probes/%{name}/epicclient.pyo

%changelog
* Wed Feb 3 2016 Christos Kanellopoulos <skanct@gmail.com> - 0.4-1
- New package version
* Fri Jan 15 2016 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.1-1
- Initial version of the package
