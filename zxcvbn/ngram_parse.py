from cffi import FFI
ffibuilder = FFI()
ffibuilder.cdef("""
#define PWD_T  40
#define MAX_N 7
typedef struct {
	wchar_t grams[PWD_T][MAX_N];
	int nbngrams;
} ngrams;

ngrams parse(wchar_t word[PWD_T], int N);
""")

ffibuilder.set_source("_ngram_parse", 
"""
#include <stdio.h>
#include <string.h>
#define PWD_T  40
#define MAX_N 7
typedef struct {
	wchar_t grams[PWD_T][MAX_N];
	int nbngrams;
} ngrams;

ngrams parse(wchar_t word[PWD_T], int N){
	ngrams ng;
	int len = 0;
	while(word[len] != L'\\0') len++;
	ng.nbngrams = len - N + 1;
	for(int i=0; i < ng.nbngrams; i++){
		for(int j=0; j < N; j++){
			ng.grams[i][j] = word[i+j];
		}
		ng.grams[i][N] = L'\\0';
	}
	return ng;
}
""", libraries=[])
if __name__ == '__main__':
	ffibuilder.compile(verbose=True)