#!/usr/bin/env python3
"""
Create an ATLAS.ti-style Network View Diagram from qualitative coding data.
Uses pure Python (no external libraries) to generate SVG output.
Professional layout with no overlapping nodes.
"""
import math

# ============================================================
# DATA STRUCTURE: Themes -> Axial Codes -> Open Codes
# ============================================================

themes_data = [
    {
        "id": "T1",
        "label": "Keterbatasan Sistem\nPencatatan Perilaku Siswa\nyang Berjalan",
        "color": "#FFF3B0",
        "border": "#D4A017",
        "axial": [
            {
                "label": "Pencatatan perilaku\nberbasis manual",
                "codes": [
                    "Pencatatan manual",
                    "Buku absensi/jurnal",
                    "Buku anekdot",
                    "Guru kelas penanggung\njawab utama",
                    "Data perilaku\nbelum digital",
                ]
            },
            {
                "label": "Format pencatatan\ntidak terstandar",
                "codes": [
                    "Format tidak seragam",
                    "Bergantung\nkebiasaan guru",
                    "Format tidak baku",
                    "Pencatatan keterlambatan\nbelum detail",
                ]
            },
            {
                "label": "Keterbatasan dokumentasi\nperilaku positif & prestasi",
                "codes": [
                    "Perilaku positif belum\nterdokumentasi",
                    "Belum ada tempat khusus\nperilaku positif",
                    "Fokus pelanggaran",
                ]
            },
            {
                "label": "Kesulitan pengelolaan\ndan pencarian data",
                "codes": [
                    "Data tersebar",
                    "Data sulit dicari\nkembali",
                    "Data rawan\nhilang/rusak",
                    "Rekapitulasi\nmemakan waktu",
                ]
            },
        ]
    },
    {
        "id": "T2",
        "label": "Ketidakefisienan Alur\nPelaporan dan\nKomunikasi",
        "color": "#D4EDFC",
        "border": "#2471A3",
        "axial": [
            {
                "label": "Alur pelaporan\ntidak efisien",
                "codes": [
                    "Alur pelaporan\nkonvensional",
                    "Pengawasan manajerial\nkurang praktis",
                    "Data tidak terpusat",
                    "Pelaporan situasional",
                ]
            },
            {
                "label": "Komunikasi dengan\norang tua bersifat\ninsidental",
                "codes": [
                    "Komunikasi orang\ntua manual",
                    "Informasi terlambat\nke orang tua",
                    "Notifikasi orang tua\nperlu diatur",
                    "Kendala komunikasi\ndengan orang tua",
                ]
            },
        ]
    },
    {
        "id": "T3",
        "label": "Penghargaan dan Pembinaan\nKarakter Belum\nTerdokumentasi Sistematis",
        "color": "#D5F5E3",
        "border": "#1E8449",
        "axial": [
            {
                "label": "Penghargaan belum\nterstruktur &\nterdokumentasi",
                "codes": [
                    "Penghargaan sederhana",
                    "Penghargaan belum\nterdokumentasi",
                    "Reward spontan",
                    "Penghargaan terstruktur\nbelum berjalan",
                ]
            },
            {
                "label": "Proses pembinaan\nkarakter melalui\npembiasaan harian",
                "codes": [
                    "Pembinaan karakter\nharian",
                    "Teguran bertahap",
                    "Tindak lanjut belum\nterdokumentasi",
                    "Rekam jejak\npembinaan penting",
                    "Pembinaan melalui\npembiasaan",
                ]
            },
        ]
    },
    {
        "id": "T4",
        "label": "Kebutuhan Fitur dan\nFungsi Sistem Informasi\nBerbasis Website",
        "color": "#FDEDEC",
        "border": "#C0392B",
        "axial": [
            {
                "label": "Kebutuhan fitur\ndan fungsi sistem\ninformasi",
                "codes": [
                    "Kebutuhan fitur lengkap",
                    "Kebutuhan rekap otomatis",
                    "Kebutuhan\npencatatan cepat",
                    "Sistem poin perilaku\notomatis",
                    "Kebutuhan\nfitur pencarian",
                    "Kebutuhan\nlaporan otomatis",
                    "Kebutuhan pembagian\nakses pengguna",
                    "Kebutuhan\nkeamanan data",
                    "Tampilan sederhana\ndan input ringkas",
                ]
            },
        ]
    },
    {
        "id": "T5",
        "label": "Kesiapan, Tantangan,\ndan Dukungan\nImplementasi Sistem",
        "color": "#E8DAEF",
        "border": "#6C3483",
        "axial": [
            {
                "label": "Ketersediaan infrastruktur\ndan kesiapan teknis",
                "codes": [
                    "Internet tersedia\ntapi fluktuatif",
                    "Perangkat tersedia",
                    "Literasi teknologi\nguru bervariasi",
                    "Belum pernah pakai\naplikasi khusus",
                ]
            },
            {
                "label": "Kekhawatiran dan\npotensi hambatan\nimplementasi",
                "codes": [
                    "Kekhawatiran\nkesiapan guru",
                    "Kekhawatiran\njaringan internet",
                    "Hambatan\nkebiasaan manual",
                    "Kemampuan teknologi\ntidak merata",
                ]
            },
            {
                "label": "Dukungan dan\nkesiapan sekolah",
                "codes": [
                    "Dukungan terhadap\nsistem website",
                    "Dukungan sekolah",
                    "Implementasi bertahap",
                    "Dukungan teknis\noperator",
                    "Sistem diterima\njika sederhana",
                ]
            },
        ]
    },
]

# Inter-theme relationships
inter_theme_links = [
    ("T1", "T2", "is cause of"),
    ("T1", "T4", "is cause of"),
    ("T2", "T4", "is cause of"),
    ("T3", "T4", "is associated with"),
    ("T4", "T5", "is associated with"),
]

# ============================================================
# SVG BUILDER
# ============================================================

class SVG:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.parts = []
    
    def add(self, s):
        self.parts.append(s)
    
    def esc(self, t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    def multiline_text(self, x, y, text, fs=11, fw="normal", fill="#000", anchor="middle", ff="Segoe UI, Arial, sans-serif"):
        lines = text.split('\n')
        lh = fs * 1.35
        sy = y - (len(lines) - 1) * lh / 2
        s = f'<text text-anchor="{anchor}" font-family="{ff}" font-size="{fs}" font-weight="{fw}" fill="{fill}">'
        for i, line in enumerate(lines):
            s += f'<tspan x="{x}" y="{sy + i * lh:.1f}">{self.esc(line)}</tspan>'
        s += '</text>'
        self.add(s)
    
    def render(self):
        header = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}">
<defs>
  <filter id="ds" x="-3%" y="-3%" width="106%" height="106%">
    <feDropShadow dx="1.5" dy="1.5" stdDeviation="2.5" flood-opacity="0.12"/>
  </filter>
  <marker id="arrowRed" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#C0392B"/>
  </marker>
  <marker id="arrowBlue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#2980B9"/>
  </marker>
</defs>
<rect width="{self.w}" height="{self.h}" fill="#FCFCFC"/>
'''
        footer = '\n</svg>'
        return header + '\n'.join(self.parts) + footer


def text_size(text, fs, pad_x=24, pad_y=16):
    lines = text.split('\n')
    max_chars = max(len(l) for l in lines)
    w = max(max_chars * fs * 0.56 + pad_x * 2, 140)
    h = len(lines) * fs * 1.35 + pad_y * 2
    return w, h


def edge_point(cx, cy, w, h, tx, ty, shape="rect"):
    """Get point on edge of shape toward target (tx, ty)"""
    dx = tx - cx
    dy = ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    if shape == "ellipse":
        rx, ry = w/2, h/2
        a = math.atan2(dy, dx)
        return cx + rx * math.cos(a), cy + ry * math.sin(a)
    else:
        hw, hh = w/2, h/2
        if dx == 0:
            return cx, cy + (hh if dy > 0 else -hh)
        if dy == 0:
            return cx + (hw if dx > 0 else -hw), cy
        sx = hw / abs(dx)
        sy = hh / abs(dy)
        s = min(sx, sy)
        return cx + dx * s, cy + dy * s


# ============================================================
# MAIN LAYOUT - Manually positioned for clean appearance
# ============================================================

WIDTH = 5000
HEIGHT = 3800

svg = SVG(WIDTH, HEIGHT)

# Title area
svg.multiline_text(WIDTH/2, 40, "NETWORK VIEW DIAGRAM", fs=26, fw="bold", fill="#2C3E50")
svg.multiline_text(WIDTH/2, 72, "Koding Wawancara Kualitatif: Pengembangan Sistem Informasi Pemantauan Perilaku Siswa Berbasis Website", fs=13, fill="#555")
svg.multiline_text(WIDTH/2, 92, "dalam Mendukung Manajemen Pembinaan Karakter di Sekolah Dasar", fs=13, fill="#555")

# Legend
lx, ly = WIDTH - 380, 25
svg.add(f'<rect x="{lx}" y="{ly}" width="350" height="90" fill="#fff" stroke="#ddd" stroke-width="1" rx="8" ry="8"/>')
svg.multiline_text(lx + 175, ly + 18, "LEGENDA", fs=11, fw="bold", fill="#333")
svg.add(f'<ellipse cx="{lx+25}" cy="{ly+40}" rx="18" ry="11" fill="#FFF3B0" stroke="#333" stroke-width="1.5"/>')
svg.multiline_text(lx + 75, ly + 44, "= Tema (Theme)", fs=9, anchor="start", fill="#333")
svg.add(f'<rect x="{lx+155}" y="{ly+32}" width="36" height="18" fill="#E8F4FD" stroke="#2980B9" stroke-width="1.2" rx="4" ry="4"/>')
svg.multiline_text(lx + 225, ly + 44, "= Axial Code", fs=9, anchor="start", fill="#333")
svg.add(f'<rect x="{lx+7}" y="{ly+60}" width="36" height="18" fill="#fff" stroke="#888" stroke-width="1" rx="9" ry="9"/>')
svg.multiline_text(lx + 75, ly + 72, "= Open Code", fs=9, anchor="start", fill="#333")
svg.add(f'<line x1="{lx+155}" y1="{ly+70}" x2="{lx+192}" y2="{ly+70}" stroke="#C0392B" stroke-width="1.5" stroke-dasharray="6,3"/>')
svg.multiline_text(lx + 225, ly + 72, "= Hubungan antar Tema", fs=9, anchor="start", fill="#333")

# ============================================================
# PRECISE MANUAL LAYOUT for each theme cluster
# Theme centers are positioned to avoid any overlap
# ============================================================

# Theme 1: Top-left area
T1_cx, T1_cy = 1000, 600
# Theme 2: Top-right area
T2_cx, T2_cy = 4000, 600
# Theme 3: Bottom-left area
T3_cx, T3_cy = 1000, 2800
# Theme 4: Center
T4_cx, T4_cy = 2500, 1800
# Theme 5: Bottom-right area
T5_cx, T5_cy = 4000, 2800

theme_centers = {
    "T1": (T1_cx, T1_cy),
    "T2": (T2_cx, T2_cy),
    "T3": (T3_cx, T3_cy),
    "T4": (T4_cx, T4_cy),
    "T5": (T5_cx, T5_cy),
}

# We'll manually set axial code positions relative to theme center
# and open code positions relative to axial codes

# Layout config per theme: list of (angle_deg, distance) for each axial code
axial_layout = {
    "T1": [
        (150, 380),   # Pencatatan manual - left-down
        (200, 380),   # Format tidak terstandar - down-left
        (250, 380),   # Keterbatasan dokumentasi - down
        (300, 380),   # Kesulitan pengelolaan - down-right
    ],
    "T2": [
        (330, 380),   # Alur pelaporan - right-up
        (30, 380),    # Komunikasi orang tua - right-down
    ],
    "T3": [
        (150, 380),   # Penghargaan belum terstruktur - left-down
        (210, 380),   # Proses pembinaan karakter - down
    ],
    "T4": [
        (270, 420),   # Kebutuhan fitur (single, below)
    ],
    "T5": [
        (310, 380),   # Ketersediaan infrastruktur - right-up
        (0, 380),     # Kekhawatiran - right
        (50, 380),    # Dukungan - right-down
    ],
}

# Store positions for connections
theme_nodes = {}
axial_nodes = {}

# ============================================================
# DRAW ALL THEMES AND THEIR CLUSTERS
# ============================================================

for theme in themes_data:
    tid = theme["id"]
    tcx, tcy = theme_centers[tid]
    tcolor = theme["color"]
    tborder = theme["border"]
    tlabel = theme["label"]
    
    # Theme ellipse size
    tw, th = text_size(tlabel, 13, 40, 24)
    tw = max(tw, 280)
    th = max(th, 80)
    
    # Draw theme ellipse
    svg.add(f'<ellipse cx="{tcx}" cy="{tcy}" rx="{tw/2:.0f}" ry="{th/2:.0f}" fill="{tcolor}" stroke="{tborder}" stroke-width="2.8" filter="url(#ds)"/>')
    svg.multiline_text(tcx, tcy, tlabel, fs=12, fw="bold", fill="#1a1a1a")
    
    theme_nodes[tid] = (tcx, tcy, tw, th)
    
    # Draw axial codes
    layouts = axial_layout[tid]
    for ai, axial in enumerate(theme["axial"]):
        if ai >= len(layouts):
            break
        
        angle_deg, dist = layouts[ai]
        rad = math.radians(angle_deg)
        acx = tcx + dist * math.cos(rad)
        acy = tcy + dist * math.sin(rad)
        
        alabel = axial["label"]
        aw, ah = text_size(alabel, 10, 20, 14)
        aw = max(aw, 180)
        ah = max(ah, 50)
        
        # Draw axial code rectangle
        svg.add(f'<rect x="{acx - aw/2:.0f}" y="{acy - ah/2:.0f}" width="{aw:.0f}" height="{ah:.0f}" fill="#E8F4FD" stroke="#2980B9" stroke-width="1.8" rx="6" ry="6" filter="url(#ds)"/>')
        svg.multiline_text(acx, acy, alabel, fs=10, fw="bold", fill="#2C3E50")
        
        axial_key = f"{tid}_A{ai}"
        axial_nodes[axial_key] = (acx, acy, aw, ah)
        
        # Connection: Theme -> Axial
        p1 = edge_point(tcx, tcy, tw, th, acx, acy, "ellipse")
        p2 = edge_point(acx, acy, aw, ah, tcx, tcy, "rect")
        svg.add(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#2980B9" stroke-width="1.5" marker-end="url(#arrowBlue)"/>')
        # Label on connection
        mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        svg.add(f'<rect x="{mx-30}" y="{my-8}" width="60" height="14" fill="#fff" stroke="none" rx="3" ry="3" opacity="0.9"/>')
        svg.multiline_text(mx, my+3, "is part of", fs=8, fill="#2980B9", fw="normal")
        
        # Draw open codes around axial code
        codes = axial["codes"]
        num_codes = len(codes)
        
        # Direction from theme to axial (open codes fan out further in same direction)
        base_dir = math.atan2(acy - tcy, acx - tcx)
        
        # Fan spread
        if num_codes <= 3:
            spread = math.pi * 0.5
        elif num_codes <= 5:
            spread = math.pi * 0.65
        else:
            spread = math.pi * 0.85
        
        oc_radius = 190
        
        for ci, code_text in enumerate(codes):
            if num_codes == 1:
                c_angle = base_dir
            else:
                c_angle = base_dir - spread/2 + spread * ci / (num_codes - 1)
            
            # Slight radius variation to avoid overlap
            r = oc_radius + (ci % 3) * 20
            
            ocx = acx + r * math.cos(c_angle)
            ocy = acy + r * math.sin(c_angle)
            
            # Open code size
            ow, oh = text_size(code_text, 9, 16, 10)
            ow = max(ow, 120)
            oh = max(oh, 32)
            
            # Draw pill-shaped open code
            svg.add(f'<rect x="{ocx - ow/2:.0f}" y="{ocy - oh/2:.0f}" width="{ow:.0f}" height="{oh:.0f}" fill="#FFFFFF" stroke="#888" stroke-width="1" rx="{oh/2:.0f}" ry="{oh/2:.0f}"/>')
            svg.multiline_text(ocx, ocy, code_text, fs=9, fill="#333")
            
            # Connection: Axial -> Open Code
            p1 = edge_point(acx, acy, aw, ah, ocx, ocy, "rect")
            p2 = edge_point(ocx, ocy, ow, oh, acx, acy, "rect")
            svg.add(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#AAA" stroke-width="0.9"/>')

# ============================================================
# DRAW INTER-THEME CONNECTIONS (dashed red arrows)
# ============================================================

for t1_id, t2_id, label in inter_theme_links:
    n1 = theme_nodes[t1_id]
    n2 = theme_nodes[t2_id]
    p1 = edge_point(n1[0], n1[1], n1[2], n1[3], n2[0], n2[1], "ellipse")
    p2 = edge_point(n2[0], n2[1], n2[2], n2[3], n1[0], n1[1], "ellipse")
    
    svg.add(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#C0392B" stroke-width="1.8" stroke-dasharray="8,4" marker-end="url(#arrowRed)"/>')
    
    # Label at midpoint
    mx = (p1[0] + p2[0]) / 2
    my = (p1[1] + p2[1]) / 2
    lw = len(label) * 6 + 16
    svg.add(f'<rect x="{mx - lw/2:.0f}" y="{my - 10}" width="{lw}" height="18" fill="#FFF5F5" stroke="#E74C3C" stroke-width="0.7" rx="4" ry="4"/>')
    svg.multiline_text(mx, my + 3, label, fs=8, fill="#C0392B")

# ============================================================
# FOOTER
# ============================================================
svg.multiline_text(WIDTH/2, HEIGHT - 35, "Network View Diagram | Analisis Koding Kualitatif (Open Coding → Axial Coding → Thematic Coding)", fs=11, fill="#888")
svg.multiline_text(WIDTH/2, HEIGHT - 15, "Sumber: Wawancara KS, WK6, WK2, OS | SD Negeri 04 Jatigunung | Peneliti: Ridwan Alif Adi Nugraha", fs=10, fill="#aaa")

# ============================================================
# OUTPUT
# ============================================================
output = svg.render()
with open("Network_View_Diagram_ATLASti.svg", "w", encoding="utf-8") as f:
    f.write(output)

print("✓ Network View Diagram created successfully!")
print(f"  File: Network_View_Diagram_ATLASti.svg")
print(f"  Size: {WIDTH}x{HEIGHT} px")
print(f"  Themes: {len(themes_data)}")
total_axial = sum(len(t['axial']) for t in themes_data)
total_open = sum(len(a['codes']) for t in themes_data for a in t['axial'])
print(f"  Axial Codes: {total_axial}")
print(f"  Open Codes: {total_open}")
