import re
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python update_cv.py NEW_NAME.pdf [--apply]")
        print("Example: python update_cv.py andrea-ramazzotti-cv-oct26.pdf --apply")
        return

    new = sys.argv[1]
    apply = "--apply" in sys.argv

    # Any href to a PDF with "cv" in its filename; keeps any folder prefix
    pattern = re.compile(
        r'(href=["\'])((?:[^"\']*/)?)[^"\'/]*cv[^"\'/]*\.pdf(["\'])',
        re.IGNORECASE,
    )

    site = Path(__file__).parent  # folder where the script sits
    total = 0

    for page in sorted(site.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        hits = pattern.findall(text)
        if hits:
            total += len(hits)
            print(f"{page.name}: {len(hits)} link(s)")
            if apply:
                updated = pattern.sub(
                    lambda m: m.group(1) + m.group(2) + new + m.group(3), text
                )
                page.write_text(updated, encoding="utf-8")

    if total == 0:
        print("No CV links found.")
    elif apply:
        print(f"Updated {total} link(s). Check the pages, then commit and push.")
    else:
        print(f"Dry run: {total} link(s) would change. Re-run with --apply to edit.")

main()