# My first working python program
# Converts Resistor Ohmic Values to Color Codes
    # coded in May 11, 2020
    # by AJ Casugod

import csv
from itertools import zip_longest

file = open(r'C:\Users\User\Desktop\resistor2color_converter\resistor_input.csv', newline='')
reader = csv.reader(file)

header = next(reader) #The firstline is the header

# Parse the contents of resistor_input.csv
data = []
for column in reader:
    try:
        ohm_val = column[0].lower().replace('ohm','').strip()
        Tol = column[1]
        tol = Tol[:3].replace('%','').replace('=','').strip()
        data.append([ohm_val, tol])
    except IndexError:
        pass

# Assign colors given the tolerances
tol_color = {
    10      :   'silver'    ,
    5       :   'gold'      ,
    1       :   'brown'     ,
    2       :   'red'       ,
    0.5     :   'green'     ,
    0.25    :   'blue'      ,
    0.1     :   'violet'    ,
    20      :   'none'      ,
}
Tolerance = []
for i in data:
    x = float(i[1])
    for key, value in tol_color.items():
        if key == x:
            Tolerance.append(value)
        else:
            pass


# Identify true ohmic values then store to Ohmic_Value
# Identify the significant digits
Ohmic_Value = []
significant = []
digitcode = {
    'kilo'  :   3   ,
    'mega'  :   6   ,
    'r'     :   0   ,
    'k'     :   3   ,
    'm'     :   6   ,
}


def replace(x, key):
    if '.' not in x:
        x = x.replace(key, '.')
    else:
        x = x.replace(key, '')
    return x


for i in data:
    x = str(i[0])
    for key, value in digitcode.items():
        if 'mega' in x:
            x = replace(x, key)
            x = x.strip('mega')
            x = float(x.replace(' ', ''))
            x *= 10**6
        elif key in x:
            x = replace(x, key)
        else:
            value = 0
    x = float(x.replace(' ', ''))
    x *= 10**value
    Ohmic_Value.append(x)
    significant.append(str(x).replace('.', '').replace('0', ''))


# Find the band colors for the significant digits
colorcode = {
    0   :     'black'     ,
    1   :     'brown'     ,
    2   :     'red'       ,
    3   :     'orange'    ,
    4   :     'yellow'    ,
    5   :     'green'     ,
    6   :     'blue'      ,
    7   :     'violet'    ,
    8   :     'grey'      ,
    9   :     'white'     ,
}
Value1 = []
Value2 = []
for i in Ohmic_Value:
    v = str(i)
    for key, value in colorcode.items():
        if str(key) == v[0]:
            Value1.append(value)
    try:
        for key, value in colorcode.items():
            if str(key) == v[1]:
                Value2.append(value)
    except IndexError:
        Value2.append('black')
            


# Find the multiplier for the ohmic value
# Identify colors for the significant digits
multiplier = {
    -2  :     'silver'   ,
    -1  :     'gold'     ,
    0   :     'black'    ,
    1   :     'brown'    ,
    2   :     'red'      ,
    3   :     'orange'   ,
    4   :     'yellow'   ,
    5   :     'green'    ,
    6   :     'blue'     ,
    7   :     'violet'   ,
    8   :     'grey'     ,
    9   :     'white'
}
Value3 = []
Value4 = []

def check_multiplier(a,b):
    """ Iterate through the multiplier dictionary to find a match """
    a = float(a)
    b = float(b)
    count = 0
    j = 0
    if a > b:
        while a > b:
            a = a / 10
            count -= 1
    elif a < b:
        while a < b:
            a = a * 10
            count += 1
    for key, value in multiplier.items():
        if key == count:
            j = value
    return j

for a, b in zip(significant, Ohmic_Value):
    x = str(a)
    if len(x) == 1:
        Value3.append(check_multiplier(a, b))
        Value4.append('')
    elif len(x) == 2:
        Value3.append(check_multiplier(a, b))
        Value4.append('')
    elif len(x) == 3:
        for key, value in colorcode.items():
            if str(key) == x[2]:
                Value3.append(value)
        Value4.append(check_multiplier(a, b))

# Output everything to a CSV file
d = [data, Value1, Value2, Value3, Value4, Tolerance]
export_data = zip_longest(*d, fillvalue='')
with open('resistor color codes.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.writer(myfile, delimiter=' ', quoting = csv.QUOTE_NONE, escapechar = ' ')
    wr.writerow(('Ohmic Value', '1st Significant Digit', '2nd Significant Digit', '3rd Significant Digit', 'Multiplier', 'Tolerance'))
    wr.writerows(export_data)
myfile.close()

from tabulate import tabulate
table_header = ['Ohmic_Value','significant', 'color1', 'color2', 'color3', 'color4','tolerance']
table =[]
for cell in zip(Ohmic_Value, significant, Value1, Value2, Value3, Value4, Tolerance):
    table.append(cell)

print(tabulate(table, headers = table_header, tablefmt = "grid"))

print(
    len(Ohmic_Value),
    len(Value1),
    len(Value2),
    len(Value3),
    len(Value4),
    len(Tolerance)  
)
