import matplotlib.pyplot as plt

m1=3.285*(10**30)
#m1=3.285*(10**23)
#m2=1.989*(10**30)
m2=3.285*(10**30)
m3=3.285*(10**30)
g=6.67*(10**(-11))


v=((g*m2)/(200000000000-100000000000))**0.5
print(v)


c=g*m1*m2*m3
dt=1000

def updaters(pos1,pos2,pos3,vel1,vel2,vel3):
    r12=(((pos1[0]-pos2[0])**2)+((pos1[1]-pos2[1])**2))**0.5
    r13=(((pos1[0]-pos3[0])**2)+((pos1[1]-pos3[1])**2))**0.5
    r23=(((pos2[0]-pos3[0])**2)+((pos2[1]-pos3[1])**2))**0.5
    #print(r)
    a_x_1= ((c/(m1*m3*r12*r12))*(pos2[0]-pos1[0])/r12)  +((c/(m1*m2*r13*r13))*(pos3[0]-pos1[0])/r13)
    a_y_1= ((c/(m1*m3*r12*r12))*(pos2[1]-pos1[1])/r12)  +((c/(m1*m2*r13*r13))*(pos3[1]-pos1[1])/r13)
    
    x_1_new=pos1[0]+(a_x_1*dt*dt)+(vel1[0]*dt)
    y_1_new=pos1[1]+(a_y_1*dt*dt)+(vel1[1]*dt)
    
    v_x_1=vel1[0]+(a_x_1*dt)
    v_y_1=vel1[1]+(a_y_1*dt)

    a_x_2= ((c/(m2*m3*r12*r12))*(pos1[0]-pos2[0])/r12)  +((c/(m2*m1*r23*r23))*(pos3[0]-pos2[0])/r23)
    a_y_2= ((c/(m2*m3*r12*r12))*(pos1[1]-pos2[1])/r12)  +((c/(m2*m1*r23*r23))*(pos3[1]-pos2[1])/r23)
    
    x_2_new=pos2[0]+(a_x_2*dt*dt)+(vel2[0]*dt)
    y_2_new=pos2[1]+(a_y_2*dt*dt)+(vel2[1]*dt)
    
    v_x_2=vel2[0]+(a_x_2*dt)
    v_y_2=vel2[1]+(a_y_2*dt)



    a_x_3= ((c/(m3*m2*r13*r13))*(pos1[0]-pos3[0])/r13)  +((c/(m3*m1*r23*r23))*(pos2[0]-pos3[0])/r23)
    a_y_3= ((c/(m3*m2*r13*r13))*(pos1[1]-pos3[1])/r13)  +((c/(m3*m1*r23*r23))*(pos2[1]-pos3[1])/r23)
    
    x_3_new=pos3[0]+(a_x_3*dt*dt)+(vel3[0]*dt)
    y_3_new=pos3[1]+(a_y_3*dt*dt)+(vel3[1]*dt)
    
    v_x_3=vel3[0]+(a_x_3*dt)
    v_y_3=vel3[1]+(a_y_3*dt)

    
    pos1=[x_1_new,y_1_new,x_2_new,y_2_new,x_3_new,y_3_new,v_x_1,v_y_1,v_x_2,v_y_2,v_x_3,v_y_3]
    return pos1







p1=[450000000000,400000000000]
p2=[350000000000,400000000000]
p3=[400000000000,300000000000]
v1=[0,v/2]
v2=[0,-0.7*v/2]
v3=[0.7*v/2,0]

for i in range(50000):
    #print(p1)
    pv=updaters(p1,p2,p3,v1,v2,v3)
    p1=[pv[0],pv[1]]
    p2=[pv[2],pv[3]]
    p3=[pv[4],pv[5]]
    v1=[pv[6],pv[7]]
    v2=[pv[8],pv[9]]
    v3=[pv[10],pv[11]]
    print(p1[0]/10000000000,p1[1]/10000000000,p2[0]/10000000000,p2[1]/10000000000,p3[0]/10000000000,p3[1]/10000000000,i)
    
        

    x=0
    
    if i%20==0:
        plt.axis([0,75,0,75])
        plt.scatter(p2[0]/10000000000,p2[1]/10000000000,s=100,color='red')
        plt.scatter(p1[0]/10000000000,p1[1]/10000000000,s=100,color='blue')
        plt.scatter(p3[0]/10000000000,p3[1]/10000000000,s=100,color='green')
        plt.savefig("C:\\Users\\Manasa\\Desktop\\plots3\\scattered6\\threebodies_"+str(i//20)+".png")
        plt.clf()
  
        
    


