import zxcvbn as zx

results = zx.zxcvbn('cloudpasswordmoon')


for x in results:
    try:
        k = x + " : "
        for y in results[x]:
            d = results[x][y]
            if k != "":
                print("\n", k)
                k = ""
            print("\t", y, ":", d)
    except:
        print("\n", x, ":", results[x])
