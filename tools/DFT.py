import cv2
from .DFT_tools import *
__all__ = ('get_contours', 'get_ani')


def color_correction(image_name, *, ID=None, reverse=True, out_name='befor2'):
    green = np.uint8([[[0, 255, 0]]])
    green_hsv = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
    image = cv2.imread(image_name)
    image = ~image if reverse else image
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    green_low = np.array([45, 100, 50])
    green_high = np.array([75, 255, 255])
    curr_mask = cv2.inRange(hsv_img, green_low, green_high)
    hsv_img[curr_mask > 0] = ([75, 255, 200])
    RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)
    ret, threshold = cv2.threshold(gray, 90, 255, 0)
    cv2.imwrite(f'{ID}_{out_name}.jpg', threshold)
    
    
def get_contours(image_name, *, ID=None):
    color_correction(image_name, ID=ID, reverse=True)
    contour_1 = create_contour(image_name)
    contour_2 = create_contour(f'{ID}_befor2.jpg')
    
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].set_aspect('equal', 'datalim')
    ax[1].set_aspect('equal', 'datalim')
    ax[0].set_title('Algorithm 1')
    ax[1].set_title('Algorithm 2')
    ax[0].plot(contour_1[1], contour_1[2], 'k-')
    ax[1].plot(contour_2[1], contour_2[2], 'k-')
    plt.savefig(f'{ID}_after.jpg')
    plt.close('all')


def get_ani(image, *, ID=None, approx_level=60, frames=180):
    time_table, x_table, y_table = create_contour(image)
    coef = coef_list(time_table, x_table, y_table, approx_level)
    space = np.linspace(0, 2*pi, frames)
    coords = np.array([DFT(t, coef, approx_level) for t in space])

    plt.close('all')
    plt.plot(x_table, y_table)
    xmin, xmax = xlim()
    ymin, ymax = ylim()

    anim = visualize(coords[:, 0], coords[:, 1], coef, approx_level, space, [xmin, xmax, ymin, ymax])
    FFwriter = animation.FFMpegWriter(fps=24, extra_args=['-vcodec', 'libx264'])
    anim.save(f'{ID}_Fourier.mp4', writer=FFwriter, dpi=150)
    plt.close('all')