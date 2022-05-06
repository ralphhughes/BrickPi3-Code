from datetime import datetime
from configparser import ConfigParser
config = ConfigParser()

# Reading from config

config.read('config.ini')
print("Reading last saved values:")
print(config.get('main', 'time_last_run')) # -> "value1"
print(config.get('main', 'key2')) # -> "value2"
print(config.get('main', 'key3')) # -> "value3"

# getfloat() raises an exception if the value is not a float
#a_float = config.getfloat('main', 'a_float')

# getint() and getboolean() also do this for their respective types
#an_int = config.getint('main', 'an_int')
input("press enter to save new values")
###########
config.read('config.ini')
if not config.has_section('main'):
    config.add_section('main')
now = datetime.now()
dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
config.set('main', 'time_last_run', dt_string)
config.set('main', 'key2', 'value2')
config.set('main', 'key3', 'value3')

with open('config.ini', 'w') as f:
    config.write(f)

print("Finished saving values. Quitting.")
##############

