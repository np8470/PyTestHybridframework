import json
import os
import subprocess
from axe_selenium_python import Axe
import logging

class AxeHelpers:
    def __init__(self, driver, report_json_path):
        self.driver = driver
        self.axe = Axe(driver)
        self.report_json_path = report_json_path
        self.logger = logging.getLogger("AxeHelper")
        self.logger.setLevel(logging.INFO)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.report_json_path), exist_ok=True)

    def run_scan(self):
        self.axe.inject()
        results = self.axe.run()
        with open(self.report_json_path, "w") as f:
            json.dump(results, f)
        return results

    def generate_html_report(self, html_path):
        if not os.path.exists(self.report_json_path):
            return

        #command = f"npx axe-html-reporter --results {self.report_json_path} --output {html_path}"
        command = f"npx axe-reports --results {self.report_json_path} --output {html_path}"

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error generating axe HTML report: {e}")

    def assert_no_violations(self, results):
        violations = results.get("violations", [])
        if violations:
            self.logger.error(f"Accessibility Violations Found: {len(violations)}")
            for v in violations:
                self.logger.warning(f"{v['help']} - {v['impact']}")
                for node in v["nodes"]:
                    self.logger.debug(f"Affected Element: {node['html']}")
            assert False, f"{len(violations)} accessibility violations found. See JSON for details."
        else:
            self.logger.info("No accessibility violations found.")