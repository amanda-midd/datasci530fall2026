"""SQL — CLASS LECTURE REFERENCE (Lectures 20–21)

Source: Lecture 20/Lecture 22 - Introduction to SQL.sqlbook.
The filename says 22, but the folder and internal lecture heading say 20.
Added November 12, 2026.
Lecture 21a–21c added November 17, 2026. Their internal headings say 23a–23c;
this reference follows the folder/filenames: SQL from Python, Merging, Advanced merging.

HOW TO USE
This .py file holds lecture SQL examples as multiline Python strings, with notes.
Copy the SQL INSIDE a string into a SQLBook code cell and run it using your
PostgreSQL Active Connection. Do not copy the Python variable name or quotes.
Running this Python file only stores strings; it does not connect to a server,
execute queries, create tables, or delete data. No new helper functions exist.
Lecture 21 adds labeled Python examples stored as raw multiline strings. Copy
their CONTENTS into Python notebook cells, not into a SQL editor. The r prefix
preserves the lecture's backslashes when storing the example source in this file.

CONTENTS
1. Connection and SQL formatting
2. Create tables and insert rows
3. Select columns, filter rows, and sort
4. Aggregate, group, and filter groups
5. Merge tables with LEFT JOIN
6. Exercises and Python comparisons
7. Python packages, SQLAlchemy connection, and table uploads (21a)
8. Escape characters and reading SQL into pandas (21a)
9. Member keys, ERDs, and left joins (21b)
10. Joining on several columns (21c)

Examples use the lecture's sample drivers/values exactly as teaching data, not
as a verified record of real-world driver statistics. Corrections are labeled.
"""


# %% 1. CONNECTION AND SQL FORMATTING
# ============================================================================
# SQL is a language for querying/managing databases. PostgreSQL is the database
# system used here. A common task is extracting data stored on a database server.
# Follow the course setup PDFs in Lecture 20:
#   Installing SQL (Mac).pdf / Installing SQL (Windows).pdf
# Create a connection in VS Code's Database panel, then select Active Connection
# in the SQLBook code cell. The lecture example uses local host 127.0.0.1,
# port 5432, database postgres. Use the credentials from your own installation.
# No Python database package or connection function is introduced in this lecture.
# The '-- Active: ...' line in the SQLBook is editor metadata, not query syntax.
#
# Refresh the Database panel after changes. The lecture's table icon opens a
# table; its pencil icon edits column attributes. A schema is a namespace holding
# tables and other database objects within a database (not simply the database).
#
# SQL formatting:
#   SELECT / FROM / WHERE ... : uppercase keywords for readability.
#   drivers / nationality    : lowercase table/column names by convention.
#   ;                        : terminates a statement, NOT every physical line.
#   ,                        : separates columns, expressions, or row values.
#   (...)                    : encloses definitions/values or groups conditions.
#   -- comment               : SQL comment; Python's # is not a SQL line comment.
#   'German'                 : string value, in SINGLE quotes.
#   "nationality"            : quoted identifier (column name), not a string.
#   =                        : equality in SQL conditions (not Python's ==).
#   *                        : all columns in SELECT; all rows in COUNT(*).
# Keywords need not be uppercase. PostgreSQL folds unquoted identifiers to
# lowercase; quoted identifiers preserve case. Prefer simple consistent names.
# The lecture's warning about double quotes displays a single-quoted query:
# that displayed query is valid. WHERE nationality = "German" would instead
# look for a column named German.


# %% 2. CREATE A TABLE AND ADD ROWS
# ============================================================================
# DROP removes the entire table and its contents. IF EXISTS avoids an error when
# it is absent. Use this reset only for the exercise table you intend to replace.
drop_drivers = """
DROP TABLE IF EXISTS drivers;
"""

create_drivers = """
CREATE TABLE drivers (
    driver_id int,
    driver_name varchar(30),
    nationality varchar(15),
    victories int
);
"""
# int holds whole numbers. varchar(n) holds text up to n characters in PostgreSQL.
# Each definition is column_name data_type; commas separate definitions, with no
# comma after the last column. CORRECTION: four columns here, not the five stated
# in a lecture comment. CREATE defines the structure but does not insert rows.
# The exercise asks for unique driver IDs, but this definition does NOT enforce
# uniqueness: it declares neither a PRIMARY KEY nor a UNIQUE constraint.

insert_drivers = """
INSERT INTO drivers VALUES (1, 'Lewis Hamilton', 'British', 103);
INSERT INTO drivers VALUES (4, 'Fernando Alonso', 'Spanish', 32);
INSERT INTO drivers VALUES (3, 'Sebastian Vettel', 'German', 91);
INSERT INTO drivers VALUES (2, 'Michael Schumacher', 'German', 53);
"""
# Without an explicit column list, values must follow the table's column order.
# Strings are quoted; numbers are not. CORRECTIONS: INSERT, not the comment's
# "INSET"; commas separate values, semicolons separate statements. Inserting
# rows does not guarantee a lasting displayed order; use ORDER BY for that.
# Re-running these INSERT statements adds the rows again; it is not an update.


# %% 3. SELECT COLUMNS, FILTER ROWS, AND SORT
# ============================================================================
select_columns = """
SELECT driver_id, nationality
FROM drivers;
"""
# SELECT lists the output columns; FROM supplies the source table.

select_all = """
SELECT * FROM drivers;
"""

filter_equal = """
SELECT * FROM drivers
WHERE nationality = 'German';
"""
# WHERE keeps rows satisfying a condition; it does not delete other stored rows.

filter_or = """
SELECT * FROM drivers
WHERE (nationality = 'Colombia') OR (nationality = 'German');
"""
# OR requires at least one condition to be true. The sample has no Colombia row,
# so this returns its German rows. The text must match stored values.

filter_and = """
SELECT * FROM drivers
WHERE (nationality = 'German') AND (driver_id = 3);
"""
# AND requires both conditions. Parentheses make grouping explicit.

sort_ascending = """
SELECT driver_name FROM drivers
ORDER BY victories ASC;
"""
# ASC: smallest to largest. You can sort by victories without displaying it.

sort_descending = """
SELECT * FROM drivers
ORDER BY victories DESC;
"""
# DESC: largest to smallest. ORDER BY changes returned order, not table contents.
# Neither insertion order nor a plain SELECT guarantees a particular row order.


# %% 4. AGGREGATES, GROUP BY, WHERE, AND HAVING
# ============================================================================
aggregate_all = """
SELECT SUM(victories) AS sum_victories,
       COUNT(*) AS num_rows,
       AVG(victories) AS mean_victories,
       MIN(victories) AS min_victories,
       MAX(victories) AS max_victories
FROM drivers;
"""
# SUM adds values; COUNT(*) counts rows; AVG averages; MIN/MAX give extremes.
# AS names the output expression (an alias); it does not rename stored columns.
# With the four supplied rows, expect sum=279, count=4, mean=69.75, min=32, max=103.
# NULL clarification: these numeric aggregates ignore missing (NULL) values;
# COUNT(*) still counts rows. Thus AVG's denominator need not equal COUNT(*)
# when some victories are missing.

group_aggregate = """
SELECT nationality,
       SUM(victories) AS sum_victories,
       AVG(victories) AS mean_victories,
       MIN(victories) AS min_victories,
       MAX(victories) AS max_victories
FROM drivers
GROUP BY nationality;
"""
# One result row per nationality. Selected nonaggregated columns here must be
# grouping columns. You may omit nationality from SELECT, but then the returned
# statistics lack group labels. GROUP BY itself does not guarantee sorted output.
# The lecture's comment accidentally joins prose with SELECT COUNT(*); the actual
# query contains the five expressions shown above. COUNT(*) can also count rows
# per group if added to that SELECT list.

filter_after_grouping = """
SELECT nationality,
       SUM(victories) AS sum_victories,
       AVG(victories) AS mean_victories,
       MIN(victories) AS min_victories,
       MAX(victories) AS max_victories
FROM drivers
GROUP BY nationality
HAVING SUM(victories) > 50;
"""
# HAVING filters GROUPS by aggregate conditions; WHERE filters individual rows
# BEFORE grouping. Here British (103) and German (144) pass; Spanish (32) does not.

filter_before_and_after = """
SELECT nationality,
       SUM(victories) AS sum_victories,
       AVG(victories) AS mean_victories,
       MIN(victories) AS min_victories,
       MAX(victories) AS max_victories
FROM drivers
WHERE (nationality = 'German') OR (nationality = 'British')
GROUP BY nationality
HAVING SUM(victories) > 50;
"""
# First restrict source rows to German/British, then compute their group summaries,
# then retain groups with sums greater than 50. This illustrates chaining clauses.
# For these examples the written order is:
# SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY
# Think about processing as: choose source -> filter rows -> group/aggregate ->
# filter groups -> select output expressions -> sort output.
# PostgreSQL does not let you use sum_victories (a SELECT alias) directly in this
# HAVING condition; repeat SUM(victories) as the lecture does.


# %% 5. MERGING WITH LEFT JOIN
# ============================================================================
drop_countries = """
DROP TABLE IF EXISTS countries;
"""

create_countries = """
CREATE TABLE countries (
    nationality varchar(15),
    region varchar(20)
);
"""

insert_countries = """
INSERT INTO countries VALUES ('British', 'Europe');
INSERT INTO countries VALUES ('Spanish', 'Europe');
INSERT INTO countries VALUES ('German', 'Europe');
"""

left_join = """
SELECT *
FROM drivers
LEFT JOIN countries
ON drivers.nationality = countries.nationality;
"""
# FROM names the left/primary table; LEFT JOIN names the right/secondary table.
# ON specifies matching keys; table.column qualifies otherwise ambiguous names.
# Keep every driver; attach matching country columns. Unmatched right-side values
# become NULL. Multiple matching country rows would duplicate a driver's result
# row, so inspect join-key uniqueness. SELECT * includes both nationality columns.
# CORRECTION: added the statement-ending semicolon omitted in the lecture.


# %% 6. EXERCISES AND PYTHON COMPARISONS
# ============================================================================
# The lecture leaves these exercises blank. Adapt the examples above:
# 1. INSERT two/three rows for you and classmates using new driver IDs.
#    Keep the order (driver_id, driver_name, nationality, victories).
# 2. SELECT nationality and driver_id for rows with victories > 60.
#    Select columns first; filter individual rows with WHERE.
# 3. Keep nationalities whose maximum victories is at most 71.
#    GROUP BY nationality, then use HAVING MAX(victories) <= 71.
#    WHERE victories <= 71 would instead discard individual rows before computing
#    maxima, potentially retaining a group that should have been excluded.
# No custom functions or extra exercise solutions are introduced here.
#
# Python / pandas concept                 SQL counterpart
# df[["a", "b"]]                          SELECT a, b FROM table_name
# df.query(...) before aggregation        WHERE
# df.groupby(...).agg(...)                GROUP BY with SUM/AVG/... in SELECT
# naming aggregate output columns         AS
# filtering grouped results afterward    HAVING
# sorting rows                           ORDER BY ... ASC / DESC
# merging and retaining left rows        LEFT JOIN ... ON ...
#
# SQL statements belong in the SQL editor; pandas syntax belongs in Python.
# The # %% markers and triple quotes in this file are only Python organization.
# Use -- for comments inside a copied SQL query. One lecture exercise has a
# stray '# Write your own code'; replace # with -- if pasting into PostgreSQL.
#
# Lecture links / syntax references:
# https://www.postgresql.org/docs/current/sql-commands.html
# https://www.postgresql.org/docs/current/sql-select.html
# https://www.postgresql.org/docs/current/sql-syntax-lexical.html


# %% 7. SQL FROM PYTHON — Lecture 21a
# ============================================================================
# Install psycopg2 and sqlalchemy in the Python environment used by the notebook;
# pandas is also required. These are packages, not PostgreSQL server installers.
# psycopg2 is the PostgreSQL driver; SQLAlchemy provides the engine/SQL interface.
# The notebook imports SQLAlchemy, which uses the driver without an explicit
# import psycopg2 statement. The server must be running and accessible separately.
# All *_python strings below hold PYTHON SOURCE to copy into notebook cells.
connection_python = r'''
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

url_server = URL.create(
    "postgresql",
    host="localhost",
    database="postgres",
    username="postgres",
    port=5432,
    password="",  # Replace with YOUR local server password, if required.
)
connection = create_engine(url_server)
'''
# URL.create assembles driver/dialect, host, database, username, port, password.
# "postgresql" selects the database dialect. localhost means your own machine.
# Lecture defaults: empty Mac password; "12345" in the Windows setup examples.
# Those are classroom setup choices, not passwords that work on every installation.
# create_engine returns an Engine, despite the variable name connection; the
# engine manages connections and normally opens one when database work begins.
# A successful Engine construction alone does not prove the login works.

load_racing_python = r'''
results = pd.read_csv("data_raw/results.csv")
races = pd.read_csv("data_raw/races.csv")
circuits = pd.read_csv("data_raw/circuits.csv")
'''
# These paths assume the working directory is Lecture 21. From the project root,
# use "Lecture 21/data_raw/..." instead. read_csv returns a pandas DataFrame.

upload_racing_python = r'''
results.to_sql("results", con=connection, if_exists="replace", index=False)
races.to_sql("races", con=connection, if_exists="replace", index=False)
circuits.to_sql("circuits", con=connection, if_exists="replace", index=False)
'''
# to_sql: first argument is destination table NAME, con supplies the Engine,
# if_exists="replace" drops/recreates an existing table, index=False omits the
# DataFrame index column. These operations change stored database data.
# CORRECTIONS: the actual first table is "results", not "results_sql" as its
# comment says. The circuits exercise calls races.to_sql('circuits', ...), which
# uploads the WRONG dataset; use circuits.to_sql as shown here.
# A pandas index or unique column does not automatically become a SQL primary key.
# Replacing a table can remove previously defined constraints/indexes.


# %% 8. ESCAPES, QUOTED IDENTIFIERS, AND READ_SQL — Lecture 21a
# ============================================================================
escape_examples_python = r'''
example_string = "This is a string \
defined over multiple lines"
example_double = "This will \"supposedly\" put double quotes inside a string"
example_single = "This will 'supposedly' put single quotes inside a string"
print(example_string)
print(example_double)
print(example_single)
example_query = "SELECT \"driverId\" FROM results;"
print(example_query)
'''
# Backslash immediately before a physical newline continues the string WITHOUT
# including that newline. Do not put trailing spaces after the backslash.
# \" puts a literal double quote inside a double-quoted Python string. A single
# quote needs no escape there. In a single-quoted Python string, double quotes
# can instead appear directly. Python escaping and SQL quoting are separate layers.
# PostgreSQL folds unquoted names to lowercase: driverId becomes driverid.
# Use "driverId", "raceId", "constructorId" to preserve the CSV column names.
# Double quotes mark SQL identifiers; single quotes mark SQL values such as names.

read_racing_python = r'''
example1 = pd.read_sql(text("SELECT * FROM results;"), connection)
example2 = pd.read_sql(text("SELECT points \
                           FROM results;"), connection)
example3 = pd.read_sql(text("SELECT * \
                           FROM races \
                           WHERE name = 'Abu Dhabi Grand Prix';"), connection)
example4 = pd.read_sql(text('SELECT "driverId" FROM results;'), connection)
example5 = pd.read_sql(text("SELECT AVG(points) AS mean_points \
                           FROM results \
                           GROUP BY \"driverId\";"), connection)
example6 = pd.read_sql(text('SELECT "raceId", "constructorId" FROM results;'),
                       con=connection)
example6
'''
# text() wraps SQL as a SQLAlchemy executable text construct; it does not run it.
# pd.read_sql(query, connection) executes a read and returns a DataFrame. The
# second argument can be positional or named con=connection. SELECT * means ALL
# columns, not "all data from a column" as one notebook comment describes it.
# example5 gives one mean per driver but omits the driver IDs from its output.
# Add "driverId" to SELECT if you want those groups identified in the result.
# example6 is the completed exercise selecting two mixed-case column names.
# Triple-quoted SQL strings, as used in Lecture 20's examples here, are another
# way to preserve multiline SQL without explicit Python line continuations.
#
# Persistence: ordinary SELECT results are held in Python/session memory; reading
# does not modify the stored tables. Committed uploads/creation/drops persist and
# are visible to other users with access. Uncommitted changes depend on transaction
# handling; not every database statement becomes permanent merely by being typed.


# %% 9. CONGRESS TABLES, KEY CHECKS, AND LEFT JOIN — Lecture 21b
# ============================================================================
# Reuse connection_python with your own server details; do not create a different
# database merely because the lecture moves from racing data to Congress data.
load_congress_python = r'''
bills_actions = pd.read_csv("data_raw/bills_actions.csv")
us_congress_members = pd.read_csv("data_raw/us_congress_members.csv")
bills_actions.to_sql("bills_actions", con=connection, if_exists="replace", index=False)
us_congress_members.to_sql("us_congress_members", con=connection,
                           if_exists="replace", index=False)
data = pd.read_sql(text("SELECT * FROM bills_actions;"), connection)
display(data)
'''
# display(data) is the notebook rich display. The exercise asks you to read and
# display us_congress_members similarly; substitute its table name in SELECT.
# The stray "Import races" comment in the notebook actually uploads members.
#
# ERD = entity relationship diagram: tables/columns and relationships between them.
# The lecture diagram links members.member_id to actions.member_id; one member
# can have many actions. The diagram calls the action table bill_actions, while
# the actual CSV/SQL table name used by the notebook is bills_actions.
# A primary key identifies each row uniquely and cannot be NULL. The ERD describes
# this role; to_sql does not automatically enforce the displayed relationship.

check_member_key_python = r'''
summary = pd.read_sql(text("SELECT COUNT(DISTINCT member_id) AS num_distinct, \
                           COUNT(*) AS num_members \
                           FROM us_congress_members;"), connection)
summary
'''
# DISTINCT counts each non-NULL member ID once. COUNT(*) counts all rows.
# Equal counts here imply every row has a different, non-NULL member_id; lower
# distinct count means duplicates and/or NULLs. This checks data, not constraints.
# Local CSV check at addition: 1,811 member rows with 1,811 distinct, nonmissing IDs.

join_members_python = r'''
example = pd.read_sql(text("SELECT * \
                           FROM bills_actions \
                           LEFT JOIN us_congress_members \
                           ON bills_actions.member_id = us_congress_members.member_id;"),
                      connection)
example
'''
# FROM gives the left/action rows. LEFT JOIN keeps them even without a member
# match; ON states equality of the keys. Missing right-side matches become NULL.
# Unique member IDs prevent multiple member matches from multiplying action rows.
# SELECT * includes both tables' member_id columns; select specific columns if
# you need a DataFrame with unambiguous names. A join does not alter either table.


# %% 10. MERGING ON SEVERAL COLUMNS — Lecture 21c
# ============================================================================
load_subjects_python = r'''
bills_actions = pd.read_csv("data_raw/bills_actions.csv")
bills_subjects = pd.read_csv("data_raw/bills_subjects.csv")
bills_actions.to_sql("bills_actions", con=connection, if_exists="replace", index=False)
bills_subjects.to_sql("bills_subjects", con=connection, if_exists="replace", index=False)
'''
# CORRECTION: the notebook reads bills_actions.csv into BOTH variables. Read
# bills_subjects.csv for the second one, or the join becomes an unintended self-join.

join_subjects_python = r'''
example = pd.read_sql(text("SELECT * \
                           FROM bills_actions \
                           LEFT JOIN bills_subjects \
                           ON bills_actions.congress = bills_subjects.congress \
                           AND bills_actions.bill_number = bills_subjects.bill_number \
                           AND bills_actions.bill_type = bills_subjects.bill_type;"),
                      connection)
example
'''
# ALL three conditions must match. A bill number alone can repeat across congress
# sessions or bill types. Joining with OR would match unrelated bills.
# The diagram shows bill identity shared by action and subject records. A bill can
# have multiple actions AND multiple subjects, so this can be a many-to-many join.
# Despite the phrase "multiple primary keys", the three columns are a composite
# JOIN KEY here: they do not uniquely identify each action or subject row.
# Local CSV check: 3,303 action rows, 1,809 repeated-key rows; 158,698 subject rows,
# 142,334 repeated-key rows (duplicates counted after the first row for each key).
# If a bill has 2 action rows and 3 subject rows, matching produces 6 rows. This
# is expected SQL behavior; be careful counting actions after joining to subjects.
# The type of relationship and intended unit of observation determine whether
# that expansion is useful. Do not assume the joined row count equals the left
# table's row count simply because the join is LEFT.
#
# Lecture resources: its introduction-to-databases and ERD links point to
# https://www.youtube.com/watch?v=wR0jg0eQsZA
# Further SQL tutorial linked in 21a: https://www.w3schools.com/sql/
# These external links are references, not additional class examples in this file.
