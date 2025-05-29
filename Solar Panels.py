import numpy as np
import matplotlib.pyplot as plt
import math




#####################################################           PANEL                #####################################

#Size of the solar panel




while True:
    height_panel_string  = input("What height do you want the panel to be in metres?")
    try:
        height_panel = eval(height_panel_string)
    except:
        print( " Not a valid number " )
        continue
    if height_panel <= -1:
        print( "Must be positive" )
    else:
        break



while True:
    width_panel_string = input("What width do you want the panel to be in metres?")
    try:
        width_panel = eval(width_panel_string)
    except:
        print( " Not a valid number " )
        continue
    if width_panel <= -1:
        print( "Must be positive" )
    else:
        break



#Altiude of panel - 45
while True:
    alt_panel_string = input( "At what angle do you want the panel to be (in degrees)?" ) #altitude of the normal of the panel
    try:
        altp = eval(alt_panel_string)
    except:
        print( " Not a valid number " )
        continue
    if altp <= -1:
        print( "angle must be between 0 to 90 degrees" )
    elif altp >= 91:
        print( "angle must be between 0 to 90 degrees" )
    else:
        break

alt_panel = math.radians(altp)


#Azimuth of panel - 0
while True:
    az_panel_string = input( "Enter the azimuth of the solar panel in degrees" ) #It is measured from the south to the normal of the soalr panel
    try:
        azp = eval(az_panel_string)
    except:
        print( " Not a valid number " )
        continue
    if azp <= -1:
        print( "Azimuth must be between 0 to 360 degrees" )
    elif azp >= 361:
        print( "Azimuth must be between 0 to 360 degrees" )
    else:
        break

az_panel = math.radians(azp) 



#Latitude of the solar panel - 53.0034
while True:
    lat_panel_string = input("What Latidude? -90 is South Pole and 90 is North Pole")
    try:
        latp = eval(lat_panel_string)
    except:
        print( " Not Valid degree " )
        continue
    if latp <= -91:
        print( "Latitude must be between -90 to 90 degrees" )
    elif latp >= 91:
        print( "Latitude must be between -90 to 90 degrees" )
    else:
        break

lat_panel = math.radians(latp)


#Longitude of the solar panel - -2.2733
while True:
    long_panel_string = input("Longitude? -180 is West and 180 is East")
    try:
        longp = eval(long_panel_string)
    except:
        print( " Not Valid degree " )
        continue
    if longp <= -181:
        print( "Longitude must be between -180 to 180 degrees" )
    elif longp >= 181:
        print( "Longitude must be between -180 to 180 degrees" )
    else:
        break

long_panel = math.radians(longp)




################################################          SUN         ##############################################

#Day
while True:
    day_string = input( "Enter the day of the year. Jan 1 = 1, Dec 31 =365  " )
    try:
        d = eval(day_string)
    except:
        print( " Not Valid  numbers " )
        continue
    if d <0:
        print( "Day must be in the range: 1-365" )
    elif d >= 366:
        print( "Day must be in the range: 1-365" )
    else:
        break
    
#d = 100 April 10th


def Power(h,d,long_panel,lat_panel):
    
    #Declination of the sun
    decl_sun = math.radians(23.45) *  math.sin(    math.radians(    (360/365)*(d+284)   )   )
    
    #Found on NOAA, check refrences
    gamma = math.radians( (360/365)*( (d -1) +  ( (h-12)/24 )  ) )
    eqtime = 229.18*(0.000075 + (0.001868*np.cos(gamma))-(0.032077*np.sin(gamma))-(0.014615*np.cos(2*gamma))-(0.040849*np.sin(2*gamma)))
    timezone = long_panel/15
    time_offset = eqtime + (4*long_panel) - (60*timezone)
    tst = h*60 + time_offset # tst = true solar time
    
    hour_angle =math.radians( (tst / 4) - 180 )
    if hour_angle < 0:
        return 0
    

    alt_sun = math.asin(  ( (np.sin(decl_sun))*(np.sin(lat_panel)) ) +  ( (np.cos(decl_sun))*(np.cos(lat_panel))*(np.cos(hour_angle)) )  )
    if alt_sun <0:
        return 0
    
    az_sun = math.acos( -((  ( np.sin(decl_sun) )-(( np.sin(alt_sun) )*(  np.sin(lat_panel)  ))   )/(  (np.cos(alt_sun))*(np.cos(lat_panel))  )) )


    theta = math.acos( (( np.sin(alt_sun)  )*( np.sin(alt_panel)  )*(  np.cos( az_sun - az_panel )  )) + (( np.cos(alt_sun) )*( np.cos(alt_panel)  )) )
    # P=I.A
    Intensity = 1361*math.exp( -0.25/( (0.5*math.pi)-(alt_sun) ) )
    Area_panel = height_panel*width_panel   
    power = Intensity*Area_panel*np.cos(theta)*0.2  #o.2 bc only 20% of the energy from the sun is converted into electrical energy
    if power < 0:
        return 0
    return power

########################################### Energy #################################################################

def trapz (x,y):
    area = []
    
    for i in range(len(x)-1):
        trap_chunk = ((y[i] + y[i+1]) / 2) * (x[i+1] - x[i])
        area.append(trap_chunk)
        total_area= sum(area)
    return total_area


#################################################        power for a day       ##############################################
print("DAY")

#for plotting energy calculated throughout the day
hours_list=[]
power_day_list=[]


#when the suns out
for i in range(0,24,1):
    h = i
    p = Power(h,d,long_panel,lat_panel)
    power_day_list.append(p)



hours_in_day=list(range(0, len(power_day_list) ,1))


plt.plot(hours_in_day,power_day_list,color='c')
plt.xlabel("Hours of the day")
plt.ylabel("Power/(W)")
plt.title("Graph of Power generated by the soalr panel throughout the day")
plt.show()




Energy = trapz(hours_in_day,power_day_list)/1000
print( "Total Energy generated in a day",'{:0.2f}'.format(Energy),"kWh" )


    
############################################## Altitude  ############################################
print("ALTITUDE")

az_panel = math.radians(0) 



asteps = 9
dsteps= (90-0.0)/asteps

hours_list=[]
power_day_list=[]

for i in range(0,asteps+1,1):
    hours_list=[]
    power_day_list=[]
  
    th=i*dsteps
    alt_panel = math.radians(th)
     
    for h in range(0,24,1):
        p = Power(h,d,long_panel,lat_panel)
        power_day_list.append(p)

    hours_list = list(range(0, len(power_day_list) ,1))
    Energy = trapz(hours_list,power_day_list)/1000
    print( '{:0.2f}'.format(Energy),"kWh","Energy was generated when altitude was",th,"degrees" )
     
    plt.plot(hours_list,power_day_list)
    

plt.xlabel("Hours of the Day")
plt.ylabel("Power generated per hour(W)")
plt.title("Graph of power generated in a day as the angle of the panel to the ground was changing")
plt.show()




############################################## Azimuth  ############################################
print("AZIMUTH")

alt_panel = math.radians(45)


asteps = 9 #number of lines 
dsteps= (360-0.0)/asteps

hours_list=[]
power_day_list=[]


for i in range(0,asteps+1,1):
    hours_list=[]
    power_day_list=[]
  
    th=i*dsteps
    az_panel = math.radians(th)
     
    for h in range(0,24,1):
        p = Power(h,d,long_panel,lat_panel)
        power_day_list.append(p)

    hours_list = list(range(0, len(power_day_list) ,1))
    Energy = trapz(hours_list,power_day_list)/1000
    print( '{:0.2f}'.format(Energy),"kWh","Energy was generated when azimuth was",th,"degrees" )
    
    plt.plot(hours_list,power_day_list)


plt.xlabel("Hours of the Day")
plt.ylabel("Power generated per hour(W)")
plt.title("Graph of power generated in a day as the aziumth was changing")
plt.show()



############################################# power for all the days of the year ######################################################
print("YEAR")

alt_panel = math.radians(45)
az_panel = math.radians(0)


power_month_list=[]

total_power=[]

for d in range(1,366,1):
    power_day_list=[]
    
    for h in range(0,24,1):
        p = Power(h,d,long_panel,lat_panel)
        power_day_list.append(p)
        total_power.append(sum(power_day_list))
        
    power_month_list.append(sum(power_day_list)/len(power_day_list))
    

else:
    print("Error in loop ")
        

print("Printing...")


limit=list(range(1, len(power_month_list)+1 ,1))


plt.bar(limit,power_month_list,0.7,color='limegreen',align='edge')

plt.xlabel("Days of the year")
plt.ylabel("Average power generated in a day(W)")
plt.title("Graph of power generated by the soalr panel in a year")
plt.show()

###### Verification ########
print("Verifying...")


Energy = trapz(limit,power_month_list)/1000
print( "Total Energy generated in a year by 1 Solar panel",'{:0.2f}'.format(Energy),"kWh" )

###########################################   Colours #################################################

#for i in range(12):
#    plt.plot([0, 1], [i, i])

#plt.show()
