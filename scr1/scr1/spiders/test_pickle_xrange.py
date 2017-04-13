#/bin/env python
# coding:utf8

#测试pickle序列化 xrange函数



import pickle
import os


def strrange(i=0):#用默认参数来控制第一次还是后几次
    x = range(i,30)
    for a in x:
        yield a


if __name__ == '__main__':

    if os.path.isfile('x.p'):
        print 'not first run,begin reload file'
        f = open('x.p')
        x = strrange(i = pickle.load(f)+1)  #用默认参数来控制
        f.close()
        t =0 
        print 'load file over'
        for a in range(10):
            print 'begin run'
            print '==',a
            try:
                t = x.next()
                print t
            except StopIteration:
                print u'data over! stop run!'
                break
            
        print "load run over,store again!"
        f = open('x.p','w')
        pickle.dump(t,f)
        f.close()       
        print 'store over!'
        
    else:
        print 'fist run,begin init.......'
        x = strrange()
        t = 0
        for a in range(10):
            print '==',a
            try:
                t = x.next()
                print t
            except StopIteration:
                print u'data over! stop run!'
                break
        print 'sotore to file first!'
        f = open('x.p','wb')
        pickle.dump(t,f)
        f.close()
        

                

