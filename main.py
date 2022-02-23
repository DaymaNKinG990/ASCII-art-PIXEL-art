from ascii_art import AsciiArtConverter, AsciiArtVideoConverter
from ascii_art_color import AsciiColorArtConverter
from pixel_art import PixelArtConverter

'''
aac = AsciiArtConverter('C:\\Users\\DaymaNKinG\\Desktop\\myself.jpg', 'C:\\Users\\DaymaNKinG\\Desktop')
aac.run()

aavc = AsciiArtVideoConverter('C:\\Users\\DaymaNKinG\\Desktop\\test.mp4', 'C:\\Users\\DaymaNKinG\\Desktop')
aavc.run()
'''
acac = AsciiColorArtConverter('C:\\Users\\DaymaNKinG\\Desktop\\myself.jpg', 'C:\\Users\\DaymaNKinG\\Desktop')
acac.save_image()
'''
pac = PixelArtConverter('C:\\Users\\DaymaNKinG\\Desktop\\myself.jpg', 'C:\\Users\\DaymaNKinG\\Desktop')
pac.save_image()
'''