import psycopg2
import csv

# conn = psycopg2.connect(database="startask", user="stardust", password="tester", host="117.50.3.122", port="5432")
conn = psycopg2.connect(database="startask-staging", user="startask", password="Startask789&*(",
                        host="rm-bp15z0r1g84i4mfm6co.pg.rds.aliyuncs.com", port="3432")
cur = conn.cursor()
# sql = f'select id from sd_task where project_id in {(309, 317, 319)} and status=6'
sql = f'select id from sd_task where project_id = 402 and status=6'
# 获取task为conflict的task_id
res = []
cur.execute(sql)
for ele in cur.fetchall():
    res.append(ele[0])
print(res)

result = []
for task_id in res:
    sql = f'''select task_id, issue, info->>'answer' from sd_task_record where task_id={task_id} order by id'''
    cur.execute(sql)
    result.append(list(cur.fetchall()[-1]))

with open('result.csv', 'w', newline='', encoding='utf8') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(['task_id', 'info', 'answer'])
    csvwriter.writerows(result)
