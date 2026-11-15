#
# spec file for package gtklp
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           gtklp
Version:        1.3.4
Release:        0
Summary:        GTK frontend to CUPS for printing files
License:        GPL-2.0-or-later
Group:          Hardware/Printing
URL:            https://sourceforge.net/projects/gtklp/
Source0:        https://downloads.sourceforge.net/project/gtklp/gtklp/%{version}/%{name}-%{version}.src.tar.gz
Source1:        gtklp.desktop
Source2:        gtklpq.desktop
# PATCH-FIX-OPENSUSE drop the second, bare AM_GNU_GETTEXT (gettext >= 0.20 refuses it) and pin autopoint to 0.21
Patch0:         gtklp-1.3.4-gettext-external.patch
# PATCH-FIX-OPENSUSE non-literal format strings in exitOnError (Debian/Gentoo, reduced)
Patch1:         gtklp-1.3.4-format-security.patch
# PATCH-FIX-OPENSUSE freadline() off-by-one heap/stack overflow, overlapping snprintf in gtklpq, PPD choice text test
Patch2:         gtklp-1.3.4-buffer-overflows.patch
# PATCH-FEATURE-OPENSUSE xdg-open instead of netscape, CUPS 2 help URL, gtklpq button on by default
Patch3:         gtklp-1.3.4-defaults.patch
# PATCH-FIX-OPENSUSE 32x32 window icon XPM declared 3 colours but has 4 (GdkPixbuf rejected it)
Patch4:         gtklp-1.3.4-icon-xpm.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext-tools
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(x11)
Requires:       cups-client
Requires:       xdg-utils

%description
GtkLP is a graphical frontend to CUPS. It shows every option of the
selected printer (including the PPD options) in a tabbed dialog and
sends the job to CUPS.

Because it also reads the data to print from standard input, it can be
used as the "print command" of programs that only know how to pipe
PostScript into lpr, e.g. Siag Office, xfig or old X11 applications:
set the print command to "gtklp" instead of "lpr".

The package also contains GtkLPQ, a small viewer for the CUPS print
queues that can cancel, hold and move jobs.

%package lang
Summary:        Translations for package %{name}
Group:          System/Localization
Requires:       %{name} = %{version}
BuildArch:      noarch

%description lang
Provides translations for the "%{name}" package.

%prep
%autosetup -p1
# the AM_GNU_GETTEXT_VERSION stamp is checked by autopoint
autoreconf -fi

%build
# globals are defined in headers included by several objects
export CFLAGS="%{optflags} -fcommon"
%configure \
  --disable-forte \
  --with-cups-config=%{_bindir}/cups-config
%make_build

%install
%make_install
install -Dpm 0644 man/gtklp-ru.1 %{buildroot}%{_mandir}/ru/man1/gtklp.1
install -Dpm 0644 man/gtklpq-ru.1 %{buildroot}%{_mandir}/ru/man1/gtklpq.1
install -Dpm 0644 man/gtklp-uk.1 %{buildroot}%{_mandir}/uk/man1/gtklp.1
install -Dpm 0644 man/gtklpq-uk.1 %{buildroot}%{_mandir}/uk/man1/gtklpq.1
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/gtklp.desktop
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/gtklpq.desktop
%find_lang %{name} --with-man

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/gtklp.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/gtklpq.desktop

%files
%license COPYING
%doc AUTHORS BUGS ChangeLog README README.FAQ TODO USAGE
%{_bindir}/gtklp
%{_bindir}/gtklpq
%{_datadir}/applications/gtklp.desktop
%{_datadir}/applications/gtklpq.desktop
%{_mandir}/man1/gtklp.1%{?ext_man}
%{_mandir}/man1/gtklpq.1%{?ext_man}

%files lang -f %{name}.lang
%lang(ru) %{_mandir}/ru/man1/gtklpq.1%{?ext_man}
%lang(uk) %{_mandir}/uk/man1/gtklpq.1%{?ext_man}

%changelog
