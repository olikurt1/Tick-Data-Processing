#deliberate tests to ensure exception handlers work
from src.Fetch import fetch_with_retry, fetch_sightings, BASE_URL

def test(name, function):
    print(f"----{name}----")
    try:
        results = function()
        print(f"OK: received {len(results)} records")
    except Exception as e:
        print(f"Failed as expected: {type(e).__name__}: {e}")

test("Normal fetch", fetch_sightings)
test("404", lambda: fetch_with_retry(f"{BASE_URL}/does-not-exist"))
test("Forced timeout", lambda: fetch_with_retry(f"{BASE_URL}/tick-sightings", timeout=0.001))

for x in range(30):
    test(f"Rate limit check {x + 1}", fetch_sightings)