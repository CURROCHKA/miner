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

