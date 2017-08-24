from numpy import genfromtxt
import treepredict

data = genfromtxt("F:\\nama yang punya laptop\\demi masa depan yang lebih cerah\\KULIAH\\SKRIPSI\\DATA XYZ\\dataset.csv", delimiter=',')

class decisionnode:
  def __init__(self,col_num=-1,test=None,results=None,tb=None,fb=None):
    self.col_num=col_num
    self.test=test
    self.results=results
    self.tb=tb
    self.fb=fb
    
def dividedata(data, col_num, test=None):
    "Doc string placeholder"
    if test==None: return data[:], []
    set0, set1 = [], []
    for row in data:
        if test(row[col_num]):
            set0.append(row)
        else:
            set1.append(row)

    return set0, set1

def uniquecounts(rows):
   results={}
   for row in rows:
      # The result is the last column
      r=row[len(row)-1]
      if r not in results: results[r]= 0
      results[r]+= 1
   return results

def entropy(rows):
   from math import log
   log2=lambda x:log(x)/log(2)  
   results=uniquecounts(rows)
   # calculate the entropy
   ent=0.0
   for r in results.keys():
      p=float(results[r])/len(rows)
      ent=ent-p*log2(p)
   return ent

def buildtree(data,scoref=entropy):
   if len(data)==0: return decisionnode()
   current_score=scoref(data)
   best_gain=0.0
   best_criteria=None
   best_sets=None
   column_count=len(data[0])-1
       
   for col_num in range(0,column_count):
            global column_values      
            column_values={}            
            for row in data:
                column_values[row[col_num]]=1 
            for test in column_values.keys():
                 (set0,set1)=dividedata(data, col_num, test=None)
                 # information gain
                 p=float(len(set0))/len(data)
                 gain=current_score-p*scoref(set0)-(1-p)*scoref(set1)
                 if gain>best_gain and len(set0)>0 and len(set1)>0:
                         best_gain=gain
                         best_criteria=(col_num, test)
                         best_sets=(set0,set1)
  
            if best_gain>0:
                 trueBranch=buildtree(best_sets[0])
                 falseBranch=buildtree(best_sets[1])
                 return decisionnode(col_num=best_criteria[0], test=best_criteria[1],
                        tb=trueBranch,fb=falseBranch)
            else:
                 return decisionnode(results=uniquecounts(data))
      
set0, set1 = dividedata(data, 2, lambda answer: answer==2017)
print(entropy(set0), entropy(set1), sep='\n')

tree=treepredict.buildtree(treepredict.data)

print(tree.col_num)
print(tree.test)
print(tree.results)
print("")
print(tree.tb.col_num)
print(tree.tb.test)
print(tree.tb.results)
print("")
print(tree.tb.tb.col_num)
print(tree.tb.tb.test)
print(tree.tb.tb.results)
print("")
print(tree.tb.fb.col_num)
print(tree.tb.fb.test)
print(tree.tb.fb.results)

def printtree(tree, indent=''):
	if tree.results != None:  # leaf node
         print(str(tree.results))
	else:
         print(str(tree.col_num)+":"+str(tree.test)+"? ")
         print(indent+'T->', end=" ")
         printtree(tree.tb,indent+'  ')
         print(indent+'F->', end=" ")
         printtree(tree.fb,indent+'  ')
         
print(treepredict.printtree(tree))

