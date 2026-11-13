/*
 * ted-mkdfa.c -- build a Ted spelling automaton (.dfa) from a word list
 *
 * To the extent possible under law, the author has waived all copyright
 * and related or neighboring rights to this file (CC0 1.0).
 *
 * Usage: mkdfa out.dfa < words.txt   (one UTF-8 word per line)
 *
 * Link against Ted's lib/ind.a lib/textEncoding.a lib/appUtil.a.
 */

#include <stdio.h>
#include <string.h>

#include <ind.h>

int main( int argc, char ** argv )
    {
    char	line[512];
    void *	ind;
    void *	mini;
    void *	renum;
    long	count= 0;
    long	skipped= 0;

    if  ( argc != 2 )
	{ fprintf( stderr, "usage: %s out.dfa < words\n", argv[0] ); return 2; }

    ind= indMake();
    if  ( ! ind )
	{ fprintf( stderr, "indMake failed\n" ); return 1;	}

    while( fgets( line, sizeof(line), stdin ) )
	{
	size_t	len= strcspn( line, "\r\n" );

	line[len]= '\0';
	if  ( len == 0 )
	    { continue;	}
	if  ( len > FORM_MAX )
	    { skipped++; continue;	}

	if  ( indPutUtf8( ind, line ) < 0 )
	    { fprintf( stderr, "indPutUtf8 failed: %s\n", line ); return 1; }
	count++;
	}

    mini= indMini( ind );
    if  ( ! mini )
	{ fprintf( stderr, "indMini failed\n" ); return 1;	}
    indFree( ind );

    renum= indRenumber( mini );
    if  ( ! renum )
	{ fprintf( stderr, "indRenumber failed\n" ); return 1;	}
    indFree( mini );

    if  ( indWrite( renum, argv[1] ) )
	{ fprintf( stderr, "indWrite %s failed\n", argv[1] ); return 1; }
    indFree( renum );

    fprintf( stderr, "%s: %ld words, %ld too long\n", argv[1], count, skipped );
    return 0;
    }
