#!/bin/sh
# Make the Chicago95 source tarball used by chicago95.spec, without the
# files that reproduce Microsoft artwork. The Microsoft files never reach
# OBS this way.
#
# The list and the relinking follow Clay Risser's Debian packaging
# (debian/drop-microsoft-assets.sh and Files-Excluded in debian/copyright,
# home:clayrisser:unstable/chicago95, 3.0.1+git20260803.e89583c+ds-1).
#
# usage: prune-microsoft-assets.sh /path/to/Chicago95-git-checkout [outdir]
# Writes chicago95-<version>.tar.xz into outdir (default: current directory).

# No set -e: the find|while loops end on a false test by design.
set -u

src=${1:?usage: $0 CHECKOUT [OUTDIR]}
out=$(cd "${2:-.}" && pwd)

hash=$(git -C "$src" rev-parse --short=7 HEAD)
date=$(git -C "$src" log -1 --format=%cd --date=format:%Y%m%d)
ver=3.0.1+git$date.$hash
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
root=$work/chicago95-$ver
git -C "$src" archive --prefix="chicago95-$ver/" HEAD | tar x -C "$work" || exit 1

bad_stem() {
	case $1 in
	application-msword | x-office-document | x-office-document-template | x-office-document-templat | \
	libreoffice-text | libreoffice-text-template | \
	application-vnd.ms-excel | x-office-spreadsheet | x-office-spreadsheet-template | \
	libreoffice-spreadsheet | libreoffice-spreadsheet-template | libreoffice-calc | \
	application-vnd.ms-powerpoint | x-office-presentation | x-office-presentation-template | \
	libreoffice-presentation | libreoffice-presentation-template | \
	application-vnd.ms-access | libreoffice-database | libreoffice-base | \
	msaccess.exe_14_259_4_48x48x4 | application-x-ms-dos-executable | \
	im-msn | im-msn_2 | im-msn_48 | \
	internet-web-browser | web-browser | gnome-web-browser | redhat-web-browser | \
	computer | computer-symbolic | desktop_old_win95) return 0 ;;
	esac
	return 1
}

# Windows-flag Start badges: only in the theme named Chicago95
# (-tux and -puffy have their own start-here icons).
flag_badge() {
	case $1 in
	*/Icons/Chicago95/places/* | */Icons/Chicago95/panel/*) ;;
	*) return 1 ;;
	esac
	case ${1##*/} in
	start-here.png | start-here.svg | start-here-symbolic.png | start-here-symbolic.svg | \
	distributor-logo.png | distributor-logo.svg) return 0 ;;
	esac
	return 1
}

theme_flag() {
	case $1 in
	*/misc/windows.png | */misc/windows_16x16px.png | */misc/windows_32x32px.png | \
	*/GTK2_start_buttons/windows_*.png | */Legay_GTK3_start_buttons/windows.png | \
	*/GTK2_start_buttons/Start-button_chicago95.png | */gnome-shell/assets/start.png) return 0 ;;
	esac
	return 1
}

is_bad() {
	f=$1; b=${f##*/}
	bad_stem "${b%.*}" || flag_badge "$f" || theme_flag "$f"
}

# 1. Hashes of every bad file, so byte-identical copies under other names
#    (menu, terminal, desktop, browser icons...) go too.
: >"$work/bad"
for d in Icons Theme Plymouth Extras/Backgrounds sounds; do
	[ -d "$root/$d" ] || continue
	find "$root/$d" -type f | while IFS= read -r f; do
		is_bad "$f" && sha256sum "$f" | cut -d' ' -f1 >>"$work/bad"
	done
done
f="$root/Extras/Microsoft Windows 95 Startup Sound.ogg"
[ -f "$f" ] && sha256sum "$f" | cut -d' ' -f1 >>"$work/bad"
sort -u "$work/bad" -o "$work/bad"

# 2. Drop them.
rm -rf "$root/Plymouth/Chicago95" "$root/Extras/Backgrounds/Wallpaper" \
	"$root/Extras/Backgrounds/Patterns" "$root/Extras/setup.png" "$root/Plus" \
	"$root/Extras/Microsoft Windows 95 Startup Sound.ogg" \
	"$root/sounds/chicago95-startup.desktop"
find "$root/sounds" -type f -name '*.wav' -delete
for d in Icons Theme; do
	find "$root/$d" \( -type f -o -type l \) | while IFS= read -r f; do
		if is_bad "$f"; then rm -f "$f"; continue; fi
		[ -L "$f" ] && continue
		grep -qx "$(sha256sum "$f" | cut -d' ' -f1)" "$work/bad" && rm -f "$f"
	done
done

# 3. Point the freed freedesktop names at generic icons the theme keeps.
link_in() { # dir name target
	[ -e "$1/$3" ] || [ -L "$1/$3" ] || return 0
	[ -e "$1/$2" ] || [ -L "$1/$2" ] && return 0
	ln -s "$3" "$1/$2"
}
link_names() { # dir target stem...
	d=$1; t=$2; shift 2
	for s in "$@"; do link_in "$d" "$s.${t#*.}" "$t"; done
}
office="application-msword x-office-document x-office-document-template
	x-office-document-templat libreoffice-text libreoffice-text-template
	application-vnd.ms-excel x-office-spreadsheet x-office-spreadsheet-template
	libreoffice-spreadsheet libreoffice-spreadsheet-template
	application-vnd.ms-powerpoint x-office-presentation x-office-presentation-template
	libreoffice-presentation libreoffice-presentation-template
	application-vnd.ms-access libreoffice-database libreoffice-base
	msaccess.exe_14_259_4_48x48x4"
browsers="internet-web-browser web-browser gnome-web-browser redhat-web-browser"
find "$root/Icons" -type d | while IFS= read -r d; do
	case $d in
	*/mimes/*)
		# shellcheck disable=SC2086
		link_names "$d" text-x-generic.png $office
		# shellcheck disable=SC2086
		link_names "$d" text-x-generic.svg $office
		link_names "$d" application-x-executable.png application-x-ms-dos-executable
		link_names "$d" application-x-executable.svg application-x-ms-dos-executable ;;
	*/apps/*)
		# shellcheck disable=SC2086
		link_names "$d" firefox.png $browsers
		# shellcheck disable=SC2086
		link_names "$d" firefox.svg $browsers
		sz=${d##*/}
		for a in libreoffice-calc libreoffice-text libreoffice-base; do
			for e in png svg; do
				[ -e "$d/../../mimes/$sz/text-x-generic.$e" ] &&
					link_in "$d" "$a.$e" "../../mimes/$sz/text-x-generic.$e"
			done
		done ;;
	*/devices/*)
		link_names "$d" computer-laptop.png computer computer-symbolic
		link_names "$d" computer-laptop.svg computer computer-symbolic ;;
	esac
done
# Chicago95 gets the Tux start-here/distributor-logo in place of the flag.
tux=$root/Icons/Chicago95-tux
for kind in places panel; do
	[ -d "$tux/$kind" ] || continue
	find "$tux/$kind" \( -type f -o -type l \) | while IFS= read -r f; do
		case ${f##*/} in
		start-here.png | start-here.svg | start-here-symbolic.png | start-here-symbolic.svg | \
		distributor-logo.png | distributor-logo.svg) ;;
		*) continue ;;
		esac
		rel=${f#"$tux/"}
		dest=$root/Icons/Chicago95/$rel
		[ -e "$dest" ] || [ -L "$dest" ] && continue
		mkdir -p "${dest%/*}"
		ln -s "../../../Chicago95-tux/$rel" "$dest"
	done
done

# Upstream aliases of the dropped files are now dangling. Menu-button
# aliases get the (Tux) start-here icon; the rest are removed, so lookup
# falls back to the inherited theme. Debian ships them dangling.
find "$root/Icons" -xtype l | while IFS= read -r f; do
	b=${f##*/}; d=${f%/*}; sz=${d##*/}
	case $b in
	org.xfce.panel.applicationsmenu.* | org.xfce.panel.whiskermenu.* | \
	xfce4-whiskermenu.* | xfce4-logo.* | xfce4_xicon*.* | xfsm-chooser-icon.*)
		t=../../places/$sz/start-here.${b##*.}
		if [ -e "$d/$t" ]; then
			ln -sfn "$t" "$f"
			continue
		fi ;;
	esac
	rm -f "$f"
done
n=$(find "$root" -xtype l | wc -l)
[ "$n" -eq 0 ] || { echo "still $n dangling links" >&2; exit 1; }

tar -C "$work" --sort=name --owner=0 --group=0 --numeric-owner \
	--mtime="@$(git -C "$src" log -1 --format=%ct)" \
	-cJf "$out/chicago95-$ver.tar.xz" "chicago95-$ver" || exit 1
echo "$out/chicago95-$ver.tar.xz"
