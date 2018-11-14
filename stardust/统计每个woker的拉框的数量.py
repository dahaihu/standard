import psycopg2
import csv

# conn = psycopg2.connect(database="startask", user="startask", password="Startask789&*(", host="rm-2zej4yocsipaw7z83qo.pg.rds.aliyuncs.com", port="3432")
# 生产环境
conn = psycopg2.connect(database="startask", user="startask", password="Startask789&*(", host="rm-bp15z0r1g84i4mfm6co.pg.rds.aliyuncs.com", port="3432")
cur = conn.cursor()

# project_id = 281

result = dict()
sql = f'''select task_id, info->>'answer', worker_id, info->>'status' from sd_task_record where project_id in {(281, 283)}'''
cur.execute(sql)
# 0 = > task_id
# 1 = > answer
# 2 = > worker_id
# 3 = > status

for line in cur.fetchall():
    # 状态为 1 说明是做题，需要纳入统计
    if line[-1] == '1':
        result[line[-2]] = result.get(line[-2], 0) + len(eval(line[-3]))

for key, val in result.items():
    print(key, ' => ', val)


id_to_phone = f'''select id, phone from sd_worker where id in {tuple(result)}'''

mark = dict()
cur.execute(id_to_phone)
for line in cur.fetchall():
    mark[line[1]] = result[line[0]]

for key, val in mark.items():
    print(key, ' => ', val)

