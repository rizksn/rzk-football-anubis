import os
import json
import time

def normalize_segment(name: str) -> str:
    """
    Normalize a segment by converting to lowercase, replacing spaces/dashes with underscores,
    and stripping leading/trailing whitespace.
    """
    return name.lower().replace(" ", "_").replace("-", "_").strip()

def save_adp_data(players, format_, type_, scoring, platform):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    base_dir = os.path.join(
        project_root,
        "anubis",
        "data",
        "raw",
        "draftsharks",
        normalize_segment(format_)
    )

    fname = (
        f"{normalize_segment(format_)}_"
        f"{normalize_segment(type_)}_"
        f"{normalize_segment(scoring)}_"
        f"{normalize_segment(platform)}.raw.json"
    )
    path = os.path.join(base_dir, fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump({
            "scraped_at": time.strftime('%Y-%m-%d %H:%M:%S'),
            "data": players
        }, f, indent=2)

    print(f"[{time.strftime('%H:%M:%S')}] ✅ Saved {len(players)} players to {path}")

def scroll_to_load_all(page):
    page.evaluate_handle("""
        () => new Promise((resolve) => {
            let lastScrollY = -1;
            let stableCount = 0;
            const interval = setInterval(() => {
                window.scrollBy(0, 1000);
                const scrollY = window.scrollY;
                const bodyHeight = document.body.scrollHeight;
                const viewBottom = window.innerHeight + scrollY;

                if (viewBottom >= bodyHeight) stableCount += 1;
                else stableCount = 0;

                if (stableCount >= 3) {
                    clearInterval(interval);
                    console.log("✅ Finished scrolling to bottom");
                    setTimeout(resolve, 1500);
                }

                if (scrollY === lastScrollY) stableCount += 1;
                else {
                    lastScrollY = scrollY;
                    stableCount = 0;
                }
            }, 400);
        })
    """).json_value()
