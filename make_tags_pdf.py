"""Writes tag16h5_cube_tags.pdf: all 30 tags (0-29), 20 per page, each a 40 mm square (5 mm cells) with a 30 mm black square
and a 5 mm white margin. Print at 100% / 'actual size' on A4, then cut along the grey lines."""
BX = [1,2,3,2,4,4,4,3,4,3,2,3,1,1,1,2]
BY = [1,1,1,2,1,2,3,2,4,4,4,3,4,3,2,3]
CODES = [0x27c8,0x31b6,0x3859,0x569c,0x6c76,0x7ddb,0xaf09,0xf5a1,0xfb8b,0x1cb9,0x28ca,0xe8dc,0x1426,0x5770,0x9253,0xb702,0x063a,0x8f34,0xb4c0,0x51ec,0xe6f0,0x5fa4,0xdd43,0x1aaa,0xe62f,0x6dbc,0xb6eb,0xde10,0x154d,0xb57a]
MM = 72 / 25.4
PW, PH = 210 * MM, 297 * MM
CELL, GAP = 5 * MM, 8 * MM
COLS, ROWS = 4, 5
PER = COLS * ROWS
ox = (PW - (COLS * 8 * CELL + (COLS - 1) * GAP)) / 2
oy = PH - 25 * MM          # top of first row

pages = []
for p0 in range(0, len(CODES), PER):
    ops = []
    for k, code in enumerate(CODES[p0:p0 + PER]):
        n = p0 + k
        col, row = k % COLS, k // COLS
        x0 = ox + col * (8 * CELL + GAP)
        ytop = oy - row * (8 * CELL + GAP)
        y0 = ytop - 8 * CELL
        ops.append(f"0.6 G 0.25 w {x0:.3f} {y0:.3f} {8*CELL:.3f} {8*CELL:.3f} re S")      # cut line (40 mm)
        ops.append(f"0 g {x0+CELL:.3f} {y0+CELL:.3f} {6*CELL:.3f} {6*CELL:.3f} re f")    # 30 mm black square
        ops.append("1 g")
        for i in range(16):
            if (code >> (15 - i)) & 1:
                cx = x0 + (BX[i] + 1) * CELL
                cy = ytop - (BY[i] + 2) * CELL
                ops.append(f"{cx:.3f} {cy:.3f} {CELL:.3f} {CELL:.3f} re f")
        ops.append(f"0 g BT /F1 8 Tf {x0:.3f} {y0-9:.3f} Td (tag16h5 id {n}) Tj ET")
    ops.append(f"0 g BT /F1 8 Tf {ox:.3f} {PH-12*MM:.3f} Td (Print at 100%. Cut on grey lines: 40 mm squares, black square inside is 30 mm.) Tj ET")
    pages.append(chr(10).join(ops).encode())

# objects: 1 catalog, 2 pages, 3 font, then per page: page obj, content obj
n_pages = len(pages)
kids = " ".join(f"{4 + 2*i} 0 R" for i in range(n_pages))
objs = [b"<</Type/Catalog/Pages 2 0 R>>",
        f"<</Type/Pages/Kids[{kids}]/Count {n_pages}>>".encode(),
        b"<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>"]
for i, content in enumerate(pages):
    objs.append(f"<</Type/Page/Parent 2 0 R/MediaBox[0 0 {PW:.3f} {PH:.3f}]/Contents {5 + 2*i} 0 R/Resources<</Font<</F1 3 0 R>>>>>>".encode())
    objs.append(b"<</Length %d>>\nstream\n" % len(content) + content + b"\nendstream")
out = bytearray(b"%PDF-1.4\n"); offs = []
for i, o in enumerate(objs, 1):
    offs.append(len(out)); out += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
xref = len(out)
out += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()
for o in offs: out += f"{o:010d} 00000 n \n".encode()
out += f"trailer\n<</Size {len(objs)+1}/Root 1 0 R>>\nstartxref\n{xref}\n%%EOF\n".encode()
open("tag16h5_cube_tags.pdf", "wb").write(out)
