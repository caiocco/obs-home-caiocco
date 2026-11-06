#
# spec file for package dillo
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           dillo
Version:        3.3.0
Release:        0
Summary:        Small and fast graphical web browser
License:        GPL-3.0-or-later
Group:          Productivity/Networking/Web/Browsers
URL:            https://dillo-browser.org/
Source0:        https://dillo-browser.org/release/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  desktop-file-utils
BuildRequires:  fltk-devel >= 1.3
BuildRequires:  gcc-c++
BuildRequires:  giflib-devel
BuildRequires:  hicolor-icon-theme
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
Requires:       ca-certificates
Recommends:     wget

%description
Dillo is a minimalistic graphical web browser built with the FLTK
toolkit. It is fast, has a small memory footprint and does not run
JavaScript, which makes it well suited for old or low-end machines and
for privacy-conscious browsing.

Features include tabbed browsing, HTTPS (OpenSSL), cookies with
per-domain rules, HSTS, images (PNG, JPEG, GIF, WebP and SVG), brotli
encoding, bookmarks and a downloads manager implemented as DPI plugins,
and the dilloc program to control the browser from scripts.

%prep
%autosetup
sed -i '1s|^#!/usr/bin/env perl|#!/usr/bin/perl|' dillo-install-hyphenation

%build
%configure \
  --docdir=%{_docdir}/%{name} \
  --enable-ipv6 \
  --enable-tls \
  --enable-openssl \
  --disable-mbedtls \
  --with-ca-certs-file=%{_sysconfdir}/ssl/ca-bundle.pem \
  --with-ca-certs-dir=%{_sysconfdir}/ssl/certs
%make_build

%check
%make_build check

%install
%make_install
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
# The help page is shipped with %%doc in the same directory, where the
# Help button looks for it (DILLO_DOCDIR)
rm -rf %{buildroot}%{_docdir}/%{name}

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md doc/Cookies.txt
%doc doc/user_help.html
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/dillorc
%config(noreplace) %{_sysconfdir}/%{name}/dpidrc
%config(noreplace) %{_sysconfdir}/%{name}/domainrc
%config(noreplace) %{_sysconfdir}/%{name}/keysrc
%config %{_sysconfdir}/%{name}/hsts_preload
%{_bindir}/dillo
%{_bindir}/dilloc
%{_bindir}/dillo-install-hyphenation
%{_bindir}/dpid
%{_bindir}/dpidc
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/dillo.1%{?ext_man}

%changelog
