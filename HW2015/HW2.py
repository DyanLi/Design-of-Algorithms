#coding: utf-8
'''
HW2.py is used to solve eight queens puzzle,
you can change the size number to resize the board.

change:
1,draw pieces with special operator not XOR but SOURCE
2,long string can write like """....""
3,format for str have symbol{} so use %d

'''
import itertools,cairo,math

size=8 #the size of the board
cnt=0 #number of right answer

#check whether it is a right step or not
def conflict(state, nextX):
    nextY = len(state)
    for i in range(nextY):
        if abs(nextX-state[i])== nextY-i:
             return True
    return False

def drawqueen(solution):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,size*100,size*100)
    ctx=cairo.Context(surface)

    #draw the board
    for i in range(0,size):
        for j in range(0,size):
            if (i+j)%2==1:
                ctx.rectangle(i*100,j*100,100,100)
    ctx.fill()

    #draw the pieces
    ctx.set_line_width(10)
    ctx.set_source_rgb(1, 1, 0.2)
    #change1
    ctx.set_operator(cairo.OPERATOR_SOURCE)
    for i in range(size):
        ctx.arc(solution[i]*100+50,i*100+50,35,0,2*math.pi)
        ctx.stroke()

    filename="chess"+str(cnt)+".png"
    surface.write_to_png(filename)



#remove the solutions in same cols
for solve in itertools.permutations(range(size)):
    flag=0
    for i in range(1,size):
        if conflict(solve[0:i],solve[i]):
            break
        else:
            flag+=1
    if flag==size-1:
        cnt+=1
        drawqueen(solve)



#make a tex ducument to generate pdf
f=open("mkreport.tex",'w')

#change2
f.write("""\documentclass[twocolumn]{article}
\usepackage{graphicx}
\\title{A Report About Eight Queens Puzzle}\n
\\begin{document}
\maketitle\n
""")

#change3
for i in range(1,cnt+1):
    f.write("""
\\begin{figure}[t]       
\centering
\includegraphics[width=0.3\\textwidth]{chess%d.png}
\caption{Sulution %d of Eight Queens Puzzle}
\end{figure}\n""" % (i,i) )

    if i%6==0:
        f.write('\n\clearpage\n')

f.write('\n\end{document}')
f.close()
