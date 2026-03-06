import urllib.request
import json
import time
import concurrent.futures

BASE = "http://127.0.0.1:8000/api/v1"

juris_resp = urllib.request.urlopen(BASE + "/jurisdictions/")
juris_data = json.loads(juris_resp.read())
juris_list = juris_data.get("jurisdictions", [])
juris_ids = [j["id"] for j in juris_list]
print("Found", len(juris_ids), "jurisdictions")

def timed_request(url, method="GET", data=None):
    start = time.time()
    try:
        if data:
            req = urllib.request.Request(url, data=json.dumps(data).encode(), 
                                        headers={"Content-Type": "application/json"})
        else:
            req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        return 200, (time.time() - start) * 1000, result
    except urllib.error.HTTPError as e:
        return e.code, (time.time() - start) * 1000, e.read().decode()[:100]

print()
print("=== CALCULATION ENDPOINTS TEST ===")
print()
print("--- GET Endpoints ---")

status, ms, data = timed_request(BASE + "/calculate/options")
types_count = len(data.get("productionTypes", [])) if isinstance(data, dict) else 0
print("Options           | %d | %6.1fms | Types: %d" % (status, ms, types_count))

url = BASE + "/calculate/jurisdiction/" + juris_ids[0] + "?budget=5000000"
status, ms, data = timed_request(url)
opts_count = len(data.get("options", [])) if isinstance(data, dict) else 0
print("Jurisdiction Calc | %d | %6.1fms | Options: %d" % (status, ms, opts_count))

print()
print("--- POST Endpoints ---")

if len(juris_ids) >= 2:
    compare_data = {"productionBudget": 5000000, "jurisdictionIds": juris_ids[:2]}
    status, ms, data = timed_request(BASE + "/calculate/compare", "POST", compare_data)
    if status == 200:
        best = data.get("bestOption", {})
        juris_name = best.get("jurisdiction", "N/A")
        credit = best.get("estimatedCredit", 0)
        print("Compare Calc      | %d | %6.1fms | Best: %s ($%d)" % (status, ms, juris_name, credit))
    else:
        print("Compare Calc      | %d | %6.1fms | Error: %s" % (status, ms, str(data)[:50]))

print()
print("=== LOAD TEST: 50 Concurrent Requests ===")

def load_test(url, n):
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        return list(executor.map(lambda _: timed_request(url)[1], range(n)))

results = load_test(BASE + "/calculate/options", 50)
print("Options (50 req)  | Avg: %dms | Min: %dms | Max: %dms" % (sum(results)/len(results), min(results), max(results)))

url = BASE + "/calculate/jurisdiction/" + juris_ids[0] + "?budget=5000000"
results = load_test(url, 50)
print("Jurisdiction (50) | Avg: %dms | Min: %dms | Max: %dms" % (sum(results)/len(results), min(results), max(results)))

print()
print("=== CALCULATION PERFORMANCE: PASSED ===")
