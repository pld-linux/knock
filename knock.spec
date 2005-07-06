Summary:	Knock - a port-knocking server/client
Summary(pl):	Knock - serwer/klient "port-knocking"
Name:		knock
Version:	0.5
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://zeroflux.org/knock/files/%{name}-%{version}.tar.gz
# Source0-md5:	ca09d61458974cff90a700aba6120891
Source1:	%{name}d.sysconfig
Source2:	%{name}d.init
URL:		http://zeroflux.org/knock/
BuildRequires:	libpcap-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Knock is a port-knocking server/client. Port-knocking is a method
where a server can sniff one of its interfaces for a special "knock"
sequence of port-hits. When detected, it will run a specified event
bound to that port knock sequence. These port-hits need not be on open
ports, since we use libpcap to sniff the raw interface traffic. This
package contains the knock client.

%description -l pl
Knock jest serwerem/klientem nas³uchuj±cym/pukaj±cym do portów. Klient
poprzez próby ³±czenia siê w okre¶lonej kolejno¶ci z odpowiednimi
portami (niekoniecznie otwartymi) powoduje wywo³anie wcze¶niej
okre¶lonej czynno¶ci. Ten pakiet zawiera klienta.

%package server
Summary:	Knock - a port-knocking server/client.
Summary(pl):	Knock - serwer/klient "port-knocking"
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig

%description server
Knock is a port-knocking server/client. Port-knocking is a method
where a server can sniff one of its interfaces for a special "knock"
sequence of port-hits. When detected, it will run a specified event
bound to that port knock sequence. These port-hits need not be on open
ports, since we use libpcap to sniff the raw interface traffic. This
package contains the knockd server.

%description server -l pl
Knock jest serwerem/klientem nas³uchuj±cym/pukaj±cym do portów. Klient
poprzez próby ³±czenia siê w okre¶lonej kolejno¶ci z odpowiednimi
portami (niekoniecznie otwartymi) powoduje wywo³anie wcze¶niej
okre¶lonej czynno¶ci. Ten pakiet zawiera serwer.

%prep
%setup -q

%build
%configure
%{__make}

sed -i 's/^/#/' knockd.conf

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/knockd
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/knockd

%clean
rm -rf $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add knockd
if [ -f /var/lock/subsys/knockd ]; then
        /etc/rc.d/init.d/knockd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/knockd start\" to start knockd daemon."
fi

%preun server
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/knockd ]; then
                /etc/rc.d/init.d/knockd stop 1>&2
        fi
        /sbin/chkconfig --del knockd
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/%{name}.*

%files server
%defattr(644,root,root,755)
%doc README ChangeLog TODO
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%attr(754,root,root) /etc/rc.d/init.d/*
%{_mandir}/man?/%{name}d.*
