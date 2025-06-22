import pytest
import platform
from selenium import webdriver
from utilities.customLogger import LogGen
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
import os
from datetime import datetime
import logging
import time



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Optional: Force plugin loading (not always necessary but helps Pytest 8+)
pytest_plugins = ["pytest_html", "pytest_metadata"]

# For session start/end log messages (optional)
@pytest.fixture(scope="session", autouse=True)
def setup_logging_once():
    logger = LogGen.loggen()
    logger.info("Pytest session started")
    yield
    logger.info("Pytest session finished")

# Actual fixture to use in test
@pytest.fixture
def logger():
    return LogGen.loggen()

@pytest.fixture()
def setup(request):
    browser = request.config.getoption("--browser").lower().strip()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # For CI
        driver = webdriver.Chrome(options=options)
        #driver = webdriver.Chrome()
        print("Launching Chrome browser...........")
    elif browser == "firefox":
        driver = webdriver.Firefox()
        print("Launching Firefox browser..........")
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    print("Closing browser")
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        driver = item.funcargs.get("setup")
        if driver:
            screenshot_dir = os.path.join("Reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_file = os.path.join(
                screenshot_dir,
                f"{item.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            )
            driver.save_screenshot(screenshot_file)

            if hasattr(item.config, "_reportportal_service"):
                with open(screenshot_file, "rb") as image_file:
                    item.config._reportportal_service.log(
                        time=int(time.time() * 1000),
                        message="Screenshot on failure",
                        level="ERROR",
                        attachment={
                            "name": os.path.basename(screenshot_file),
                            "data": image_file.read(),
                            "mime": "image/png"
                        }
                    )