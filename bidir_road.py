#left:vehicles entering from left side, right:vehicles entering from right side
import numpy as np
import random
import time
space=10   #road length for 10 cars
roadlefttoright=space*[0]  #list of size space for right heading vehicles 
roadrighttoleft=space*[0]  #list of size space for left heading vehicles
sproad=space*[0]           #list of size space for special lane
#roadrighttoleft[2]=2

#injecting vehicles at one end of a road, moving cars along the road if ind=stay. If
#ind=switch, divert cars to special lane
def injcars(list,ind):
    list[1:10]=list[0:9]
    x=random.randint(0,2)
    if ind=='switch':
        list[0]=0
        return x 
    elif ind=='stay':
        list[0]=x
        return 'stay' 

#injecting vehicles onto the special lane
def injsp(list,input,left_or_right):
    list[1:10]=list[0:9]
    if input=='stay':
        list[0]=0
    else:
        list[0]=input
    if left_or_right=='left' or left_or_right=='right':
        return left_or_right 
    else:
        return 'clr_run'

#shifts vehicles on special lane
def movesp(list):
    list[1:10]=list[0:9]
    list[0]=0

#tracks the number of vehicles and computes the score 
def tracker(roadl,roadr):
    L_l=0 #num of long vehicles on left
    N_l=0 #num of cars on left
    L_r=0 #num of long vehicles on right
    N_r=0 #num of cars on right
   
    for i in roadl:
        if i==2:   
            L_l+=1
        if i==1:
            N_l+=1
            
    for i in roadr:
        if i==2:
            L_r+=1 
        if i==1:
            N_r+=1
    
    print "Long vehicle(left)="+str(L_l)+" cars(left)="+str(N_l)+" Long vehicle(right)="+str(L_r)+" cars(right)="+str(N_r)
    num_vehicles=np.matrix([[L_l,L_r],[N_l,N_r]])
    #takes difference between both sides and finds sum of weighted (2:long vehicles, 1:cars) difference
    return np.dot(np.dot(num_vehicles,np.matrix([1 ,-1]).transpose()).transpose(),np.matrix([[2],[1]])) 
  

def main():
    spstat='clr_run'
    #tracker(roadlefttoright,roadrighttoleft[::-1])
    #time.sleep(500) 
    for i in range(60):
        tr=tracker(roadlefttoright,roadrighttoleft[::-1])
        print 'net difference positive left side has priority, net difference negative right has priority'
        print 'net difference: '+str(tr)
        
        if tr<0: #right has priority
            if spstat=='clr_run':
                injcars(roadlefttoright,'stay')
                spstat=injsp(sproad,injcars(roadrighttoleft,'switch'),'right')	
                
            elif spstat=='left':
                injcars(roadlefttoright,'stay')
                movesp(sproad)
                injcars(roadrighttoleft,'stay')
                
            elif spstat=='right':
                injcars(roadlefttoright,'stay')
                injsp(sproad,injcars(roadrighttoleft,'switch'),'right')
        
        elif tr>0:  #left has priority
            if spstat=='clr_run':
                injcars(roadrighttoleft,'stay')
                spstat=injsp(sproad,injcars(roadlefttoright,'switch'),'left')
                
            elif spstat=='left':
                injcars(roadrighttoleft,'stay')
                injsp(sproad,injcars(roadlefttoright,'switch'),'left')
                
            elif spstat=='right':
                injcars(roadlefttoright,'stay')
                movesp(sproad)
                injcars(roadrighttoleft,'stay')
        else:
            injcars(roadlefttoright,'stay')
            injcars(roadrighttoleft,'stay')
            if spstat=='left' or spstat=='right':
                 movesp(sproad)
                    
        print roadlefttoright
        if spstat=='right':   #current status :vehicles are travelling right to left
            print sproad[::-1]
            
        elif spstat=='left':  #current status :vehicles are travelling left to right
            print sproad
            
        else:                 #no vehicles on special lane
            print sproad
        
        print roadrighttoleft[::-1]
        print 'current status:' +spstat    
        print "__________"
        time.sleep(0.01)
        if sproad[:]==space*[0]:
            spstat='clr_run'
            print '###sp clear### '

if __name__=="__main__":
    main()
