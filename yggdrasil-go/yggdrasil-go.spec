#
# spec file for package yggdrasil-go
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define appname yggdrasil
Name:           yggdrasil-go
Version:        0.5.15
Release:        0
Summary:        End-to-end encrypted IPv6 overlay mesh network
License:        LGPL-3.0-only
Group:          Productivity/Networking/Other
URL:            https://yggdrasil-network.github.io/
Source0:        https://github.com/yggdrasil-network/yggdrasil-go/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# "go mod vendor" of the tag above (OBS builds have no network access)
Source1:        vendor.tar.zst
Source2:        %{name}.sysusers
BuildRequires:  go >= 1.26
BuildRequires:  systemd-rpm-macros
BuildRequires:  sysuser-tools
BuildRequires:  zstd
Requires:       kmod
Provides:       %{appname} = %{version}-%{release}
%{?systemd_requires}
%sysusers_requires

%description
Yggdrasil is an implementation of a fully end-to-end encrypted IPv6
network. It is lightweight, self-arranging, and allows pretty much any
IPv6-capable application to communicate securely with other Yggdrasil
nodes. It does not require IPv6 Internet connectivity; it also works
over IPv4, connecting to public peers or to nodes found on the LAN by
multicast.

The yggdrasil service is not enabled by default. On first start it
generates /etc/yggdrasil.conf (add Peers there), then:
"systemctl enable --now yggdrasil". Members of the yggdrasil group can
use yggdrasilctl through the admin socket without root.

%prep
%autosetup -p1 -a1

%build
%sysusers_generate_pre %{SOURCE2} %{name} %{name}.conf
export CGO_ENABLED=0
for cmd in %{appname} %{appname}ctl; do
  go build -mod=vendor -trimpath -buildmode=pie -v \
    -ldflags "-s -w \
      -X github.com/yggdrasil-network/yggdrasil-go/src/version.buildName=%{appname} \
      -X github.com/yggdrasil-network/yggdrasil-go/src/version.buildVersion=%{version}" \
    -o $cmd ./cmd/$cmd
done

%install
install -Dpm 0755 %{appname}    %{buildroot}%{_bindir}/%{appname}
install -Dpm 0755 %{appname}ctl %{buildroot}%{_bindir}/%{appname}ctl
for u in %{appname} %{appname}-default-config; do
  sed 's|/sbin/modprobe|%{_sbindir}/modprobe|' contrib/systemd/$u.service \
    > $u.service
  install -Dpm 0644 $u.service %{buildroot}%{_unitdir}/$u.service
done
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
mkdir -p %{buildroot}%{_sbindir}
ln -s service %{buildroot}%{_sbindir}/rc%{appname}
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/%{appname}.conf

%check
./%{appname} -version | grep -F %{version}
./%{appname} -genconf > test.conf
./%{appname} -useconffile test.conf -normaliseconf > /dev/null
go test -mod=vendor ./src/...

%pre -f %{name}.pre
%service_add_pre %{appname}.service %{appname}-default-config.service

%post
%service_add_post %{appname}.service %{appname}-default-config.service

%preun
%service_del_preun %{appname}.service %{appname}-default-config.service

%postun
%service_del_postun %{appname}.service %{appname}-default-config.service

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/%{appname}
%{_bindir}/%{appname}ctl
%{_sbindir}/rc%{appname}
%{_unitdir}/%{appname}.service
%{_unitdir}/%{appname}-default-config.service
%{_sysusersdir}/%{name}.conf
%ghost %config(noreplace) %attr(0640,root,%{appname}) %{_sysconfdir}/%{appname}.conf

%changelog
