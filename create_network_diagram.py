#!/usr/bin/env python3
"""
Network View Diagram - ATLAS.ti authentic style
Outputs: PDF (A3 Landscape) ready for thesis appendix

Visual style:
- All nodes are rounded rectangles (like ATLAS.ti)
- Color-coded by theme group
- Connector lines with relationship labels on the line
- Clean, organic layout without overlap
"""
import math
import sys
sys.path.insert(0, '.')
from pdf_writer import PDFWriter

# ============================================================
# DATA: Themes -> Axial Codes -> Representative Open Codes
# ============================================================

themes_data = [
    {
        "id": "T1",
        "label": "Keterbatasan Sistem Pencatatan\nPerilaku Siswa yang Berjalan",
        "color": (1.0, 0.92, 0.55),       # warm yellow
        "border": (0.78, 0.65, 0.0),
        "axial": [
            {"label": "Pencatatan perilaku\nberbasis manual",
             "codes": ["Pencatatan manual", "Buku absensi/jurnal",
                       "Buku anekdot", "Guru kelas PJ utama",
                       "Data perilaku belum digital"]},
            {"label": "Format pencatatan\ntidak terstandar",
             "codes": ["Format tidak seragam", "Bergantung kebiasaan guru",
                       "Format tidak baku", "Keterlambatan belum detail"]},
            {"label": "Keterbatasan dokumentasi\nperilaku positif & prestasi",
             "codes": ["Perilaku positif belum\nterdokumentasi",
                       "Belum ada tempat khusus\nperilaku positif",
                       "Fokus pelanggaran"]},
            {"label": "Kesulitan pengelolaan\ndan pencarian data",
             "codes": ["Data tersebar", "Data sulit dicari",
                       "Data rawan hilang/rusak", "Rekapitulasi lama"]},
        ]
    },
    {
        "id": "T2",
        "label": "Ketidakefisienan Alur Pelaporan\ndan Komunikasi",
        "color": (0.73, 0.88, 1.0),       # light blue
        "border": (0.14, 0.44, 0.64),
        "axial": [
            {"label": "Alur pelaporan\ntidak efisien",
             "codes": ["Alur pelaporan konvensional",
                       "Pengawasan manajerial\nkurang praktis",
                       "Data tidak terpusat", "Pelaporan situasional"]},
            {"label": "Komunikasi orang tua\nbersifat insidental",
             "codes": ["Komunikasi orang tua manual",
                       "Informasi terlambat\nke orang tua",
                       "Notifikasi perlu diatur",
                       "Kendala komunikasi\norang tua"]},
        ]
    },
    {
        "id": "T3",
        "label": "Penghargaan & Pembinaan Karakter\nBelum Terdokumentasi Sistematis",
        "color": (0.75, 0.94, 0.80),       # soft green
        "border": (0.12, 0.52, 0.29),
        "axial": [
            {"label": "Penghargaan belum\nterstruktur",
             "codes": ["Penghargaan sederhana",
                       "Penghargaan belum\nterdokumentasi",
                       "Reward spontan",
                       "Penghargaan terstruktur\nbelum berjalan"]},
            {"label": "Pembinaan karakter melalui\npembiasaan harian",
             "codes": ["Pembinaan karakter harian",
                       "Teguran bertahap",
                       "Tindak lanjut belum\nterdokumentasi",
                       "Rekam jejak pembinaan\npenting",
                       "Pembinaan melalui\npembiasaan"]},
        ]
    },
    {
        "id": "T4",
        "label": "Kebutuhan Fitur & Fungsi Sistem\nInformasi Berbasis Website",
        "color": (1.0, 0.85, 0.78),       # salmon
        "border": (0.75, 0.22, 0.17),
        "axial": [
            {"label": "Kebutuhan fitur dan\nfungsi sistem informasi",
             "codes": ["Kebutuhan fitur lengkap",
                       "Kebutuhan rekap otomatis",
                       "Kebutuhan pencatatan cepat",
                       "Sistem poin otomatis",
                       "Kebutuhan fitur pencarian",
                       "Kebutuhan laporan otomatis",
                       "Pembagian akses pengguna",
                       "Kebutuhan keamanan data",
                       "Tampilan sederhana"]},
        ]
    },
    {
        "id": "T5",
        "label": "Kesiapan, Tantangan, dan Dukungan\nImplementasi Sistem",
        "color": (0.87, 0.80, 0.93),       # lavender
        "border": (0.42, 0.20, 0.51),
        "axial": [
            {"label": "Ketersediaan infrastruktur\ndan kesiapan teknis",
             "codes": ["Internet tersedia tapi fluktuatif",
                       "Perangkat tersedia",
                       "Literasi teknologi guru\nbervariasi",
                       "Belum pernah pakai\naplikasi khusus"]},
            {"label": "Kekhawatiran & hambatan\nimplementasi",
             "codes": ["Kekhawatiran kesiapan guru",
                       "Kekhawatiran jaringan internet",
                       "Hambatan kebiasaan manual",
                       "Kemampuan teknologi\ntidak merata"]},
            {"label": "Dukungan dan\nkesiapan sekolah",
             "codes": ["Dukungan thd sistem website",
                       "Dukungan sekolah",
                       "Implementasi bertahap",
                       "Dukungan teknis operator",
                       "Sistem diterima jika sederhana"]},
        ]
    },
]

inter_theme_links = [
    ("T1", "T2", "is cause of"),
    ("T1", "T4", "is cause of"),
    ("T2", "T4", "is cause of"),
    ("T3", "T4", "is associated with"),
    ("T4", "T5", "is associated with"),
]

# ============================================================
# HELPERS
# ============================================================

def node_size(text, fs, px=10, py=6):
    lines = text.split('\n')
    cw = fs * 0.47
    w = max(len(l) for l in lines) * cw + px * 2
    h = len(lines) * fs * 1.25 + py * 2
    return max(w, 70), max(h, 18)

def edge_pt(cx, cy, w, h, tx, ty):
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    hw, hh = w/2, h/2
    if dx == 0:
        return cx, cy + (hh if dy > 0 else -hh)
    if dy == 0:
        return cx + (hw if dx > 0 else -hw), cy
    s = min(hw/abs(dx), hh/abs(dy))
    return cx + dx*s, cy + dy*s

# ============================================================
# PDF GENERATION - A3 Landscape
# ============================================================

PW = 1190.55  # A3 width in pt
PH = 841.89   # A3 height in pt

pdf = PDFWriter(PW, PH)

# White background
pdf.set_color(1, 1, 1)
pdf.draw_rect(0, 0, PW, PH, fill=True, stroke=False)

# Title
pdf.set_color(0.15, 0.15, 0.15)
pdf.draw_text_centered(PW/2, 22, "NETWORK VIEW", size=16, bold=True)
pdf.set_color(0.3, 0.3, 0.3)
pdf.draw_text_centered(PW/2, 38, "Pengembangan Sistem Informasi Pemantauan Perilaku Siswa Berbasis Website", size=8)
pdf.draw_text_centered(PW/2, 49, "dalam Mendukung Manajemen Pembinaan Karakter di Sekolah Dasar", size=8)

# ============================================================
# POSITIONS - carefully laid out to prevent overlap
# Theme nodes are central hubs, axial codes radiate out,
# open codes radiate further out from axial codes.
#
# Layout zones (A3 Landscape):
#   T1: top-left quadrant     (x: 80-450, y: 80-380)
#   T2: top-right quadrant    (x: 740-1110, y: 80-380)
#   T3: bottom-left quadrant  (x: 80-450, y: 490-780)
#   T4: center                (x: 450-740, y: 300-550)
#   T5: bottom-right quadrant (x: 740-1110, y: 490-780)
# ============================================================

theme_pos = {
    "T1": (250, 210),
    "T2": (940, 210),
    "T3": (250, 650),
    "T4": (595, 430),
    "T5": (940, 650),
}

# Angles (degrees) and distances for axial codes from theme center
axial_config = {
    "T1": [(135, 130), (180, 130), (225, 130), (270, 130)],
    "T2": [(0, 130), (315, 130)],
    "T3": [(180, 130), (225, 130)],
    "T4": [(270, 145)],
    "T5": [(0, 130), (315, 130), (45, 130)],
}

# Open code distance from axial
OC_DIST = 68

theme_nodes = {}  # tid -> (cx, cy, w, h)

def draw_node(cx, cy, text, fs, px, py, fill_rgb, border_rgb, lw=0.8, bold=False):
    """Draw an ATLAS.ti style rounded-rect node"""
    w, h = node_size(text, fs, px, py)
    pdf.save_state()
    pdf.set_color(*fill_rgb)
    pdf.set_stroke_color(*border_rgb)
    pdf.set_line_width(lw)
    r = min(4, h/4)
    pdf.draw_rounded_rect(cx - w/2, cy - h/2, w, h, r, fill=True, stroke=True)
    pdf.set_color(0.1, 0.1, 0.1)
    pdf.draw_text_centered(cx, cy, text, size=fs, bold=bold)
    pdf.restore_state()
    return w, h

def draw_link(x1, y1, x2, y2, label, color=(0.4, 0.4, 0.4), lw=0.5, dashed=False):
    """Draw a link line with label in the middle (ATLAS.ti style)"""
    pdf.save_state()
    pdf.set_stroke_color(*color)
    pdf.set_line_width(lw)
    if dashed:
        pdf.set_dash(3, 2)
    pdf.draw_line(x1, y1, x2, y2)
    if dashed:
        pdf.clear_dash()
    # Arrow at end
    pdf.set_color(*color)
    pdf.draw_arrow(x1, y1, x2, y2, size=3)
    pdf.restore_state()
    
    # Label on line
    mx, my = (x1+x2)/2, (y1+y2)/2
    lbl_w = len(label) * 3.2 + 6
    pdf.save_state()
    pdf.set_color(1, 1, 1)
    pdf.draw_rect(mx - lbl_w/2, my - 4.5, lbl_w, 8, fill=True, stroke=False)
    pdf.set_color(*color)
    pdf.draw_text_centered(mx, my, label, size=4.5)
    pdf.restore_state()

# ============================================================
# RENDER ALL NODES AND CONNECTIONS
# ============================================================

for theme in themes_data:
    tid = theme["id"]
    tcx, tcy = theme_pos[tid]
    tc = theme["color"]
    tb = theme["border"]
    
    # Draw theme node (larger, bold, colored)
    tw, th = draw_node(tcx, tcy, theme["label"], 7.5, 14, 8, tc, tb, lw=1.2, bold=True)
    theme_nodes[tid] = (tcx, tcy, tw, th)
    
    configs = axial_config[tid]
    for ai, axial in enumerate(theme["axial"]):
        if ai >= len(configs):
            break
        ang_deg, dist = configs[ai]
        rad = math.radians(ang_deg)
        acx = tcx + dist * math.cos(rad)
        acy = tcy + dist * math.sin(rad)
        
        # Draw axial node (medium, colored lighter)
        lighter = tuple(min(1.0, c*0.3 + 0.7) for c in tc)
        aw, ah = draw_node(acx, acy, axial["label"], 6, 8, 5,
                           lighter, tb, lw=0.7, bold=True)
        
        # Link theme -> axial
        p1 = edge_pt(tcx, tcy, tw, th, acx, acy)
        p2 = edge_pt(acx, acy, aw, ah, tcx, tcy)
        draw_link(p1[0], p1[1], p2[0], p2[1], "is part of",
                  color=tb, lw=0.6)
        
        # Open codes around axial
        codes = axial["codes"]
        nc = len(codes)
        base_dir = math.atan2(acy - tcy, acx - tcx)
        
        # Fan spread
        spread = math.pi * (0.5 if nc <= 3 else 0.65 if nc <= 5 else 0.8)
        
        for ci, ct in enumerate(codes):
            if nc == 1:
                ca = base_dir
            else:
                ca = base_dir - spread/2 + spread * ci / (nc - 1)
            
            r = OC_DIST + (ci % 2) * 10
            ocx = acx + r * math.cos(ca)
            ocy = acy + r * math.sin(ca)
            
            # Draw open code node (small, white/light gray)
            ow, oh = draw_node(ocx, ocy, ct, 5, 6, 3,
                               (1.0, 1.0, 1.0), (0.6, 0.6, 0.6), lw=0.4)
            
            # Link axial -> open code
            p1 = edge_pt(acx, acy, aw, ah, ocx, ocy)
            p2 = edge_pt(ocx, ocy, ow, oh, acx, acy)
            pdf.save_state()
            pdf.set_stroke_color(0.7, 0.7, 0.7)
            pdf.set_line_width(0.3)
            pdf.draw_line(p1[0], p1[1], p2[0], p2[1])
            pdf.restore_state()

# ============================================================
# INTER-THEME CONNECTIONS (dashed, with relationship label)
# ============================================================

for t1_id, t2_id, label in inter_theme_links:
    n1 = theme_nodes[t1_id]
    n2 = theme_nodes[t2_id]
    p1 = edge_pt(n1[0], n1[1], n1[2], n1[3], n2[0], n2[1])
    p2 = edge_pt(n2[0], n2[1], n2[2], n2[3], n1[0], n1[1])
    draw_link(p1[0], p1[1], p2[0], p2[1], label,
              color=(0.7, 0.2, 0.15), lw=0.7, dashed=True)

# ============================================================
# LEGEND (bottom-right corner, compact)
# ============================================================

lx, ly = PW - 200, PH - 70
pdf.save_state()
pdf.set_color(0.98, 0.98, 0.98)
pdf.set_stroke_color(0.8, 0.8, 0.8)
pdf.set_line_width(0.4)
pdf.draw_rounded_rect(lx, ly, 185, 55, 3, fill=True, stroke=True)
pdf.set_color(0.15, 0.15, 0.15)
pdf.draw_text(lx + 5, ly + 10, "Legenda:", size=5.5, bold=True)
# Theme
pdf.set_color(1.0, 0.92, 0.55)
pdf.set_stroke_color(0.5, 0.5, 0.5)
pdf.draw_rounded_rect(lx+5, ly+16, 20, 8, 2, fill=True, stroke=True)
pdf.set_color(0.15, 0.15, 0.15)
pdf.draw_text(lx+30, ly+22, "= Tema (Theme)", size=5)
# Axial
pdf.set_color(0.9, 0.95, 0.98)
pdf.draw_rounded_rect(lx+5, ly+28, 20, 8, 2, fill=True, stroke=True)
pdf.set_color(0.15, 0.15, 0.15)
pdf.draw_text(lx+30, ly+34, "= Axial Code (Kategori)", size=5)
# Open code
pdf.set_color(1, 1, 1)
pdf.draw_rounded_rect(lx+5, ly+40, 20, 8, 2, fill=True, stroke=True)
pdf.set_color(0.15, 0.15, 0.15)
pdf.draw_text(lx+30, ly+46, "= Open Code", size=5)
# Dashed line
pdf.set_stroke_color(0.7, 0.2, 0.15)
pdf.set_line_width(0.6)
pdf.set_dash(3, 2)
pdf.draw_line(lx+100, ly+10, lx+125, ly+10)
pdf.clear_dash()
pdf.set_color(0.15, 0.15, 0.15)
pdf.draw_text(lx+130, ly+12, "= Relasi antar Tema", size=5)
pdf.restore_state()

# Footer
pdf.set_color(0.5, 0.5, 0.5)
pdf.draw_text_centered(PW/2, PH - 12,
    "Sumber: Wawancara KS, WK6, WK2, OS | SD Negeri 04 Jatigunung | Peneliti: Ridwan Alif Adi Nugraha", size=5.5)

# ============================================================
# SAVE PDF
# ============================================================
pdf_bytes = pdf.build()
with open("Network_View_Diagram_ATLASti.pdf", "wb") as f:
    f.write(pdf_bytes)

print("OK - Network View Diagram (ATLAS.ti style) created!")
print(f"  Output: Network_View_Diagram_ATLASti.pdf")
print(f"  Format: A3 Landscape ({PW:.0f} x {PH:.0f} pt)")
total_axial = sum(len(t['axial']) for t in themes_data)
total_open = sum(len(a['codes']) for t in themes_data for a in t['axial'])
print(f"  Content: {len(themes_data)} Themes, {total_axial} Axial Codes, {total_open} Open Codes")
