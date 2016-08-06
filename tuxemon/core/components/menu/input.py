# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from functools import partial

from core import tools
from core.components.menu import Menu
from core.components.menu.interface import MenuItem
from core.components.ui.text import TextArea

import pygame


class InputMenu(Menu):
    background = None
    draw_borders = False

    chars = u"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890.-_!@#$%&*"
    alphabet_length = 26

    def startup(self, *items, **kwargs):
        """

        Accepted Keyword Arguments:
            prompt: String used to let user know what value is being inputted (ie "Name?", "IP Address?")

        :param items:
        :param kwargs:
        :return:
        """
        super(InputMenu, self).startup(*items, **kwargs)
        self.input_string = ""

        # area where the input will be shown
        self.text_area = TextArea(self.font, self.font_color, (96, 96, 96))
        self.text_area.animated = False
        self.text_area.rect = pygame.Rect(tools.scale_sequence([100, 20, 80, 100]))
        self.sprites.add(self.text_area)

        # prompt
        self.prompt = TextArea(self.font, self.font_color, (96, 96, 96))
        self.prompt.animated = False
        self.prompt.rect = pygame.Rect(tools.scale_sequence([50, 20, 80, 100]))
        self.sprites.add(self.prompt)

        self.prompt.text = kwargs.get("prompt", "")

    def calc_internal_rect(self):
        w = self.rect.width - self.rect.width * .8
        h = self.rect.height - self.rect.height * .5
        rect = self.rect.inflate(-w, -h)
        rect.top = self.rect.centery * .7
        return rect

    def initialize_items(self):
        self.menu_items.columns = self.alphabet_length // 2

        # add the keys
        for char in self.chars:
            yield MenuItem(self.shadow_text(char), None, None, partial(self.add_input_char, char))

        yield MenuItem(self.shadow_text("<="), None, None, partial(self.backspace))
        yield MenuItem(self.shadow_text("END"), None, None, partial(self.confirm))

    def process_event(self, event):
        super(InputMenu, self).process_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.backspace()

            char = event.unicode
            if char in self.chars:
                self.add_input_char(char)

    def backspace(self):
        self.input_string = self.input_string[:-1]
        self.update_text_area()

    def add_input_char(self, char):
        self.input_string += char
        self.update_text_area()

    def update_text_area(self):
        self.text_area.text = self.input_string

    def confirm(self):
        pass