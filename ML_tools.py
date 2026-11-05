"""MACHINE LEARNING — CLASS LECTURE NOTES (Lectures 10–17)

A Python-format reference, not a library of new helper functions.
These are the class calls, examples, concepts, and formatting from the existing
functions reference. No new functions or classes are defined here.

READING / USING THIS FILE
Use the # %% cells separately in VS Code, or copy the example you need into your
notebook. Do NOT import or run this whole file top to bottom: different examples
reuse variables for different datasets. Replace placeholder paths/column names
and prepare the X/y or DataFrame inputs described in each section.

ORDER
1. Linear regression and formula syntax (including tables and manual OLS)
2. Regression trees, pruning, bagging, forests, and boosting
3. Cross-validation and expanding windows
4. Logistic classification and Poisson regression
5. Scaling, SVM classification, metrics, and tuning
6. Neural networks
7. PCA and K-means
8. Optional panel regression

Regression is included because it provides continuous-outcome models and useful
baselines. Logistic regression predicts classes; Poisson models a conditional
mean often used for counts. PCA and clustering use X without known outcomes.

Comments marked correction/supplemental distinguish fixes or exercise syntax
from literal lecture code. Imported-only APIs are identified as such. New
helper wrappers and the supplemental Pipeline implementations are omitted.
FUNCTIONS_REFERENCE.md is unchanged and remains the full course-wide catalog.
"""

# %% COMMON IMPORTS — run only those needed for your chosen example
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import patsy
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score
from sklearn.model_selection import GridSearchCV, KFold
import sklearn.model_selection as skm
from sklearn.tree import DecisionTreeRegressor as DTR
from sklearn.ensemble import RandomForestRegressor as RF
from sklearn.ensemble import GradientBoostingRegressor as GBR
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, get_scorer_names
from sklearn import preprocessing, tree
from IPython.display import display

# Optional lecture packages; uncomment the ones used by your chosen section.
# import maketables as mt
# import graphviz
# import ISLP
# from ISLP import load_data
# from ISLP.models import sklearn_sm
# from ucimlrepo import fetch_ucirepo
# from linearmodels.datasets import wage_panel
# from linearmodels.panel import (PooledOLS, PanelOLS, BetweenOLS,
#                                RandomEffects, FirstDifferenceOLS)
# Neural-network/PCA/FAISS imports appear in their own sections below.

# Data prerequisites: select explicit predictors and exclude the target.
# X_train = training_df.drop(columns=["outcome"])
# y_train = training_df["outcome"]  # one-dimensional, unlike [["outcome"]]
# X_test = testing_df[X_train.columns]  # same features and order
# y_test = testing_df["outcome"]
# Keep row order aligned. Use training data for fitting/tuning and reserve test
# data for final evaluation. Random splitting is inappropriate for time series.



# %% Lecture 10 — Linear regression, model tables, and custom prediction (10a–10d)
# ============================================================================


# %% Fit OLS and inspect results — 10a–10c
# ============================================================================


model = smf.ols(formula="y ~ x", data=df)  # Specify an ordinary least squares model.
results = model.fit(cov_type="HC1")       # Fit with HC1 heteroskedasticity-robust standard errors.
results.params                           # Series of estimated coefficients; no parentheses.
results.params["Intercept"]              # Intercept by name.
results.params["x"]                      # Slope by name; avoid ambiguous integer indexing.
results.summary()                        # Detailed regression diagnostics and table.
print(results.summary())                 # Print the text summary.
round(value, 3)                          # Python built-in rounding to 3 decimal places.
abs(value)                               # Absolute value; also used inside df.query().


# Use `cov_type="HC1"`, not Lecture 10a's `cov="HC1"`, to request robust standard errors; see
# the [OLS fit
# parameters](https://www.statsmodels.org/v0.12.2/generated/statsmodels.regression.linear_model.OLS.fit.html).
# Robust covariance changes standard errors, not the OLS coefficient estimates. Fit before
# accessing result attributes.


# %% Regression formulas — 10b–10c
# ============================================================================

# Formulas are quoted strings; column names inside them are generally unquoted. The formula
# interface includes an intercept by default.

# | Formula | Meaning |
# | --- | --- |
# | `"y ~ x"` | Outcome y explained by x and an intercept. |
# | `"y ~ x + z"` | Include x and z as separate regressors. |
# | `'y ~ x + Q("z with spaces")'` | Quote a column name containing spaces with `Q()`. |
# | `"y ~ x + C(d)"` | Treat d as categorical; compare included levels with a reference level. |
# | `"y ~ x + z + x:z"` | Include main effects and their interaction. |
# | `"y ~ x * z"` | Shorthand for `x + z + x:z`. |
# | `"y ~ x + I(x ** 2)"` | Include x and its square; syntax support for the polynomial exercise
# in Lecture 12b. `I()` protects arithmetic from formula-operator interpretation. |

# `C()` and `Q()` here belong to formula syntax. In Lecture 10c, `treat * ave` allows the
# treatment difference to vary with baseline scores. The formula `treat + ave + treat*ave`
# repeats main effects in its text, but the formula parser includes each term only once.


# %% Display and export regression tables — 10b–10c
# ============================================================================


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


# Pass fitted results in a list, with one heading per model. `keep` selects and orders displayed
# coefficients; with `exact_match=True`, use names from `.params.index` exactly, including
# interaction order and category labels. Omitting `Intercept` from `keep` hides it in the table,
# not in the fitted model. The output folder must exist; `replace=True` permits overwriting an
# existing export. Keep the `ETable` object to call `.save()` separately from `.make()`.


# %% Complete cases and manual OLS — 10d
# ============================================================================


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


# This is the lecture's manual OLS formula, `(W'W)^(-1)W'y`. It requires numeric data and an
# invertible `W'W` matrix; redundant predictors can make it fail. The `OrdinaryLeastSquares`
# class in the notebook is user-defined: create it with `(X, y)`, call `.fit()` to create
# `.beta`, `.coefficients`, and `.intercept`, then call `.predict(Xtest)`. Its `.fit()` returns
# `self`, allowing `OrdinaryLeastSquares(X, y).fit()` chaining. Those attributes do not exist
# before fitting.

# The helper is named `compute_ols(X, y)` and returns the coefficient array with the intercept
# first. The custom class stores its training inputs as `.Xtrain` and `.ytrain` during
# initialization. In Lecture 10a, `fn_positive_error(error)` is a lambda returning `error >= 0`;
# passing a numeric Series produces elementwise Booleans, while `.apply(fn_positive_error)`
# calls it on each value.



# %% Lecture 13 — Regression trees, pruning, forests, and boosting (13a–13b)
# ============================================================================


# %% Dataset loading and input shapes
# ============================================================================


ISLP.load_data("Boston")                 # Load the named ISLP dataset as a DataFrame.
load_data("Smarket")                    # Same function after `from ISLP import load_data` (14b).
X_train = training_df.drop(columns=["outcome"])
X_test = testing_df.drop(columns=["outcome"])
y_train = training_df["outcome"]         # Single brackets give a 1D Series.
y_test = testing_df["outcome"]
X_train.shape[1]                         # Number of predictor columns; shape[0] counts rows.


# The lecture's `df[["shares"]]` creates a two-dimensional one-column DataFrame. For a single
# outcome, use `df["shares"]` or `np.ravel(y)` to get a 1D target. Training/test predictors must
# have the same columns in the same order; exclude the outcome from the predictors. The Boston
# exercise uses `crim` as its outcome.


# %% Train, predict, and evaluate a regression tree — 13a
# ============================================================================


tree_model = DTR(max_depth=3, random_state=0)
tree_model.fit(X_train, y_train)          # Learn splits and leaf predictions; returns this estimator.
y_pred = tree_model.predict(X_test)      # Numeric predictions, one per test row for a single outcome.
mse = np.mean((np.ravel(y_test) - np.ravel(y_pred)) ** 2)


# `DTR` aliases `DecisionTreeRegressor`. `max_depth` limits tree depth, not the total number of
# branches or leaves. `random_state` makes randomized aspects of fitting, including
# tie-breaking, reproducible. The default regression criterion is squared error. Fit before
# prediction; lower held-out MSE is better.

# **Shape correction:** subtracting an `(n, 1)` target array from `(n,)` predictions broadcasts
# to an `(n, n)` array. That averages errors between different observations and can silently
# give the wrong MSE. Flatten both single-outcome arrays and ensure they have equal lengths and
# matching row order before subtracting.


# %% Visualize the fitted tree — 13a
# ============================================================================


dot_text = tree.export_graphviz(
    decision_tree=tree_model,
    feature_names=X_train.columns.values,
    filled=True
)
graphviz.Source(dot_text)                # Wrap DOT source for notebook rendering.


# `export_graphviz` returns a DOT-format string when no output file is specified.
# `feature_names` supplies one label per predictor in training-column order. `filled=True`
# colors nodes; the pruned-tree example omits it. `graphviz.Source` is a constructor, not a tree
# estimator. Notebook rendering also needs the Graphviz executable `dot` available on PATH;
# installing the Python package alone may not provide it. The lecture suggests `conda install
# python-graphviz` if needed. See the [Graphviz installation
# guide](https://graphviz.readthedocs.io/en/stable/manual.html).


# %% Cost-complexity pruning and grid search — 13a
# ============================================================================


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


# `cost_complexity_pruning_path` computes candidate subtrees for the estimator's settings; it
# does not modify the fitted tree into the selected pruned model. Larger `ccp_alpha` generally
# means more pruning. The parameter grid is a dictionary with exact estimator parameter names as
# string keys and collections of candidate values. `cv` supplies the fold scheme; `refit=True`
# fits the winner on the full search-training data. `best_estimator_` is available after
# fitting, with a trailing underscore and no parentheses.

# `GridSearchCV` chooses the highest score. Negative MSE therefore makes a smaller error score
# better: −10 beats −100. `skm.GridSearchCV` and a directly imported `GridSearchCV` are the same
# class. See [decision-tree
# pruning](https://scikit-learn.org/1.7/modules/generated/sklearn.tree.DecisionTreeRegressor.html).
# Keep the final test data out of pruning selection.


# %% Bagging and random forests — 13b
# ============================================================================


bagged_model = RF(max_features=X_train.shape[1], random_state=0)
bagged_model.fit(X_train, np.ravel(y_train))

rf_model = RF(random_state=0)             # The notebook's second specification.
rf_model.fit(X_train, np.ravel(y_train))
rf_predictions = rf_model.predict(X_test)


# `RF` aliases `RandomForestRegressor`; predictions average the fitted trees. With its default
# `bootstrap=True`, each tree fits a sample drawn with replacement. `max_features` controls
# candidate features **at each split**, not a permanent set of discarded columns. An integer
# specifies a count; a fraction such as `0.5` selects roughly half the features; `"sqrt"`
# selects about the square root of the feature count.

# **Default clarification:** current `RF()` uses `max_features=1.0`, meaning all features. Thus
# the two notebook specifications both use all predictors at each split; the second does not
# automatically introduce feature subsampling. For an explicit feature-subsampling comparison,
# use a setting such as `RF(max_features="sqrt", random_state=0)`. See [RandomForestRegressor
# parameters](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html?highlight=randomforest).


# %% Gradient boosting — 13b
# ============================================================================


boost_model = GBR(
    n_estimators=5000, learning_rate=0.2, max_depth=3, random_state=0
)
boost_model.fit(X_train, np.ravel(y_train))
y_hat_boost = boost_model.predict(X_test)
boost_mse = np.mean((np.ravel(y_test) - np.ravel(y_hat_boost)) ** 2)


# `GBR` aliases `GradientBoostingRegressor`. `n_estimators` is the number of boosting stages,
# `learning_rate` scales each added tree's contribution, and `max_depth` limits each individual
# tree. Boosting adds trees sequentially to improve the current predictions, unlike averaging
# independently fitted bootstrap trees. Tune learning rate and stage count together. The
# notebook uses 5,000 stages; that can take time. The trailing semicolon after `.predict(...)`
# in the notebook is optional Python syntax, not part of the method.



# %% Lecture 14 — Cross-validation and expanding windows (14a–14b)
# ============================================================================


# %% K-fold splitting and cross-validation — 14a
# ============================================================================


cv = KFold(n_splits=5, shuffle=True, random_state=0)
cv_results = cross_validate(tree_model, X_estimate, np.ravel(y_estimate), cv=cv)
np.mean(cv_results["test_score"])        # Average held-out R² for a standard regression tree.


# `KFold` splits observations into `n_splits` folds; each is held out once while the other folds
# train the model. The split count must be at least 2 and no greater than the number of
# observations. `shuffle=True` randomizes row allocation before splitting; `random_state` fixes
# that shuffle. `skm.KFold(5, ...)` uses the same class, with a positional split count.

# `cross_validate` clones and fits the estimator separately in each fold, so it does not require
# the preliminary `.fit()` shown in the notebook. It returns a dictionary of arrays, including
# `"test_score"`, `"fit_time"`, and `"score_time"`. Here “test” means the held-out fold within
# the supplied data, not the separate external dataset. This call does not refit the supplied
# estimator on the full dataset.

# **Choose the metric explicitly when comparing errors:** without `scoring`, `cross_validate`
# uses the estimator's `.score()`; for `DTR` that is R², not MSE. For MSE:


cv_results = cross_validate(
    tree_model, X_estimate, np.ravel(y_estimate), cv=cv,
    scoring="neg_mean_squared_error"
)
cv_mse = -np.mean(cv_results["test_score"])  # Negate once to obtain positive MSE.


# R² is higher-is-better and can be negative; MSE is lower-is-better. Use training folds to
# compare settings, refit the selected model on the estimation data, then evaluate on the
# untouched validation/test data. See
# [cross_validate](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html).


# %% Commented-out leave-one-out example and statsmodels adapter — 14a
# ============================================================================


M = sklearn_sm(sm.OLS)                   # Adapt a statsmodels model class to sklearn's interface.
X = sm.add_constant(np.array(X_estimate)) # Add an intercept column; default prepends it.
Y = np.ravel(y_estimate)
cv_results = cross_validate(
    M, X, Y, cv=X_estimate.shape[0], scoring="neg_mean_squared_error"
)
loo_mse = -np.mean(cv_results["test_score"])

ols_results = sm.OLS(Y, X).fit()          # Direct matrix-interface OLS; outcome comes first.


# `sm.OLS` is a model class, passed **without parentheses** to `sklearn_sm`; the adapter
# provides fitting and prediction for cross-validation. `sm.add_constant` supplies the intercept
# that matrix-based `sm.OLS` does not add automatically. By default it skips adding another
# column if it detects an existing nonzero constant column. `cv=n` gives leave-one-out folds for
# this regression example and fits n models; it can be slow.

# The notebook's commented variable `X_estiamte` is a typo for `X_estimate`. Its `sklearn_sm`
# example omits `scoring`; the installed ISLP adapter uses positive MSE for OLS, unlike a
# sklearn tree's default R². Adapter behavior can vary by version, so the explicit negative-MSE
# scorer above fixes the meaning. Flatten Y to avoid the same broadcasting issue as Lecture 13.
# R² is not defined for a one-observation held-out fold. The adapter comes from [ISLP's sklearn
# wrappers](https://intro-stat-learning.github.io/ISLP/api/generated/ISLP.models.sklearn_wrap.html).


# %% Time ordering, row numbers, and expanding windows — 14b
# ============================================================================


Smarket = load_data("Smarket")
Smarket.plot(y="Volume")                # Plot the selected column against the DataFrame index.
Smarket["obs_num"] = np.arange(1, len(Smarket) + 1)
split = len(Smarket) // 2                # Integer floor division: initial half-sample size.
training = Smarket.query("obs_num <= @split")
testing = Smarket.query("obs_num > @split")


# `np.arange(start, stop, step)` returns evenly spaced values with stop excluded; step defaults
# to 1, so `np.arange(1, n + 1)` gives row numbers 1 through n. The row-number column is an
# identifier, not automatically a predictor. The lecture assumes the data are already in
# chronological order.

# For the exercise, choose a numeric outcome and predictors available at prediction time; define
# `features` explicitly. `DTR` must be imported in this notebook, and `.fit()` needs both X and
# y. The current exercise cell has a bare `features` expression and empty `.fit()` calls, so it
# is an unfinished template. Supplemental syntax for one-step-ahead evaluation:


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


# The initial window needs at least one training row and one later test row. This example
# implements the first fit, the half-plus-one fit, and up to ten further fits, using only
# earlier observations to predict the next one. The lecture leaves the evaluation horizon open;
# choose it consistently if predicting several future rows instead. Do not randomly shuffle
# time-series rows or use future outcomes in predictors. String labels such as `Direction` need
# a classification workflow rather than regression MSE.



# %% Lecture 12 — Logistic classification and Poisson regression (12a–12b)
# ============================================================================


# %% Build model matrices and estimate logistic regression — 12a
# ============================================================================


y, X = patsy.dmatrices(
    "request_loan ~ 1 + received_info + owns_house + home_numrooms",
    df, return_type="dataframe"
)
y = np.ravel(y)                         # Flatten the response to a 1D array.

logit_results = smf.logit("request_loan ~ received_info + owns_house + home_numrooms",
                          data=df).fit(cov_type="HC1")
matrix_results = sm.Logit(y, X).fit(cov_type="HC1")


# Patsy returns outcome and design matrices, expanding formula terms and dropping rows with
# missing model inputs by default. The `1` requests an intercept column. The matrix interface
# uses the supplied columns as-is, so include the intercept in `X`. A binary logistic outcome is
# coded 0/1. Use the Lecture 10 table methods for fitted statsmodels results.


classifier = LogisticRegression(
    penalty=None, fit_intercept=False, solver="lbfgs",
    max_iter=1000, tol=1e-10
).fit(X, y)
classifier.coef_                        # Fitted coefficient array; trailing underscore.
classifier.coef_.ravel()                # Flatten coefficients for a binary model.
pd.Series(classifier.coef_.ravel(), index=X.columns)  # Attach predictor names.


# This preserves the lecture's unpenalized sklearn specification. `fit_intercept=False` avoids
# adding a second intercept because Patsy already supplied one. `max_iter` is the iteration
# limit; `tol` controls convergence tolerance. Newer sklearn versions deprecate `penalty`; their
# unpenalized alternative uses `C=np.inf` in place of `penalty=None`. See [LogisticRegression
# parameters](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).
# Full-sample coefficient comparison and held-out prediction evaluation are separate tasks.


# %% Split data, predict probabilities, and classify — 12a
# ============================================================================


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


# `test_size=0.5` reserves half the observations for testing; `random_state` makes the split
# reproducible. Train on the training sample and evaluate on the test sample. With the lecture's
# threshold rule, probabilities at or below 0.2 become class 0 and those above become class 1.
# `include_lowest=True` also classifies exactly zero, which the notebook's default `pd.cut` call
# would leave missing. Keep outcome values aligned with design-matrix rows.


# %% Confusion matrix and annotations — 12a
# ============================================================================


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


# `labels=[0, 1]` keeps a consistent 2×2 layout. `ax.text(x, y, text, ...)` places annotations
# at data coordinates; `ha` and `va` control horizontal and vertical alignment. Accuracy is `(TN
# + TP) / total`; changing the threshold changes the tradeoff between false positives and false
# negatives.


# %% Poisson regression — optional 12b
# ============================================================================


y, X = patsy.dmatrices("wage ~ age + tenure", df, return_type="dataframe")
y = np.ravel(y)
poisson_results = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1")
poisson_results.summary()
mt.ETable([poisson_results]).make(type="gt")
poisson_results.predict(X_test)         # Predicted means; test matrix must match training columns.


# `sm.GLM` specifies a generalized linear model. `sm.families.Poisson()` uses a log link by
# default, giving conditional mean `exp(X @ beta)`. Poisson is commonly used for nonnegative
# counts; the lecture's wage example uses the exponential mean specification with robust
# covariance. Skewness alone does not establish that this is an appropriate model. Reuse
# train/test splitting for the prediction exercise and compare mean squared errors using
# `np.mean((actual - predicted) ** 2)`.



# %% Lecture 15 — Scaling, SVM classification, metrics, and tuning
# ============================================================================


# %% Retrieve UCI data and prepare inputs
# ============================================================================


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


# `fetch_ucirepo` returns a dataset object; `.data.features` and `.data.targets` hold its
# predictors and outcomes. The lecture removes two string columns to leave features suitable for
# the numeric estimator. `test_size=0.25` reserves a quarter of the rows; `shuffle=True`
# randomizes the split and `random_state` makes it reproducible. The proportional crosstab
# excludes missing labels from its counts but divides by all rows, so it sums to one only when y
# has no missing values. Source: [UCI's Python
# package](https://github.com/uci-ml-repo/ucimlrepo/blob/main/README.md?plain=1).


# %% Standardize features with the training scaler
# ============================================================================


scaler = preprocessing.StandardScaler() # Create a transformer; default centers and scales each feature.
scaler.fit(X_train)                     # Learn feature means/variances from training rows; returns self.
X_train_scale = scaler.transform(X_train)
X_test_scale = scaler.transform(X_test)  # Reuse exactly the same learned transformation.


# `StandardScaler` applies `(x - training_mean) / training_standard_deviation` column by column
# and normally returns a NumPy array. Nonconstant training features have mean zero and unit
# variance after scaling; test features need not. Keep columns in the same order.
# `scaler.transform` applies learned values without fitting again; this is a different method
# from pandas `groupby(...).transform(...)` in Lecture 3.

# **Correction to the notebook:** do not fit `scaler_test` on `X_test`. That gives test rows a
# different coordinate system and uses information from the evaluation data. Fit on training
# rows only and transform both sets with that scaler. For cross-validation, learn the scaler
# inside each fold, as shown below. See [scikit-learn's preprocessing
# guidance](https://scikit-learn.org/stable/common_pitfalls) and
# [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html?highlight=standardscaler).


# %% Fit and score an SVM classifier
# ============================================================================


svm = SVC()                             # Support-vector classifier; default RBF kernel and C=1.
svm.fit(X_train_scale, y_train)          # Fit on scaled features and class labels; returns self.
predictions = svm.predict(X_test_scale) # Predicted class labels, not probabilities.
svm.classes_                           # Class labels in estimator order; trailing underscore.
accuracy = svm.score(X_test_scale, y_test)  # Fraction correctly classified; higher is better.
candidate = SVC(gamma=0.1, C=1)         # Separate unfitted model with explicit tuning parameters.


# `C` must be positive: larger C penalizes training errors more strongly (weaker
# regularization). For the RBF kernel, a larger positive `gamma` makes each observation's
# influence more local. The default is `gamma="scale"`, calculated as `1 / (n_features *
# X.var())`; `gamma="auto"` uses `1 / n_features`. The notebook's default-gamma statement omits
# the variance factor. Scaling can make these values similar, but they are not universally
# identical. See [SVC
# parameters](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html).

# Always pass data in the representation used during fitting: an SVC fitted on `X_train_scale`
# must receive `X_test_scale` in `.predict()` and `.score()`. The notebook's later calls on raw
# `X_test` do not follow that rule. Unlike regression-tree `.score()` (R²), SVC `.score()`
# reports classification accuracy.


# %% Confusion-matrix proportions and display
# ============================================================================


cm = confusion_matrix(y_test, predictions, labels=svm.classes_) / len(y_test)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=svm.classes_)
disp.plot()                             # Draw the display; returns the display object.
plt.show()


# Rows are actual labels and columns are predictions, both ordered by `svm.classes_`. Dividing
# the entire matrix by `len(y_test)` gives proportions of **all test observations**; it is not
# normalization separately within each actual class. The diagonal sum equals overall accuracy
# when every label is included. `ConfusionMatrixDisplay` accepts the precomputed matrix and
# matching labels; `.plot()` renders it.


# %% Discover scorers and evaluate multiple metrics
# ============================================================================


get_scorer_names()                       # List of valid named scorers available in installed sklearn.
list_scorers = pd.DataFrame(get_scorer_names())


# The lecture calls `cross_validate(SVC(), X_train_scale, y_train, scoring=["accuracy",
# "roc_auc", "recall_macro"], return_train_score=False, cv=5)`. This requests five-fold scores
# for three metrics. For a binary classifier with integer `cv`, sklearn uses stratified folds,
# without shuffling by default. Each class needs enough observations for the chosen number of
# folds.

# | Scorer | Meaning and required prediction type |
# | --- | --- |
# | `"accuracy"` | Fraction of predicted class labels that are correct. |
# | `"roc_auc"` | Binary ranking performance across thresholds; uses decision scores or
# probabilities, not hard labels. SVC provides decision scores, so probability estimation is not
# required for this scorer. |
# | `"recall_macro"` | Recall computed for each class, then averaged with equal class weights,
# regardless of class sizes. |

# All three are higher-is-better. With multiple named metrics, result keys are
# `"test_accuracy"`, `"test_roc_auc"`, and `"test_recall_macro"` rather than just
# `"test_score"`. `return_train_score=False` omits training-fold scores. `pd.DataFrame(res)`
# shows one row per fold; `.mean()` averages numeric columns, including `fit_time` and
# `score_time`, which are seconds, not performance measures.

# Correction: scaling before CV leaks held-out-fold information. Fit the scaler within each
# training fold; the supplemental Pipeline implementation remains in FUNCTIONS_REFERENCE.md.


# %% Manual tuning, dictionaries, and string formatting
# ============================================================================


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


# `X_valid_scale` is a validation set transformed by the training scaler, with aligned labels
# `y_valid`; these are placeholders for a separate tuning split. Nested loops try every C/gamma
# pair. `**best_parameters` is equivalent to writing `C=..., gamma=...` explicitly, not
# exponentiation in this call context. String `.format(value)` substitutes into `{}`; `\n`
# inserts a newline. This string method is distinct from pandas Styler `.format(...)`.

# The notebook initializes `best_score=0`; if every score is zero, its strict `>` test never
# defines `best_parameters`. It also tunes repeatedly on the named test set, which then acts as
# validation data and is no longer an untouched final test. Its heading says “all data,” but
# `.fit(X_train_scale, y_train)` fits only that training subset. Prefer CV on the training set
# for parameter selection and reserve test data for final evaluation.


# %% Grid search options and the forest exercise
# ============================================================================


param_grid = {
    "C": [0.01, 0.1],
    "gamma": [0.01 / k_features, 0.1 / k_features]
}
grid_search = GridSearchCV(
    SVC(), param_grid, cv=2, return_train_score=True, n_jobs=-1
)
# Constructor matches the lecture. Use a pipeline below to include scaling within folds.


# The grid defines four parameter combinations, with exact SVC parameter names as keys. `cv=2`
# uses two stratified folds for this classifier; increasing it uses a larger training fraction
# per fit but requires more fits. `return_train_score=True` includes training scores in
# `cv_results_`; `n_jobs=-1` requests all available processors. Without explicit `scoring`, the
# search maximizes SVC's accuracy. Default `refit=True` fits the best setting on all rows
# supplied to the search's `.fit()`.

# The final exercise asks for a **random forest classifier** grid, not the regression estimator
# `RF` from Lecture 13. The exercise asks for n_estimators values [10, 50]. It counts trees, not
# forests. The original exercise cell is blank; no new solution function is added here.


# %% Lecture 16 — Neural networks and TensorFlow
# ============================================================================


# %% Imports, environment, and numeric inputs
# ============================================================================


import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense           # Exact lecture import.
# Consistent alternative: from tensorflow.keras.layers import Dense
X = np.asarray(X).astype(np.float32)
y = np.asarray(y).astype(np.float32)


# Use the notebook's **Python (Computing 530 — TensorFlow)** kernel, backed by
# `.venv-tensorflow`. Installing a package into another Python environment does not make it
# available to that kernel. Lecture 17 also records `/opt/anaconda3/bin/python -m pip install
# faiss-cpu`, which targets Anaconda specifically. Installation commands belong in a terminal,
# not a plain `.py` statement.

# `np.asarray` converts the feature table/target Series to arrays; `.astype(np.float32)`
# converts values to 32-bit floating point. This removes pandas column labels, so retain feature
# names separately if needed. Boolean targets become 0.0/1.0. Shapes are `(n, k_features)` for X
# and `(n,)` for y; `X.shape[1]` obtains the number of features and `print(k_features)` displays
# it.

# The lecture repeats `fetch_ucirepo(id=468)`, `.data.features`, `.data.targets["Revenue"]`,
# `.drop(columns=["Month", "VisitorType"])`, and `train_test_split(..., random_state=104,
# test_size=0.25, shuffle=True)` from Lecture 15. Its imported `SVC`, `cross_val_score`,
# `GridSearchCV`, `cross_validate`, and `get_scorer_names` have no calls here; see Lectures
# 14–15 for their syntax and purpose.


# %% Configure, compile, and train
# ============================================================================

# The following follows the lecture architecture with two corrections: set the seed before
# constructing layers, and use one training-fitted scaler throughout.


tf.keras.utils.set_random_seed(0)
scaler_train = preprocessing.StandardScaler().fit(X_train)
X_train_scale = scaler_train.transform(X_train)
X_test_scale = scaler_train.transform(X_test)
k_features = X_train.shape[1]

basic_model = keras.models.Sequential()
basic_model.add(Dense(units=16, activation="relu", input_shape=(k_features,)))
basic_model.add(Dense(units=1, activation="sigmoid"))
adam = keras.optimizers.Adam(learning_rate=0.001)
basic_model.compile(loss="binary_crossentropy", optimizer=adam, metrics=["accuracy"])
history = basic_model.fit(X_train_scale, y_train, epochs=100)


# | Call / option | Use and syntax details |
# | --- | --- |
# | `keras.models.Sequential()` | Model whose layers run in sequence. `.add(layer)` appends a
# layer to that model. |
# | `Dense(units=16, activation="relu", input_shape=(k_features,))` | Fully connected layer with
# 16 neurons. Each neuron applies an activation to a weighted sum plus bias. The input shape
# excludes the batch dimension; the comma makes a one-element tuple. |
# | `activation="relu"` | Rectified linear unit: `max(0, z)`, giving a nonlinear hidden layer. |
# | `Dense(units=1, activation="sigmoid")` | One output probability for binary classification:
# sigmoid is `1 / (1 + exp(-z))`. Two classes do **not** require two output neurons with this
# setup. |
# | `keras.optimizers.Adam(learning_rate=0.001)` | Optimizer that adjusts weights using
# gradients and adaptive updates. Learning rate controls step size. |
# | `.compile(loss=..., optimizer=..., metrics=[...])` | Configures training. Binary
# cross-entropy is the loss being minimized; accuracy is a separate reported metric. Compilation
# does not train weights. |
# | `.fit(X, y, epochs=100)` | Trains for 100 passes through the training data; returns a
# History object, unlike sklearn `.fit()` returning the estimator. Batch size controls
# observations per update; the lecture omits `batch_size` (array-input default is 32). |
# | `tf.keras.utils.set_random_seed(0)` | Sets Python, NumPy, and TensorFlow seeds. Place before
# model construction so random initial weights are covered; some operations/hardware can still
# be nondeterministic. |

# The lecture uses input_shape on Dense; newer Keras may warn about this syntax.
# The first Dense layer is a hidden layer receiving input, followed by an output layer.

# **Notebook corrections:** it fits a separate test scaler and even repeats
# `.fit(X_test).transform(X_test)`. Use the training scaler for test data. Its actual model
# `.fit(X_train, ...)` and `.predict(X_test)` use raw features, so its scaling cells have no
# effect on that fitted model. The example above deliberately uses scaled features for both. Its
# seed is set after layer construction; move it earlier for reproducible initialization.

# Sources: [Dense](https://keras.io/api/layers/core_layers/dense/), [training
# APIs](https://keras.io/api/models/model_training_apis/), and [random seed
# utility](https://www.tensorflow.org/api_docs/python/tf/keras/utils/set_random_seed).


# %% Probabilities, thresholds, and confusion matrices
# ============================================================================


predicted_prob = basic_model.predict(X_test_scale)  # Shape (n_test, 1).
predicted_prob = tf.squeeze(predicted_prob, axis=-1)
threshold = 0.5
predicted = np.array([1 if x >= threshold else 0 for x in predicted_prob])
cm = confusion_matrix(y_test, predicted)
displ = ConfusionMatrixDisplay(confusion_matrix=cm)
displ.plot()
plt.show()


# Keras `.predict()` here returns probabilities, whereas SVC `.predict()` returns labels. The
# list comprehension applies the threshold element by element and `np.array` collects the
# integer labels. `tf.squeeze` removes dimensions of length one; the lecture uses
# `tf.squeeze(predicted_prob)` with no axis, which removes **all** such dimensions. The explicit
# `axis=-1` above preserves the observation dimension even for a single prediction. See
# [TensorFlow squeeze](https://www.tensorflow.org/api_docs/python/tf/squeeze).

# This confusion matrix contains **counts**, unlike Lecture 15's matrix divided by sample size.
# Rows are true labels and columns predicted labels. For labels `[0, 1]`, entries are `[[TN,
# FP], [FN, TP]]`. Accuracy is `(TP + TN) / n`; false-positive rate is `FP / (FP + TN)` when the
# denominator is nonzero. Lowering the threshold usually increases both true-positive and
# false-positive rates; choose a threshold with validation data, then assess on untouched test
# data.


# %% Concepts and exercises
# ============================================================================

# Logistic regression applies sigmoid to one linear predictor. A neural network adds hidden
# transformations, learning weights and biases from examples. More neurons/layers increase
# flexibility but do not guarantee better test accuracy. Universal approximation means
# sufficiently expressive networks can approximate continuous functions on a compact domain; it
# does not guarantee training will find those weights or generalize.

# Training repeats **forward propagation → loss calculation → backpropagation → optimizer
# update** for batches across epochs. Architecture, activation, learning rate, batch size, and
# epochs are hyperparameters chosen before a training run; weights and biases are fitted
# parameters. Loss guides optimization, while evaluation metrics answer how well the model
# performs on the task.

# | Task / metric mentioned in the notes | Meaning / when to use |
# | --- | --- |
# | Regression: MAE, MSE, RMSE, R² | Absolute error; squared error; square root of MSE in
# outcome units; improvement relative to predicting the mean. |
# | Precision, recall, F1 | `TP/(TP+FP)`; `TP/(TP+FN)`; harmonic mean of precision and recall
# (when defined). Useful when mistakes or classes have unequal importance. |
# | ROC-AUC, log loss | Ranking across thresholds; quality of predicted probabilities with
# confident wrong predictions penalized heavily. |
# | PR-AUC | Area under a precision–recall curve; useful for rare positive outcomes. Accuracy
# alone can hide failure on a minority class. |

# These metrics are named concepts here; no corresponding metric functions are called in this
# notebook beyond the confusion-matrix display and compiled accuracy.

# The exercises ask you to increase units, add hidden layers, and use
# `ArticlesTrain.csv`/`ArticlesTest.csv`. To add a hidden layer, place another
# `basic_model.add(Dense(units=16, activation="relu"))` **before** the output layer, then
# compile and train a fresh model. Compare architectures on validation data. For article shares
# as a continuous outcome, a supplemental suitable output is `Dense(units=1,
# activation="linear")` with a regression loss such as `loss="mse"`; use binary cross-entropy
# only if a binary target has actually been defined. Load the files with the previously covered
# `pd.read_csv`, separate the target from predictors, and keep train/test feature columns
# aligned.



# %% Lecture 17 — Optimization, PCA, and K-means clustering
# ============================================================================


# %% Imports and dataset attributes
# ============================================================================


from sklearn.decomposition import PCA
from sklearn.datasets import load_breast_cancer
from sklearn.cluster import MiniBatchKMeans  # Imported only; supplemental example below.
import seaborn as sns
import faiss

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
print(X_train.shape)
print(X_test.shape)
cancer.feature_names


# `load_breast_cancer()` returns a dataset container: `.data` is the numeric feature array,
# `.target` holds labels, and `.feature_names` gives the feature names. The label mapping is **0
# = malignant, 1 = benign**; `.target_names` is a supplemental way to check it. With both split
# sizes omitted, `train_test_split` reserves 25% for testing; `random_state=0` fixes the split.
# See [dataset
# documentation](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html).

# The repeated imports `fetch_ucirepo`, `SVC`, `cross_val_score`, `GridSearchCV`,
# `confusion_matrix`, `ConfusionMatrixDisplay`, `cross_validate`, and `get_scorer_names` are not
# called here; their uses are covered in Lectures 14–15. SVC is requested in an exercise.


# %% Optimization concepts
# ============================================================================

# Gradient descent updates parameters by `theta_new = theta_old - learning_rate *
# gradient(loss)`. Full-batch descent uses all training observations per update; stochastic
# gradient descent uses one, and mini-batch methods use a subset. Smaller updates can be slow;
# overly large updates can overshoot. Noisy updates can help exploration but guarantee neither
# escape from poor solutions nor a global optimum.

# Setting a derivative to zero identifies a stationary point in a differentiable unconstrained
# problem, not necessarily a minimum. More iterations give an algorithm more opportunity to
# converge, but the notebook's proposed inverse relationship between runtime and accuracy is not
# a general law. Iterative optimization can stop before its iteration limit, and more
# computation need not improve test performance.


# %% Fit PCA and compute component scores
# ============================================================================


pca = PCA(n_components=3)
pca.fit(X_train)
factor_loadings = pd.DataFrame(pca.components_, columns=cancer.feature_names)
X_pca = pca.transform(X_train)

# Scaling exercise: fit preprocessing and PCA using training rows only.
scaler_train = preprocessing.StandardScaler().fit(X_train)
X_train_scale = scaler_train.transform(X_train)
X_test_scale = scaler_train.transform(X_test)
pca = PCA(n_components=3)
pca.fit(X_train_scale)
factor_loadings = pd.DataFrame(pca.components_, columns=cancer.feature_names)
X_pca = pca.transform(X_train_scale)
X_test_pca = pca.transform(X_test_scale)


# `PCA(n_components=3)` retains three directions. `.fit()` learns the training mean and
# directions; `.components_` has shape `(3, n_features)` with one row of weights per component.
# `.transform()` centers using the learned mean and projects each observation, producing
# `(n_rows, 3)`. `.fit()` returns the PCA estimator; `.transform()` returns scores. PCA centers
# automatically but does not standardize feature variances. Scaling changes which features
# dominate; use the same scaler/PCA on held-out data. See [PCA
# documentation](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).

# For centered feature matrix `Xc`, scores are `F = Xc @ omega`. The first direction maximizes
# variance, equivalently the Rayleigh quotient `omega.T @ Xc.T @ Xc @ omega / (omega.T @
# omega)`; subsequent directions capture remaining variance while orthogonal to earlier
# directions. Components' scores are uncorrelated on the fitting data, not necessarily
# statistically independent. The constraint `sum(omega_j ** 2) = 1` means the **squared
# weights** sum to one; the weights themselves need not sum to one and may be negative. A
# component's sign can flip without changing its meaning.

# PCA is unsupervised dimensionality reduction: it uses X, not y, and high variance need not be
# predictive. Fewer components can reduce complexity and discard noise, but can also discard
# predictive information. There is no guarantee the first two capture most variation; perfectly
# lower-rank data can even have all variation in one direction. Supplemental diagnostics are
# `pca.explained_variance_ratio_` and `pca.explained_variance_ratio_.sum()` to inspect retained
# variance.


# %% Loadings heatmap and scatterplot formatting
# ============================================================================


plt.matshow(pca.components_, cmap="viridis")
plt.yticks([0, 1, 2], ["First component", "Second component", "Third component"])
plt.colorbar()
plt.xticks(range(len(cancer.feature_names)), cancer.feature_names, rotation=60, ha="left")
plt.xlabel("Feature")
plt.ylabel("Principal components")
plt.show()

ax = sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=y_train)
ax.set(xlabel="First Principal Component", ylabel="Second Principal Component")
ax.legend(title="Cancer Screening", loc="upper left")
plt.show()


# `plt.matshow` displays the weight matrix as a colored grid; `cmap` selects its color map and
# `plt.colorbar()` adds the value scale. `plt.yticks(positions, labels)` labels rows;
# `plt.xticks` labels columns, `rotation=60` tilts text 60 degrees, and `ha="left"` left-aligns
# it. `range(len(...))` supplies positions. `plt.xlabel`/`ylabel` set axis names and
# `plt.show()` displays the figure. Color shows signed weight, so a large negative weight can
# also be a strong contribution.

# `X_pca[:, 0]` selects the first component for every row; `[:, 1]` selects the second.
# `sns.scatterplot(x=..., y=..., hue=...)` colors points by the supplied variable and returns an
# Axes. `ax.set(xlabel=..., ylabel=..., title=...)` sets plot properties. `ax.legend(title=...,
# loc=..., labels=[...])` can override legend text, but labels must match the plotted order. The
# notebook's `labels=["Benign", "Malignant"]` reverses the dataset's numeric order; the example
# leaves numeric labels intact. Use a mapping from 0/1 to malignant/benign if descriptive labels
# are desired.

# **Notebook clarification:** it fits three components but labels only two heatmap rows and
# describes `.transform()` as returning two. The heatmap above labels all three; the scatterplot
# intentionally displays just the first two.

# The SVM exercise combines supervised prediction with PCA: fit the scaler and PCA on training
# data, fit `SVC()` on training component scores and `y_train`, then call `.score(X_test_pca,
# y_test)` for held-out accuracy. If tuning by CV, use a `Pipeline` containing scaler, PCA, and
# SVC so each fold fits its own preprocessing (see Lecture 15). PCA and a classifier can be used
# together; PCA alone does not predict class labels.


# %% Fit FAISS K-means and assign clusters
# ============================================================================


ncentroids = 3
niter = 100
verbose = True
d = X_train.shape[1]
kmeans = faiss.Kmeans(d, ncentroids, niter=niter, verbose=verbose, seed=0)
Xtilde = np.float32(X_train)
kmeans.train(Xtilde)
results = kmeans.index.search(Xtilde, 1)
indexes_train = results[1]
cluster_labels = indexes_train.ravel()


# `faiss.Kmeans` creates the clusterer: `d` is feature count, `ncentroids` is K, `niter` limits
# iterations, `verbose=True` prints progress, and `seed` controls random initialization.
# `np.float32(X_train)` converts the array to float32; `.train()` learns centroids.
# `.index.search(Xtilde, 1)` retrieves the nearest **one** centroid for each row, returning
# `(squared_distances, centroid_indices)`, both shaped `(n_rows, 1)`. Thus `results[1]` is
# membership, not distance; `.ravel()` flattens it to `(n_rows,)`. IDs run from 0 to K−1 and
# have no inherent class meaning. Source: [FAISS
# clustering](https://github.com/facebookresearch/faiss/wiki/Faiss-building-blocks:-clustering,-PCA,-quantization).

# The notebook converts training input but passes the original array to `.search()`. Passing the
# same float32 representation to both is clearer and avoids relying on wrapper conversions. For
# the scaling exercise:


Xtilde_scale = np.float32(X_train_scale)
kmeans.train(Xtilde_scale)
results_scale = kmeans.index.search(Xtilde_scale, 1)
indexes_train_scale = results_scale[1]
cluster_labels = indexes_train_scale.ravel()


# Retraining this object replaces its learned centroids; use separate objects if retaining raw
# and scaled results for comparison. New observations need the training scaler before
# assignment. Keep the feature count and column order unchanged.

# K-means is **unsupervised clustering**, not supervised classification. It alternates
# nearest-centroid assignment with recomputing each centroid as the mean of assigned points,
# minimizing within-cluster squared distances. A centroid is a point in feature space, but need
# not be an observed row. Initialization matters and the result can be a local optimum. Roughly
# spherical, similarly sized clusters suit this distance-based method; scaling changes
# distances. Increasing iterations does not guarantee the global optimum or better class
# prediction.

# The notes name the **elbow method** (look for diminishing reduction in within-cluster squared
# distances as K increases) and **silhouette score** (compare cohesion within a cluster with
# separation from other clusters) for choosing K. Neither is actually called or plotted in the
# notebook. Clusters need not correspond to benign/malignant labels, and cluster IDs cannot be
# directly interpreted as predicted classes.


# %% Plot clusters in PCA coordinates
# ============================================================================


fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(
    x=X_pca[:, 0], y=X_pca[:, 1], hue=cluster_labels,
    palette="viridis", alpha=0.8, ax=ax
)
ax.set(xlabel="First Principal Component", ylabel="Second Principal Component",
       title="K-means Clusters Projected onto PCA")
ax.legend(title="Cluster")
plt.show()


# `plt.subplots` returns Figure and Axes; `figsize=(8, 6)` gives width and height in inches.
# `palette` supplies seaborn's hue colors, `alpha=0.8` sets opacity, and `ax=ax` draws into that
# Axes. Unlike `cmap` in `matshow`, `palette` belongs to seaborn. Points and cluster labels must
# have identical row order. This is a two-dimensional **view of clusters fitted in the original
# feature space** (raw or scaled); the displayed plot does not mean K-means was trained on two
# PCs. Use the PCA fitted on the same chosen representation when comparing plots.



# %% Panel models — optional 11e
# ============================================================================


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


# Pooled OLS combines observations; between OLS uses entity averages; first differences use
# changes within entities. Random effects requires assumptions about the relationship between
# entity effects and regressors. `EntityEffects`/`TimeEffects` request fixed effects in
# `PanelOLS` formulas. Entity effects absorb time-invariant regressors. Entity-clustered
# covariance permits within-entity error dependence. Unlike statsmodels formulas, these
# linearmodels formulas need an explicit `1 +` if an intercept is wanted; first-difference
# models must not contain a constant.
