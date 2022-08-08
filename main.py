from math import ceil
import drawSvg as draw
from PIL import Image
import tkinter
from tkinter import filedialog

def round_up(value, r):
  if r == 0: r = 1
  return ceil(value / r) * r

def closest(value, r):
  if r == 0: r = 1
  return int(value / r) * r

def most_frequent(List):
  return max(set(List), key = List.count)

def append_dict(dic, key, value):
  if key in dic:
    dic[key].append(value)
  else:
    dic[key] = [value]

def hexify(v, p):
  return ("0" + hex(closest(v, p)).replace("0x", ""))[-2:]

def convert(path, r, p, m):
  with Image.open(path).convert('RGBA') as image:
    groups = {}
    w = round_up(image.width, r)
    h = round_up(image.height, r)
    d = draw.Drawing(w, h)
    for x in range(r, w, 2 * r):
      print(f"{int(100 * x / w)} %   ", end="\r")
      for y in range(r, h, 2 * r):
        if m == "mode":
          pixels = []
          for xx in range(x - r, min(x + r, image.width)):
            for yy in range(y - r, min(y + r, image.height)):
              pixels.append("".join(
                [hexify(v, p) for v in image.getpixel((xx, yy))]))
          rgba = most_frequent(pixels)
        else:
          cr, cg, cb, ca, px_count = 0, 0, 0, 0, 0
          for xx in range(x - r, min(x + r, image.width)):
            for yy in range(y - r, min(y + r, image.height)):
              px_count += 1
              px = image.getpixel((xx, yy))
              cr += px[0]
              cg += px[1]
              cb += px[2]
              ca += px[3]
          rgba = "".join(
                [hexify(v / px_count, p) for v in (cr, cg, cb, ca)])
        dot = draw.Circle(x, h - y, r, 
          fill=f"#{rgba[:6]}", fill_opacity=int(rgba[6:], base=16)/255)
        append_dict(groups, f"circle{rgba}", dot)
    for group in groups.values():
      d.append(draw.Group(group))
    name = f"{path.split('.')[0]}-r{r}-p{p}-m{m}.svg"
    d.saveSvg(name)
    return name

def main():
  while True:
    try:
      print("\n-- Let's make some dots 🤓 --\n")
      tkinter.Tk().withdraw()
      path = filedialog.askopenfile().name
      print(f"📂 Filename: {path}")
      r = int(input("🔴 Radius (px): "))
      p = int(input("🌈 Posterize factor (default: 0): "))
      m = input("🖌️ Color picker (avg, mode): ")
      name = convert(path, r, p, m)
      print(f"\n✅ Successfully created {name}!")
      if input("Exit? (y/n)") == "y": break
    except Exception as ex:
      print(ex)
      print("\nSomething went wrong 🤔\n")

if __name__ == "__main__":
  main()
