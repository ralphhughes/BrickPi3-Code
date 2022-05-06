# Hardcoded location
latitude=0
longitude=0

# Prompt for target azimuth and inclination
strTargetAzimuth = input("Enter compass bearing to target in degrees")

strTargetElevation = input("Enter elevation to target in degrees")

# Prompt for current azimuth
strAzimuth = input("Please enter current azimuth? (leave blank for due north)")
if not strAzimuth:
    numAzimuth = 0
else:
    numAzimuth = float(strAzimuth)

# Home the elevation axis using the limit switch
# (run motor A in -ve encoder direction until touch sensor fires. Stop motor A and reset motor A encoder for zero position)

# Calculate azimuth & inclination of sun right now for the given lat/long

# Bisect the azimuth and inclination angle deltas to work out mirror azimuth and inclination

# Debug: print everything I've been given or calculated
print(f'Azimuth: {numAzimuth}')


#Convert mirror azimuth to motor encoder counts using gear ratio and wheel size

#Instruct motors to move to specified position
