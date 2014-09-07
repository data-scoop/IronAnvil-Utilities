# Search NFL Birthdays
# search-birthdays.py

# This is a simple search utility that runs in IDLE or Windows Command Processor.
# It takes advantage of the "nfldb" datastore to provide an easy way to return a
# list of NFL players from the criteria of Birthday and/or Team. 

# This program requires: Python 2.7.8 and PostgreSQL

# It also requires / utilizes two modules which are not
# included in the Python27 distribution:

# Required -----------------------------------
# nfldb 1.2.7 (included in nflgame)
# PyPI: https://pypi.python.org/pypi/nflgame
# GitHub: https://github.com/BurntSushi/nflgame
# pip install nflgame

# Utilized ----------------------------------
# colorama 0.3.2
# PyPI: https://pypi.python.org/pypi/colorama
# GitHub: https://github.com/tartley/colorama
# pip install colorama


import datetime, nfldb, os, re, sys
os.system('cls' if os.name == 'nt' else 'clear')

# This application uses the 'colorama' module
# Get Colorama using "pip install colorama"

# If you do not wish to use Colorama, you can
# comment-out the code below, then un-comment
# the class declaration just below it to run.

# Colorama code begins here ---------->
from colorama import init
init()
from colorama import Fore, Back, Style
print Fore.GREEN + Style.BRIGHT
# Colorama code ends here ------------^

"""
class Fore:
    GREEN = ''
    RED = ''
    WHITE = ''
    YELLOW = ''
"""



teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAC', 'KC', 'MIA', 'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'OAK', 'PHI', 'PIT', 'SD', 'SEA', 'SF', 'STL', 'TB', 'TEN', 'WAS']
afc_east = 'BUF, MIA, NE, NYJ'
afc_north = 'BAL, CIN, CLE, PIT'
afc_south = 'HOU, IND, JAC, TEN'
afc_west = 'DEN, KC, OAK, SD'
nfc_east = 'DAL, NYG, PHI, WAS'
nfc_north = 'CHI, DET, GB, MIN'
nfc_south = 'ATL, CAR, NO, TB'
nfc_west = 'AZ, SF, SEA, STL'
afc = '\n\t' + afc_east + ', ' + afc_north + ', ' + afc_south + ', ' + afc_west
nfc = '\n\t' + nfc_east + ', ' + nfc_north + ', ' + nfc_south + ', ' + nfc_west
nfl = afc+nfc


def validate(date_text):
    try:
        date_text == '' or datetime.datetime.strptime(date_text, '%m/%d')
    except ValueError:
        print Fore.RED + "\n\tError: Format the date as MM/DD, or leave it blank to use today's date.\n" + Fore.GREEN
        date_text = validate(raw_input('\tDate:'))
    return date_text

def valiteam(team_text):
    try:
        assert (team_text == '') or (team_text in teams)
    except AssertionError:
        print Fore.RED + "\n\tError: Use one of these team abbreviations:" + Fore.GREEN, nfl, "\n"
        team_text = valiteam(raw_input('\tTeam: ').upper())
    return team_text
        


# Specify Date and or Team
print '\n Find player birthdays by Date and/or Team'
print '\n\tDate format: ' + Fore.YELLOW + '(MM/DD):' + Fore.GREEN
print '\n\tTeams: ' + Fore.YELLOW + nfl + Fore.GREEN
print '\n\tOmitting the Date will cause today\'s date to be used in the search'
print '\tOmitting the Team will include all teams in the search\n'

date_text = validate(raw_input(Fore.GREEN + '\tDate: ' + Fore.WHITE))
team_text = valiteam(raw_input(Fore.GREEN + '\tTeam: ' + Fore.WHITE).upper())



db = nfldb.connect()
q = nfldb.Query(db).player(status='Active')

if date_text == '':
    date_text = str(datetime.date.today().month) + '/' + str(datetime.date.today().day)

if team_text != '':
    q = nfldb.Query(db).player(status='Active', team=team_text)

s=0
for p in q.sort([('team','asc'), ('last_name','asc')]).as_players():
    

    if p.last_name != 'Nunley':
        # Parse Height from inches into Feet and Inches
        h = str(p.height/12) + "'" + str(p.height%12) + '"'
        dt = date_text.split('/')
        bd = p.birthdate.split('/')
        if (dt[0] == bd[0]) and (dt[1] == bd[1]):
            s+=1 # On the first iteration, print the Title and Column Headings
            if s<2:
                print Fore.GREEN + '\n\tBirthdays' + Fore.WHITE
                print Fore.GREEN + '\t', 'Height','\t', 'Weight','\t', 'Exp','\t', 'Birthdate','\t','Team','\t', 'Nbr','\t', 'Pos','\t', 'Name' + Fore.WHITE
            print '\t', h, '\t', p.weight, '\t', "("+str(p.years_pro)+")", '\t', p.birthdate, '\t', p.team, '\t', p.uniform_number, '\t', p.position, '\t', p.full_name

print '\n\t', s, Fore.GREEN + 'results' + Fore.WHITE
