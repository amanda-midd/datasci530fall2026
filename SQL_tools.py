"""SQL — CLASS LECTURE REFERENCE (Lecture 20)

Source: Lecture 20/Lecture 22 - Introduction to SQL.sqlbook.
The filename says 22, but the folder and internal lecture heading say 20.
Added November 12, 2026.

HOW TO USE
This .py file holds lecture SQL examples as multiline Python strings, with notes.
Copy the SQL INSIDE a string into a SQLBook code cell and run it using your
PostgreSQL Active Connection. Do not copy the Python variable name or quotes.
Running this Python file only stores strings; it does not connect to a server,
execute queries, create tables, or delete data. No new helper functions exist.

CONTENTS
1. Connection and SQL formatting
2. Create tables and insert rows
3. Select columns, filter rows, and sort
4. Aggregate, group, and filter groups
5. Merge tables with LEFT JOIN
6. Exercises and Python comparisons

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
