
# txt den liste okuma:
with open(f'output_list/berlin_mobile_jobs.txt', 'r',encoding="utf-8") as f:
        data = f.read()
        listem = data.split(",")

print(len(listem))
print(listem[-2])

