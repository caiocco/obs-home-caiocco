#
# spec file for package siag
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           siag
Version:        3.6.1
Release:        0
Summary:        Siag Office: spreadsheet, word processor, animator and tools for X11
License:        GPL-2.0-or-later AND LGPL-2.0-or-later AND MIT
Group:          Productivity/Office/Suite
URL:            https://siag.nu/
Source0:        https://siag.nu/pub/siag/%{name}-%{version}.tar.gz
Source1:        siag.desktop
Source2:        siag-pw.desktop
Source3:        siag-egon.desktop
Source4:        siag-xedplus.desktop
Source5:        siag-xfiler.desktop
Source6:        siag-gvu.desktop
# PATCH-FIX-UPSTREAM siag-gcc15.patch -- missing includes/casts (GCC 15), strptime feature macro, ncurses stdscr is not an lvalue, tsiag screen margin clashed with libsiag's paper left_margin (-fno-common)
Patch0:         siag-gcc15.patch
# PATCH-FIX-UPSTREAM siag-egon-drop-types.patch -- egon wrote through a NULL drop_types pointer at startup
Patch1:         siag-egon-drop-types.patch
# PATCH-FIX-UPSTREAM siag-xfiler-argv-overflow.patch -- argv[4] = NULL past the end of char *argv[4]
Patch2:         siag-xfiler-argv-overflow.patch
# PATCH-FIX-UPSTREAM siag-install-duplicate-xpm.patch -- xedplus.xpm listed twice; install(1) refuses to overwrite it
Patch3:         siag-install-duplicate-xpm.patch
# PATCH-FIX-OPENSUSE siag-siaghelp-xdg-open.patch -- open the online help with xdg-open before netscape/lynx
Patch4:         siag-siaghelp-xdg-open.patch
# PATCH-FIX-UPSTREAM siag-xim-latin1.patch -- spreadsheet keys through the Mowitz XIM helper, so dead keys and accented letters work
Patch5:         siag-xim-latin1.patch
# PATCH-FEATURE-OPENSUSE siag-pointer-cursors.patch -- plus pointer over the spreadsheet grid, I-beam over text input
Patch6:         siag-pointer-cursors.patch
# PATCH-FIX-UPSTREAM siag-buffer-name-latin1.patch -- buffer names from UTF-8 file names converted to Latin-1 for lists, tabs and prompts; titles converted back to the locale
Patch7:         siag-buffer-name-latin1.patch
# PATCH-FIX-UPSTREAM siag-selection-utf8.patch -- paste UTF8_STRING (or UTF-8 sent as STRING) as Latin-1 in siag and pw, offer UTF8_STRING when copying; pw rebreaks pasted paragraphs to the margins
Patch8:         siag-selection-utf8.patch
# PATCH-FIX-UPSTREAM siag-xedplus-delete-key.patch -- Delete/KP_Delete deleted backwards like BackSpace
Patch9:         siag-xedplus-delete-key.patch
# PATCH-FIX-UPSTREAM siag-form-dialog-focus.patch -- form dialogs no longer warp the pointer to mid-screen; set _NET_WM_USER_TIME so focus-stealing prevention gives them the focus; WM close button cancels instead of killing the program
Patch10:        siag-form-dialog-focus.patch
# PATCH-FIX-UPSTREAM siag-print-format-save.patch -- File > Print Format shows the current commands and saves them; load-applications was a stub, so ~/.siag/applications.sh was never read; Egon had no print-format
Patch11:        siag-print-format-save.patch
# PATCH-FIX-UPSTREAM siag-pw-modified-flag.patch -- PW: typing or pasting text did not mark the document as modified, so Exit/close quit without asking to save
Patch12:        siag-pw-modified-flag.patch
# PATCH-FIX-UPSTREAM siag-pw-keyboard-focus.patch -- PW: keys typed with the pointer outside the window were lost under click-to-focus
Patch13:        siag-pw-keyboard-focus.patch
BuildRequires:  Mowitz-devel
BuildRequires:  XawM-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  t1lib-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xt)
# gvu and print preview
Requires:       ghostscript
# Helvetica/Times bitmaps used by the widget resources
Requires:       xorg-x11-fonts-core
Requires:       xorg-x11-fonts-legacy
Recommends:     netpbm
Recommends:     xdg-utils
Recommends:     xterm

%description
Siag Office is a free office package for X11 by Ulric Eriksson:

 * Siag (Scheme In A Grid), a spreadsheet programmable in Scheme
 * Pathetic Writer (pw), a word processor
 * Egon Animator, for animations and presentations
 * Xedplus, a text editor; Xfiler, a file manager; Gvu, a PostScript viewer
 * tsiag, a text-mode version of the spreadsheet

This build uses the Motif-like XawM widget set (instead of the default
NeXTSTEP-like neXtaw) and renders document text with t1lib.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure \
  --with-xawm=XawM \
  --with-t1lib \
  --disable-kdeinst \
  --with-docdir=%{_docdir}/%{name} \
  CPPFLAGS="-I%{_includedir}/XawM" \
  CFLAGS="%{optflags} -std=gnu17"
%make_build

%install
%make_install
install -d %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/pixmaps
install -m 0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} \
  %{buildroot}%{_datadir}/applications/
install -m 0644 common/bitmaps/siag.xpm %{buildroot}%{_datadir}/pixmaps/siag.xpm
for a in pw egon xedplus xfiler gvu; do
  install -m 0644 common/bitmaps/$a.xpm %{buildroot}%{_datadir}/pixmaps/siag-$a.xpm
done

%check
for f in %{buildroot}%{_datadir}/applications/*.desktop; do
  desktop-file-validate "$f"
done

%files
%license COPYING
%{_bindir}/egon
%{_bindir}/gvu
%{_bindir}/mgptotxt
%{_bindir}/pw
%{_bindir}/runcmd
%{_bindir}/siag
%{_bindir}/siaghelp
%{_bindir}/siagrun
%{_bindir}/tsiag
%{_bindir}/xedplus
%{_bindir}/xfiler
%{_libdir}/siag
%{_datadir}/siag
# online help, read at run time by the Help menu
%{_docdir}/%{name}
%{_mandir}/man1/*.1%{?ext_man}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/siag*.xpm

%changelog
