#!/usr/bin/env python3
"""The PinkSun mark, generated from the t-shirt proof's geometry.

Read off the proof (see the isolated artwork):
  - 12 rays, alternating pink and yellow, leftmost pink
  - straight, not curved, with flat (butt) ends
  - ray width is roughly equal to the gap between rays as judged mid-fan
  - a solid pink semicircle dome with a flat base and no outline
  - a clear gap between the dome edge and the inner ends of the rays
  - the script sits below the dome and is wider than the sun

The mark is geometry only. Each world roughens it with its own material
filter, which is how the same logo reads as chalk, wax or ballpoint.
"""
import math

CX, CY = 100.0, 104.0   # centre of the dome base
DOME_R = 34.0           # the proof's dome is a true semicircle
RAY_IN = 50.0           # inner end, leaving a gap off the dome (dome edge 34)
RAY_OUT = 96.0          # outer end
RAY_W = 9.0             # ~1:1 against the mid-fan gap
RAYS = 12

VIEWBOX = "0 0 200 112"
SUN_WIDTH = 2 * RAY_OUT          # 192 units wide
SCRIPT_TO_SUN = SUN_WIDTH * 1.45  # the proof's script is wider than the sun


def ray_lines(color_a="#FF5AA7", color_b="#FFE800", width=RAY_W, indent="        "):
    """12 straight butt-ended rays, alternating colour, leftmost = color_a."""
    lines = []
    for i in range(RAYS):
        a = math.radians(180.0 - i * (180.0 / (RAYS - 1)))
        x1, y1 = CX + RAY_IN * math.cos(a), CY - RAY_IN * math.sin(a)
        x2, y2 = CX + RAY_OUT * math.cos(a), CY - RAY_OUT * math.sin(a)
        color = color_a if i % 2 == 0 else color_b
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width:.1f}" stroke-linecap="butt"/>'
        )
    return "\n".join(lines)


def dome(fill="#FF3D9A", stroke=None, width=0, indent="      "):
    d = f"M{CX - DOME_R:.0f},{CY:.0f} A{DOME_R:.0f},{DOME_R:.0f} 0 0 1 {CX + DOME_R:.0f},{CY:.0f} Z"
    extra = f' stroke="{stroke}" stroke-width="{width}"' if stroke else ""
    return f'{indent}<path d="{d}" fill="{fill}"{extra}/>'


def sun_symbol(color_a="#FF5AA7", color_b="#FFE800", dome_fill="#FF3D9A",
               dome_stroke=None, dome_width=0, ink_outline=None, ink_width=None,
               ray_scale=1.0, hatch_fill=None):
    """The full symbol body. ink_outline draws a pen line under each ray first."""
    parts = []
    if ink_outline:
        parts.append(ray_lines(ink_outline, ink_outline, ink_width or (RAY_W + 3), "        "))
        parts.append(ray_lines(color_a, color_b, RAY_W * ray_scale, "        "))
    else:
        parts.append(ray_lines(color_a, color_b, RAY_W * ray_scale, "        "))
    parts.append(dome(hatch_fill or dome_fill, dome_stroke, dome_width))
    body = "\n".join(parts)
    return f'    <symbol id="sun" viewBox="{VIEWBOX}">\n{body}\n    </symbol>\n'


if __name__ == "__main__":
    print(f"# mark geometry: {RAYS} rays, butt ends, dome r={DOME_R:.0f}, "
          f"sun {SUN_WIDTH:.0f} units wide, script {SCRIPT_TO_SUN:.0f} units wide target")
    print(sun_symbol())
