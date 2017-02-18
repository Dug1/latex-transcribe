from PIL import Image
import numpy as np
from matplotlib import pyplot

def prepare_image(image_url):
    image = Image.open(image_url).convert("L")
    return 1 - (np.float_(np.array(image)) /255)

def histogram(array, axis=0):
    new_arr = np.sum(array, axis=axis)
    return new_arr

def image_blur(image_matrix):
    

def generate_histogram_seperators(image, threshold=0, passes=1, axis=1, box=None):
    if not box:
        box = ((0, 0), image.shape)

    if passes <= 0:
        return [box]

    tl, br =  box
    crop = image[tl[0]:br[0],tl[1]:br[1]]
    h = histogram(crop, 1 - axis)
    pyplot.plot(h)
    pyplot.show()

    prev = threshold - 1
    prev_coordinate = tl[axis]
    boxes = []
    for i in range(h.shape[0]):
        if prev <= threshold and h[i] > threshold:
            box = ((prev_coordinate, tl[1]), (i, br[1])) if axis == 0 else ((tl[0], prev_coordinate), (br[0], i))
            prev_coordinate = i
            boxes.extend(generate_histogram_seperators(image,  threshold, passes - 1, 1 - axis, box))

        prev = h[i]

    box = ((prev_coordinate, tl[1]), (br[0], br[1])) if axis == 0 else ((tl[0], prev_coordinate), (br[0], br[1]))
    boxes.extend(generate_histogram_seperators(image,  threshold, passes - 1, 1 - axis, box))
    return boxes


im_name = "test_images/img3.png"
image = prepare_image(im_name)
boxes = generate_histogram_seperators(image, 0, passes=2)
print(boxes)
for box in boxes:
    tl, br =  box
    crop = image[tl[0]:br[0],tl[1]:br[1]]
    pyplot.imshow(crop)
    pyplot.show()
