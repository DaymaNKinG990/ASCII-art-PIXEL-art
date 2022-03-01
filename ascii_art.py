import pygame as pg
import cv2
from numba import njit


class AsciiArtConverter:
    def __init__(self, input_path: str, output_path: str, font_size: int = 12) -> None:
        pg.init()
        self.input_path = input_path
        self.output_path = output_path
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.ASCII_CHARS = ' .",:;!~+-xmo*#W&8@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.SysFont('Сourier', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

    def draw_converted_image(self) -> None:
        char_indices = self.image // self.ASCII_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[x, y]
                if char_index:
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))

    def get_image(self) -> cv2:
        self.cv2_image = cv2.imread(self.input_path)
        transposed_image = cv2.transpose(self.cv2_image)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_RGB2GRAY)
        return gray_image

    def draw_cv2_image(self) -> None:
        resized_cv2_image = cv2.resize(self.cv2_image, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.imshow('img', resized_cv2_image)

    def draw(self) -> None:
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()

    def save_image(self) -> None:
        pygame_image = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_image)
        cv2.imwrite(self.output_path + '\\ascii_art.jpg', cv2_img)

    def run(self) -> None:
        self.draw()
        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick()
        self.save_image()
        exit()


class AsciiArtVideoConverter:
    def __init__(self, input_path: str, output_path: str, font_size: int = 12) -> None:
        pg.init()
        self.input_path = input_path
        self.output_path = output_path
        self.capture = cv2.VideoCapture(input_path)
        self.image = self.get_image()
        self.cv2_image = None
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.ASCII_CHARS = ' .",:;!~+-xmo*#W&8@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.SysFont('Сourier', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]
        self.rec_fps = 25
        self.record = False
        self.recorder = cv2.VideoWriter(output_path + '\\ascii.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                                        self.rec_fps, self.RES)

    def get_frame(self) -> cv2:
        return cv2.transpose(pg.surfarray.array3d(self.surface))

    def record_frame(self) -> None:
        if self.record:
            frame = self.get_frame()
            self.recorder.write(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                self.record = not self.record
                cv2.destroyAllWindows()

    @staticmethod
    @njit(fastmath=True)
    def accelerate_conversion(image: cv2, width: int, height: int, ascii_coeff: int, step: int) -> list:
        array_of_values = []
        for x in range(0, width, step):
            for y in range(0, height, step):
                char_index = image[x, y] // ascii_coeff
                if char_index:
                    array_of_values.append((char_index, (x, y)))
        return array_of_values

    def draw_converted_image(self) -> None:
        self.image = self.get_image()
        array_of_values = self.accelerate_conversion(self.image, self.WIDTH, self.HEIGHT, self.ASCII_COEFF,
                                                     self.CHAR_STEP)
        for char_index, pos in array_of_values:
            self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], pos)

    def get_image(self) -> cv2:
        ret, self.cv2_image = self.capture.read()
        if not ret:
            exit()
        transposed_image = cv2.transpose(self.cv2_image)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def draw(self) -> None:
        self.surface.fill('black')
        self.draw_converted_image()

    def run(self) -> None:
        self.record = not self.record
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
            self.record_frame()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()
