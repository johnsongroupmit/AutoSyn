# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 09:54:16 2019

@author: Folia
"""

#READ  SYRINGE FILE FOR DEPTHS AND CLEARANCES
import xlrd
syringe_book =  xlrd.open_workbook('syringe.xlsx')
sheet=syringe_book.sheet_by_index(0)

exp_vial_depth=sheet.cell_value(2,1)
exp_vial_clearance=sheet.cell_value(3,1)
stock_depth=sheet.cell_value(4,1)
wash_and_waste_depth=sheet.cell_value(6,1)
wash_and_waste_clearance=sheet.cell_value(7,1)
conversion_factor=sheet.cell_value(5,1)
volume=sheet.cell_value(1,1)

#READ TEST LOCATIONS
coordinate_book = xlrd.open_workbook('plate_coordinates.xlsx')
sheet=coordinate_book.sheet_by_index(0)
test_location=[]

for x in range(36):
    test_location.append((sheet.cell_value(x,1),sheet.cell_value(x,2)))

#READ WASH PROTOCAL LOCATIONS AND CLEARANCES
wash_location=(sheet.cell_value(37,1),sheet.cell_value(37,2))
waste_location=(sheet.cell_value(38,1),sheet.cell_value(38,2))

#READ PLATE AND MONOMER LOCATIONS

plate1=sheet.cell_value(40,1)
plate2=sheet.cell_value(41,1)
stock_dict={}

for x in range(42,sheet.nrows):
    
    
    if sheet.cell_value(x,1) == '' or sheet.cell_value(x,2) == '':
        continue
    
    stock_dict[sheet.cell_value(x,0)]=(sheet.cell_value(x,1),sheet.cell_value(x,2))

########################################################################
#UNCOMMENT FOR 96 WELL PLATE LOCATION AND COMMENT ABOVE TEST LOCATION
#96 WELL PLATE COORDINATES GENERATE. WORKS FINE.

#x_position=[]
#x=30
#x_start=30
#x_end=128
#x_position.append(x)
#for y in range(11):
#    
#    x+=((x_end-x_start)/11)
#    x_position.append(x)
##print(ran)
#
#y_position=[]
#y=1.5
#y_start=1.5
#y_end=64
#y_position.append(y)
#for x in range(7):
#    y+=((y_end-y_start)/7)
#    y_position.append(y)                
#
#test_location=[]    
#for x in range(7,-1,-1):
#    for y in range(12):
#      test_location.append((x_position[y],y_position[x]))


########################################################################

          
test_book = xlrd.open_workbook('polymer tests.xlsx')
sheet=test_book.sheet_by_index(0)

#GENERATE EXPERIMENT TESTS

biglist=[]
timer=0
for x in range(1,sheet.nrows):
    waittime=0
    be=[]
    for r in range(1,sheet.ncols,2):
        
        if sheet.cell_value(x,r) == '' or sheet.cell_value(x,r+1) == '':
            continue
        if sheet.cell_value(x,r) == 'WAIT' and sheet.cell_value(x,r+1) != '':
            waittime+=sheet.cell_value(x,r+1)
            continue
        
        be.append((sheet.cell_value(x,0),test_location[int((sheet.cell_value(x,0)))-1],sheet.cell_value(x,r),sheet.cell_value(x,r+1),waittime))
    if be != []:
        biglist.append(be)


flat=[i for j in biglist for i in j]

sortbiglist=sorted(flat, key=lambda flat: (flat[4],(flat[2][0],flat[2][1]),(flat[1][0],flat[1][1])))


#AMOUNTS TO E VALUE GCODE         
def conversion(microL):
    amount=(conversion_factor*microL)/volume
    return amount

    
#KEEPS TRACK ON CURRENT AND PREVIOUS POSITION FROM EACH MOVE FUNCTION CALL

lastPoint = {"x": None, "y": None, "z": None, "e":None, "speed":None}
currentPoint= {"x": 0, "y": 0, "z": 0, "e":0, "speed":1000}


def move(x=None, y=None, z=None, e=None, speed=None):            # Generate the move command with optional parameters
    #print "  ## move() ##"
    global currentPoint
    global lastPoint
    s = "G1 "
    if x is not None: 
        s += "X" + str(x) + " "
        lastPoint["x"]=currentPoint["x"]
        currentPoint["x"] = x 
    if y is not None: 
        s += "Y" + str(y) + " "
        lastPoint["y"]=currentPoint["y"]
        currentPoint["y"] = y 
    if z is not None: 
        s += "Z" + str(z) + " "
        lastPoint["z"]=currentPoint["z"]
        currentPoint["z"] = z 
    if e is not None:
        s += "E"+"-" + str(e) + " "
        lastPoint["e"]=currentPoint["e"]
        currentPoint["e"] = e
    if speed is not None:
        s += "F" + str(speed)
        lastPoint["speed"]=currentPoint["speed"]
        currentPoint["speed"] = speed

    #s += "\n"
    return s

# GERNERATE WAIT COMMAND IN MINUTES
def wait(time=None):            
    #print "  ## move() ##"
    
    s = "G4 "
    if time is not None: 
        s += "P" + str(time*60000)

    #s += "\n"
    return s

#CALCULATE TIME
def time(start_coordinate,end_coordinate,acceleration):
        
        distance=(((end_coordinate[0]-start_coordinate[0])**2)+((end_coordinate[1]-start_coordinate[1])**2)+((end_coordinate[2]-start_coordinate[2])**2))**(1/2)
        time=((2*distance)/2000)**(1/2)
        return time 





def block(x,y):
    if 0  <= x <= 25 and 0 <= y <= 200 :
        return move(x=None,y=None,z=45,e=None,speed=1000)
    if 25  <= x <= 175 and 0 <= y <= 200:
        return move(x=None,y=None,z=3,e=None,speed=1000)
    if 175  <= x <= 200 and 0 <= y <= 200:
        return move(x=None,y=None,z=45,e=None,speed=1000)



#EXTRUDE AMOUUNT(ENERGY) INTO VIAL AT Z HEIGHT
def dispense(destination,test,Z,energy,result):

    
    result.append(move(x=destination[test][0],y=destination[test][1],z=None,e=None,speed=2000))
    
    
                    
    result.append(move(x=None,y=None,z=Z,e=None,speed=1000))
    

    
    result.append(move(x=None, y=None, z=None,e=energy,speed=2000))
     
#TIME TAKES TO DISPENSE
def dispense_time(destination,test,Z,energy,result):
 
    times=0
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(destination[test][0],destination[test][1],lastPoint["z"]),2000)
    
                    
  
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(destination[test][0],destination[test][1],Z),2000)        
    
    
        
    times+=time((lastPoint['e'],lastPoint['y'],lastPoint['z']),(energy,destination[test][1],Z),2000)
    return times


#WASH PROTOCOL
def wash(result):
    
    
    result.append(move(x=None,y=None,z=wash_and_waste_clearance,e=None,speed=1000))
    
    
    result.append(move(x=wash_location[0],y=wash_location[1],z=None,e=None,speed=1000))
    
    
    result.append(move(x=None,y=None,z=wash_and_waste_depth,e=None,speed=1000))
    
    
    result.append(move(x=None,y=None,z=None,e=0,speed=500))
    result.append(move(x=None,y=None,z=None,e=conversion_factor,speed=500))
    result.append(wait(1/60))
    
    result.append(move(x=None,y=None,z=wash_and_waste_clearance,e=None,speed=1000))
    
    
    result.append(move(x=waste_location[0],y=waste_location[1],z=None,e=None,speed=1000))
    
    
    result.append(move(x=None,y=None,z=None,e=0,speed=500))
    

#TIME IT TAKES TO WASH
def wash_time(result):
    times=0
    
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(lastPoint['x'],lastPoint['y'],wash_and_waste_clearance),1000)
    
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(wash_location[0],wash_location[1],lastPoint['z']),1000)
    
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(lastPoint['x'],lastPoint['y'],wash_and_waste_depth),1000)
    
    
    times+=time((lastPoint['e'],lastPoint['y'],lastPoint['z']),(0,lastPoint['y'],lastPoint['z']),2000)
    
    times+=time((lastPoint['e'],lastPoint['y'],lastPoint['z']),(conversion_factor,lastPoint['y'],lastPoint['z']),2000)
    
    
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(lastPoint['x'],lastPoint['y'],wash_and_waste_clearance),1000)
    
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(waste_location[0],waste_location[1],lastPoint['z']),1000)
    
    times+=time((lastPoint['e'],lastPoint['y'],lastPoint['z']),(0,lastPoint['y'],lastPoint['z']),1000)
    
    return times

    
    
def refill(source,beak,amount,result): #draw certain amount of liquid from stock solution vial (beaker)
    
    mL=conversion(amount)
    result.append(move(x=None,y=None,z=exp_vial_clearance,e=None,speed=1000))
    
    
    result.append(move(x=source[beak][0],y=source[beak][1],z=None,e=None,speed=1000))
    
    
    result.append(move(x=None,y=None,z=stock_depth,e=None,speed=1000))
  
    
    
    result.append(move(x=None,y=None,z=None,e=mL,speed=500))
    
    result.append(wait(1/60))
    
    result.append(move(x=None,y=None,z=exp_vial_clearance,e=None,speed=1000))
    
    
    result.append(move(x=source[beak][0],y=source[beak][1],z=None,e=None,speed=1000))
    
    
def refill_time(source,beak,amount,result):
    times=0
    mL=conversion(amount)
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(lastPoint['x'],lastPoint['y'],exp_vial_clearance),1000)
    
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(source[beak][0],source[beak][1],lastPoint['z']),1000)
    
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(lastPoint['x'],lastPoint['y'],stock_depth),1000)
    
    
    
    times+=time((lastPoint['e'],lastPoint['y'],lastPoint['z']),(mL,lastPoint['y'],lastPoint['z']),1000)
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(lastPoint['x'],lastPoint['y'],exp_vial_clearance),1000)
    
    
    times+=time((lastPoint['x'],lastPoint['y'],lastPoint['z']),(source[beak][0],source[beak][1],lastPoint['z']),1000)
    return times
    
####################################################################################    

#START GCODE GENERATION
result=[]
result.append('G28')
result.append('G92 E0')
result.append('G90')
 
amount=0 #total mL to dispense whether grouped or individual dispense
track=[] #store group of same monomer in same time stamp
timer=0 
skip=[] #keep track of which instructions to skip because they are grouped together
for index in range(len(sortbiglist)):
    #reset skip once last grouped instruction is reached
    if skip != []:
        if index == skip[-1]:
            skip=[]
            continue
    
        else:
            #skip grouped instructions
            if index in skip:
                continue
    
    
    track.append(sortbiglist[index])
    amount+=sortbiglist[index][3]
    
    #END OF LIST DISPENSE LAST AMOUNT
    if index == len(sortbiglist)-1:
        #draw amount
        result.append('draw ' + str(amount) + ' mL of ' + str(sortbiglist[index][2]))
        refill(stock_dict,sortbiglist[index][2],amount,result)
        
        dispense_convert=conversion(amount)
        for i in track:
            
            dispense_convert-=conversion(i[3])
            #dispense
            result.append('dispense '+ str(i[3]) + ' mL of ' + str(i[2]) + ' into ' + str(test_location[int(i[0]-1)]))
            dispense(test_location,int(i[0]-1),exp_vial_depth,dispense_convert,result)
            
            
            track=[]
            amount=0
            result.append('wash')
            wash(result)
            break
        break
        
        
        
    #SAME MONOMER AND TIME STAMP GROUPED TOGETHER
    #check is next sequential dispense is the same monomer and time stamp
    if (sortbiglist[index+1][2]==sortbiglist[index][2] and sortbiglist[index+1][4]==sortbiglist[index][4]):
        # look at all subsequent instructions and check for group conditions
        # Next line asks for the same compound and the same timestamp
        for jndex in range(index+1,len(sortbiglist)):
            
            if (sortbiglist[jndex][2]==sortbiglist[index][2] and sortbiglist[jndex][4]==sortbiglist[index+1][4]):
                #add instruction to group track and increase total dispense amount
                track.append(sortbiglist[jndex])
                amount+=sortbiglist[jndex][3]
                #note that add instructions do not need to be dispensed again. they are filled.
                skip.append(jndex)
                continue
            #group condition not met
            else:
                break
    
    
    #ADD TOTAL AMOUNT AND DRAW AND DISPENSE WHETHER SINGLE STEP OR GROUP OF STEPS
    #draw total amount
    result.append('draw ' + str(amount) + ' mL of ' + str(sortbiglist[index][2]))
    refill(stock_dict,sortbiglist[index][2],amount,result)
    timer+=refill_time(stock_dict,sortbiglist[index][2],amount,result)
    dispense_convert=conversion(amount)
    for i in track:
        dispense_convert-=conversion(i[3])
        
        if plate1=='VIALS' or plate2 == 'VIALS':
            result.append('dispense '+ str(i[3]) + ' mL of ' + str(i[2]) + ' into ' + str(test_location[int(i[0]-1)]))
            dispense(test_location,int(i[0]-1),exp_vial_depth,dispense_convert,result)
            timer+=dispense_time(test_location,int(i[0]-1),exp_vial_depth,dispense_convert,result)
            
            #RAISE HEIGHT TO GET OUT OF PUNCTURE VIALS
            result.append(move(x=None,y=None,z=exp_vial_clearance,e=None,speed=1000))
            timer+=time((0,0,lastPoint['z']),(0,0,exp_vial_clearance),2000)
            
        else: #WELLS dispense at constant height
            result.append('dispense '+ str(i[3]) + ' mL of ' + str(i[2]) + ' into ' + str(test_location[int(i[0]-1)]))
            dispense(test_location,int(i[0]-1),exp_vial_clearance,dispense_convert,result)
            timer+=dispense_time(test_location,int(i[0]-1),exp_vial_clearance,dispense_convert,result)
    
    result.append('wash')         
    wash(result)
    timer+=wash_time(result)
    
    #after dispense(s) check if next dispense in sequence is in same time stamp
    #NEXT MONOMER IS DIFFERENT TIME STAMP. RECALCULATE WAIT TIME INBETWEEN
    if sortbiglist[index][4]!=sortbiglist[index+1][4]:
        #no point reducing zero wait time
        if sortbiglist[index][4] != 0:
            if timer >= sortbiglist[index][4]:
                final_wait=0
                result.append('wait ' + str(final_wait) + ' from ' + str(sortbiglist[index][4]))
                result.append(wait(final_wait))
                timer=0
            
            #reduce upcoming wait time
            else:
                final_wait=sortbiglist[index][4]-timer
            
                result.append('wait ' + str(final_wait) + ' from ' + str(sortbiglist[index][4]))
                result.append(wait(final_wait))
                timer=0    
    
    #GROUP OF SAME MONOMER AND TIME BUT NEXT DISPENSE IS DIFFERENT TIME STAMP FROM GROUP. RECALCULATE TIME INBETWEEN.
    if track != [] and skip != []:
        
        if track[-1][4]!=sortbiglist[int(skip[-1]+1)][4]:
                
                
                if sortbiglist[index][4] != 0:
                    if timer >= sortbiglist[index][4]:
                        final_wait=0
                        result.append('wait ' + str(final_wait) + ' from ' + str(sortbiglist[index][4]))
                        result.append(wait(final_wait))
                        timer=0
            
            #reduce upcoming wait time
                    else:
                        final_wait=sortbiglist[index][4]-timer
                    
                        result.append('wait ' + str(final_wait) + ' from ' + str(sortbiglist[index][4]))
                        result.append(wait(final_wait))
                        timer=0  
                      
        
    
    #instructions in group are dispensed. reset and look for another group of instructions. also reset amount to 0. all dispenses handled.
    
    track=[]
    amount=0
    
    
    
    
########################################################################
    
#GENERATE COORDINATES FOR SMALL VILAS (NEEDS TWEAKING, COORDS NOT EXACTLY RIGHT)

#x_positions=[]
#x=29
#
#x_start=29
#x_end=133.5666667
#
#x_positions.append(x)
#for y in range(7):
#    
#    x+=((x_end-x_start)/7)
#    x_positions.append(x)
##print(ran)
#
#y_positions=[]
#y=6.166666667
#
#y_start=6.166666667
#
#y_end=64
#y_positions.append(y)
#for x in range(4):
#    y+=((y_end-y_start)/4)
#    y_positions.append(y)
#
#
#test_location=[]    
#for x in range(4,-1,-1):
#    for y in range(8):
#      test_location.append((x_positions[y],y_positions[x]))

#print(result)
#SEND GCODE TO PRINTER

#import serial
#ser = serial.Serial('COM4', 115200)
#out = ser.readline()

#ser.write(b'G28 \n')
#for i in result:
#    solve=i+' \n'
#    ser.write(str.encode(solve)) 
########################################################################


# output txt
import os
with open(os.path.join(os.getcwd(), 'result.txt'), 'w') as f:
    for e in result:
        f.write(e + '\n')
    