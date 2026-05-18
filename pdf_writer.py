#!/usr/bin/env python3
"""Minimal PDF writer using only Python standard library."""
import struct
import zlib
import math

class PDFWriter:
    """Creates a simple PDF with vector graphics (lines, rects, ellipses, text)."""
    
    def __init__(self, width_pt, height_pt):
        self.w = width_pt
        self.h = height_pt
        self.objects = []
        self.pages = []
        self.fonts = {}
        self.stream_parts = []
        
    def _add_obj(self, content):
        self.objects.append(content)
        return len(self.objects)
    
    def set_color(self, r, g, b):
        self.stream_parts.append(f"{r:.3f} {g:.3f} {b:.3f} rg")
    
    def set_stroke_color(self, r, g, b):
        self.stream_parts.append(f"{r:.3f} {g:.3f} {b:.3f} RG")
    
    def set_line_width(self, w):
        self.stream_parts.append(f"{w:.2f} w")
    
    def set_dash(self, on=4, off=2):
        self.stream_parts.append(f"[{on} {off}] 0 d")
    
    def clear_dash(self):
        self.stream_parts.append("[] 0 d")
    
    def move_to(self, x, y):
        self.stream_parts.append(f"{x:.2f} {self.h - y:.2f} m")
    
    def line_to(self, x, y):
        self.stream_parts.append(f"{x:.2f} {self.h - y:.2f} l")
    
    def draw_line(self, x1, y1, x2, y2):
        self.move_to(x1, y1)
        self.line_to(x2, y2)
        self.stream_parts.append("S")
    
    def draw_rect(self, x, y, w, h, fill=True, stroke=True):
        self.stream_parts.append(f"{x:.2f} {self.h - y - h:.2f} {w:.2f} {h:.2f} re")
        if fill and stroke:
            self.stream_parts.append("B")
        elif fill:
            self.stream_parts.append("f")
        else:
            self.stream_parts.append("S")
    
    def draw_rounded_rect(self, x, y, w, h, r, fill=True, stroke=True):
        """Draw rounded rectangle using bezier curves."""
        r = min(r, w/2, h/2)
        k = 0.5523  # bezier approximation for quarter circle
        # Convert y
        by = self.h - y - h
        
        self.stream_parts.append(f"{x+r:.2f} {by:.2f} m")
        self.stream_parts.append(f"{x+w-r:.2f} {by:.2f} l")
        self.stream_parts.append(f"{x+w-r+r*k:.2f} {by:.2f} {x+w:.2f} {by+r-r*k:.2f} {x+w:.2f} {by+r:.2f} c")
        self.stream_parts.append(f"{x+w:.2f} {by+h-r:.2f} l")
        self.stream_parts.append(f"{x+w:.2f} {by+h-r+r*k:.2f} {x+w-r+r*k:.2f} {by+h:.2f} {x+w-r:.2f} {by+h:.2f} c")
        self.stream_parts.append(f"{x+r:.2f} {by+h:.2f} l")
        self.stream_parts.append(f"{x+r-r*k:.2f} {by+h:.2f} {x:.2f} {by+h-r+r*k:.2f} {x:.2f} {by+h-r:.2f} c")
        self.stream_parts.append(f"{x:.2f} {by+r:.2f} l")
        self.stream_parts.append(f"{x:.2f} {by+r-r*k:.2f} {x+r-r*k:.2f} {by:.2f} {x+r:.2f} {by:.2f} c")
        
        if fill and stroke:
            self.stream_parts.append("B")
        elif fill:
            self.stream_parts.append("f")
        else:
            self.stream_parts.append("S")
    
    def draw_ellipse(self, cx, cy, rx, ry, fill=True, stroke=True):
        """Draw ellipse using bezier curves."""
        k = 0.5523
        ey = self.h - cy
        
        self.stream_parts.append(f"{cx+rx:.2f} {ey:.2f} m")
        self.stream_parts.append(f"{cx+rx:.2f} {ey+ry*k:.2f} {cx+rx*k:.2f} {ey+ry:.2f} {cx:.2f} {ey+ry:.2f} c")
        self.stream_parts.append(f"{cx-rx*k:.2f} {ey+ry:.2f} {cx-rx:.2f} {ey+ry*k:.2f} {cx-rx:.2f} {ey:.2f} c")
        self.stream_parts.append(f"{cx-rx:.2f} {ey-ry*k:.2f} {cx-rx*k:.2f} {ey-ry:.2f} {cx:.2f} {ey-ry:.2f} c")
        self.stream_parts.append(f"{cx+rx*k:.2f} {ey-ry:.2f} {cx+rx:.2f} {ey-ry*k:.2f} {cx+rx:.2f} {ey:.2f} c")
        
        if fill and stroke:
            self.stream_parts.append("B")
        elif fill:
            self.stream_parts.append("f")
        else:
            self.stream_parts.append("S")
    
    def draw_text(self, x, y, text, size=10, bold=False):
        """Draw text at position (centered horizontally)."""
        font = "/F2" if bold else "/F1"
        ey = self.h - y
        # Escape special PDF chars
        text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        self.stream_parts.append("BT")
        self.stream_parts.append(f"{font} {size} Tf")
        self.stream_parts.append(f"{x:.2f} {ey:.2f} Td")
        self.stream_parts.append(f"({text}) Tj")
        self.stream_parts.append("ET")
    
    def draw_text_centered(self, cx, cy, text, size=10, bold=False):
        """Draw text centered at cx, cy. Handles multiline."""
        lines = text.split('\n')
        line_h = size * 1.3
        start_y = cy - (len(lines) - 1) * line_h / 2
        for i, line in enumerate(lines):
            # Approximate width
            char_w = size * 0.45 if not bold else size * 0.48
            tw = len(line) * char_w
            self.draw_text(cx - tw/2, start_y + i * line_h, line, size, bold)
    
    def draw_arrow(self, x1, y1, x2, y2, size=5):
        """Draw arrowhead at (x2,y2) pointing in direction from (x1,y1)."""
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return
        udx, udy = dx/length, dy/length
        # Arrow points
        ax = x2 - udx * size
        ay = y2 - udy * size
        px, py = -udy * size * 0.5, udx * size * 0.5
        
        ey2 = self.h - y2
        eax = ax
        eay = self.h - ay
        
        self.stream_parts.append(f"{x2:.2f} {ey2:.2f} m")
        self.stream_parts.append(f"{eax+px:.2f} {eay+py:.2f} l")  
        self.stream_parts.append(f"{eax-px:.2f} {eay-py:.2f} l")
        self.stream_parts.append("f")
    
    def save_state(self):
        self.stream_parts.append("q")
    
    def restore_state(self):
        self.stream_parts.append("Q")
    
    def build(self):
        """Generate the complete PDF bytes."""
        pdf_objects = []
        
        # Object 1: Catalog
        pdf_objects.append("<< /Type /Catalog /Pages 2 0 R >>")
        
        # Object 2: Pages
        pdf_objects.append(f"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
        
        # Object 3: Page
        pdf_objects.append(
            f"<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 {self.w:.2f} {self.h:.2f}] "
            f"/Contents 4 0 R "
            f"/Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>"
        )
        
        # Object 4: Content stream
        stream_content = "\n".join(self.stream_parts)
        stream_bytes = stream_content.encode('latin-1', errors='replace')
        pdf_objects.append(
            f"<< /Length {len(stream_bytes)} >>\nstream\n" + 
            "STREAM_PLACEHOLDER" +
            "\nendstream"
        )
        
        # Object 5: Font (Helvetica)
        pdf_objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        
        # Object 6: Font Bold
        pdf_objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        
        # Build PDF
        output = b"%PDF-1.4\n"
        offsets = []
        
        for i, obj in enumerate(pdf_objects):
            offsets.append(len(output))
            obj_num = i + 1
            if "STREAM_PLACEHOLDER" in obj:
                header = f"{obj_num} 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n"
                output += header.encode('latin-1')
                output += stream_bytes
                output += b"\nendstream\nendobj\n"
            else:
                output += f"{obj_num} 0 obj\n{obj}\nendobj\n".encode('latin-1')
        
        # Cross-reference table
        xref_offset = len(output)
        output += b"xref\n"
        output += f"0 {len(pdf_objects) + 1}\n".encode()
        output += b"0000000000 65535 f \n"
        for off in offsets:
            output += f"{off:010d} 00000 n \n".encode()
        
        output += b"trailer\n"
        output += f"<< /Size {len(pdf_objects) + 1} /Root 1 0 R >>\n".encode()
        output += b"startxref\n"
        output += f"{xref_offset}\n".encode()
        output += b"%%EOF"
        
        return output
