#!/usr/bin/env python3
"""
Network View Diagram ala ATLAS.ti - SVG version (compact layout matching PDF).
"""
import math

# Same data as PDF version
themes_data = [
    {
        "id": "T1",
        "label": "Keterbatasan Sistem\nPencatatan Perilaku Siswa\nyang Berjalan",
        "color": "#FFF3B0", "border": "#B38D08",
        "axial": [
            {"label": "Pencatatan perilaku\nberbasis manual",
             "codes": ["Pencatatan manual", "Buku absensi/jurnal", "Buku anekdot",
                       "Guru kelas PJ utama", "Data perilaku belum digital"]},
            {"label": "Format pencatatan\ntidak terstandar",
             "codes": ["Format tidak seragam", "Bergantung\nkebiasaan guru",
                       "Format tidak baku", "Keterlambatan\nbelum detail"]},
            {"label": "Keterbatasan dokumentasi\nperilaku positif & prestasi",
             "codes": ["Perilaku positif belum\nterdokumentasi", "Belum ada tempat\nkhusus perilaku positif",
                       "Fokus pelanggaran"]},
            {"label": "Kesulitan pengelolaan\ndan pencarian data",
             "codes": ["Data tersebar", "Data sulit dicari", "Data rawan\nhilang/rusak",
                       "Rekapitulasi lama"]},
        ]
    },
    {
        "id": "T2",
        "label": "Ketidakefisienan Alur\nPelaporan dan Komunikasi",
        "color": "#D4EDFC", "border": "#2471A3",
        "axial": [
            {"label": "Alur pelaporan\ntidak efisien",
             "codes": ["Alur pelaporan\nkonvensional", "Pengawasan manajerial\nkurang praktis",
                       "Data tidak terpusat", "Pelaporan situasional"]},
            {"label": "Komunikasi orang tua\nbersifat insidental",
             "codes": ["Komunikasi orang tua\nmanual", "Informasi terlambat\nke orang tua",
                       "Notifikasi orang tua\nperlu diatur", "Kendala komunikasi\ndengan orang tua"]},
        ]
    },
    {
        "id": "T3",
        "label": "Penghargaan & Pembinaan\nKarakter Belum\nTerdokumentasi Sistematis",
        "color": "#D5F5E3", "border": "#1E8449",
        "axial": [
            {"label": "Penghargaan belum\nterstruktur",
             "codes": ["Penghargaan sederhana", "Penghargaan belum\nterdokumentasi",
                       "Reward spontan", "Penghargaan terstruktur\nbelum berjalan"]},
            {"label": "Pembinaan karakter\nmelalui pembiasaan harian",
             "codes": ["Pembinaan karakter\nharian", "Teguran bertahap",
                       "Tindak lanjut belum\nterdokumentasi", "Rekam jejak\npembinaan penting",
                       "Pembinaan melalui\npembiasaan"]},
        ]
    },
    {
        "id": "T4",
        "label": "Kebutuhan Fitur & Fungsi\nSistem Informasi\nBerbasis Website",
        "color": "#FDEDEC", "border": "#C0392B",
        "axial": [
            {"label": "Kebutuhan fitur dan\nfungsi sistem informasi",
             "codes": ["Kebutuhan fitur lengkap", "Kebutuhan rekap otomatis",
                       "Kebutuhan\npencatatan cepat", "Sistem poin otomatis",
                       "Kebutuhan\nfitur pencarian", "Kebutuhan\nlaporan otomatis",
                       "Pembagian akses\npengguna", "Kebutuhan\nkeamanan data",
                       "Tampilan sederhana"]},
        ]
    },
    {
        "id": "T5",
        "label": "Kesiapan, Tantangan,\ndan Dukungan\nImplementasi Sistem",
        "color": "#E8DAEF", "border": "#6C3483",
        "axial": [
            {"label": "Ketersediaan infrastruktur\ndan kesiapan teknis",
             "codes": ["Internet tersedia\ntapi fluktuatif", "Perangkat tersedia",
                       "Literasi teknologi\nguru bervariasi", "Belum pernah pakai\naplikasi khusus"]},
            {"label": "Kekhawatiran & hambatan\nimplementasi",
             "codes": ["Kekhawatiran\nkesiapan guru", "Kekhawatiran\njaringan internet",
                       "Hambatan\nkebiasaan manual", "Kemampuan teknologi\ntidak merata"]},
            {"label": "Dukungan dan\nkesiapan sekolah",
             "codes": ["Dukungan thd\nsistem website", "Dukungan sekolah",
                       "Implementasi bertahap", "Dukungan teknis\noperator",
                       "Sistem diterima\njika sederhana"]},
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
    return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def multitext(x, y, text, fs=11, fw="normal", fill="#000"):
    lines = text.split('\n')
    lh = fs * 1.3
    sy = y - (len(lines)-1)*lh/2
    s = f'<text text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="{fs}" font-weight="{fw}" fill="{fill}">'
    for i, l in enumerate(lines):
        s += f'<tspan x="{x}" y="{sy+i*lh:.1f}">{esc(l)}</tspan>'
    s += '</text>'
    return s

def node_size(text, fs, px=12, py=8):
    lines = text.split('\n')
    w = max(len(l) for l in lines)*fs*0.52 + px*2
    h = len(lines)*fs*1.3 + py*2
    return max(w, 80), max(h, 24)

def edge_point(cx, cy, w, h, tx, ty, shape="rect"):
    dx, dy = tx-cx, ty-cy
    if dx==0 and dy==0: return cx, cy
    if shape == "ellipse":
        a = math.atan2(dy, dx)
        return cx+(w/2)*math.cos(a), cy+(h/2)*math.sin(a)
    hw, hh = w/2, h/2
    if dx==0: return cx, cy+(hh if dy>0 else -hh)
    if dy==0: return cx+(hw if dx>0 else -hw), cy
    s = min(hw/abs(dx), hh/abs(dy))
    return cx+dx*s, cy+dy*s

# ============================================================
# LAYOUT (same as PDF, scaled 2x for better SVG readability)
# ============================================================

S = 2.0  # scale factor
W = int(1191 * S)
H = int(842 * S)

theme_pos = {
    "T1": (230*S, 230*S),
    "T2": (960*S, 230*S),
    "T3": (230*S, 640*S),
    "T4": (595*S, 470*S),
    "T5": (960*S, 640*S),
}

axial_layout = {
    "T1": [(160, 140*S), (200, 140*S), (240, 140*S), (290, 140*S)],
    "T2": [(340, 140*S), (20, 140*S)],
    "T3": [(160, 140*S), (220, 140*S)],
    "T4": [(270, 160*S)],
    "T5": [(310, 140*S), (0, 140*S), (50, 140*S)],
}

parts = []
parts.append(f'<?xml version="1.0" encoding="UTF-8"?>')
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
parts.append(f'<rect width="{W}" height="{H}" fill="#FCFCFC"/>')

# Title
parts.append(multitext(W/2, 40*S, "NETWORK VIEW DIAGRAM", fs=14*S, fw="bold", fill="#2C3E50"))
parts.append(multitext(W/2, 62*S, "Koding Wawancara Kualitatif: Pengembangan Sistem Informasi Pemantauan Perilaku Siswa Berbasis Website", fs=8*S, fill="#555"))
parts.append(multitext(W/2, 74*S, "dalam Mendukung Manajemen Pembinaan Karakter di Sekolah Dasar", fs=8*S, fill="#555"))

theme_nodes = {}

for theme in themes_data:
    tid = theme["id"]
    tcx, tcy = theme_pos[tid]
    tlabel = theme["label"]
    
    tw, th = node_size(tlabel, 8*S, 18*S, 10*S)
    tw = max(tw, 140*S); th = max(th, 40*S)
    
    parts.append(f'<ellipse cx="{tcx}" cy="{tcy}" rx="{tw/2:.0f}" ry="{th/2:.0f}" fill="{theme["color"]}" stroke="{theme["border"]}" stroke-width="{1.5*S}"/>')
    parts.append(multitext(tcx, tcy, tlabel, fs=7*S, fw="bold", fill="#1a1a1a"))
    
    theme_nodes[tid] = (tcx, tcy, tw, th)
    
    layouts = axial_layout[tid]
    for ai, axial in enumerate(theme["axial"]):
        if ai >= len(layouts): break
        angle_deg, dist = layouts[ai]
        rad = math.radians(angle_deg)
        acx = tcx + dist*math.cos(rad)
        acy = tcy + dist*math.sin(rad)
        
        alabel = axial["label"]
        aw, ah = node_size(alabel, 6.5*S, 10*S, 6*S)
        aw = max(aw, 100*S); ah = max(ah, 22*S)
        
        parts.append(f'<rect x="{acx-aw/2:.0f}" y="{acy-ah/2:.0f}" width="{aw:.0f}" height="{ah:.0f}" fill="#E8F4FD" stroke="#2980B9" stroke-width="{0.8*S}" rx="{3*S}"/>')
        parts.append(multitext(acx, acy, alabel, fs=6.5*S, fw="bold", fill="#2C3E50"))
        
        # Connection theme->axial
        p1 = edge_point(tcx, tcy, tw, th, acx, acy, "ellipse")
        p2 = edge_point(acx, acy, aw, ah, tcx, tcy, "rect")
        parts.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#2980B9" stroke-width="{0.7*S}" marker-end="url(#ab)"/>')
        mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        parts.append(f'<rect x="{mx-20*S}" y="{my-5*S}" width="{40*S}" height="{9*S}" fill="#fff" opacity="0.9" rx="{2*S}"/>')
        parts.append(multitext(mx, my+1*S, "is part of", fs=5*S, fill="#2980B9"))
        
        # Open codes
        codes = axial["codes"]
        nc = len(codes)
        base_dir = math.atan2(acy-tcy, acx-tcx)
        spread = math.pi*(0.55 if nc<=3 else 0.7 if nc<=5 else 0.85)
        oc_r = (75 + (nc>5)*15) * S
        
        for ci, ct in enumerate(codes):
            ca = base_dir if nc==1 else base_dir - spread/2 + spread*ci/(nc-1)
            r = oc_r + (ci%2)*12*S
            ocx = acx + r*math.cos(ca)
            ocy = acy + r*math.sin(ca)
            ow, oh = node_size(ct, 5.5*S, 8*S, 4*S)
            ow = max(ow, 65*S); oh = max(oh, 15*S)
            
            parts.append(f'<rect x="{ocx-ow/2:.0f}" y="{ocy-oh/2:.0f}" width="{ow:.0f}" height="{oh:.0f}" fill="#fff" stroke="#888" stroke-width="{0.4*S}" rx="{oh/2:.0f}"/>')
            parts.append(multitext(ocx, ocy, ct, fs=5.5*S, fill="#333"))
            
            cp1 = edge_point(acx, acy, aw, ah, ocx, ocy, "rect")
            cp2 = edge_point(ocx, ocy, ow, oh, acx, acy, "rect")
            parts.append(f'<line x1="{cp1[0]:.1f}" y1="{cp1[1]:.1f}" x2="{cp2[0]:.1f}" y2="{cp2[1]:.1f}" stroke="#AAA" stroke-width="{0.4*S}"/>')

# Inter-theme links
for t1, t2, label in inter_theme_links:
    n1, n2 = theme_nodes[t1], theme_nodes[t2]
    p1 = edge_point(n1[0],n1[1],n1[2],n1[3],n2[0],n2[1],"ellipse")
    p2 = edge_point(n2[0],n2[1],n2[2],n2[3],n1[0],n1[1],"ellipse")
    parts.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#C0392B" stroke-width="{1*S}" stroke-dasharray="{4*S},{2*S}" marker-end="url(#ar)"/>')
    mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
    lw = len(label)*3.5*S + 8*S
    parts.append(f'<rect x="{mx-lw/2:.0f}" y="{my-5*S:.0f}" width="{lw:.0f}" height="{9*S:.0f}" fill="#FFF5F5" stroke="#E74C3C" stroke-width="{0.3*S}" rx="{2*S}"/>')
    parts.append(multitext(mx, my+1*S, label, fs=5*S, fill="#C0392B"))

# Footer
parts.append(multitext(W/2, H-20*S, "Network View Diagram | Open Coding - Axial Coding - Thematic Coding", fs=6.5*S, fill="#888"))
parts.append(multitext(W/2, H-9*S, "Sumber: Wawancara KS, WK6, WK2, OS | SD Negeri 04 Jatigunung | Peneliti: Ridwan Alif Adi Nugraha", fs=5.5*S, fill="#aaa"))

# Markers (add at top after opening svg)
defs = f'''<defs>
<marker id="ab" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#2980B9"/></marker>
<marker id="ar" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#C0392B"/></marker>
</defs>'''

# Insert defs after first rect
parts.insert(3, defs)

parts.append('</svg>')

with open("Network_View_Diagram_ATLASti.svg", "w", encoding="utf-8") as f:
    f.write('\n'.join(parts))

print("SVG created: Network_View_Diagram_ATLASti.svg")
