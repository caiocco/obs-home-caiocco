#!/bin/sh
# Make the hardinfo2 source tarball used by hardinfo2.spec, without the
# window background pictures (pixmaps/bg*_{dark,light}.jpg) and their
# license proofs. hardinfo2-no-background-themes.patch removes the Theme
# menu that used them, so the pictures never reach OBS.
#
# usage: prune-backgrounds.sh VERSION [OUTDIR]
# Downloads the release-VERSION tag from GitHub and writes
# hardinfo2-VERSION.tar.xz into OUTDIR (default: current directory).

set -eu

ver=${1:?usage: $0 VERSION [OUTDIR]}
out=$(cd "${2:-.}" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

curl -fsSL -o "$work/src.tar.gz" \
	"https://github.com/hardinfo2/hardinfo2/archive/refs/tags/release-$ver.tar.gz"
tar xzf "$work/src.tar.gz" -C "$work"
mv "$work/hardinfo2-release-$ver" "$work/hardinfo2-$ver"
root=$work/hardinfo2-$ver

rm -f "$root"/pixmaps/bg[0-9]*_dark.jpg "$root"/pixmaps/bg[0-9]*_light.jpg
rm -f "$root"/tools/LICENSES/BG[0-9]*

tar -C "$work" --sort=name --owner=0 --group=0 --numeric-owner \
	--mtime="@$(stat -c %Y "$root/CMakeLists.txt")" \
	-cJf "$out/hardinfo2-$ver.tar.xz" "hardinfo2-$ver"
echo "$out/hardinfo2-$ver.tar.xz"
