from logic import *
# sanity: 3 var mayoría
on=[3,5,6,7]
m=minimize(3,on); print(sop_str(3,m,'ABC',latex=False))
assert all(eval_sop(m,i)==(i in on) for i in range(8))
# con indiferentes
m=minimize(4,[1,3,7,11,15],[0,2,5]); print(sop_str(4,m,'ABCD',latex=False))
print(pos_str(3,pos_minimize(3,on),'ABC',latex=False))
