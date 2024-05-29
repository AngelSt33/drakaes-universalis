# for every file inside the gfx/flags folder

import os

flags_directory = os.getcwd() + '/../gfx/flags/'
new_countries_directory = os.getcwd() + '/../common/countries/'
countries_tag_file = os.getcwd() + '/../common/country_tags/00_countries.txt'


new_country_file_content = """
# %s
graphical_culture = westerngfx

color = {      }
revolutionary_colors = {    }

historical_idea_groups = {
offensive_ideas
defensive_ideas
trade_ideas
administrative_ideas
spy_ideas
economic_ideas
innovativeness_ideas
diplomatic_ideas
quality_ideas
religious_ideas
maritime_ideas
}

army_names = {
}

fleet_names = {
}

leader_names = {
}

monarch_names = {
}

ship_names = {
}
"""

def fill_countries_flags():
    flags = os.listdir(flags_directory)
    flags = [flag for flag in flags if flag.endswith('.tga') and " " in flag]

    for flag in flags:
        country_tag = flag.split(' ')[0]
        country_name = flag.split(' ')[1].split('.')[0]

        # create new country file -> country_name.txt
        with open(new_countries_directory + ('%s.txt' % country_name), 'w', encoding='utf-8') as output:
            output.write(new_country_file_content % country_name)
        
        # add country to country_tags file
        with open(countries_tag_file, 'a', encoding='utf-8') as output:
            if output.read()[-1] != '\n':
                output.write('\n')
            output.write('%s = "countries/%s.txt"\n' % (country_tag, country_name))


fill_countries_flags()