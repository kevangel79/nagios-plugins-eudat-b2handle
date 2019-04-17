Name:		nagios-plugins-eudat-b2handle
Version:	0.7
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

Requires:	python2-pip

%description
Nagios probes to check functionality of Handle service and EPIC API

%prep
%setup -q

%define _unpackaged_files_terminate_build 0 

%install

install -d %{buildroot}/%{_libexecdir}/argo-monitoring/probes/eudat-b2handle
install -d %{buildroot}/%{_sysconfdir}/nagios/plugins/eudat-b2handle
install -m 755 check_handle_resolution.pl %{buildroot}/%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/check_handle_resolution.pl
install -m 755 check_epic_api.py %{buildroot}/%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/check_epic_api.py
install -m 644 epicclient.py %{buildroot}%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/epicclient.py
install -m 644 check_handle_api.py %{buildroot}%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/check_handle_api.py

%files
%dir /%{_libexecdir}/argo-monitoring
%dir /%{_libexecdir}/argo-monitoring/probes/
%dir /%{_libexecdir}/argo-monitoring/probes/eudat-b2handle
%dir /%{_sysconfdir}/nagios/plugins/eudat-b2handle

%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/check_handle_resolution.pl
%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/check_epic_api.py
%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/epicclient.py
%attr(0644,root,root) /%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/epicclient.pyc
%attr(0644,root,root) /%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/epicclient.pyo
%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/eudat-b2handle/check_handle_api.py
%attr(0755,root,root) /%{_sysconfdir}/nagios/plugins/eudat-b2handle

%pre
pip install b2handle

%changelog
* Thu Jan 17 2019 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.7-1
- check_handle_resolution.pl : Updated version that works with HS_SERV values
* Thu Oct 4 2018 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.6-1
- Add configuration directory /etc/nagios/plugins/
* Thu Jan 12 2017 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.5-1
- Add check_handle_api.py probe for Handle v8 REST API
- Change installation directory name to eudat-b2handle
* Wed Feb 3 2016 Christos Kanellopoulos <skanct@gmail.com> - 0.4-1
- New package version
* Fri Jan 15 2016 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 0.1-1
- Initial version of the package
