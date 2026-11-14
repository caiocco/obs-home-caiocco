#!/bin/sh
# Make the axene-office source tarball used by axene-office.spec from the
# upstream SDK, without the non-redistributable fonts.
#
# Common-2.0.1/lib/fonts/*.pfc are the original Adobe/Linotype Type 1
# fonts ("All Rights Reserved"); the GPL release never covered them.  They
# and their Adobe AFM files are removed here, so they never reach OBS.  The
# package links the standard PostScript names to the URW clones from
# ghostscript-fonts-std instead.  The Utopia fonts (put*.pfa/afm) are
# freely redistributable and stay.
#
# usage: prune-nonfree-fonts.sh /path/to/AxeneSDK-v2.0.1.tar.gz [outdir]
# Upstream: http://linuxmafia.com/pub/linux/apps/axene/AxeneSDK-v2.0.1.tar.gz
# Writes axene-office-2.0.1.tar.xz into outdir (default: current directory).

set -eu

sdk=${1:?usage: $0 AxeneSDK-v2.0.1.tar.gz [OUTDIR]}
out=$(cd "${2:-.}" && pwd)
ver=2.0.1
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

tar xzf "$sdk" -C "$work"
mv "$work/Axene-$ver" "$work/axene-office-$ver"
root=$work/axene-office-$ver

for f in "$root"/Common-$ver/lib/fonts/*.pfc; do
	base=$(basename "$f" .pfc)
	rm -f "$f" "$root/Common-$ver/lib/metrics/$base.afm"
done

# Nothing proprietary may be left behind
if find "$root" -name '*.pfc' | grep -q .; then
	echo "error: .pfc fonts left" >&2
	exit 1
fi

tar --sort=name --owner=0 --group=0 --numeric-owner \
    --mtime='2003-03-27 00:00Z' -C "$work" -cJf "$out/axene-office-$ver.tar.xz" \
    "axene-office-$ver"
echo "$out/axene-office-$ver.tar.xz"
