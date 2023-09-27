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

class MORPH:
    
    
    
    def __init__(self, image, param):
        self.data = image
        self.param = param
        
    def dilation(self):
        # Decode the image data
        image_data = decodeURI(self.data)
    
        # Convert to grayscale if it's a color image
        if len(image_data.shape) == 3:
            image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    
        # Define the disk-shaped kernel for dilation
        
        radius = self.param.get('radius')
        size = 2 * int(radius) + 1
        structure_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))

        
        
    
        # Perform image dilation
        dilated_image = cv2.dilate(image_data, structure_element, iterations=1)
    
        font_path = r"C:/Users/ankit/Project_DRDO_1-20230923T191948Z-001/Project_DRDO_1/Poppins-SemiBold.ttf"
        font_props = FontProperties(fname=font_path)
    
        data = {
            'image': dilated_image,
            'x_label': 'X Spatial Location',
            'x_label_color': 'white',
            'y_label': 'Y Spatial Location',
            'y_label_color': 'white'
        }
    
        # Create a new figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
    
        # Customize the plot based on the provided data
        im = ax.imshow(dilated_image, cmap='gray')
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
        ax.set_xticks(np.arange(0, dilated_image.shape[1], 50))  # Adjust the step size as needed
        ax.set_yticks(np.arange(0, dilated_image.shape[0], 50))  # Adjust the step size as needed
        ax.xaxis.set_tick_params(labelcolor='white')
        ax.yaxis.set_tick_params(labelcolor='white')
        
        
        
    
        # Convert the plot to a base64 URI
        result = plot_to_base64_uri(fig)
        intensity_hist_base64 = plot_to_base64_uri(intensity_histogram(result))
        
        
    
        # Create a dictionary containing both results
        result_dict = {
            "primary": result,
            "intensity_histogram": intensity_hist_base64,
        }
    
        # Serialize the dictionary to JSON
        json_result = json.dumps(result_dict)
    
        return json_result


    def erosion(self):
        # Decode the image data
        image_data = decodeURI(self.data)
    
        # Convert to grayscale if it's a color image
        if len(image_data.shape) == 3:
            image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    
        # Define the disk-shaped kernel for dilation
        
        radius = self.param.get('radius')
        size = 2 * int(radius) + 1
        structure_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
    
        
        
    
        # Perform image dilation
        dilated_image = cv2.erode(image_data, structure_element, iterations=1)
    
        font_path = r"C:/Users/ankit/Project_DRDO_1-20230923T191948Z-001/Project_DRDO_1/Poppins-SemiBold.ttf"
        font_props = FontProperties(fname=font_path)
    
        data = {
            'image': dilated_image,
            'x_label': 'X Spatial Location',
            'x_label_color': 'white',
            'y_label': 'X Spatial Location',
            'y_label_color': 'white'
        }
    
        # Create a new figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
    
        # Customize the plot based on the provided data
        im = ax.imshow(dilated_image, cmap='gray')
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
        ax.set_xticks(np.arange(0, dilated_image.shape[1], 50))  # Adjust the step size as needed
        ax.set_yticks(np.arange(0, dilated_image.shape[0], 50))  # Adjust the step size as needed
        ax.xaxis.set_tick_params(labelcolor='white')
        ax.yaxis.set_tick_params(labelcolor='white')
        
        
        
    
        # Convert the plot to a base64 URI
        result = plot_to_base64_uri(fig)
        intensity_hist_base64 = plot_to_base64_uri(intensity_histogram(result))
        
        
    
        # Create a dictionary containing both results
        result_dict = {
            "primary": result,
            "intensity_histogram": intensity_hist_base64,
        }
    
        # Serialize the dictionary to JSON
        json_result = json.dumps(result_dict)
    
        return json_result
    
    
    def opening(self):
        # Decode the image data
        image_data = decodeURI(self.data)
    
        # Convert to grayscale if it's a color image
        if len(image_data.shape) == 3:
            image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    
        # Define the disk-shaped kernel for dilation
        
        radius = self.param.get('radius')
        size = 2 * int(radius) + 1
        structure_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
    
        
        
    
        # Perform image dilation
        opened_image = cv2.morphologyEx(image_data, cv2.MORPH_OPEN, structure_element)
    
        font_path = r"C:/Users/ankit/Project_DRDO_1-20230923T191948Z-001/Project_DRDO_1/Poppins-SemiBold.ttf"
        font_props = FontProperties(fname=font_path)
    
        data = {
            'image': opened_image,
            'x_label': 'X Spatial Location',
            'x_label_color': 'white',
            'y_label': 'Y Spatial Location',
            'y_label_color': 'white'
        }
    
        # Create a new figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
    
        # Customize the plot based on the provided data
        im = ax.imshow(opened_image, cmap='gray')
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
        ax.set_xticks(np.arange(0, opened_image.shape[1], 50))  # Adjust the step size as needed
        ax.set_yticks(np.arange(0, opened_image.shape[0], 50))  # Adjust the step size as needed
        ax.xaxis.set_tick_params(labelcolor='white')
        ax.yaxis.set_tick_params(labelcolor='white')
        
        
        
    
        # Convert the plot to a base64 URI
        result = plot_to_base64_uri(fig)
        intensity_hist_base64 = plot_to_base64_uri(intensity_histogram(result))
        
        
    
        # Create a dictionary containing both results
        result_dict = {
            "primary": result,
            "intensity_histogram": intensity_hist_base64,
        }
    
        # Serialize the dictionary to JSON
        json_result = json.dumps(result_dict)
    
        return json_result
    
    def closing(self):
            # Decode the image data
            image_data = decodeURI(self.data)
        
            # Convert to grayscale if it's a color image
            if len(image_data.shape) == 3:
                image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        
            # Define the disk-shaped kernel for dilation
            
            radius = self.param.get('radius')
            size = 2 * int(radius) + 1
            structure_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
        
            
            
        
            # Perform image dilation
            closed_image = cv2.morphologyEx(image_data, cv2.MORPH_CLOSE, structure_element)
    
        
            font_path = r"C:/Users/ankit/Project_DRDO_1-20230923T191948Z-001/Project_DRDO_1/Poppins-SemiBold.ttf"
            font_props = FontProperties(fname=font_path)
        
            data = {
                'image': closed_image,
                'x_label': 'X Spatial Location',
                'x_label_color': 'white',
                'y_label': 'Y Spatial Location',
                'y_label_color': 'white'
            }
        
            # Create a new figure and axis
            fig, ax = plt.subplots(figsize=(8, 6))
        
            # Customize the plot based on the provided data
            im = ax.imshow(closed_image, cmap='gray')
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
            ax.set_xticks(np.arange(0, closed_image.shape[1], 50))  # Adjust the step size as needed
            ax.set_yticks(np.arange(0, closed_image.shape[0], 50))  # Adjust the step size as needed
            ax.xaxis.set_tick_params(labelcolor='white')
            ax.yaxis.set_tick_params(labelcolor='white')
            
            
            
        
            # Convert the plot to a base64 URI
            result = plot_to_base64_uri(fig)
            intensity_hist_base64 = plot_to_base64_uri(intensity_histogram(result))
            
            
        
            # Create a dictionary containing both results
            result_dict = {
                "primary": result,
                "intensity_histogram": intensity_hist_base64,
            }
        
            # Serialize the dictionary to JSON
            json_result = json.dumps(result_dict)
        
            return json_result