#!/usr/bin/env python3
"""
Network View Diagram ala ATLAS.ti - Output PDF & SVG
Compact, structured layout for thesis appendix.
"""
import math
import sys
sys.path.insert(0, '.')
from pdf_writer import PDFWriter

# ============================================================
# DATA
# ============================================================

themes_data = [
    {
        "id": "T1",
        "label": "Keterbatasan Sistem\nPencatatan Perilaku Siswa\nyang Berjalan",
        "color": (1.0, 0.95, 0.7),
        "border": (0.7, 0.55, 0.05),
        "axial": [
            {"label": "Pencatatan perilaku\nberbasis manual",
             "codes": ["Pencatatan manual", "Buku absensi/jurnal", "Buku anekdot",
                       "Guru kelas PJ utama", "Data perilaku belum digital"]},
            {"label": "Format pencatatan\ntidak terstandar",
             "codes": ["Format tidak seragam", "Bergantung kebiasaan guru",
                       "Format tidak baku", "Keterlambatan belum detail"]},
            {"label": "Keterbatasan dokumentasi\nperilaku positif & prestasi",
             "codes": ["Perilaku positif belum\nterdokumentasi", "Belum ada tempat\nkhusus perilaku positif",
                       "Fokus pelanggaran"]},
            {"label": "Kesulitan pengelolaan\ndan pencarian data",
             "codes": ["Data tersebar", "Data sulit dicari", "Data rawan hilang/rusak",
                       "Rekapitulasi lama"]},
        ]
    },
    {
        "id": "T2",
        "label": "Ketidakefisienan Alur\nPelaporan dan Komunikasi",
        "color": (0.82, 0.93, 1.0),
        "border": (0.14, 0.44, 0.64),
        "axial": [
            {"label": "Alur pelaporan\ntidak efisien",
             "codes": ["Alur pelaporan konvensional", "Pengawasan manajerial\nkurang praktis",
                       "Data tidak terpusat", "Pelaporan situasional"]},
            {"label": "Komunikasi orang tua\nbersifat insidental",
             "codes": ["Komunikasi orang tua\nmanual", "Informasi terlambat\nke orang tua",
                       "Notifikasi orang tua\nperlu diatur", "Kendala komunikasi\ndengan orang tua"]},
        ]
    },
    {
        "id": "T3",
        "label": "Penghargaan & Pembinaan\nKarakter Belum\nTerdokumentasi Sistematis",
        "color": (0.84, 0.96, 0.88),
        "border": (0.12, 0.52, 0.29),
        "axial": [
            {"label": "Penghargaan belum\nterstruktur",
             "codes": ["Penghargaan sederhana", "Penghargaan belum\nterdokumentasi",
                       "Reward spontan", "Penghargaan terstruktur\nbelum berjalan"]},
            {"label": "Pembinaan karakter\nmelalui pembiasaan harian",
             "codes": ["Pembinaan karakter harian", "Teguran bertahap",
                       "Tindak lanjut belum\nterdokumentasi", "Rekam jejak\npembinaan penting",
                       "Pembinaan melalui\npembiasaan"]},
        ]
    },
    {
        "id": "T4",
        "label": "Kebutuhan Fitur & Fungsi\nSistem Informasi\nBerbasis Website",
        "color": (0.99, 0.92, 0.88),
        "border": (0.75, 0.22, 0.17),
        "axial": [
            {"label": "Kebutuhan fitur dan\nfungsi sistem informasi",
             "codes": ["Kebutuhan fitur lengkap", "Kebutuhan rekap otomatis",
                       "Kebutuhan pencatatan cepat", "Sistem poin otomatis",
                       "Kebutuhan fitur pencarian", "Kebutuhan laporan otomatis",
                       "Pembagian akses pengguna", "Kebutuhan keamanan data",
                       "Tampilan sederhana"]},
        ]
    },
    {
        "id": "T5",
        "label": "Kesiapan, Tantangan,\ndan Dukungan\nImplementasi Sistem",
        "color": (0.91, 0.85, 0.93),
        "border": (0.42, 0.20, 0.51),
        "axial": [
            {"label": "Ketersediaan infrastruktur\ndan kesiapan teknis",
             "codes": ["Internet tersedia\ntapi fluktuatif", "Perangkat tersedia",
                       "Literasi teknologi\nguru bervariasi", "Belum pernah pakai\naplikasi khusus"]},
            {"label": "Kekhawatiran & hambatan\nimplementasi",
             "codes": ["Kekhawatiran kesiapan guru", "Kekhawatiran jaringan\ninternet",
                       "Hambatan kebiasaan manual", "Kemampuan teknologi\ntidak merata"]},
            {"label": "Dukungan dan\nkesiapan sekolah",
             "codes": ["Dukungan thd sistem website", "Dukungan sekolah",
                       "Implementasi bertahap", "Dukungan teknis operator",
                       "Sistem diterima jika\nsederhana"]},
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
# LAYOUT HELPERS
# ============================================================

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0,2,4))

def text_width(text, size, bold=False):
    factor = 0.48 if bold else 0.45
    lines = text.split('\n')
    return max(len(l) for l in lines) * size * factor

def text_height(text, size):
    lines = text.split('\n')
    return len(lines) * size * 1.3

def node_size(text, fs, pad_x=12, pad_y=8):
    w = text_width(text, fs, True) + pad_x * 2
    h = text_height(text, fs) + pad_y * 2
    return max(w, 80), max(h, 24)

def edge_point(cx, cy, w, h, tx, ty, shape="rect"):
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    if shape == "ellipse":
        a = math.atan2(dy, dx)
        return cx + (w/2)*math.cos(a), cy + (h/2)*math.sin(a)
    hw, hh = w/2, h/2
    if dx == 0:
        return cx, cy + (hh if dy > 0 else -hh)
    if dy == 0:
        return cx + (hw if dx > 0 else -hw), cy
    sx = hw / abs(dx)
    sy = hh / abs(dy)
    s = min(sx, sy)
    return cx + dx*s, cy + dy*s

# ============================================================
# GENERATE PDF - A3 Landscape (compact layout)
# ============================================================

# A3 landscape in points: 1190.55 x 841.89
PAGE_W = 1190.55
PAGE_H = 841.89

pdf = PDFWriter(PAGE_W, PAGE_H)

# Background
pdf.set_color(0.98, 0.98, 0.98)
pdf.draw_rect(0, 0, PAGE_W, PAGE_H, fill=True, stroke=False)

# Title
pdf.set_color(0.17, 0.24, 0.31)
pdf.draw_text_centered(PAGE_W/2, 28, "NETWORK VIEW DIAGRAM", size=14, bold=True)
pdf.set_color(0.33, 0.33, 0.33)
pdf.draw_text_centered(PAGE_W/2, 44, "Koding Wawancara Kualitatif: Pengembangan Sistem Informasi Pemantauan Perilaku Siswa", size=8)
pdf.draw_text_centered(PAGE_W/2, 54, "Berbasis Website dalam Mendukung Manajemen Pembinaan Karakter di Sekolah Dasar", size=8)

# Legend (top-left)
lx, ly = 15, 22
pdf.set_color(1, 1, 1)
pdf.set_stroke_color(0.8, 0.8, 0.8)
pdf.set_line_width(0.5)
pdf.draw_rounded_rect(lx, ly, 180, 50, 4, fill=True, stroke=True)
pdf.set_color(0.17, 0.24, 0.31)
pdf.draw_text(lx+5, ly+12, "LEGENDA", size=7, bold=True)
# Theme ellipse
pdf.set_color(1.0, 0.95, 0.7)
pdf.set_stroke_color(0.4, 0.4, 0.4)
pdf.set_line_width(0.8)
pdf.draw_ellipse(lx+15, ly+28, 10, 6, fill=True, stroke=True)
pdf.set_color(0.17, 0.24, 0.31)
pdf.draw_text(lx+30, ly+30, "= Tema", size=6)
# Axial box
pdf.set_color(0.91, 0.96, 0.99)
pdf.set_stroke_color(0.16, 0.50, 0.73)
pdf.draw_rounded_rect(lx+70, ly+23, 18, 10, 2, fill=True, stroke=True)
pdf.set_color(0.17, 0.24, 0.31)
pdf.draw_text(lx+92, ly+30, "= Axial Code", size=6)
# Open code pill
pdf.set_color(1, 1, 1)
pdf.set_stroke_color(0.53, 0.53, 0.53)
pdf.draw_rounded_rect(lx+5, ly+38, 18, 8, 4, fill=True, stroke=True)
pdf.set_color(0.17, 0.24, 0.31)
pdf.draw_text(lx+30, ly+44, "= Open Code", size=6)
# Dashed line
pdf.set_stroke_color(0.75, 0.22, 0.17)
pdf.set_line_width(0.8)
pdf.set_dash(3, 2)
pdf.draw_line(lx+70, ly+42, lx+88, ly+42)
pdf.clear_dash()
pdf.set_color(0.17, 0.24, 0.31)
pdf.draw_text(lx+92, ly+44, "= Hubungan antar Tema", size=6)

# ============================================================
# THEME POSITIONS - Compact layout, 5 themes
# ============================================================

# Usable area: x=30..1160, y=70..820
# Layout: T1 top-left, T2 top-right, T3 bottom-left, T4 center, T5 bottom-right

theme_pos = {
    "T1": (230, 230),
    "T2": (960, 230),
    "T3": (230, 640),
    "T4": (595, 470),
    "T5": (960, 640),
}

# Axial positions relative to theme (angle, distance)
axial_layout = {
    "T1": [(160, 140), (200, 140), (240, 140), (290, 140)],
    "T2": [(340, 140), (20, 140)],
    "T3": [(160, 140), (220, 140)],
    "T4": [(270, 160)],
    "T5": [(310, 140), (0, 140), (50, 140)],
}

theme_nodes = {}
all_positions = []  # for overlap checking

# ============================================================
# DRAW
# ============================================================

for theme in themes_data:
    tid = theme["id"]
    tcx, tcy = theme_pos[tid]
    tc = theme["color"]
    tb = theme["border"]
    tlabel = theme["label"]
    
    # Theme ellipse
    tw, th = node_size(tlabel, 8, 18, 10)
    tw = max(tw, 140)
    th = max(th, 40)
    
    pdf.save_state()
    pdf.set_color(*tc)
    pdf.set_stroke_color(*tb)
    pdf.set_line_width(1.5)
    pdf.draw_ellipse(tcx, tcy, tw/2, th/2, fill=True, stroke=True)
    pdf.set_color(0.1, 0.1, 0.1)
    pdf.draw_text_centered(tcx, tcy, tlabel, size=7, bold=True)
    pdf.restore_state()
    
    theme_nodes[tid] = (tcx, tcy, tw, th)
    
    # Axial codes
    layouts = axial_layout[tid]
    for ai, axial in enumerate(theme["axial"]):
        if ai >= len(layouts):
            break
        angle_deg, dist = layouts[ai]
        rad = math.radians(angle_deg)
        acx = tcx + dist * math.cos(rad)
        acy = tcy + dist * math.sin(rad)
        
        alabel = axial["label"]
        aw, ah = node_size(alabel, 6.5, 10, 6)
        aw = max(aw, 100)
        ah = max(ah, 22)
        
        # Draw axial box
        pdf.save_state()
        pdf.set_color(0.91, 0.96, 0.99)
        pdf.set_stroke_color(0.16, 0.50, 0.73)
        pdf.set_line_width(0.8)
        pdf.draw_rounded_rect(acx - aw/2, acy - ah/2, aw, ah, 3, fill=True, stroke=True)
        pdf.set_color(0.12, 0.18, 0.27)
        pdf.draw_text_centered(acx, acy, alabel, size=6, bold=True)
        pdf.restore_state()
        
        # Connection theme -> axial
        p1 = edge_point(tcx, tcy, tw, th, acx, acy, "ellipse")
        p2 = edge_point(acx, acy, aw, ah, tcx, tcy, "rect")
        pdf.save_state()
        pdf.set_stroke_color(0.16, 0.50, 0.73)
        pdf.set_line_width(0.7)
        pdf.draw_line(p1[0], p1[1], p2[0], p2[1])
        pdf.set_color(0.16, 0.50, 0.73)
        pdf.draw_arrow(p1[0], p1[1], p2[0], p2[1], size=3)
        pdf.restore_state()
        # "is part of" label
        mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        pdf.save_state()
        pdf.set_color(1, 1, 1)
        pdf.draw_rect(mx-18, my-5, 36, 9, fill=True, stroke=False)
        pdf.set_color(0.16, 0.50, 0.73)
        pdf.draw_text_centered(mx, my, "is part of", size=4.5)
        pdf.restore_state()
        
        # Open codes around axial
        codes = axial["codes"]
        num_codes = len(codes)
        base_dir = math.atan2(acy - tcy, acx - tcx)
        
        if num_codes <= 3:
            spread = math.pi * 0.55
        elif num_codes <= 5:
            spread = math.pi * 0.7
        else:
            spread = math.pi * 0.85
        
        oc_radius = 75 + (num_codes > 5) * 15
        
        for ci, code_text in enumerate(codes):
            if num_codes == 1:
                c_angle = base_dir
            else:
                c_angle = base_dir - spread/2 + spread * ci / (num_codes - 1)
            
            r = oc_radius + (ci % 2) * 12
            ocx = acx + r * math.cos(c_angle)
            ocy = acy + r * math.sin(c_angle)
            
            ow, oh = node_size(code_text, 5.5, 8, 4)
            ow = max(ow, 65)
            oh = max(oh, 15)
            
            # Draw pill
            pdf.save_state()
            pdf.set_color(1, 1, 1)
            pdf.set_stroke_color(0.6, 0.6, 0.6)
            pdf.set_line_width(0.4)
            pdf.draw_rounded_rect(ocx - ow/2, ocy - oh/2, ow, oh, oh/2, fill=True, stroke=True)
            pdf.set_color(0.2, 0.2, 0.2)
            pdf.draw_text_centered(ocx, ocy, code_text, size=5)
            pdf.restore_state()
            
            # Connection axial -> open
            p1 = edge_point(acx, acy, aw, ah, ocx, ocy, "rect")
            p2 = edge_point(ocx, ocy, ow, oh, acx, acy, "rect")
            pdf.save_state()
            pdf.set_stroke_color(0.7, 0.7, 0.7)
            pdf.set_line_width(0.4)
            pdf.draw_line(p1[0], p1[1], p2[0], p2[1])
            pdf.restore_state()

# ============================================================
# INTER-THEME CONNECTIONS
# ============================================================

for t1_id, t2_id, label in inter_theme_links:
    n1 = theme_nodes[t1_id]
    n2 = theme_nodes[t2_id]
    p1 = edge_point(n1[0], n1[1], n1[2], n1[3], n2[0], n2[1], "ellipse")
    p2 = edge_point(n2[0], n2[1], n2[2], n2[3], n1[0], n1[1], "ellipse")
    
    pdf.save_state()
    pdf.set_stroke_color(0.75, 0.22, 0.17)
    pdf.set_line_width(0.9)
    pdf.set_dash(4, 2)
    pdf.draw_line(p1[0], p1[1], p2[0], p2[1])
    pdf.clear_dash()
    pdf.set_color(0.75, 0.22, 0.17)
    pdf.draw_arrow(p1[0], p1[1], p2[0], p2[1], size=4)
    pdf.restore_state()
    
    # Label
    mx = (p1[0] + p2[0]) / 2
    my = (p1[1] + p2[1]) / 2
    lw = len(label) * 3.5 + 8
    pdf.save_state()
    pdf.set_color(1.0, 0.96, 0.96)
    pdf.set_stroke_color(0.75, 0.22, 0.17)
    pdf.set_line_width(0.3)
    pdf.draw_rounded_rect(mx - lw/2, my - 5, lw, 9, 2, fill=True, stroke=True)
    pdf.set_color(0.75, 0.14, 0.11)
    pdf.draw_text_centered(mx, my, label, size=4.5)
    pdf.restore_state()

# Footer
pdf.set_color(0.5, 0.5, 0.5)
pdf.draw_text_centered(PAGE_W/2, PAGE_H - 18, 
    "Network View Diagram | Open Coding - Axial Coding - Thematic Coding", size=6)
pdf.draw_text_centered(PAGE_W/2, PAGE_H - 9,
    "Sumber: Wawancara KS, WK6, WK2, OS | SD Negeri 04 Jatigunung | Peneliti: Ridwan Alif Adi Nugraha", size=5.5)

# ============================================================
# SAVE
# ============================================================

pdf_bytes = pdf.build()
with open("Network_View_Diagram_ATLASti.pdf", "wb") as f:
    f.write(pdf_bytes)

print("PDF Network View Diagram created!")
print(f"  File: Network_View_Diagram_ATLASti.pdf")
print(f"  Size: A3 Landscape ({PAGE_W:.0f} x {PAGE_H:.0f} pt)")
print(f"  Themes: {len(themes_data)}")
total_axial = sum(len(t['axial']) for t in themes_data)
total_open = sum(len(a['codes']) for t in themes_data for a in t['axial'])
print(f"  Axial Codes: {total_axial}")
print(f"  Open Codes: {total_open}")
