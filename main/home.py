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

def plot_to_base64_uri(plot):
        # Capture the plot as a BytesIO object
    buffer = BytesIO()
    plot.savefig(buffer, format='jpeg')
    buffer.seek(0)

    # Encode the BytesIO object as Base64
    base64_image_uri = base64.b64encode(buffer.read()).decode()
    
    
    # Close the plot
    plt.close(plot)
    
    
    # Return the Base64 image URI
    return f'data:image/jpeg;base64,{base64_image_uri}'

def intensity_histogram(image_path):
    
    image = decodeURI(image_path)
    
    
    if image is not None:
        # Continue with histogram calculations
        hist = cv2.calcHist([image], [0], None, [256 if image.max() > 1 else 2], [0, 256] if image.max() > 1 else [0, 1])
        hist = np.ravel(hist)
        # Create the histogram plot
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.hist(hist, bins=256 if image.max() > 1 else 2, range=(0, 256) if image.max() > 1 else (0, 1), density=True, color='#FBAF00', alpha=0.7)
        plt.xlabel('Pixel Value')
        plt.ylabel('Normalized Frequency')
        plt.xlim([0, 256] if image.max() > 1 else [0, 1])

        # Remove the grid and plot box
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.grid(False)
        
        return fig
        


class HOME:
    
    
    
    def __init__(self, image, param):
        self.data = image
        self.param = param
    
        
    def histo(self):
        
    
        
      
        image = decodeURI(self.data)
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        equalized_image = cv2.equalizeHist(image)
        
        font_path = r"C:/Users/ankit/Project_DRDO_1-20230923T191948Z-001/Project_DRDO_1/Poppins-SemiBold.ttf"
        font_props = FontProperties(fname=font_path)
        
        data = {
            'image': equalized_image,
            'x_label': 'Pixel Value',
            'x_label_color': 'white',
            'y_label': 'Frequency',
            'y_label_color': 'white'
        }
        
        # Create a new figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Customize the plot based on the provided data
        im = ax.imshow(data['image'], cmap='gray')
        
        cbar = plt.colorbar(im)
        cbar.ax.yaxis.set_tick_params(color='white')  # Set color of colorbar tick labels
        cbar.outline.set_edgecolor('white')
        
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.set_xlabel(data['x_label'], color=data['x_label_color'], fontproperties=font_props)
        ax.set_ylabel(data['y_label'], color=data['y_label_color'], fontproperties=font_props)
        
        # Set x and y-axis tick labels
        ax.set_xticks(np.arange(0, equalized_image.shape[1], 50))  # Adjust the step size as needed
        ax.set_yticks(np.arange(0, equalized_image.shape[0], 50))  # Adjust the step size as needed
        ax.xaxis.set_tick_params(labelcolor='white')
        ax.yaxis.set_tick_params(labelcolor='white')

        result = plot_to_base64_uri(fig)
        intensity_hist_base64 = plot_to_base64_uri(intensity_histogram(result))

        # Create a dictionary containing both results
        result_dict = {
            "primary": result,
            "intensity_histogram": intensity_hist_base64
        }

        # Serialize the dictionary to JSON
        json_result = json.dumps(result_dict)

        return json_result
    
    
    
    

    def canny(self):
        # Decode the image data
        image_data = decodeURI(self.data)
    
        # Convert to grayscale if it's a color image
        if len(image_data.shape) == 3:
            image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    
        font_path = r"C:/Users/ankit/Project_DRDO_1-20230923T191948Z-001/Project_DRDO_1/Poppins-SemiBold.ttf"
        font_props = FontProperties(fname=font_path)
    
        # Customize Canny parameters based on the provided parameters
        threshold1 = self.param.get("threshold1", 50)
        threshold2 = self.param.get("threshold2", 150)
       
    
        # Apply Canny edge detection
        edges = cv2.Canny(image_data, threshold1, threshold2)
    
        data = {
            'image': edges,
            'x_label': 'Pixel Value',
            'x_label_color': 'white',
            'y_label': 'Frequency',
            'y_label_color': 'white'
        }
    
        # Create a new figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
    
        # Customize the plot based on the provided data
        im = ax.imshow(edges, cmap='gray')
    
        # Set colorbar properties
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
        ax.set_xlabel(data['x_label'], color=data['x_label_color'], fontproperties=font_props)
        ax.set_ylabel(data['y_label'], color=data['y_label_color'], fontproperties=font_props)
    
        # Set x and y-axis tick labels
        ax.set_xticks(np.arange(0, edges.shape[1], 50))  # Adjust the step size as needed
        ax.set_yticks(np.arange(0, edges.shape[0], 50))  # Adjust the step size as needed
        ax.xaxis.set_tick_params(labelcolor='white')
        ax.yaxis.set_tick_params(labelcolor='white')
    
        # Convert the plot to a base64 URI
        result = plot_to_base64_uri(fig)
        intensity_hist_base64 = plot_to_base64_uri(intensity_histogram(result))
    
        # Create a dictionary containing both results
        result_dict = {
            "primary": result,
            "intensity_histogram": intensity_hist_base64
        }
    
        # Serialize the dictionary to JSON
        json_result = json.dumps(result_dict)
    
        return json_result
    
    def pseudo_color_mapping(self):
        # Decode the image data
        image_data = decodeURI(self.data)
    
        # Convert to grayscale if it's a color image
        if len(image_data.shape) == 3:
            image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    
        font_path = r"C:/Users/ankit/Project_DRDO_1-20230923T191948Z-001/Project_DRDO_1/Poppins-SemiBold.ttf"
        font_props = FontProperties(fname=font_path)
    
        # Define the colormap to use
        if self.param.get('colorMap') == 0:
            colormap =  cv2.COLORMAP_JET
        elif self.param.get('colorMap') == 1:
            colormap =  cv2.COLORMAP_GRAY
        elif self.param.get('colorMap') == 2:
            colormap =  cv2.COLORMAP_VIRIDIS
        elif self.param.get('colorMap') == 3:
            colormap =  cv2.COLORMAP_PARULA
        else:
            colormap =  cv2.COLORMAP_HOT
            
        
            
 
    
        # Apply pseudo-color mapping to the grayscale image
        pseudo_color_image = cv2.applyColorMap(image_data, colormap)
    
        data = {
            'image': pseudo_color_image,
            'x_label': 'X Label',
            'x_label_color': 'white',
            'y_label': 'Y Label',
            'y_label_color': 'white'
        }
    
        # Create a new figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
    
        # Customize the plot based on the provided data
        im = ax.imshow(pseudo_color_image)
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
        ax.set_xlabel(data['x_label'], color=data['x_label_color'], fontproperties=font_props)
        ax.set_ylabel(data['y_label'], color=data['y_label_color'], fontproperties=font_props)
    
        # Set x and y-axis tick labels
        ax.set_xticks(np.arange(0, pseudo_color_image.shape[1], 50))  # Adjust the step size as needed
        ax.set_yticks(np.arange(0, pseudo_color_image.shape[0], 50))  # Adjust the step size as needed
        ax.xaxis.set_tick_params(labelcolor='white')
        ax.yaxis.set_tick_params(labelcolor='white')
    
        # Convert the plot to a base64 URI
        result = plot_to_base64_uri(fig)
        intensity_hist_base64 = plot_to_base64_uri(intensity_histogram(result))
    
        # Create a dictionary containing both results
        result_dict = {
            "primary": result,
            "intensity_histogram": intensity_hist_base64
        }
    
        # Serialize the dictionary to JSON
        json_result = json.dumps(result_dict)
    
        return json_result
