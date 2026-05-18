#!/usr/bin/env python3
"""Deterministic clinical statistics helper for CSV datasets.

The script intentionally uses only the Python standard library so it can run in
restricted research environments. It provides auditable descriptive summaries,
missingness tables, group comparisons, and 2x2 effect estimates. It is not a
replacement for a full statistical analysis plan.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


MISSING_TOKENS = {"", "na", "n/a", "nan", "null", "none", "."}
Z_975 = 1.959963984540054
EPS = 1e-14


@dataclass(frozen=True)
class ContinuousSummary:
    n: int
    missing: int
    mean: float | None
    sd: float | None
    median: float | None
    q1: float | None
    q3: float | None
    minimum: float | None
    maximum: float | None


def is_missing(value: Any) -> bool:
    if value is None:
        return True
    return str(value).strip().lower() in MISSING_TOKENS


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit("Input CSV has no header row.")
        rows = [dict(row) for row in reader]
    return list(reader.fieldnames), rows


def parse_var_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def require_columns(columns: Iterable[str], required: Iterable[str]) -> None:
    missing = [col for col in required if col and col not in columns]
    if missing:
        raise SystemExit(f"Missing required columns: {', '.join(missing)}")


def to_float(value: str) -> float | None:
    if is_missing(value):
        return None
    try:
        parsed = float(str(value).replace(",", ""))
    except ValueError:
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * pct
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[int(rank)]
    weight = rank - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def summarize_continuous(rows: list[dict[str, str]], var: str) -> ContinuousSummary:
    values = [to_float(row.get(var, "")) for row in rows]
    nums = [value for value in values if value is not None]
    missing = len(values) - len(nums)
    if not nums:
        return ContinuousSummary(0, missing, None, None, None, None, None, None, None)
    mean = statistics.fmean(nums)
    sd = statistics.stdev(nums) if len(nums) > 1 else None
    return ContinuousSummary(
        n=len(nums),
        missing=missing,
        mean=mean,
        sd=sd,
        median=percentile(nums, 0.50),
        q1=percentile(nums, 0.25),
        q3=percentile(nums, 0.75),
        minimum=min(nums),
        maximum=max(nums),
    )


def summarize_categorical(rows: list[dict[str, str]], var: str) -> dict[str, Any]:
    values = [row.get(var, "") for row in rows]
    observed = [str(value).strip() for value in values if not is_missing(value)]
    counts = Counter(observed)
    total = sum(counts.values())
    levels = []
    for level, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        levels.append({"level": level, "n": count, "percent": safe_percent(count, total)})
    return {"n": total, "missing": len(values) - total, "levels": levels}


def safe_percent(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return 100.0 * numerator / denominator


def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def betacf(a: float, b: float, x: float) -> float:
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < EPS:
        d = EPS
    d = 1.0 / d
    h = d
    for m in range(1, 201):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < EPS:
            d = EPS
        c = 1.0 + aa / c
        if abs(c) < EPS:
            c = EPS
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < EPS:
            d = EPS
        c = 1.0 + aa / c
        if abs(c) < EPS:
            c = EPS
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-7:
            break
    return h


def regularized_beta(x: float, a: float, b: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x)
        + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t_stat: float, df: float) -> float | None:
    if df <= 0 or math.isnan(t_stat):
        return None
    x = df / (df + t_stat * t_stat)
    return min(1.0, max(0.0, regularized_beta(x, df / 2.0, 0.5)))


def gammaincc(a: float, x: float) -> float:
    if x < 0.0 or a <= 0.0:
        return math.nan
    if x == 0.0:
        return 1.0
    if x < a + 1.0:
        ap = a
        delta = 1.0 / a
        summation = delta
        for _ in range(1, 1000):
            ap += 1.0
            delta *= x / ap
            summation += delta
            if abs(delta) < abs(summation) * 1e-14:
                break
        gammp = summation * math.exp(-x + a * math.log(x) - math.lgamma(a))
        return max(0.0, min(1.0, 1.0 - gammp))
    b = x + 1.0 - a
    c = 1.0 / EPS
    d = 1.0 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < EPS:
            d = EPS
        c = b + an / c
        if abs(c) < EPS:
            c = EPS
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-14:
            break
    return max(0.0, min(1.0, h * math.exp(-x + a * math.log(x) - math.lgamma(a))))


def chi_square_p(chi2: float, df: int) -> float | None:
    if df <= 0:
        return None
    return gammaincc(df / 2.0, chi2 / 2.0)


def welch_t_test(group_a: list[float], group_b: list[float]) -> dict[str, Any]:
    n1, n2 = len(group_a), len(group_b)
    if n1 < 2 or n2 < 2:
        return {"test": "Welch t-test", "status": "insufficient data"}
    mean1, mean2 = statistics.fmean(group_a), statistics.fmean(group_b)
    var1, var2 = statistics.variance(group_a), statistics.variance(group_b)
    se2 = var1 / n1 + var2 / n2
    if se2 <= 0:
        return {"test": "Welch t-test", "status": "zero variance"}
    t_stat = (mean1 - mean2) / math.sqrt(se2)
    df_num = se2 * se2
    df_den = (var1 * var1) / (n1 * n1 * (n1 - 1)) + (var2 * var2) / (n2 * n2 * (n2 - 1))
    df = df_num / df_den if df_den > 0 else math.nan
    p_value = t_two_sided_p(t_stat, df)
    return {
        "test": "Welch t-test",
        "status": "ok",
        "n_by_group": [n1, n2],
        "mean_difference": mean1 - mean2,
        "t": t_stat,
        "df": df,
        "p_value": p_value,
    }


def grouped_values(rows: list[dict[str, str]], group_var: str, value_var: str) -> dict[str, list[float]]:
    groups: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        group = row.get(group_var, "")
        value = to_float(row.get(value_var, ""))
        if not is_missing(group) and value is not None:
            groups[str(group).strip()].append(value)
    return dict(sorted(groups.items()))


def categorical_table(rows: list[dict[str, str]], group_var: str, var: str) -> dict[str, Any]:
    group_levels = sorted({str(row.get(group_var, "")).strip() for row in rows if not is_missing(row.get(group_var, ""))})
    var_levels = sorted({str(row.get(var, "")).strip() for row in rows if not is_missing(row.get(var, ""))})
    matrix = []
    for group in group_levels:
        matrix.append([
            sum(
                1
                for row in rows
                if str(row.get(group_var, "")).strip() == group and str(row.get(var, "")).strip() == level
            )
            for level in var_levels
        ])
    return {"group_levels": group_levels, "variable_levels": var_levels, "counts": matrix}


def chi_square_test(matrix: list[list[int]]) -> dict[str, Any]:
    rows_n = len(matrix)
    cols_n = len(matrix[0]) if matrix else 0
    if rows_n < 2 or cols_n < 2:
        return {"test": "Chi-square test", "status": "requires at least 2x2 table"}
    row_totals = [sum(row) for row in matrix]
    col_totals = [sum(matrix[r][c] for r in range(rows_n)) for c in range(cols_n)]
    total = sum(row_totals)
    if total == 0:
        return {"test": "Chi-square test", "status": "empty table"}
    chi2 = 0.0
    min_expected = math.inf
    for r in range(rows_n):
        for c in range(cols_n):
            expected = row_totals[r] * col_totals[c] / total
            min_expected = min(min_expected, expected)
            if expected > 0:
                chi2 += (matrix[r][c] - expected) ** 2 / expected
    df = (rows_n - 1) * (cols_n - 1)
    return {
        "test": "Pearson chi-square test",
        "status": "ok",
        "chi_square": chi2,
        "df": df,
        "p_value": chi_square_p(chi2, df),
        "min_expected_cell": min_expected,
        "warning": "expected cell count below 5; prefer exact/simulation method" if min_expected < 5 else None,
    }


def hypergeom_probability(a: int, row1: int, col1: int, total: int) -> float:
    return math.exp(
        math.lgamma(row1 + 1)
        + math.lgamma(total - row1 + 1)
        + math.lgamma(col1 + 1)
        + math.lgamma(total - col1 + 1)
        - math.lgamma(total + 1)
        - math.lgamma(a + 1)
        - math.lgamma(row1 - a + 1)
        - math.lgamma(col1 - a + 1)
        - math.lgamma(total - row1 - col1 + a + 1)
    )


def fisher_exact_2x2(matrix: list[list[int]]) -> dict[str, Any]:
    if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
        return {"test": "Fisher exact test", "status": "requires 2x2 table"}
    a, b = matrix[0]
    c, d = matrix[1]
    row1 = a + b
    row2 = c + d
    col1 = a + c
    total = row1 + row2
    lower = max(0, col1 - row2)
    upper = min(row1, col1)
    observed = hypergeom_probability(a, row1, col1, total)
    p_two = 0.0
    for possible_a in range(lower, upper + 1):
        probability = hypergeom_probability(possible_a, row1, col1, total)
        if probability <= observed + 1e-12:
            p_two += probability
    return {
        "test": "Fisher exact test",
        "status": "ok",
        "p_value": min(1.0, p_two),
    }


def effect_estimates_2x2(matrix: list[list[int]]) -> dict[str, Any]:
    if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
        return {"status": "requires 2x2 table"}
    a, b = matrix[0]
    c, d = matrix[1]
    corrected = any(cell == 0 for row in matrix for cell in row)
    aa, bb, cc, dd = (a, b, c, d)
    if corrected:
        aa, bb, cc, dd = (a + 0.5, b + 0.5, c + 0.5, d + 0.5)
    risk1 = aa / (aa + bb)
    risk0 = cc / (cc + dd)
    odds_ratio = (aa * dd) / (bb * cc)
    log_or_se = math.sqrt(1 / aa + 1 / bb + 1 / cc + 1 / dd)
    risk_ratio = risk1 / risk0 if risk0 > 0 else None
    rr_ci = None
    if risk_ratio is not None:
        log_rr_se = math.sqrt((1 / aa) - (1 / (aa + bb)) + (1 / cc) - (1 / (cc + dd)))
        rr_ci = [math.exp(math.log(risk_ratio) - Z_975 * log_rr_se), math.exp(math.log(risk_ratio) + Z_975 * log_rr_se)]
    return {
        "status": "ok",
        "haldane_anscombe_correction": corrected,
        "risk_exposed": risk1,
        "risk_unexposed": risk0,
        "risk_difference": risk1 - risk0,
        "risk_ratio": risk_ratio,
        "risk_ratio_ci95": rr_ci,
        "odds_ratio": odds_ratio,
        "odds_ratio_ci95": [
            math.exp(math.log(odds_ratio) - Z_975 * log_or_se),
            math.exp(math.log(odds_ratio) + Z_975 * log_or_se),
        ],
    }


def missingness_table(rows: list[dict[str, str]], columns: list[str]) -> list[dict[str, Any]]:
    total = len(rows)
    table = []
    for column in columns:
        missing = sum(1 for row in rows if is_missing(row.get(column, "")))
        table.append({"variable": column, "missing": missing, "percent": safe_percent(missing, total)})
    return table


def round_floats(value: Any, digits: int) -> Any:
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return round(value, digits)
    if isinstance(value, dict):
        return {key: round_floats(val, digits) for key, val in value.items() if val is not None}
    if isinstance(value, list):
        return [round_floats(item, digits) for item in value]
    if hasattr(value, "__dict__"):
        return round_floats(value.__dict__, digits)
    return value


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    columns, rows = read_csv(Path(args.input))
    continuous = parse_var_list(args.continuous)
    categorical = parse_var_list(args.categorical)
    required = continuous + categorical + [args.group or ""]
    require_columns(columns, required)

    report: dict[str, Any] = {
        "metadata": {
            "input": str(args.input),
            "n_rows": len(rows),
            "n_columns": len(columns),
            "group": args.group,
            "determinism": "Python standard library only; deterministic sorting and no random resampling.",
            "limitations": [
                "No multivariable modeling is performed.",
                "Statistical tests are unadjusted and require protocol-level interpretation.",
                "For sparse RxC tables, use exact/simulation methods in a full statistics package.",
            ],
        },
        "missingness": missingness_table(rows, columns),
        "continuous": {var: summarize_continuous(rows, var) for var in continuous},
        "categorical": {var: summarize_categorical(rows, var) for var in categorical},
        "group_comparisons": {},
    }

    if args.group:
        group_levels = sorted({str(row.get(args.group, "")).strip() for row in rows if not is_missing(row.get(args.group, ""))})
        report["metadata"]["group_levels"] = group_levels
        comparisons: dict[str, Any] = {}
        for var in continuous:
            groups = grouped_values(rows, args.group, var)
            item: dict[str, Any] = {"groups": {key: summarize_continuous([{var: str(v)} for v in values], var) for key, values in groups.items()}}
            if len(groups) == 2:
                left, right = sorted(groups)
                item["comparison"] = welch_t_test(groups[left], groups[right])
                item["comparison"]["contrast"] = f"{left} minus {right}"
            else:
                item["comparison"] = {"status": "Welch t-test requires exactly 2 groups"}
            comparisons[var] = item
        for var in categorical:
            table = categorical_table(rows, args.group, var)
            table["chi_square"] = chi_square_test(table["counts"])
            if len(table["counts"]) == 2 and len(table["counts"][0]) == 2:
                table["fisher_exact"] = fisher_exact_2x2(table["counts"])
                table["effect_estimates"] = effect_estimates_2x2(table["counts"])
            comparisons[var] = table
        report["group_comparisons"] = comparisons

    return round_floats(report, args.digits)


def fmt(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def markdown_report(report: dict[str, Any]) -> str:
    lines = ["# Clinical Statistics Report", ""]
    meta = report["metadata"]
    lines.extend([
        f"- Input: `{meta['input']}`",
        f"- Rows: {meta['n_rows']}",
        f"- Columns: {meta['n_columns']}",
        f"- Group variable: {fmt(meta.get('group'))}",
        "",
        "## Missingness",
        "",
        "| Variable | Missing | Percent |",
        "|---|---:|---:|",
    ])
    for item in report["missingness"]:
        lines.append(f"| {item['variable']} | {item['missing']} | {fmt(item.get('percent'))} |")
    lines.extend(["", "## Continuous Variables", "", "| Variable | N | Missing | Mean | SD | Median | Q1 | Q3 | Min | Max |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"])
    for var, summary in report["continuous"].items():
        lines.append(
            f"| {var} | {summary['n']} | {summary['missing']} | {fmt(summary.get('mean'))} | {fmt(summary.get('sd'))} | "
            f"{fmt(summary.get('median'))} | {fmt(summary.get('q1'))} | {fmt(summary.get('q3'))} | {fmt(summary.get('minimum'))} | {fmt(summary.get('maximum'))} |"
        )
    lines.extend(["", "## Categorical Variables", ""])
    for var, summary in report["categorical"].items():
        lines.extend([f"### {var}", "", "| Level | N | Percent |", "|---|---:|---:|"])
        for level in summary["levels"]:
            lines.append(f"| {level['level']} | {level['n']} | {fmt(level.get('percent'))} |")
        lines.append("")
    if report.get("group_comparisons"):
        lines.extend(["## Group Comparisons", ""])
        for var, item in report["group_comparisons"].items():
            lines.extend([f"### {var}", "", "```json", json.dumps(item, ensure_ascii=False, indent=2), "```", ""])
    lines.extend(["## Interpretation Guardrails", ""])
    for limitation in meta["limitations"]:
        lines.append(f"- {limitation}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic clinical statistics for CSV files.")
    parser.add_argument("--input", required=True, help="Input CSV file.")
    parser.add_argument("--continuous", help="Comma-separated continuous variables.")
    parser.add_argument("--categorical", help="Comma-separated categorical variables.")
    parser.add_argument("--group", help="Optional grouping variable for table 1 comparisons.")
    parser.add_argument("--json-out", help="Write JSON report to this path.")
    parser.add_argument("--md-out", help="Write Markdown report to this path.")
    parser.add_argument("--digits", type=int, default=4, help="Decimal places for numeric output.")
    args = parser.parse_args()

    report = build_report(args)
    json_text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        Path(args.json_out).write_text(json_text, encoding="utf-8")
    if args.md_out:
        Path(args.md_out).write_text(markdown_report(report), encoding="utf-8")
    if not args.json_out and not args.md_out:
        print(json_text, end="")


if __name__ == "__main__":
    main()
