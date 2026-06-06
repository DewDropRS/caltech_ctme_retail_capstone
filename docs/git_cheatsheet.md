# Git Cheat Sheet

A workflow-based reference for the most common Git commands.
For commit message conventions, see `conventional_commits_guide.md`.

---

## One-Time Setup

```bash
# Initialize a new repo in the current folder
git init

# Set your identity (first time only)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Connect local repo to a remote GitHub repo
git remote add origin https://github.com/username/repo-name.git

# Rename default branch to main and push for the first time
git branch -M main
git push -u origin main
```

> The `-u` flag only needs to be used once — it sets the upstream tracking.
> After that, `git push` is enough.

---

## Cloning an Existing Repo

```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

---

## The Working Session Loop

### 1. Pull before starting (sync with remote)

```bash
git pull origin main
```

Always pull first if you've worked from another machine or Codespaces.

---

### 2. Check what changed

```bash
# See which files were modified, added, or deleted
git status

# See the actual line-by-line changes (unstaged)
git diff

# See changes in a specific file
git diff src/data_cleaning.py
```

---

### 3. Stage your changes

```bash
# Stage a specific file
git add src/data_cleaning.py

# Stage all changed files at once
git add .

# Stage specific lines within a file (interactive)
git add -p src/data_cleaning.py
```

---

### 4. Review what is staged

```bash
# See staged changes before committing
git diff --staged

# See staged changes in a specific file
git diff --staged src/data_cleaning.py
```

---

### 5. Commit

```bash
# Simple commit
git commit -m "feat: add RFM quartile scoring"

# Commit with body (multiple -m flags)
git commit -m "feat: complete K-Means module" \
           -m "- add elbow method with distortion and WCSS" \
           -m "- add silhouette scoring for k validation" \
           -m "- add cluster profile heatmap"

# Skip git add for already-tracked files (not new files)
git commit -am "fix: correct CSV index export"
```

---

### 6. Push to GitHub

```bash
git push origin main

# Or simply (once upstream is set)
git push
```

---

### Rinse and repeat steps 2–6 for each logical unit of work.

---

## Viewing History

```bash
# One-line summary of all commits
git log --oneline

# Full details of the last commit
git log -1

# Full diff of the last commit
git log -1 -p

# Show all commits for a specific file
git log --oneline src/data_cleaning.py
```

---

## Fixing Mistakes

```bash
# Amend the last commit message (before pushing)
git commit --amend -m "corrected message"

# Amend the last commit message (after pushing — use carefully)
git commit --amend -m "corrected message"
git push --force origin main

# Undo the last commit but keep changes locally
git reset HEAD~1

# Untrack a file without deleting it locally
git rm --cached filename.py
```

---

## Remote Management

```bash
# View current remote URL
git remote -v

# Change remote URL (e.g. after a typo)
git remote set-url origin https://github.com/username/correct-repo.git
```

---

## Branching (Basic)

```bash
# Create and switch to a new branch
git checkout -b feature/my-new-feature

# Switch back to main
git checkout main

# List all branches
git branch

# Merge a branch into main
git merge feature/my-new-feature

# Delete a branch after merging
git branch -d feature/my-new-feature
```

---

## .gitignore Quick Reference

Files and folders listed in `.gitignore` are never tracked by Git.

```
# Common entries for Python data science projects
.venv/
__pycache__/
*.pyc
data/
outputs/
*.joblib
*.pkl
.env
.idea/
.pytest_cache/
```

Add a file to `.gitignore` after accidentally tracking it:
```bash
git rm --cached filename
```

---

## Resources

- Official docs: https://git-scm.com/doc
- Interactive practice: https://learngitbranching.js.org
- Conventional commits: see `conventional_commits_guide.md`