import matplotlib.pyplot as plt
import random
G=6.67*(10**(-11))
v=50000
dt=800
n=2800


def updaters(n,posx,posy,velx,vely,m):
    a_x=[0]*n
    a_y=[0]*n
    x_new=[0]*n
    y_new=[0]*n
    vx_new=[0]*n
    vy_new=[0]*n
    
    for i in range(n):
        a_x[i]=0
        a_y[i]=0
        x_new[i]=0
        y_new[i]=0
        vx_new[i]=0
        vy_new[i]=0
        
        for j in range(n):
            if j!=i:
                a_x[i]+=((G*m[j])/(((((posx[i]-posx[j])**2))+(((posy[i]-posy[j])**2)))**1))*((posx[j]-posx[i])/(((((posx[i]-posx[j])**2))+(((posy[i]-posy[j])**2)))**0.5))
                a_y[i]+=((G*m[j])/(((((posx[i]-posx[j])**2))+(((posy[i]-posy[j])**2)))**1))*((posy[j]-posy[i])/(((((posx[i]-posx[j])**2))+(((posy[i]-posy[j])**2)))**0.5))
        x_new[i]=posx[i]+(a_x[i]*dt*dt)+(velx[i]*dt)
        y_new[i]=posy[i]+(a_y[i]*dt*dt)+(vely[i]*dt)
        vx_new[i]=velx[i]+(a_x[i]*dt)
        vy_new[i]=vely[i]+(a_y[i]*dt)
        new_pos=[x_new,y_new,vx_new,vy_new]
    return new_pos

px=[0]*n
py=[0]*n
vx=[0]*n
vy=[0]*n
m=[0]*n

px[0]=20*10000000000
py[0]=175*10000000000
mrb=5*1000000
m[0]=mrb*(10**29)
vx[0]=3000000
vy[0]=0

for i in range(1,n//2):
    pxr=random.randint(-50,90)
    pyr=random.randint(105,245)
    if (pxr > 0 and pxr <40) and (pyr > 160 and pyr <190):
        pxr+=((-1)**random.randint(1,2))*random.randint(40,60)  
        pyr+=((-1)**random.randint(1,2))*random.randint(40,60)
    
        
    for j in range(i):
        if pyr==py[j]/10000000000:
            pyr+=(random.randint(7,9)*0.1)
    for j in range(i):
        if pxr==px[j]/10000000000:
            pxr+=(random.randint(7,9)*0.1)
            
    
    #vxr=random.randint(-50,50)
    #vyr=random.randint(-50,50)
    mr=random.randint(50,55)
    px[i]=pxr*10000000000
    py[i]=pyr*10000000000
    
    r=((((((200000000000-px[i])**2))+(((1750000000000-py[i])**2)))**0.25))
    
    xv=(1750000000000-py[i])/(r**2)
    yv=(px[i]-200000000000)/(r**2)
    
    m[i]=mr*(10**29)

    vx[i]=((((G*m[i])**0.5)/r)*xv*r/3000)+3000000
    print(vx[i])
    
    vy[i]=(((G*m[i])**0.5)/r)*yv*r/3000







px[(n//2)]=380*10000000000
py[(n//2)]=225*10000000000
mrb=5*1000000
m[(n//2)]=mrb*(10**29)
vx[(n//2)]=-3000000
vy[(n//2)]=0



for i in range((n//2)+1,n):
    pxr=random.randint(310,450)
    pyr=random.randint(155,295)
    if (pxr > 365 and pxr <395) and (pyr > 210 and pyr <240):
        pxr+=((-1)**random.randint(1,2))*random.randint(40,60)  
        pyr+=((-1)**random.randint(1,2))*random.randint(40,60)
    
        
    for j in range(i):
        if pyr==py[j]/10000000000:
            pyr+=(random.randint(7,9)*0.1)
    for j in range(i):
        if pxr==px[j]/10000000000:
            pxr+=(random.randint(7,9)*0.1)
            
    
    #vxr=random.randint(-50,50)
    #vyr=random.randint(-50,50)
    mr=random.randint(50,55)
    px[i]=pxr*10000000000
    py[i]=pyr*10000000000
    
    r=((((((3800000000000-px[i])**2))+(((2250000000000-py[i])**2)))**0.25))
    
    xv=(2250000000000-py[i])/(r**2)
    yv=(px[i]-3800000000000)/(r**2)
    
    m[i]=mr*(10**29)

    vx[i]=((((G*m[i])**0.5)/r)*xv*r/3000)-3000000
    print(vx[i])
    
    vy[i]=(((G*m[i])**0.5)/r)*yv*r/3000    
    
    




                
            
for i in range(50000):

    if i%2==0:
        plt.axis([0,400,0,400])
        for j in range(n):
            if(j==0):
                plt.scatter(px[j]/10000000000,py[j]/10000000000,s=110,color='black')
            elif j<n//2:
                plt.scatter(px[j]/10000000000,py[j]/10000000000,s=0.25,color='red')
            elif j==n//2:
                plt.scatter(px[j]/10000000000,py[j]/10000000000,s=110,color='black')
            else:
                plt.scatter(px[j]/10000000000,py[j]/10000000000,s=0.25,color='blue')
                
            
            
        #plt.scatter(px[1]/10000000000,py[1]/10000000000,s=1,color='blue')
        #plt.scatter(px[2]/10000000000,py[2]/10000000000,s=1,color='green')
        plt.savefig("D:\\Physics\\Simulation\\Gravity_model\\collision_of_galaxies\\test1\\galaxy_"+str(i//2)+".png")
        plt.clf()
    #print(p1)
    print(px[0]/10000000000,py[0]/10000000000,px[1]/10000000000,py[1]/10000000000,px[2]/10000000000,py[2]/10000000000,i)    
    pv=updaters(n,px,py,vx,vy,m)
    px=pv[0]
    py=pv[1]
    
    vx=pv[2]
    vy=pv[3]

   
   
   
    
    
 
    x=0
    
    
 
