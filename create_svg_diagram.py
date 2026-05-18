#!/usr/bin/env python3
"""
Network View Diagram - ATLAS.ti authentic style (SVG version)
Same layout as PDF version but in SVG format for browser preview.
"""
import math

# ============================================================
# DATA (same as PDF version)
# ============================================================

themes_data = [
    {
        "id": "T1",
        "label": "Keterbatasan Sistem Pencatatan\nPerilaku Siswa yang Berjalan",
        "color": "#FFE84D", "border": "#C7A600",
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
        "color": "#B9E0FF", "border": "#2471A3",
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
        "color": "#B8F0C8", "border": "#1E8449",
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
        "color": "#FFD4C4", "border": "#C0392B",
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
        "color": "#DECCEE", "border": "#6C3483",
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
# SVG HELPERS
# ============================================================

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def node_size(text, fs, px=10, py=6):
    lines = text.split('\n')
    cw = fs * 0.52
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

# Scale: SVG is 2x the PDF for clarity
S = 2.5
W = int(1191 * S)
H = int(842 * S)

theme_pos = {
    "T1": (250*S, 210*S),
    "T2": (940*S, 210*S),
    "T3": (250*S, 650*S),
    "T4": (595*S, 430*S),
    "T5": (940*S, 650*S),
}

axial_config = {
    "T1": [(135, 130*S), (180, 130*S), (225, 130*S), (270, 130*S)],
    "T2": [(0, 130*S), (315, 130*S)],
    "T3": [(180, 130*S), (225, 130*S)],
    "T4": [(270, 145*S)],
    "T5": [(0, 130*S), (315, 130*S), (45, 130*S)],
}

OC_DIST = 68 * S

parts = []
parts.append(f'<?xml version="1.0" encoding="UTF-8"?>')
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
parts.append(f'<defs>')
parts.append(f'<marker id="ar" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#B33326"/></marker>')
parts.append(f'<marker id="ab" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#555"/></marker>')
parts.append(f'</defs>')
parts.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')

# Title
parts.append(f'<text x="{W/2}" y="{28*S}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{16*S}" font-weight="bold" fill="#222">NETWORK VIEW</text>')
parts.append(f'<text x="{W/2}" y="{42*S}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{7*S}" fill="#555">Pengembangan Sistem Informasi Pemantauan Perilaku Siswa Berbasis Website dalam Mendukung Manajemen Pembinaan Karakter di Sekolah Dasar</text>')

theme_nodes = {}

def svg_multitext(x, y, text, fs, fw="normal", fill="#222"):
    lines = text.split('\n')
    lh = fs * 1.25
    sy = y - (len(lines)-1)*lh/2
    s = f'<text text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{fs}" font-weight="{fw}" fill="{fill}">'
    for i, l in enumerate(lines):
        s += f'<tspan x="{x}" y="{sy+i*lh:.1f}">{esc(l)}</tspan>'
    s += '</text>'
    return s

def svg_node(cx, cy, text, fs, px, py, fill, stroke, sw=1, bold=False):
    w, h = node_size(text, fs, px, py)
    r = min(6, h/4)
    s = f'<rect x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" ry="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    s += svg_multitext(cx, cy, text, fs, "bold" if bold else "normal", "#222")
    parts.append(s)
    return w, h

def svg_link(x1, y1, x2, y2, label, color="#555", sw=1, dashed=False):
    d = f' stroke-dasharray="{4*S},{2*S}"' if dashed else ""
    me = ' marker-end="url(#ar)"' if dashed else ' marker-end="url(#ab)"'
    parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}"{d}{me}/>')
    mx, my = (x1+x2)/2, (y1+y2)/2
    lw = len(label)*3.5*S + 6*S
    parts.append(f'<rect x="{mx-lw/2:.1f}" y="{my-4.5*S:.1f}" width="{lw:.1f}" height="{8*S:.1f}" fill="#fff" stroke="none"/>')
    parts.append(f'<text x="{mx:.1f}" y="{my+1.5*S:.1f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{5*S}" fill="{color}">{esc(label)}</text>')

# ============================================================
# RENDER
# ============================================================

for theme in themes_data:
    tid = theme["id"]
    tcx, tcy = theme_pos[tid]

    # Theme node
    tw, th = svg_node(tcx, tcy, theme["label"], 7.5*S, 14*S, 8*S,
                      theme["color"], theme["border"], sw=1.5*S, bold=True)
    theme_nodes[tid] = (tcx, tcy, tw, th)

    configs = axial_config[tid]
    for ai, axial in enumerate(theme["axial"]):
        if ai >= len(configs):
            break
        ang_deg, dist = configs[ai]
        rad = math.radians(ang_deg)
        acx = tcx + dist * math.cos(rad)
        acy = tcy + dist * math.sin(rad)

        # Axial node - lighter version of theme color
        aw, ah = svg_node(acx, acy, axial["label"], 6*S, 8*S, 5*S,
                          "#F5F9FF", theme["border"], sw=0.8*S, bold=True)

        # Link theme -> axial
        p1 = edge_pt(tcx, tcy, tw, th, acx, acy)
        p2 = edge_pt(acx, acy, aw, ah, tcx, tcy)
        svg_link(p1[0], p1[1], p2[0], p2[1], "is part of",
                 color=theme["border"], sw=0.7*S)

        # Open codes
        codes = axial["codes"]
        nc = len(codes)
        base_dir = math.atan2(acy - tcy, acx - tcx)
        spread = math.pi * (0.5 if nc <= 3 else 0.65 if nc <= 5 else 0.8)

        for ci, ct in enumerate(codes):
            ca = base_dir if nc == 1 else base_dir - spread/2 + spread*ci/(nc-1)
            r = OC_DIST + (ci % 2)*10*S
            ocx = acx + r * math.cos(ca)
            ocy = acy + r * math.sin(ca)

            ow, oh = svg_node(ocx, ocy, ct, 5*S, 6*S, 3*S,
                              "#FFFFFF", "#999", sw=0.5*S)

            cp1 = edge_pt(acx, acy, aw, ah, ocx, ocy)
            cp2 = edge_pt(ocx, ocy, ow, oh, acx, acy)
            parts.append(f'<line x1="{cp1[0]:.1f}" y1="{cp1[1]:.1f}" x2="{cp2[0]:.1f}" y2="{cp2[1]:.1f}" stroke="#CCC" stroke-width="{0.4*S}"/>')

# Inter-theme links
for t1, t2, label in inter_theme_links:
    n1, n2 = theme_nodes[t1], theme_nodes[t2]
    p1 = edge_pt(n1[0], n1[1], n1[2], n1[3], n2[0], n2[1])
    p2 = edge_pt(n2[0], n2[1], n2[2], n2[3], n1[0], n1[1])
    svg_link(p1[0], p1[1], p2[0], p2[1], label, color="#B33326", sw=1*S, dashed=True)

# Footer
parts.append(f'<text x="{W/2}" y="{H-12*S}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{5.5*S}" fill="#999">Sumber: Wawancara KS, WK6, WK2, OS | SD Negeri 04 Jatigunung | Peneliti: Ridwan Alif Adi Nugraha</text>')

parts.append('</svg>')

with open("Network_View_Diagram_ATLASti.svg", "w", encoding="utf-8") as f:
    f.write('\n'.join(parts))

print("OK - SVG Network View created: Network_View_Diagram_ATLASti.svg")
