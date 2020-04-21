import numpy as np
import matplotlib.pyplot as plt

def grayscale(img):
    '''
    Converts RGB image to Grayscale
    '''
    gray=np.zeros((img.shape[0],img.shape[1]))
    gray=img[:,:,0]*0.2989+img[:,:,1]*0.5870+img[:,:,2]*0.1140
    return gray

def plot_optical_flow(img,U,V,titleStr):
    '''
    Plots optical flow given U,V and one of the images
    '''
    
    # Change t if required, affects the number of arrows
    # t should be between 1 and min(U.shape[0],U.shape[1])
    t = 10 
    
    # Subsample U and V to get visually pleasing output
    U1 = U[::t,::t]
    V1 = V[::t,::t]
    
    # Create meshgrid of subsampled coordinates
    r, c = img.shape[0],img.shape[1]
    cols,rows = np.meshgrid(np.linspace(0,c-1,c), np.linspace(0,r-1,r))
    cols = cols[::t,::t]
    rows = rows[::t,::t]
    
    # Plot optical flow
    plt.figure(figsize=(10,10))
    plt.imshow(img)
    plt.quiver(cols,rows,U1,V1)
    plt.title(titleStr)
    plt.show()


    
def LucasKanadeOpticalFlow(im1,im2,window):
    '''
    Implement the Lucas-Kanade algorithm
    Inputs: the two images, window size
    Returns: u, v - the optical flow
    '''
    
    """ ==========
    YOUR CODE HERE
    ========== """
    
    return u, v


images = []
for i in range(1,5):
    images.append(plt.imread('OpticalFlowImages/im'+str(i)+'.png')[:,:288,:])
# each image after converting to gray scale is of size -> 400x288

window = 13
U, V = LucasKanadeOpticalFlow(grayscale(images[0]),grayscale(images[1]), window)
plot_optical_flow(images[0], U, V, 'image2 = ' + str(1) + ', window = ' + str(window))

window = 13
U, V = LucasKanadeOpticalFlow(grayscale(images[0]),grayscale(images[2]), window)
plot_optical_flow(images[0], U, V, 'image2 = ' + str(2) + ', window = ' + str(window))

window = 13
U, V = LucasKanadeOpticalFlow(grayscale(images[0]),grayscale(images[3]), window)
plot_optical_flow(images[0], U, V, 'image2 = ' + str(3) + ', window = ' + str(window))
