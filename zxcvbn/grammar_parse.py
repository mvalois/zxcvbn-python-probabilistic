from cffi import FFI
ffibuilder = FFI()
ffibuilder.cdef("""
#define PWD_T  40
#define BASE_T 40
#define TERM_T 40
typedef struct {
	char base[BASE_T];
	wchar_t terms[TERM_T][PWD_T];
	int  nbterms;
} gramm;

gramm parse(wchar_t word[PWD_T]);
""")

ffibuilder.set_source("_parse", 
"""
#include <stdio.h>

#define PWD_T  40
#define BASE_T 40
#define TERM_T 40
typedef struct {
	char base[BASE_T];
	wchar_t terms[TERM_T][PWD_T];
	int  nbterms;
} gramm;

void wstrcpy(wchar_t* outbuff, wchar_t* inbuff, int size){
	for(int j = 0; j < size; j++){
		outbuff[j] = inbuff[j];
	}
	outbuff[size] = L'\\0';
}

gramm parse(wchar_t word[PWD_T]){
	gramm g;
	g.nbterms = 0;
	int i = 0;
	wchar_t c;
	int chain_length = 0;
	wchar_t term[TERM_T];
	memset(term, '\\0', TERM_T);
	while(word[i] != L'\\0' && i < PWD_T){
		c = word[i];
		if      (c >= L'a' && c <= L'z')  g.base[i] = 'L';
		else if (c >= L'A' && c <= L'Z')  g.base[i] = 'L';
		else if (c >= L'0' && c <= L'9')  g.base[i] = 'D';
		else                              g.base[i] = 'S';
		if (i > 0 && (g.base[i] != g.base[i-1])){
			wstrcpy(g.terms[g.nbterms], term, chain_length);
			memset(term, L'\\0', TERM_T);
			g.nbterms++;
			chain_length = 0;
		}
		term[chain_length] = c;
		chain_length++;
		i++;
	}
	wstrcpy(g.terms[g.nbterms], term, chain_length);
	g.nbterms++;
	g.base[i] = '\\0';
	return g;
}
""", libraries=[])
if __name__ == '__main__':
	ffibuilder.compile(verbose=True)