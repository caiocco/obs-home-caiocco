# Append to an Axene app-defaults file a renderTable for every fontList.
#
# The interface text is Latin-1 and the app-defaults only set fontList
# (core iso8859-1 fonts).  A user resource such as "*renderTable: rt" with
# an Xft rendition overrides every fontList, and Motif draws Xft text as
# UTF-8, so a label stops at the first accented byte ("Authors: St"
# instead of "Authors: Stéphane ...", "XQuad" instead of "XQuad®") and
# the program's own fonts are lost.  "<Class>*<path>renderTable" binds
# more tightly than any "*..." user resource, which restores the original
# fonts while leaving other Motif programs alone.
#
# Usage: awk -v cls=<Class> -f axene-rendertable.awk <app-defaults file>
/^\*[^!]*fontList:/ {
  line = $0
  sub(/^\*/, "", line)
  i = index(line, "fontList:")
  path = substr(line, 1, i - 1)
  font = substr(line, i + 9)
  sub(/^[ \t]+/, "", font)
  out = out cls "*" path "renderTable:\t" font "\n"
}
END {
  if (out != "")
    printf "\n! Core-font renderTables for every fontList above: the interface\n! is Latin-1, which Xft renderTables would draw as UTF-8.\n%s", out
}
