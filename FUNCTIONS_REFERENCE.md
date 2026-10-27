# Function reference — Lectures 1–15

Covers Lectures 1–12, audited October 15, 2026 against 47 local notebooks (including exercises and optional material), five supporting Python scripts, and the Lecture 5 introductory slides. Includes calls in code, examples in Markdown/comments, named exercise functions, and formatting shown in reference figures. Repeated library functions share entries; distinct receiver types and important options are described separately. This is a reference snapshot; pulling new lectures does not automatically update it. External reading links are not additional lecture content.

**Reading the syntax:** `df` = DataFrame; `s` = one column (Series); `a` = array; other unquoted names are placeholders to replace with your variables. Quoted text is a string; replace placeholder column names and paths inside the quotes. Entries show the inputs and options taught, not every option available in the library. Code blocks are syntax templates, not a script to run top to bottom.

Lectures 13a–13b and 14a–14b added October 27, 2026, including Markdown explanations, commented-out examples, current exercise code, and imported-only helpers. Earlier coverage was audited on the date above; the reference now covers 51 notebooks in total.

Lecture 15 added October 27, 2026, including all code calls, scoring options, Markdown explanations, and the random-forest exercise. Total coverage is now 52 notebooks.

Functions defined by the lectures must be defined or imported before use; see each lecture's custom-function entries. Imported-only helpers have a separate section with explicitly supplemental examples. Corrections to notebook typos are collected at the end.

## Packages and imports

Run installation commands in the terminal, in your course environment. `json`, `time`, `functools`, `os`, and `datetime` are built into Python. Lecture 9b also shows `!pip install wordcloud` in a notebook cell; `!` runs a shell command and is not valid ordinary Python script syntax.

```sh
pip install numpy pandas matplotlib requests jmespath ipython beautifulsoup4 html5lib selenium webdriver-manager multiprocess wordcloud
pip install statsmodels maketables linearmodels scikit-learn patsy
pip install graphviz ISLP
pip install ucimlrepo
# Alternative installation syntax from the lectures:
conda install package_name
conda install conda-forge::html5lib
conda install conda-forge::selenium
conda install conda-forge::webdriver-manager
conda install conda-forge::multiprocess
conda install wordcloud
conda install statsmodels
conda install -c conda-forge linearmodels
conda install python-graphviz
```

```python
import numpy as np                         # Arrays, mathematics, random numbers.
import pandas as pd                        # Tables and data manipulation.
import matplotlib.pyplot as plt            # Charts.
import requests                            # HTTP/API requests.
import json                                # JSON encoding and decoding.
import os                                  # Working directory, paths, and folders.
import functools                           # Create function variants with fixed arguments.
import multiprocess as mp                  # Run functions across processor workers.
from wordcloud import WordCloud, STOPWORDS  # Word clouds and default words to exclude.
import statsmodels.api as sm               # Matrix-based statistical models and families.
import statsmodels.formula.api as smf       # Formula-based statistical models.
import maketables as mt                    # Regression tables and export.
import patsy                               # Build response/design matrices from formulas.
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay, get_scorer_names
from sklearn.svm import SVC
from sklearn import preprocessing
from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor as DTR
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor as RF
from sklearn.ensemble import GradientBoostingRegressor as GBR
import sklearn.model_selection as skm
from sklearn.model_selection import cross_validate, KFold, ShuffleSplit
import graphviz
import ISLP
from ISLP import load_data
from ISLP.models import sklearn_sm, summarize
from matplotlib import ticker
import matplotlib.dates as mdates
from linearmodels.datasets import wage_panel
from linearmodels.panel import BetweenOLS, FirstDifferenceOLS, PanelOLS, PooledOLS, RandomEffects
import jmespath                            # Search nested JSON data.
from IPython.display import display, HTML   # Notebook display and HTML objects.
from bs4 import BeautifulSoup              # Parse HTML.
from selenium import webdriver             # Browser automation.
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Also imported by the Lecture 6 script; no calls demonstrated:
import time                                # Time utilities.
import html5lib                            # Additional HTML parser.
from selenium.webdriver.support.ui import WebDriverWait  # Explicit waits.
from selenium.webdriver.common.by import By             # Locator constants.
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command  # WebDriver commands.
```

Excel `.xlsx` read/write may additionally require `openpyxl` (`pip install openpyxl`); no import is needed. Chrome must be installed for the browser sections. `HTML` is imported in Lecture 5; rendering there uses `%%html`.

Additional imports without demonstrated calls in Lectures 11–12: `from datetime import date, time, datetime` (standard library), `from linearmodels.datasets import mroz`, `from linearmodels.iv import IV2SLS`, `from sklearn.metrics import classification_report`, and `from statsmodels.iolib.summary2 import summary_col`. Importing `time` from `datetime` replaces the name of the `time` module if both imports are run in one environment.

## Lecture 1 — Python basics, files, and NumPy

### Built-ins and basic formatting

```python
print(value)                  # Print a value; print(value1, value2) prints several.
type(value)                   # Return its type: int, float, str, list, etc.
str(value)                    # Convert to a string.
int(value)                    # Integer conversion; truncates a float toward zero.
float(value)                  # Floating-point conversion; e.g. float("3.5").
bool(value)                   # Truth-value conversion; empty objects and numeric zero are False.
list(iterable)                # Convert an iterable to a list.
len(obj)                      # Number of items; for a DataFrame, number of rows.
display(obj)                  # Rich notebook display, including tables.

name = value                  # Assign a value; names are unquoted.
"text"                        # Strings use matching single or double quotes.
True                          # Boolean literals are True and False, unquoted.
[value1, value2]               # List: square brackets, comma-separated values.
{"key1": value1, "key2": value2}  # Dictionary: key:value pairs in braces.
items[i]                      # List/array index: first item is 0.
items[-1]                     # Last item; negative indices count backward from the end.
items[start:stop]              # Slice includes start, excludes stop.
items[i][j]                   # Index a nested list.
mapping["key"]                # Retrieve a dictionary value by key.
mapping["outer"]["inner"]     # Retrieve a nested dictionary value.
records[i]["key"]             # Retrieve a field from a list of dictionaries.
text1 + text2                 # Join strings; convert numbers with str() first.
list1 + list2                 # Join lists.
x + y; x - y; x * y; x / y     # Arithmetic; parentheses control grouping.
x ** power                    # Exponentiation; **, not ^.
```

`int`, `float`, `str`, and `bool` are also type objects, used without parentheses in type checks such as `isinstance(value, int)`. These conversion examples explain the types introduced in the lectures. A tuple is written `(value1, value2)`; a one-item tuple needs a trailing comma: `(value,)`. Do not name a variable `list`, `str`, or another built-in you need to call later.

### Read and write datasets

Paths are quoted strings, relative to the current working directory or absolute. Destination folders must exist.

```python
pd.read_csv("folder/file.csv")                 # Read CSV into a DataFrame.
pd.read_stata("folder/file.dta")               # Read Stata data.
pd.read_excel("folder/file.xlsx")              # Read the first Excel sheet.
pd.read_excel("folder/file.xlsx", sheet_name="sheet")  # Read a named sheet.
df.to_csv("folder/file.csv")                   # Write CSV; includes index by default.
df.to_stata("folder/file.dta")                 # Write Stata; includes index by default.
df.to_excel("folder/file.xlsx")                # Write Excel; includes index by default.
```

### Arrays and mathematics

```python
np.array([value1, value2])         # Create a 1D array from a list.
np.array([[a11, a12], [a21, a22]]) # Create a matrix; nested lists are rows.
np.ones(n)                        # Array of n ones; n is a nonnegative integer.
a.shape                           # Dimension sizes as a tuple; no parentheses.
np.pi                             # Constant π; no parentheses.
np.log(x)                         # Natural logarithm; positive real inputs.
np.exp(x)                         # e raised to x.
np.sin(x)                         # Sine; x in radians.
np.cos(x)                         # Cosine; x in radians.
np.sqrt(x)                        # Square root; nonnegative real inputs.
np.round(a, decimals)             # Round to an integer number of decimal places.
np.sum(a)                         # Sum array elements (used again in Lecture 8).
np.mean(a)                        # Arithmetic mean.
np.std(a)                         # Standard deviation; population (ddof=0) by default.
np.min(a)                         # Minimum.
np.median(a)                      # Median (not np.mean).
np.max(a)                         # Maximum.
```

Arithmetic on arrays is elementwise. Shapes must be compatible for broadcasting; equal shapes work. Arrays can hold nonnumeric data, but numeric calculations require suitable numeric values.

### Random numbers

```python
np.random.seed(seed)                          # Integer seed; set before drawing to reproduce results.
np.random.normal(loc=mean, scale=sd, size=n)   # Normal draws; sd >= 0; n is number of draws.
np.random.chisquare(df=degrees, size=n)        # Chi-square draws; degrees > 0.
np.random.choice(values, size=n, p=probabilities)  # Draw from a 1D list/array (Lecture 2).
# Lecture 10 also names the first argument: np.random.choice(a=values, size=n, p=probabilities).
# p: one nonnegative probability per value; probabilities must sum to 1.
# choice samples with replacement by default; omit p for equal probabilities.
```

### Matrix operations

```python
np.column_stack((a, b))  # Stack 1D arrays as columns; equal lengths required.
np.matrix.transpose(X)  # Lecture syntax for transposing a 2D array; rows ↔ columns.
np.dot(X, Y)            # Dot product; for 2D matrices, X columns must equal Y rows.
np.matmul(X, Y)         # Matrix multiplication; same rule for 2D matrices.
np.linalg.det(X)        # Determinant; X must be square.
np.linalg.inv(X)        # Inverse; X must be square and nonsingular.
```

## Lecture 2 — Conditions, selection, and loops

### Conditions and control flow

```python
isinstance(value, int)   # Check type; int, float, str are type objects, not strings.
x == y                  # Equality; = is assignment.
x < y; x <= y           # Less than; less than or equal.
x > y; x >= y           # Greater than; greater than or equal.
item in items           # Exact membership in a list.
"text" in sentence      # Case-sensitive substring search in a string.
not condition           # Negate a single Boolean condition.
(condition1) & (condition2)  # AND; parenthesize each comparison.
(condition1) | (condition2)  # OR; parenthesize each comparison.
# Array comparisons return elementwise Booleans. if requires one truth value.

if condition1:          # Colon required; indent each body consistently (4 spaces).
    statement
elif condition2:        # Optional additional condition(s).
    statement
else:                   # Optional fallback; no condition after else.
    statement

for item in iterable:   # Loop through items; colon and indented body required.
    statement

range(n)                # Integer sequence 0 through n-1; n excluded (Lecture 6).
sum(values)             # Sum a numeric iterable.
a.sum()                 # Sum array elements.
```

### DataFrame selection and inspection

```python
df["column"]                   # Select one column as a Series.
df[["column1", "column2"]]      # Select columns as a DataFrame; double brackets.
df["new_column"] = values      # Create/replace a column; matching length or scalar.
df.columns                     # Column labels; no parentheses.
df.columns.values              # Column labels as an array.
df.head(n)                     # First n rows; omit n for 5.
pd.unique(s)                   # Distinct values in encounter order.
s.unique()                     # Series version of unique (Lecture 4).
df.sort_values(by="column", ascending=False)  # Descending; True gives ascending.
s.sort_values(ascending=True)  # Sort Series values; no by argument.

df.iloc[i, :]                  # One row by integer position; all columns.
df.iloc[[i, j], :]             # Multiple rows; list of integer positions.
df.iloc[start:stop, :]         # Row slice; stop excluded; either bound may be omitted.
df.iloc[:, j]                  # One column by integer position.
df.iloc[:, [i, j]]             # Multiple columns by integer positions.
df.iloc[[i, j], [k, m]]        # Selected rows and columns by integer positions.
df[condition]                  # Keep rows where a Boolean Series is True (Lecture 3).
df.loc[condition, "column"]    # Select rows by condition and column by label (Lecture 3).
df.loc[condition, ["column"]]  # List of labels retains a DataFrame.
df.loc[condition, "column"] = value  # Assign into selected rows.
df.loc[["row_label1", "row_label2"]]  # Select rows by labels, not integer positions.
df.describe().loc[["mean", "std"]]    # Keep two summary rows (Lecture 10c).
df.copy()                      # Independent DataFrame copy (Lecture 3).
```

### Query formatting

```python
df.query("column >= @threshold")         # Expression is a string; @ uses a Python variable.
df.query('column == "text"')             # Quote string values inside the expression.
df.query("`column with spaces` > @value") # Backticks around awkward column names.
df.query("(column1 >= @low) & (column2 < @high)")  # Combine comparisons; | means OR.
df.query("column.str.isnumeric() == False")       # String accessor inside query (Lecture 3).
```

Inside `query`, ordinary column names are unquoted, external variables use `@`, and Boolean literals use `True`/`False`.

## Lecture 3 — Cleaning, statistics, and table formatting

### Construct, clean, and recode

```python
pd.DataFrame()                          # Empty table.
pd.DataFrame({"column1": values1, "column2": values2})  # Equal-length column lists.
pd.DataFrame(records)                   # List of dictionaries: one dictionary per row.
pd.DataFrame(mapping, index=[0])         # One row from a dictionary of scalar values.
pd.DataFrame(mapping.keys())            # Dictionary keys as a one-column table (Lecture 5).
df.dtypes                              # Type of every column; no parentheses.
s.dtype                                # Type of a single Series; s.dtypes also works.
np.nan                                 # Missing numeric value; no quotes or parentheses.
np.nanmean(a)                          # Mean ignoring NaNs.
s.str.isnumeric()                      # Numeric-character test on strings; not a number parser.
# Negative signs and decimal points do not pass isnumeric().
s.replace(old_value, new_value)         # Replace matching values.
s.replace([old1, old2], [new1, new2])    # Pairwise replacements; equal-length lists.
pd.to_numeric(s)                       # Convert to numbers; invalid text raises an error.
float("inf"); float("-inf")            # Positive/negative infinity for open-ended bin edges.
pd.cut(s, bins=edges, right=True, labels=labels)  # Assign values to intervals.
# edges: increasing numeric boundaries; len(labels) = len(edges)-1.
# right=True gives (lower, upper]; False gives [lower, upper).
# Out-of-range values become missing; with right=True, the lowest edge is excluded by default.
df.rename(columns={"old_name": "new_name"})  # Rename columns; dictionary maps old to new.
```

Assign returned results to retain changes: `s = s.replace(...)`, `df = df.rename(...)`. A literal backslash in a Python string is escaped: `"\\N"` represents the lecture's missing-value marker.

### Summaries, groups, and ranks

```python
df.describe()                        # Numeric count, mean, std, min, quartiles, max.
s.describe()                         # Summary of one column; output depends on its type.
s.mean()                             # Mean; pandas skips missing values by default.
s.median()                           # Median; skips missing values.
s.std()                              # Sample standard deviation (ddof=1).
s.min()                              # Minimum.
s.max()                              # Maximum.
s.sum()                              # Sum.
df.mean()                            # Column means for a numeric DataFrame.
df.std()                             # Column sample standard deviations; ddof=1.
pd.crosstab(index=s, columns="count") # Frequency table with a custom column label (Lecture 1).
table.columns.name = "label"         # Name the column axis, not the individual columns.

df.groupby("group")                  # Group by one column.
df.groupby(["group1", "group2"])    # Group by combinations of columns.
df.groupby("group").size()           # Number of rows in each group.
df.groupby("group")["column"].mean() # Group statistic; also .sum(), .std(), .min(), .max().

df.agg(output_name=("column", "mean"))  # Named aggregation without grouping.
df.groupby("group").agg(
    output_name=("column", "mean"),
    row_count=("column", len)
)
# Each keyword names an output; tuple is (source column, aggregation).
# String aggregations taught: "mean", "std", "min", "max", "sum".
# len is an unquoted callable and counts rows, including missing values.
# groupby().agg() creates one row per group, named outputs as columns.
# df.agg() above places output names on rows, source columns on columns.

df.groupby("group")["column"].transform("mean")  # Repeat group mean at each original row.
# Also taught: "std", "max", "min"; output aligns with the original data.
s.rank(method="dense", ascending=False)          # Largest value ranks 1; ties share ranks, no gaps.
df.groupby("group")["column"].transform(
    "rank", method="dense", ascending=True
)  # Rank within groups; True gives the smallest value rank 1.
```

Methods can be chained in order: `df.query(...).groupby(...).agg(...).sort_values(...)`. Wrap a multiline chain in parentheses.

### Number and table formatting

```python
f"{value}"              # Insert a variable/expression into a string.
f"{value:.0f}"          # Fixed-point, zero decimal places.
f"{value:.2f}"          # Fixed-point, two decimal places.
f"{value:,.2f}"         # Thousands separators and two decimal places.
f"${value:,.2f}"        # Literal currency symbol before the formatted value.
# A space after ':' reserves a leading sign space for positive numbers.
# \n inside a string inserts a newline.

df.style                # Styler object; no parentheses.
df.style.format({"column": "{:,.2f}", "other_column": "{:,.0f}"})
# Keys are existing column names; values are format strings containing {:...}.
# Use "${:,.2f}" for currency; formatting changes display, not stored values.
style.hide(axis="index")       # Hide row index; style is a Styler object.
style.set_caption("caption")   # Set table caption; chain after .style.format(...).
```

## Lecture 4 — Combining data and plotting

### Merge, concatenate, and reshape

```python
pd.merge(left, right, on="key", how="left")  # Keep left rows; match right rows by key.
pd.merge(left, right, on=["key1", "key2"], how="left")  # Match on multiple keys.
# Keys must exist in both tables (or be named index levels).
# Repeated right-side keys can multiply rows; unmatched right values become missing.
# Overlapping non-key column names receive _x (left) and _y (right).
# Select needed right columns with right[["key", "column"]] before merging.
pd.concat([df1, df2, df3])          # Stack rows; align columns by name, preserve indices.
# Columns absent from one table receive missing values for its rows.
df.drop(columns=["column1", "column2"])  # Return table without selected columns.
grouped_result.unstack("level")    # Move a named row-index level into columns for plotting.
```

### Charts and plot options — Lectures 1, 2, and 4

```python
plt.scatter(x=x_values, y=y_values)       # Scatterplot; x and y must have equal length.
plt.hist(x=values)                       # Histogram from a 1D sequence.
plt.hist(x=values, bins=n, color="color", alpha=opacity)
# Optional: bins = integer bin count or numeric edges; color = color string;
# alpha = 0 (transparent) through 1 (opaque).

series_or_df.plot(kind="bar", stacked=False)  # Vertical bars; True stacks column series.
series_or_df.plot(kind="barh")                # Horizontal bars.
series_or_df.plot(kind="line")                # Line chart.
grouped_series.plot.hist(alpha=opacity)       # Overlay histograms for groups.
# grouped_series comes from df.groupby("group")["numeric_column"].
# Multi-group bars use grouped_result.unstack("level").plot(...).

plt.xlabel("label")          # X-axis label.
plt.ylabel("label")          # Y-axis label.
plt.title("title")           # Plot title.
plt.legend(labels=labels, title="title")  # Labels in plotted-series order; title optional.
plt.legend(title="title", bbox_to_anchor=(x, y), loc="center left")
# bbox_to_anchor: coordinate tuple; usual axes coordinates run 0–1.
# loc: which part of the legend attaches to that point; omit labels to use plot labels.
plt.style.available           # Available style names; no parentheses.
plt.style.use("style_name")   # Apply an available style; "default" resets it.
plt.savefig("folder/plot.png") # Save figure; .jpg also taught; save before show().
plt.show()                    # Display figure; parentheses required.
```

Repeated plotting calls before `plt.show()` overlay plots. Place `plt.show()` between calls for separate plots.

## Lecture 5 — Scripts, APIs, JSON, and HTML

### Files and scripts

```python
open("folder/file.txt", "r")  # Open text file; "r" reads (default), "w" creates/overwrites.
file.read()                   # Read file contents into a string.
file.write(text)              # Write a string; does not add a newline automatically.

with open("folder/file.txt", "w") as file:
    file.write(text)          # Colon and indentation required; file closes on block exit.

exec(code_string)             # Execute Python source text.
exec(open("./scripts/import_packages.py").read())  # Run the lecture import script.
os.getcwd()                  # Current working directory as a string.
os.path.join(base_dir, "folder", "file.json")  # Build a path using OS separators.
os.makedirs("folder/subfolder", exist_ok=True)  # Create parent folders; allow an existing folder.
```

Relative paths are resolved from the working directory, not necessarily the notebook's location. Import `os` before the Lecture 5b path examples. Use the actual response variable when saving; a name such as `AI_search_results` must already have been assigned.

Lecture 5 also splits long expressions across lines. Parentheses allow line breaks inside an expression; a backslash at the end of a line explicitly continues it and must not be followed by a comment or other characters.

```python
message = ("First part "
           + "second part")
```

### API requests and JSON

```python
requests.get(url)                       # HTTP GET; url is a complete URL string.
response.json()                         # Decode response JSON into Python objects.
requests.get(url).json()                # Request and decode in one chain.
json.dumps(obj, indent=4)               # Python dict/list → JSON string; indent is optional.
json.dump(obj, file, indent=4)          # Write JSON directly to an already-open text file.
json.loads(json_text)                   # JSON string → Python dict/list/scalar.
mapping.keys()                         # View dictionary keys, not nested keys.
mapping.get("key")                     # Retrieve a value; missing key returns None.
mapping.get("key", default_value)      # Use a chosen fallback for an absent key.
jmespath.search("expression", obj)     # Query decoded data; expression is a string.
```

JMESPath expression formats:

| Expression | Meaning |
| --- | --- |
| `"outer.inner"` | Follow nested object keys. |
| `"[0]"` | First item in a list; zero-based. |
| `"[0].field"` | Field from the first list item. |
| `"[*].field"` | Field from each list item. |

JSON text uses double-quoted keys/strings and `true`/`false`/`null`; decoded Python uses dictionaries/lists and `True`/`False`/`None`.

Use `with open("folder/file.json", "w") as file:` followed by an indented `json.dump(obj, file, indent=4)` to save JSON directly. `json.dumps` returns a string, while `json.dump` writes to a file and returns `None`. Dictionary `.get()` only substitutes its default for an absent key, not for an existing key whose value is `None`.

### HTML syntax taught alongside the functions

`%%html` must be the first line of a Jupyter code cell; put raw HTML on subsequent lines.

| Syntax | Purpose / required formatting |
| --- | --- |
| `<tag>content</tag>` | Container; matching opening/closing tags. |
| `<html>…</html>`, `<head>…</head>`, `<body>…</body>` | Document, metadata section, visible content. |
| `<title>text</title>` | Document title inside head. |
| `<meta name="name" content="value">` | Metadata; no closing tag. |
| `<meta charset="utf-8">` | Specify the document character encoding. |
| `<header>…</header>`, `<span>…</span>` | Header region and inline text container; also used for targeting in Lecture 6. |
| `<div class="class_name">…</div>` | Section with a CSS class. |
| `<p>text</p>`, `<h1>text</h1>`, `<br>` | Paragraph, heading, line break. |
| `<!-- comment -->` | HTML comment. |
| `<style>.class_name { property: value; }</style>` | CSS class rule; leading dot, braces, colon, semicolon. |
| `<form>…</form>` | Form container. |
| `<form action="/action_page.php">…</form>` | Form whose submission targets the given address. |
| `<input type="submit" value="Submit">` | Submit control for a form. |
| `<select><option value="value">label</option></select>` | Dropdown; value is internal, label is visible. |
| `<label for="field_id">text</label>` | Label; for must match the input's id. |
| `<input type="text" id="field_id" value="text">` | Text field; no closing tag. |
| `<input type="checkbox" id="field_id" name="name" value="value">` | Checkbox; no closing tag. |

CSS properties taught: `background-color: color;`, `color: color;`, `border: width style color;`, `margin: size;`, `padding: size;`. Widths and sizes use units such as `px`.

## Lecture 6 — Web scraping and interaction

### Browser setup

```python
options = Options()                        # Chrome settings; also webdriver.ChromeOptions().
options.add_argument("--headless=new")      # Optional: hide browser; omit to show it.
ChromeDriverManager().install()            # Obtain ChromeDriver; return its path.
Service(driver_path)                       # Configure driver service from that path.
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)                                         # Launch Chrome with the lecture's driver manager.
# Alternative from Lecture 6d: driver = webdriver.Chrome(options=options)
driver.get(url)                            # Navigate to a URL string.
driver.close()                             # Close current window/tab.
driver.quit()                              # End session and close all its browser windows.
```

The lecture's `options.headless = True/False` is legacy syntax; use the argument above or omit it. See [Selenium's headless change](https://www.selenium.dev/blog/2023/headless-is-going-away/). The imports above also correct `service` → `Service` and use the public [IPython display module](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html).

### Find and extract elements

```python
driver.find_element("xpath", xpath_string)   # First match; raises if no element matches.
driver.find_elements("xpath", xpath_string)  # List of all matches; [] if none.
element.find_element("xpath", xpath_string)  # Search from an existing element.
element.find_elements("xpath", xpath_string) # Multiple matches from an existing element.
element.get_attribute("attribute")          # Attribute value; "class", "role", "value" taught.
element.get_attribute("outerHTML")          # HTML including the element's own tag.
element.get_attribute("innerHTML")          # HTML inside the element.
element.text                                # Visible text; property, NOT .text().
BeautifulSoup(html_text, "html.parser")      # Parse HTML string with the built-in parser.
soup.prettify()                             # Formatted HTML string from a BeautifulSoup object.
text.splitlines()                           # List of lines; [0] selects first if nonempty.
```

XPath formats (pass the entire path as a quoted string):

| XPath string | Meaning |
| --- | --- |
| `'//tag'` | Match tag anywhere in the document. |
| `'//parent/child'` | Direct child tags of matching parents. |
| `'/html/body/…'` | Absolute path from the document root; replace … with actual steps. |
| `'child'` | Direct children of the current element. |
| `'.//tag'` | Descendants of the current element; use for searches within a result. |
| `'//tag[@attribute="value"]'` | Match tag and exact attribute value. |
| `'//*[@attribute="value"]'` | Match any tag with that exact attribute value. |
| `'.//tag[@attribute="value"]'` | Attribute match restricted to current element's descendants. |
| `'path[1]'` | First matching item at that path step; XPath positions start at 1. |

Use different inner/outer quote styles. A leading `//` searches from the document root even when called on an element; `.//` keeps the search inside it. Lists returned to Python still use zero-based indexing.

### Forms and storing results

```python
select = Select(element)                  # Wrap an HTML <select> element.
select.options                            # List of option elements; no parentheses.
select.select_by_visible_text("label")    # Match displayed option text.
select.select_by_index(i)                 # Select by zero-based integer position.
select.select_by_value("value")           # Match option's HTML value attribute as a string.
element.clear()                          # Clear an editable text field.
element.send_keys("text")                # Type text into the field.
element.send_keys(Keys.RETURN)            # Press Return; Keys.RETURN is unquoted.
element.click()                          # Click the element.
items.append(value)                       # Add one item to a list in place; returns None.
records.append({"field1": value1, "field2": value2})  # Add one extracted record.
pd.DataFrame(records)                     # Convert stored records into table rows.
```


## Lecture 7 — Loops, while loops, and simulations (7a–7c)

Uses the existing `numpy as np`, `matplotlib.pyplot as plt`, and `pandas as pd` imports; no new packages.

### Lists and numeric conversion — 7a

```python
None                         # Null placeholder; capital N, no quotation marks.
items = []                   # Empty list to fill using .append(value).
items = [None] * n           # Preallocate n placeholders; n is a nonnegative integer.
[value] * n                  # Repeat a single value n times.
items * n                    # Repeat an entire list n times; does not multiply its values.
items[i] = value             # Replace an existing position; first position is 0.
index = index + 1            # Increase a counter; initialize it before the loop.
pd.to_numeric(s, errors="coerce")  # Convert to numbers; invalid entries become NaN.
```

Use `items.append(value)` to grow a list or `items[i] = value` to fill existing positions. Multiplying a NumPy array by a number multiplies each element instead of repeating the list.

### Indexed loops, nested loops, and comprehensions — 7a

```python
list(range(n))               # List of integers from 0 through n-1.

for i in range(len(items)):   # Iterate over valid zero-based positions.
    value = items[i]
    statement

for outer_value in outer_items:
    for inner_value in inner_items:
        statement            # Inner body is indented twice (8 spaces).
    statement                # Runs after the inner loop, once per outer iteration.

[expression for value in items]       # List comprehension: one result per item.
[expression for i in range(n)]        # Indexed comprehension; expression can use i.
lower <= value <= upper              # Inclusive chained comparison of scalar values.
```

Each loop header ends with `:`. The inner loop runs fully for each outer item. When using one index across multiple lists, that index must exist in every list.

```python
for value in items:
    if skip_condition:
        continue             # Skip the rest of this iteration; proceed to the next.
    statement

for value in items:
    if stop_condition:
        break                # Exit the innermost loop immediately.
    statement
```

### While loops — 7b

```python
while condition:             # Test before each iteration; repeat while True.
    statement
    update_statement         # Update the state used by the condition.
```

Initialize the condition's variables before the loop. Use a colon and an indented body. A condition that starts false runs zero times; a condition that never becomes false requires `break` to stop. When indexing a list, stop before the index reaches `len(items)`.

### Random draws and simulation summaries — 7c

```python
np.random.uniform(low=lower, high=upper, size=n)  # Uniform draws; lower < upper, n draws.
# Intended interval: [lower, upper); floating-point rounding may include upper.
a.mean()                     # NumPy array mean; equivalent to np.mean(a).
a.std()                      # NumPy standard deviation; default ddof=0, not pandas' ddof=1.
np.mean(boolean_values)       # Proportion True; True counts as 1, False as 0.
```

The lecture also reuses `np.random.normal(loc=mean, scale=sd, size=n)`, `np.random.chisquare(df=degrees, size=n)`, and `np.sqrt(n)` from Lecture 1. In simulations, `size` is the number of observations per draw; `range(num_simulations)` controls the number of repeated draws. Initialize result storage before the simulation loop, and reset it inside each outer loop when comparing sample sizes. For a sample standard deviation, use `a.std(ddof=1)`; the lecture's `a.std()` uses `ddof=0`.

### Subplots — 7c

```python
fig, axes = plt.subplots(nrows, ncols, figsize=(width, height))
# Returns a Figure and its Axes; row/column counts are positive integers.
# figsize is a (width, height) tuple in inches.
# With one row or column and multiple panels: axes[i], zero-based.
# With multiple rows AND columns: axes[row, column], zero-based.
# With just one panel: axes is a single Axes object; do not index it.

ax.hist(x=values)             # Histogram on one Axes; ax is axes[i] or another selected Axes.
ax.set_title("title")         # Title for that subplot.
ax.set_xlabel("label")        # X-axis label for that subplot.
ax.set_ylabel("label")        # Y-axis label for that subplot.
plt.tight_layout()           # Adjust subplot spacing; call after labels, before show/save.
```

## Lecture 8 — Functions, mapping, scripts, and multiprocessing (8a–8d)

### Define and call functions — 8a

```python
def function_name(parameter1, parameter2):  # Define a reusable function; colon required.
    result = expression                     # Parameters and intermediate values are local.
    return result                           # Send a value back to the caller.

function_name(argument1, argument2)         # Positional arguments follow parameter order.
function_name(parameter1=value1, parameter2=value2)  # Keyword arguments use parameter names.

function_name = lambda parameter1, parameter2: expression
# A lambda is a one-expression function; its expression is returned automatically.
```

Defining a function does not run its body. Call it with parentheses to run it. `return value` makes a result available to the caller; `print(value)` only displays it. A function without `return` returns `None`. The lecture uses `fn_` as an optional naming convention for function objects.

```python
def fn_agebracket(age):
    if age >= 18:
        status = "Adult"
    elif (age >= 10) & (age < 18):
        status = "Adolescent"
    else:
        status = "Child"
    return status
```

### Apply and map functions over values — 8b and 8d

```python
s.apply(function_name)                    # Apply a one-argument function to each Series value.
s.apply(lambda value: expression)         # Define the elementwise function inline.
map(function_name, iterable1)             # Lazy map object: one function result per item.
list(map(function_name, iterable1))       # Materialize mapped results as a list.
list(map(function_name, iterable1, iterable2))  # Pass paired items to a two-argument function.
```

With multiple iterables, `map` stops when the shortest iterable is exhausted. Assign the result to a DataFrame column to create or replace it; the result length must match the number of rows.

```python
df["new_column"] = df["column"].apply(function_name)
df["new_column"] = list(map(function_name, df["column1"], df["column2"]))
```

Use `df.drop(columns=[...])` from Lecture 4 to remove columns after mapping.

### Run and import external Python scripts — 8b

```python
import scripts.example_functions as ef            # Import a module with an alias.
ef.fn_quadratic(x)                                 # Access an imported function through the alias.
import scripts.example_variables as ev
ev.alpha                                           # Access an imported module variable.
```

An imported `.py` file is a module; a folder containing modules can be a package. The `exec(open(...).read())` pattern from Lecture 5 runs a script that can read and modify names in the current environment. Imported module contents stay in the module namespace and are referenced as `alias.name`, reducing accidental name collisions.

### Multiprocessing and partial functions — 8c

```python
mp.cpu_count()                              # Number of logical CPUs available to Python.

with mp.Pool(processes) as pool:            # Create and automatically close a worker pool.
    results = pool.map(function_name, items) # Apply function in parallel; preserve item order.

functools.partial(function_name, parameter=value)  # New callable with an argument fixed.
```

`processes` is a positive integer, often stored from `mp.cpu_count()`. The mapped function must accept one item from `items`; use `functools.partial` to fix its other arguments. Pool workers run separately, so do not rely on them to update ordinary variables in the notebook. When each result is a DataFrame, combine the returned list with `pd.concat(results)`.

### Local and global variables — 8d

```python
global_name = value                  # A name assigned outside a function is global.

def function_name(parameter):
    local_name = expression          # Parameter and assigned name are local to this call.
    return local_name

def modify_global():
    global global_name               # Declare assignment to the existing global name.
    global_name = new_value
```

A function can read a global name, but the lecture recommends passing every input as a parameter. Local names exist only during the call and take precedence over same-named globals. Use `global` only when the function intentionally must reassign a module-level variable; returning a value and assigning it outside the function is usually clearer.

### Exact custom-function names from Lecture 8

These are user-defined examples, not built-in Python functions. The signatures below omit `self` because Python supplies it for bound method calls. Redefining a name replaces its previous definition in the current environment.

| Lecture | Call / definition name | Inputs, behavior, and return value |
| --- | --- | --- |
| 8a | `function_v(P, r, n, t)`; `fn_v(P, r, n, t)` | Compound value `P * (1 + r/n)**(n*t)`; `n` must not be zero. `fn_v` is the lambda version. The comment's `fn_compute_value` is a suggested name, not another implemented function. |
| 8a | `function_poly(x)` | Return `x**2 + 2*x + 1`. |
| 8a | `fn_grade(numeric_grade)` | Print `"pass"` for grades at least 55, otherwise `"fail"`; the current code returns `None`. The exercise asks for a returned status, which would require `return status`. |
| 8a | `fn_name_car(first_name, last_name, car_model)` | Print the customer/car message with f-strings and newlines; current code returns `None`, rather than the string requested in the exercise. |
| 8a | `fn_sum(x, y, z)` | Lambda returning the sum of three arguments. |
| 8b, 8d | `fn_sum(x, y)` | Redefined lambda returning the sum of two arguments; used by `map`. |
| 8a–8d | `fn_iseligible_vote(age)` | Return the Boolean test `age >= 18`. |
| 8b, 8d | `fn_istwenties(age)` | Return `(age >= 20) & (age < 30)`. |
| 8b, 8d | `fn_agebracket(age)` | Return `"Adult"` for age ≥18, `"Adolescent"` for 10–17, otherwise `"Child"`. |
| 8b script | `ef.fn_quadratic(x)` | Return `x**2`; `ef` aliases `scripts.example_functions`. |
| 8b script | `ef.fn_cubic(x)` | The provided script actually returns `x**2`, despite its name; a cubic would use `x**3`. |
| 8b script | `ef.message_hello(x)` | Return `"hi " + x`; x must be a string. |
| 8c | `fn_twoarguments(x, y)` | Lambda returning `x + y`. |
| 8c | `fn_oneargument(x)` | Callable made with `functools.partial(fn_twoarguments, y=2)`; returns `x + 2`. |
| 8c | `bubble_sort(x)` | First definition doubles an array; the later definition returns a one-row DataFrame with `x_bar=np.sum(x)` and `xsd=np.std(x)`. Neither version sorts; `x_bar` is a sum despite the label. |
| 8c | `simulate_estimator(iteration)` | Draw a uniform sample using global `sample_size`; return a one-row DataFrame with mean `xbar` and standard deviation `xsd`. `iteration` is accepted for `pool.map` but unused in the calculation. |
| 8d | `fn_add_recommended(x, y, z)` | Return `x + y + z`, with every input passed explicitly. |
| 8d | `fn_add_notrecommended(x, y)` | Return `x + y + z` using global z; fails if z is undefined. |
| 8d | `fn_square(x)` | Return `x**2` using a local intermediate y; does not reassign global x or y. |
| 8d | `modify_x()` | Add 5 to global x in place; x must exist first; returns `None`. |

`my_function(parameter)` and `myfunction` in the prose are placeholder names for the `def`, `lambda`, `apply`, and `map` templates, not additional library functions. `example_script.py` creates `message_output` from an existing `message`; it does not define a function. `example_variables.py` defines module attributes `alpha`, `beta`, `gamma`, `delta`, and `epsilon`, accessed through `ev.name`.

## Lecture 9 — Text data, word clouds, and classes (9a–9d)

Reviewed against the current notebooks and completed exercises on October 5, 2026.

### Text frequencies, filtering, and replacement — 9a

```python
s.value_counts()                       # Count distinct values; descending counts, missing values excluded.
df.query("category in @categories")    # Keep categories in an external list named categories.
s.str.contains("text")                # Test each string for a match; case-sensitive, regex by default.
s.str.contains("text", regex=False, na=False)  # Literal substring; missing values become False.
s.str.replace("old", "new", regex=False)     # Replace literal substrings within each string.
s.str.findall(r"pattern")             # List of all non-overlapping regex matches in each string.
```

Use `df[s.str.contains(..., na=False)]` to filter rows and `.mean()` on a Boolean result to calculate the proportion matching. `.str.replace()` changes text inside values; `s.replace()` from Lecture 3 replaces whole values. Assign the returned result to retain changes. When adding a column to a filtered table, create an independent table with `.copy()` first.

### Regular expression syntax — 9a

Use raw strings such as `r"Amdt\.\d*"` so Python passes backslashes to the regex engine. A regex match is case-sensitive unless configured otherwise.

| Pattern | Meaning |
| --- | --- |
| `\d` | One digit. |
| `\D` | One non-digit character. |
| `\s` | One whitespace character, including spaces, tabs, and newlines. |
| `\S` | One non-whitespace character. |
| `.` | One character other than a newline by default. |
| `\.` | A literal period. |
| `*` | Zero or more repetitions of the preceding pattern; greedy by default. |
| `?` | Zero or one occurrence of the preceding pattern. |

```python
s.str.findall(r"Amdt\.\d*")  # 'Amdt.' followed by zero or more digits; includes the prefix.
s.str.findall(r".Amdt\.")    # One character before 'Amdt.'.
s.str.findall(r".*Amdt\.")   # Text through 'Amdt.'; greedy .* can span earlier occurrences.
s.str.findall(r"Senator \S*") # 'Senator ' followed by consecutive non-whitespace characters.
s.str.findall(r"Senator\s\S")  # 'Senator', one whitespace character, and the next non-whitespace character.
s.str.findall(r"Senator\s\S*") # Same prefix, followed by zero or more non-whitespace characters.
```

`*` allows an empty match for the part it repeats: the first example can match `"Amdt."` without a number. `\S*` can include punctuation and stops at whitespace, so it does not reliably extract an entire person's name. For a nonmissing string with no matches, `.str.findall()` returns an empty list.

### Join text and create word clouds — 9b

```python
"separator".join(strings)               # Combine strings, placing the separator between items.
text = " ".join(df["text_column"])     # Combine a text column with spaces between records.
# All items must be strings; handle missing values before joining.

STOPWORDS                              # Default set of common words excluded from word clouds.
stop_words = list(STOPWORDS) + ["custom", "words"]  # Extend the default exclusions.

cloud = WordCloud(
    background_color="white",
    stopwords=stop_words,
    width=400,
    height=200,
    relative_scaling=0.9
)
cloud.generate(text)                   # Generate a cloud from a string; returns the cloud object.
cloud.process_text(text)               # Return a dictionary of processed words and frequencies.
```

The constructor options are optional. `width` and `height` are pixel dimensions. `relative_scaling` ranges from 0 (rank only) to 1 (frequency ratios), or can be `"auto"`. Omit `stopwords` to use `STOPWORDS`; use `stopwords=[]` to exclude none. Generation needs at least one word remaining after processing. The notebook uses `"".join(...)`; a space separator avoids merging the last word of one record with the first word of the next.

Passing `stopwords=["the", "and", "to"]` replaces the default stopword collection with that list. To keep the default exclusions and add your own, use the `list(STOPWORDS) + [...]` pattern above.

```python
plt.imshow(cloud)                      # Display the generated cloud as an image.
plt.axis("off")                        # Hide axes, ticks, and borders.
ax.imshow(cloud)                       # Display on one Axes from plt.subplots().
ax.axis("off")                         # Hide axes on that subplot.
```

For subgroup comparisons, filter each group with `query`, join its text, and generate a separate cloud. Use `plt.subplots()` and `ax.set_title()` from Lecture 7 to arrange and label the panels.

### Classes, instances, and attributes — 9c

```python
class Course:                          # Class definition; colon and indented body required.
    hours = 9                          # Class attribute: a shared default.

course = Course()                      # Create an instance; parentheses required.
Course.hours                          # Read the class attribute.
course.hours                          # Read through the instance; no parentheses for attributes.
course.hours = 4                       # Set an instance attribute, overriding its class default.
Course.hours = 5                       # Change the shared class attribute.
```

An instance is an object created from a class. Class attributes are looked up when an instance has no attribute of its own with that name. Changing `Course.hours` therefore affects both new and existing instances that have not overridden `hours`; `course.hours` stays 4 in the example. Instances do not automatically receive independent copies of every class attribute. Store data specific to each instance using `self` in `__init__`.

### Initialize instances and call methods — 9c

```python
class Teacher:
    def __init__(self, first_name, last_name):  # Two underscores before and after init.
        self.first_name = first_name           # Store data on this instance.
        self.last_name = last_name

    def modify_lastname(self, last_name):      # A function in a class is a method.
        self.last_name = last_name

    def message(self):
        return f"{self.first_name} {self.last_name}"

teacher = Teacher("Alejandro", "Sanchez")    # __init__ runs when the instance is created.
teacher.modify_lastname("Sanchez-Becerra")   # Change the instance's stored attribute.
teacher.message()                            # Call a method with parentheses.
```

`self` is the conventional name for the current instance. Include it as the first parameter in instance-method definitions; Python supplies it automatically when calling a method through an instance. `__init__` initializes attributes and should not return a value. Other methods can return results, print messages, or update attributes, just as ordinary functions can.

### Inheritance — 9c

```python
class Student(Teacher):                # Child class inherits attributes and methods from Teacher.
    def __init__(self, first_name, last_name, program):
        super().__init__(first_name, last_name)  # Run the parent initializer in this example.
        self.program = program                  # Add a child-specific attribute.

student = Student("Alejandro", "Sanchez", "Data Science Masters")
student.message()                     # Use an inherited method.
student.program                       # Access the added attribute.
```

### Store and analyze text in a class — 9d

```python
text.lower()                          # Return a lowercase copy of a string.
text.split()                          # Split on whitespace into a list; no separator argument needed.
words.count(word)                     # Count exact matches in a list of words.

class TextAnalysis:
    def __init__(self, text):
        self.text = text

    def count_word(self, word):
        words = self.text.lower().split()
        return words.count(word.lower())

document = TextAnalysis("The bill is a Senate bill")
document.count_word("BILL")           # Returns 2; lowercase conversion makes this case-insensitive.
document.text = "The House passed the bill"  # Replace stored text for subsequent method calls.
```

Splitting on whitespace leaves punctuation attached: `"bill."` does not match `"bill"`. Each instance stores its own text and uses the same method definition. `WordCloud` uses the same instance-and-method pattern: create an object, then call its `.generate(text)` method.

### Exact custom-class names from Lecture 9

The earlier examples use shorter illustrative class names; these are the names in the actual notebooks. Run each class definition before creating its instances.

| Call / attribute | Use and behavior |
| --- | --- |
| `dsci_template()` | Create an instance using the class defaults `lecture1`, `lecture2`, `lecture3`, and `hours`; no constructor arguments. |
| `student_template(first_name_arg, last_name_arg)` | Initialize instance attributes `first_name` and `last_name`. |
| `teacher_template(first_name_arg, last_name_arg)` | Initialize a teacher with the same two instance attributes. |
| `teacher.modify_lastname_fn(last_name_arg)` | Replace `teacher.last_name`; returns `None`. |
| `teacher.message_fn()` | Print first and last names; returns `None`. |
| `dsci_template_input(first_name_arg, last_name_arg)` | Combine course class defaults with instance-specific names. |
| `student_messages(first_name, last_name, program)` | Initialize the parent through `super().__init__` and add `program`. |
| `student.messages()` | Print the student's name and program; returns `None`. |
| `text_template(text_arg)` | Store `text_arg` as the instance's `.text`. |
| `document.count_word(word_arg)` | Count exact whitespace-separated tokens after lowercasing both text and target; return an integer. |
| `weekday_template()` | Named exercise: define class defaults `message`, `class1`, and `class2`, then customize instances. No implementation is provided in the exercise cell. |
| `movie_template(name, year, quantity_sales, price_tickets)` | Named exercise: define an initializer storing these four attributes. |
| `movie.compute_revenue()` | Named exercise method: compute `self.quantity_sales * self.price_tickets`; use `return` to make that value available to the caller. |

## Lecture 10 — Linear regression, model tables, and custom prediction (10a–10d)

### Fit OLS and inspect results — 10a–10c

```python
model = smf.ols(formula="y ~ x", data=df)  # Specify an ordinary least squares model.
results = model.fit(cov_type="HC1")       # Fit with HC1 heteroskedasticity-robust standard errors.
results.params                           # Series of estimated coefficients; no parentheses.
results.params["Intercept"]              # Intercept by name.
results.params["x"]                      # Slope by name; avoid ambiguous integer indexing.
results.summary()                        # Detailed regression diagnostics and table.
print(results.summary())                 # Print the text summary.
round(value, 3)                          # Python built-in rounding to 3 decimal places.
abs(value)                               # Absolute value; also used inside df.query().
```

Use `cov_type="HC1"`, not Lecture 10a's `cov="HC1"`, to request robust standard errors; see the [OLS fit parameters](https://www.statsmodels.org/v0.12.2/generated/statsmodels.regression.linear_model.OLS.fit.html). Robust covariance changes standard errors, not the OLS coefficient estimates. Fit before accessing result attributes.

### Regression formulas — 10b–10c

Formulas are quoted strings; column names inside them are generally unquoted. The formula interface includes an intercept by default.

| Formula | Meaning |
| --- | --- |
| `"y ~ x"` | Outcome y explained by x and an intercept. |
| `"y ~ x + z"` | Include x and z as separate regressors. |
| `'y ~ x + Q("z with spaces")'` | Quote a column name containing spaces with `Q()`. |
| `"y ~ x + C(d)"` | Treat d as categorical; compare included levels with a reference level. |
| `"y ~ x + z + x:z"` | Include main effects and their interaction. |
| `"y ~ x * z"` | Shorthand for `x + z + x:z`. |
| `"y ~ x + I(x ** 2)"` | Include x and its square; syntax support for the polynomial exercise in Lecture 12b. `I()` protects arithmetic from formula-operator interpretation. |

`C()` and `Q()` here belong to formula syntax. In Lecture 10c, `treat * ave` allows the treatment difference to vary with baseline scores. The formula `treat + ave + treat*ave` repeats main effects in its text, but the formula parser includes each term only once.

### Display and export regression tables — 10b–10c

```python
table = mt.ETable([results], model_heads=["Model 1"])
table.make(type="gt")                    # Render a formatted table in the notebook.

comparison = mt.ETable(
    [results1, results2],
    model_heads=["Model 1", "Model 2"],
    keep=["x", "z", "z:x", "C(d)[T.2]"],
    exact_match=True,
    model_stats=["N", "r2"],
    model_stats_labels={"N": "Observations", "r2": "R-squared"},
    caption="Regression Results",
)
comparison.make(type="gt")
comparison.save(
    type="docx", file_name="results/regression_models.docx",
    show=False, replace=True
)
```

Pass fitted results in a list, with one heading per model. `keep` selects and orders displayed coefficients; with `exact_match=True`, use names from `.params.index` exactly, including interaction order and category labels. Omitting `Intercept` from `keep` hides it in the table, not in the fitted model. The output folder must exist; `replace=True` permits overwriting an existing export. Keep the `ETable` object to call `.save()` separately from `.make()`.

### Complete cases and manual OLS — 10d

```python
X.notnull()                             # Boolean table: True for nonmissing entries.
y.notnull()                             # Boolean Series for a nonmissing outcome.
X.notnull().all(axis=1)                  # True where every predictor in a row is present.
valid_rows = X.notnull().all(axis=1) & y.notnull()
X = X[valid_rows]                        # Apply the same mask to predictors and outcome.
y = y[valid_rows]

n = X.shape[0]                          # Number of rows.
W = np.c_[np.ones((n, 1)), X]            # Column-bind an intercept of ones and the predictors.
W.T                                    # Transpose; no parentheses.
W.T.dot(W)                              # Array method form of matrix dot product.
beta = np.linalg.inv(W.T.dot(W)).dot(np.dot(W.T, y))
predictions = X @ beta[1:] + beta[0]     # @ is matrix multiplication; preserve predictor order.
```

This is the lecture's manual OLS formula, `(W'W)^(-1)W'y`. It requires numeric data and an invertible `W'W` matrix; redundant predictors can make it fail. The `OrdinaryLeastSquares` class in the notebook is user-defined: create it with `(X, y)`, call `.fit()` to create `.beta`, `.coefficients`, and `.intercept`, then call `.predict(Xtest)`. Its `.fit()` returns `self`, allowing `OrdinaryLeastSquares(X, y).fit()` chaining. Those attributes do not exist before fitting.

The helper is named `compute_ols(X, y)` and returns the coefficient array with the intercept first. The custom class stores its training inputs as `.Xtrain` and `.ytrain` during initialization. In Lecture 10a, `fn_positive_error(error)` is a lambda returning `error >= 0`; passing a numeric Series produces elementwise Booleans, while `.apply(fn_positive_error)` calls it on each value.

## Lecture 11 — Dates, reshaping, plots, and panel models (11a–11e)

### Parse and format dates — 11a

```python
pd.to_datetime(s)                       # Convert date strings to datetime values.
pd.to_datetime(s, format="%B %d %Y")    # Parse a specified input format, e.g. October 15 2026.
pd.read_csv("folder/file.csv", parse_dates=["date"])  # Parse a date column while reading.
s.dt.strftime("%Y-%m")                 # Datetime Series → formatted strings.
s.dt.strftime("This is the month of %B") # Mix date directives with literal text.
```

The `.dt` accessor requires datetime-like values. Parsing turns strings into dates; `strftime` turns dates into strings. Format directives are case-sensitive.

| Directive | Meaning |
| --- | --- |
| `%Y`, `%y` | Four-digit year, two-digit year. |
| `%m`, `%B` | Zero-padded month number, full month name. |
| `%d`, `%A` | Zero-padded day of month, full weekday name. |
| `%W` | Monday-based week number, 00–53; days before the first Monday are week 00. |
| `%b`, `%a` | Abbreviated month and weekday names (e.g. Oct, Thu). |
| `%H`, `%I` | Hour on a 24-hour clock (00–23) or 12-hour clock (01–12). |
| `%M`, `%S` | Minute and second; `%M` is not the month directive. |

The lecture's formatting figures also show abbreviated names and clock fields. Match punctuation literally: `format="%b-%d, %y"` parses `"Apr-04, 18"`, and `s.dt.strftime("%A, %B %d, %Y")` creates strings such as `"Thursday, October 15, 2026"`. A 12-hour clock needs AM/PM to distinguish morning and evening; `%p` is the AM/PM directive. The further-reading note mentions microseconds (`%f`) and time zones (`%z` for numeric UTC offset, `%Z` for a zone name); these are supplemental details, not worked lecture examples.

### Group by time, calculate lags, and subset — 11a–11b

```python
pd.Grouper(key="date", freq="ME")      # Group a datetime column into month-end periods.
df.groupby(pd.Grouper(key="date", freq="ME")).agg(
    value_mean=("value", "mean")
).reset_index()                         # Return grouped date index to a regular column.
df.reset_index()                        # Move index levels into columns; create a default index.
df.set_index("date")                   # Use a column as the index; assign result to retain it.
s.diff()                                # Current value minus previous row; first is missing.
s.shift(1)                              # Previous row's value aligned with the current row.
growth = 100 * s.diff() / s.shift(1)     # Percent change; zero denominators need attention.
elapsed = df["date"] - df["date"].shift(1)
elapsed.dt.days                         # Whole days in each time difference.
df["date"].dt.month                    # Calendar month number from datetime values.
df["date"].dt.year                     # Calendar year from datetime values.
s.between(lower, upper)                 # Boolean mask; both endpoints included by default.
df.query('date.between("2020-03-01", "2020-05-01")')
df.query('date <= "2019-01-01"')
max(s)                                  # Built-in maximum, used on dates in the lecture.
```

Sort by date before drawing lines or computing differences/lags. `shift(1)` refers to the previous row, which may be several calendar days earlier. `elapsed.dt.days` belongs to timedelta data; it is not a calendar month/year extractor.

Use `"ME"` for month-end, `"YE"` for year-end, `"W"` for weekly, and `"D"` for daily grouping in current pandas. Lecture 11a's `freq='y'` groups annually even though its variable and chart labels say monthly. Older pandas versions use `"M"`/`"Y"` for month/year ends; the reference uses the explicit modern aliases shown in the [pandas time-grouping documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html).

### Reshape between wide and long — 11b

```python
long = pd.melt(
    df, id_vars="date", value_vars=["sp500", "djia"],
    var_name="portfolio_type", value_name="portfolio_value"
)                                      # Separate portfolio columns → type/value rows.
wide = pd.pivot(
    long, index="date", columns="portfolio_type", values="portfolio_value"
)                                      # Type/value rows → separate portfolio columns.
```

`id_vars` identifies columns to retain while stacking the selected value columns. `pivot` requires each index/column combination to be unique; it does not aggregate duplicates. Use `.reset_index()` afterward if the date should be a column again.

### Lines, shading, and plot configuration — 10a and 11b–11d

```python
plt.plot(x, y, color="green")            # Line plot; connects points in supplied order.
plt.plot("date", "value", data=df)      # Look up x/y columns by name.
plt.fill_between(x=dates, y1=lower, y2=upper, where=mask, alpha=0.2, color="red")
# Shade between lower/upper curves or constants where the mask selects intervals.

ax.plot(x, y, linewidth=1, color="steelblue", label="Series")
ax.scatter(x=x, y=y)                    # Scatter plot on one Axes; Lecture 11c exercise hint.
ax.plot(df.set_index("date"))           # One line per numeric data column, using the index as x.
ax.legend()                             # Use labels given to plotted series.
ax.legend(["Series 1", "Series 2"])    # Explicit labels in plotted-series order.
ax.set_xlabel("Date", fontsize=8, color="purple", labelpad=40)
ax.set_ylabel("Growth", fontsize=20, color="pink", labelpad=5)
ax.set_title("Title", fontsize=14)
ax.tick_params(axis="both", labelsize=10)
ax.xaxis.set_tick_params(labelsize=10, rotation=-90, colors="red")
ax.yaxis.set_tick_params(labelsize=12, rotation=0, colors="blue")
ax.grid(True)                           # Show grid; False hides it.
ax.set_ylim(lower, upper)               # Set y-axis limits; reversed limits invert the axis.
fig.tight_layout()                      # Figure method version of plt.tight_layout().
```

Lecture 11d's `PlotStyle` is a user-defined class that stores `color`, `tick_size`, `title_size`, and `grid=True`. Its `.plot(ax, x, y, title, label)` method applies those saved preferences using the methods above. Create separate instances for different styles; the class must be defined before use.

### Date and numeric ticks — 11c

```python
mdates.MonthLocator(interval=12)         # Place a date tick every 12 months.
mdates.DayLocator()                      # Daily ticks; mentioned as an alternative.
mdates.YearLocator()                     # Annual ticks; mentioned as an alternative.
mdates.DateFormatter("%y-%m-%d")        # Display datetime ticks with a date format.
ticker.MaxNLocator(10)                   # Target at most 10 intervals; not exactly 10 ticks.
ticker.FormatStrFormatter("%.1f")       # Display numeric ticks with one decimal place.
# The lecture figure also shows "%.0f" (no decimals) and "%.2f" (two decimals).
ax.xaxis.set_major_locator(locator)      # Configure tick positions; yaxis works too.
ax.xaxis.set_major_formatter(formatter)  # Configure tick labels; yaxis works too.
```

Assign an appropriate locator/formatter object to each placeholder. Locators choose where ticks appear; formatters choose their text.

### Panel models — optional 11e

```python
panel = wage_panel.load()               # Load the package's example panel dataset.
wage_panel.DESCR                         # Dataset description; no parentheses.
s.astype("category")                   # Convert to a categorical dtype.
panel = panel.set_index(["nr", "year"]).sort_index()
# Two-level index: entity first, time second. sort_index orders index labels.

pooled = PooledOLS.from_formula("lwage ~ married + union", data=panel)
pooled_results = pooled.fit(cov_type="clustered", cluster_entity=True)

fixed = PanelOLS.from_formula(
    "lwage ~ married + union + EntityEffects + TimeEffects", data=panel
)
fixed_results = fixed.fit(cov_type="clustered", cluster_entity=True)

BetweenOLS.from_formula("lwage ~ exper + expersq + married + union", data=panel).fit()
RandomEffects.from_formula("lwage ~ exper + expersq + married + union", data=panel).fit()
FirstDifferenceOLS.from_formula("lwage ~ exper + expersq + married + union", data=panel).fit()
fixed_results.params                    # Estimated coefficient Series.
print(fixed_results.summary)            # Property here, unlike statsmodels' .summary().
```

Pooled OLS combines observations; between OLS uses entity averages; first differences use changes within entities. Random effects requires assumptions about the relationship between entity effects and regressors. `EntityEffects`/`TimeEffects` request fixed effects in `PanelOLS` formulas. Entity effects absorb time-invariant regressors. Entity-clustered covariance permits within-entity error dependence. Unlike statsmodels formulas, these linearmodels formulas need an explicit `1 +` if an intercept is wanted; first-difference models must not contain a constant.

## Lecture 12 — Logistic classification and Poisson regression (12a–12b)

### Build model matrices and estimate logistic regression — 12a

```python
y, X = patsy.dmatrices(
    "request_loan ~ 1 + received_info + owns_house + home_numrooms",
    df, return_type="dataframe"
)
y = np.ravel(y)                         # Flatten the response to a 1D array.

logit_results = smf.logit("request_loan ~ received_info + owns_house + home_numrooms",
                          data=df).fit(cov_type="HC1")
matrix_results = sm.Logit(y, X).fit(cov_type="HC1")
```

Patsy returns outcome and design matrices, expanding formula terms and dropping rows with missing model inputs by default. The `1` requests an intercept column. The matrix interface uses the supplied columns as-is, so include the intercept in `X`. A binary logistic outcome is coded 0/1. Use the Lecture 10 table methods for fitted statsmodels results.

```python
classifier = LogisticRegression(
    penalty=None, fit_intercept=False, solver="lbfgs",
    max_iter=1000, tol=1e-10
).fit(X, y)
classifier.coef_                        # Fitted coefficient array; trailing underscore.
classifier.coef_.ravel()                # Flatten coefficients for a binary model.
pd.Series(classifier.coef_.ravel(), index=X.columns)  # Attach predictor names.
```

This preserves the lecture's unpenalized sklearn specification. `fit_intercept=False` avoids adding a second intercept because Patsy already supplied one. `max_iter` is the iteration limit; `tol` controls convergence tolerance. Newer sklearn versions deprecate `penalty`; their unpenalized alternative uses `C=np.inf` in place of `penalty=None`. See [LogisticRegression parameters](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html). Full-sample coefficient comparison and held-out prediction evaluation are separate tasks.

### Split data, predict probabilities, and classify — 12a

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=42
)
# Fit the classifier on X_train, y_train before evaluating X_test.
classifier.fit(X_train, y_train)
probabilities = classifier.predict_proba(X_test)  # One column per class.
classifier.classes_                             # Class labels in probability-column order.
p1 = probabilities[:, 1]                        # P(class=1) when classes_ is [0, 1].
predicted_labels = pd.cut(
    p1, bins=[0, 0.2, 1], labels=[0, 1], right=True, include_lowest=True
)
```

`test_size=0.5` reserves half the observations for testing; `random_state` makes the split reproducible. Train on the training sample and evaluate on the test sample. With the lecture's threshold rule, probabilities at or below 0.2 become class 0 and those above become class 1. `include_lowest=True` also classifies exactly zero, which the notebook's default `pd.cut` call would leave missing. Keep outcome values aligned with design-matrix rows.

### Confusion matrix and annotations — 12a

```python
cm = confusion_matrix(y_test, predicted_labels, labels=[0, 1])
# Rows = actual class; columns = predicted class: [[TN, FP], [FN, TP]].
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(cm)
ax.grid(False)
ax.xaxis.set(ticks=(0, 1), ticklabels=("Predicted 0", "Predicted 1"))
ax.yaxis.set(ticks=(0, 1), ticklabels=("Actual 0", "Actual 1"))
ax.set_ylim(1.5, -0.5)
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i, j], ha="center", va="center")
```

`labels=[0, 1]` keeps a consistent 2×2 layout. `ax.text(x, y, text, ...)` places annotations at data coordinates; `ha` and `va` control horizontal and vertical alignment. Accuracy is `(TN + TP) / total`; changing the threshold changes the tradeoff between false positives and false negatives.

### Poisson regression — optional 12b

```python
y, X = patsy.dmatrices("wage ~ age + tenure", df, return_type="dataframe")
y = np.ravel(y)
poisson_results = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1")
poisson_results.summary()
mt.ETable([poisson_results]).make(type="gt")
poisson_results.predict(X_test)         # Predicted means; test matrix must match training columns.
```

`sm.GLM` specifies a generalized linear model. `sm.families.Poisson()` uses a log link by default, giving conditional mean `exp(X @ beta)`. Poisson is commonly used for nonnegative counts; the lecture's wage example uses the exponential mean specification with robust covariance. Skewness alone does not establish that this is an appropriate model. Reuse train/test splitting for the prediction exercise and compare mean squared errors using `np.mean((actual - predicted) ** 2)`.

## Lecture 13 — Regression trees, pruning, forests, and boosting (13a–13b)

### Dataset loading and input shapes

```python
ISLP.load_data("Boston")                 # Load the named ISLP dataset as a DataFrame.
load_data("Smarket")                    # Same function after `from ISLP import load_data` (14b).
X_train = training_df.drop(columns=["outcome"])
X_test = testing_df.drop(columns=["outcome"])
y_train = training_df["outcome"]         # Single brackets give a 1D Series.
y_test = testing_df["outcome"]
X_train.shape[1]                         # Number of predictor columns; shape[0] counts rows.
```

The lecture's `df[["shares"]]` creates a two-dimensional one-column DataFrame. For a single outcome, use `df["shares"]` or `np.ravel(y)` to get a 1D target. Training/test predictors must have the same columns in the same order; exclude the outcome from the predictors. The Boston exercise uses `crim` as its outcome.

### Train, predict, and evaluate a regression tree — 13a

```python
tree_model = DTR(max_depth=3, random_state=0)
tree_model.fit(X_train, y_train)          # Learn splits and leaf predictions; returns this estimator.
y_pred = tree_model.predict(X_test)      # Numeric predictions, one per test row for a single outcome.
mse = np.mean((np.ravel(y_test) - np.ravel(y_pred)) ** 2)
```

`DTR` aliases `DecisionTreeRegressor`. `max_depth` limits tree depth, not the total number of branches or leaves. `random_state` makes randomized aspects of fitting, including tie-breaking, reproducible. The default regression criterion is squared error. Fit before prediction; lower held-out MSE is better.

**Shape correction:** subtracting an `(n, 1)` target array from `(n,)` predictions broadcasts to an `(n, n)` array. That averages errors between different observations and can silently give the wrong MSE. Flatten both single-outcome arrays and ensure they have equal lengths and matching row order before subtracting.

### Visualize the fitted tree — 13a

```python
dot_text = tree.export_graphviz(
    decision_tree=tree_model,
    feature_names=X_train.columns.values,
    filled=True
)
graphviz.Source(dot_text)                # Wrap DOT source for notebook rendering.
```

`export_graphviz` returns a DOT-format string when no output file is specified. `feature_names` supplies one label per predictor in training-column order. `filled=True` colors nodes; the pruned-tree example omits it. `graphviz.Source` is a constructor, not a tree estimator. Notebook rendering also needs the Graphviz executable `dot` available on PATH; installing the Python package alone may not provide it. The lecture suggests `conda install python-graphviz` if needed. See the [Graphviz installation guide](https://graphviz.readthedocs.io/en/stable/manual.html).

### Cost-complexity pruning and grid search — 13a

```python
ccp_path = tree_model.cost_complexity_pruning_path(X_train, y_train)
ccp_path.ccp_alphas                      # Candidate nonnegative pruning strengths; attribute.
kfold = skm.KFold(5, shuffle=True, random_state=10)
grid = skm.GridSearchCV(
    tree_model,
    {"ccp_alpha": ccp_path.ccp_alphas},
    refit=True,
    cv=kfold,
    scoring="neg_mean_squared_error"
)
G = grid.fit(X_train, y_train)            # Fit candidates across folds; returns the search object.
pruned_tree = grid.best_estimator_       # Best model refitted on all data supplied to grid.fit.
pruned_predictions = pruned_tree.predict(X_test)
```

`cost_complexity_pruning_path` computes candidate subtrees for the estimator's settings; it does not modify the fitted tree into the selected pruned model. Larger `ccp_alpha` generally means more pruning. The parameter grid is a dictionary with exact estimator parameter names as string keys and collections of candidate values. `cv` supplies the fold scheme; `refit=True` fits the winner on the full search-training data. `best_estimator_` is available after fitting, with a trailing underscore and no parentheses.

`GridSearchCV` chooses the highest score. Negative MSE therefore makes a smaller error score better: −10 beats −100. `skm.GridSearchCV` and a directly imported `GridSearchCV` are the same class. See [decision-tree pruning](https://scikit-learn.org/1.7/modules/generated/sklearn.tree.DecisionTreeRegressor.html). Keep the final test data out of pruning selection.

### Bagging and random forests — 13b

```python
bagged_model = RF(max_features=X_train.shape[1], random_state=0)
bagged_model.fit(X_train, np.ravel(y_train))

rf_model = RF(random_state=0)             # The notebook's second specification.
rf_model.fit(X_train, np.ravel(y_train))
rf_predictions = rf_model.predict(X_test)
```

`RF` aliases `RandomForestRegressor`; predictions average the fitted trees. With its default `bootstrap=True`, each tree fits a sample drawn with replacement. `max_features` controls candidate features **at each split**, not a permanent set of discarded columns. An integer specifies a count; a fraction such as `0.5` selects roughly half the features; `"sqrt"` selects about the square root of the feature count.

**Default clarification:** current `RF()` uses `max_features=1.0`, meaning all features. Thus the two notebook specifications both use all predictors at each split; the second does not automatically introduce feature subsampling. For an explicit feature-subsampling comparison, use a setting such as `RF(max_features="sqrt", random_state=0)`. See [RandomForestRegressor parameters](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html?highlight=randomforest).

### Gradient boosting — 13b

```python
boost_model = GBR(
    n_estimators=5000, learning_rate=0.2, max_depth=3, random_state=0
)
boost_model.fit(X_train, np.ravel(y_train))
y_hat_boost = boost_model.predict(X_test)
boost_mse = np.mean((np.ravel(y_test) - np.ravel(y_hat_boost)) ** 2)
```

`GBR` aliases `GradientBoostingRegressor`. `n_estimators` is the number of boosting stages, `learning_rate` scales each added tree's contribution, and `max_depth` limits each individual tree. Boosting adds trees sequentially to improve the current predictions, unlike averaging independently fitted bootstrap trees. Tune learning rate and stage count together. The notebook uses 5,000 stages; that can take time. The trailing semicolon after `.predict(...)` in the notebook is optional Python syntax, not part of the method.

## Lecture 14 — Cross-validation and expanding windows (14a–14b)

### K-fold splitting and cross-validation — 14a

```python
cv = KFold(n_splits=5, shuffle=True, random_state=0)
cv_results = cross_validate(tree_model, X_estimate, np.ravel(y_estimate), cv=cv)
np.mean(cv_results["test_score"])        # Average held-out R² for a standard regression tree.
```

`KFold` splits observations into `n_splits` folds; each is held out once while the other folds train the model. The split count must be at least 2 and no greater than the number of observations. `shuffle=True` randomizes row allocation before splitting; `random_state` fixes that shuffle. `skm.KFold(5, ...)` uses the same class, with a positional split count.

`cross_validate` clones and fits the estimator separately in each fold, so it does not require the preliminary `.fit()` shown in the notebook. It returns a dictionary of arrays, including `"test_score"`, `"fit_time"`, and `"score_time"`. Here “test” means the held-out fold within the supplied data, not the separate external dataset. This call does not refit the supplied estimator on the full dataset.

**Choose the metric explicitly when comparing errors:** without `scoring`, `cross_validate` uses the estimator's `.score()`; for `DTR` that is R², not MSE. For MSE:

```python
cv_results = cross_validate(
    tree_model, X_estimate, np.ravel(y_estimate), cv=cv,
    scoring="neg_mean_squared_error"
)
cv_mse = -np.mean(cv_results["test_score"])  # Negate once to obtain positive MSE.
```

R² is higher-is-better and can be negative; MSE is lower-is-better. Use training folds to compare settings, refit the selected model on the estimation data, then evaluate on the untouched validation/test data. See [cross_validate](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html).

### Commented-out leave-one-out example and statsmodels adapter — 14a

```python
M = sklearn_sm(sm.OLS)                   # Adapt a statsmodels model class to sklearn's interface.
X = sm.add_constant(np.array(X_estimate)) # Add an intercept column; default prepends it.
Y = np.ravel(y_estimate)
cv_results = cross_validate(
    M, X, Y, cv=X_estimate.shape[0], scoring="neg_mean_squared_error"
)
loo_mse = -np.mean(cv_results["test_score"])

ols_results = sm.OLS(Y, X).fit()          # Direct matrix-interface OLS; outcome comes first.
```

`sm.OLS` is a model class, passed **without parentheses** to `sklearn_sm`; the adapter provides fitting and prediction for cross-validation. `sm.add_constant` supplies the intercept that matrix-based `sm.OLS` does not add automatically. By default it skips adding another column if it detects an existing nonzero constant column. `cv=n` gives leave-one-out folds for this regression example and fits n models; it can be slow.

The notebook's commented variable `X_estiamte` is a typo for `X_estimate`. Its `sklearn_sm` example omits `scoring`; the installed ISLP adapter uses positive MSE for OLS, unlike a sklearn tree's default R². Adapter behavior can vary by version, so the explicit negative-MSE scorer above fixes the meaning. Flatten Y to avoid the same broadcasting issue as Lecture 13. R² is not defined for a one-observation held-out fold. The adapter comes from [ISLP's sklearn wrappers](https://intro-stat-learning.github.io/ISLP/api/generated/ISLP.models.sklearn_wrap.html).

### Time ordering, row numbers, and expanding windows — 14b

```python
Smarket = load_data("Smarket")
Smarket.plot(y="Volume")                # Plot the selected column against the DataFrame index.
Smarket["obs_num"] = np.arange(1, len(Smarket) + 1)
split = len(Smarket) // 2                # Integer floor division: initial half-sample size.
training = Smarket.query("obs_num <= @split")
testing = Smarket.query("obs_num > @split")
```

`np.arange(start, stop, step)` returns evenly spaced values with stop excluded; step defaults to 1, so `np.arange(1, n + 1)` gives row numbers 1 through n. The row-number column is an identifier, not automatically a predictor. The lecture assumes the data are already in chronological order.

For the exercise, choose a numeric outcome and predictors available at prediction time; define `features` explicitly. `DTR` must be imported in this notebook, and `.fit()` needs both X and y. The current exercise cell has a bare `features` expression and empty `.fit()` calls, so it is an unfinished template. Supplemental syntax for one-step-ahead evaluation:

```python
X = ordered_df[feature_names]
y = ordered_df[outcome_name]             # One numeric outcome; exclude it from feature_names.
start = len(ordered_df) // 2
errors = []
for stop in range(start, min(start + 12, len(ordered_df))):
    model = DTR(max_depth=3, random_state=0)
    model.fit(X.iloc[:stop], y.iloc[:stop])
    prediction = model.predict(X.iloc[stop:stop + 1])
    errors.append((y.iloc[stop] - prediction[0]) ** 2)
expanding_mse = np.mean(errors)
```

The initial window needs at least one training row and one later test row. This example implements the first fit, the half-plus-one fit, and up to ten further fits, using only earlier observations to predict the next one. The lecture leaves the evaluation horizon open; choose it consistently if predicting several future rows instead. Do not randomly shuffle time-series rows or use future outcomes in predictors. String labels such as `Direction` need a classification workflow rather than regression MSE.

### Imported-only helpers — 14a–14b

These imports have no worked calls in the notebooks. The syntax below is supplemental, so their presence in an import block is not mistaken for a completed example.

```python
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn import preprocessing

ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
# Repeated random train/test splits; test sets can overlap between repetitions.
scores = cross_val_score(model, X, y, cv=cv, scoring="neg_mean_squared_error")
# Return just the score array; cross_validate also returns timings.
svm = SVC()                             # Support-vector classifier, not a regression tree.
svm.fit(X_train, y_train)                # Use categorical class labels as the target here.
labels = svm.predict(X_test)
ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1]).plot()
# Display a precomputed confusion matrix; label order must match its rows/columns.
summarize(ols_results)                  # ISLP coefficient table from fitted statsmodels results.
```

`GridSearchCV` is the same search class documented in Lecture 13. `preprocessing` is a module for feature transformations, not a callable; no particular preprocessing function is named or used in the lecture. Any learned preprocessing must be fitted on training data only. `summarize` returns coefficient estimates, standard errors, test statistics, and p-values; see the [ISLP regression example](https://intro-stat-learning.github.io/ISLP/labs/Ch03-linreg-lab.html). Other repeated imports—`LogisticRegression`, `classification_report`, `confusion_matrix`, `train_test_split`, and `patsy`—are covered in Lectures 12 and the imported-only section below.

## Lecture 15 — Scaling, SVM classification, metrics, and tuning

### Retrieve UCI data and prepare inputs

```python
online_shopping = fetch_ucirepo(id=468)   # Fetch the named dataset by its numeric UCI ID; needs network access.
X = online_shopping.data.features        # Feature DataFrame; attributes have no parentheses.
X = X.drop(columns=["Month", "VisitorType"])
y = online_shopping.data.targets["Revenue"]  # Select one outcome as a Series.
dataset_names = pd.DataFrame(X.columns)  # Column names as a one-column table.
table_y = pd.crosstab(y, "Purchased ?") / len(y)  # Outcome counts divided by total row count.
display(table_y)
display(X.describe())
X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=104, test_size=0.25, shuffle=True
)
```

`fetch_ucirepo` returns a dataset object; `.data.features` and `.data.targets` hold its predictors and outcomes. The lecture removes two string columns to leave features suitable for the numeric estimator. `test_size=0.25` reserves a quarter of the rows; `shuffle=True` randomizes the split and `random_state` makes it reproducible. The proportional crosstab excludes missing labels from its counts but divides by all rows, so it sums to one only when y has no missing values. Source: [UCI's Python package](https://github.com/uci-ml-repo/ucimlrepo/blob/main/README.md?plain=1).

### Standardize features with the training scaler

```python
scaler = preprocessing.StandardScaler() # Create a transformer; default centers and scales each feature.
scaler.fit(X_train)                     # Learn feature means/variances from training rows; returns self.
X_train_scale = scaler.transform(X_train)
X_test_scale = scaler.transform(X_test)  # Reuse exactly the same learned transformation.
```

`StandardScaler` applies `(x - training_mean) / training_standard_deviation` column by column and normally returns a NumPy array. Nonconstant training features have mean zero and unit variance after scaling; test features need not. Keep columns in the same order. `scaler.transform` applies learned values without fitting again; this is a different method from pandas `groupby(...).transform(...)` in Lecture 3.

**Correction to the notebook:** do not fit `scaler_test` on `X_test`. That gives test rows a different coordinate system and uses information from the evaluation data. Fit on training rows only and transform both sets with that scaler. For cross-validation, learn the scaler inside each fold, as shown below. See [scikit-learn's preprocessing guidance](https://scikit-learn.org/stable/common_pitfalls) and [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html?highlight=standardscaler).

### Fit and score an SVM classifier

```python
svm = SVC()                             # Support-vector classifier; default RBF kernel and C=1.
svm.fit(X_train_scale, y_train)          # Fit on scaled features and class labels; returns self.
predictions = svm.predict(X_test_scale) # Predicted class labels, not probabilities.
svm.classes_                           # Class labels in estimator order; trailing underscore.
accuracy = svm.score(X_test_scale, y_test)  # Fraction correctly classified; higher is better.
candidate = SVC(gamma=0.1, C=1)         # Separate unfitted model with explicit tuning parameters.
```

`C` must be positive: larger C penalizes training errors more strongly (weaker regularization). For the RBF kernel, a larger positive `gamma` makes each observation's influence more local. The default is `gamma="scale"`, calculated as `1 / (n_features * X.var())`; `gamma="auto"` uses `1 / n_features`. The notebook's default-gamma statement omits the variance factor. Scaling can make these values similar, but they are not universally identical. See [SVC parameters](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html).

Always pass data in the representation used during fitting: an SVC fitted on `X_train_scale` must receive `X_test_scale` in `.predict()` and `.score()`. The notebook's later calls on raw `X_test` do not follow that rule. Unlike regression-tree `.score()` (R²), SVC `.score()` reports classification accuracy.

### Confusion-matrix proportions and display

```python
cm = confusion_matrix(y_test, predictions, labels=svm.classes_) / len(y_test)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=svm.classes_)
disp.plot()                             # Draw the display; returns the display object.
plt.show()
```

Rows are actual labels and columns are predictions, both ordered by `svm.classes_`. Dividing the entire matrix by `len(y_test)` gives proportions of **all test observations**; it is not normalization separately within each actual class. The diagonal sum equals overall accuracy when every label is included. `ConfusionMatrixDisplay` accepts the precomputed matrix and matching labels; `.plot()` renders it.

### Discover scorers and evaluate multiple metrics

```python
get_scorer_names()                       # List of valid named scorers available in installed sklearn.
list_scorers = pd.DataFrame(get_scorer_names())
```

The lecture calls `cross_validate(SVC(), X_train_scale, y_train, scoring=["accuracy", "roc_auc", "recall_macro"], return_train_score=False, cv=5)`. This requests five-fold scores for three metrics. For a binary classifier with integer `cv`, sklearn uses stratified folds, without shuffling by default. Each class needs enough observations for the chosen number of folds.

| Scorer | Meaning and required prediction type |
| --- | --- |
| `"accuracy"` | Fraction of predicted class labels that are correct. |
| `"roc_auc"` | Binary ranking performance across thresholds; uses decision scores or probabilities, not hard labels. SVC provides decision scores, so probability estimation is not required for this scorer. |
| `"recall_macro"` | Recall computed for each class, then averaged with equal class weights, regardless of class sizes. |

All three are higher-is-better. With multiple named metrics, result keys are `"test_accuracy"`, `"test_roc_auc"`, and `"test_recall_macro"` rather than just `"test_score"`. `return_train_score=False` omits training-fold scores. `pd.DataFrame(res)` shows one row per fold; `.mean()` averages numeric columns, including `fit_time` and `score_time`, which are seconds, not performance measures.

**Supplemental correction for scaling within CV:** a pipeline ensures each fold learns its own scaler using only that fold's training rows. `Pipeline` is added here to make the lecture workflow correct; it is not a lecture import.

```python
from sklearn.pipeline import Pipeline
svm_pipeline = Pipeline([
    ("scale", preprocessing.StandardScaler()),
    ("svm", SVC())
])
res = cross_validate(
    svm_pipeline, X_train, y_train,
    scoring=["accuracy", "roc_auc", "recall_macro"],
    return_train_score=False, cv=5
)
display(pd.DataFrame(res))
pd.DataFrame(res).mean()
```

Pass raw features to this pipeline; it scales them internally. Scaling the entire training dataset before splitting into CV folds lets held-out folds influence preprocessing. `cross_val_score`, also imported but not called in Lecture 15, returns a single scorer's array rather than this multi-metric result dictionary; see Lecture 14.

### Manual tuning, dictionaries, and string formatting

```python
k_features = X.shape[1]                 # Number of predictor columns.
best_score = -np.inf                    # Supplemental safeguard: allow the first candidate to win.
for gamma in [0.1 / k_features, 1 / k_features]:
    for C in [0.1, 1]:
        candidate = SVC(gamma=gamma, C=C)
        candidate.fit(X_train_scale, y_train)
        score = candidate.score(X_valid_scale, y_valid)
        if score > best_score:
            best_score = score
            best_parameters = {"C": C, "gamma": gamma}
svm = SVC(**best_parameters)            # Unpack dictionary keys into keyword arguments.
svm.fit(X_train_scale, y_train)
print("Parameter grid:\n{}".format(best_parameters))
```

`X_valid_scale` is a validation set transformed by the training scaler, with aligned labels `y_valid`; these are placeholders for a separate tuning split. Nested loops try every C/gamma pair. `**best_parameters` is equivalent to writing `C=..., gamma=...` explicitly, not exponentiation in this call context. String `.format(value)` substitutes into `{}`; `\n` inserts a newline. This string method is distinct from pandas Styler `.format(...)`.

The notebook initializes `best_score=0`; if every score is zero, its strict `>` test never defines `best_parameters`. It also tunes repeatedly on the named test set, which then acts as validation data and is no longer an untouched final test. Its heading says “all data,” but `.fit(X_train_scale, y_train)` fits only that training subset. Prefer CV on the training set for parameter selection and reserve test data for final evaluation.

### Grid search options and the forest exercise

```python
param_grid = {
    "C": [0.01, 0.1],
    "gamma": [0.01 / k_features, 0.1 / k_features]
}
grid_search = GridSearchCV(
    SVC(), param_grid, cv=2, return_train_score=True, n_jobs=-1
)
# Constructor matches the lecture. Use a pipeline below to include scaling within folds.
```

The grid defines four parameter combinations, with exact SVC parameter names as keys. `cv=2` uses two stratified folds for this classifier; increasing it uses a larger training fraction per fit but requires more fits. `return_train_score=True` includes training scores in `cv_results_`; `n_jobs=-1` requests all available processors. Without explicit `scoring`, the search maximizes SVC's accuracy. Default `refit=True` fits the best setting on all rows supplied to the search's `.fit()`.

```python
pipeline_grid = {
    "svm__C": param_grid["C"],
    "svm__gamma": param_grid["gamma"]
}
grid_search = GridSearchCV(
    svm_pipeline, pipeline_grid, cv=2, return_train_score=True, n_jobs=-1
)
grid_search.fit(X_train, y_train)
grid_search.best_params_                # Selected parameter dictionary; supplemental inspection.
grid_search.best_estimator_             # Refitted pipeline, including the scaler.
pd.DataFrame(grid_search.cv_results_)   # Per-candidate scores, timings, parameters, and ranks.
predictions = grid_search.predict(X_test)  # Raw test features; pipeline applies its fitted scaler.
```

Pipeline parameters use `step_name__parameter`, with **two underscores**; here the classifier step was named `"svm"`. The final exercise asks for a **random forest classifier** grid, not the regression estimator `RF` from Lecture 13. The required import and syntax are:

```python
from sklearn.ensemble import RandomForestClassifier
forest_search = GridSearchCV(
    RandomForestClassifier(random_state=0),
    {"n_estimators": [10, 50]}, cv=2, return_train_score=True, n_jobs=-1
)
forest_search.fit(X_train, y_train)
```

`n_estimators` counts trees in each forest, not the number of forests. Classification uses class labels; the fitted classifier supports `.predict(X_test)`, `.score(X_test, y_test)` for accuracy, and `.classes_`. This example supplies syntax for the exercise; the notebook's exercise cell is blank.

## Imported-only helpers — uses and syntax

These objects appear in lecture imports or supporting scripts but have no worked calls there. The examples below explain their purpose and are supplemental reference syntax, not additional lecture exercises. Import the relevant names before using them.

### HTML display, time utilities, and browser waits — Lectures 5–6

```python
display(HTML("<b>Hello</b>"))             # Render an HTML string inside a notebook.
import time as time_module              # Alias avoids collision with datetime.time.
time_module.sleep(1)                    # Pause execution for one second.
```

`html5lib` is an HTML parser imported by the Lecture 6 script. It can be selected as `BeautifulSoup(html_text, "html5lib")` when installed; the worked lecture calls use `"html.parser"` instead.

```python
wait = WebDriverWait(driver, 10)         # Explicit wait, with a timeout in seconds.
element = wait.until(EC.presence_of_element_located((By.XPATH, "//header")))
```

`By.XPATH` is a locator constant equivalent to the strategy string `"xpath"`. `EC` aliases the expected-conditions module; the example condition waits for presence in the document, not necessarily visibility. `WebDriverWait` performs explicit polling, not an implicit wait. `Command` contains low-level WebDriver command constants; it is not a browser-health function and the lecture does not use it. See [Selenium's expected-condition example](https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html?highlight=presence_of_all_elements_located).

### Python date/time constructors — Lecture 11a

```python
from datetime import date, time, datetime
date(2026, 10, 15)                      # Calendar date: year, month, day.
time(14, 30, 0)                         # Time of day: hour, minute, second.
datetime(2026, 10, 15, 14, 30, 0)       # Combined date/time; no timezone supplied here.
```

These create individual Python objects; `pd.to_datetime` handles the lecture's date columns. Calendar fields must form valid dates/times. `time(...)` here is a constructor, unlike the separate `time` module imported in Lecture 6.

### Extra model and reporting imports — Lectures 11e and 12

```python
from linearmodels.datasets import mroz
from linearmodels.iv import IV2SLS
from sklearn.metrics import classification_report
from statsmodels.iolib.summary2 import summary_col

mroz.load()                             # Load the package's labor-supply example DataFrame.
iv_model = IV2SLS(y, exog, endog, instruments)
iv_results = iv_model.fit()             # Instrumental-variable two-stage least squares.
# y: outcome; exog: exogenous regressors; endog: endogenous regressors;
# instruments: excluded instruments. Include a constant in exog if wanted.

classification_report(y_test, predicted_labels)  # Text report: precision, recall, F1, support.
summary_col([results1, results2], model_names=["Model 1", "Model 2"],
            float_format="%.3f", stars=True)    # Side-by-side statsmodels regression summary.
```

`classification_report` consumes class labels, not raw probabilities; print the returned string for readable output. `summary_col` is an alternative reporting helper; the worked Lecture 10–12 tables use `mt.ETable`. `IV2SLS` is imported but no IV model is estimated in Lecture 11e. Parameter details: [IV2SLS](https://bashtage.github.io/linearmodels/iv/iv/linearmodels.iv.model.IV2SLS.html), [summary_col](https://www.statsmodels.org/0.9.0/_modules/statsmodels/iolib/summary2.html).

## Reading lecture syntax and correcting typos

| If you see this in a lecture | Use / interpretation |
| --- | --- |
| `jmes.search(...)` in the Lecture 5b exercise | `jmespath.search(expression, obj)` matches the actual import. |
| `.find_elments(...)` or `.findelements(...)` | `.find_elements("xpath", path)` returns a list. |
| `.text()` on a Selenium element | `.text` is an attribute; omit parentheses. |
| `plt.imgshow(...)` in a word-cloud comment | `plt.imshow(...)` is the actual image-display function. |
| `fit(cov="HC1")` in Lecture 10a | `fit(cov_type="HC1")` requests the intended robust covariance. |
| `dt.months` in a time-data comment | Use `.dt.month` on datetimes; `.dt.days` is for timedeltas. Calendar months have varying lengths. |
| `ascending=TRUE` in a hint | Python spells the Boolean `True`, with only the first letter capitalized. |
| `fn_cubic`, `bubble_sort`, or `fn_grade` | See the exact custom-function table: the current code's behavior does not always match the name or exercise request. |
| `freq='y'` with a monthly chart label | The grouping is yearly; use the intended month/year frequency explicitly. |
| `np.mean(...)` described as a median | Mean and median differ; use `np.median(...)` for the median. |
| `class`, `role`, `id`, or `value` in HTML | These are attributes of elements, not HTML tag names or Python functions. |

The receiver matters: `requests.get(url)` makes an HTTP request, `driver.get(url)` navigates a browser, and `mapping.get(key)` reads a dictionary. Likewise, `.fit()`, `.predict()`, `.plot()`, and `.summary` have object-specific meanings. Use the example for the object's library or custom class rather than assuming every method with the same name accepts the same inputs.
