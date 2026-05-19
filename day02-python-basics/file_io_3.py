with open("test.txt","w",encoding="utf-8") as f:
    f.write("Hello AI World\n第二行\n")

with open("test.txt","r",encoding="utf-8") as f:
    for line in f:
        print(line.strip()) ## strip()去掉行末的换行符