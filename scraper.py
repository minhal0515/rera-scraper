# -*- coding: utf-8 -*-
import base64, json, logging, requests, pandas as pd
from time import sleep

BASE_URL = "https://rera.odisha.gov.in"
API_LIST = "https://reraapps.odisha.gov.in/pms/api/master/Projects/projectListing"

REQUEST_DATA = "eyJzZWFyY2hUZXJtIjoiIiwiZGlzdHJpY3QiOjAsInN0cnRZZWFyIjowLCJlbmRZZWFyIjowLCJwcm9qZWN0U3RhdHVzIjpbXSwiY2FycGV0QXJlYSI6IiIsInByb3BlcnR5VHlwZSI6W10sImxhdGl0dWRlIjoiIiwibG9uZ2l0dWRlIjoiIiwicmFkaXVzIjoiIiwiYXBwcm92ZWRTdGF0dXMiOmZhbHNlLCJyZXZva2VkU3RhdHVzIjpmYWxzZSwicGFnZSI6MSwicGFnZVNpemUiOjEwLCJzb3J0T3JkZXIiOiJhc2MifQ=="
REQUEST_TOKEN = "27a0f2c450a1ca0d6684c1b192d3025b89e9e178c23171ff74e1c96d5fee20dd"

HEADERS = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
}


def fetch_projects_list():
    payload = {"REQUEST_DATA": REQUEST_DATA, "REQUEST_TOKEN": REQUEST_TOKEN }
    resp = requests.post(API_LIST, json=payload, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    blob = resp.json().get("RESPONSE_DATA")
    decoded = base64.b64decode(blob).decode("utf-8")
    data = json.loads(decoded).get("result", [])
    return data





def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logging.info("Fetching projects list standby")
    projects = fetch_projects_list()
    records = []
    for idx, row in enumerate(projects[:6], 1):
    	logging.info("(%d/6) %s", idx, row.get("project_Name"))
    	records.append({
    		"Rera Regd. No":      row.get("reg_no", ""),
            "Project Name":       row.get("project_Name", ""),
            "Promoter Name":      row.get("promotorName", ""),
            "Promoter Address":   f"{row.get('addressArea','')} {row.get('addressTown','')}".strip(),
            "GST No":             row.get("gstNo", "")
    		})
    	sleep(0.2)

    df = pd.DataFrame(records)
    df.to_csv("rera_projects.csv", index = False)
    print(df.to_string(index = False))


if __name__ == "__main__":
    main()
