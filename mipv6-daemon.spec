Name:		mipv6-daemon
Version:	0.4
Release:	10
Summary:	Mobile IPv6 (MIPv6) Daemon
Group:		System/Servers
License:	GPLv2
URL:		https://www.linux-ipv6.org/memo/mipv6/
Source0:	ftp://ftp.linux-ipv6.org/pub/usagi/patch/mipv6/umip-%{version}/daemon/tarball/mipv6-daemon-umip-%{version}.tar.gz
Source1:	mip6d.service
Source2:	mip6d.sysconfig
Source3:	mip6d.conf
Patch0:		mipv6-daemon-header-fix.patch
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	indent

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
%make

%install
%makeinstall_std

install -d %{buildroot}%{_unitdir}
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}/mip6d.service
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/mip6d
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/mip6d.conf

mkdir -p %{buildroot}%{_includedir}/netinet
cp -av include/netinet/ip6mh.h %{buildroot}%{_includedir}/netinet/

%preun
%systemd_preun mip6d.service

%post
%systemd_post mip6d.service

%postun
%systemd_postun_with_restart mip6d.service

%files
%doc AUTHORS BUGS COPYING NEWS README README.IPsec THANKS extras
%{_unitdir}/mip6d.service
%config(noreplace) %{_sysconfdir}/sysconfig/mip6d
%config(noreplace) %{_sysconfdir}/mip6d.conf
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files devel
%{_includedir}/netinet/*.h
