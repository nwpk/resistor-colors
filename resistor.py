# My first working python program (v2)
# Converts Resistor Ohmic Values to Color Codes
# start coded in May 11, 2020
# pushed to github May 24, 2020
# by AJ Casugod


import math as m
import csv
from itertools import zip_longest
from tabulate import tabulate


file = open('resistor_input.csv', newline='')
reader = csv.reader(file)

header = next(reader)  # The firstline is the header

# Parse the contents of resistor_input.csv
r_value = []
r_t_value = []
r_tolerance = []
for column in reader:
    try:
        rsst = column[0]
        r_t_value.append(rsst)
        ohm_val = rsst.lower().replace('ohm', '').replace(' ','')
        r_value.append(ohm_val)
        Tol = column[1]
        indx = Tol.index('%')
        r_tolerance.append(str(Tol[:indx]).strip())
    except IndexError:
        pass


# Identify true ohmic values then store to resistor_numeric_value
# Identify the significant digits
digitcode = {
    'kilo'  :   3   ,
    'mega'  :   6   ,
    'r'     :   0   ,
    'k'     :   3   ,
    'm'     :   6   }
significant = []
resistor_numeric_value = []
for i in r_value:
    try:
        x = float(i)
        resistor_numeric_value.append(x)
    except ValueError:
        done = False
        for key, value in digitcode.items():
            if key in i and done == False:
                x = i.replace(key,'.')
                if x[-1] == '.':
                    x = x.rstrip(x[-1])
                x = float(x) * (10**value)
                resistor_numeric_value.append(x)
                done = True
    y = str(x).replace('0', '').replace('.', '')
    if len(y) == 1:
        y += '0'
    significant.append(y)

# Identify band colors for the significant digits
color_significant_digits = {
    0   :     'black'     ,
    1   :     'brown'     ,
    2   :     'red'       ,
    3   :     'orange'    ,
    4   :     'yellow'    ,
    5   :     'green'     ,
    6   :     'blue'      ,
    7   :     'violet'    ,
    8   :     'grey'      ,
    9   :     'white'     }
significant1 = []
significant2 = []
significant3 = []
for i in significant:
    significant1.append(color_significant_digits.get(int(i[0])))
    significant2.append(color_significant_digits.get(int(i[1])))
    try:
        significant3.append(color_significant_digits.get(int(i[2])))
    except IndexError:
        significant3.append('')

# Identify band color for the multiplier
color_multiplier = {
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
    9   :     'white'    }
multiplier = []
for sig, val in zip(significant, resistor_numeric_value):
    x = m.log10(val/int(sig))
    multiplier.append(color_multiplier.get(x))

# Identify band color for the tolerance
color_tolerance = {
    10      :   'silver'    ,
    5       :   'gold'      ,
    1       :   'brown'     ,
    2       :   'red'       ,
    0.5     :   'green'     ,
    0.25    :   'blue'      ,
    0.1     :   'violet'    ,
    20      :   'none'      }
tolerance = []
for i in r_tolerance:
    tolerance.append(color_tolerance.get(float(i)))




# Output everything to a CSV file
d = [r_value, r_tolerance,
     significant1, significant2, significant3, multiplier, tolerance]
export_data = zip_longest(*d, fillvalue='')
with open('resistor color codes.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.writer(myfile, delimiter=' ',
                    quoting=csv.QUOTE_NONE, escapechar=' ')
    wr.writerow(('r_value', 'r_tolerance', 'color1',
                 'color2', 'color3', 'color4', 'tolerance'))
    wr.writerows(export_data)
myfile.close()


# Output everything as table to the terminal
table_header = ['r_t_value', 'r_tolerance', 'color1',
                'color2', 'color3', 'color4', 'tolerance']
table = []
for cell in zip_longest(r_t_value, r_tolerance, significant1, significant2, significant3, multiplier, tolerance):
    table.append(cell)
print(
    tabulate(
        table,
        headers = table_header,
        tablefmt = "simple",
        stralign = 'left',
        numalign = 'center'
    )
)
