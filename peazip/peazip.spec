#
# spec file for package peazip
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           peazip
Version:        11.4.0
Release:        0
Summary:        File manager and archiver
License:        LGPL-3.0-only AND Zlib
Group:          Productivity/Archiving/Compression
URL:            https://peazip.github.io/
Source0:        https://github.com/peazip/PeaZip/releases/download/%{version}/%{name}-%{version}.src.zip
BuildRequires:  7zip
BuildRequires:  brotli
BuildRequires:  fdupes
BuildRequires:  fpc >= 3.2.0
BuildRequires:  fpc-src
BuildRequires:  hicolor-icon-theme
BuildRequires:  lazarus-ide >= 3.0
BuildRequires:  lazarus-lcl-gtk2 >= 3.0
BuildRequires:  lazarus-lcl-nogui
BuildRequires:  lazarus-lcl-qt6 >= 3.0
BuildRequires:  lazarus-tools
BuildRequires:  libQt6Pas-devel
BuildRequires:  unzip
BuildRequires:  zstd
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)
ExclusiveArch:  x86_64 aarch64 %{ix86}

%description
PeaZip is a file and archive manager. It creates 7z, Brotli, bzip2,
gzip, PEA, split, TAR, WIM, XZ, ZIP and Zstandard archives, and opens
over 200 formats, such as ARJ, CAB, CPIO, ISO, LHA, RPM and DEB.

It also offers strong encryption, an encrypted password manager,
batch renaming, file splitting and joining, secure deletion, file
comparison, checksums and hashes, and a benchmark.

Archive formats are handled by the system 7z, zstd and brotli tools.

%package gtk
Summary:        File manager and archiver (GTK 2)
Group:          Productivity/Archiving/Compression
Requires:       7zip
Requires:       brotli
Requires:       zstd
Provides:       %{name} = %{version}-%{release}
Conflicts:      %{name}-qt
RemovePathPostfixes: .gtk

%description gtk
PeaZip is a file and archive manager. It creates 7z, Brotli, bzip2,
gzip, PEA, split, TAR, WIM, XZ, ZIP and Zstandard archives, and opens
over 200 formats, such as ARJ, CAB, CPIO, ISO, LHA, RPM and DEB.

This package contains the GTK 2 build.

%package qt
Summary:        File manager and archiver (Qt 6)
Group:          Productivity/Archiving/Compression
Requires:       7zip
Requires:       brotli
Requires:       zstd
Provides:       %{name} = %{version}-%{release}
Conflicts:      %{name}-gtk
RemovePathPostfixes: .qt

%description qt
PeaZip is a file and archive manager. It creates 7z, Brotli, bzip2,
gzip, PEA, split, TAR, WIM, XZ, ZIP and Zstandard archives, and opens
over 200 formats, such as ARJ, CAB, CPIO, ISO, LHA, RPM and DEB.

This package contains the Qt 6 build.

%prep
%autosetup -n %{name}-%{version}.src
sed -i 's/\r$//' res/share/readme/readme_Linux.txt

# Build the two widgetsets in separate trees
cd ..
rm -rf %{name}-%{version}.src-qt
cp -a %{name}-%{version}.src %{name}-%{version}.src-qt

%build
# $1 = widgetset
build_peazip() {
  local conf=$(pwd)/../lazconf-$1
  mkdir -p $conf
  export HOME=$conf
  local opts="--pcp=$conf --ws=$1"
  lazbuild $opts dev/metadarkstyle/metadarkstyle.lpk
  lazbuild $opts -B dev/project_pea.lpi
  lazbuild $opts -B dev/project_peach.lpi
  test -x dev/pea
  test -x dev/peazip
}

build_peazip gtk2

cd ../%{name}-%{version}.src-qt
build_peazip qt6

%install
pkgdir=%{buildroot}%{_libdir}/%{name}
install -d $pkgdir
for f in pea peazip; do
  install -m 0755 dev/$f $pkgdir/$f.gtk
  install -m 0755 ../%{name}-%{version}.src-qt/dev/$f $pkgdir/$f.qt
done

# Architecture independent resources, without the Windows and macOS bits
install -d %{buildroot}%{_datadir}
cp -a res/share %{buildroot}%{_datadir}/%{name}
pushd %{buildroot}%{_datadir}/%{name}
rm -rf lang-wincontext batch/bat batch/Windows "batch/macOS service menus"
rm -f readme/readme_Windows.txt readme/readme_macOS.txt
rm -f icons/*.ico icons/*.icns icons/*.icl
popd
find %{buildroot}%{_datadir}/%{name} -type d -exec chmod 0755 {} +
find %{buildroot}%{_datadir}/%{name} -type f -exec chmod 0644 {} +
# Only the sample scripts with a shebang are meant to be executed
grep -rlZ --null '^#!' %{buildroot}%{_datadir}/%{name}/batch | \
  while IFS= read -r -d '' f; do
    if head -c2 "$f" | grep -q '^#!'; then chmod 0755 "$f"; fi
  done

# Installed (non portable) layout: no res/portable, configuration
# goes to $XDG_CONFIG_HOME/peazip
install -d $pkgdir/res
ln -s %{_datadir}/%{name} $pkgdir/res/share

# Use the system backends instead of the bundled ones
for b in 7z zstd brotli; do
  install -d $pkgdir/res/bin/$b
  ln -s %{_bindir}/$b $pkgdir/res/bin/$b/$b
done

# The binary only gets its final name at packaging time
# (RemovePathPostfixes), so use a wrapper instead of a symlink
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh
exec %{_libdir}/%{name}/%{name} "\$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

# Desktop integration
fd=res/share/batch/freedesktop_integration
install -Dm 0644 $fd/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
for i in %{name} %{name}_add %{name}_extract; do
  install -Dm 0644 $fd/$i.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/$i.png
done

%fdupes -s %{buildroot}%{_datadir}

%files gtk
%license res/share/copying/copying.txt
%doc res/share/readme/readme_Linux.txt
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/pea.gtk
%{_libdir}/%{name}/%{name}.gtk
%{_libdir}/%{name}/res
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}*.png

%files qt
%license res/share/copying/copying.txt
%doc res/share/readme/readme_Linux.txt
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/pea.qt
%{_libdir}/%{name}/%{name}.qt
%{_libdir}/%{name}/res
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}*.png

%changelog
