#
# spec file for package moxfm
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define mx_commit   e81d6c2d7c118a405992666692d51c927f2d7355
%define mx_short    e81d6c2
%define mx_date     20260915
%define mx_datadir  %{_datadir}/%{name}

Name:           moxfm
Version:        1.0.1+git%{mx_date}.%{mx_short}
Release:        0
Summary:        Motif version of the X File Manager (xfm)
License:        GPL-2.0-or-later
Group:          Productivity/File utilities
URL:            https://github.com/ThomasAdam/moxfm
Source0:        https://github.com/ThomasAdam/moxfm/archive/%{mx_commit}.tar.gz#/%{name}-%{mx_commit}.tar.gz
Source1:        %{name}.desktop
# PATCH-FIX-UPSTREAM moxfm-install-destdir.patch -- install data files under DESTDIR
Patch0:         moxfm-install-destdir.patch
# PATCH-FEATURE-OPENSUSE moxfm-xft-fonts.patch -- render text with Xft; keep CDE's *Font from overriding it
Patch1:         moxfm-xft-fonts.patch
# PATCH-FEATURE-OPENSUSE moxfm-modern-defaults.patch -- replace vanished programs in the default config, freedesktop trash, magic for PNG/PDF/Exif
Patch2:         moxfm-modern-defaults.patch
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  imake
BuildRequires:  make
BuildRequires:  motif-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xt)
Requires:       glib2-tools
Requires:       xterm
Suggests:       gv
Suggests:       mupdf
Suggests:       nedit
Suggests:       ximaging

%description
Moxfm is a file and application manager for X11 built with the Motif
toolkit. It was written by Oliver Mai in 1995 as a Motif port of xfm
1.3.2 and extended with desktop icons, several application windows,
background copying, file monitoring, a mount table window and ICCCM
drag and drop between applications.

This package follows Thomas Adam's maintained repository.

%prep
%autosetup -p1 -n %{name}-%{mx_commit}
# The sample mail monitor points at the old X11 lib directory
sed -i 's|/usr/lib/X11/moxfm/checkmail|%{_libexecdir}/%{name}/checkmail|' lib/xfmmon

%build
xmkmf -a
%make_build \
  CDEBUGFLAGS="%{optflags}" \
  EXTRA_LDOPTIONS="%{?build_ldflags}" \
  XFMLIBDIR=%{mx_datadir} \
  PIXMAPDIR=%{mx_datadir}/pixmaps \
  BITMAPDIR=%{mx_datadir}/bitmaps

%install
make install install.man DESTDIR=%{buildroot} \
  XFMLIBDIR=%{mx_datadir} \
  PIXMAPDIR=%{mx_datadir}/pixmaps \
  BITMAPDIR=%{mx_datadir}/bitmaps \
  INSTDATFLAGS="-m 0644" INSTMANFLAGS="-m 0644" INSTAPPFLAGS="-m 0644" \
  MANSUFFIX=1 MANDIR=%{_mandir}/man1
# dot.moxfm is copied to ~/.moxfm on first start; the sample mail
# checker is a script, so it goes to libexec
install -d %{buildroot}%{_libexecdir}/%{name}
mv %{buildroot}%{mx_datadir}/checkmail %{buildroot}%{_libexecdir}/%{name}/
chmod 0755 %{buildroot}%{_libexecdir}/%{name}/checkmail
install -d %{buildroot}%{_datadir}/pixmaps
ln -s ../%{name}/pixmaps/fileman.xpm %{buildroot}%{_datadir}/pixmaps/%{name}.xpm
install -Dm 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license COPYING
%doc ChangeLog README README.moxfm-xfm README.xfm-1.3 BUGS TODO
%{_bindir}/%{name}
%dir %{_datadir}/X11/app-defaults
%{_datadir}/X11/app-defaults/Moxfm
%{mx_datadir}
%{_libexecdir}/%{name}
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1%{?ext_man}

%changelog
