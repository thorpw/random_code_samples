import mysql.connector
import os


# Create function for datatype mapping from MYSQL to Redshift
def column_mapping(datatype, length, *precision, **scale):
    result = "INSERT_COLUMN_DATATYPE"

    if datatype == "varchar" or datatype == "char" or datatype == "text":
        result = "VARCHAR({})".format(length)
    elif datatype == "decimal" or datatype == "numeric" or datatype == "double" or datatype == "float":
        result = "DECIMAL{}".format(precision, scale)
    elif datatype == "bit":
        result = "BOOLEAN"
    elif datatype == "blob":
        result = "VARCHAR(MAX)"
    elif datatype == "tinyint":
        result = "SMALLINT"
    elif datatype == "bigint" or datatype == "int" or datatype == "date" or datatype == "datetime" or datatype == "smallint":
        result = datatype.upper()
    # elif datatype == "int":
    #     result = "INT({}, {})".format(precision, scale)
    # elif datatype == "datetime":
    #     result = "DATETIME"
    # elif datatype == "smallint":
    #     result = "INT2"
    return result


# Create function for DDL generation for Redshift
def generate_ddl_file(user, password, host, database, rs_schema):
    # Create connection to SQL Server
    cnx = mysql.connector.connect(user=user,
                                  password=password,
                                  host=host,
                                  database=database)

    # Create Cursors
    cur = cnx.cursor()  # table
    cur1 = cnx.cursor()  # column

    # create = "CREATE TABLE {}".format(rs_schema)

    # Get a distinct list of table names
    cur.execute("""SELECT DISTINCT table_name
                           FROM information_schema.columns
                           WHERE table_schema = '{}'""".format(database))

    tableList = cur.fetchall()
    tableCount = len(tableList)
    print("There are {} tables in the {} database.".format(tableCount, database))

    # Delete DDL file if exists
    if os.path.exists("table_create_ddl_{}.sql".format(database)):
        os.remove("table_create_ddl_{}.sql".format(database))

    # Loop for each table name in list
    for row in tableList:
        columns = ''
        tables = row[0]

        # Get column names, datatypes and precision
        cur1.execute("""SELECT COLUMN_NAME, DATA_TYPE, COALESCE(CHARACTER_MAXIMUM_LENGTH, 0),
                                COALESCE(NUMERIC_PRECISION, 0), COALESCE(NUMERIC_SCALE, 0)        
                                FROM information_schema.columns                     
                                WHERE table_schema = '{}'              
                                AND table_name = '{}'
                                ORDER BY ORDINAL_POSITION""".format(database, tables))

        columnList = cur1.fetchall()

        # Loop for every column and format code
        for line in columnList:
            ColumnRows = ("\t" + line[0].lower() + " " + column_mapping(line[1].lower(), line[2], line[3], line[4]) + "," + "\n")
            columns += ColumnRows

        # Format create statements
        # statement = create + tables.lower() + "\n" + "(" + "\n" + columns[:-2] \
        #             + "\n" + ")" + "\n" + "--DISTKEY (insert column)" + "\n" \
        #             + "--SORTKEY (insert column)" + "\n" + ";" + "\n"

        statement = "CREATE TABLE {}.{}\n(\n {} \n)\n--DISTKEY (insert column)\n--SORTKEY (insert column)\n;\n".format(rs_schema, tables.lower(), columns[:-2])

        # write DDLs to file
        with open("table_create_ddl_{}.sql".format(database), 'a') as f:
            f.write("\n" + statement)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--database', help='Database Name', type=str, required=True)
    parser.add_argument('--host', help='Host Name', type=str, required=True)
    parser.add_argument('--user', help='Database User Name', type=str, required=True)
    parser.add_argument('--password', help='Database Password', type=str, required=True)
    parser.add_argument('--rs_schema', help='Redshift Database Schema', type=str, required=False)
    options = parser.parse_args()

    generate_ddl_file(options.user, options.password, options.host, options.database, options.rs_schema)
