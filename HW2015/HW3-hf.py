#coding: utf-8
'''
huarongdao pass puzzle

ver：1.0
it is a original version

by HF
Dec 2015

'''
from __future__ import division
import cairo
import colorsys
import copy
#define soldiers
#from IPython import embed
from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()


class block(object):
    
    def __init__(self, w, h, name, kind, x=-1, y=-1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.kind = kind

    def move(self, dir):
        if dir=="U": #y-1
            if self.y==1: 
                return False
            self.y -= 1
            return True
        if dir=="D": #y+1
            if self.y + self.h > 5: 
                return False
            self.y += 1
            return True
        if dir=="L": #x-1
            if self.x==1: 
                return False
            self.x -= 1
            return True
        if dir=="R": #x+1
            if self.x + self.w > 4: 
                return False
            self.x += 1
            return True    
        assert False
    
    def draw(self, ctx):
        h = (hash(self.name) & 0x0f)/16.0
        r,g,b = colorsys.hsv_to_rgb(h, 0.6, .9)
        ctx.set_source_rgb(r,g,b)

        ctx.rectangle(self.x+0.05,self.y+0.05,self.w-0.1,self.h-0.1)
        ctx.fill_preserve()
        ctx.set_line_width(0.03)
        ctx.set_source_rgb(0,0,0)
        ctx.stroke()
       
        ctx.select_font_face("u微软雅黑", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(0.3);
        
        x_bearing, y_bearing, width, height = ctx.text_extents (self.name)[:4]
        ctx.move_to( self.x + self.w/2 - width / 2 - x_bearing, self.y + self.h/2 - height / 2 - y_bearing)
        
        ctx.show_text(self.name)

class board(object):
    def __init__(self):
        self.items = [
            block(2,2,u"曹操",1,2,1),
            block(2,1,u"关羽",3,2,3),
            block(1,2,u"张飞",2,1,1),
            block(1,2,u"马超",2,1,3),
            block(1,2,u"赵云",2,4,1),
            block(1,2,u"黄忠",2,4,3),
            block(1,1,u"卒1",4,1,5),
            block(1,1,u"卒2",4,2,4),
            block(1,1,u"卒3",4,3,4),
            block(1,1,u"卒4",4,4,5)
        ]
        self.items = [
            block(2,2,u"曹操",1,1,3),
            block(2,1,u"关羽",3,1,5),
            block(1,2,u"张飞",2,1,1),
            block(1,2,u"马超",2,2,1),
            block(1,2,u"赵云",2,3,1),
            block(1,2,u"黄忠",2,4,1),
            block(1,1,u"卒1",4,3,3),
            block(1,1,u"卒2",4,4,3),
            block(1,1,u"卒3",4,3,4),
            block(1,1,u"卒4",4,4,4)
        ]
        print "OK?", self.is_ok()

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return self.pattern()
        s
    def pattern(self):
        mask = [ [0]*5 for j in range(4) ]
        for b in self.items:
            for x in range(b.w):
                for y in range(b.h):
                    #print b.x, b.y, b.name, b.kind
                    mask[x+b.x-1][y+b.y-1] = b.kind
        
        s = ""
        for j in range(4):
            s += "".join("%d" % n for n in mask[j])
        return s
    
    def is_ok(self):
        return self.pattern().count('0')==2
    
    def is_done(self):
        return self.items[0].x==2 and self.items[0].y==4
        
    def draw(self, ctx):
        for i in self.items:
            i.draw(ctx)
        #draw self
        
    def nextState(self):
        result = []
        for i, b in enumerate(self.items):
            for m in ("U","D","L","R"):
                new_board = self.copy()
                if new_board.items[i].move(m):
                    if new_board.is_ok():
                       result.append(new_board)
        return result

def bfs(initboard):
    open_list = [initboard]
    close_list = []
    visited = {}
    distance = {}
    visited[initboard.pattern()] = initboard
    distance[initboard.pattern()] = 0
    prev = {}
    prev[initboard.pattern()] = None
    found = False
    
    cnt = 0
    while open_list and not found:
        v = open_list.pop(0)
        close_list.append(v)
        vd = distance[v.pattern()]
        
        if vd >=10:
            ipshell()
        
        cnt += 1
        if cnt%100==0:
            print "Iter %d, Len(open)=%d, len(close)=%d, Dist=%d" % (cnt, len(open_list), len(close_list), vd)
                
        for nv in v.nextState():
            if nv.is_done():
                prev[nv.pattern()] = v.pattern()
                visited[np] = nv
                found = True
                break
            np = nv.pattern()
            if np in  visited:
                continue
            open_list.append(nv)
            visited[np] = nv
            distance[np] = vd + 1
            prev[np] = v.pattern()
    
    if found:
        result = [nv]
        while prev[nv.pattern()]!=None:
            nv = visited[ prev[nv.pattern()] ]
            result.append(nv)
        print "Done"  
        return result[::-1]
    return None
        
        
if __name__ == "__main__":
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,500,500)
    ctx=cairo.Context(surface)
    ctx.scale(50, 50)
    bd = board()
    bd.draw(ctx)
    surface.write_to_png("1.png")
    
    nbd = bd.nextState()
    

    result = bfs(bd)
    for i, b in enumerate(result):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,500,500)
        ctx=cairo.Context(surface)
        ctx.scale(50, 50)
        b.draw(ctx)
        surface.write_to_png("t%d.png" %i)
   
