import os

csv_file = '/map/definition.csv'

base_file_format = """
#%s

add_core = JVK
owner = JVK
controller = JVK
culture = Jorv
religion = hussite
hre = no
base_tax = 5 
base_production = 5
trade_goods = grain
base_manpower = 3
capital = "Jorvick"
is_city = yes
discovered_by = eastern
discovered_by = western
discovered_by = muslim
discovered_by = ottoman

"""

output_directory = os.getcwd() + '/history/provinces/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(os.getcwd() + csv_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            line = line.strip().split(';')
            province_name = line[4]
            if province_name != 'x':
                province_id = line[0]
                with open(output_directory + ('%s-%s.txt' % (province_id, province_name.replace('/', '-'))), 'w', encoding='utf-8') as output:
                    output.write(base_file_format % province_name)
        except UnicodeDecodeError:
            print(line)