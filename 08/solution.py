class Image():
  def __init__(self, raw, nrows, ncols):
    self.raw = raw
    self.nrows = nrows
    self.ncols = ncols
    self.layers = self._read(raw, nrows, ncols)

  def _read(self, raw, nrows, ncols):
    if len(raw)%(nrows*ncols) != 0:
      raise ValueError(f"Length of input ({len(raw)}) is not a multiple of\
                        layer size ({nrows}x{ncols})")
    layers = []
    l = 0
    while True:
      layer = []
      for r in range(nrows):
        row = []
        for c in range(ncols):
          pos = (l*nrows*ncols)+(r*ncols)+c
          row.append(raw[pos])
        layer.append(row)
      layers.append(layer)
      l += 1
      if pos+1 == len(raw):
        break
    return layers

  def _render(self):
    rendered = []
    for r in range(self.nrows):
      row = []
      for c in range(self.ncols):
        pixels = [l[r][c] for l in self.layers]
        row.append("2")
        for p in pixels:
          if p in ["0","1"]:
            row[c] = p
            break
      rendered.append(row)
    return rendered

  def _get_color(self, p):
    if p == "0":
      return u"\u25A0"
    elif p == "1":
      return u"\u25A1"
    elif p == "2":
      return u"\u2800"
    else:
      raise ValueError(f"{p} is not a valid pixel")

  def show(self):
    rendered = self._render()
    for r in rendered:
      c = [self._get_color(p) for p in r]
      print("".join(c))

with open('08/input.txt') as input_file:
  img_raw = input_file.read().rstrip('\n')

height = 6
width = 25
img = Image(img_raw, height, width)

zeros = []
for layer in img.layers:
  count = 0
  for row in layer:
    count += row.count("0")
  zeros.append(count)

l = img.layers[zeros.index(min(zeros))]
ones = 0
twos = 0
for row in l:
  ones += row.count("1")
  twos += row.count("2")

print(f"Result: {ones*twos}")

img.show()
