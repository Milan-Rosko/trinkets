# CSS2Letter

A browser-based DIN 5008-style A4 letter template with automatic pagination, print output, lightweight inline emphasis, and MathJax equations.

## Use

Open [`index.html`](index.html) in a current browser. The preview paginates after fonts and mathematics finish rendering; use **Print** to open the browser’s A4 print dialog.

No build step is required. An internet connection is needed for the IBM Plex web fonts and MathJax CDN.

## Customize

- Edit `scripts/letter-content.js` for the recipient, subject, body, and signature name.
- Edit `index.html` for the sender identity, letterhead, and footer.
- Replace `assets/logo.png` and `assets/signature.png` while keeping their filenames, or update the corresponding references.
- Tune page geometry and typography in `styles/din5008.css`.

Inline content supports `*italic*`, `**bold**`, `***bold italic***`, `$inline math$`, and `$$display math$$`.

## Geometry

The stylesheet uses the project’s finalized A4 measurements:

| Element | Position or size |
| --- | --- |
| Page | 210 × 297 mm |
| Address window | 25 mm from the left, 50 mm from the top; 80 × 40 mm |
| Information block | 50 mm from the top |
| Subject and date | 100 mm from the top |
| Fold and punch marks | 105 mm, 148.5 mm, and 210 mm |
| First-page body | 110 mm from the top; 31 lines at 5 mm |
| Continuation body | 45 mm from the top; 44 lines at 5 mm |

## Structure

```text
css2letter/
├── index.html
├── assets/
│   ├── logo.png
│   ├── signature.png
│   └── reference/
├── scripts/
│   ├── letter-content.js
│   ├── letter-engine.js
│   └── pagination.js
└── styles/
    └── din5008.css
```

The images under `assets/reference/` are design references and are not loaded by default.
