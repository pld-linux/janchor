%include	/usr/lib/rpm/macros.perl
Summary:	Janchor - headline delivery for jabber
Name:		janchor
Version:	0.3.9
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://janchor.jabberstudio.org/all_versions/janchor-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-external_config.patch
Url:		http://janchor.jabberstudio.org/
Requires:	jabber
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Janchor polls a series of sources (RSS or RDF file on the web), and, according
to user's interests (individual source subscriptions), forwards those new items
as Jabber messages.

%prep
%setup -q
%patch0 -p1

%build
awk '
BEGIN { config=0; }

/# END [A-Z ]*CONFIGURATION/ { print; config=0; }
	{ if (config==1) print; }
/# BEGIN [A-Z ]*CONFIGURATION/ { print; config=1; }
' janchor.pl > janchor.rc



%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},/etc/rc.d/init.d,/etc/sysconfig,/var/log,/var/lib/janchor}
install janchor.pl $RPM_BUILD_ROOT%{_sbindir}/janchor
install janchor.rc $RPM_BUILD_ROOT%{_sysconfdir}/janchor.rc
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/janchor
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/janchor
touch $RPM_BUILD_ROOT/var/log/janchor.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add janchor
if [ -r /var/lock/subsys/janchor ]; then
       	/etc/rc.d/init.d/janchor restart >&2
else
        echo "Run \"/etc/rc.d/init.d/janchor start\" to start Jabber GaduGadu transport."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/janchor ]; then
		/etc/rc.d/init.d/janchor stop >&2
	fi
	/sbin/chkconfig --del janchor
fi

%files
%defattr(644,root,root,755)
%doc README.html VISION.html
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/janchor.rc
%attr(754,root,root) /etc/rc.d/init.d/janchor
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/janchor
%attr(664,root,jabber) /var/log/janchor.log
%dir %attr(775,root,jabber) /var/lib/janchor
