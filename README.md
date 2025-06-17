# AI Insights Charts

![CI/CD Pipeline](https://github.com/your-username/ai-insights-charts/workflows/CI/CD%20Pipeline/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A comprehensive SQLite database project for managing AI model insights and charts data.

## 🚀 Features

- **Automated Database Setup**: Scripts to automatically create and populate SQLite databases from SQL files
- **Data Validation**: Comprehensive testing suite to ensure data integrity
- **PostgreSQL to SQLite Conversion**: Automatic conversion of PostgreSQL syntax to SQLite-compatible format
- **CI/CD Pipeline**: Automated testing, validation, and deployment using GitHub Actions

## 📋 Requirements

- Python 3.8 or higher
- No external dependencies required (uses only Python standard library)

## 🛠️ Installation & Usage

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/your-username/ai-insights-charts.git
cd ai-insights-charts
```

2. Set up the database:
```bash
cd db
python setup_database.py
```

3. Test the database:
```bash
python test_database.py
```

4. Run query examples:
```bash
python query_examples.py
```

### Development Environment

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run code formatting:
```bash
black .
isort .
```

3. Run linting:
```bash
flake8 .
```

4. Run tests:
```bash
pytest
```

## 🗂️ Project Structure

```
ai-insights-charts/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline configuration
├── db/
│   ├── setup_database.py       # Database setup script
│   ├── test_database.py        # Database testing script
│   ├── query_examples.py       # Example queries
│   └── README.md               # Database documentation
├── data/
│   └── models/                 # SQL files for data models
├── requirements.txt            # Python dependencies
├── pytest.ini                 # Pytest configuration
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## 🤖 CI/CD Pipeline

The project includes a comprehensive GitHub Actions CI/CD pipeline that:

### 🧪 Testing Jobs

- **Multi-Python Testing**: Tests across Python 3.8, 3.9, 3.10, and 3.11
- **Code Quality**: Runs flake8, black, and isort checks
- **Database Validation**: Tests database setup and data integrity
- **Coverage Reporting**: Generates code coverage reports

### 🔒 Security Jobs

- **Vulnerability Scanning**: Uses Trivy to scan for security vulnerabilities
- **SARIF Upload**: Uploads security scan results to GitHub Security tab

### 📦 Build Jobs

- **Artifact Creation**: Builds production database on main branch pushes
- **Release Automation**: Creates GitHub releases with database artifacts when tags are pushed

### Pipeline Triggers

- **Push Events**: Runs on pushes to `main` and `develop` branches
- **Pull Requests**: Runs on PRs targeting `main` and `develop` branches
- **Tag Events**: Creates releases when version tags are pushed

## 📊 Database Schema

The database contains AI model information including:

- Model names and organizations
- Publication dates and parameter counts
- Frontier model classifications
- Performance metrics and benchmarks

See `db/README.md` for detailed database documentation.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and ensure tests pass
4. Run code formatting: `black . && isort .`
5. Commit your changes: `git commit -am 'Add your feature'`
6. Push to the branch: `git push origin feature/your-feature`
7. Create a Pull Request

## 📈 Monitoring & Quality

- **Code Coverage**: Maintained above 80%
- **Security Scanning**: Automated vulnerability detection
- **Code Quality**: Enforced through automated linting and formatting
- **Multi-Platform Testing**: Tested across multiple Python versions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/aidoge-lab/ai-insights-charts/issues) page
2. Review the database documentation in `db/README.md`
3. Create a new issue with detailed information about your problem

## 🎯 Roadmap

---
