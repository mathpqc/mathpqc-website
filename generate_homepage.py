import re
from pathlib import Path
from typing import List

from PyPDF2 import PdfReader

PDF_FILE = Path('MathPQC- AC26 affiliated event.pdf')
OUTPUT_FILE = Path('index.html')


def read_pdf_text(path: Path) -> str:
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ''
        pages.append(text)
    return '\n\n'.join(pages)


def normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def extract_block(text: str, start_phrase: str, end_phrase: str) -> str:
    start = text.find(start_phrase)
    if start == -1:
        return ''
    start += len(start_phrase)
    end = text.find(end_phrase, start)
    if end == -1:
        end = len(text)
    return normalize(text[start:end])


def split_list_block(block: str) -> List[str]:
    items = re.split(r',\s*|\s+etc\.?\s*', block)
    return [item.strip() for item in items if item.strip()]


def build_homepage(content: str) -> str:
    title = 'Mathematics for Post-Quantum Cryptography (MathPQC 2026)'
    date = 'Monday, December 7, 2026'
    location = 'Hong Kong Polytechnic University, Hong Kong'
    event_description = (
        'MathPQC 2026 is a one-day affiliated workshop held during ASIACRYPT 2026. '
        'It brings together mathematicians and cryptographers to explore the mathematical foundations of post-quantum cryptography.'
    )

    organizers = [
        {'name': 'Shi Bai', 'affiliation': 'Shanghai Jiao Tong University', 'email': 'baishi@sjtu.edu.cn'},
        {'name': 'Mingjie Chen', 'affiliation': 'COSIC, KU Leuven', 'email': 'mjchennn555@gmail.com'},
        {'name': 'Steven Galbraith', 'affiliation': 'University of Auckland', 'email': 'S.Galbraith@auckland.ac.nz'},
    ]

    format_description = 'A one-day workshop featuring invited talks and contributed talks.'
    abstract = extract_block(content, 'Abstract summarising the proposed event and its justification', '6.')
    if not abstract:
        abstract = (
            'Post-quantum cryptographic schemes are built on hard mathematical problems across lattices, isogenies, coding theory, and multivariate algebra. '
            'This workshop aims to connect the mathematics community with cryptographers to exchange ideas, highlight recent developments, and foster new interdisciplinary interaction.'
        )

    attendance = 'Estimated attendance: 30 to 50 participants total, including 20 to 30 student participants.'
    speakers_block = extract_block(content, 'List of specific potential attendees', '9.')
    potential_speakers = split_list_block(speakers_block)

    funding = extract_block(content, 'No external funding is currently planned for the event.', '11.')
    if not funding:
        funding = 'No external funding is currently planned. Organizers expect to cover their own travel costs.'

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MathPQC 2026 Event</title>
    <meta
      name="description"
      content="MathPQC 2026 affiliated event homepage: summary, schedule, organizers, and key information."
    />
    <style>
      :root {{
        color-scheme: light;
        --bg: #f7fbff;
        --surface: #ffffff;
        --text: #0f172a;
        --muted: #475569;
        --accent: #2563eb;
        --border: #e2e8f0;
      }}
      * {{ box-sizing: border-box; }}
      body {{ margin: 0; font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); }}
      main {{ max-width: 980px; margin: 0 auto; padding: 40px 20px 60px; }}
      .hero, .section {{ background: var(--surface); border: 1px solid var(--border); border-radius: 22px; box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08); margin-bottom: 24px; }}
      .hero {{ padding: 36px 34px; }}
      .hero h1 {{ margin: 0 0 12px; font-size: clamp(2rem, 3vw, 3rem); line-height: 1.05; }}
      .hero p {{ max-width: 760px; line-height: 1.72; color: var(--muted); font-size: 1.05rem; }}
      .label {{ display: inline-flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; }}
      .label span {{ display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 999px; background: #eef4ff; color: #1d4ed8; font-weight: 600; font-size: 0.95rem; }}
      .section {{ padding: 28px 32px; }}
      .section h2 {{ margin-top: 0; font-size: 1.4rem; }}
      .section p, .section li {{ line-height: 1.75; color: var(--muted); }}
      .grid {{ display: grid; gap: 24px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }}
      .card {{ padding: 22px 20px; border-radius: 20px; background: #f8fbff; border: 1px solid #dbe7f3; }}
      ul {{ padding-left: 20px; margin: 0; }}
      li {{ margin-bottom: 12px; }}
      .organizer-name {{ font-weight: 700; color: var(--text); }}
      .small {{ color: var(--muted); font-size: 0.95rem; }}
      .footer {{ text-align: center; font-size: 0.95rem; color: var(--muted); margin-top: 14px; }}
    </style>
  </head>
  <body>
    <main>
      <section class="hero">
        <h1>{title}</h1>
        <p>{event_description}</p>
        <div class="label">
          <span>📅 {date}</span>
          <span>📍 {location}</span>
          <span>⏳ Whole-day workshop</span>
        </div>
      </section>

      <section class="section">
        <h2>Event summary</h2>
        <p>{abstract}</p>
      </section>

      <section class="section grid">
        <div class="card">
          <h2>Purpose</h2>
          <p>{format_description}</p>
        </div>
        <div class="card">
          <h2>Expected attendance</h2>
          <p>{attendance}</p>
        </div>
      </section>

      <section class="section">
        <h2>Organizers</h2>
        <ul>
          {''.join(f'<li><span class="organizer-name">{o["name"]}</span>, {o["affiliation"]} <span class="small">({o["email"]})</span></li>' for o in organizers)}
        </ul>
      </section>

      <section class="section">
        <h2>Potential speakers & attendees</h2>
        <p>This affiliated event is expected to attract leaders in mathematical foundations of post-quantum cryptography.</p>
        <ul>
          {''.join(f'<li>{speaker}</li>' for speaker in potential_speakers[:12])}
          {('<li>...and more invited experts</li>' if len(potential_speakers) > 12 else '')}
        </ul>
      </section>

      <section class="section">
        <h2>Additional notes</h2>
        <p>{funding}</p>
        <p>Source: MathPQC 2026 affiliated event proposal for ASIACRYPT 2026.</p>
      </section>

      <div class="footer">Generated from the proposal PDF in the repository.</div>
    </main>
  </body>
</html>"""
    return html


if __name__ == '__main__':
    text = read_pdf_text(PDF_FILE)
    content = normalize(text)
    html = build_homepage(content)
    OUTPUT_FILE.write_text(html, encoding='utf-8')
    print(f'Wrote {OUTPUT_FILE}')
