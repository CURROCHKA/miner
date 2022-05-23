map = [[0] * 10 for i in range(10)]
for i in range(10):
    for j in range(10):
        if [i, j] in planets_coord:
            map[i][j] = 'planet'

for i in map:
    print(i)