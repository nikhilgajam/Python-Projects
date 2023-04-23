import json
import timeit

s = timeit.default_timer()
p = open("data.json", "r")
data = str(p.read())
p.close()
x = json.loads(data)

# print(len(x))

q = open("dictionary.data", "w", encoding="utf-8")
q.write("_Keyword_ == Meaning||Another Meaning||etc...\n")
# print(x.get("Print"))
for i, j in x.items():
    d = i + " == " + "||".join(j) + "\n"
    d = d.replace("\\n", " ").replace("\\t", " ")
    q.write(d)
e = timeit.default_timer()
q.close()

print("Time Taken:", (e-s)/60)
