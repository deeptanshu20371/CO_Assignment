#input
import os
import sys
lines = os.read(0, 10**6).strip().splitlines() 
i=0;
size=len(lines)
instruction=[];
for x in range(len(lines)):
    line = lines[x].decode('utf-8') 
    l=line.split();
    instruction.append(l)

#Giving labels to binary values
#Appends binary values of the label to instruction list
#['loop:','add', 'R1', 'R1', 'R2'] => ['loop:','add', 'R1', 'R1', 'R2','00000000']
no_of_variables=0
for i in instruction:
    if(i[0]=='var'):
        no_of_variables+=1;
for i in range(len(instruction)):
    if(instruction[i][0][-1]==':'):
        binary_of_label=bin(i-no_of_variables).replace('0b','')
        x = binary_of_label[::-1] 
        while len(x) < 8:
            x += '0'
        binary_of_label = x[::-1]
        instruction[i].append(binary_of_label)

#Giving variables binary values
#['var', 'x'] => ['var', 'x', '00000000']
for i in range(len(instruction)):
    if(instruction[i][0]=='var'):
        binary_of_var=bin(len(instruction)-no_of_variables+i).replace('0b','')
        x = binary_of_var[::-1] 
        while len(x) < 8:
            x += '0'
        binary_of_var = x[::-1]
        instruction[i].append(binary_of_var)

#Dictionary for Op code
Dict = {'add':'00000',
        'sub':'00001',
        'ld':'00100',
        'st':'00101',
        'mul':'00110',
        'div':'00111',
        'rs':'01000',
        'ls':'01001',
        'xor':'01010',
        'or':'01011',
        'and':'01100',
        'not':'01101',
        'cmp':'01110',
        'jmp':'01111',
        'jlt':'10000',
        'jgt':'10001',
        'je':'10010',
        'hlt':'10011'}

#Dictionary for register adress
Reg_Address={
        'R0':'000',
        'R1':'001',
        'R2':'010',
        'R3':'011',
        'R4':'100',
        'R5':'101',
        'R6':'110',
        'FLAGS':'111'}

#=========================Error_Handling=========================

#Typos in instruction name
for i in instruction:
    if(i[0]=='var'):
        continue
    opcodeindex=0
    if(i[opcodeindex][-1]==':'):
        opcodeindex=1
    if(i[opcodeindex]=='add' or i[opcodeindex]=='sub' or i[opcodeindex]=='mov' or i[opcodeindex]=='ld' or i[opcodeindex]=='st' or i[opcodeindex]=='mul' or i[opcodeindex]=='div' or i[opcodeindex]=='rs' or i[opcodeindex]=='ls' or i[opcodeindex]=='xor' or i[opcodeindex]=='or' or i[opcodeindex]=='and' or i[opcodeindex]=='not' or i[opcodeindex]=='cmp' or i[opcodeindex]=='jmp' or i[opcodeindex]=='jlt' or i[opcodeindex]=='jgt' or i[opcodeindex]=='je' or i[opcodeindex]=='hlt' ):
        continue
    else:
        print(i[opcodeindex]+" is not a valid instruction name.")
        sys.exit()

#=========================Error_Handling=========================

#Driver code
for i in instruction:
    opcodeindex=0;
    if(i[opcodeindex][-1]==':'):
            opcodeindex=1;

    #TypeA
    if(i[opcodeindex]=="add" or i[opcodeindex]=="sub" or i[opcodeindex]=="mul" or i[opcodeindex]=="xor" or i[opcodeindex]=="or" or i[opcodeindex]=="and"):
    	for k in Dict:
    		if i[opcodeindex]==k:
    			print(Dict[k],end='')
    			break
    	print("00",end='')
    	for reg in Reg_Address:
    		if (reg==i[opcodeindex+1]):
    			print(Reg_Address[reg],end='')
    			break
    	for reg in Reg_Address:
    		if (reg==i[opcodeindex+2]):
    			print(Reg_Address[reg],end='')
    			break
    	for reg in Reg_Address:
    		if (reg==i[opcodeindex+3]):
    			print(Reg_Address[reg])
    			break

    #TypeB 
    elif(i[opcodeindex]=="rs" or i[opcodeindex]=="ls" or (i[opcodeindex]=="mov" and i[opcodeindex+2][0]=="$")):
        if (i[opcodeindex]=="mov"):
        	print("00010",end='')
        else:
        	for k in Dict:
        		if i[opcodeindex]==k:
        			print(Dict[k],end='')
        			break
        for reg in Reg_Address:
        	if (reg==i[opcodeindex+1]):
        		print(Reg_Address[reg],end='')
        		break
        imm=i[opcodeindex+2][1:]
        imm=bin(int(imm)).replace("0b","")
        z_add=8-len(imm)
        imm=("0"*z_add)+imm
        print(imm)

    #TypeE
    elif(i[opcodeindex]=='jgt' or i[opcodeindex]=='jmp' or i[opcodeindex]=='jlt' or   i[opcodeindex]=='je'):
        for k in Dict:
            if i[opcodeindex]==k:
                print(Dict[k],end='')
                break
        for j in instruction:
            if j[0][0:len(j[0])-1]==i[opcodeindex+1]:
                print('000'+j[-1])
                break

    #TypeF
    elif(i[opcodeindex]=='hlt'):
        for k in Dict:
            if i[opcodeindex]==k:
                print(Dict[k],end='')
                break
        print('00000000000')

