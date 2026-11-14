#
# spec file for package axene-office
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define axene_data  %{_datadir}/axene
%define axene_exec  %{_libexecdir}/axene
%define axene_apps  XAllWrite Xclamation XQuad XMayday AxeneOffice

Name:           axene-office
Version:        2.0.1
Release:        0
Summary:        Motif office suite: word processor, DTP, spreadsheet and help browser
License:        GPL-2.0-or-later
Group:          Productivity/Office/Suite
URL:            http://linuxmafia.com/pub/linux/apps/axene/
# Made from AxeneSDK-v2.0.1.tar.gz (see URL) by Source99, which removes the
# non-redistributable Adobe/Linotype Type 1 fonts:
#   sh prune-nonfree-fonts.sh AxeneSDK-v2.0.1.tar.gz .
Source0:        %{name}-%{version}.tar.xz
Source1:        axene-launcher.in
Source99:       prune-nonfree-fonts.sh
# PATCH-FIX-OPENSUSE axene-office-modern-toolchain.patch -- build with GCC 15/glibc 2.40 on LP64: varargs.h -> stdarg.h, ISO token pasting, <stdint.h> types, strerror, missing ';' and string continuation
Patch0:         axene-office-modern-toolchain.patch
# PATCH-FIX-OPENSUSE axene-office-ximage-bpp.patch -- probe bits per pixel with a valid XImage; modern Xlib rejected the old one, so 32 bpp screens were handled as 24 bpp and icon loading overflowed
Patch1:         axene-office-ximage-bpp.patch
# PATCH-FIX-OPENSUSE axene-office-urw-fonts.patch -- use .pfb names for the standard fonts (URW replacements linked in %%install)
Patch2:         axene-office-urw-fonts.patch
# PATCH-FIX-OPENSUSE axene-office-no-launcher-killpg.patch -- XAllWrite took any init-parented start (AxeneOffice bar, double-forking launchers) for the uninstalled Axene Launcher and on exit sent SIGUSR1 to the whole launching process group, killing the window manager or the X session
Patch3:         axene-office-no-launcher-killpg.patch
# PATCH-FIX-OPENSUSE axene-office-lp64-window-ids.patch -- the internal document window manager of XAllWrite, Xclamation and XQuad passed an int where XGetGeometry and XQueryTree store a Window (8 bytes on LP64): stack smashing abort when the main window was resized or a document iconified
Patch4:         axene-office-lp64-window-ids.patch
# PATCH-FIX-OPENSUSE axene-office-dead-keys.patch -- XAllWrite and Xclamation read the keyboard with XLookupString, which does not compose dead keys: typing an accent on us-intl or ABNT2 layouts inserted the spacing accent and the bare letter; compose them into Latin-1
Patch5:         axene-office-dead-keys.patch
# PATCH-FIX-OPENSUSE axene-office-about-authors.patch -- Xclamation's Help > mAuthor item (no label, no mnemonic) freed its dialog with the wrong destructor and crashed on Ok: drop it and add a translated authors line to every About box, whose release line was lost to an overlapping sprintf; pin the status bar font to the oblique Helvetica of the original look
Patch6:         axene-office-about-authors.patch
# PATCH-FIX-OPENSUSE axene-office-launcher-close.patch -- closing the AxeneOffice bar from the window manager destroyed its window but left the process running: quit on WM_DELETE_WINDOW
Patch7:         axene-office-launcher-close.patch
# PATCH-FEATURE-OPENSUSE axene-office-more-urw-fonts.patch -- offer Bookman, Palatino and Zapf Chancery (URW clones linked in %%install) besides the eight families Axene shipped
Patch8:         axene-office-more-urw-fonts.patch
# PATCH-FIX-OPENSUSE axene-office-wm-close.patch -- closing XQuad, XAllWrite, Xclamation or an XMayday window from the window manager destroyed it but left the process running with no window: ask to quit (or close that XMayday window) instead
Patch9:         axene-office-wm-close.patch
# PATCH-FIX-OPENSUSE axene-office-lp64-drop-data.patch -- the frame list pointer sent in drag-and-drop ClientMessages was rebuilt by adding its sign-extended low half: dragging a frame (e.g. a rectangle) to the trash or to another place crashed when bit 31 of that half was set
Patch10:        axene-office-lp64-drop-data.patch
# PATCH-FIX-OPENSUSE axene-office-xquad-header-font.patch -- XQuad drew the row and column headers with its 1-bit Type 1 rasterizer, which made jagged digits and letters at 12 px: use the closest core X bitmap Helvetica, as the rest of the UI does
Patch11:        axene-office-xquad-header-font.patch
# PATCH-FIX-OPENSUSE axene-office-dialog-placement.patch -- dialogs were centred over where their parent was when first created (or over the hidden shell in the middle of the X screen, i.e. on the second monitor): centre them over the application window at each popup
Patch12:        axene-office-dialog-placement.patch
# PATCH-FIX-OPENSUSE axene-office-window-placement.patch -- the help browser always opened at the right edge of the whole X screen: dock it beside the window that asked for help (same height); the launcher bar reopens where it was left, in its last layout and modes
Patch13:        axene-office-window-placement.patch
BuildRequires:  desktop-file-utils
BuildRequires:  ed
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  ghostscript-fonts-std
BuildRequires:  gperf
BuildRequires:  make
BuildRequires:  motif-devel
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xt)
# Type 1 URW clones of the standard PostScript fonts, linked from
# %%{axene_data}/fonts (Leap's urw-base35-fonts is OpenType only)
Requires:       ghostscript-fonts-std
Requires:       xorg-x11-fonts-core
# the interface asks for 75/100 dpi helvetica and lucidatypewriter bitmaps
Requires:       xorg-x11-fonts-legacy

%description
Axene Office is a Motif office suite for X11, formerly proprietary
(1994-2000) and re-released by Axene under the GNU GPL.

It contains:
- XAllWrite, a frame-oriented word processor;
- Xclamation, a desktop publishing program;
- XQuad, a spreadsheet with charts and Excel/text import;
- XMayday, the HTML help browser used by the other programs;
- AxeneOffice, a small launch bar for them.

The documents use their own formats; text and HTML can be imported and
exported. The user interface and the help pages follow the locale:
English, French, German or Spanish (German and Spanish fall back to
the English help pages, and XAllWrite has no German translation);
set AXENE_LANGUAGE to override.

%prep
%autosetup -p1
# The SDK ships without these empty directories; the header linking
# script runs "rm -f *" in the wrong directory when Headers is missing.
for app in %{axene_apps}; do
  mkdir -p $app-%{version}/Sources/Headers $app-%{version}/Sources/lib
done

%build
# K&R C from the nineties: gnu89 with the pre-GCC 14 diagnostics
export CC=gcc
export CFLAGS="%{optflags} -std=gnu89 -fpermissive -fcommon -fno-strict-aliasing -Wno-return-type -Wno-implicit-int -Wno-return-mismatch -Wno-incompatible-pointer-types -Wno-int-conversion -Wno-implicit-function-declaration -Wno-unused -Wno-parentheses -Wno-pointer-sign"
export CPPFLAGS="-D___PSEUDO_COMPOSE_MACRO -D___linux_glibc -D_NO_PROTO"
export LDFLAGS="%{?build_ldflags}"
export SOCK_LIBS=""
export MOTIF_LIBS="-lXm -lXpm"
export X11_LIBS="-lXt -lSM -lICE -lXext -lXinerama -lXmu -lX11"
export X11CONFIG='-DXc_XTOP=\"%{axene_data}/X11\"'
export ARFLAGS=rvs
export SYSTEM_NAME="Linux %{_arch}" PACKAGE_NAME="%{_arch}-linux-glibc"
for app in %{axene_apps}; do
  pushd $app-%{version}/Sources
  Utils/mkmakefile
  make buildenv
  # the products' makefiles are not parallel-safe
  make notrace
  test -x main
  popd
done

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{axene_exec} \
  %{buildroot}%{axene_data}/{locale,lang,fonts,metrics,X11,license,doc} \
  %{buildroot}%{_datadir}/pixmaps %{buildroot}%{_datadir}/applications

for app in %{axene_apps}; do
  src=$app-%{version}/Sources
  lc=$(echo $app | tr A-Z a-z)
  install -m0755 $src/main %{buildroot}%{axene_exec}/$app
  install -m0644 $src/AD/$app.English.* $src/AD/$app.French \
    $src/AD/$app.German $src/AD/$app.Spanish %{buildroot}%{axene_data}/locale/
  if [ -f $src/RC/${lc}rc.English.us ]; then
    install -m0644 $src/RC/${lc}rc.* %{buildroot}%{axene_data}/locale/
  fi
  if [ -f $src/PostScript/xcalibur.prc ]; then
    install -m0644 $src/PostScript/xcalibur.prc %{buildroot}%{axene_data}/
  fi
  if [ -d $app-%{version}/Documentation ]; then
    cp -a $app-%{version}/Documentation %{buildroot}%{axene_data}/doc/$app
  fi
  install -m0644 Archives-%{version}/Icons/$app.bin.xpm \
    %{buildroot}%{_datadir}/pixmaps/$lc.xpm

  # Launcher: the environment the original launch scripts set up
  # (AXENE_LIB plus every <APP>_LIB, which the rc files use for the help
  # location), with the language picked from the locale at run time
  # instead of once at install time
  sed -e "s|@APP@|$app|g" \
      -e "s|@DATA@|%{axene_data}|g" -e "s|@EXEC@|%{axene_exec}|g" \
      %{SOURCE1} > %{buildroot}%{_bindir}/$app
  chmod 0755 %{buildroot}%{_bindir}/$app
done

# One library tree per language, as the original per-install postinstall
# symlinks made: <app>rc and app-defaults for that language, everything
# else shared
for lang in English.us English.uk French German Spanish; do
  d=%{buildroot}%{axene_data}/lang/$lang
  install -d $d/app-defaults
  for x in fonts metrics X11 license doc locale xcalibur.prc; do
    ln -s ../../$x $d/$x
  done
  for app in %{axene_apps}; do
    lc=$(echo $app | tr A-Z a-z)
    l=$lang
    # XAllWrite was still a beta: its German resources are incomplete
    # (English labels, some missing), so use the English ones
    [ $app-$lang = XAllWrite-German ] && l=English.us
    ln -s ../../../locale/$app.$l $d/app-defaults/$app
    if [ -f %{buildroot}%{axene_data}/locale/${lc}rc.$l ]; then
      ln -s ../../locale/${lc}rc.$l $d/${lc}rc
    fi
  done
done

# editor leftovers in the documentation
find %{buildroot}%{axene_data}/doc -name '*~' -delete

common=Common-%{version}/lib
install -m0644 $common/X11/XKeysymDB %{buildroot}%{axene_data}/X11/
install -m0644 $common/fonts/put*.pfa %{buildroot}%{axene_data}/fonts/
install -m0644 $common/metrics/put*.afm %{buildroot}%{axene_data}/metrics/
install -m0644 Archives-%{version}/InfoFiles/LICENSE %{buildroot}%{axene_data}/license/
# Standard PostScript names -> URW Type 1 clones (ghostscript-fonts-std)
while read ps urw; do
  ln -s %{_datadir}/fonts/ghostscript/$urw.pfb %{buildroot}%{axene_data}/fonts/$ps.pfb
  ln -s %{_datadir}/fonts/ghostscript/$urw.afm %{buildroot}%{axene_data}/metrics/$ps.afm
done <<EOF
Times-Roman n021003l
Times-Bold n021004l
Times-Italic n021023l
Times-BoldItalic n021024l
Helvetica n019003l
Helvetica-Bold n019004l
Helvetica-Oblique n019023l
Helvetica-BoldOblique n019024l
Courier n022003l
Courier-Bold n022004l
Courier-Oblique n022023l
Courier-BoldOblique n022024l
Bookman-Light b018012l
Bookman-Demi b018015l
Bookman-LightItalic b018032l
Bookman-DemiItalic b018035l
Palatino-Roman p052003l
Palatino-Bold p052004l
Palatino-Italic p052023l
Palatino-BoldItalic p052024l
ZapfChancery-MediumItalic z003034l
Symbol s050000l
AvantGarde-Book a010013l
AvantGarde-BookOblique a010033l
AvantGarde-Demi a010015l
AvantGarde-DemiOblique a010035l
NewCenturySchlbk-Roman c059013l
NewCenturySchlbk-Bold c059016l
NewCenturySchlbk-Italic c059033l
NewCenturySchlbk-BoldItalic c059036l
ZapfDingbats d050000l
EOF

# Desktop entries
desktop() {
  cat > %{buildroot}%{_datadir}/applications/$1.desktop <<EOF
[Desktop Entry]
Type=Application
Name=$2
GenericName=$3
Comment=$4
Exec=$5
Icon=$1
Terminal=false
Categories=$6
EOF
}
desktop xallwrite XAllWrite "Word Processor" "Axene word processor (Motif)" "XAllWrite %%F" "Office;WordProcessor;"
desktop xclamation Xclamation "Desktop Publishing" "Axene desktop publishing (Motif)" "Xclamation %%F" "Office;Publishing;"
desktop xquad XQuad "Spreadsheet" "Axene spreadsheet (Motif)" "XQuad %%F" "Office;Spreadsheet;"
desktop xmayday XMayday "Help Browser" "Axene Office documentation" "XMayday" "Office;Documentation;"
desktop axeneoffice "Axene Office" "Office Launcher" "Launch bar for the Axene Office programs" "AxeneOffice" "Office;"

# documentation images are shared between the programs
%fdupes -s %{buildroot}%{axene_data}

%check
for f in %{buildroot}%{_datadir}/applications/*.desktop; do
  desktop-file-validate $f
done

%files
%license Archives-%{version}/InfoFiles/LICENSE
%doc Archives-%{version}/InfoFiles/README
%{_bindir}/AxeneOffice
%{_bindir}/XAllWrite
%{_bindir}/XMayday
%{_bindir}/XQuad
%{_bindir}/Xclamation
%{axene_exec}
%{axene_data}
%{_datadir}/pixmaps/*.xpm
%{_datadir}/applications/*.desktop

%changelog
