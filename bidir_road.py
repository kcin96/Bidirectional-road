import numpy as np
import random
import time
space=10   #road length for 10 cars
roadtoleft=space*[0]
roadtoright=space*[0]
sproad=space*[0]
roadtoright[2]=2
def injcars(list,ind):
    list[1:10]=list[0:9]
    
    x=random.randint(0,2)
#    print "<<"+str(x)+">>"
    if ind=='switch':
	list[0]=0
	return x 
    elif ind=='stay':
	list[0]=x
    	return 'stay' 

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

def injcarss(list):
    list[1:10]=list[0:9]
    list[0]=0

def tracker(roadl,roadr):
    L_l=0
    N_l=0
    L_r=0
    N_r=0
   
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
    return np.sum(np.multiply(np.dot(num_vehicles,np.matrix([1 ,-1]).transpose()),np.matrix([[2],[1]])))

#injsp(sproad,3,'right')
#print sproad

spstat='clr_run'
#tracker(roadtoleft,roadtoright[::-1])
#time.sleep(500) 
for i in range(60):
    tr=tracker(roadtoleft,roadtoright[::-1])
    print 'd:'+str(tr)
    if tr<0: #right has priority
	if spstat=='clr_run':
	    injcars(roadtoleft,'stay')
	    spstat=injsp(sproad,injcars(roadtoright,'switch'),'right')	
	    print spstat,spstat,spstat
	elif spstat=='left':
	    injcars(roadtoleft,'stay')
	    injcarss(sproad)
	    injcars(roadtoright,'stay')
	elif spstat=='right':
	    injcars(roadtoleft,'stay')
	    injsp(sproad,injcars(roadtoright,'switch'),'right')
    elif tr>0:  #left has priority
	if spstat=='clr_run':
	    injcars(roadtoright,'stay')
	    spstat=injsp(sproad,injcars(roadtoleft,'switch'),'left')	
	    print spstat,spstat,spstat
	elif spstat=='left':
	    injcars(roadtoright,'stay')
	    injsp(sproad,injcars(roadtoleft,'switch'),'left')
	elif spstat=='right':
            injcars(roadtoleft,'stay')
	    injcarss(sproad)
	    injcars(roadtoright,'stay')
    else:
	injcars(roadtoleft,'stay')
	injcars(roadtoright,'stay')
	if spstat=='left':
	     injcarss(sproad)
	elif spstat=='right':
	     injcarss(sproad)
    
    print roadtoleft
    if spstat=='right':
        print sproad[::-1]
    elif spstat=='left':
	print sproad
    else:
	print sproad
    print roadtoright[::-1]
    print spstat    

    print "__________"
    time.sleep(0.01)
    if sproad[:]==space*[0]:
	spstat='clr_run'
	print '###sp clear### '
   

