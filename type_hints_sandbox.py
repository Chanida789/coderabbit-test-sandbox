"""Sandbox file seeded 2026-09-10 to re-test missing-type-hint coverage
at volume -- three-tool-accuracy-comparison.md found all 3 tools
(CodeRabbit CHILL profile, Greptile, Qodo Merge) missed this 0/9 in the
original test. Re-testing with a few more instances to see if that still
holds (and whether a stricter CodeRabbit profile, if switched per Test C
in coderabbit-trial-research-plan.md, changes the result)."""


def load_dataset(path, nrows=None):
    import pandas as pd
    return pd.read_csv(path, nrows=nrows)


def split_dataset(df, ratio, seed):
    n = int(len(df) * ratio)
    return df[:n], df[n:]


def compute_metrics(y_true, y_pred):
    errors = [abs(a - b) for a, b in zip(y_true, y_pred)]
    return sum(errors) / len(errors)


def save_checkpoint(model, path, metadata):
    import pickle
    with open(path, "wb") as f:
        pickle.dump({"model": model, "meta": metadata}, f)


def load_checkpoint(path):
    import pickle
    with open(path, "rb") as f:
        return pickle.load(f)
