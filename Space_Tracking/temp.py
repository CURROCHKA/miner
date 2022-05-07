map_ = [['.'] * 10 for i in range(10)]

for i in map_:
    print(i)

    '''if (self.map[pos_x][pos_y] == self.map[0][0] and
        self.map[pos_x + 1][pos_y] == '.' and self.map[pos_x][pos_y + 1] == '.' and self.map[pos_x + 1][
            pos_y + 1] == '.') or \
            (self.map[pos_x][pos_y] == self.map[-1][0] and
             self.map[pos_x + 1][pos_y] == '.' and self.map[pos_x][pos_y - 1] == '.' and self.map[pos_x + 1][
                 pos_y - 1] == '.') or \
            (self.map[pos_x][pos_y] == self.map[-1][0] and
             self.map[pos_x - 1][pos_y] == '.' and self.map[pos_x][pos_y + 1] == '.' and self.map[pos_x - 1][
                 pos_y + 1] == '.') or \
            (self.map[pos_x][pos_y] == self.map[-1][-1] and
             self.map[pos_x - 1][pos_y] == '.' and self.map[pos_x][pos_y - 1] == '.' and self.map[pos_x - 1][
                 pos_y - 1] == '.'):
        return True
    elif (self.map[pos_x][pos_y] == self.map[0][pos_y] and
          self.map[pos_x + 1][pos_y] == '.' and self.map[pos_x][pos_y - 1] == '.' and self.map[pos_x + 1][
              pos_y - 1] == '.' and
          self.map[pos_x][pos_y + 1] == '.' and self.map[pos_x + 1][pos_y + 1] == '.') or \
            (self.map[pos_x][pos_y] == self.map[pos_x][0] and
             self.map[pos_x - 1][pos_y] == '.' and self.map[pos_x][pos_y + 1] == '.' and self.map[pos_x - 1][
                 pos_y + 1] == '.' and
             self.map[pos_x + 1][pos_y] == '.' and self.map[pos_x + 1][pos_y + 1]):
        return True'''