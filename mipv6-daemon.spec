Name:		mipv6-daemon
Version:	0.4
Release:	%mkrel 6
Summary:	Mobile IPv6 (MIPv6) Daemon

Group:		System/Servers
License:	GPLv2
URL:		http://www.linux-ipv6.org/memo/mipv6/
Source0:	ftp://ftp.linux-ipv6.org/pub/usagi/patch/mipv6/umip-%{version}/daemon/tarball/mipv6-daemon-umip-%{version}.tar.gz
Source1:	mip6d.init
Source2:	mip6d.sysconfig
Source3:	mip6d.conf
Patch0:		mipv6-daemon-header-fix.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	flex bison indent
Requires:	initscripts, chkconfig

%description
The mobile IPv6 daemon allows nodes to remain
reachable while moving around in the IPv6 Internet.

%package devel
Group:	Development/Other
Summary:	Mobile IPv6 (MIPv6) header files

%description devel
Mobile IPv6 (MIPv6) header files

%prep
%setup -q -n mipv6-daemon-umip-%{version}
%patch0 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_initrddir}
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/mip6d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mip6d
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/mip6d.conf

mkdir -p $RPM_BUILD_ROOT%{_includedir}/netinet
cp -av include/netinet/ip6mh.h $RPM_BUILD_ROOT%{_includedir}/netinet/

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ "$1" = 0 ]
then
	/sbin/service mip6d stop > /dev/null 2>&1 ||:
	/sbin/chkconfig --del mip6d
fi

%post
/sbin/chkconfig --add mip6d

%postun
if [ "$1" -ge "1" ]; then
	/sbin/service mip6d condrestart > /dev/null 2>&1 ||:
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING NEWS README README.IPsec THANKS extras
%{_initrddir}/mip6d
%config(noreplace) %{_sysconfdir}/sysconfig/mip6d
%config(noreplace) %{_sysconfdir}/mip6d.conf
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files devel
%{_includedir}/netinet/*.h



%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4-6mdv2011.0
+ Revision: 612871
- the mass rebuild of 2010.1 packages

* Mon Feb 22 2010 Antoine Ginies <aginies@mandriva.com> 0.4-5mdv2010.1
+ Revision: 509533
- change group for devel package
- change the group
- spec file based on fedora one
- import mipv6-daemon


