import json
import os
import subprocess
import logging
from axe_selenium_python import Axe
from selenium.webdriver.remote.webdriver import WebDriver
from datetime import datetime

class AxeHelper:
    def __init__(self, driver: WebDriver, report_json_path="Reports/axe_report.json"):
        self.driver = driver
        self.axe = Axe(driver)
        self.json_path = self._sanitize_path(report_json_path)
        self.logger = logging.getLogger("AxeHelper")
        self.logger.setLevel(logging.INFO)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)

    def _sanitize_path(self, path):
        # Remove problematic characters for filenames
        path = path.replace("[", "_").replace("]", "_").replace(" ", "_")
        return path

    def run_scan(self, context=None, options=None):
        self.logger.info("Injecting axe-core and running accessibility scan...")
        self.axe.inject()
        results = self.axe.run(context=context, options=options)

        self.logger.info(f"Writing axe scan results to {self.json_path}")
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        return results

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

    def generate_html_reportsss(self, html_path="reports/axe_report.html"):
        html_path = self._sanitize_path(html_path)
        os.makedirs(os.path.dirname(html_path), exist_ok=True)

        if not os.path.exists(self.json_path):
            self.logger.error(f"Cannot generate HTML report. JSON file not found: {self.json_path}")
            raise FileNotFoundError(f"Axe result JSON not found: {self.json_path}")

        command = f"npx axe-html-reporter --results {self.json_path} --output {html_path}"
        self.logger.info(f"Generating HTML accessibility report: {html_path}")
        try:
            subprocess.run(command, shell=True, check=True)
            self.logger.info("HTML report generated successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to generate HTML report: {e}")
            raise RuntimeError(f"axe-html-reporter failed with exit code {e.returncode}")


    def generate_html_reportttt(self, html_path="reports/axe_report.html"):
        html_path = self._sanitize_path(html_path)
        os.makedirs(os.path.dirname(html_path), exist_ok=True)

        if not os.path.exists(self.json_path):
            self.logger.error(f"Cannot generate HTML report. JSON file not found: {self.json_path}")
            raise FileNotFoundError(f"Axe result JSON not found: {self.json_path}")

        command = f"npx axe-html-reporter --results {self.json_path} --output {html_path}"
        self.logger.info(f"Generating HTML accessibility report: {html_path}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.logger.info(result.stdout)
            if result.stderr:
                self.logger.warning(result.stderr)
            self.logger.info("HTML report generated successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to generate HTML report. Exit Code: {e.returncode}")
            self.logger.error(f"STDOUT: {e.stdout}")
            self.logger.error(f"STDERR: {e.stderr}")
            raise RuntimeError("axe-html-reporter failed. Check logs for details.")

    def generate_html_reporttss(self, html_path="Reports/axe_report.html"):
        html_path = self._sanitize_path(html_path)
        os.makedirs(os.path.dirname(html_path), exist_ok=True)

        if not os.path.exists(self.json_path):
            self.logger.error(f"Cannot generate HTML report. JSON file not found: {self.json_path}")
            raise FileNotFoundError(f"Axe result JSON not found: {self.json_path}")

        # Check if JSON is valid
        try:
            with open(self.json_path, "r") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid axe result JSON: {e}")

        #command = f"npx axe-html-reporter --results {self.json_path} --output {html_path}"
        command = f"npx --yes axe-reports --results {self.json_path} --output {html_path}"

        self.logger.info(f"Generating HTML accessibility report: {html_path}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.logger.info(result.stdout)
            if result.stderr:
                self.logger.warning(result.stderr)
            self.logger.info("HTML report generated successfully.")
        except subprocess.CalledProcessError as e:
            print("STDERR:", e.stderr)
            print("STDOUT:", e.stdout)
            raise RuntimeError("axe-html-reporter failed. Check logs for details.")



    def generate_html_report(self, html_path="Reports/axe_report.html"):
        html_path = self._sanitize_path(html_path)
        os.makedirs(os.path.dirname(html_path), exist_ok=True)

        if not os.path.exists(self.json_path):
            self.logger.error(f"Cannot generate HTML report. JSON file not found: {self.json_path}")
            raise FileNotFoundError(f"Axe result JSON not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            results = json.load(f)

        violations = results.get("violations", [])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""
        <html>
        <head>
            <title>Axe Accessibility Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .violation {{ border: 1px solid #ccc; padding: 10px; margin-bottom: 15px; }}
                .impact {{ font-weight: bold; color: red; }}
                .code {{ background: #f4f4f4; padding: 5px; font-family: monospace; }}
            </style>
        </head>
        <body>
            <h1>Accessibility Report</h1>
            <p><strong>Generated:</strong> {timestamp}</p>
            <p><strong>Total Violations:</strong> {len(violations)}</p>
        """

        for v in violations:
            html += f"""
            <div class="violation">
                <h2>{v['help']} ({v['id']})</h2>
                <p class="impact">Impact: {v.get('impact', 'N/A')}</p>
                <p>{v['description']}</p>
                <ul>
            """
            for node in v['nodes']:
                html += f"<li><div class='code'>{node['html']}</div><p>{node['failureSummary']}</p></li>"
            html += "</ul></div>"

        html += "</body></html>"

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        self.logger.info(f"HTML accessibility report saved to {html_path}")
