import psycopg2
import csv
# conn = psycopg2.connect(database="startask", user="startask", password="Startask789&*(", host="rm-2zej4yocsipaw7z83qo.pg.rds.aliyuncs.com", port="3432")
conn = psycopg2.connect(database="startask", user="stardust", password="tester", host="117.50.3.122", port="5432")
cur = conn.cursor()


project_id = 556
status = 4


sql = f'select id from sd_task where project_id={project_id} and status={status}'
# 获取task为conflict的task_id
res = []
cur.execute(sql)
for ele in cur.fetchall():
    res.append(ele[0])
print(res)

result = []
for task_id in res:
    sql = f'''select task_id, info->>'answer' from sd_task_record where task_id={task_id} order by id'''
    cur.execute(sql)
    temp = list(cur.fetchall()[-1])
    # print(f"{eval(temp[-1])}")
    for ele in eval(temp[-1]):
        print(ele)
    result.append(len(eval(temp[-1])))
print(sum(result))

# with open('result.csv', 'w', newline='', encoding='utf8') as file:
#     csvwriter = csv.writer(file)
#     csvwriter.writerow(['task_id', '框数'])
#     csvwriter.writerows(result)


# 项目为39， task完结的框的个数为2870
# 项目为556，task完结的框的个数为643