#!/usr/bin/env python3
"""Generate the two top-of-README assets, on-brand and text-accurate:

    00_hero.png        the single share image (ONE SEED -> E8 -> SM + 23 preds)
    verify-demo.gif    an animated terminal running `./verify`

Both are drawn with Pillow (no external SVG renderer needed) so every number is
exact.  Re-run after changing the palette or the verifier output:

    python3 assets/readme/make_readme_assets.py

The GIF text mirrors the real `./verify` output (verification/verify_quick.py);
that script remains the source of truth and is what CI actually runs.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent

# ---- palette (matches the README mermaid diagram) --------------------------
BG        = (11, 18, 32)       # #0b1220
PANEL     = (17, 24, 39)       # #111827
PANEL2    = (13, 20, 35)
BLUE      = (96, 165, 250)     # inputs
PURPLE    = (167, 139, 250)    # anchor
GREEN     = (52, 211, 153)     # E8 hull / pass
PINK      = (244, 114, 182)    # outputs
TEXT      = (226, 232, 240)
DIM       = (130, 144, 166)
WHITE     = (245, 248, 252)
YELLOW    = (250, 204, 21)

# ---- fonts -----------------------------------------------------------------
FONT_DIR = "/System/Library/Fonts"
SUP = FONT_DIR + "/Supplemental"


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def sans(size):      return _font(SUP + "/Arial Unicode.ttf", size)
def sans_bold(size): return _font(SUP + "/Arial Bold.ttf", size)
def mono(size):      return _font(FONT_DIR + "/SFNSMono.ttf", size)


# ---- shared drawing helpers ------------------------------------------------
def soft_glow(size, color, alpha=70):
    """A blurred radial glow layer to sit behind an accent box."""
    from PIL import ImageFilter
    w, h = size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([w * 0.12, h * 0.12, w * 0.88, h * 0.88], fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius=max(w, h) // 6))


def draw_check(d, x, y, s, color=GREEN, w=3):
    d.line([(x, y + s * 0.55), (x + s * 0.38, y + s * 0.9)], fill=color, width=w)
    d.line([(x + s * 0.38, y + s * 0.9), (x + s, y)], fill=color, width=w)


def arrow_down(d, cx, y0, y1, color=DIM, w=2):
    d.line([(cx, y0), (cx, y1)], fill=color, width=w)
    d.polygon([(cx - 6, y1 - 8), (cx + 6, y1 - 8), (cx, y1)], fill=color)


# ===========================================================================
#  1. THE HERO SHARE IMAGE
# ===========================================================================
def build_hero():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)

    # subtle green glow behind the central hull
    from PIL import ImageFilter
    img = img.convert("RGBA")
    img.alpha_composite(soft_glow((W, H), GREEN, 48))
    d = ImageDraw.Draw(img)

    # --- header ------------------------------------------------------------
    d.text((60, 46), "TFPT", font=sans_bold(66), fill=WHITE)
    d.text((66, 120), "T O P O L O G I C A L   F I X E D - P O I N T   T H E O R Y",
           font=sans(15), fill=BLUE)
    tag = "a reality compiler"
    d.text((W - 60, 60), tag, font=sans(22), fill=DIM, anchor="ra")
    d.text((W - 60, 92), "0 free dimensionless dials · only π primitive",
           font=sans(15), fill=DIM, anchor="ra")

    cx = W // 2

    def box(y, h, w, border, title, sub, title_color=None, sub_font=None,
            title_font=None, fill=PANEL):
        x0, x1 = cx - w // 2, cx + w // 2
        d.rounded_rectangle([x0, y, x1, y + h], radius=16, fill=fill,
                            outline=border, width=3)
        d.text((cx, y + h * 0.34), title, font=title_font or sans_bold(26),
               fill=title_color or WHITE, anchor="mm")
        if sub:
            d.text((cx, y + h * 0.70), sub, font=sub_font or mono(22),
                   fill=TEXT, anchor="mm")

    # input seed
    box(168, 84, 560, BLUE, "ONE SEED", "a = (1, 1, 2)      +      \u03c0",
        title_color=BLUE)
    arrow_down(d, cx, 252, 286)

    # E8 hull (emphasised)
    box(286, 96, 560, GREEN, "E8   CONSISTENCY HULL",
        "240 roots  \u00b7  rank 8  \u00b7  dim 248",
        title_color=GREEN, fill=(12, 26, 26))
    # fan-out arrows
    for tx in (cx - 300, cx, cx + 300):
        d.line([(cx, 382), (cx, 400)], fill=DIM, width=2)
        d.line([(cx, 400), (tx, 418)], fill=DIM, width=2)
    for tx in (cx - 300, cx, cx + 300):
        d.polygon([(tx - 5, 418), (tx + 5, 418), (tx, 426)], fill=DIM)

    # three output chips
    chips = [
        ("STANDARD MODEL", "3 generations", PINK),
        ("1/\u03b1 = 137.0359992", "unique Ward root", PINK),
        ("GRAVITY + COSMOLOGY", "G + \u039bg = 8\u03c0\u00b7T", PINK),
    ]
    cw, gap = 350, 18
    total = 3 * cw + 2 * gap
    x = cx - total // 2
    for title, sub, col in chips:
        d.rounded_rectangle([x, 432, x + cw, 512], radius=14, fill=PANEL,
                            outline=col, width=2)
        d.text((x + cw / 2, 458), title, font=sans_bold(21), fill=WHITE, anchor="mm")
        d.text((x + cw / 2, 488), sub, font=mono(18), fill=DIM, anchor="mm")
        x += cw + gap

    # footer strip
    d.line([(60, 556), (W - 60, 556)], fill=(40, 52, 74), width=1)
    foot = "23 FALSIFIABLE PREDICTIONS     \u00b7     3 INDEPENDENT ENGINES: Python \u00b7 Wolfram \u00b7 Lean"
    d.text((cx, 588), foot, font=sans_bold(20), fill=TEXT, anchor="mm")

    img.convert("RGB").save(OUT / "00_hero.png")
    print("wrote", OUT / "00_hero.png")


# ===========================================================================
#  2. THE ANIMATED TERMINAL DEMO
# ===========================================================================
# colour keys for terminal segments
TC = {"dim": DIM, "cyan": BLUE, "green": GREEN, "pink": PINK,
      "white": WHITE, "text": TEXT, "yellow": YELLOW, "bold": WHITE}

CHK = "\u0000CHK"   # sentinel -> draw a vector check mark

# each line is a list of (text, colorkey) segments; CHK draws a check
LINES = [
    [("  TFPT Verification Suite", "bold"), ("   v5.4 \u00b7 reality compiler", "dim")],
    [("RULE", "dim")],
    [("  Input", "cyan")],
    [("  parabolic anchor ", "text"), (".............. ", "dim"), ("a = (1, 1, 2)", "white")],
    [("  transcendental ", "text"), ("................ ", "dim"), ("\u03c0", "white")],
    [("  \u2192 fixes c3 = 1/(8\u03c0) and g_car = 5 \u2014 no free dimensionless dial", "dim")],
    [("", "dim")],
    [("  Compiler closure", "cyan")],
    [("  E8 roots ", "text"), ("...................... ", "dim"), ("240", "white"), ("      ", "dim"), (CHK, "green")],
    [("  E8 dimension ", "text"), (".................. ", "dim"), ("248", "white"), ("      ", "dim"), (CHK, "green")],
    [("  rank ", "text"), (".......................... ", "dim"), ("8", "white"), ("        ", "dim"), (CHK, "green")],
    [("  gauge structure ", "text"), ("............... ", "dim"), ("SU(3)\u00d7SU(2)\u00d7U(1)", "white"), ("   ", "dim"), (CHK, "green")],
    [("  fermion generations ", "text"), ("........... ", "dim"), ("3", "white"), ("        ", "dim"), (CHK, "green")],
    [("  \u03b1\u207b\u00b9 (unique Ward root) ", "text"), ("...... ", "dim"), ("137.0359992", "pink"), ("   ", "dim"), (CHK, "green")],
    [("  frozen registry (locks) ", "text"), ("..... ", "dim"), ("31/31", "white"), ("    ", "dim"), (CHK, "green")],
    [("", "dim")],
    [("  Independent engines", "cyan")],
    [("  Python (this run) ", "text"), ("........... ", "dim"), ("PASS", "green"), ("  89 checks", "dim")],
    [("  Wolfram Engine ", "text"), ("............... ", "dim"), ("116/116", "white"), ("   \u2192 --wolfram", "dim")],
    [("  Lean 4 (no sorry/admit) ", "text"), (".... ", "dim"), ("proven", "white"), ("    \u2192 --lean", "dim")],
    [("", "dim")],
    [("  ", "dim"), (CHK, "green"), (" CORE CLAIMS VERIFIED", "green"), ("  in 0.10s \u00b7 23 predictions \u00b7 --full", "dim")],
]


def _render_terminal(reveal, typed, cursor):
    W, H = 940, 640
    img = Image.new("RGB", (W, H), (6, 10, 20))
    d = ImageDraw.Draw(img)
    # window chrome
    d.rounded_rectangle([16, 16, W - 16, H - 16], radius=14, fill=(10, 15, 26),
                        outline=(38, 48, 70), width=1)
    d.rounded_rectangle([16, 16, W - 16, 56], radius=14, fill=(18, 24, 38))
    d.rectangle([16, 44, W - 16, 56], fill=(18, 24, 38))
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([40 + i * 26, 30, 54 + i * 26, 44], fill=col)
    d.text((W // 2, 36), "tfpt \u2014 ./verify", font=mono(15), fill=DIM, anchor="mm")

    f = mono(18)
    ch = d.textlength("M", font=f)
    x0, y = 40, 76
    lh = 24

    # the typed command line
    cmd = "$ " + typed
    d.text((x0, y), "$ ", font=f, fill=GREEN)
    d.text((x0 + 2 * ch, y), typed, font=f, fill=WHITE)
    if cursor and reveal == 0:
        cxp = x0 + (2 + len(typed)) * ch
        d.rectangle([cxp, y + 2, cxp + ch, y + 20], fill=TEXT)
    y += lh

    for li in range(reveal):
        line = LINES[li]
        x = x0
        for text, key in line:
            if text == "RULE":
                d.line([(x0, y + 11), (W - 48, y + 11)], fill=(40, 52, 74), width=1)
                continue
            if text == CHK:
                draw_check(d, x, y + 2, 14, GREEN, 2)
                x += 3 * ch
                continue
            d.text((x, y), text, font=f, fill=TC[key])
            x += d.textlength(text, font=f)
        y += lh

    return img


def build_gif():
    frames, durations = [], []

    cmd = "./verify"
    # phase 1: type the command
    for i in range(1, len(cmd) + 1):
        frames.append(_render_terminal(0, cmd[:i], cursor=True))
        durations.append(70)
    frames.append(_render_terminal(0, cmd, cursor=True)); durations.append(350)

    # phase 2: reveal output lines
    for r in range(1, len(LINES) + 1):
        frames.append(_render_terminal(r, cmd, cursor=False))
        # small pauses at section headers, faster on plain rows
        durations.append(150 if LINES[r - 1] and LINES[r - 1][0][1] == "cyan" else 90)

    # phase 3: hold the final frame, then loop
    frames.append(_render_terminal(len(LINES), cmd, cursor=False))
    durations.append(2600)

    frames[0].save(
        OUT / "verify-demo.gif", save_all=True, append_images=frames[1:],
        duration=durations, loop=0, optimize=True, disposal=2,
    )
    print("wrote", OUT / "verify-demo.gif", f"({len(frames)} frames)")


if __name__ == "__main__":
    build_hero()
    build_gif()
