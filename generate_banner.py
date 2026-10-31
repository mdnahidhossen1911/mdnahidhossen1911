import os
import math
from PIL import Image, ImageDraw, ImageFont

WIDTH = 920
HEIGHT = 270
NUM_FRAMES = 32
DURATION = 85  # ms per frame (~12 fps)

# Fonts
font_dir = r"C:\Windows\Fonts"
title_font = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 18)
sub_font = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 11)
code_font = ImageFont.truetype(os.path.join(font_dir, "consola.ttf"), 12)
code_font_bold = ImageFont.truetype(os.path.join(font_dir, "consolab.ttf"), 12)
badge_font = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 10)
center_font = ImageFont.truetype(os.path.join(font_dir, "consolab.ttf"), 11)

# Color Palette (Dark Theme / GitHub Tokyonight style)
BG_COLOR = (13, 17, 23)           # #0d1117
PANEL_BG = (22, 27, 34)           # #161b22
PANEL_BORDER = (48, 54, 61)       # #30363d
FLUTTER_BLUE = (2, 117, 194)      # #0275c2
FLUTTER_CYAN = (64, 208, 253)     # #40d0fd
GO_CYAN = (0, 173, 216)           # #00add8
GO_DARK = (0, 125, 156)           # #007d9c
TEXT_WHITE = (240, 246, 252)
TEXT_MUTED = (139, 148, 158)
KW_PINK = (255, 123, 114)         # #ff7b72
FN_PURPLE = (210, 168, 255)       # #d2a8ff
VAR_BLUE = (121, 192, 255)        # #79c0ff
STR_GREEN = (126, 231, 135)       # #7ee787
NUM_ORANGE = (255, 166, 87)       # #ffa657

def draw_flutter_logo(draw, x, y, scale=1.0):
    # Origami-style Flutter logo using polygons
    # Top right chevron
    p1 = [(x + 18*scale, y + 2*scale), (x + 28*scale, y + 12*scale), (x + 21*scale, y + 19*scale), (x + 11*scale, y + 9*scale)]
    draw.polygon(p1, fill=(2, 86, 155))
    # Bottom chevron
    p2 = [(x + 8*scale, y + 12*scale), (x + 15*scale, y + 19*scale), (x + 5*scale, y + 29*scale), (x - 2*scale, y + 22*scale)]
    draw.polygon(p2, fill=(1, 117, 194))
    # Mid triangle
    p3 = [(x + 15*scale, y + 19*scale), (x + 23*scale, y + 27*scale), (x + 15*scale, y + 29*scale)]
    draw.polygon(p3, fill=(2, 86, 155))
    # Bottom right chevron
    p4 = [(x + 15*scale, y + 29*scale), (x + 23*scale, y + 27*scale), (x + 28*scale, y + 32*scale), (x + 20*scale, y + 40*scale), (x + 5*scale, y + 29*scale)]
    draw.polygon(p4, fill=(64, 208, 253))

def draw_go_logo(draw, x, y, scale=1.0):
    # Stylized Go letters
    # 'G'
    draw.rounded_rectangle([x, y + 6*scale, x + 24*scale, y + 34*scale], radius=7*scale, outline=GO_CYAN, width=int(4*scale))
    draw.line([x + 14*scale, y + 20*scale, x + 24*scale, y + 20*scale], fill=GO_CYAN, width=int(4*scale))
    # 'O'
    draw.ellipse([x + 28*scale, y + 6*scale, x + 52*scale, y + 34*scale], outline=GO_CYAN, width=int(4*scale))
    # Speed trails behind G
    draw.line([x - 10*scale, y + 12*scale, x - 2*scale, y + 12*scale], fill=GO_CYAN, width=2)
    draw.line([x - 14*scale, y + 20*scale, x - 4*scale, y + 20*scale], fill=GO_CYAN, width=2)
    draw.line([x - 8*scale, y + 28*scale, x - 2*scale, y + 28*scale], fill=GO_CYAN, width=2)

frames = []

for frame_idx in range(NUM_FRAMES):
    progress = frame_idx / NUM_FRAMES
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Subtle Background Grid Points
    for gx in range(20, WIDTH, 36):
        for gy in range(20, HEIGHT, 36):
            draw.point((gx, gy), fill=(24, 30, 40))

    # Ambient Top Glowing Border Line
    glow_pos = int((progress * (WIDTH + 200)) - 100)
    draw.line([(0, 0), (WIDTH, 0)], fill=(30, 36, 45), width=2)
    draw.line([(0, HEIGHT - 1), (WIDTH, HEIGHT - 1)], fill=(30, 36, 45), width=2)
    for g in range(120):
        intensity = math.sin((g / 120) * math.pi)
        col_val = int(intensity * 180)
        px = glow_pos + g - 60
        if 0 <= px < WIDTH:
            draw.point((px, 0), fill=(col_val // 2, col_val, int(col_val * 1.2)))
            draw.point((px, HEIGHT - 1), fill=(col_val // 2, col_val, int(col_val * 1.2)))

    # -------------------------------------------------------------
    # 2. LEFT PANEL: FLUTTER & DART
    # -------------------------------------------------------------
    p_left = (24, 20, 385, HEIGHT - 20)
    # Border glow pulse
    pulse_fl = 0.5 + 0.5 * math.sin(progress * 2 * math.pi)
    border_fl = (
        int(PANEL_BORDER[0] + (FLUTTER_BLUE[0] - PANEL_BORDER[0]) * 0.4 * pulse_fl),
        int(PANEL_BORDER[1] + (FLUTTER_BLUE[1] - PANEL_BORDER[1]) * 0.4 * pulse_fl),
        int(PANEL_BORDER[2] + (FLUTTER_BLUE[2] - PANEL_BORDER[2]) * 0.4 * pulse_fl),
    )
    draw.rounded_rectangle(p_left, radius=12, fill=PANEL_BG, outline=border_fl, width=1)

    # Header
    draw_flutter_logo(draw, 42, 34, scale=0.85)
    draw.text((76, 32), "FLUTTER & DART", fill=TEXT_WHITE, font=title_font)
    draw.text((76, 54), "Mobile Client • Reactive MVVM", fill=FLUTTER_CYAN, font=sub_font)

    # Simulated Code Snippet (Flutter)
    code_y = 80
    cursor_on = (frame_idx % 12) < 6
    cur_char = "_" if cursor_on else ""

    fl_lines = [
        [("class ", KW_PINK), ("MobileApp ", VAR_BLUE), ("extends ", KW_PINK), ("StatelessWidget", FN_PURPLE)],
        [("  Widget ", FN_PURPLE), ("build", VAR_BLUE), ("(BuildContext ctx) {", TEXT_WHITE)],
        [("    return ", KW_PINK), ("CleanMVVMScaffold(", VAR_BLUE)],
        [("      viewModel: ", TEXT_WHITE), ("AppProvider()", FN_PURPLE), (",", TEXT_WHITE)],
        [("      cache: ", TEXT_WHITE), ("OfflineFirstCache()", STR_GREEN), (cur_char, FLUTTER_CYAN)],
        [("    );", TEXT_WHITE)],
    ]
    for line in fl_lines:
        cur_x = 42
        for seg_text, seg_col in line:
            draw.text((cur_x, code_y), seg_text, fill=seg_col, font=code_font)
            cur_x += int(draw.textlength(seg_text, font=code_font))
        code_y += 18

    # Bottom Pills (Badges)
    fl_badges = ["Clean MVVM", "60/120 FPS", "Offline-First", "Material 3"]
    bx = 42
    for b_text in fl_badges:
        bw = int(draw.textlength(b_text, font=badge_font)) + 14
        draw.rounded_rectangle([bx, HEIGHT - 46, bx + bw, HEIGHT - 28], radius=6, fill=(16, 32, 54), outline=(2, 117, 194), width=1)
        draw.text((bx + 7, HEIGHT - 44), b_text, fill=(120, 200, 255), font=badge_font)
        bx += bw + 8

    # -------------------------------------------------------------
    # 3. RIGHT PANEL: PURE GOLANG
    # -------------------------------------------------------------
    p_right = (535, 20, WIDTH - 24, HEIGHT - 20)
    pulse_go = 0.5 + 0.5 * math.cos(progress * 2 * math.pi)
    border_go = (
        int(PANEL_BORDER[0] + (GO_CYAN[0] - PANEL_BORDER[0]) * 0.4 * pulse_go),
        int(PANEL_BORDER[1] + (GO_CYAN[1] - PANEL_BORDER[1]) * 0.4 * pulse_go),
        int(PANEL_BORDER[2] + (GO_CYAN[2] - PANEL_BORDER[2]) * 0.4 * pulse_go),
    )
    draw.rounded_rectangle(p_right, radius=12, fill=PANEL_BG, outline=border_go, width=1)

    # Header
    draw_go_logo(draw, 560, 32, scale=0.85)
    draw.text((618, 32), "PURE GOLANG", fill=TEXT_WHITE, font=title_font)
    draw.text((618, 54), "net/http Engine • Zero Bloat", fill=GO_CYAN, font=sub_font)

    # Simulated Code Snippet (Go)
    code_y = 80
    go_lines = [
        [("func ", KW_PINK), ("StartEngine", FN_PURPLE), ("() {", TEXT_WHITE)],
        [("  mux := ", TEXT_WHITE), ("http.NewServeMux", FN_PURPLE), ("()", TEXT_WHITE)],
        [("  mux.", TEXT_WHITE), ("HandleFunc", VAR_BLUE), ("(", TEXT_WHITE), ('"/api/v1"', STR_GREEN), (", h)", TEXT_WHITE)],
        [("  srv := &", TEXT_WHITE), ("http.Server", FN_PURPLE), ("{Handler: mux}", TEXT_WHITE)],
        [("  log.", TEXT_WHITE), ("Fatal", VAR_BLUE), ("(srv.ListenAndServe())", TEXT_WHITE), (cur_char, GO_CYAN)],
        [("}", TEXT_WHITE)],
    ]
    for line in go_lines:
        cur_x = 555
        for seg_text, seg_col in line:
            draw.text((cur_x, code_y), seg_text, fill=seg_col, font=code_font)
            cur_x += int(draw.textlength(seg_text, font=code_font))
        code_y += 18

    # Bottom Pills (Badges)
    go_badges = ["Pure net/http", "Goroutines", "Raw SQL / ORM", "Microservices"]
    bx = 555
    for b_text in go_badges:
        bw = int(draw.textlength(b_text, font=badge_font)) + 14
        draw.rounded_rectangle([bx, HEIGHT - 46, bx + bw, HEIGHT - 28], radius=6, fill=(10, 38, 48), outline=(0, 173, 216), width=1)
        draw.text((bx + 7, HEIGHT - 44), b_text, fill=(100, 230, 255), font=badge_font)
        bx += bw + 8

    # -------------------------------------------------------------
    # 4. CENTER BRIDGE: DYNAMIC DATA STREAM
    # -------------------------------------------------------------
    center_y = HEIGHT // 2
    x_start = 385
    x_end = 535
    wire_length = x_end - x_start

    # Connection bus lines
    draw.line([(x_start, center_y - 12), (x_end, center_y - 12)], fill=(35, 42, 54), width=2)
    draw.line([(x_start, center_y + 12), (x_end, center_y + 12)], fill=(35, 42, 54), width=2)

    # Animated Packets: Left to Right (Flutter Requests -> Go)
    for p_offset in [0.0, 0.5]:
        p_prog = (progress + p_offset) % 1.0
        px = x_start + int(p_prog * wire_length)
        draw.circle((px, center_y - 12), radius=3, fill=FLUTTER_CYAN)
        # Tail
        tail_x = px - 6
        if x_start <= tail_x <= x_end:
            draw.line([(tail_x, center_y - 12), (px, center_y - 12)], fill=FLUTTER_BLUE, width=2)

    # Animated Packets: Right to Left (Go Responses -> Flutter)
    for p_offset in [0.25, 0.75]:
        p_prog = (1.0 - ((progress + p_offset) % 1.0))
        px = x_start + int(p_prog * wire_length)
        draw.circle((px, center_y + 12), radius=3, fill=GO_CYAN)
        tail_x = px + 6
        if x_start <= tail_x <= x_end:
            draw.line([(px, center_y + 12), (tail_x, center_y + 12)], fill=GO_DARK, width=2)

    # Center Badge: REST / JSON / HTTP
    cb_w, cb_h = 104, 30
    cb_x = (WIDTH - cb_w) // 2
    cb_y = center_y - (cb_h // 2)
    draw.rounded_rectangle([cb_x, cb_y, cb_x + cb_w, cb_y + cb_h], radius=7, fill=(18, 24, 32), outline=(56, 139, 253), width=1)
    badge_label = "REST • JSON"
    bl_w = int(draw.textlength(badge_label, font=center_font))
    draw.text((cb_x + (cb_w - bl_w) // 2, cb_y + 8), badge_label, fill=(240, 246, 252), font=center_font)

    # Sub-caption under center badge
    sub_c = "< SYNC >"
    sc_w = int(draw.textlength(sub_c, font=badge_font))
    draw.text(((WIDTH - sc_w) // 2, cb_y + cb_h + 8), sub_c, fill=TEXT_MUTED, font=badge_font)

    # Convert to adaptive palette for crisp GIF output
    pal_img = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=128)
    frames.append(pal_img)

# Save animated GIF
out_path = os.path.join("assets", "flutter-golang.gif")
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=DURATION,
    loop=0,
    optimize=True
)

file_size_kb = os.path.getsize(out_path) / 1024
print(f"Generated {out_path} ({len(frames)} frames, {file_size_kb:.1f} KB)")

