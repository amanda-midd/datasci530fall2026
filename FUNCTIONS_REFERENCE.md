# Function reference — Lectures 1–7

Covers the local lecture notebooks, exercises, and imported scripts through Lecture 6 reviewed September 22, 2026; Lecture 7a–7c added September 27, 2026. Repeated functions appear once. This file is a reference snapshot; pulling new lectures does not automatically update it.

**Reading the syntax:** `df` = DataFrame; `s` = one column (Series); `a` = array; other unquoted names are placeholders to replace with your variables. Quoted text is a string; replace placeholder column names and paths inside the quotes. Entries show the inputs and options taught, not every option available in the library. Code blocks are syntax templates, not a script to run top to bottom.

## Packages and imports

Run installation commands in the terminal, in your course environment. `json` and `time` are built into Python.

```sh
pip install numpy pandas matplotlib requests jmespath ipython beautifulsoup4 html5lib selenium webdriver-manager
# Alternative installation syntax from the lectures:
conda install package_name
conda install conda-forge::html5lib
conda install conda-forge::selenium
conda install conda-forge::webdriver-manager
```

```python
import numpy as np                         # Arrays, mathematics, random numbers.
import pandas as pd                        # Tables and data manipulation.
import matplotlib.pyplot as plt            # Charts.
import requests                            # HTTP/API requests.
import json                                # JSON encoding and decoding.
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

## Lecture 1 — Python basics, files, and NumPy

### Built-ins and basic formatting

```python
print(value)                  # Print a value; print(value1, value2) prints several.
type(value)                   # Return its type: int, float, str, list, etc.
str(value)                    # Convert to a string.
list(iterable)                # Convert an iterable to a list.
len(obj)                      # Number of items; for a DataFrame, number of rows.
display(obj)                  # Rich notebook display, including tables.

name = value                  # Assign a value; names are unquoted.
"text"                        # Strings use matching single or double quotes.
True                          # Boolean literals are True and False, unquoted.
[value1, value2]               # List: square brackets, comma-separated values.
{"key1": value1, "key2": value2}  # Dictionary: key:value pairs in braces.
items[i]                      # List/array index: first item is 0.
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
```

### API requests and JSON

```python
requests.get(url)                       # HTTP GET; url is a complete URL string.
response.json()                         # Decode response JSON into Python objects.
requests.get(url).json()                # Request and decode in one chain.
json.dumps(obj, indent=4)               # Python dict/list → JSON string; indent is optional.
json.loads(json_text)                   # JSON string → Python dict/list/scalar.
mapping.keys()                         # View dictionary keys, not nested keys.
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

### HTML syntax taught alongside the functions

`%%html` must be the first line of a Jupyter code cell; put raw HTML on subsequent lines.

| Syntax | Purpose / required formatting |
| --- | --- |
| `<tag>content</tag>` | Container; matching opening/closing tags. |
| `<html>…</html>`, `<head>…</head>`, `<body>…</body>` | Document, metadata section, visible content. |
| `<title>text</title>` | Document title inside head. |
| `<meta name="name" content="value">` | Metadata; no closing tag. |
| `<div class="class_name">…</div>` | Section with a CSS class. |
| `<p>text</p>`, `<h1>text</h1>`, `<br>` | Paragraph, heading, line break. |
| `<!-- comment -->` | HTML comment. |
| `<style>.class_name { property: value; }</style>` | CSS class rule; leading dot, braces, colon, semicolon. |
| `<form>…</form>` | Form container. |
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
