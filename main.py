from math import ceil
import drawSvg as draw
from PIL import Image

def round_up(value, r):
  return ceil(value / r) * r

def most_frequent(List):
  return max(set(List), key = List.count)

def append_dict(dic, key, value):
  if key in dic:
    dic[key].append(value)
  else:
    dic[key] = [value]

def convert(filename, r):
  with Image.open(filename).convert('RGB') as image:
    groups = {}
    w = round_up(image.width, r)
    h = round_up(image.height, r)
    d = draw.Drawing(w, h)
    for x in range(r, w, 2 * r):
      for y in range(r, h, 2 * r):
        pixels = []
        for xx in range(x - r, min(x + r, image.width)):
          for yy in range(y - r, min(y + r, image.height)):
            pixels.append("".join(
              [hex(v).replace("0x", "") for v in image.getpixel((xx, yy))]))
        rgb = most_frequent(pixels)
        dot = draw.Circle(x, h - y, r, fill=f"#{rgb}")
        append_dict(groups, f"dot{rgb}", dot)
    for group in groups.values():
      d.append(draw.Group(group))
    name = f"{filename.split('.')[0]}-r{r}.svg"
    d.saveSvg(name)
    return name

def main():
  while True:
    try:
      print("\n-- Let's make some dots 🤓 --\n")
      filename = input("📂 Filename: ")
      r = int(input("🔴 Radius (px): "))
      name = convert(filename, r)
      print(f"\n✅ Successfully created {name}!")
      if input("Exit? (y/n)") != "n": break
    except Exception as ex:
      print(ex)
      print("\nSomething went wrong 🤔\n")

if __name__ == "__main__":
  main()
