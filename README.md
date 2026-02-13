# Selenium WebDriver Automation Demo

Automated test suite using Python, Selenium WebDriver, and Pytest. The project demonstrates fundamental web UI automation capabilities with Page Object Model (POM) design pattern implementation.

## Project Goal

Gain practical Selenium WebDriver experience through testing a real web application, applying modern QA automation best practices.

## Technology Stack

- **Python** 3.13
- **Selenium WebDriver** 4.x - Browser automation
- **Pytest** - Test framework and execution
- **WebDriver Manager** - Automatic driver management
- **Page Object Model** - Design pattern for code reusability

## Tested Features

### Login Tests
- Successful login with valid credentials
- Failed login with invalid password
- Locked user login attempt
- Empty fields login attempt

### Shopping Cart Tests
- Add single item to cart
- Add multiple items
- Cart badge dynamic update
- Remove item from cart
- Cart inspection to see if contains item
- Checkout process

## Installation and Execution

### Prerequisites
- Python 3.8 or newer
- Chrome browser

### 1. Clone the repository
```bash
git clone https://github.com/csokanandor95/selenium-automation-demo.git
cd selenium-automation-demo
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run tests
```bash
# Run all tests
pytest tests/ -v

# Run only login tests
pytest tests/test_login_pom.py -v

# Run only shopping tests
pytest tests/test_shopping_pom.py -v

# Generate HTML report after running tests
pytest tests/ --html=report.html --self-contained-html
```

## Project Structure
```
selenium-automation-demo/
│
├── tests/                      # Test files
│   ├── test_login.py          # Basic login tests
│   ├── test_shopping.py       # Basic shopping tests
│   ├── test_login_pom.py      # Login tests with POM
│   └── test_shopping_pom.py   # Shopping tests with POM
│
├── pages/                      # Page Object Model classes
│   ├── base_page.py           # Base page class
│   ├── login_page.py          # Login page object
│   └── products_page.py       # Products page object
│
├── utils/                      # Utility files
│
├── screenshots/                # Test result screenshots
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
└── README.md                   # Project documentation
```

## Applied Concepts

### Page Object Model (POM)
The project demonstrates the use of Page Object Model design pattern:
- **Separation of concerns**: Each page has its own class
- **Code reusability**: Common operations in base_page.py
- **Easy maintenance**: UI changes only needed in one place

### Best Practices
- Explicit and implicit wait strategies
- Pytest fixtures for setup/teardown management
- Descriptive test names and docstrings
- Assertion messages for detailed error reporting
- WebDriver Manager - no manual driver installation needed

## Demo Website

Tests run on: [SauceDemo](https://www.saucedemo.com)

## Learning Outcomes

Skills acquired during project development:
- Selenium WebDriver basics (locators, actions, waits)
- Pytest test framework usage
- Page Object Model implementation
- Git version control and GitHub usage
- Test automation best practices

## Future Enhancements

- [ ] Cross-browser testing (Firefox, Edge)
- [ ] CI/CD integration (GitHub Actions)
- [ ] Screenshot capture on test failure
- [ ] Data-driven tests (CSV/JSON)
- [ ] Advanced reporting (other than pytest-html)

## Author

**[Your Name]**
- GitHub: [@csokanandor95](https://github.com/csokanandor95)
- LinkedIn: [linkedin.com/in/your-profile](https://www.linkedin.com/in/n%C3%A1ndor-cs%C3%B3ka-ba76171a2/)

## License

This is a learning/portfolio project.