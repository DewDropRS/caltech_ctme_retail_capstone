# Conventional Commits Guide

A standardized format for Git commit messages that makes history readable and
searchable. Widely adopted in professional software development.

---

## Format

```
<type>(<optional scope>): <short description>

<optional body>

<optional footer>
```

---

## Commit Types

| Type | When to Use |
|------|-------------|
| `feat` | Adding a new feature or function |
| `fix` | Fixing a bug |
| `config` | Changes to configuration files |
| `refactor` | Restructuring code without changing behavior |
| `docs` | Documentation changes (README, guides, comments) |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks (dependencies, gitignore, etc.) |
| `style` | Formatting changes, no logic change |
| `perf` | Performance improvements |
| `ci` | CI/CD pipeline changes |

---

## Examples

### Simple one-line commit

```
feat: add RFM quartile scoring function
```

### With scope (optional — identifies the module or area)

```
feat(rfm): add quartile scoring with duplicates='drop'
fix(data_cleaning): handle NaN in StockCode before regex match
docs(readme): add conventional commits guide
```

### With body for complex changes

```
feat: complete K-Means clustering pipeline

- add prepare_features with log transform and StandardScaler
- add compute_elbow_metrics with distortion, WCSS, silhouette
- add train_final_model with joblib serialization
- add build_cluster_profile and heatmap visualization
```

---

## Rules

- Subject line under 72 characters
- Use present tense — "add feature" not "added feature"
- No period at the end of the subject line
- First `-m` flag is the subject, subsequent `-m` flags are the body
- Keep subject line descriptive but concise

---

## Running in Terminal

### Simple commit

```bash
git commit -m "feat: add SHAP beeswarm plot by cluster"
```

### With body using multiple `-m` flags

```bash
git commit -m "feat: complete SHAP explainer module" \
           -m "- build_shap_explainer trains XGBoost on cluster labels" \
           -m "- compute_shap_values returns list of numpy arrays" \
           -m "- plot_shap_summary saves beeswarm per cluster" \
           -m "- plot_shap_bar saves mean absolute SHAP bar chart"
```

---

## Common Mistakes

| Mistake | Instead |
|---------|---------|
| `git commit -m "fixed stuff"` | `fix(data_cleaning): remove duplicate index on CSV export` |
| `git commit -m "WIP"` | Commit only when a logical unit is complete |
| `git commit -m "Added the new feature for RFM scoring and also fixed the bug in cleaning and updated readme"` | Split into three separate commits |
| Using past tense: `"added feature"` | Use present tense: `"add feature"` |

---

## Amending the Last Commit

If you made a typo or forgot to include a file:

```bash
# Before pushing — safe to amend
git commit --amend -m "corrected message"

# After pushing — requires force push (use carefully on shared branches)
git commit --amend -m "corrected message"
git push --force origin main
```

---

## Viewing Commit History

```bash
# One-line summary
git log --oneline

# Full details of last commit
git log -1

# Full diff of last commit
git log -1 -p

# Diff of a specific file
git diff src/data_cleaning.py

# Diff of staged changes
git diff --staged src/data_cleaning.py
```

---

## Resources

- Official spec: https://www.conventionalcommits.org
- Angular convention (origin): https://github.com/angular/angular/blob/main/CONTRIBUTING.md