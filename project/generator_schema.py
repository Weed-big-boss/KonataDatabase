from sql_injects import generate_sql_for_table
from sql_injects import generate_users, generate_insert_sql,generate_uuid_insert

def schema_generator(table,relations):
     insert_sql = generate_sql_for_table(table,relations)

     return insert_sql

def generator(table):

    users = generate_users(10, table=table, use_uuid=True)

    insert_sql = generate_insert_sql(users, use_uuid=True,table=table)

    return insert_sql,users

def relations_generator(users_array,relations):
    insert_sql = generate_uuid_insert(users_array,relations)

    return insert_sql
