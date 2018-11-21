import csv

path = '/Users/mac/Desktop/2.csv'
res = dict()
with open(path, encoding='utf8', newline='') as file:
    for line in file:
        a, b = line.split('**')
        if a in res:
            res[a].append(b.strip())
        else:
            res[a] = [b.strip()]
for key, value in res.items():
    value = ["\"" + ele + "\"" for ele in value]
    print("lpush {}:NEW {}".format(key, ' '.join(value)))


def zhangxin():
    file_path = '/Users/dexter/Desktop/3.csv'
    result = {}
    with open(file_path, newline='', encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            pid = int(row['project_id'])
            tid = int(row['id'])
            wid = int(row['worker_id'])
            result.setdefault((pid, tid), []).append(wid)
    switch = 0
    string = 'first'
    for key, value in result.items():
        pid, tid = key
        wid_list = value
        if pid != switch:
            print(string)
            string = f'RPUSH {pid}:OLD'
            switch = pid

            string += f' \"({tid}, {str(wid_list)})\"'
            continue
        string += f' \"({tid}, {str(wid_list)})\"'

    print(string)
