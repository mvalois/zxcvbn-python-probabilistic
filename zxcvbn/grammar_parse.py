from cffi import FFI
ffibuilder = FFI()
ffibuilder.cdef("""
#define PWD_T  40
#define BASE_T 40
#define TERM_T 40
typedef struct {
	char base[BASE_T];
	char terms[TERM_T][PWD_T];
	int  nbterms;
} gramm;

gramm parse(char word[PWD_T]);
""")

ffibuilder.set_source("_parse", 
"""
#include <stdio.h>

#define PWD_T  40
#define BASE_T 40
#define TERM_T 40
typedef struct {
	char base[BASE_T];
	char terms[TERM_T][PWD_T];
	int  nbterms;
} gramm;

gramm parse(char word[PWD_T]){
	gramm g;
	g.nbterms = 0;
	int i = 0;
	char c;
	int chain_length = 0;
	char term[TERM_T];
	memset(term, '\\0', TERM_T);
	while(word[i] != '\\0' && i < PWD_T){
		c = word[i];
		if      (c >= 'a' && c <= 'z')  g.base[i] = 'L';
		else if (c >= 'A' && c <= 'Z')  g.base[i] = 'L';
		else if (c >= '0' && c <= '9')  g.base[i] = 'D';
		else                            g.base[i] = 'S';
		if (i > 0 && (g.base[i] != g.base[i-1])){
			term[i+1] = '\\0';
			strcpy(g.terms[g.nbterms], term);
			memset(term, '\\0', TERM_T);
			g.nbterms++;
			chain_length = 0;
		}
		term[chain_length] = c;
		chain_length++;
		i++;
	}
	strcpy(g.terms[g.nbterms], term);
	g.nbterms++;
	g.base[i] = '\\0';
	return g;
}
""", libraries=[])
if __name__ == '__main__':
	ffibuilder.compile(verbose=True)