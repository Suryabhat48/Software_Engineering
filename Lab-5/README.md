# Lab 5: Static Code Analysis — Car Rental System

**Student Name:** SURYA A BHAT  
**SRN:** PES1UG24AM296  
**Course:** Software Engineering (UE24CS252AA / Lab 5)  
**Assigned Source Repository:** [SETAPESU26/L5_56_car-rental](https://github.com/SETAPESU26/L5_56_car-rental)  
**Target Submission Repository:** [Suryabhat48/Software_Engineering](https://github.com/Suryabhat48/Software_Engineering)  

---

## 🎯 Lab Objectives & Score Summary

The goal of this lab is to utilize static code analysis tools (**Pylint**, **Bandit**, and **Flake8**) to detect, diagnose, document, and eliminate security vulnerabilities, logical bugs, and style violations from an assigned Python script (`car_rental.py`).

### 📈 Static Analysis Score Card

| Tool | Focus Area | Before Refactoring | After Refactoring | Target Requirement | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bandit** | Security Analysis | **11 issues** (2 High, 4 Medium, 5 Low) | **0 issues (Clean)** | Zero security issues | ✅ **PASSED** |
| **Pylint** | Code Quality & Logic | **4.94 / 10.00** (42 issues) | **10.00 / 10.00** | Score > 9.5 / 10.0 | ✅ **PASSED (10.00/10)** |
| **Flake8** | PEP 8 Formatting | **25 violations** | **0 violations (Clean)** | Zero style violations | ✅ **PASSED** |

---

## 📂 Deliverables Directory Structure

All required lab deliverables are organized under the `Lab-5/` directory:

```text
Lab-5/
├── car_rental.py                  # Cleaned, fully refactored, and secure Python script
├── issues.md                      # Detailed table of all identified issues, line numbers, and fixes
├── reflection.md                  # Answers to all four static code analysis reflection questions
├── README.md                      # Comprehensive lab overview and execution guide
├── pylint_report_before.txt       # Initial Pylint report (Score: 4.94/10)
├── pylint_report_after.txt        # Final Pylint report (Score: 10.00/10)
├── bandit_report_before.txt       # Initial Bandit report (11 issues found)
├── bandit_report_after.txt        # Final Bandit report (0 issues found)
├── flake8_report_before.txt       # Initial Flake8 report (25 violations)
├── flake8_report_after.txt        # Final Flake8 report (0 violations)
├── reports/                       # Nested folder with reports partitioned by phase
│   ├── before/
│   │   ├── pylint_report.txt
│   │   ├── bandit_report.txt
│   │   └── flake8_report.txt
│   └── after/
│       ├── pylint_report.txt
│       ├── bandit_report.txt
│       └── flake8_report.txt
├── pylint_report.txt              # Standard root copy of final Pylint report
├── bandit_report.txt              # Standard root copy of final Bandit report
└── flake8_report.txt              # Standard root copy of final Flake8 report
```

---

## 🛠️ Step-by-Step Task & Commit Breakdown

Per the lab handout instructions (*"3 Commits for changes you made for fixing the issues raised by three tools"*), independent, dedicated commits were created for each phase:

1. **Baseline Commit:**
   - Saved original `car_rental.py` and captured initial baseline reports (`*_before.txt`).
2. **Commit 1 (Bandit Fixes):**
   - Fixed SQL injection vulnerabilities in customer registration and search via parameterized queries (`B608`).
   - Removed arbitrary code execution `exec()` in promo rule application (`B102`).
   - Upgraded weak SHA-1 licence hashing to SHA-256 (`B324`).
   - Replaced insecure `tempfile.mktemp()` with `tempfile.NamedTemporaryFile` (`B306`).
   - Replaced permissive file permissions `0o777` with restrictive `0o600` (`B103`).
   - Removed hardcoded administrative credentials and default arguments (`B105`, `B107`).
   - Replaced `assert` with explicit exception raising `ValueError` (`B101`).
   - Switched to cryptographically secure `secrets` module (`B311`).
3. **Commit 2 (Pylint Fixes - Score 10.00/10):**
   - Eliminated dangerous mutable default argument `features=[]` by using `features=None` (`W0102`).
   - Replaced bare `except:` with explicit error handling (`W0702`).
   - Added complete PEP 257 docstrings to module and all functions (`C0114`, `C0116`).
   - Converted function names to PEP 8 standard `snake_case` (`C0103`).
   - Removed unused import `json` (`W0611`).
   - Enforced consistent return statements across all execution branches (`R1710`).
   - Optimized dictionary iteration and singleton checks (`C0206`, `C0121`).
   - Converted string formatting to modern Python f-strings (`C0209`).
4. **Commit 3 (Flake8 Formatting & Documentation):**
   - Enforced maximum line length (<79 characters) across the entire script (`E501`).
   - Standardized 2 blank lines between all top-level functions (`E302`, `E305`).
   - Generated final `*_after.txt` reports for all three tools.
   - Authored complete `issues.md` documentation table and `reflection.md` report.

---

## 🚀 How to Run and Verify

### 1. Execute the Program
```bash
python car_rental.py
```

### 2. Verify with Bandit
```bash
python -m bandit -r car_rental.py
```
*(Result: No issues identified)*

### 3. Verify with Pylint
```bash
python -m pylint car_rental.py
```
*(Result: 10.00 / 10.00)*

### 4. Verify with Flake8
```bash
python -m flake8 car_rental.py
```
*(Result: 0 errors / clean exit)*
