#
# spec file for package osmo
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           osmo
Version:        0.4.5
Release:        1%{?dist}
Summary:        Personal organizer for GTK+
License:        GPL-2.0-or-later
Group:          Productivity/Office/Organizers
URL:            https://clayo.org/osmo/
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.10
BuildRequires:  pkgconfig(libxml-2.0) >= 2.0
BuildRequires:  pkgconfig(gthread-2.0) >= 2.6.0
BuildRequires:  pkgconfig(libnotify) >= 0.7.0
BuildRequires:  pkgconfig(webkit2gtk-4.1) >= 2.8.0
BuildRequires:  pkgconfig(libical) >= 1.0
BuildRequires:  pkgconfig(gspell-1) >= 1.2.0
BuildRequires:  pkgconfig(libarchive) >= 3.0.0
BuildRequires:  pkgconfig(pango) >= 1.20
BuildRequires:  gettext-tools
BuildRequires:  update-desktop-files
BuildRequires:  hicolor-icon-theme

Requires:       hicolor-icon-theme

%description
Osmo is a handy personal organizer which includes:
- Calendar with day notes and iCalendar support
- Tasks manager with alarms and notifications
- Contacts manager with birthdays browser
- Notes manager with encryption support

%prep
%setup -q

%build
%configure \
    --enable-printing=yes \
    --enable-backup=no

%make_build

%install
%make_install

# Install desktop file
%suse_update_desktop_file -r %{name} Office Calendar ContactManagement

# Find and install locale files
%find_lang %{name}

%post
%icon_theme_cache_post

%postun
%icon_theme_cache_postun

%files -f %{name}.lang
%license COPYING
%doc README AUTHORS ChangeLog
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/*/actions/%{name}-*.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_logo.png
%{_datadir}/pixmaps/moonphase_*_data.png
%dir %{_datadir}/sounds/%{name}
%{_datadir}/sounds/%{name}/alarm.wav
%{_mandir}/man1/%{name}.1%{?ext_man}

%changelog
* Sat Jun 07 2025 Caio <caiocco@yahoo.com.br> - 0.4.5-2
- Add openSUSE Leap 16.0 support

* Thu Jan 16 2025 Caio <caio@localhost> - 0.4.5-1
- Initial package for openSUSE
- Fixed infinite loop issues in calendar and GUI
