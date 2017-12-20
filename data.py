import linecache
import json

with open('Frames_usable_4050.json', 'r') as f:
    all_data = json.load(f)

for i in range(len(all_data)):
    x = all_data[i]['nl_ch']
    x_1 = ''
    for j in range(len(x)):
        x_1 += x[j]+' '
    with open('seq.in', 'a') as f:
        f.write(x_1+'\n')
    seq = all_data[i]['label_seq']
    with open('seq.out', 'a') as f:
        f.write(seq+'\n')