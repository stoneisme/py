#/usr/bin/env python

t  = ((1,2,3),(4,5,6))
t1 = (7,8,9)
print (t1,t[0:])
#结果:((7, 8, 9), ((1, 2, 3), (4, 5, 6)))

'''
t=((1,2,3),(4,5,6))
t1=(7,8,9)
print ((t1,)+t[0:])
#结果:((7, 8, 9), (1, 2, 3), (4, 5, 6))

t=((1,2,3),(4,5,6))
t1=(7,8,9)
print (t1+t[0:])
#结果:(7, 8, 9, (1, 2, 3), (4, 5, 6))
'''