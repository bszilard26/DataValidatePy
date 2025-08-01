# DataValidatePy 🚀

&#x20;

A robust, enterprise‐style **Pytest**-based test automation project for the [Reqres.in public API](https://reqres.in/api-docs/), demonstrating industry best practices in API testing, CI/CD, and maintainable test architecture.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Structure](#test-structure)
- [CI/CD Integration](#cicd-integration)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

**DataValidatePy** is a modular, scalable test automation framework written in Python using Pytest. It targets the Reqres.in API and covers:

- **CRUD** operations on `/users` endpoints
- **Parameterized** and **data-driven** tests
- **Boundary** and **edge case** validation
- **Performance** (response-time) checks
- **Error-handling** scenarios (4XX/5XX codes)

This repo demonstrates:

- Clean **Fixture** design (`conftest.py`)
- Environment-based configuration via `.env`
- Custom **markers** for test categorization
- Integration with **GitHub Actions** for CI
- **CodeCov** integration for coverage reporting

---

## ✨ Features

- ✅ **Smoke**, **API**, **Error-handling**, **Slow**, and **Integration** test markers
- ✅ **JSON-schema** or contract checks (via `utils/`)
- ✅ **Parameterized** tests for multiple data scenarios
- ✅ **Timeout** fixtures and performance assertions
- ✅ **.env** support for configurable `BASE_URL`, `API_KEY`, etc.
- ✅ **GitHub Actions** multi-Python build matrix
- ✅ **Codecov** coverage badges

---

## 🔧 Prerequisites

- Python 3.9+ (3.10 or 3.11 recommended)
- [pipenv](https://pipenv.pypa.io) or `venv` for virtual environments
- [Docker](https://docker.com) & Docker Compose (optional, for containerized runs)
- GitHub account (for CI badges/secrets)

---

## 🛠 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<USERNAME>/DataValidatePy.git
   cd DataValidatePy
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Prepare environment variables**

   - Copy `.env.example` to `.env` and fill in your values:
     ```ini
     BASE_URL=https://reqres.in/api
     API_KEY=reqres-free-v1
     TIMEOUT=5
     ```

---

## 🚀 Running Tests

### Run the full suite

```bash
pytest --disable-warnings --maxfail=1
```

### Run by marker

```bash
pytest -m api
pytest -m smoke
pytest -m "not slow"
```

### Generate coverage report

```bash
pytest --cov=src --cov-report=html
# then open htmlcov/index.html
```

### Output JUnit-style XML (for CI)

```bash
pytest --junitxml=reports/junit.xml
```

---

## 📁 Test Structure

```
tests/
└── api/
    ├── users/
    │   ├── test_list.py
    │   ├── test_single.py
    │   ├── test_create.py
    │   └── test_error.py
    └── auth/
        ├── test_login.py
        └── test_register.py
```

- \`\`: fixtures for `base_url`, `headers`, `timeout`.
- \`\`: environment loader + constants.

---

## 🔄 CI/CD Integration

We use **GitHub Actions** to automate linting, security scans, and testing across Python versions.

- \`\`: Runs on `push`/`pull_request` for `main`, `develop`, and `feature/*`

  - **Lint** with `flake8` + `pre-commit`
  - **CodeQL** static analysis
  - **Test matrix** on Python 3.9/3.10/3.11
  - **Coverage** upload to Codecov

- \`\`: (Planned) Docker image build, tag, and push on `vX.Y.Z` tags, with staging deployment and notifications.

Badges in this README reflect live build and coverage status.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/XYZ`)
3. Commit changes with clear messages
4. Submit a Pull Request against `develop`
5. Ensure all CI checks pass

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with ❤️ by Test Automation GPT

