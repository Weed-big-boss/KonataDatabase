from faker import Faker
import uuid
import random
import json
faker = Faker()


faker.name()

convertor={"str":"TEXT","int":"INTEGER",'None':"JSON","bytes":"BLOB","bool":"BOOLEAN","datetime":"DATETIME","list":"JSON","tuple":"JSON",
                        "NoneType":"JSON","Decimal":"NUMERIC","Zoneinfo":"VARCHAR(255)","dict":"JSON","set":"JSON","GENERATOR":"JSON",'timedelta':"JSON",
                        "time":"TEXT","date":"TEXT",'float':"FLOAT"}
def generate_sql_for_table(table,relations):
    lines = [f"CREATE TABLE {table['name']} (", "    id VARCHAR(36) PRIMARY KEY"]
    if len(table['columns'])!=0 or ((table['name'] in relations) and len(relations[table['name']])>0):
        lines[1]+=','




    for i, col in enumerate(table["columns"]):
        line = f"    {col['name']} {col['type']}"
        if col["not_null"]:
            line += " NOT NULL"


        if i < len(table["columns"]) - 1:
            line += ","
        else:
            if table['name'] in relations:
                    line += ","
        lines.append(line)



    if table['name'] in relations:
        for table2 in relations[table['name']]:
                line = f"    {table2}_id VARCHAR(36),"
                lines.append(line)
        for i,table2 in enumerate(relations[table['name']]):
                line = f"    FOREIGN KEY ({table2}_id) REFERENCES {table2}(id)"
                if i<len(relations[table['name']])-1:
                    line+=","
                lines.append(line)

    lines.append(");")
    return "\n".join(lines)

def generate_users(n=10,table=None, use_uuid=False):

        users = []
        for _ in range(n):
            user_id = str(uuid.uuid4()) if use_uuid else None
            data = [user_id]
            for i, col in enumerate(table["columns"]):
                    if hasattr(faker, col['name'].lower()):
                        method = getattr(faker, col['name'].lower())
                        if callable(method):
                            try:
                                result = method()

                                if convertor[str(type(result).__name__)]=="JSON":
                                    json_data = json.dumps(result, ensure_ascii=False)
                                    result=json_data
                                    print(result)
                            except:
                                result=faker.word()
                            data.append(result)
                        else:
                            data.append(faker.word())
                    else:
                        data.append(faker.word())


            users.append(data)


        return users

def generate_insert_sql(users,use_uuid=False,table=None):
    sql = ""

    for idx, user in enumerate(users):
        uid = f"'{user[0]}'" if use_uuid else ''
        id_value = uid if use_uuid else ''
        sql += f"INSERT INTO {table['name']} ({'id, ' if (use_uuid and len(table['columns'])>0) else 'id)'''}"

        for i, col in enumerate(table["columns"]):
            sql+=f"{col['name']}"
            if i< len(table['columns'])-1:
                sql+=','
            else:
                sql+=")"
        if len(table['columns'])!=0:
            sql+=f' VALUES ({id_value + ', ' if use_uuid else ''}'
        else:
            sql += f' VALUES ({id_value + ');\n' if use_uuid else ''}'

        for i,col in enumerate(table["columns"],start=1):

            if i<len(table['columns']):
               sql+=f"'{user[i]}',"
            else:
                sql+=f"'{user[i]}');\n"

    return sql

def generate_uuid_insert(users_array,relations):
      sql = ''
      for table1 in relations:
          for table2 in relations[table1]:

              all_data = [elem[0] for elem in users_array[table2]]
              for i in range(10):
                  sql+=f"UPDATE {table1} SET {table2}_id = '{random.choice(all_data)}' WHERE id = '{users_array[table1][i][0]}';\n"
      return sql

