'''
Created on 2016/6/15

@author: Gan
'''
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
activition = 0
p = 0
class Muscle_Tendon:
	"""
	Muscle_Tendon model built with Hill model
	alpha_coordi: start coodination of musle
	end_coordi: the end coodination of musle
	l_m: musle length
	l_t: tendon length
	flag:1 means support musle,0 means unsupport 
	a_R:the parameters of musle activition model
	MT_length: musle_tendon length
	theta: pennation angle,set as constant
	"""
	
	def __init__(self,alpha_coordi,end_coordi,activition = 0,l_m = 0.15,l_t =0.13,flag = 1):
		self.MT_length = 0.31
		self.theta = 0.087
		self.l_m = l_m
		self.l_t = l_t
		self.a_R = [0.01,0.01]
		self.max_force = [390,650]
		self.alpha_coordi = alpha_coordi
		self.end_coordi = end_coordi
		self.activition = activition
		self.flag = flag
		self.force = 0
		self.Calculate_MTlength()
		
	def calculate_activition(self,EMG,R,A):
		iir_b,iir_a = signal.iirfilter(2, Wn=0.2, rp=5, rs=60, btype='lowpass', ftype='ellip')
		U_t = signal.lfilter(iir_b,iir_a, np.abs(EMG))
		U_t[U_t<0] = 0
		self.activition = (np.exp(A*R*U_t)-1)/(np.exp(-2.5)-1)
		
		
	def Calculate_MTlength(self):
		_R = np.array([ [np.cos(p),-np.sin(p),    0,   0],
						[np.sin(p), np.cos(p),    0,   0],
						[	     0,	        0,	  1,   0],
						[		 0,	        0, 	  0,   1] ])
		p_0 = self.alpha_coordi
		p_e	= self.end_coordi
		P_i = np.dot(_R,p_e)
		l_mt = P_i - p_0
		if self.flag == 0:
			self.MT_length = 0.29 + 0.06*p
		else:
			self.MT_length = np.sqrt(sum([i*i for i in l_mt]))

	def force_Estimition(self,activition):
		self.Calculate_MTlength()
		#self.calculate_activition(EMG,self.a_R[self.flag],-2.5)
		l = np.sqrt((self.l_m * np.sin(self.theta))**2+(self.MT_length - self.l_t)**2)
		l_normal = l / self.l_m
		funA_l = 0.9866*np.exp(-((l_normal-1.073)/0.2952)**2) + 0.6533*np.exp(-((l_normal-0.7201)/0.1759)**2)
		funP_l = 0.000065*np.exp(6.47*l_normal)
		self.force = (funA_l * activition + funP_l)*self.max_force[self.flag]*np.cos(self.theta)
	
'''
#plot musle length

Biceps = Muscle_Tendon(np.array([0.031,0.29,0,1]),np.array([0.027,-0.03,0, 1]),flag = 1)
Biceps1 = Muscle_Tendon(np.array([0.031,0.32,0,1]),np.array([0.027,-0.03,0, 1]),flag = 0)
p1 = np.arange(0,1.7453,0.02)
Biceps_length = []
Biceps_length1 = []
for angle in p1:
	p = angle
	Biceps.Calculate_MTlength()
	Biceps1.Calculate_MTlength()
	Biceps_length.append(Biceps.MT_length)
	Biceps_length1.append(Biceps1.MT_length)
	

plt.plot(p1/np.pi*180, np.array(Biceps_length),label="$Biceps musle-tendon length$")
plt.plot(p1/np.pi*180,np.array(Biceps_length1),label="$Ticeps musle-tendon length$")
plt.legend()
plt.xlabel("Angle(Rad)")
plt.ylabel("length(m)")
plt.show()
'''



#plot musle force

Biceps = Muscle_Tendon(np.array([0.031,0.30,0,1]),np.array([0.027,-0.03,0, 1]))
activition = np.arange(0.2,0.9,0.06)
p1 = np.arange(0,1.7453,0.06)
Biceps_force = []
X = []
Y = []
for acti in activition:
	for angle in p1:
		p = angle
		Biceps.force_Estimition(acti)
		X.append(angle*180/np.pi)
		Y.append(acti)
		Biceps_force.append(Biceps.force)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(X,Y,Biceps_force)
plt.show()

	
