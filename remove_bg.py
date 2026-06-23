import rembg
from PIL import Image

input_path = r'C:\Users\ARJAV\PycharmProjects\EComm\EComm\main\static\favicon.png'
output_path = r'C:\Users\ARJAV\PycharmProjects\EComm\EComm\main\static\favicon_transparent.png'

input_image = Image.open(input_path)
output_image = rembg.remove(input_image)
output_image.save(output_path)
print("Saved transparent image to", output_path)
