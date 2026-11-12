#
# spec file for package thenextlevel
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Greg J. Badros' entry in Red Hat's 1996 desktop contest, shipped by Red Hat
# Linux 4.x as TheNextLevel-1.1.  The tarball is the one inside
#   https://www.ibiblio.org/pub/historic-linux/distributions/redhat-4.2/src/SRPMS/TheNextLevel-1.1-3.src.rpm
# taken unchanged; Red Hat's own patch (Windows 95 style buttons, fvwm95)
# is not used.  Its title bar needs the fvwm2 package from home:caiocco,
# which centers the title text in a bar smaller than the font set height.
#

Name:           thenextlevel
Version:        0.1
Release:        0
Summary:        Greg J. Badros' fvwm2 desktop from Red Hat Linux 4.x
License:        GPL-1.0-or-later
Group:          System/GUI/Other
URL:            https://www.ibiblio.org/pub/historic-linux/distributions/redhat-4.2/
Source0:        TheNextLevel-%{version}.tar.gz
Source1:        thenextlevel-fvwm2rc
Source2:        thenextlevel-session
Source3:        thenextlevel.desktop
Source4:        README.openSUSE
# PATCH-FEATURE-OPENSUSE thenextlevel-system-wide.patch -- read the files from /etc/X11/TheNextLevel unless the user has a copy
Patch0:         thenextlevel-system-wide.patch
# PATCH-FIX-OPENSUSE thenextlevel-fvwm-2.7.patch -- fvwm 2.7 syntax, fixed pixel fonts, title bar height
Patch1:         thenextlevel-fvwm-2.7.patch
# PATCH-FIX-OPENSUSE thenextlevel-current-system.patch -- xlockmore modes, removed modules, Restart, journalctl, xdg-open
Patch2:         thenextlevel-current-system.patch
BuildRequires:  fdupes
BuildRequires:  m4
Requires:       cpp
Requires:       fvwm2
Requires:       m4
Requires:       xorg-x11-fonts-core
Requires:       xorg-x11-fonts-legacy
Requires:       xrdb
Requires:       xsetroot
Requires:       xterm
Recommends:     xclock
Recommends:     xdg-utils
Recommends:     xlockmore
Provides:       TheNextLevel = %{version}
BuildArch:      noarch

%description
The Next Level is the fvwm2 desktop configuration that won Red Hat's 1996
desktop contest and shipped with Red Hat Linux 4.x. It is written in m4
and adapts itself to the screen size and the installed programs: title
bar buttons drawn as pixmaps, menus with mini icons and keyboard
shortcuts, tear-off button bars, a Preferences menu and HTML help.

This is the original configuration, ported to fvwm 2.7. Select the
"TheNextLevel" session in the display manager.

%prep
%autosetup -p1 -n The_Next_Level-files

%build
cd docs
sh ./make-indexes

%install
d=%{buildroot}%{_sysconfdir}/X11/TheNextLevel
install -d -m 0755 $d
install -m 0644 .fvwm2rc.* .Xdefaults .Xdefaults-fvwm-defines $d/
sed -e 's|@TNL_DIR@|%{_sysconfdir}/X11/TheNextLevel|g' \
    -e 's|@TNL_PIXMAPS@|%{_datadir}/%{name}/pixmaps|g' \
    %{SOURCE1} > $d/fvwm2rc
chmod 0644 $d/fvwm2rc

install -d -m 0755 %{buildroot}%{_datadir}/%{name}/pixmaps
install -m 0644 icons/*.xpm %{buildroot}%{_datadir}/%{name}/pixmaps/
%fdupes -s %{buildroot}%{_datadir}/%{name}

install -d -m 0755 %{buildroot}%{_bindir}
sed -e 's|@TNL_DIR@|%{_sysconfdir}/X11/TheNextLevel|g' %{SOURCE2} \
    > %{buildroot}%{_bindir}/thenextlevel-session
chmod 0755 %{buildroot}%{_bindir}/thenextlevel-session

install -D -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/xsessions/thenextlevel.desktop

dd=%{buildroot}%{_docdir}/%{name}
install -d -m 0755 $dd/docs
install -m 0644 README DESKTOP FILES Sample.Xmodmap %{SOURCE4} $dd/
install -m 0644 docs/*.html $dd/docs/
cp -a docs/gif docs/man $dd/docs/
chmod -R u=rwX,go=rX $dd

%files
%dir %{_sysconfdir}/X11/TheNextLevel
%config(noreplace) %{_sysconfdir}/X11/TheNextLevel/.fvwm2rc.*
%config(noreplace) %{_sysconfdir}/X11/TheNextLevel/.Xdefaults
%config(noreplace) %{_sysconfdir}/X11/TheNextLevel/.Xdefaults-fvwm-defines
%config %{_sysconfdir}/X11/TheNextLevel/fvwm2rc
%{_bindir}/thenextlevel-session
%{_datadir}/%{name}
%{_datadir}/xsessions/thenextlevel.desktop
%{_docdir}/%{name}

%changelog
