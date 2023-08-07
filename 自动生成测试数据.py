with open("words.json","w",encoding="utf-8") as f:
    f.write("{")
    i=1
    for i in range(10):
        f.write(f"\"test{i}\":\"测试{i}\",")
    f.write(f"\"test{i+1}\":\"测试{i+1}\"")
    f.write("}")