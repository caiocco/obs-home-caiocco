#
# spec file for package textadept
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# One CMake run builds the three front ends: textadept (Qt 6), textadept-gtk
# (GTK 3, chosen over GTK 2 when both are present) and textadept-curses.
# The dependencies are the exact archives upstream's CMakeLists.txt fetches
# (same SHA-256); %%prep puts them in build/_deps under the names CMake
# looks for, so FetchContent never touches the network.  The HTML manual is
# only in the binary release, so docs/ comes from there.
#
# textadept-modules is the official modules.zip (pure Lua, with upstream's
# Lua dependencies already in place).  Its prebuilt .so files are dropped
# and rebuilt here against the bundled Lua headers: file_diff (with
# diff-match-patch), spellcheck (system hunspell instead of the bundled
# copy, dictionaries from myspell-*) and the debugger's LuaSocket core.
# They go in %%{_libdir}/textadept, symlinked from the module dirs.  The
# update_notifier module is left out: updates come from the package.
#

%define scintilla_ver 568
%define scinterm_ver  6.0
%define scintillua_ver 6.8
%define lua_ver       5.5.1
%define lpeg_ver      1.1.0
%define lfs_ver       1_8_0
%define regex_ver     1.0
%define cdk_ver       t20260119
%define termkey_ver   0.22
%define reproc_ver    14.2.5
%define qtsa_commit   777e95ba69952f11eaec0adfb0cb987fabcdecb3
%define dmp_commit    7f95b37e554453262e2bcda830724fc362614103
%define luasocket_ver 3.0-rc1

Name:           textadept
Version:        13.1
Release:        0
Summary:        Fast, minimalist and extensible text editor (Qt version)
License:        BSD-3-Clause AND HPND AND MIT
Group:          Productivity/Text/Editors
URL:            https://orbitalquark.github.io/textadept/
Source0:        https://github.com/orbitalquark/textadept/archive/textadept_%{version}.tar.gz
Source1:        https://github.com/orbitalquark/textadept/releases/download/textadept_%{version}/textadept_%{version}.linux.tgz
Source2:        https://github.com/orbitalquark/textadept/releases/download/textadept_%{version}/textadept_%{version}.modules.zip
Source10:       https://www.scintilla.org/scintilla%{scintilla_ver}.tgz
Source11:       https://github.com/orbitalquark/scinterm/archive/scinterm_%{scinterm_ver}.zip
Source12:       https://github.com/orbitalquark/scintillua/archive/scintillua_%{scintillua_ver}.zip
Source13:       https://lua.org/ftp/lua-%{lua_ver}.tar.gz
Source14:       https://www.inf.puc-rio.br/~roberto/lpeg/lpeg-%{lpeg_ver}.tar.gz
Source15:       https://github.com/keplerproject/luafilesystem/archive/v%{lfs_ver}.zip#/luafilesystem-%{lfs_ver}.zip
Source16:       https://github.com/orbitalquark/lua-std-regex/archive/%{regex_ver}.zip#/lua-std-regex-%{regex_ver}.zip
Source17:       https://github.com/ThomasDickey/cdk-snapshots/archive/refs/tags/%{cdk_ver}.tar.gz#/cdk-snapshots-%{cdk_ver}.tar.gz
Source18:       https://www.leonerd.org.uk/code/libtermkey/libtermkey-%{termkey_ver}.tar.gz
Source19:       https://github.com/DaanDeMeyer/reproc/archive/refs/tags/v%{reproc_ver}.zip#/reproc-%{reproc_ver}.zip
Source20:       https://github.com/qtproject/qt-solutions/archive/%{qtsa_commit}.zip#/qt-solutions-777e95ba.zip
Source21:       https://github.com/leutloff/diff-match-patch-cpp-stl/archive/%{dmp_commit}.zip#/diff-match-patch-cpp-stl-7f95b37e.zip
Source22:       https://github.com/diegonehab/luasocket/archive/v%{luasocket_ver}.zip#/luasocket-%{luasocket_ver}.zip
# Upstream's install(CODE) links ignore DESTDIR; install .desktop files directly.
Patch0:         textadept-install-destdir.patch
BuildRequires:  cmake >= 3.22
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  unzip
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(ncursesw)
Requires:       %{name}-data = %{version}
Provides:       bundled(lpeg) = %{lpeg_ver}
Provides:       bundled(lua) = %{lua_ver}
Provides:       bundled(lua-std-regex) = %{regex_ver}
Provides:       bundled(luafilesystem) = 1.8.0
Provides:       bundled(qtsingleapplication)
Provides:       bundled(scintilla) = 5.6.8

%global _desc \
Textadept is a fast, minimalist and extensible cross-platform text editor\
for programmers. Most of it is written in Lua, which gives full control over\
the editor through scripts; it has syntax highlighting for over 100\
languages (Scintillua lexers), multiple carets and selections, split views,\
a command entry, snippets, find in files and a build/run system.

%description %{_desc}

This package contains the Qt 6 version, /usr/bin/textadept.

%package gtk
Summary:        Fast, minimalist and extensible text editor (GTK version)
Group:          Productivity/Text/Editors
Requires:       %{name}-data = %{version}
Provides:       bundled(lpeg) = %{lpeg_ver}
Provides:       bundled(lua) = %{lua_ver}
Provides:       bundled(lua-std-regex) = %{regex_ver}
Provides:       bundled(luafilesystem) = 1.8.0
Provides:       bundled(scintilla) = 5.6.8

%description gtk %{_desc}

This package contains the GTK 3 version, /usr/bin/textadept-gtk.

%package curses
Summary:        Fast, minimalist and extensible text editor (terminal version)
Group:          Productivity/Text/Editors
Requires:       %{name}-data = %{version}
Provides:       bundled(cdk) = %{cdk_ver}
Provides:       bundled(libtermkey) = %{termkey_ver}
Provides:       bundled(lpeg) = %{lpeg_ver}
Provides:       bundled(lua) = %{lua_ver}
Provides:       bundled(lua-std-regex) = %{regex_ver}
Provides:       bundled(luafilesystem) = 1.8.0
Provides:       bundled(reproc) = %{reproc_ver}
Provides:       bundled(scintilla) = 5.6.8
Provides:       bundled(scinterm) = %{scinterm_ver}

%description curses %{_desc}

This package contains the terminal (ncurses) version,
/usr/bin/textadept-curses.

%package data
Summary:        Lua core, lexers, themes and manual for Textadept
Group:          Productivity/Text/Editors
BuildArch:      noarch

%description data %{_desc}

This package contains the files shared by all Textadept front ends: the Lua
core and modules, Scintillua lexers, themes, translations and the manual.

%package modules
Summary:        Official extra modules for Textadept
Group:          Productivity/Text/Editors
License:        Apache-2.0 AND MIT
Requires:       %{name}-data = %{version}
Recommends:     myspell-dictionary
# The Lua language server runs textadept-curses as a background interpreter.
Recommends:     %{name}-curses
Provides:       bundled(diff-match-patch-cpp-stl)
Provides:       bundled(dkjson)
Provides:       bundled(ldoc) = 1.4.6
Provides:       bundled(lua-penlight) = 1.13.1
Provides:       bundled(lualogging) = 1.8.1
Provides:       bundled(luasocket) = %{luasocket_ver}
Provides:       bundled(mobdebug) = 0.80

%description modules %{_desc}

This package contains the official optional modules: debugger (Lua via
MobDebug, GDB, Go), export, file_diff, format, lsp (Language Server
Protocol client), lua_repl, open_file_mode, scratch and spellcheck.
Each one is enabled by adding e.g. "local lsp = require('lsp')" to
~/.textadept/init.lua.

%prep
%autosetup -p1 -n textadept-textadept_%{version}
# The HTML manual (Help > Manual / API Reference) only ships in the release.
tar xzf %{SOURCE1} --strip-components=1 --wildcards 'textadept/docs/*.html'
# The Qt and GTK entries both say "Textadept"; tell them apart in menus.
sed -i 's/^Name=Textadept$/Name=Textadept (GTK)/' src/textadept-gtk.desktop
mkdir -p build/_deps
cp -p %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE18} build/_deps/
cp -p %{SOURCE15} build/_deps/v%{lfs_ver}.zip
cp -p %{SOURCE16} build/_deps/%{regex_ver}.zip
cp -p %{SOURCE17} build/_deps/%{cdk_ver}.tar.gz
cp -p %{SOURCE19} build/_deps/v%{reproc_ver}.zip
cp -p %{SOURCE20} build/_deps/%{qtsa_commit}.zip
# Extra modules: drop prebuilt binaries, build files and update_notifier.
mkdir mods
unzip -q -d mods %{SOURCE2}
unzip -q -d mods %{SOURCE21}
unzip -q -d mods %{SOURCE22}
patch -d mods/luasocket-%{luasocket_ver} -p1 < mods/textadept-modules/debugger/luasocket.patch
pushd mods/textadept-modules
mv update_notifier ../update_notifier.unused
# Loaded as modules (the Lua LSP server runs under textadept-curses -L),
# never executed directly.
sed -i '1{/^#!/d}' lsp/ldoc.lua lsp/ldoc/markdown.lua lsp/server.lua
chmod 644 lsp/server.lua
find . \( -name '*.so' -o -name '*.dll' -o -name '*.patch' -o -name 'CMakeLists.txt' \
  -o -name Makefile -o -name .luacov -o -name .github -o -name '*.cxx' \
  -o -name 'en_US.aff' -o -name 'en_US.dic' \) -prune -printf '%%P\n' > ../dropped.list
popd

%build
# The bundled libraries (and reproc's own CMake project) are meant to be
# static; %%cmake's BUILD_SHARED_LIBS=ON would leave libreproc.so behind.
# FindCurses picks the narrow /usr/include/ncurses.h, which lacks the
# wide-character API (mvwin_wch, getcchar) that scinterm needs.
%cmake \
  -DBUILD_SHARED_LIBS=OFF \
  -DQT_DIR=%{_libdir}/cmake/Qt6 \
  -DCURSES_INCLUDE_PATH=%{_includedir}/ncursesw \
  -DTEXTADEPT_HOME=%{_datadir}/%{name} \
  -DQT=ON -DGTK3=ON -DGTK2=OFF -DCURSES=ON
%cmake_build

# Lua C modules: Lua API symbols are resolved from the textadept executables.
mods=$PWD/../mods
luainc=$PWD/_deps/lua-src/src
g++ %{optflags} -std=c++17 -fPIC -shared -I$mods/diff-match-patch-cpp-stl-%{dmp_commit} -I$luainc \
  $mods/textadept-modules/file_diff/diff.cxx -o $mods/diff.so
g++ %{optflags} -std=c++17 -fPIC -shared -I$luainc $(pkg-config --cflags hunspell) \
  $mods/textadept-modules/spellcheck/spell.cxx -o $mods/spell.so $(pkg-config --libs hunspell)
pushd $mods/luasocket-%{luasocket_ver}/src
gcc %{optflags} -fPIC -shared -DLUASOCKET_NODEBUG -DLUA_NOCOMPAT_MODULE -I$luainc \
  auxiliar.c buffer.c except.c inet.c io.c luasocket.c options.c select.c tcp.c \
  timeout.c udp.c usocket.c -o $mods/core.so
popd

%install
%cmake_install

# Extra modules.
moddir=%{buildroot}%{_datadir}/%{name}/modules
(cd mods/textadept-modules && tar cf - --exclude-from=../dropped.list .) | tar xf - -C $moddir
install -Dm755 mods/diff.so %{buildroot}%{_libdir}/%{name}/file_diff/diff.so
install -Dm755 mods/spell.so %{buildroot}%{_libdir}/%{name}/spellcheck/spell.so
install -Dm755 mods/core.so %{buildroot}%{_libdir}/%{name}/debugger/socket/core.so
ln -sr %{buildroot}%{_libdir}/%{name}/file_diff/diff.so $moddir/file_diff/diff.so
ln -sr %{buildroot}%{_libdir}/%{name}/spellcheck/spell.so $moddir/spellcheck/spell.so
ln -sr %{buildroot}%{_libdir}/%{name}/debugger/socket/core.so $moddir/debugger/lua/socket/core.so
for m in debugger export file_diff format lsp lua_repl open_file_mode scratch spellcheck; do
  echo "%{_datadir}/%{name}/modules/$m" >> modules.files
done
%fdupes %{buildroot}%{_datadir}/%{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
# The C modules get the Lua API from the executable they are loaded into;
# make sure every lua* symbol they need is exported by all three.
for exe in textadept textadept-gtk textadept-curses; do
  nm -D --defined-only %{buildroot}%{_bindir}/$exe | awk '{print $3}' | sort -u > $exe.syms
  for so in $(find %{buildroot}%{_libdir}/%{name} -name '*.so'); do
    for sym in $(nm -D --undefined-only $so | awk '{print $2}' | grep '^lua'); do
      grep -qx "$sym" $exe.syms || { echo "$exe lacks $sym (${so##*/})"; exit 1; }
    done
  done
done

%files
%{_bindir}/textadept
%{_datadir}/applications/textadept.desktop

%files gtk
%{_bindir}/textadept-gtk
%{_datadir}/applications/textadept-gtk.desktop

%files curses
%{_bindir}/textadept-curses
%{_datadir}/applications/textadept-curses.desktop

%files data
%license LICENSE
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/LICENSE
%exclude %{_datadir}/%{name}/modules/[!t]*
%{_datadir}/icons/hicolor/scalable/apps/textadept.svg

%files modules -f modules.files
%{_libdir}/%{name}

%changelog
