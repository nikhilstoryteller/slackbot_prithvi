#!/usr/bin/env python3
import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Report Links Dictionary
def get_reports():
    return {
        "BW Generation": "https://lookerstudio.google.com/reporting/7f396517-bca2-4f32-bdd4-6e3d69bc593b",
        "Sunoh":          "https://lookerstudio.google.com/reporting/39b65949-427b-46b7-b005-bdb5cc8a109e",
        "Healow":         "https://lookerstudio.google.com/reporting/8c4d2445-2567-482c-b6e7-fe4b035c704f",
        "UA":             "https://lookerstudio.google.com/reporting/ba3d152c-3c93-4dd6-a4af-f779f598a234",
        "FCC":            "https://lookerstudio.google.com/reporting/34ca31e9-0dd5-4f5e-88a5-b0c3b1dea831",
        "Scuderia":       "https://lookerstudio.google.com/reporting/da8ba832-1df3-4412-9785-000262daa084",
        "Confido":        "https://lookerstudio.google.com/reporting/7018b15a-0d1a-45e0-b5b1-8eb9122d66be",
        "KodeKloud":      "https://lookerstudio.google.com/reporting/7c9e0649-d145-46e3-a8e5-ee09955071d7",
        "HPFY":           "https://lookerstudio.google.com/reporting/8b7be612-b8b5-4acd-bccf-a520fc4da59e",
        "AOL(Intuition)": "https://lookerstudio.google.com/reporting/10eac558-48e9-46eb-b5f9-1a7f0fa1e885",
        "AOL(SSSY)":      "https://lookerstudio.google.com/reporting/69aa7bb2-e88c-4d26-8e82-fd9bd56c5f31",
        "CoveNLane":      "https://lookerstudio.google.com/reporting/b2ae0d43-2e1f-409e-8ea0-0a20e8e89140"
    }

# Month names
MONTHS = {1: "January", 2: "February", 3: "March", 4: "April",
          5: "May", 6: "June", 7: "July", 8: "August",
          9: "September", 10: "October", 11: "November", 12: "December"}


def run_report(report_name, start_date, end_date, output_path):
    reports = get_reports()
    if report_name not in reports:
        raise ValueError(f"Invalid report name: {report_name}")
    url = reports[report_name]

    # Parse dates (DD/MM/YYYY)
    sd, sm, sy = map(int, start_date.split('/'))
    ed, em, ey = map(int, end_date.split('/'))

    # Configure headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(25)  # allow full page load

    try:
        # Open the date picker
        date_picker_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".canvas-date-input"))
        )
        driver.execute_script("arguments[0].click();", date_picker_btn)
        time.sleep(2)

        # Select start date
        driver.find_element(By.CSS_SELECTOR, ".mat-calendar-period-button").click()
        driver.find_element(By.CSS_SELECTOR, f"button.mat-calendar-body-cell[aria-label='{sy}']").click()
        driver.find_element(By.CSS_SELECTOR, f"button.mat-calendar-body-cell[aria-label='{MONTHS[sm]} {sy}']").click()
        driver.find_element(By.CSS_SELECTOR, f"button.mat-calendar-body-cell[aria-label='{sd} {MONTHS[sm][:3]} {sy}']").click()
        time.sleep(1)

        # Select end date
        driver.find_element(By.CSS_SELECTOR, ".end-date-picker .mat-calendar-period-button").click()
        driver.find_element(By.CSS_SELECTOR, f".end-date-picker button.mat-calendar-body-cell[aria-label='{ey}']").click()
        driver.find_element(By.CSS_SELECTOR, f".end-date-picker button.mat-calendar-body-cell[aria-label='{MONTHS[em]} {ey}']").click()
        driver.find_element(By.CSS_SELECTOR, f".end-date-picker button.mat-calendar-body-cell[aria-label='{ed} {MONTHS[em][:3]} {ey}']").click()

        # Apply
        driver.find_element(By.CSS_SELECTOR, ".apply-button").click()
        time.sleep(10)

        # Save screenshot
        driver.save_screenshot(output_path)
        print(f"Screenshot saved to {output_path}")

    finally:
        driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Run LookerStudio report and capture date-range screenshot"
    )
    parser.add_argument('report', help='Report name key (e.g. Sunoh)')
    parser.add_argument('start',  help='Start date in DD/MM/YYYY format')
    parser.add_argument('end',    help='End date in DD/MM/YYYY format')
    parser.add_argument('-o', '--out', default='report.png', help='Output screenshot file path')

    args = parser.parse_args()
    try:
        run_report(args.report, args.start, args.end, args.out)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
