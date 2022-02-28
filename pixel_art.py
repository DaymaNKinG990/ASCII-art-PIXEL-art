import pygame as pg
import numpy as np
import pygame.gfxdraw
import cv2


class PixelArtConverter:
    def __init__(self, input_path: str, output_path: str, pixel_size: int = 7, color_lvl: int = 8) -> None:
        pg.init()
        self.input_path = input_path
        self.output_path = output_path
        self.PIXEL_SIZE = pixel_size
        self.COLOR_LVL = color_lvl
        self.image = self.get_image()
        self.cv2_image = None
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

    def draw_converted_image(self) -> None:
        color_indices = self.image // self.COLOR_COEFF
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                color_key = tuple(color_indices[x, y])
                if sum(color_key):
                    color = self.PALETTE[color_key]
                    pygame.gfxdraw.box(self.surface, (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE), color)

    def create_palette(self) -> (dict, int):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = {}
        color_coeff = int(color_coeff)
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color
        return palette, color_coeff

    def get_image(self) -> cv2:
        self.cv2_image = cv2.imread(self.input_path)
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
        return image

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
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(self.output_path + '\\pixel_art.jpg', cv2_img)

    def run(self) -> None:
        self.draw()
        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick()
        self.save_image()
        exit()


class PixelArtVideoConverter:
    def __init__(self, input_path: str, output_path: str, pixel_size: int = 7, color_lvl: int = 8) -> None:
        pg.init()
        self.input_path = input_path
        self.output_path = output_path
        self.capture = cv2.VideoCapture(input_path)
        self.PIXEL_SIZE = pixel_size
        self.COLOR_LVL = color_lvl
        self.image = self.get_image()
        self.cv2_image = None
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.PALETTE, self.COLOR_COEFF = self.create_palette()
        self.rec_fps = 25
        self.record = False
        self.recorder = cv2.VideoWriter(output_path + '\\pixel_art.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                                        self.rec_fps, self.RES)

    @staticmethod
    @njit(fastmath=True)
    def accelerate_conversion(image: cv2, width: int, height: int, color_coeff: int, step: int) -> list:
        array_of_values = []
        for x in range(0, width, step):
            for y in range(0, height, step):
                r, g, b = image[x, y] // color_coeff
                if r + g + b:
                    array_of_values.append(((r, g, b), (x, y)))
        return array_of_values

    def get_frame(self) -> cv2:
        frame = pg.surfarray.array3d(self.surface)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return cv2.transpose(frame)

    def record_frame(self) -> None:
        if self.record:
            frame = self.get_frame()
            self.recorder.write(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                self.record = not self.record
                cv2.destroyAllWindows()

    def draw_converted_image(self) -> None:
        self.image = self.get_image()
        array_of_values = accelerate_conversion(self.image, self.WIDTH, self.HEIGHT, self.COLOR_COEFF, self.PIXEL_SIZE)
        for color_key, (x, y) in array_of_values:
            color = self.PALETTE[color_key]
            pygame.gfxdraw.box(self.surface, (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE), color)

    def create_palette(self) -> (dict, int):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = {}
        color_coeff = int(color_coeff)
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color
        return palette, color_coeff

    def get_image(self) -> cv2:
        ret, self.cv2_image = self.capture.read()
        if not ret:
            exit()
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
        return image

    def draw_cv2_image(self) -> None:
        resized_cv2_image = cv2.resize(self.cv2_image, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.imshow('img', resized_cv2_image)

    def draw(self) -> None:
        self.surface.fill('black')
        self.draw_converted_image()

    def run(self):
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
