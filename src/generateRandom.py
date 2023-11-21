import random

f = open("sampleData.csv", "a")
t = 0
for i in range(0,100):
    v = random.randint(0,9)
    a = random.randint(0,9)
    t += 0.1
    value = str(v)+","+str(a)+","+str(t)+"\n"
    print(value)
    f.write(value)
f.close()