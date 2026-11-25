"""Run the Ames house price demo locally with python app.py."""
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from string import Template
from urllib.parse import parse_qs, urlsplit
import webbrowser

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent
BUNDLE = joblib.load(ROOT / "model" / "ames.joblib")
PAGE = Template((ROOT / "demo.html").read_text(encoding="utf-8"))
EXAMPLE = {"area": "1500", "Neighborhood": "NAmes", "Year.Built": "1975", "Overall.Qual": "6"}


def render(query):
    values = EXAMPLE.copy()
    result = ""
    status = 200
    if query:
        try:
            fields = parse_qs(query, keep_blank_values=True, max_num_fields=10)
            if set(fields) != set(EXAMPLE) or any(len(items) != 1 for items in fields.values()):
                raise ValueError
            values = {name: items[0] for name, items in fields.items()}
            if values["Neighborhood"] not in BUNDLE["neighbourhoods"]:
                raise ValueError
            row = {"Neighborhood": values["Neighborhood"]}
            for name, (low, high) in BUNDLE["limits"].items():
                row[name] = int(values[name])
                if not low <= row[name] <= high:
                    raise ValueError
            frame = pd.DataFrame([row], columns=BUNDLE["features"])
            price = BUNDLE["model"].predict(frame)[0]
            if price <= 0:
                result = "This combination falls outside the model’s useful range."
            else:
                result = f"Estimated sale price <strong>US${price:,.0f}</strong>"
        except ValueError:
            result = "Check the neighbourhood and enter whole numbers within the displayed ranges."
            status = 400
    fields_html = []
    labels = {"area": "Living area (sq ft)", "Neighborhood": "Neighbourhood code",
              "Year.Built": "Year built", "Overall.Qual": "Overall quality (1–10)"}
    for name in EXAMPLE:
        if name == "Neighborhood":
            options = "".join(
                f'<option{" selected" if code == values[name] else ""}>{escape(code)}</option>'
                for code in BUNDLE["neighbourhoods"]
            )
            control = f'<select name="{name}">{options}</select>'
        else:
            low, high = BUNDLE["limits"][name]
            control = (f'<input name="{name}" type="number" min="{low}" max="{high}" '
                       f'value="{escape(values[name], quote=True)}" required>')
        fields_html.append(f"<label>{labels[name]}{control}</label>")
    return status, PAGE.substitute(fields="".join(fields_html), result=result)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        if url.path != "/":
            self.send_error(404)
            return
        status, html = render(url.query)
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    with ThreadingHTTPServer(("127.0.0.1", 8000), Handler) as server:
        address = "http://127.0.0.1:8000"
        print(f"Open {address} · Press Ctrl+C to stop.", flush=True)
        webbrowser.open(address)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
