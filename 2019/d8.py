def num_zeros(layer):
    num = 0
    for row in layer:
        num += row.count('0')
    return num

def min_zeros_layer(img):
    min_zeros = float('inf')
    min_layer = None
    for layer in img:
        cur_zeros = num_zeros(layer)
        if cur_zeros < min_zeros:
            min_zeros = cur_zeros
            min_layer = layer
    return min_layer

def product_min_layer(layer):
    count_one, count_two = 0, 0
    for row in layer:
        count_one += row.count('1')
        count_two += row.count('2')
    return count_one * count_two

def get_pixel(img, i, j):
    pixel = None
    for layer in img:
        # not transparent
        pixel = layer[i][j]
        if pixel != '2':
            return pixel
    return pixel

def decode_image(img):
    nimg = []
    row, col = 6, 25
    for i in range(row):
        pixels = []
        for j in range(col):
            pixel = get_pixel(img, i, j)
            if pixel == '0':
                pixels.append(' ')
            else:
                pixels.append('#')
        nimg.append(''.join(pixels))
    return nimg

if __name__ == '__main__':
    img = []
    with open('d8.txt') as fin:
        row, col = 6, 25
        read_all = False
        while not read_all:
            layer = []
            for _ in range(row):
                s = fin.read(col)
                if s.strip() == '':
                    read_all = True
                    break
                layer.append(s)
            if layer: img.append(layer)
    
    # min_layer = min_zeros_layer(img)
    # x = product_min_layer(min_layer)
    # print(x)
    nimg = decode_image(img)
    for l in nimg:
        print(l)
