# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 07:31:17 2016

@author: tanmay
"""

 # Binary Batch Distillation Column
	#! Component 1 = methanol
	#! Component 2 = ethanol
	n = 40  #stages
	x0 = 0.59 # initial composition
	
	! Constants for heat of vaporization
	A_m = 3.2615e7
	B_m = -1.0407
	C_m = 1.8695
	D_m = -0.60801
	A_e = 6.5831e7
	B_e = 1.1905
	C_e = -1.7666
	D_e = 1.0012
	
	! Critical temperatures
	Tc_m = 512.5 # kelvin
	Tc_e = 514 
	
	! Density coefficients
	rho_m_1 = 2.3267
	rho_m_2 = 0.27073
	rho_m_3 = 512.05
	rho_m_4 = 0.24713
	rho_e_1 = 1.6288
	rho_e_2 = 0.27469
	rho_e_3 = 514
	rho_e_4 = 0.23178
	
	! Heat capacity coefficients
	cp_m_liq_1 = 2.5604E5
	cp_m_liq_2 = -2.7414E3
	cp_m_liq_3 = 1.4777E1
	cp_m_liq_4 = -3.5078E-2
	cp_m_liq_5 = 3.2719E-5
	cp_e_liq_1 = 1.0264E5
	cp_e_liq_2 = -1.3963E2
	cp_e_liq_3 = -3.0341E-2
	cp_e_liq_4 = 2.0386E-3
	cp_e_liq_5 = 0
	
	! Standard heats of formation
	h_form_std_m = -2.391E8 !j/kmol
	h_form_std_e = -2.7698E8 !j/kmol
	
	! Vapor pressure coefficients
	vpm[1] = 82.718
	vpm[2] = -6904.5
	vpm[3] = -8.8622
	vpm[4] = 7.4664E-06
	vpm[5] = 2
	vpe[1] = 73.304
	vpe[2] = -7122.3
	vpe[3] = -7.1424
	vpe[4] = 2.8853E-06
	vpe[5] = 2
	End Constants
	
	Parameters
	rr = 3.5 # reflux ratio
	hf = 0.8 # fractional heat loss fraction
	vf = 0.45 # tray efficiency
	tray_hol = 0.07 #tray holdup
	condenser_hol = 0.144 # condenser holdup
	heat_rate = 36000 , > 0 ! 36000 J/min = 600 W
	gamma = 1.0 #activity coefficient
	End Parameters
	
	Variables
	x[1:n] = x0 , >= 0 , <= 1
	y[2:n] = x0 , >= 0 , <= 1
	L[1:n-1] = 0.36 , > 0 # mol/min
	V[2:n] = 0.72 , > 0 #mol/min
	D = 0.36 , > 0 #mol/min
	boil_hol = 28 , >0 #mol
	Q_cond = 0
	np = 0 , >= 0 # mol
	xp = 0.99 , >= 0 , <= 1
	T[1:n] = 320 #tray temperature
	ystar[2:n] = x0 # theoretical vapor composition
	End Variables
	
	Intermediates
	! tray pressures
	P[1] = 101325 * 0.86 # local atmospheric pressure
	P[2:n] = P[1:n-1] + 101325/760 # pressure drop
	
	! pure component and mixture vapor pressure (Pa)
	vp1[1:n] = exp(vpm[1]+vpm[2]/T[1:n]+vpm[3]*LOG(T[1:n])+vpm[4]*(T[1:n]^vpm[5]))
	vp2[1:n] = exp(vpe[1]+vpe[2]/T[1:n]+vpe[3]*LOG(T[1:n])+vpe[4]*(T[1:n]^vpe[5]))
	vp[1:n] = x[1:n] * vp1[1:n] + (1-x[1:n]) * vp2[1:n]
	
	! pure component and mixutre density (kmol/m3 or mol/L)
	rho_meth[1:n-1] = rho_m_1 / (rho_m_2^(1+(1-T[1:n-1]/rho_m_3)^rho_m_4))
	rho_etha[1:n-1] = rho_e_1 / (rho_e_2^(1+(1-T[1:n-1]/rho_e_3)^rho_e_4))
	rho_mix[1:n-1] = rho_meth[1:n-1] * x[1:n-1] + rho_etha[1:n-1] * (1-x[1:n-1])
	
	! pure component heat of vaporization (J/mol)
	Hvap_m[1:n] = A_m*(1-T[1:n]/Tc_m)^(B_m+C_m*(T[1:n]/Tc_m)+D_m*(T[1:n]/Tc_m)^2)/1000
	Hvap_e[1:n] = A_e*(1-T[1:n]/Tc_e)^(B_e+C_e*(T[1:n]/Tc_e)+D_e*(T[1:n]/Tc_e)^2)/1000
	
	! pure component liquid enthalpies (J/mol)
	h_liq_m[1:n] = (cp_m_liq_1 * (T[1:n]) + cp_m_liq_2 * (T[1:n])^2/2 + &
	cp_m_liq_3 * (T[1:n])^3/3 + cp_m_liq_4 * (T[1:n])^4/4 + &
	cp_m_liq_5 * (T[1:n])^5/5)/1000
	h_liq_e[1:n] = (cp_e_liq_1 * (T[1:n]) + cp_e_liq_2 * (T[1:n])^2/2 + &
	cp_e_liq_3 * (T[1:n])^3/3 + cp_e_liq_4 * (T[1:n])^4/4 + &
	cp_e_liq_5 * (T[1:n])^5/5)/1000
	
	! pure component vapor enthalpies (J/mol)
	h_gas_m[2:n] = h_liq_m[2:n] + Hvap_m[2:n]
	h_gas_e[1:n] = h_liq_e[1:n] + Hvap_e[1:n]
	
	! tray vapor and liquid enthalpies (J/mol)
	h_gas[2:n] = y[2:n] * h_gas_m[2:n] + (1-y[2:n])*h_gas_e[2:n]
	h_liq[1:n] = x[1:n] * h_liq_m[1:n] + (1-x[1:n])*h_liq_e[1:n]
	End Intermediates
	
	#Equations
	# tray bubble point temperature
	P[1:n] = vp[1:n]
	
	# vapor liquid equilibrium
	ystar[2:n] * P[2:n] = x[2:n] * vp1[2:n]
	
	# non-ideal separation with tray efficiency
	y[n] = ystar[n]
	y[2:n-1] = y[3:n]-vf*(y[3:n]-ystar[2:n-1])
	
	#reflux ratio = L/D
	L[1] = rr * D
	
	# Condenser mole balance (methanol)
	condenser_hol * $x[1] = - (L[1]+D) * x[1] + V[2] * y[2]
	
	# Tray mole balance (methanol)
	tray_hol * $x[2:n-1] = L[1:n-2] * x[1:n-2] &
	- (L[2:n-1]) * x[2:n-1] &
	- V[2:n-1] * y[2:n-1] &
	+ y[3:n] * V[3:n]
	
	# Reboiler mole balance (methanol)
	boil_hol * $x[n] + $boil_hol * x[n] = L[n-1] * x[n-1] &
	- V[n] * y[n]
	
	#Overall condenser mole balance
	V[2] = D * (rr+1)
	
	# Overall tray mole balance
	0 = V[3:n] + L[1:n-2] - V[2:n-1] - L[2:n-1]
	
	# Energy balance (no dynamics)
	0 = (V[2]* (h_gas[2] - h_liq[1]) - Q_cond)
	0 = V[3:n] * (h_gas[3:n] - h_liq[2:n-1]) &
	- V[2:n-1] * (h_gas[2:n-1] - h_liq[2:n-1]) &
	- L[1:n-2] * (h_liq[1:n-2] - h_liq[2:n-1])
	0 = heat_rate * hf - V[n] * (h_gas[n]-h_liq[n]) &
	- L[n-1] * (h_liq[n-1]-h_liq[n])
	
	# Production rate equations
	$boil_hol = -D
	$np = D
	xp*$np + np*$xp = x[1] * D
	End Equation