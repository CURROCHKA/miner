'''stats_button = {'topleft': [self.buttons['topleft_button'].button_rect.collidepoint(mouse_pos),
                                    self.settings.topleft_who, self.settings.topleft_active],
                        'top': [self.buttons['top_button'].button_rect.collidepoint(mouse_pos),
                                self.settings.top_who, self.settings.top_active],
                        'topright': [self.buttons['topright_button'].button_rect.collidepoint(mouse_pos),
                                     self.settings.topright_who, self.settings.topright_active],
                        'left': [self.buttons['left_button'].button_rect.collidepoint(mouse_pos),
                                 self.settings.left_who, self.settings.left_active],
                        'center': [self.buttons['center_button'].button_rect.collidepoint(mouse_pos),
                                   self.settings.center_who, self.settings.center_active],
                        'right': [self.buttons['right_button'].button_rect.collidepoint(mouse_pos),
                                  self.settings.right_who, self.settings.right_active],
                        'bottomleft': [self.buttons['bottomleft_button'].button_rect.collidepoint(mouse_pos),
                                       self.settings.bottomright_who, self.settings.bottomright_active],
                        'bottom': [self.buttons['bottom_button'].button_rect.collidepoint(mouse_pos),
                                   self.settings.bottom_who, self.settings.bottom_active],
                        'bottomright': [self.buttons['bottomright_button'].button_rect.collidepoint(mouse_pos),
                                        self.settings.bottomleft_who, self.settings.bottomleft_active]}
        for i in stats_button:
            if stats_button[i][0] and stats_button[i][2]:
                print(stats_button[i][0], stats_button[i][1], stats_button[i][2])
                stats_button[i][1] = self.who
                self.whose_move()
                stats_button[i][2] = False
                print(stats_button[i][0], stats_button[i][1], stats_button[i][2])
                print(self.settings.bottomright_who, self.settings.bottomright_active)'''

'''def check_mouse_events(self, mouse_pos):
        topleft_clicked = self.buttons['topleft_button'].button_rect.collidepoint(mouse_pos)
        top_clicked = self.buttons['top_button'].button_rect.collidepoint(mouse_pos)
        topright_clicked = self.buttons['topright_button'].button_rect.collidepoint(mouse_pos)
        left_clicked = self.buttons['left_button'].button_rect.collidepoint(mouse_pos)
        center_clicked = self.buttons['center_button'].button_rect.collidepoint(mouse_pos)
        right_clicked = self.buttons['right_button'].button_rect.collidepoint(mouse_pos)
        bottomleft_clicked = self.buttons['bottomleft_button'].button_rect.collidepoint(mouse_pos)
        bottom_clicked = self.buttons['bottom_button'].button_rect.collidepoint(mouse_pos)
        bottomright_clicked = self.buttons['bottomright_button'].button_rect.collidepoint(mouse_pos)

        # Topleft button
        if topleft_clicked and self.settings.topleft_active:
            self.settings.topleft_who = self.who
            self.whose_move()
            self.settings.topleft_active = False

        # Center button
        if center_clicked and self.settings.center_active:
            self.settings.center_who = self.who
            self.whose_move()
            self.settings.center_active = False

        # Topright button
        if topright_clicked and self.settings.topright_active:
            self.settings.topright_who = self.who
            self.whose_move()
            self.settings.topright_active = False

        # Top button
        if top_clicked and self.settings.top_active:
            self.settings.top_who = self.who
            self.whose_move()
            self.settings.top_active = False

        # Left button
        if left_clicked and self.settings.left_active:
            self.settings.left_who = self.who
            self.whose_move()
            self.settings.left_active = False

        # Bottomleft button
        if bottomleft_clicked and self.settings.bottomleft_active:
            self.settings.bottomleft_who = self.who
            self.whose_move()
            self.settings.bottomleft_active = False

        # Bottom button
        if bottom_clicked and self.settings.bottom_active:
            self.settings.bottom_who = self.who
            self.whose_move()
            self.settings.bottom_active = False

        # Bottomright button
        if bottomright_clicked and self.settings.bottomright_active:
            self.settings.bottomright_who = self.who
            self.whose_move()
            self.settings.bottomright_active = False

        # Right button
        if right_clicked and self.settings.right_active:
            self.settings.right_who = self.who
            self.whose_move()
            self.settings.right_active = False'''


'''def buttons_update(self):
    # Topleft button
    if not self.settings.topleft_active:
        if self.settings.topleft_who == self.zero:
            self.screen.blit(self.zero.image, self.buttons['topleft_button'].button_rect)
        else:
            self.screen.blit(self.cross.image, self.buttons['topleft_button'].button_rect)

    # Top button
    if not self.settings.top_active:
        if self.settings.top_who == self.zero:
            self.screen.blit(self.zero.image, self.buttons['top_button'].button_rect)
        else:
            self.screen.blit(self.cross.image, self.buttons['top_button'].button_rect)

    # Topright button
    if not self.settings.topright_active:
        if self.settings.topright_who == self.zero:
            self.screen.blit(self.zero.image, self.buttons['topright_button'].button_rect)
        else:
            self.screen.blit(self.cross.image, self.buttons['topright_button'].button_rect)

    # Left button
    if not self.settings.left_active:
        if self.settings.left_who == self.zero:
            self.screen.blit(self.zero.image, self.buttons['left_button'].button_rect)
        else:
            self.screen.blit(self.cross.image, self.buttons['left_button'].button_rect)

    # Center button
    if not self.settings.center_active:
        if self.settings.center_who == self.zero:
            self.screen.blit(self.zero.image, self.buttons['center_button'].button_rect)
        else:
            self.screen.blit(self.cross.image, self.buttons['center_button'].button_rect)

    # Right button
    if not self.settings.right_active:
        if self.settings.right_who == self.zero:
            self.screen.blit(self.zero.image, self.buttons['right_button'].button_rect)
        else:
            self.screen.blit(self.cross.image, self.buttons['right_button'].button_rect)

    # Bottomleft button
    if not self.settings.bottomleft_active:
        if self.settings.bottomleft_who == self.zero:
            self.screen.blit(self.zero.image, self.buttons['bottomleft_button'].button_rect)
        else:
            self.screen.blit(self.cross.image, self.buttons['bottomleft_button'].button_rect)

    # Bottom button
    if not self.settings.bottom_active:
        if self.settings.bottom_who == self.zero:
            self.screen.blit(self.zero.image, self.buttons['bottom_button'].button_rect)
        else:
            self.screen.blit(self.cross.image, self.buttons['bottom_button'].button_rect)

    # Bottomright button
    if not self.settings.bottomright_active:
        if self.settings.bottomright_who == self.zero:
            self.screen.blit(self.zero.image, self.buttons['bottomright_button'].button_rect)
        else:
            self.screen.blit(self.cross.image, self.buttons['bottomright_button'].button_rect)'''
