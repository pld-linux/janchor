%include	/usr/lib/rpm/macros.perl
Summary:	Janchor - headline delivery for Jabber
Summary(pl):	Janchor - dostarczanie skrótów wiadomo¶ci do Jabbera
Name:		janchor
Version:	0.3.9
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://janchor.jabberstudio.org/all_versions/%{name}-%{version}.tar.gz
# Source0-md5:	3facec92cb34c0e4609c345990a411bd
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-external_config.patch
Patch1:		%{name}-restrict.patch
Patch2:		%{name}-unicode.patch
Patch3:		%{name}-default_config.patch
Patch4:		%{name}-presence_type_available.patch
URL:		http://janchor.jabberstudio.org/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	daemon
Requires:	jabber-common
Requires:	rc-scripts
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Janchor polls a series of sources (RSS or RDF file on the web), and,
according to user's interests (individual source subscriptions),
forwards those new items as Jabber messages.

%description -l pl
Janchor odczytuje szereg ¼róde³ (plików RSS lub RDF w sieci) i,
zgodnie z zainteresowaniami u¿ytkownika (indywidualn± prenumerat±),
przekierowuje te nowe wiadomo¶ci jako wiadomo¶ci Jabbera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

awk '
BEGIN { config=0; }

/# END [A-Z ]*CONFIGURATION/ { print; config=0; }
	{ if (config==1) print; }
/# BEGIN [A-Z ]*CONFIGURATION/ { print; config=1; }
' janchor.pl > janchor.rc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,%{_sbindir}} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,/var/log,/var/lib/janchor}

install janchor.pl $RPM_BUILD_ROOT%{_sbindir}/janchor
install janchor.rc $RPM_BUILD_ROOT%{_sysconfdir}/jabber/janchor.rc
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/janchor
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/janchor
touch $RPM_BUILD_ROOT/var/log/janchor.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in janchor.rc..."
		%{__sed} -i -e "s/'secret'/'$SECRET'/" /etc/jabber/janchor.rc
	fi
fi

/sbin/chkconfig --add janchor
%service janchor restart "Janchor"

%preun
if [ "$1" = "0" ]; then
	%service janchor stop
	/sbin/chkconfig --del janchor
fi

%files
%defattr(644,root,root,755)
%doc README.html VISION.html
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/janchor.rc
%attr(754,root,root) /etc/rc.d/init.d/janchor
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/janchor
%attr(664,root,jabber) /var/log/janchor.log
%dir %attr(775,root,jabber) /var/lib/janchor
