import pytest
import platform
from selenium import webdriver
from utilities.customLogger import LogGen

# ✅ Optional: Force plugin loading (not always necessary but helps Pytest 8+)
pytest_plugins = ["pytest_html", "pytest_metadata"]

# For session start/end log messages (optional)
@pytest.fixture(scope="session", autouse=True)
def setup_logging_once():
    logger = LogGen.loggen()
    logger.info("🔥 Pytest session started")
    yield
    logger.info("🧊 Pytest session finished")

# Actual fixture to use in test
@pytest.fixture
def logger():
    return LogGen.loggen()

@pytest.fixture()
def setup(request):
    browser = request.config.getoption("--browser").lower().strip()
    if browser == "chrome":
        driver = webdriver.Chrome()
        print("🚀 Launching Chrome browser...........")
    elif browser == "firefox":
        driver = webdriver.Firefox()
        print("🚀 Launching Firefox browser..........")
    else:
        raise ValueError(f"❌ Unsupported browser: {browser}")

    yield driver
    print("🔧 Closing browser")
    driver.quit()

def pytest_addoption(parser): # This will get the value from CLI/hooks
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests against: chrome or firefox")
    parser.addoption("--env", action="store", default="qa", help="Environment to run tests: qa/dev/staging/prod")

# PyTest- HTML Report

# Hook to add environment info to HTML report
# terminal -  pytest -s -v --html=Reports\report.html -n=2 --browser=chrome --env=qa testCases/test_login.py::Test_001_Login::test_homepageTitle
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # This will add metadata if pytest-html is installed and configured
    config._metadata = {
        "Environment": "QA",
        "Browser": "Chrome",
        "Build": "2025.06.15"
    }
    if hasattr(config, '_metadata'):
        config._metadata['Project Name'] = 'PyTest HybridFramework'
        config._metadata['Developer'] = 'Niraj Patel'
        config._metadata['Platform'] = platform.system()
        config._metadata['Python Version'] = platform.python_version()

        # Inject dynamic metadata (browser/environment)
        browser = config.getoption("--browser")
        env = config.getoption("--env")
        config._metadata['Browser'] = browser
        config._metadata['Test Environment'] = env

# Hook to modify/remove default metadata entries
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)
