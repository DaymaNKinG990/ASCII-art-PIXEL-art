from ascii_art import AsciiArtConverter, AsciiArtVideoConverter
from ascii_art_color import AsciiColorArtConverter, AsciiColorArtVideoConverter
from pixel_art import PixelArtConverter, PixelArtVideoConverter


aac = AsciiArtConverter('C:\\Users\\DaymaNKinG\\Desktop\\myself.jpg', 'C:\\Users\\DaymaNKinG\\Desktop')
aac.run()

aavc = AsciiArtVideoConverter('C:\\Users\\DaymaNKinG\\Desktop\\test.mp4', 'C:\\Users\\DaymaNKinG\\Desktop')
aavc.run()

acac = AsciiColorArtConverter('C:\\Users\\DaymaNKinG\\Desktop\\myself.jpg', 'C:\\Users\\DaymaNKinG\\Desktop')
acac.run()

acavc = AsciiColorArtVideoConverter('C:\\Users\\DaymaNKinG\\Desktop\\test.mp4', 'C:\\Users\\DaymaNKinG\\Desktop')
acavc.run()

pac = PixelArtConverter('C:\\Users\\DaymaNKinG\\Desktop\\myself.jpg', 'C:\\Users\\DaymaNKinG\\Desktop')
pac.run()

pavc = PixelArtVideoConverter('C:\\Users\\DaymaNKinG\\Desktop\\test.mp4', 'C:\\Users\\DaymaNKinG\\Desktop')
pavc.run()
