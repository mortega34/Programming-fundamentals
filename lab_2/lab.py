im = {"width": 3,"height": 4,"pixels": [10,10,10,20,20,20,30,30,30,40,40,90]}

def width(image):
    return image["width"]

def height(image):
    return image["height"]

def pixel(image, x, y):
    index = y + width(image)*x
    return image["pixels"][index]

def set_pixel(image, x, y, color):
    index = y + width(image)*x
    image["pixels"][index] = color

def make_image(width, height):
    return {"width": width, "height": height, "pixels": ([0]*width*height)}

def apply_per_pixel(image, f):
    """
     return a new image by applying function f to each pixel of the input image
    """
    result = make_image(width(image), height(image))
    for x in range(height(result)):
        for y in range(width(result)):
            color = pixel(image, x, y)
            set_pixel(result, x, y, f(color))
    return result
                      

def invert(c):
    return abs(255-c)
    
def filter_invert(image):
    return apply_per_pixel(image, invert)


def filter_gaussian_blur(image):
    kernel = [1.0/16, 2.0/16, 1.0/16,
              2.0/16, 4.0/16, 2.0/16,
              1.0/16, 2.0/16, 1.0/16]
    result = convolve2d(image, kernel)
    return result

    

def convolve2d(image, kernel3x3):
    result = make_image(width(image), height(image))
    for x in xrange(height(image)):
        for y in xrange(width(image)):
            blur = apply_kernel(image, x, y, kernel3x3)
            set_pixel(result, x, y, blur)
    return result

def apply_kernel(image, x, y, kernel):
    blur = 0
    kernel_index = 0
    for i in range(-1,2):
        for j in range(-1,2):
            try:
                if in_bounds(image,i,j,x,y):
                    neighbor = pixel(image, x+i, y+j)
                    blur = blur + neighbor * kernel[kernel_index]
                kernel_index += 1
            except IndexError:
                pass

    return int(round(blur))
    


def in_bounds(image, current_i, current_j, pixel_x_index, pixel_y_index):
    if (pixel_x_index+current_i)>=0 and (pixel_y_index+current_j) >=0 and (pixel_x_index+current_i)< height(image) and (pixel_y_index+current_j) < width(image):
        return True
    return False

def filter_edge_detect(image):
    Kx = [-1, 0, 1,
          -2, 0, 2,
          -1, 0, 1]
    Ky = [-1, -2, -1,
           0, 0, 0,
           1, 2, 1]
    Ox = convolve2d(image, Kx)
    Oy = convolve2d(image, Ky)

    assert width(Ox) == width(Oy)
    assert height(Oy) == height(Oy)

    
    result = combine_images(Ox, Oy, root_sum_squares)
    return result



def combine_images(image1, image2, f):
    
    result = make_image(width(image1), height(image1))
    
    for i in xrange(width(image1)*height(image1)):
            result["pixels"][i] = legalize_range(f(image1["pixels"][i], image2["pixels"][i]))

    return result


def root_sum_squares(pixel1, pixel2):
    return int(round(((pixel1**2 + pixel2**2))**0.5))
    


def legalize_range(color):
    """Sets max pixel color values 0 <= color<= 255
    """
    if color > 255:
        return 255
    elif color < 0:
        return 0
    return color
            
    

        
        
