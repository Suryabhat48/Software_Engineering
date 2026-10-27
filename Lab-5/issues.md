# Lab 5: Static Code Analysis — Identified Issues & Fix Table

**Student Name:** SURYA A BHAT  
**SRN:** PES1UG24AM296  
**File Analyzed:** `car_rental.py`  
**Tools Used:** Bandit 1.9.4, Pylint 4.1.3, Flake8 7.4.1  

---

## 📊 Summary of Static Analysis Findings

| Tool | Focus Area | Before Fix Status | After Fix Status |
| :--- | :--- | :--- | :--- |
| **Bandit** | Security Vulnerabilities | 11 issues (2 High, 4 Medium, 5 Low) | **0 issues (No issues identified)** |
| **Pylint** | Code Quality & Logic | **4.94 / 10.00** (42 issues) | **10.00 / 10.00 (Perfect score)** |
| **Flake8** | PEP 8 Formatting & Style | 25 violations | **0 violations (Clean)** |

---

## 📋 Comprehensive Issue Documentation Table

Below is the structured table documenting the identified issues across all three static analysis tools, ordered by severity:

| Issue | Tool | Type / Code | Line(s)* | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SQL Injection (Insert)** | Bandit | Security (Medium) / `B608` | 23 | String formatting `%s` in SQL query allows arbitrary SQL injection during customer registration. | Replaced string interpolation with safe SQLite parameterized placeholder query `INSERT INTO customers VALUES (?, ?, ?)`. |
| **SQL Injection (Select)** | Bandit | Security (Medium) / `B608` | 26 | String concatenation `+ name +` in query allows attackers to bypass authentication and dump table data. | Replaced string concatenation with parameterized query `SELECT * FROM customers WHERE name = ?` passing `(name,)`. |
| **Arbitrary Code Execution** | Bandit / Pylint | Security (Medium) / `B102` (`W0122`) | 53 | Dynamic execution of arbitrary promo rules via `exec()` creates a critical remote code execution vulnerability. | Removed `exec()` completely; replaced with safe regex-based formula evaluation for arithmetic and percentage rules. |
| **Weak Cryptographic Hash** | Bandit | Security (High) / `B324` | 48 | Use of obsolete and insecure SHA-1 algorithm for hashing driving licence numbers. | Upgraded hash algorithm to industry-standard cryptographically secure `hashlib.sha256()`. |
| **Insecure Temporary File** | Bandit | Security (Medium) / `B306` | 63 | `tempfile.mktemp()` is deprecated and vulnerable to race conditions (TOCTOU attacks). | Replaced with `tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")` ensuring atomic, secure file creation. |
| **Overly Permissive File Permissions** | Bandit | Security (High) / `B103` | 67 | Chmod set to `0o777` grants read, write, and execute permissions to all users on the system. | Changed file permissions to restrictive `0o600` (read/write access restricted solely to the file owner). |
| **Hardcoded Admin Password** | Bandit | Security (Low) / `B105`, `B107` | 70-71 | Plaintext password `'admin@rent'` hardcoded in function signature default arguments and comparison. | Removed password default arguments; retrieved credentials from environment variables (`ADMIN_USER`, `ADMIN_PASSWORD`). |
| **Assert in Production Code** | Bandit | Security (Low) / `B101` | 30 | `assert` statement used for input validation; gets completely disabled when Python runs with optimization flags (`-O`). | Replaced `assert` with explicit control flow and raised standard `ValueError("Customer not registered")`. |
| **Broad Exception & Silent Pass** | Bandit / Flake8 / Pylint | Bug / `B110`, `E722`, `W0702` | 41-42 | Bare `except:` statement with `pass` silently swallows all exceptions, including `KeyboardInterrupt` and fatal errors. | Removed bare except; added explicit dictionary membership validation (`if plate not in fleet: return 0`). |
| **Insecure Random Generator** | Bandit | Security (Low) / `B311` | 45 | Pseudo-random `random.randint()` is predictable and unsuitable for security-sensitive booking identifiers. | Switched to cryptographically secure `secrets.randbelow(90000) + 10000`. |
| **Mutable Default Argument** | Pylint | Bug / `W0102` | 16 | Mutable list `features=[]` in function signature is shared across all function calls, leading to data bleeding across cars. | Changed default parameter to `features=None` and dynamically initialized `features = []` inside the function body. |
| **Missing Module & Function Docstrings** | Pylint | Quality / `C0114`, `C0116` | 1, 16-82 | Lack of docstrings makes code undocumented and fails maintainability standards. | Added comprehensive PEP 257 docstrings for the module and every function explaining arguments and behavior. |
| **Non-conforming Naming Convention** | Pylint | Style / `C0103` | 16-75 | Function names used `camelCase` (`addCar`, `rentCar`, etc.) violating PEP 8 snake_case standards. | Renamed all functions to clean `snake_case` (`add_car`, `rent_car`, `register_customer`, etc.). |
| **Inconsistent Return Statements** | Pylint | Design / `R1710` | 16, 36 | Functions returned values on some paths and implicitly returned `None` on others. | Ensured all code paths return consistent types (e.g. dictionary or `None`, integer fee or `0`). |
| **Unused Import** | Pylint / Flake8 | Quality / `W0611`, `F401` | 2 | `import json` was imported at the top of the file but never used anywhere in the codebase. | Removed unused `json` import to declutter namespace and optimize module loading. |
| **Singleton & Dict Iteration Inefficiencies** | Pylint / Flake8 | Quality / `C0121`, `C0206`, `E712` | 77-78 | `if fleet[p]['available'] == True` compared singleton with `==`, and iterated keys rather than items. | Refactored to idiomatic list comprehension: `[p for p, c in fleet.items() if c.get('available')]`. |
| **Missing Resource Management & Encoding** | Pylint | Bug / `R1732`, `W1514` | 64 | `open(path, "w")` without context manager leaked file handles on error and omitted explicit encoding. | Wrapped file access in `with open(...) as temp_file:` specifying explicit `encoding="utf-8"`. |
| **Line Length & Spacing Violations** | Flake8 | Style / `E501`, `E302`, `E305` | Multiple | Lines exceeded 79 characters and lacked 2 blank lines separating top-level function definitions. | Refactored lines to < 79 characters and enforced standard 2 blank lines between all top-level functions. |

*\*Line numbers reference the original uncleaned `car_rental.py`.*
