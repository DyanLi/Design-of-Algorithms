#coding: utf-8
'''
huarongdao pass puzzle

ver:3.3
a  reconstruction version of ver3.0
draw every state like a tree

by Dyan
Dec 2015
'''
from __future__ import division
import cairo
import colorsys
import copy
import collections



class Block(object):
    u'''华容道具有10个块，棋盘左上角坐标(1,1),右下角坐标(4,5)'''
    
    def __init__ (self, width, height, name, kind ,x=-1 ,y=-1):
        self.width = width
        self.height = height
        self.name = name
        self.kind = kind #1:cao 2:guanyu 3:generals 4:pawns

        self.x=x
        self.y=y

    def move(self, dir):
        #move the Block based on dir 
        if dir=="U": #y-1
            if self.y==1: 
                return False
            self.y -= 1
            return True
        if dir=="D": #y+1
            if self.y + self.height > 5: 
                return False
            self.y += 1
            return True
        if dir=="L": #x-1
            if self.x==1: 
                return False
            self.x -= 1
            return True
        if dir=="R": #x+1
            if self.x + self.width > 4: 
                return False
            self.x += 1
            return True    
        assert False

    def draw(self,px,py,ctx):
        #draw the Block
        h = (hash(self.name) & 0x0f)/16.0
        r,g,b = colorsys.hsv_to_rgb(h, .75, .9)
        ctx.set_source_rgb(r,g,b)

        ctx.rectangle( px+self.x, py+self.y ,self.width-.1,self.height-.1)
        ctx.fill_preserve()

        #stroke the edges
        ctx.set_line_width(0.03)
        ctx.set_source_rgb(0,0,0)
        ctx.stroke()

        #give a text
        ctx.select_font_face("u微软雅黑", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(0.3)
        x_bearing, y_bearing, width, height = ctx.text_extents (self.name)[:4]
        ctx.move_to( px+self.x + self.width / 2 - width / 2 - x_bearing, py+self.y + self.height/2 - height / 2 - y_bearing)
        ctx.show_text(self.name)


class Board(object):
    u'''棋盘'''
    def __init__ (self,pos):
        self.items = [
            Block(2,2,u"曹操",1,pos[0][0],pos[0][1]),
            Block(2,1,u"关羽",2,pos[1][0],pos[1][1]),
            Block(1,2,u"张飞",3,pos[2][0],pos[2][1]),
            Block(1,2,u"马超",3,pos[3][0],pos[3][1]),
            Block(1,2,u"赵云",3,pos[4][0],pos[4][1]),
            Block(1,2,u"黄忠",3,pos[5][0],pos[5][1]),
            Block(1,1,u"卒1",4,pos[6][0],pos[6][1]),
            Block(1,1,u"卒2",4,pos[7][0],pos[7][1]),
            Block(1,1,u"卒3",4,pos[8][0],pos[8][1]),
            Block(1,1,u"卒4",4,pos[9][0],pos[9][1])
        ]
        print "OK?", self.is_ok()

    def __str__(self):
        return self.pattern()

    def copy(self):
        return copy.deepcopy(self)

    def pattern(self):
        #使用一个二维数组唯一地表示一个棋盘的状态
        mask = [ [0]*5 for i in range(4) ]
        for i, b in enumerate(self.items):
            for x in range(b.width):
                for y in range(b.height):
                    mask[b.x+x-1][b.y+y-1]= b.kind
        #print mask
        #数组变字符串，一个字符串唯一地表示一个棋盘的状态
        s = ""
        for j in range(4):
            s += "".join("%d" % n for n in mask[j])
        return s

    def is_ok(self):
        #check the move is available?
        return self.pattern().count('0')==2

    def is_done(self):
        #check the board is sulution?
        return self.items[0].x==2 and self.items[0].y==4

    def draw(self,px,py,ctx):
        #draw current board
        #draw every block based on self.pos
        for i, b in enumerate(self.items):
                b.draw(px,py,ctx)
        #draw the board boundary
        ctx.set_line_width(0.1)
        ctx.rectangle( px+1 -.1, py+1 -.1 ,4 +.1,5 +.1 )
        ctx.stroke()

    def nextstate(self):
        u''' 列举可行的移动，返回几种新的棋盘 '''
        result = []
        for i ,b in enumerate(self.items):
            for m in ("U","D","R","L"):
                new_board = self.copy()
                if new_board.items[i].move(m):
                    if new_board.is_ok():
                       result.append(new_board)
        return result

def bfs(board):
    u'''广度优先搜索求棋盘解 '''
    open_list = [board]    #待搜索的Board()实例
    close_list = []    #搜索过的实例

    searched= {}    #已经寻找到的节点 dict k:pattern v:board instance of Board()
    distance = {}    #dict k:pattern v:number of moves
    searched[board.pattern()] = board
    distance[board.pattern()] = 0
    
    prev = {}   #dict k:pattern v:father node pattern
    prev[board.pattern()] = None
    found = False

    #记录迭代次数
    cnt = 0
    while open_list and not found:
        #从openlist取出一个节点，放入closelist
        v = open_list.pop(0)
        close_list.append(v)
        #v 's distance
        vd = distance[v.pattern()]
        
        #每处理1k个结点，输出信息    
        cnt+=1
        if cnt%1==0:
            print "Iter %d, Len(open)=%d, len(close)=%d, Dist=%d" % (cnt, len(open_list), len(close_list), vd)

        # 这个结点棋盘所有可行的下一步
        for i, nv in enumerate(v.nextstate()):
            np = nv.pattern()
            #如果是正解 跳出
            if nv.is_done():
                searched[np] = nv
                prev[np] = v.pattern()
                found = True
                break
            #如果这一步曾经走过 不再处理
            if np in searched:
                continue

            prev[np] = v.pattern()
            open_list.append(nv)
            searched[np] = nv
            distance[np] = vd + 1

    if found:
        prev[nv.pattern()] = v.pattern()
        close_list.append(nv)
        distance[nv.pattern()] = vd + 1

        result = [nv]
        while prev[nv.pattern()]!=None:
            nv = searched[ prev[nv.pattern()] ]
            result.append(nv)
        print "Done!" 
        drawtree(close_list,distance,prev,result[::1]) 
        return result[::-1]       
    return None

def drawtree(close_list,distance,prev,result):
    #计算每一层的孩子总数目
    alldst = []
    for s in close_list:
        alldst.append(distance[s.pattern()])
    laycnt = collections.Counter(alldst) 

    #画出棋盘状态的树状结构
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,6000,7000)
    ctx = cairo.Context(surface)
    #ctx.translate(3000,0)
    ctx.scale(50, 50)
    #x指示s是当前层第几个孩子
    x = [0]*20
    #s横向的位置
    sx = {}    

    while close_list:
        s = close_list.pop(0)
        sp = s.pattern()
        sd = distance[sp]

        factor = 120/(laycnt[sd]+1)
        #记录s的横向位置
        x[sd]+=1
        sx[sp] = x[sd]*factor
        s.draw(sx[sp] ,sd*10, ctx)

        if prev[sp]:
            ctx.set_line_width(.1)
            ctx.move_to(sx[sp]+3,sd*10+1)
            ctx.line_to(sx[ prev[sp] ]+3,(sd-1)*10+6)
            ctx.stroke()

    for i, s in enumerate(result):
        sp = s.pattern()
        sd = distance[sp]

        ctx.set_line_width(0.2)
        ctx.set_source_rgb(1,1,0.2)
        if prev[sp]:
            ctx.move_to(sx[sp]+3,sd*10+1)
            ctx.line_to(sx[ prev[sp] ]+3,(sd-1)*10+6)
            ctx.stroke()

    surface.write_to_png("t1.png")


if __name__ == "__main__":
    # 开局棋子位置
    # 横刀立马
    #init = [(2,1),(2,3),
    #        (1,1),(1,3),(4,1),(4,3),    
    #        (1,5),(2,4),(3,4),(4,5)]
    
    # easy 
    init = [(1,3),(3,3),
            (1,1),(2,1),(3,1),(4,1),    
            (1,5),(2,5),(3,4),(4,5)]
    
    # most easy
    #init = [(1,4),(1,3),
    #        (1,1),(2,1),(3,1),(4,1),
    #        (3,3),(3,5),(4,4),(4,5)]

    board=Board(init)
    #board.draw()
    result = bfs(board)
    print "Find a solution after %d moves." % (len(result)-1)
  


        

