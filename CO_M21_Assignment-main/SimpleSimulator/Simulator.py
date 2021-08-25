import os
import matplotlib.pyplot as plt

def binary_converter(num):
    return_val=bin(num).replace('0b','')
    return return_val


def sixteenbit(s):
    x = s[::-1] 
    while len(x) < 16:
        x += '0'
    s = x[::-1]
    return s

#input
lines = os.read(0, 10**6).strip().splitlines() 
i=0;
size=len(lines)
instruction=[];
for x in range(len(lines)):
    line = lines[x].decode('utf-8') 
    instruction.append(line)
for i in range(len(instruction),256):
    instruction.append('0000000000000000')

#register values
RF={ '000':'0000000000000000',
            '001':'0000000000000000',
            '010':'0000000000000000',
            '011':'0000000000000000',
            '100':'0000000000000000',
            '101':'0000000000000000',
            '110':'0000000000000000',
            '111':'0000000000000000',
            }

def MEM_getdata(): 
    return instruction[PC];

def MEM_dump():
    for i in instruction:
        print(i)

def RF_dump():
    for i in RF:
        print(RF[i], end='')
        print(' ',end='')
    print();

def PC_dump():
    binary_of_PC=bin(PC).replace('0b','')
    x = binary_of_PC[::-1] 
    while len(x) < 8:
        x += '0'
    binary_of_PC = x[::-1]
    print(binary_of_PC,end='')
    print(' ',end='')

def execute(current_instruction):
    if (current_instruction[0:5]=='00000'):
        #Addition
        if(int(RF[current_instruction[10:13]],2)+int(RF[current_instruction[13:16]],2))>256:
            RF[current_instruction[7:10]]='0000000000000000'
            RF['111']='0000000000001000'
        else:
            RF[current_instruction[7:10]]=sixteenbit((binary_converter(int(RF[current_instruction[10:13]],2)+int(RF[current_instruction[13:16]],2))))
            RF['111']='0000000000000000'
        return False,PC+1;
    
    elif (current_instruction[0:5]=='00001'):
        #Subtraction
        if(int(RF[current_instruction[13:16]],2)>int(RF[current_instruction[10:13]],2)):
            RF[current_instruction[7:10]]='0000000000000000'
            RF['111']='0000000000001000'
        else:
            RF[current_instruction[7:10]]=sixteenbit((binary_converter(int(RF[current_instruction[10:13]],2)-int(RF[current_instruction[13:16]],2))))
            RF['111']='0000000000000000'
        return False,PC+1;
    
    elif (current_instruction[0:5]=='00010'):
        #Move Immediate
        RF[current_instruction[5:8]]=sixteenbit(current_instruction[8:16])
        RF['111']='0000000000000000'
        return False,PC+1
    
    elif (current_instruction[0:5]=='00011'):
        #Move Register
        RF[current_instruction[10:13]]=RF[current_instruction[13:16]]
        RF['111']='0000000000000000'
        return False,PC+1
    
    elif (current_instruction[0:5]=='00100'):
        #Load
        RF[current_instruction[5:8]]=instruction[int(current_instruction[8:16],2)]
        RF['111']='0000000000000000'
        memadd.append(int(current_instruction[8:16],2));
        cycle.append(cyclevar)
        return False,PC+1
    
    elif (current_instruction[0:5]=='00101'):
        #Store
        instruction[int(current_instruction[8:16],2)]=sixteenbit(RF[current_instruction[5:8]])
        RF['111']='0000000000000000'
        memadd.append(int(current_instruction[8:16],2));
        cycle.append(cyclevar)
        return False,PC+1
    
    elif (current_instruction[0:5]=='00110'):
        #Multiply
        if(int(RF[current_instruction[10:13]],2)*int(RF[current_instruction[13:]],2))>256:
            RF[current_instruction[7:10]]='0000000000000000'
            RF['111']='0000000000001000'
        else:
            RF[current_instruction[7:10]]=sixteenbit((binary_converter(int(RF[current_instruction[10:13]],2)*int(RF[current_instruction[13:]],2))))
            RF['111']='0000000000000000'
        return False,PC+1
    
    elif (current_instruction[0:5]=='00111'):
        #Divide
        a=int(RF[current_instruction[10:13]],2)
        b=int(RF[current_instruction[13:]],2)
        RF['000']=binary_converter(a//b)
        RF['001']=binary_converter(a%b)
        RF['111']='0000000000000000'
        return False,PC+1
    
    elif (current_instruction[0:5]=='01000'):
        #Right Shift
        imm=int(current_instruction[8:],2)
        b=RF[current_instruction[5:8]]
        for i in range(imm):
            b=b[:-1]
            b='1'+b
        RF[current_instruction[5:8]]=b
        RF['111']='0000000000000000'
        return False,PC+1

    elif (current_instruction[0:5]=='01001'):
        #Left Shift
        imm=int(current_instruction[8:],2)
        b=RF[current_instruction[5:8]]
        for i in range(imm):
            b=b[1:]
            b=b+'0'
        RF[current_instruction[5:8]]=b
        RF['111']='0000000000000000'
        return False,PC+1
    
    elif (current_instruction[0:5]=='01010'):
        #Exclusive OR
        reg_first=RF[current_instruction[10:13]]
        reg_second=RF[current_instruction[13:]]
        result=""
        for i in range(8):
            a=reg_first[i]
            b=reg_second[i]
            if (a=='0' and b=='0') or (a=='1' and b=='1'):
                result=result+'0'
            else:
                result=result+'1'
        RF[current_instruction[7:10]]=result
        RF['111']='0000000000000000'
        return False,PC+1

    elif (current_instruction[0:5]=='01011'):
        #Or
        reg_first=RF[current_instruction[10:13]]
        reg_second=RF[current_instruction[13:]]
        result=""
        for i in range(8):
            a=reg_first[i]
            b=reg_second[i]
            if (a=='0' and b=='0'):
                result=result+'0'
            else:
                result=result+'1'
        RF[current_instruction[7:10]]=result
        RF['111']='0000000000000000'
        return False,PC+1

    elif (current_instruction[0:5]=='01100'):
        #And
        reg_first=RF[current_instruction[10:13]]
        reg_second=RF[current_instruction[13:]]
        result=""
        for i in range(8):
            a=reg_first[i]
            b=reg_second[i]
            if (a=='1' and b=='1'):
                result=result+'1'
            else:
                result=result+'0'
        RF[current_instruction[7:10]]=result
        RF['111']='0000000000000000'
        return False,PC+1
    
    elif (current_instruction[0:5]=='01101'):
        #Invert
        for i in len(RF[current_instruction[10:13]]):
            if (RF[current_instruction[10:13][i]]==0):
                (RF[current_instruction[7:10][i]]==1)
            else:
                (RF[current_instruction[7:10][i]]==0)
        RF['111']='0000000000000000'
        return False,PC+1
    
    elif (current_instruction[0:5]=='01110'):
        #Compare
        if (int(RF[current_instruction[10:13]],2) < int(RF[current_instruction[13:16]],2)):
            RF['111']='0000000000000100'
        elif (int(RF[current_instruction[10:13]],2) > int(RF[current_instruction[13:16]],2)):
            RF['111']='0000000000000010'
        else:
            RF['111']='0000000000000001'
        return False,PC+1

    elif (current_instruction[0:5]=='01111'):
        #Unconditional Jump 
        new_PC=int(current_instruction[8:16],2)
        RF['111']='0000000000000000'
        return False,new_PC
    
    elif (current_instruction[0:5]=='10000'):
        #Jump if less than
        if RF['111']=='0000000000000100':
            new_PC=int(current_instruction[8:16],2)
            RF['111']='0000000000000000'
            return False,new_PC
        else:
            RF['111']='0000000000000000'
            return False,PC+1          
    
    elif (current_instruction[0:5]=='10001'):
        #Jump if greater than
        if RF['111']=='0000000000000010':
            new_PC=int(current_instruction[8:16],2)
            RF['111']='0000000000000000'
            return False,new_PC
        else:
            RF['111']='0000000000000000'
            return False,PC+1
    
    elif (current_instruction[0:5]=='10010'):
        #Jump if equal
        if RF['111']=='0000000000000001':
            new_PC=int(current_instruction[8:16],2)
            RF['111']='0000000000000000'
            return False,new_PC
        else:
            RF['111']='0000000000000000'
            return False,PC+1
    
    elif (current_instruction[0:5]=='10011'):
        RF['111']='0000000000000000'
        return True,PC+1
        #Halt
    
                    
    return False,PC+1   #place holder values

def PC_update(new_PC):
    PC=new_PC
    return PC


#Driver Code  
PC=0;
halted=False;
cycle=[]
cyclevar=0
memadd=[]

while(not halted):
    current_instruction=MEM_getdata();
    halted, new_PC= execute(current_instruction);
    PC_dump();
    RF_dump();
    memadd.append(PC)
    PC=PC_update(new_PC);
    cycle.append(cyclevar)
    cyclevar+=1
MEM_dump();

plt.scatter(cycle, memadd)
plt.savefig('plot.png')