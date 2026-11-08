#To the extent possible under law, the person who associated CC0 with
#this spec file has waived all copyright and related or neighboring rights
#to this spec file.
#
#You should have received a copy of the CC0 legalcode along with this
#work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

# Bluecurve cursors from Red Hat's bluecurve-icon-theme (the last release,
# packaged by Fedora until F25). Packaging and the cursor alias list follow
# Phantom X's chinforpms Copr (bluecurve-icon-theme 1:8.0.2-103), which also
# adds the Bluecurve-classic cursor sets. Only the cursors are packaged here.
#
# Epoch 1 matches the Copr package so this one replaces it as an upgrade.

%define srcname bluecurve-icon-theme

Name:           bluecurve-cursor-theme
Epoch:          1
Version:        8.0.2
Release:        0
Summary:        Bluecurve cursor theme
License:        GPL-1.0-or-later
Group:          System/X11/Icons
URL:            https://github.com/PhantomX/chinforpms/tree/main/bluecurve-icon-theme
# There is no upstream any more; Fedora's lookaside cache keeps the tarball
Source0:        https://src.fedoraproject.org/repo/pkgs/%{srcname}/%{srcname}-%{version}.tar.bz2/3a3ecac0922f964bb1c4be617e8dec37/%{srcname}-%{version}.tar.bz2
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{srcname}/Bluecurve-classic.tar.bz2/b0a34d7a0af0e0c1786f7d459a94b9ee/Bluecurve-classic.tar.bz2
BuildRequires:  fdupes
BuildArch:      noarch

%description
Bluecurve style X11 cursors, from the Red Hat Linux and early Fedora
desktop. Includes the Bluecurve and LBluecurve (left-handed) themes,
their inverse variants, and the Bluecurve-classic sets.

%prep
%setup -q -n %{srcname}-%{version} -a 1

%build
# The cursors ship pre-built (Xcursor files); nothing to compile.

%install
install -dm 0755 %{buildroot}%{_datadir}/icons
for dir in {,L}Bluecurve{,-inverse} ; do
  install -dm 0755 %{buildroot}%{_datadir}/icons/${dir}
  cp -a theme/${dir}/cursors %{buildroot}%{_datadir}/icons/${dir}/
  install -pm 0644 theme/${dir}/${dir}.cursortheme %{buildroot}%{_datadir}/icons/${dir}/
done
cp -a Bluecurve-classic Bluecurve-classic-inverse %{buildroot}%{_datadir}/icons/
find %{buildroot}%{_datadir}/icons/ -type d -exec chmod 0755 {} +
find %{buildroot}%{_datadir}/icons/ -type f -exec chmod 0644 {} +

# Symlinks that upstream's "make install" recreates from symlink.manifest
grep '^cursors/' theme/Bluecurve/symlink.manifest | while read link target ; do
  ln -s ${target} %{buildroot}%{_datadir}/icons/Bluecurve/${link}
done

# Aliases for freedesktop, Qt/KDE, GTK and Mozilla cursor names
# (from the chinforpms spec)
for dir in {,L}Bluecurve{,-inverse} ; do
  ( cd %{buildroot}%{_datadir}/icons/${dir}/cursors
    ln -s hand1 9d800788f1b08800ae810202380a0822
    ln -s hand1 5aca4d189052212118709018842178c0
    ln -s hand2 e29285e634086352946a0e7090d73106
    ln -s hand2 pointer
    ln -s hand2 pointing_hand
    ln -s cross cell
    ln -s dnd-copy 6407b0e94181790501fd1e167b474872
    ln -s dnd-copy 1081e37283d90000800003c07f3ef6bf
    ln -s dnd-copy 08ffe1cb5fe6fc01f906f1c063814ccf
    ln -s dnd-copy b66166c04f8c3109214a4fbd64a50fc8
    ln -s dnd-copy copy
    ln -s dnd-move 4498f0e0c1937ffe01fd06f973665830
    ln -s dnd-move 9081237383d90e509aa00f00170e968f
    ln -s dnd-link alias
    ln -s dnd-link link
    ln -s dnd-link 0876e1c15ff2fc01f906f1c363074c0f
    ln -s dnd-link 640fb0e74195791501fd1ed57b41487f
    ln -s dnd-link a2a266d0498c3104214a47bd64ab0fc8
    ln -s dnd-move move
    ln -s dnd-none 03b6e0fcb3499374a867c041f52298f0
    ln -s dnd-none fcf21c00b30f7e3f83fe0dfd12e71cff
    ln -s dnd-none closedhand
    ln -s dnd-none forbidden
    ln -s dnd-none no-drop
    ln -s dnd-none not-allowed
    ln -s fleur all-scroll
    ln -s fleur size_all
    ln -s left_ptr default
    ln -s left_ptr_watch 00000000000000020006000e7e9ffc3f
    ln -s left_ptr_watch 3ecb610c1bf2410f44200f48c40d3599
    ln -s left_ptr_watch 0426c94ea35c87780ff01dc239897213
    ln -s left_ptr_watch half-busy
    ln -s left_ptr_watch wait
    ln -s left_ptr_watch 9116a3ea924ed2162ecab71ba103b17f
    ln -s left_ptr_watch progress
    ln -s top_right_corner fcf1c3c7cd4491d801f1e1c78f100000
    ln -s top_right_corner 50585d75b494802d0151028115016902
    ln -s top_right_corner nesw-resize
    ln -s top_right_corner size_bdiag
    ln -s plus 3085a0e285430894940527032f8b26df
    ln -s sb_h_double_arrow 14fef782d02440884392942c11205230
    ln -s sb_h_double_arrow 028006030e0e7ebffc7f7070c0600140
    ln -s sb_h_double_arrow 043a9f68147c53184671403ffa811cc5
    ln -s sb_h_double_arrow col-resize
    ln -s sb_h_double_arrow ew-resize
    ln -s sb_h_double_arrow e-resize
    ln -s sb_h_double_arrow size_hor
    ln -s sb_h_double_arrow split_h
    ln -s sb_h_double_arrow w-resize
    ln -s top_left_corner c7088f0f3e6c8088236ef8e1e3e70000
    ln -s top_left_corner 38c5dff7c7b8962045400281044508d2
    ln -s top_left_corner nwse-resize
    ln -s top_left_corner size_fdiag
    ln -s sb_up_arrow up_arrow
    ln -s sb_v_double_arrow 2870a09082c103050810ffdffffe0204
    ln -s sb_v_double_arrow c07385c7190e701020ff7ffffd08103c
    ln -s sb_v_double_arrow n-resize
    ln -s sb_v_double_arrow row-resize
    ln -s sb_v_double_arrow size_ver
    ln -s sb_v_double_arrow split_v
    ln -s sb_v_double_arrow v_double_arrow
    ln -s question_arrow d9ce0ab605698f320427677b458ad60b
    ln -s question_arrow help
    ln -s question_arrow whats_this
    ln -s double_arrow 00008160000006810000408080010102
    ln -s double_arrow ns-resize
    ln -s xterm ibeam
    ln -s xterm term
  )
done

# The non-inverse themes already ship this one as a regular file
for dir in {,L}Bluecurve-inverse ; do
  ln -s question_arrow \
    %{buildroot}%{_datadir}/icons/${dir}/cursors/5c6cd98b3f3ebcb1f9c7f1c204630408
done

%fdupes -s %{buildroot}%{_datadir}/icons

%files
%license COPYING
%doc AUTHORS
%{_datadir}/icons/Bluecurve/
%{_datadir}/icons/Bluecurve-inverse/
%{_datadir}/icons/LBluecurve/
%{_datadir}/icons/LBluecurve-inverse/
%{_datadir}/icons/Bluecurve-classic/
%{_datadir}/icons/Bluecurve-classic-inverse/

%changelog
