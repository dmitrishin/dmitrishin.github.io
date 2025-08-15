import os
import re

# The exact snippet to insert
json_ld_snippet = """<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"Person",
  "@id":"https://dmitrishin.github.io/#person"
}
</script>"""

# Canonical Person ID
canonical_person_id = "https://dmitrishin.github.io/#person"

# List of files to process
files_to_process = [
    "lang/ku/index.html", "lang/jv/index.html", "lang/sr/index.html", "lang/pt-BR/index.html",
    "lang/si/index.html", "lang/ha/index.html", "lang/is/index.html", "lang/id/index.html",
    "lang/lv/index.html", "lang/ms/index.html", "lang/lt/index.html", "lang/mk/index.html",
    "lang/ur/index.html", "lang/eu/index.html", "lang/index.html", "lang/nl/index.html",
    "lang/af/index.html", "lang/ba/index.html", "lang/tk/index.html", "lang/vi/index.html",
    "lang/sq/index.html", "lang/ka/index.html", "lang/ee/index.html", "lang/or/index.html",
    "lang/bg/index.html", "lang/ts/index.html", "lang/hr/index.html", "lang/yo/index.html",
    "lang/ay/index.html", "lang/gu/index.html", "lang/ru/index.html", "lang/gd/index.html",
    "lang/so/index.html", "lang/fi/index.html", "lang/rm/index.html", "lang/hi/index.html",
    "lang/ro/index.html", "lang/su/index.html", "lang/mt/index.html", "lang/fr/index.html",
    "lang/uk/index.html", "lang/pl/index.html", "lang/zu/index.html", "lang/sv/index.html",
    "lang/de/index.html", "lang/my/index.html", "lang/te/index.html", "lang/sw/index.html",
    "lang/ja/index.html", "lang/ca/index.html", "lang/tl/index.html", "lang/pt/index.html",
    "lang/tr/index.html", "lang/dv/index.html", "lang/qu/index.html", "lang/cs/index.html",
    "lang/ps/index.html", "lang/lo/index.html", "lang/zh/index.html", "lang/es/index.html",
    "lang/ky/index.html", "lang/am/index.html", "lang/xh/index.html", "lang/hy/index.html",
    "lang/fa/index.html", "lang/gl/index.html", "lang/th/index.html", "lang/sl/index.html",
    "lang/bs/index.html", "lang/sn/index.html", "lang/az/index.html", "lang/be/index.html",
    "lang/uz/index.html", "lang/no/index.html", "lang/ne/index.html", "lang/tg/index.html",
    "lang/et/index.html", "lang/sk/index.html", "lang/bn/index.html", "lang/rw/index.html",
    "lang/el/index.html", "lang/ig/index.html", "lang/mn/index.html", "lang/mr/index.html",
    "lang/zh-TW/index.html", "lang/hu/index.html", "lang/kn/index.html", "lang/ko/index.html",
    "lang/pa/index.html", "lang/da/index.html", "lang/fj/index.html", "lang/co/index.html",
    "lang/kk/index.html", "lang/he/index.html", "lang/ml/index.html", "lang/ga/index.html",
    "lang/tt/index.html", "lang/ar/index.html", "lang/it/index.html", "lang/ta/index.html",
    "lang/ti/index.html"
]

report = []
files_to_modify = []

# Regex to find JSON-LD scripts
ld_json_re = re.compile(r'<script type="application/ld\+json".*?>(.*?)</script>', re.DOTALL)

for filepath in files_to_process:
    if not os.path.exists(filepath):
        report.append(f"{filepath}: skipped-file-not-found")
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        report.append(f"{filepath}: skipped-read-error ({e})")
        continue

    if '</head>' not in content:
        report.append(f"{filepath}: skipped-no-head")
        continue

    # Simple string search logic
    has_canonical = False
    has_person = False

    json_ld_scripts = ld_json_re.findall(content)
    for script_content in json_ld_scripts:
        # Normalize script content to handle whitespace variations
        normalized_script = re.sub(r'\s', '', script_content)

        if '"@type":"Person"' in normalized_script:
            has_person = True
            # Use regex to find @id to avoid issues with spacing/quotes
            id_match = re.search(r'"@id"\s*:\s*"' + re.escape(canonical_person_id) + r'"', script_content)
            if id_match:
                has_canonical = True
                break

    status = ""
    if has_canonical:
        status = "already-present"
    elif has_person:
        status = "conflict-different-id"
    else:
        status = "needs-insertion"
        files_to_modify.append(filepath)

    report.append(f"{filepath}: {status}")

print("--- Files to Modify ---")
for f in files_to_modify:
    print(f)

print("\\n--- Processing Report ---")
for r in sorted(report):
    print(r)
