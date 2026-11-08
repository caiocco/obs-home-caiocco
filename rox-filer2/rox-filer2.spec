#
# spec file for package rox-filer2
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define upstream_version 2.14.0-6
%define appdir %{_prefix}/lib/rox-filer2
Name:           rox-filer2
Version:        2.14.0.6
Release:        0
Summary:        Lightweight GTK3 file manager and desktop for X11 and Wayland
License:        (AFL-2.0 OR LGPL-2.0-or-later) AND GPL-2.0-or-later AND GPL-3.0-or-later
Group:          Productivity/File utilities
URL:            https://github.com/josejp2424/ROX-Filer2
Source0:        https://github.com/josejp2424/ROX-Filer2/archive/v%{upstream_version}.tar.gz#/%{name}-%{upstream_version}.tar.gz
Source99:       %{name}-rpmlintrc
# PATCH-FIX-OPENSUSE rox-filer2-compact-modern-toolbar.patch -- drop the hardcoded 48px height of the Modern navigation toolbar
Patch0:         %{name}-compact-modern-toolbar.patch
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  gettext-tools
BuildRequires:  hicolor-icon-theme
BuildRequires:  meson >= 0.61.0
BuildRequires:  pkgconfig
BuildRequires:  polkit
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.70.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.22.0
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(shared-mime-info)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
Requires:       file
Requires:       shared-mime-info
Recommends:     libgtk-layer-shell0
Recommends:     pkexec
Recommends:     udisks2
Suggests:       cifs-utils
Suggests:       fuse3
Suggests:       imobiledevice-tools
Suggests:       samba-client
Suggests:       samba-client-libs
Suggests:       simple-mtpfs
Suggests:       usbmuxd
Provides:       rox-filer = %{version}
Conflicts:      rox-filer

%description
Rox-Filer2 is a continuation of the classic ROX-Filer file manager and
desktop by Thomas Leonard, ported to GTK3. It runs natively on X11 and
on Wayland (using GTK Layer Shell for the desktop surface) and provides
a desktop with icons and wallpaper, drive icons, paired filer windows,
XDG MIME and application integration, custom actions, Trash support,
file templates and the ROX File Search companion (rox-find).

SMB browsing, Samba usershares, portable devices (MTP, PTP, iOS) and
the Wayland desktop are enabled at runtime when the corresponding
optional libraries and helpers are installed.

%package lang
Summary:        Translations for package %{name}
Group:          System/Localization
Requires:       %{name} = %{version}
BuildArch:      noarch

%description lang
Translations of the Rox-Filer2 and ROX File Search user interfaces and
the translated manuals. Installed only on request; without it the
programs run in English.

%prep
%autosetup -p1 -n ROX-Filer2-%{upstream_version}
# Template for new user files, not a packaged executable
chmod 0644 ROX-Filer/Templates/python3.py

%build
%meson -Dsmb=auto -Dportable_devices=auto
%meson_build
# Regenerate the translation catalogues shipped in the AppDir
rm -rf ROX-Filer/Messages
pushd ROX-Filer/src/po
for po in *.po; do
  sh ./make-mo "${po%.po}"
done
popd
pushd rox-find/po
for po in *.po; do
  lang=${po%.po}
  mkdir -p ../locale/$lang/LC_MESSAGES
  msgfmt -c -o ../locale/$lang/LC_MESSAGES/rox-find.mo $po
done
popd

%install
# AppDir runtime
install -d %{buildroot}%{appdir}
cp -a ROX-Filer/. %{buildroot}%{appdir}/
rm -rf %{buildroot}%{appdir}/src %{buildroot}%{appdir}/build \
       %{buildroot}%{appdir}/ROX %{buildroot}%{appdir}/ROX-Filer.dbg
cp -a package-assets/ROX %{buildroot}%{appdir}/ROX
install -m0755 %{_vpath_builddir}/ROX-Filer %{buildroot}%{appdir}/ROX-Filer
install -m0755 %{_vpath_builddir}/rox-mount-helper %{buildroot}%{appdir}/rox-mount-helper
install -m0755 %{_vpath_builddir}/rox-open-root-helper %{buildroot}%{appdir}/rox-open-root-helper
install -m0644 data/icons/hicolor/256x256/apps/rox-filer2.png %{buildroot}%{appdir}/ROX-Filer.png
ln -sfn ROX-Filer.png %{buildroot}%{appdir}/.DirIcon

# Launchers
install -Dm0755 package-base/usr/bin/roxfiler %{buildroot}%{_bindir}/roxfiler
for l in rox ROX-Filer Rox-Filer2; do
  ln -s roxfiler %{buildroot}%{_bindir}/$l
done
for l in rox-wayland rox-x11; do
  ln -s ../lib/rox-filer2/ROX-Filer %{buildroot}%{_bindir}/$l
done
install -Dm0755 %{_vpath_builddir}/rox-find %{buildroot}%{_bindir}/rox-find

# Desktop entries, polkit actions and pixmaps
install -d %{buildroot}%{_datadir}/applications
install -m0644 package-base/usr/share/applications/*.desktop \
  rox-find/data/rox-find.desktop %{buildroot}%{_datadir}/applications/
install -d %{buildroot}%{_datadir}/polkit-1/actions
install -m0644 package-base/usr/share/polkit-1/actions/*.policy \
  %{buildroot}%{_datadir}/polkit-1/actions/
install -d %{buildroot}%{_datadir}/pixmaps
install -m0644 package-base/usr/share/pixmaps/rox-desktop-wallpaper.svg \
  package-base/usr/share/pixmaps/roxfiler2-desktop-apps-icon.svg \
  ROX-Filer-root.svg rox-find/data/rox-find.svg \
  %{buildroot}%{_datadir}/pixmaps/
for i in rox-filer2.svg ROX-Filer.svg Rox-Filer2.svg; do
  install -m0644 data/icons/hicolor/scalable/apps/rox-filer2.svg \
    %{buildroot}%{_datadir}/pixmaps/$i
done

# Icon theme
for size in 16 22 24 32 48 64 96 128 192 256; do
  install -Dm0644 data/icons/hicolor/${size}x${size}/apps/rox-filer2.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/rox-filer2.png
done
install -Dm0644 data/icons/hicolor/scalable/apps/rox-filer2.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/rox-filer2.svg
for size in 48 64 128 256; do
  install -Dm0644 rox-find/data/icons/${size}x${size}/apps/rox-find.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/rox-find.png
done
for i in application-pet.svg application-x-sfs.svg application-x-squashfs-image.svg; do
  install -Dm0644 package-assets/ROX/MIME/$i \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/$i
done

# MIME types for disk images
install -Dm0644 data/mime/rox-filer2-image-mounter.xml \
  %{buildroot}%{_datadir}/mime/packages/rox-filer2-image-mounter.xml

# rox-find translations
install -d %{buildroot}%{_datadir}/locale
cp -a rox-find/locale/. %{buildroot}%{_datadir}/locale/
%find_lang rox-find

# ROX-Filer catalogues and translated manuals live in the AppDir; move
# them to the -lang subpackage (the manual falls back to Manual.html)
: > %{name}.files
echo "%%dir %{appdir}/Messages" >> rox-find.lang
for d in %{buildroot}%{appdir}/Messages/*; do
  l=${d##*/}
  echo "%%lang($l) %{appdir}/Messages/$l" >> rox-find.lang
done
echo "%%exclude %{appdir}/Messages" >> %{name}.files
for f in %{buildroot}%{appdir}/Help/Manual-*.html; do
  l=${f##*/Manual-}
  l=${l%%.html}
  [ "$l" = en ] && continue
  echo "%%lang($l) %{appdir}/Help/Manual-$l.html" >> rox-find.lang
  echo "%%exclude %{appdir}/Help/Manual-$l.html" >> %{name}.files
done

# Manual pages
install -Dm0644 data/man/rox.1 %{buildroot}%{_mandir}/man1/rox.1
install -Dm0644 data/man/rox-find.1 %{buildroot}%{_mandir}/man1/rox-find.1
for l in roxfiler Rox-Filer2 ROX-Filer rox-wayland rox-x11; do
  echo ".so man1/rox.1" > %{buildroot}%{_mandir}/man1/$l.1
done

%fdupes -s %{buildroot}%{_prefix}

%files -f %{name}.files
%license LICENSE
%doc README.md CHANGELOG
%{_bindir}/rox
%{_bindir}/roxfiler
%{_bindir}/ROX-Filer
%{_bindir}/Rox-Filer2
%{_bindir}/rox-find
%{_bindir}/rox-wayland
%{_bindir}/rox-x11
%{appdir}
%{_datadir}/applications/rox-desktop-apps.desktop
%{_datadir}/applications/rox-filer.desktop
%{_datadir}/applications/rox-find.desktop
%{_datadir}/applications/rox-wallpaper.desktop
%dir %{_datadir}/polkit-1
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.rox-filer2.mount.policy
%{_datadir}/polkit-1/actions/org.rox-filer2.open-root.policy
%{_datadir}/pixmaps/*.svg
%{_datadir}/icons/hicolor/*/apps/rox-filer2.*
%{_datadir}/icons/hicolor/*/apps/rox-find.png
%{_datadir}/icons/hicolor/scalable/mimetypes/application-*.svg
%{_datadir}/mime/packages/rox-filer2-image-mounter.xml
%{_mandir}/man1/*.1%{?ext_man}

%files lang -f rox-find.lang

%changelog
