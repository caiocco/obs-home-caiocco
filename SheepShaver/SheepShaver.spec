#
# spec file for package SheepShaver
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Built from the kanjitalk755 fork of macemu, the maintained upstream.
# Same tarball as the BasiliskII package; SheepShaver/ reaches into
# BasiliskII/ through symlinks that are already in git.
# Two binaries, as Debian does for BasiliskII (see README.SUSE):
#  - SheepShaver: -DMEM_BULK (as the Windows port), no JIT.  The Mac address
#    space is one block reserved anywhere, so it runs out of the box.
#  - SheepShaver-jit: upstream's real addressing + JIT.  It must mmap() page
#    zero, so it needs vm.mmap_min_addr=0 ("Cannot map Low Memory Globals").
#    The precompiled x86_64 JIT ops assume real addressing, so the JIT crashes
#    with MEM_BULK or --enable-addressing=direct (tested with Mac OS 8.6).
# No sysctl.d file is installed; an example goes to the docs.
# SheepShaver.png is the 256x256 PNG taken from src/MacOSX/SheepShaver.icns.
#

%define commit  f532be3d
%define gitdate 20261021
%define tarname macemu-%{gitdate}.%{commit}
# the PowerPC JIT (dyngen) does not like LTO
%define _lto_cflags %{nil}
Name:           SheepShaver
Version:        2.4+git%{gitdate}.%{commit}
Release:        0
Summary:        PowerPC Macintosh emulator
License:        GPL-2.0-or-later
Group:          System/Emulators/Other
URL:            https://github.com/kanjitalk755/macemu
Source0:        %{tarname}.tar.xz
Source1:        SheepShaver.desktop
Source2:        SheepShaver.png
Source3:        README.SUSE
Source4:        90-sheepshaver.conf
# Adapted from Debian (1001_use_system_tinyxml2.patch), extended to SheepShaver
Patch0:         macemu-system-tinyxml2.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  libvdeplug-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(tinyxml2)
BuildRequires:  pkgconfig(x11)
ExclusiveArch:  x86_64

%description
SheepShaver is a PowerPC Macintosh emulator. It runs Mac OS 7.5.2
through 9.0.4 with a PowerPC emulator (with a JIT compiler on x86),
so you need a copy of Mac OS and a PowerPC Macintosh ROM image
(Old World ROM or "Mac OS ROM" file) to use it.

Features: SDL2 video and sound, HFS/HFS+ volumes, CD-ROM (incl.
BIN/CUE), floppies, networking (slirp, TUN/TAP, VDE), host file
sharing through a "Unix" icon on the Mac desktop, clipboard exchange
and a GTK3 preferences editor.

Two programs are included: SheepShaver (no JIT, works out of the box)
and SheepShaver-jit (much faster, but needs vm.mmap_min_addr=0; see
README.SUSE).

%prep
%autosetup -p1 -n %{tarname}
# make sure the bundled tinyxml2 copy is not used
rm -f BasiliskII/src/Unix/tinyxml2.cpp BasiliskII/src/Unix/tinyxml2.h

# second copy of the tree for the JIT build (relative symlinks survive cp -a)
mkdir jit
cp -a BasiliskII SheepShaver jit/

%build
%define ss_configure \
%configure \\\
        --enable-sdl-video \\\
        --enable-sdl-audio \\\
        --with-gtk=gtk3 \\\
        --without-esd \\\
        --without-mon \\\
        --with-bincue \\\
        --with-vdeplug
top=$PWD
# JIT build: real addressing (upstream default)
cd $top/jit/SheepShaver/src/Unix
NO_CONFIGURE=1 ./autogen.sh
%ss_configure --enable-jit
%make_build
# default build: MEM_BULK, no JIT
cd $top/SheepShaver/src/Unix
export CXXFLAGS="%{optflags} -DMEM_BULK"
NO_CONFIGURE=1 ./autogen.sh
%ss_configure --disable-jit
%make_build

%install
cd SheepShaver/src/Unix
%make_install
cd -
install -m0755 jit/SheepShaver/src/Unix/SheepShaver %{buildroot}%{_bindir}/SheepShaver-jit
echo ".so man1/SheepShaver.1" > %{buildroot}%{_mandir}/man1/SheepShaver-jit.1
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/SheepShaver.desktop
install -Dm0644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/SheepShaver.png
mkdir -p %{buildroot}%{_docdir}/%{name}/html
install -m0644 SheepShaver/doc/Linux/*.html SheepShaver/doc/Linux/*.gif \
        %{buildroot}%{_docdir}/%{name}/html/
install -m0644 SheepShaver/NEWS SheepShaver/doc/Linux/gnome_keybindings.txt \
        %{SOURCE3} %{SOURCE4} \
        %{buildroot}%{_docdir}/%{name}/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/SheepShaver.desktop

%files
%license SheepShaver/COPYING
%{_docdir}/%{name}/
%{_bindir}/SheepShaver
%{_bindir}/SheepShaver-jit
%{_mandir}/man1/SheepShaver.1%{?ext_man}
%{_mandir}/man1/SheepShaver-jit.1%{?ext_man}
%{_datadir}/SheepShaver/
%{_datadir}/applications/SheepShaver.desktop
%{_datadir}/icons/hicolor/256x256/apps/SheepShaver.png

%changelog
