/*
 * axene-latin1-labels.c - show UTF-8 file names in the Latin-1 interface
 *
 * The Axene programs run in the C locale with core iso8859-1 fonts, and
 * all their own text is Latin-1.  Under a UTF-8 locale, though, the file
 * names they read from the disk are UTF-8, and messages, document window
 * names and labels showed them byte by byte ("/home/x/MÃºsica/").
 *
 * The programs are linked with
 *   -Wl,--wrap=XmStringCreate,--wrap=XmStringCreateLtoR,
 *   -Wl,--wrap=XmStringCreateSimple,--wrap=XStoreName
 * so every call they make goes through the functions below first.  Text
 * that is valid UTF-8 and contains at least one multi-byte sequence is
 * converted to Latin-1 (characters beyond U+00FF become '?'); anything
 * else, the programs' own Latin-1 text included, is passed on unchanged.
 * Latin-1 text is almost never valid UTF-8 ("St\xe9phane" is not), so
 * the test is reliable in practice.  Nothing is converted unless
 * LC_ALL, LC_CTYPE or LANG names a UTF-8 locale.
 *
 * License: GPL-2.0-or-later, like Axene Office.
 */

#include <stdlib.h>
#include <string.h>
#include <X11/Xlib.h>
#include <Xm/Xm.h>

XmString __real_XmStringCreate(char *text, XmStringCharSet charset);
XmString __real_XmStringCreateLtoR(char *text, XmStringCharSet charset);
XmString __real_XmStringCreateSimple(char *text);
int __real_XStoreName(Display *display, Window w, const char *name);

static int utf8_locale(void)
{
	static int cached = -1;

	if (cached < 0) {
		const char *loc = getenv("LC_ALL");

		if (!loc || !*loc)
			loc = getenv("LC_CTYPE");
		if (!loc || !*loc)
			loc = getenv("LANG");
		cached = loc && (strstr(loc, "UTF-8") || strstr(loc, "utf-8") ||
				 strstr(loc, "UTF8") || strstr(loc, "utf8"));
	}
	return cached;
}

/* Latin-1 copy of s (to free) when s is UTF-8 with non-ASCII text, else NULL */
static char *to_latin1(const char *s)
{
	const unsigned char *p;
	char *out, *o;
	int multi = 0;

	if (!s || !utf8_locale())
		return NULL;

	for (p = (const unsigned char *)s; *p; ) {
		int len, i;

		if (*p < 0x80) {
			p++;
			continue;
		}
		if (*p >= 0xC2 && *p <= 0xDF)
			len = 2;
		else if (*p >= 0xE0 && *p <= 0xEF)
			len = 3;
		else if (*p >= 0xF0 && *p <= 0xF4)
			len = 4;
		else
			return NULL;
		for (i = 1; i < len; i++)
			if ((p[i] & 0xC0) != 0x80)
				return NULL;
		multi = 1;
		p += len;
	}
	if (!multi || !(out = malloc(strlen(s) + 1)))
		return NULL;

	for (p = (const unsigned char *)s, o = out; *p; ) {
		unsigned long c;
		int len, i;

		if (*p < 0x80) {
			*o++ = (char)*p++;
			continue;
		}
		len = *p >= 0xF0 ? 4 : *p >= 0xE0 ? 3 : 2;
		c = *p & (0x7F >> len);
		for (i = 1; i < len; i++)
			c = (c << 6) | (p[i] & 0x3F);
		*o++ = c <= 0xFF ? (char)c : '?';
		p += len;
	}
	*o = 0;
	return out;
}

XmString __wrap_XmStringCreate(char *text, XmStringCharSet charset)
{
	char *l = to_latin1(text);
	XmString s = __real_XmStringCreate(l ? l : text, charset);

	free(l);
	return s;
}

XmString __wrap_XmStringCreateLtoR(char *text, XmStringCharSet charset)
{
	char *l = to_latin1(text);
	XmString s = __real_XmStringCreateLtoR(l ? l : text, charset);

	free(l);
	return s;
}

XmString __wrap_XmStringCreateSimple(char *text)
{
	char *l = to_latin1(text);
	XmString s = __real_XmStringCreateSimple(l ? l : text);

	free(l);
	return s;
}

/* WM_NAME is a STRING property, which ICCCM defines as Latin-1 */
int __wrap_XStoreName(Display *display, Window w, const char *name)
{
	char *l = to_latin1(name);
	int r = __real_XStoreName(display, w, l ? l : name);

	free(l);
	return r;
}
