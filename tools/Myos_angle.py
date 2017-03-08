from myo import init, Hub, Feed, StreamEmg
import time
import numpy as np

	
def GetDegreeFromACC(ACCs):
	R = 0
	angle=[]
	ACC_angle = []
	for ACC in ACCs:
		R = 0
		for data in ACC:
			R += data**2
		R = np.sqrt(R)
		ACC_angle = []
		for data in ACC:
			ACC_angle.append(np.arccos(data/R)*180/np.pi)
		ACC_angle[2] = np.sign(ACC_angle[2])*(abs(ACC_angle[2])-abs(90-abs(ACC_angle[1])))
		angle.append(ACC_angle*np.sign([-ACC[1],-ACC[1],-ACC[0]]))
	return angle

def angle_init(myo,angle,which_myo):
	index =0
	for _one_myo in which_myo:
		angle[index]= GetDegreeFromACC([myo[_one_myo].acceleration])[0][2]
		index +=1
	return angle
	
def updataAngle(myo,angle,which_myo,T):
	index = 0
	GRY_3D=[(data**2) for data in myo[which_myo].gyroscope]
	main_index = np.argmax([abs(data) for data in myo[which_myo].gyroscope])
	w_sign = np.sign(myo[which_myo].gyroscope[1])
	w_combine=np.sqrt(sum(GRY_3D))	
	angle = angle+ w_combine*w_sign*0.02*T*180/np.pi	
	return angle
			
	#for data in GYO:
	
def show_output(data, t1, t2, T, r):

	t2=time.time()
	if t2 - t1 < T: 
		with open(r, "a") as text_file:
			text_file.write("{}\n".format(data))
	else:  		
		exit()
	return t2

def get_angle(myo,angle, t_start, t_s ,t1 ,t2, T, which_use):
	flag = [] 
	if len(which_use)==2:
		Angle_ACC= GetDegreeFromACC([myo[which_use[0]].acceleration,myo[which_use[1]].acceleration])
	if len(which_use)==1:
		Angle_ACC= GetDegreeFromACC([myo[which_use[0]].acceleration])
	t_s = time.time()
	if len(which_use)==1:
		angle[0] = updataAngle(myo,angle[0],which_use[0],t_s-t_start)
	else:
		for n in range(2):
			angle[n] = updataAngle(myo,angle[n],which_use[n],t_s-t_start)
	t_start = time.time()
	index = 0
	for _one_myo in which_use:
		flag.append(sum([abs(data) for data in myo[_one_myo].gyroscope]))
		if flag[index] >= 120:
			Angle_ACC[index][2] = 0.8*angle[index] + 0.2*Angle_ACC[index][2]
		if flag[index]<=50:
			angle[index] = Angle_ACC[index][2]
		if flag[index]>50 and flag[index]<120: 
			Angle_ACC[index][2] = 0.5*angle[index] + 0.5*Angle_ACC[index][2]
		
	if len(which_use)==1:
		data1 = (Angle_ACC[0][2],myo[which_use[0]].acceleration[1]) 
		t2 = show_output(data1,t1, t2, T,'Angle&w.txt')
		print("Continue,angle={:.2f} ,w={:.2f} ## {:.2f} seconds left" .format(data1[0],data1[1],T-t2+t1))
	else:
		data2 = (Angle_ACC[0][2], myo[which_use[0]].acceleration[1], Angle_ACC[1][2], myo[which_use[1]].acceleration[1])
		t2 = show_output(data2,t1, t2, T,'Angle&w.txt')
		print("Continue,angle1={:.2f} ,w1={:.2f} # angle2={:.2f} ,w2={:.2f} # {:.2f} seconds left".format(data2[0],data2[1],data2[2],data2[3],T-t2+t1))
	return t_start
