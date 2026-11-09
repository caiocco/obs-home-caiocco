#
# spec file for package xfile
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define xf_commit   ab96ebd4027504def1aacd656a2f5637889b9781
%define xf_short    ab96ebd
%define xf_date     20260914

Name:           xfile
Version:        1.2.1+git%{xf_date}.%{xf_short}
Release:        0
Summary:        File manager for X11 based on Motif
License:        MIT
Group:          Productivity/File utilities
URL:            https://fastestcode.org/xfile.html
Source0:        https://github.com/alx210/xfile/archive/%{xf_commit}.tar.gz#/%{name}-%{xf_commit}.tar.gz
Source1:        %{name}.desktop
# PATCH-FIX-UPSTREAM xfile-cde-font-resource.patch -- reload Xft renditions clobbered by CDE's global *Font resource (crash in XmStringWidth)
Patch0:         xfile-cde-font-resource.patch
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  motif-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xt)
Suggests:       xterm
Suggests:       xedit

%description
XFile is a file manager for Unix/X11 built with the Motif toolkit.
It provides directory browsing with icon and detailed list views,
a path bar, file operations with progress reporting, mounting of
file systems listed in fstab, a user-extensible file type database
that associates actions with file types, and an xfile-open command
that opens files according to that database.

%prep
%autosetup -p1 -n %{name}-%{xf_commit}
ln -s ../mf/Makefile.Linux src/Makefile
sed -i \
  -e 's|^CFLAGS = .*|CFLAGS = %{optflags} -Wall|' \
  -e 's|^INCDIRS = .*|INCDIRS =|' \
  -e 's|^LIBDIRS = .*|LIBDIRS =|' \
  mf/Makefile.Linux
# Unprivileged install; the xfile-open symlink is created in %%install
sed -i \
  -e 's|install -o 0 -g 0 |install |' \
  -e 's|-m 664 |-m 644 |' \
  -e '/ln -s .*xfile-open/d' \
  src/common.mf

%build
%make_build -C src \
  LDFLAGS="%{optflags} %{?build_ldflags}"

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_datadir}/pixmaps
# PREFIX is only overridden at install time; the binary keeps /usr
%make_install -C src \
  PREFIX=%{buildroot}%{_prefix} \
  MANDIR=%{buildroot}%{_mandir} \
  SHAREDIR=%{buildroot}%{_datadir}/%{name} \
  APPLRESDIR=%{buildroot}%{_datadir}/X11/app-defaults
ln -s xfile %{buildroot}%{_bindir}/xfile-open
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license COPYING
%doc README
%{_bindir}/xfile
%{_bindir}/xfile-open
%dir %{_datadir}/X11/app-defaults
%{_datadir}/X11/app-defaults/XFile
%{_datadir}/%{name}
%{_datadir}/pixmaps/xfile_48x48.xpm
%{_datadir}/pixmaps/xfile_64x64.xpm
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/xfile.1%{?ext_man}

%changelog
