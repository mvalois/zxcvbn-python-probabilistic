import src.zxcvbn_functions as zx
import json

results = zx.zxcvbn('azerty')

# for x in results:
#     try :
#         k = x + " : "
#         for y in results[x]:
#             d = results[x][y]
#             if k != "":
#                 print("\n", k)
#                 k = ""
#             print("\t", y, ":", d)
#     except:
#         print("\n", x, ":", results[x])

print("\npassword :", results['password'])
print("\nscore :", results['score'])
print("\nguesses :", results['guesses'])
print("\ncrack_times_display :")
for y in results['crack_times_display']:
    d = results['crack_times_display'][y]
    print("\t", y, ":", d)
print("\nfeedback :")
if results['feedback']['warning'] != "":
    print("\twarning :",results['feedback']['warning'])
    k = "\tsuggestions : "
    for s in results['feedback']['suggestions']:
        if k == "":
            k = "\t\t      "
        k += s
        print(k)
        k = ""
print("\nsequence :", results['sequence'])
print("\temps :", results['calc_time'])
print("\n")
