def get_sql_tables(database):
    database_cursor = database.cursor()
    database_cursor.execute("SHOW Tables")
    ###
    # SHOW Tables query result sends back a tuple of tuples. First element is a bytearray, which needs to be decoded
    # to be able to use what's inside.
    ###
    return database_cursor.fetchall()


def get_sql_table(database, table_name):
    ###
    # Initialize a cursor to create queries to the MYSQL Database
    ###
    database_cursor = database.cursor()
    ###
    # Execute query and get the query results into the cursor
    ###
    database_cursor.execute("SELECT * FROM " + table_name)
    ###
    # Fetch all query results from the cursor
    # Result is a tuple with all elements
    ###
    return database_cursor.fetchall()


def get_sql_row(database, table_name, row_name):
    database_cursor = database.cursor()

    database_cursor.execute("SELECT " + row_name + " FROM " + table_name)

    return database_cursor.fetchall()


###
#  Executes a join query. All arguments are strings. Similarly, left and right joins are implemented later.
###
def get_sql_join(database, left_table, right_table, select_target, condition):
    database_cursor = database.cursor()
    database_cursor.execute(
        "SELECT DISTINCT " + select_target + " FROM " + left_table + " JOIN " + right_table + " ON " + condition)
    return database_cursor.fetchall()


# LEFT join
def get_sql_left_join(database, left_table, right_table, select_target, condition):
    database_cursor = database.cursor()
    database_cursor.execute(
        "SELECT DISTINCT " + select_target + " FROM " + left_table + " LEFT JOIN " + right_table + " ON " + condition)
    return database_cursor.fetchall()


# RIGHT join
def get_sql_right_join(database, left_table, right_table, select_target, condition):
    database_cursor = database.cursor()
    database_cursor.execute(
        "SELECT DISTINCT " + select_target + " FROM " + left_table + " RIGHT JOIN " + right_table + " ON " + condition)
    return database_cursor.fetchall()


###
#  Executes a join query with the left table being a string, the right tables being an array of strings.
#  Select_target is a string array (SELECT table.row,table2.row2 FROM ...).
#  Conditions is a string array with the conditions of the join (table1.row1 = table2.row2)
###
def get_sql_multiple_joins(database, table_name_left, table_names_right, select_target, conditions):
    if len(table_names_right) != len(conditions):
        print("Your conditions are not equal to your right tables!")
        return
    database_cursor = database.cursor()
    ###
    #  Initialize the query with the "stable" part
    ###
    query = "SELECT DISTINCT " + select_target + " FROM " + table_name_left
    ###
    #  Iterate through the right tables and conditions at the same time to build the "dynamic" part of the query
    ###
    for right_table, condition in zip(table_names_right, conditions):
        query += " JOIN " + right_table + " ON " + condition
    database_cursor.execute(query)
    return database_cursor.fetchall()
