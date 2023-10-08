import wordfreq
import string
import re
import subprocess

#from itertools import permutations
from itertools import chain, permutations, groupby, product
from operator import itemgetter

from sympy.combinatorics import Permutation

def is_5digit_lowercase(s):
        return re.match("^[a-z][a-z][a-z][a-z][a-z]$", s)


Ndict = 8000
lang = 'en'    

words = {}

for w in wordfreq.iter_wordlist(lang):
        if is_5digit_lowercase(w):
            words[w] = wordfreq.word_frequency(w,lang)
            if len(words)>=Ndict:
                break


def printletter(let,col):
        if col == 'g':
            print('\033[42m'+let.upper()+"\033[0m",end="")
        elif col == 'y':
            print('\033[103m'+let.upper()+"\033[0m",end="")
        else:
            print(let.upper(),end="")
    

def printwaffle(letters,colors):
    for (i,(let,col)) in enumerate(zip(letters,colors)):
        printletter(let,col)
        print(" ",end='')
        if i in {5,6,13,14}:
             print("  ",end="")
        if i in {4,7,12,15}:
             print()
    print()


while True:
    letters = input('letters: ')# 'ciiacihenmoflvanpdllt'
    if len(letters)==0:
        print('using waffle #14')
        letters= 'siatnoyodhdverhetrmoe'
        colors = 'gyyygyywwwgwywwwgwywg'
        printwaffle(letters,colors)
        break
    colors =  input('colors: ')#'ggywgwwyywgwywywgwywg'      
# #letters = '012345678901234567890'
    printwaffle(letters,colors)
    if input('OK?').strip().upper()=='Y':
        break


# letters= 'ciiacihenmoflvanpdllt'
# colors = 'ggywgwwyywgwywywgwywg'
# printwaffle(letters,colors)

#first find allowable words for each wordspace
# horizontal wordspaces are listed first

wordspaces = [[0,1,2,3,4],[8,9,10,11,12],[16,17,18,19,20],
              [0,5,8,13,16],[2,6,10,14,18],[4,7,12,15,20]]

# for ws in wordspaces:
#     ls = [letters[k] for k in ws]
#     cs = [colors[k] for k in ws]
#     for (l,c) in zip(ls,cs):
#          printletter(l,c)
#     print()


#work out possible words for each wordspace
allpossiblewords = []


di = open('dlxinput.txt','w')

di.write('| solving waffles\n')
#write description of items

#primary
#the contraint that guarantees we have a word in each of the word spaces
for k in range(6):
        di.write(f'w{k} ')
#write the contraint that guarantees we have a letter in each of the letter spaces
for k in range(21):
        di.write(f'l{k} ')
#write the constraint that counts the letters
for k in string.ascii_lowercase:
        cnt = letters.count(k)
        if cnt!=0:
                di.write(f'{cnt}:{cnt}|{k} ')

di.write('| ')
#secondary contraints
for k in range(21):
        di.write(f'c{k} ')
di.write('\n')



#write out options that involves filling each cell with each letter
for k in range(21):
        for ch in set(letters):#string.ascii_lowercase:
            di.write(f'l{k} {ch} c{k}:{ch}\n')


                     


for (wordnum,ws) in enumerate(wordspaces):
#for ws in wordspaces:
    possiblewords = []
    letterset = set(letters)
    freeletters = []
    for (l,c) in zip(letters,colors):
        if c!='g':
             freeletters.append(l)
    freeletters =set(freeletters)



    #make regex to check if w has the correct green letters
    rex = ['^','[a-z]','[a-z]','[a-z]','[a-z]','[a-z]','$']
    nongreenletters = []
    for k in range(5):
               #import pdb;pdb.set_trace()
                if colors[ws[k]] =='g':
                    rex[k+1] = letters[ws[k]]
                else:
                     nongreenletters.append(letters[ws[k]])
    rex = ''.join(rex)
    nongreenletters=set(nongreenletters)
    #print(rex)
  

    for w in words:
        if not re.match(rex, w):
            continue
        if not len(set(w)-letterset)==0:
            continue
        #print(w)
        di.write(f'w{wordnum}')
        for (i,j) in enumerate(ws):
            di.write(f' c{j}:{w[i]}')
        di.write('\n')
di.close()

                         
dlx3 = subprocess.Popen('knuth/dlx3 m1'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
dlx3.stdin.write(bytes(open('dlxinput.txt','r').read(),'utf-8'))
dlx3.stdin.close()
dlx3.wait()



#a regular expression that matches things like "c4:a" and gives 4 and a for cell and letter
regex = re.compile(r'c(?P<cell>\d+):(?P<letter>\w)')

for kk in [0]:
    line = dlx3.stdout.readline().decode('utf-8')
    if line=='':
        break
    print(line,end='')
    solutionletters = ['.' for i in range(21)]
    for k in range(27):
        ress = dlx3.stdout.readline().decode('utf-8').strip().split()
        for res in ress:
            if regex.match(res):
                (cell,letter) = regex.match(res).groups()
                cell = int(cell)
                solutionletters[cell] = letter
    solutionletters=''.join(solutionletters)
    assert(solutionletters.count('.')==0)
    allgreen = ''.join(['w' for iii in range(21)])
    printwaffle(solutionletters,allgreen)


L  = [(letters[i],i) for i in range(len(letters))]
L.sort()
(sortedletters,p1) = zip(*L)
p1=Permutation(p1)

L  = [(solutionletters[i],i) for i in range(len(solutionletters))]
L.sort()
(sortedletters,p2) = zip(*L)
p2=Permutation(p2)

#print(list(solutionletters) == [letters[i] for i in ~p2*p1])

#thanks stack exchange!!
#https://stackoverflow.com/questions/70125930/sorting-a-list-by-another-list-with-duplicates/70126643#70126643

def all_sorts(numbers, letters):
    return [list(map(itemgetter(1), chain.from_iterable(p))) for p in product(*(permutations(g) for _,g in groupby(sorted(zip(numbers, letters)), key=itemgetter(0))))]

#print( all_sorts([1,2,3,1,2,1], 'abcdef') )
# [['a', 'd', 'f', 'b', 'e', 'c'], ['a', 'd', 'f', 'e', 'b', 'c'], ['a', 'f', 'd', 'b', 'e', 'c'], ['a', 'f', 'd', 'e', 'b', 'c'], ['d', 'a', 'f', 'b', 'e', 'c'], ['d', 'a', 'f', 'e', 'b', 'c'], ['d', 'f', 'a', 'b', 'e', 'c'], ['d', 'f', 'a', 'e', 'b', 'c'], ['f', 'a', 'd', 'b', 'e', 'c'], ['f', 'a', 'd', 'e', 'b', 'c'], ['f', 'd', 'a', 'b', 'e', 'c'], ['f', 'd', 'a', 'e', 'b', 'c']]

    
ps = all_sorts(solutionletters,range(len(solutionletters)))

max_cycles=1

for (k,p) in enumerate(ps):
    if (~Permutation(p)*p1).cycles > max_cycles:
         max_cycles = (~Permutation(p)*p1).cycles
         bestp = ~Permutation(p)*p1

print()
print(f"Solution possible in {21-max_cycles} swaps")

#work with the optimal permutations cycles
bestp = bestp.full_cyclic_form
bestp.sort(key=len)



partialsolution = list(letters)

for cycle in bestp:
    m = len(cycle)
    print('We have a cycle: ',end='')
    print(cycle )
    for k in range(m-1):
        print(f'Swap {cycle[(k+1)]} and {cycle[k]}')
        
        swapcolors = (['w' for iii in range(21)])
        swapcolors[cycle[(k+1)]] = 'g'
        swapcolors[cycle[k]] = 'g'
        tmp = partialsolution[cycle[k+1]]
        partialsolution[cycle[(k+1)]]=partialsolution[cycle[(k)]]
        partialsolution[cycle[k]]=tmp

        printwaffle(partialsolution,''.join(swapcolors))
        print()
        print()
          
