fuel = '100'
try:
    int(fuel)
except ValueError:
    print('str')
else:
    print('int')