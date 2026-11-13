#
# spec file for package ted
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define ted_langs bg_BG cs_CZ da_DK de_DE en_GB es_AR es_ES fi_FI fr_FR hr_HR hu_HU it_IT mg_MG nb_NO nl_NL pl_PL pt_BR pt_PT ru_RU sk_SK sv_SE

Name:           ted
Version:        2.23
Release:        0
Summary:        Easy rich text processor (RTF) for X11
License:        GPL-2.0-or-later
Group:          Productivity/Office/Word Processor
URL:            https://ftp.nluug.nl/pub/editors/ted/
Source0:        https://ftp.nluug.nl/pub/editors/ted/%{name}-%{version}.src.tar.gz
Source1:        ted.desktop
Source2:        ted-gtk.desktop
# Brazilian Portuguese spelling automaton, built from VERO (myspell-pt_BR)
Source3:        ted-pt_BR-wordlist.py
Source4:        ted-mkdfa.c
# Localization tarballs (unversioned upstream; released together with 2.23)
Source10:       https://ftp.nluug.nl/pub/editors/ted/ted_bg_BG.tar.gz
Source11:       https://ftp.nluug.nl/pub/editors/ted/ted_cs_CZ.tar.gz
Source12:       https://ftp.nluug.nl/pub/editors/ted/ted_da_DK.tar.gz
Source13:       https://ftp.nluug.nl/pub/editors/ted/ted_de_DE.tar.gz
Source14:       https://ftp.nluug.nl/pub/editors/ted/ted_en_GB.tar.gz
Source15:       https://ftp.nluug.nl/pub/editors/ted/ted_es_AR.tar.gz
Source16:       https://ftp.nluug.nl/pub/editors/ted/ted_es_ES.tar.gz
Source17:       https://ftp.nluug.nl/pub/editors/ted/ted_fi_FI.tar.gz
Source18:       https://ftp.nluug.nl/pub/editors/ted/ted_fr_FR.tar.gz
Source19:       https://ftp.nluug.nl/pub/editors/ted/ted_hr_HR.tar.gz
Source20:       https://ftp.nluug.nl/pub/editors/ted/ted_hu_HU.tar.gz
Source21:       https://ftp.nluug.nl/pub/editors/ted/ted_it_IT.tar.gz
Source22:       https://ftp.nluug.nl/pub/editors/ted/ted_mg_MG.tar.gz
Source23:       https://ftp.nluug.nl/pub/editors/ted/ted_nb_NO.tar.gz
Source24:       https://ftp.nluug.nl/pub/editors/ted/ted_nl_NL.tar.gz
Source25:       https://ftp.nluug.nl/pub/editors/ted/ted_pl_PL.tar.gz
Source26:       https://ftp.nluug.nl/pub/editors/ted/ted_pt_BR.tar.gz
Source27:       https://ftp.nluug.nl/pub/editors/ted/ted_pt_PT.tar.gz
Source28:       https://ftp.nluug.nl/pub/editors/ted/ted_ru_RU.tar.gz
Source29:       https://ftp.nluug.nl/pub/editors/ted/ted_sk_SK.tar.gz
Source30:       https://ftp.nluug.nl/pub/editors/ted/ted_sv_SE.tar.gz
# PATCH-FIX-UPSTREAM ted-2.23-memory-bugs.patch -- PNG palette heap overflow, uninitialized time_t in ZIP/EPUB, SVG pattern viewBox height
Patch0:         ted-2.23-memory-bugs.patch
# PATCH-FIX-UPSTREAM ted-2.23-motif-xft-default-font.patch -- crash when the Motif renderTable font is Xft (CDE/NsCDE *renderTable resources)
Patch1:         ted-2.23-motif-xft-default-font.patch
# PATCH-FIX-UPSTREAM ted-2.23-gtk-default-font-size.patch -- use the GTK theme font size (points) instead of a fixed 10px
Patch2:         ted-2.23-gtk-default-font-size.patch
# PATCH-FIX-UPSTREAM ted-2.23-motif-selection-format32.patch -- X BadValue exit on 64-bit when another client asks for TARGETS (format 8*sizeof(Atom)=64)
Patch3:         ted-2.23-motif-selection-format32.patch
# PATCH-FEATURE-OPENSUSE ted-2.23-motif-center-on-pointer-monitor.patch -- center new Motif windows on the monitor under the pointer instead of at 0,0
Patch4:         ted-2.23-motif-center-on-pointer-monitor.patch
# PATCH-FIX-UPSTREAM ted-2.23-gtk-ibeam-cursor.patch -- the GTK text area never got the I-beam cursor (Motif sets it with XDefineCursor)
Patch5:         ted-2.23-gtk-ibeam-cursor.patch
# PATCH-FIX-UPSTREAM ted-2.23-motif-format-tool-size.patch -- Motif text boxes sized by the widest Xft glyph made the Format Tool ~2x too wide; make the tool resizable
Patch6:         ted-2.23-motif-format-tool-size.patch
# PATCH-FEATURE-OPENSUSE ted-2.23-motif-xft-ruler-text.patch -- draw ruler numbers and the "Page n/n, Section n/n" line with the Xft renderTable font (antialiased) instead of a core bitmap font
Patch7:         ted-2.23-motif-xft-ruler-text.patch
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  libjpeg8-devel
BuildRequires:  libpaper-devel
BuildRequires:  libtiff-devel
BuildRequires:  make
BuildRequires:  motif-devel
BuildRequires:  myspell-pt_BR
BuildRequires:  pcre-devel
BuildRequires:  pkgconfig
BuildRequires:  python3-base
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(zlib)
Requires:       %{name}-common = %{version}-%{release}
Provides:       ted-motif = %{version}-%{release}

%description
Ted is a text processor running under X11. It edits rich text (RTF)
documents in a WYSIWYG way, supports multiple fonts, tables, images,
footnotes and a spelling checker, and prints to PostScript.
From the command line it also converts RTF to PostScript, PDF, HTML,
EPUB and plain text.

This package contains the classic Motif version of Ted.

%package gtk
Summary:        Easy rich text processor (RTF) - GTK+ 2 version
Group:          Productivity/Office/Word Processor
Requires:       %{name}-common = %{version}-%{release}

%description gtk
Ted is a text processor running under X11. It edits rich text (RTF)
documents in a WYSIWYG way.

This package contains Ted built with GTK+ 2, installed as Ted-gtk.

%package common
Summary:        Data files shared by the Motif and GTK+ versions of Ted
Group:          Productivity/Office/Word Processor
Recommends:     ghostscript
Recommends:     urw-base35-fonts
BuildArch:      noarch

%description common
Font metrics, the American English spelling dictionary, the manual,
PostScript helpers and the rtf2pdf/rtf2ps/rtf2html/rtf2txt/rtf2epub
conversion scripts used by Ted.

%package spell
Summary:        Spelling dictionaries for Ted
Group:          Productivity/Office/Word Processor
Requires:       %{name}-common = %{version}-%{release}
BuildArch:      noarch

%description spell
Spelling dictionaries for Ted: Bulgarian, Croatian, Czech, Danish,
Dutch, British English, Finnish, French, German, Italian, Norwegian
Bokmaal, Polish, Portuguese (Brazil and Portugal), Russian, Slovak,
Spanish and Swedish.

The Brazilian Portuguese dictionary is generated from VERO
(myspell-pt_BR) at build time.

%package lang
Summary:        Translations and localized manuals for Ted
Group:          Productivity/Office/Word Processor
Requires:       %{name}-common = %{version}-%{release}
BuildArch:      noarch

%description lang
User interface translations of Ted (Czech, Danish, Dutch, French,
German, Hungarian, Italian, Malagasy, Norwegian, Polish, Portuguese
(Brazil), Slovak and Spanish), plus the German, French and Malagasy
manuals. Ted picks the translation from the locale at startup.

%prep
%autosetup -p1 -n Ted-%{version}
cp -a . ../Ted-%{version}-gtk

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
opts="--prefix=%{_prefix} --datadir=%{_datadir} --libdir=%{_libdir}"
make CONFIGURE_OPTIONS="$opts --with-MOTIF" compile.shared
# pt_BR.dfa: upstream ships no Brazilian dictionary; derive a clean
# word list from VERO and compile it with Ted's own automaton library
gcc $CFLAGS -Iind -IappUtil -ItextEncoding -Iinclude -o mkdfa %{SOURCE4} \
    lib/ind.a lib/textEncoding.a lib/appUtil.a
python3 %{SOURCE3} %{_datadir}/hunspell/pt_BR.aff %{_datadir}/hunspell/pt_BR.dic \
    | ./mkdfa pt_BR.dfa
cd ../Ted-%{version}-gtk
make CONFIGURE_OPTIONS="$opts --with-GTK" compile.shared

%install
install -Dpm 0755 Ted/Ted %{buildroot}%{_bindir}/Ted
install -Dpm 0755 ../Ted-%{version}-gtk/Ted/Ted %{buildroot}%{_bindir}/Ted-gtk

install -d %{buildroot}%{_datadir}/Ted
tar xf tedPackage/TedDatadir.tar -C %{buildroot}%{_datadir}/Ted --no-same-owner
# The upstream gtkrc squeezes the GTK tool window (zero x/ythickness,
# "Sans 7", 8px option menu indicators), which breaks most themes.
# Let the theme draw the widgets; keep the original for reference.
cd %{buildroot}%{_datadir}/Ted/config
mv ted.gtkrc-2.0 ted.gtkrc-2.0.upstream
cat > ted.gtkrc-2.0 <<'GTKRC'
# Ted reads this file before the user's ~/.gtkrc-2.0.
# The upstream compact styles for the Format Tool are kept in
# ted.gtkrc-2.0.upstream; include it from ~/.gtkrc-2.0 to use them.
GTKRC
cd -

for t in %{ted_langs}; do
    tar xzf %{_sourcedir}/ted_$t.tar.gz -C %{buildroot} --no-same-owner \
        --exclude='usr/share/Ted/varia/*'
done
install -pm 0644 pt_BR.dfa %{buildroot}%{_datadir}/Ted/dfa/pt_BR.dfa
cat >> %{buildroot}%{_datadir}/Ted/Ted-pt_BR.properties <<'PROPS'
Ted.NAME_pt_BR:	Português (Brasil)
Ted.NAME_pt_PT:	Português (Portugal)
PROPS

# Man pages, with the data directory filled in
install -d %{buildroot}%{_mandir}/man1
for m in Ted rtf2pdf rtf2ps; do
    sed -e 's:@DATADIR@:%{_datadir}:g' %{buildroot}%{_datadir}/Ted/doc/$m.1 \
        > %{buildroot}%{_mandir}/man1/$m.1
done
ln -s Ted.1 %{buildroot}%{_mandir}/man1/Ted-gtk.1

# Conversion scripts
for s in rtf2pdf rtf2ps rtf2html rtf2txt rtf2epub; do
    ln -s ../share/Ted/examples/$s.sh %{buildroot}%{_bindir}/$s
done

install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/ted.desktop
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/ted-gtk.desktop
install -Dpm 0644 %{buildroot}%{_datadir}/Ted/Ted.png %{buildroot}%{_datadir}/pixmaps/ted.png

chmod 0644 %{buildroot}%{_datadir}/Ted/*.rtf %{buildroot}%{_datadir}/Ted/*.properties
chmod 0755 %{buildroot}%{_datadir}/Ted/examples/*.sh %{buildroot}%{_datadir}/Ted/fontsdocs/*.sh

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/ted.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/ted-gtk.desktop

%files
%{_bindir}/Ted
%{_datadir}/applications/ted.desktop

%files gtk
%{_bindir}/Ted-gtk
%{_mandir}/man1/Ted-gtk.1%{?ext_man}
%{_datadir}/applications/ted-gtk.desktop

%files common
%license gpl.txt
%{_bindir}/rtf2*
%{_mandir}/man1/Ted.1%{?ext_man}
%{_mandir}/man1/rtf2pdf.1%{?ext_man}
%{_mandir}/man1/rtf2ps.1%{?ext_man}
%{_datadir}/pixmaps/ted.png
%dir %{_datadir}/Ted
%{_datadir}/Ted/afm
%{_datadir}/Ted/config
%dir %{_datadir}/Ted/dfa
%{_datadir}/Ted/dfa/en_US.dfa
%{_datadir}/Ted/doc
%{_datadir}/Ted/examples
%{_datadir}/Ted/fontsdocs
%{_datadir}/Ted/ps
%{_datadir}/Ted/varia
%{_datadir}/Ted/Ted.png
%{_datadir}/Ted/TedDocument-en_US.rtf

%files spell
%{_datadir}/Ted/dfa/*.dfa
%exclude %{_datadir}/Ted/dfa/en_US.dfa

%files lang
%{_datadir}/Ted/Ted-*.properties
%{_datadir}/Ted/TedDocument-de_DE.rtf
%{_datadir}/Ted/TedDocument-fr_FR.rtf
%{_datadir}/Ted/TedDocument-mg_MG.rtf

%changelog
