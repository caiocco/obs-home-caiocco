#
# spec file for package outwiker
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Replaces the Flatpak (net.jenyay.Outwiker): the Flatpak ignores the GTK
# theme and its WebKit preview stays blank on this system.  Installed the
# way upstream's Makefile does it (program in /usr/share/outwiker, plugins
# in /usr/share/outwiker/plugins).  The plugins keep their bundled Python
# libraries (Pygments, Markdown, bs4, html5lib, Jinja2, blockdiag...).
# Upstream builds against wxPython 4.3; Leap 16.0 has 4.2.3 (the Flatpak
# itself ships 4.2.5).
#

%define tag_name    4.1.0-stable

Name:           outwiker
Version:        4.1.0.982
Release:        0
Summary:        Outliner and personal wiki that keeps notes in a tree
License:        GPL-3.0-or-later AND MIT AND BSD-2-Clause AND BSD-3-Clause AND Apache-2.0 AND LGPL-2.1-or-later
Group:          Productivity/Office/Other
URL:            https://jenyay.net/Outwiker/English
Source0:        https://github.com/Jenyay/outwiker/archive/refs/tags/%{tag_name}.tar.gz#/outwiker-%{tag_name}.tar.gz
# Upstream forces GTK_THEME=":light", which throws away the user's theme;
# only replace dark themes (by their light variant or Adwaita) instead
Patch0:         outwiker-avoid-dark-gtk-theme.patch
# Also offer the system hunspell dictionaries (e.g. myspell-pt_BR)
Patch1:         outwiker-system-hunspell-dicts.patch
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  hicolor-icon-theme
BuildRequires:  python-rpm-macros
BuildRequires:  python3
# for the import test in %%check
BuildRequires:  python3-Pillow
BuildRequires:  python3-chunspell
BuildRequires:  python3-idna
BuildRequires:  python3-pyparsing
BuildRequires:  python3-rcssmin
BuildRequires:  python3-six
BuildRequires:  python3-wxPython >= 4.2
Requires:       python3-Pillow
Requires:       python3-chunspell
Requires:       python3-idna
Requires:       python3-pyparsing
Requires:       python3-rcssmin
# used by the bundled python-dateutil (datagraph plugin)
Requires:       python3-six
Requires:       python3-wxPython >= 4.2
BuildArch:      noarch

%description
OutWiker is designed to store notes in a tree.  Such programs are called
outliners, personal wikis or tree-like editors.  Unlike most of them,
OutWiker keeps the tree as directories on disk, and pages can carry
attachments, tags and icons.  Pages can be plain text, HTML, wiki
(with its own wiki notation), Markdown or web pages saved from the
Internet.

This build includes the official plugins (Markdown, source code
highlighting, diagrams, snippets, table of contents, LaTeX equations,
web page saving and others).

%prep
%autosetup -p1 -n outwiker-%{tag_name}

%build
# Nothing to build

%install
%make_install
rm -r %{buildroot}%{_datadir}/outwiker/outwiker/tests
rm %{buildroot}%{_datadir}/outwiker/README %{buildroot}%{_datadir}/outwiker/copyright.txt

# Upstream's launcher does "cd /usr/share/outwiker", which breaks
# relative paths given on the command line
cat > %{buildroot}%{_bindir}/outwiker <<'EOF'
#!/bin/sh
exec %{__python3} %{_datadir}/outwiker/runoutwiker.py "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/outwiker

# Modules, not scripts
find %{buildroot}%{_datadir}/outwiker -name '*.py' -perm /111 -exec chmod 644 {} +
sed -i '1{/^#!/d}' %{buildroot}%{_datadir}/outwiker/runoutwiker.py \
                   %{buildroot}%{_datadir}/outwiker/outwiker/__main__.py

# Desktop file under the id the AppStream metadata refers to
rm %{buildroot}%{_datadir}/applications/outwiker.desktop
sed -e 's/^Categories=.*/Categories=Office;/' \
    -e '/^Icon=/a StartupWMClass=runoutwiker.py' \
    need_for_build/linux/outwiker.desktop > net.jenyay.Outwiker.desktop
install -Dpm 0644 net.jenyay.Outwiker.desktop %{buildroot}%{_datadir}/applications/net.jenyay.Outwiker.desktop
install -Dpm 0644 need_for_build/linux/net.jenyay.Outwiker.appdata.xml %{buildroot}%{_datadir}/metainfo/net.jenyay.Outwiker.metainfo.xml

%py3_compile %{buildroot}%{_datadir}/outwiker
%fdupes %{buildroot}%{_datadir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/net.jenyay.Outwiker.desktop
# The program and its dependencies import (no display needed); importing
# the core already creates the config directory
export HOME=$(mktemp -d)
export XDG_CONFIG_HOME=$HOME/.config
mkdir -p $XDG_CONFIG_HOME
cd /
PYTHONPATH=%{buildroot}%{_datadir}/outwiker %{__python3} -c "
import outwiker, outwiker.core.system, outwiker.core.htmltemplate, outwiker.app.owapplication
print('OutWiker', outwiker.__version_str__, 'imports OK')
"

%files
%license LICENSE.txt
%doc README.md copyright.txt
%{_bindir}/outwiker
%{_datadir}/outwiker
%{_datadir}/applications/net.jenyay.Outwiker.desktop
%{_datadir}/metainfo/net.jenyay.Outwiker.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/outwiker.*
%{_datadir}/pixmaps/outwiker.png
%{_datadir}/pixmaps/outwiker.xpm
%{_mandir}/man1/outwiker.1%{?ext_man}
%{_mandir}/ru/man1/outwiker.1%{?ext_man}

%changelog
