#！/usr/bin/python3
import os
import math
import json


def log(msg):
	print(msg)

class ArrayNumbers():
	def __init__(self,numbers=[],level=9):
		'''
		初始化数组，包括内容和级别
		'''
		self.level=level
		self.base=[]
		for i in range(level):
			self.base.append(i+1)
		self.length=level*level
		self.numbers=[]
		self.dict={}
		for i in range(self.length):
			if i<len(numbers):
				self.numbers.append(numbers[i])
				if numbers[i]>0:
					self.dict[str(i)]=[numbers[i]]
				else:
					self.dict[str(i)]=self.base.copy()
			else:
				self.numbers.append(0)
				self.dict[str(i)]=self.base.copy()
		self.gonglen=0
		sqrt=math.sqrt(self.level)
		if int(sqrt)==sqrt:
			self.gonglen=int(sqrt)
		self.ok=False
		log("初始状态数组:%s"%self.get_numbers_text())
		#log("初始状态字典:%s"%json.dumps(self.dict,indent=4))
	def get_numbers_text(self):
		'''
			获取当前整个数组的字符串打印信息
		'''
		flag="+"+"++"*self.level+"++"*self.gonglen
		ret_text=os.linesep+flag+os.linesep
		for i in range(self.level):
			line_str="+ "
			for j in range(self.level):
				line_str+=str(self.numbers[self.convert_rc_to_index((i,j))])+" "
				if self.gonglen>0 and j>0 and (j+1)%self.gonglen==0:
					line_str+="+ "
			ret_text+=line_str+os.linesep
			if self.gonglen>0 and i>0 and (i+1)%self.gonglen==0:
				ret_text+=flag+os.linesep
		if self.gonglen==0:
			ret_text+=flag+os.linesep
		return ret_text
	def convert_index_to_rc(self,index):
		'''转化index到(row,col)'''
		row=int(index/self.level)
		col=index%self.level
		return (row,col)
	def convert_rc_to_index(self,rc):
		'''转化(row,col)到index'''
		index=rc[0]*self.level+rc[1]
		return index
	def get_row_indexs_from_index(self,index):
		'''从格子获取一行的index'''
		rows=[]
		_row=int(index/self.level)
		for i in range(self.level):
			rows.append(_row*self.level+i)
		return rows
	def get_col_indexs_from_index(self,index):
		'''从格子获取一列的index'''
		cols=[]
		_col=index%self.level
		for i in range(self.level):
			cols.append(self.level*i+_col)
		return cols
	def get_gong_indexs_from_index(self,index):
		'''从格子获取宫的index'''
		grc=self.get_gongrc_from_index(index)
		return self.get_gong_indexs_from_gongrc(grc)
	def get_gongrc_from_index(self,index):
		'''从格子获取宫的row，col '''
		(row,col)=self.convert_index_to_rc(index)
		if self.gonglen>0:
			grow=int(row/self.gonglen)
			gcol=int(col/self.gonglen)
			return (grow,gcol)
		else:
			return (0,0)
	def get_gong_indexs_from_gongrc(self,grc):
		'''从宫的col和row获取宫的所有index '''
		indexs=[]
		if self.gonglen>0:
			for i in range(self.gonglen):
				for j in range(self.gonglen):
					row=grc[0]*self.gonglen+i
					col=grc[1]*self.gonglen+j
					indexs.append(self.convert_rc_to_index((row,col)))
			return indexs
		else:
			return []
	def remove_number_from_index(self,index,number):
		'''remove one number form an index'''
		v0=self.dict[str(index)]
		if self.dict[str(index)].count(number)==1:
			msg="字典计算结果:index=%d发生改变,改变前为:%s"%(index,str(v0))
			v0.remove(number)
			msg+=",改变后为:%s,减少数字%d"%(str(v0),number)
			self.dict[str(index)]=v0
			log(msg)
			if len(self.dict[str(index)])==1:
				self.numbers[index]=self.dict[str(index)][0]
				log("数组计算结果:index=%d确定数字为%d,整个数组为:%s"%(index,v0[0],self.get_numbers_text()))
			return len(v0)
		else:
			msg="字典计算结果:index=%d结果不变,结果为:%s"%(index,str(v0))
			log(msg)
			return len(v0)
	def remove_number_about_index(self,index,number):
		'''remove one number form a col'''
		(row,col)=self.convert_index_to_rc(index)
		rows=self.get_row_indexs_from_index(index)
		rows.remove(index)
		log("在第%d行(序号[%s])去除数字%d"%(row+1,str(rows),number))
		for i in rows:
			if self.remove_number_from_index(i,number):
				continue
			else:
				rc=self.convert_index_to_rc(i)
				log("在第%d行(序号[%s])去除数字%d时，第%d行第%d列(序号%d)无解"%(row+1,str(rows),number,rc[0]+1,rc[1]+1,i))
				return False
		cols=self.get_col_indexs_from_index(index)
		cols.remove(index)
		log("在第%d列(序号[%s])去除数字%d"%(col+1,str(cols),number))
		for i in cols:
			if self.remove_number_from_index(i,number):
				continue
			else:
				rc=self.convert_index_to_rc(i)
				log("在第%d列(序号[%s])去除数字%d时，第%d行第%d列(序号%d)无解"%(col+1,str(cols),number,rc[0]+1,rc[1]+1,i))
				return False
		if self.gonglen>0:
			(grow,gcol)=self.get_gongrc_from_index(index)
			gongs=self.get_gong_indexs_from_gongrc((grow,gcol))
			gongs.remove(index)
			log("在宫(%d,%d)(序号[%s])去除数字%d"%(grow,gcol,str(gongs),number))
			for i in gongs:
				if self.remove_number_from_index(i,number):
					continue
				else:
					rc=self.convert_index_to_rc(i)
					log("在宫(%d,%d)(序号[%s])去除数字%d时，第%d行第%d列(序号%d)无解"%(grow,gcol,str(gongs),number,rc[0]+1,rc[1]+1,i))
					return False
		return True
	def update(self):
		for k in self.dict:
			if len(self.dict[k])==1:
				self.numbers[int(k)]==self.dict[k][0]
		if self.numbers.count(0)==0:
			self.ok=True
	def compute(self):
		breakflag=False
		while not self.ok and not breakflag:
			for i in range(self.length):
				if self.numbers[i]!=0:
					if not self.remove_number_about_index(i,self.numbers[i]):
						log("解题失败")
						breakflag=True
						break
			self.update()
			log("解题结果：%s"%self.get_numbers_text())
		if self.ok:
			log("解题成功")
			log("最终答案：%s"%self.get_numbers_text())


if __name__=="__main__":
	#numbers=[0,3,1,0,1,0,0,3,2,0,3,4,0,4,2,0]
	#level=4
	numbers=[0,0,0,1,0,0,2,6,0]
	numbers+=[7,0,0,0,3,0,0,0,0]
	numbers+=[3,0,2,0,8,0,4,0,0]
	
	numbers+=[0,0,0,4,0,8,0,0,1]
	numbers+=[0,3,5,0,0,0,9,4,0]
	numbers+=[2,0,0,3,0,5,0,0,0]
	
	numbers+=[0,0,6,0,5,0,7,0,9]
	numbers+=[0,0,0,0,4,0,0,0,8]
	numbers+=[0,5,7,0,0,9,0,0,0]
	
	level=9
	shudu=ArrayNumbers(numbers,level)
	shudu.compute()