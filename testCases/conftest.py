import pytest
import platform
from selenium import webdriver

from utilities.AxeHelpers import AxeHelpers
from utilities.customLogger import LogGen
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
import os
from datetime import datetime
import logging
import time
from reportportal_client import RPLogger

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# Optional: Force plugin loading (not always necessary but helps Pytest 8+)
pytest_plugins = ["pytest_html", "pytest_metadata"]


# -------------------Logging setup--------------------------
@pytest.fixture(scope='session', autouse=True)
def configure_rp_logger():
    # MUST be done before any logger is initialized
    logging.setLoggerClass(RPLogger)

@pytest.fixture(scope="function")
def logger():
    # For console/file logging
    return LogGen.loggen()

@pytest.fixture(scope="function")
def rp_logger():
    # Dedicated RPLogger for attachments/logs in ReportPortal
    return logging.getLogger("reportportal_logger")

@pytest.fixture(scope="session", autouse=True)
def setup_logging_once():
    logger = LogGen.loggen()
    logger.info("Pytest session started")
    yield
    logger.info("Pytest session finished")

# --- Browser Setup --------------------------------------------------------

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
        "Build": "2025.06.15",
        "Project Name": "PyTest HybridFramework",
        "Developer": "Niraj Patel",
        "Platform": platform.system(),
        "Python Version": platform.python_version(),
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
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshots_dir = os.path.join("Reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}_{timestamp}.png")
            driver.save_screenshot(screenshot_path)

            if hasattr(item.config, "_reportportal_service"):
                with open(screenshot_path, "rb") as f:
                    item.config._reportportal_service.log(
                        time=int(time.time() * 1000),
                        message="Failure Screenshot",
                        level="ERROR",
                        attachment={
                            "name": f"{item.name}.png",
                            "data": f.read(),
                            "mime": "image/png"
                        }
                    )

@pytest.fixture(scope="function")
def axe(request, setup):
    safe_name = request.node.name.replace("[", "_").replace("]", "_")
    axe_report_json = f"Reports/{safe_name}.json"
    html_path = f"Reports/{safe_name}.html"
    axe_helper = AxeHelpers(setup, axe_report_json)
    yield axe_helper
    axe_helper.generate_html_report(html_path)

    if hasattr(request.config, "_reportportal_service") and os.path.exists(html_path):
        with open(html_path, "rb") as f:
            request.config._reportportal_service.log(
                time=int(time.time() * 1000),
                message="Axe Accessibility HTML Report",
                level="INFO",
                attachment={
                    "name": os.path.basename(html_path),
                    "data": f.read(),
                    "mime": "text/html"
                }
            )