from flask import request
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import base64
from PIL import Image
from io import BytesIO
import json

def decodeURI(data):
    image_data = data.split(',')[1]

    # Decode the Base64 data
    image_bytes = base64.b64decode(image_data)
    
    # Open the image using PIL
    image = Image.open(BytesIO(image_bytes))
    
    return np.array(image);

def plot_to_base64_uri(fig):
    # Capture the plot as a BytesIO object
    buffer = BytesIO()
    fig.savefig(buffer, format='jpeg')
    buffer.seek(0)

    # Encode the BytesIO object as Base64
    base64_image_uri = base64.b64encode(buffer.read()).decode()

    # Close the plot
    plt.close(fig)

    # Return the Base64 image URI
    return f'data:image/jpeg;base64,{base64_image_uri}'


def generate_custom_plot(image_data, x_label='X Spatial Location', y_label='Y Spatial Location', x_label_color='white', y_label_color='white'):
    font_path = r"C:/Users/ankit/Project_DRDO_1-20230923T191948Z-001/Project_DRDO_1/Poppins-SemiBold.ttf"
    font_props = FontProperties(fname=font_path)

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Customize the plot based on the provided data
    im = ax.imshow(image_data, cmap='gray')

    cbar = plt.colorbar(im)
    tick_labels = cbar.ax.get_yticklabels()
    for label in tick_labels:
        label.set_color('white')
    cbar.outline.set_edgecolor('white')

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.set_xlabel(x_label, color=x_label_color, fontproperties=font_props)
    ax.set_ylabel(y_label, color=y_label_color, fontproperties=font_props)

    return fig


    
class THRESHOLD:
    
    def __init__(self, image, param):
        self.data = image
        self.param = param
        
    def seg(self):
        
        image = decodeURI(self.data)
        
        radius = self.param.get('radius')
        ksize = int(self.param.get('ksize'))
        
        size = 2 * int(radius) + 1
        structure_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
        opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, structure_element)

# Subtract the opened image from the original image to get the skull image
        skull_image = cv2.subtract(image, opened_image)

# Subtract the skull image from the opened image to get the clear skull image
        clear_skull_image = cv2.subtract(skull_image, opened_image)

# Subtract the clear skull image from the original image to get the output image
        output_image = cv2.subtract(image, clear_skull_image)
        
        unique_values = np.unique(output_image)
        unique_values = unique_values[unique_values != 0]
        euler_phi = np.zeros(unique_values.shape, dtype=int)
        
        for i, a in enumerate(unique_values):
            for b in unique_values:
                if a != b:
                    gcd_ab = np.gcd(a, b)
                    if gcd_ab == 1:
                        euler_phi[i] += 1
                        
        

        # Step 3: Calculate the sum of Euler's totient function for all pairs
        sum_euler_phi = sum(euler_phi)
        
        # Step 4: Divide the sum by the count of unique pixel values (excluding 0) to calculate the threshold T
        T = sum_euler_phi / len(unique_values)
        
        # Step 5: Apply the threshold to the original image to generate the segmented image
        segmented_image = np.where(output_image > T, 255, 0).astype(np.uint8)  # Convert to uint8 for OpenCV
        
        # If you want to label connected components in the segmented image:
            
        if ksize % 2 == 0:
            ksize += 1
        
        # Apply median blur to the segmented image
        median_filtered_image = cv2.medianBlur(segmented_image, ksize=ksize)

# Convert images to uint8 for proper display
        opened_image = opened_image.astype('uint8')
        skull_image = skull_image.astype('uint8')
        clear_skull_image = clear_skull_image.astype('uint8')
        output_image = output_image.astype('uint8')
        org_image = image.astype('uint8')
        
        opened_image = generate_custom_plot(opened_image)
        skull_image = generate_custom_plot(skull_image)
        clear_skull_image = generate_custom_plot(clear_skull_image)
        output_image = generate_custom_plot(output_image)
        org_image = generate_custom_plot(org_image)
        segmented_image = generate_custom_plot(segmented_image)
        # Create a Matplotlib figure for median_filtered_image
        median_filtered_image_figure = generate_custom_plot(median_filtered_image)
        
        
        
        # Convert the Matplotlib figure to a Base64 URI
        


        
        opened_image = plot_to_base64_uri(opened_image)
        skull_image = plot_to_base64_uri(skull_image)
        clear_skull_image = plot_to_base64_uri(clear_skull_image)
        output_image = plot_to_base64_uri(output_image)
        org_image = plot_to_base64_uri(org_image)
        segmented_image = plot_to_base64_uri(segmented_image)
        final_result = plot_to_base64_uri(median_filtered_image_figure)
        
        
        if self.param.get('subsubtype') == "open":
            
            result_dict = {
                "primary": opened_image,
                "intensity_histogram": final_result,
            }
        
                    
        elif self.param.get('subsubtype') == "clear":
            
            result_dict = {
                "primary": clear_skull_image,
                "intensity_histogram": final_result,
            }
            
        elif self.param.get('subsubtype') == "output":
            
            result_dict = {
                "primary": output_image,
                "intensity_histogram": final_result,
            }
            
        else:
            
            result_dict = {
                "primary": segmented_image,
                "intensity_histogram": final_result,
            }
            
        
        
        
        
        
        json_result = json.dumps(result_dict)
        return json_result
    
        
    