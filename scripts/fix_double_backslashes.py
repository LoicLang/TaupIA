#!/usr/bin/env python3
"""
Passe 1: Fix double-escaped backslashes in exercise JSON files.

In correct JSON: "\\mathbb{R}" → parsed as \mathbb{R} (valid LaTeX)
In broken JSON:  "\\\\mathbb{R}" → parsed as \\mathbb{R} (KaTeX sees \\ + mathbb = broken)

This script fixes the broken case by replacing \\command with \command
for known LaTeX commands in all string fields of exercise JSON files.
"""

import json
import re
import os
import sys
from pathlib import Path

# Known LaTeX commands (sorted longest-first for correct matching)
LATEX_COMMANDS = sorted([
    # Arrows
    'longrightarrow', 'longleftarrow', 'longmapsto', 'Leftrightarrow',
    'hookrightarrow', 'twoheadrightarrow', 'rightarrow', 'leftarrow',
    'leftrightarrow', 'Rightarrow', 'Leftarrow', 'mapsto', 'to',
    # Font commands
    'operatorname', 'DeclareMathOperator',
    'displaystyle', 'textstyle', 'scriptstyle',
    'mathbb', 'mathcal', 'mathscr', 'mathrm', 'mathbf', 'mathit',
    'textbf', 'textit', 'textrm', 'texttt', 'text',
    # Decorations
    'overline', 'underline', 'widehat', 'widetilde',
    'vec', 'hat', 'bar', 'tilde', 'dot', 'ddot',
    # Limits and big ops
    'limsup', 'liminf', 'lim',
    'sum', 'prod', 'int', 'iint', 'iiint', 'oint',
    'bigcup', 'bigcap', 'bigoplus', 'bigotimes',
    'sup', 'inf', 'max', 'min', 'det', 'dim', 'ker', 'rank', 'im',
    # Trig and functions
    'arcsin', 'arccos', 'arctan',
    'sin', 'cos', 'tan', 'cot', 'sec', 'csc',
    'ln', 'log', 'exp',
    # Fractions and roots
    'frac', 'dfrac', 'tfrac', 'binom', 'sqrt', 'root',
    # Greek letters
    'varepsilon', 'varphi', 'varnothing',
    'alpha', 'beta', 'gamma', 'Gamma', 'delta', 'Delta',
    'epsilon', 'zeta', 'eta', 'theta', 'Theta',
    'iota', 'kappa', 'lambda', 'Lambda', 'mu', 'nu',
    'xi', 'Xi', 'pi', 'Pi', 'rho', 'sigma', 'Sigma',
    'tau', 'phi', 'Phi', 'chi', 'psi', 'Psi', 'omega', 'Omega',
    # Relations
    'subseteq', 'supseteq', 'subsetneq',
    'subset', 'supset', 'cup', 'cap', 'in', 'notin', 'ni',
    'leq', 'geq', 'neq', 'le', 'ge', 'ne',
    'sim', 'simeq', 'equiv', 'approx', 'cong', 'perp',
    'mid', 'nmid', 'parallel',
    'forall', 'exists',
    # Logic
    'implies', 'iff', 'therefore', 'because',
    'neg', 'land', 'lor', 'wedge', 'vee', 'not',
    'models', 'vdash', 'top', 'bot',
    # Misc math
    'infty', 'times', 'cdot', 'cdots', 'ldots', 'dots', 'vdots', 'ddots',
    'partial', 'nabla', 'grad',
    'oplus', 'otimes', 'circ', 'bullet', 'star', 'ast',
    'setminus', 'emptyset',
    # Spacing
    'quad', 'qquad', 'hspace', 'vspace', 'hfill',
    # Delimiters
    'left', 'right', 'bigl', 'bigr', 'Bigl', 'Bigr',
    # Environments
    'begin', 'end', 'item',
    'pmatrix', 'bmatrix', 'vmatrix', 'Vmatrix', 'cases',
    'itemize', 'enumerate',
    # Formatting
    'par', 'hline', 'cline',
], key=len, reverse=True)

# Build regex pattern:
# Match TWO backslashes followed by a known command name, not preceded by another backslash
# In Python strings after JSON parsing:
#   \\mathbb = two chars: \, \, m, a, t, h, b, b (BROKEN - double backslash)
#   \mathbb = one char: \, m, a, t, h, b, b (CORRECT - single backslash)
COMMANDS_RE = '|'.join(re.escape(c) for c in LATEX_COMMANDS)
DOUBLE_BS_PATTERN = re.compile(
    r'(?<!\\)\\\\(' + COMMANDS_RE + r')(?![a-zA-Z])'
)


def fix_double_backslashes(s: str) -> str:
    """Replace \\command with \command for known LaTeX commands."""
    if not isinstance(s, str):
        return s
    # Keep applying until no more double backslashes (handles triple+ escaping)
    prev = None
    while prev != s:
        prev = s
        s = DOUBLE_BS_PATTERN.sub(lambda m: '\\' + m.group(1), s)
    return s


def walk_and_fix(obj, path="", changes=None):
    """Recursively walk JSON and fix all string values."""
    if changes is None:
        changes = []

    if isinstance(obj, str):
        fixed = fix_double_backslashes(obj)
        if fixed != obj:
            changes.append((path, obj, fixed))
        return fixed, changes

    if isinstance(obj, list):
        new_list = []
        for i, item in enumerate(obj):
            fixed_item, changes = walk_and_fix(item, f"{path}[{i}]", changes)
            new_list.append(fixed_item)
        return new_list, changes

    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            fixed_value, changes = walk_and_fix(value, f"{path}.{key}", changes)
            new_dict[key] = fixed_value
        return new_dict, changes

    return obj, changes


def process_file(filepath: Path) -> list:
    """Process a single exercise JSON file. Returns list of changes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_data, changes = walk_and_fix(data)

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, ensure_ascii=False, indent=2)
            f.write('\n')

    return changes


def main():
    exercises_dir = Path(__file__).parent.parent / 'data' / 'exercices'

    if not exercises_dir.exists():
        print(f"ERROR: Directory not found: {exercises_dir}")
        sys.exit(1)

    json_files = sorted(exercises_dir.glob('*.json'))
    print(f"Scanning {len(json_files)} exercise files...\n")

    total_changes = 0
    files_changed = 0

    for filepath in json_files:
        changes = process_file(filepath)
        if changes:
            files_changed += 1
            total_changes += len(changes)
            print(f"  {filepath.name}: {len(changes)} fixes")
            for path, old, new in changes[:3]:  # Show first 3 examples
                # Truncate for display
                old_short = old[:80] + '...' if len(old) > 80 else old
                new_short = new[:80] + '...' if len(new) > 80 else new
                print(f"    {path}:")
                print(f"      OLD: {repr(old_short)}")
                print(f"      NEW: {repr(new_short)}")
            if len(changes) > 3:
                print(f"    ... and {len(changes) - 3} more fixes")
            print()

    print(f"{'='*60}")
    print(f"SUMMARY: {total_changes} fixes in {files_changed} files (out of {len(json_files)} total)")

    if total_changes == 0:
        print("No double-backslash issues found!")


if __name__ == '__main__':
    main()
