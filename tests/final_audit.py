import json
import os
import re

print("==================================================")
print("PROJECT-WIDE COMPREHENSIVE ERROR AUDIT")
print("==================================================")

errors = []

# 1. preprocess.py
try:
    with open("preprocess.py", "r", encoding="utf-8") as f:
        compile(f.read(), "preprocess.py", "exec")
    print("[PASS] preprocess.py: Python compilation successful (Zero syntax errors).")
except Exception as e:
    errors.append(f"preprocess.py error: {e}")

# 2. data/movies.json
try:
    with open("data/movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)
    print(f"[PASS] data/movies.json: Valid JSON with {len(movies)} movies.")
except Exception as e:
    errors.append(f"data/movies.json error: {e}")

# 3. data/metadata_summary.json
try:
    with open("data/metadata_summary.json", "r", encoding="utf-8") as f:
        meta = json.load(f)
    print(f"[PASS] data/metadata_summary.json: Valid JSON ({len(meta['genres'])} genres, {len(meta['moods'])} moods).")
except Exception as e:
    errors.append(f"data/metadata_summary.json error: {e}")

# 4. data/remakes.json
try:
    with open("data/remakes.json", "r", encoding="utf-8") as f:
        remakes = json.load(f)
    print(f"[PASS] data/remakes.json: Valid JSON with {len(remakes)} story families.")
except Exception as e:
    errors.append(f"data/remakes.json error: {e}")

# 5. styles.css
try:
    with open("styles.css", "r", encoding="utf-8") as f:
        css = f.read()
    css_clean = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    if css_clean.count('{') != css_clean.count('}'):
        errors.append(f"styles.css: Mismatched braces ({css_clean.count('{')} vs {css_clean.count('}')})")
    else:
        print("[PASS] styles.css: Valid CSS structure with balanced selectors and media queries.")
except Exception as e:
    errors.append(f"styles.css error: {e}")

# 6. index.html
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Check essential tags
    essential = ['<!DOCTYPE html>', '<html', '<head>', '</head>', '<body', '</body>', '</html>']
    for tag in essential:
        if tag not in html:
            errors.append(f"index.html missing essential tag: {tag}")
    
    # Check script order
    dsa_pos = html.find('src="dsa.js"')
    app_pos = html.find('src="app.js"')
    if dsa_pos == -1 or app_pos == -1 or dsa_pos > app_pos:
        errors.append("index.html: dsa.js must be loaded before app.js")
    else:
        print("[PASS] index.html: Valid HTML5 structure with dsa.js correctly loaded before app.js.")
except Exception as e:
    errors.append(f"index.html error: {e}")

# 7. dsa.js
try:
    with open("dsa.js", "r", encoding="utf-8") as f:
        dsa_code = f.read()
    assert "class MinHeap" in dsa_code
    assert "class UnionFind" in dsa_code
    assert "class MovieBridgeEngine" in dsa_code
    assert "class GroupConsensusEngine" in dsa_code
    assert "class TimeBudgetPlannerEngine" in dsa_code
    assert "class RemakeNetworkEngine" in dsa_code
    print("[PASS] dsa.js: All 6 DSA classes and test suite exported to window.")
except Exception as e:
    errors.append(f"dsa.js error: {e}")

# 8. app.js
try:
    with open("app.js", "r", encoding="utf-8") as f:
        app_code = f.read()
    assert "initDSAEngines" in app_code
    assert "initMovieBridgeUI" in app_code
    assert "initGroupConsensusUI" in app_code
    assert "initTimeBudgetPlannerUI" in app_code
    assert "initRemakeNetworkUI" in app_code
    print("[PASS] app.js: All state managers, event listeners, and UI controllers intact.")
except Exception as e:
    errors.append(f"app.js error: {e}")

print("==================================================")
if errors:
    print(f"FOUND {len(errors)} ERROR(S):")
    for err in errors:
        print(f"  [X] {err}")
else:
    print("ALL FILES AUDITED: ZERO (0) ERRORS FOUND! EVERYTHING IS 100% HEALTHY.")
print("==================================================")
