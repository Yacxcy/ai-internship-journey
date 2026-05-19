class Persion:
    """人类"""
    species = "Homo Sapiens"  # 类属性
    
    def __init__(self,name:str,age:int):
        self.name = name
        self.age = age
    def __str__(self):
        return f"人的名字是{self.name}，年龄是{self.age}"
    @property
    def is_adult(self):
        return self.age >= 18

class Student(Persion):
    """学生"""
    def __init__(self,name:str,age:int,school:str):
        super().__init__(name,age)
        self.school = school
    def __str__(self):
        return f"学生的名字是{self.name}，年龄是{self.age}，学校是{self.school}"

s = Student("张三", 20, "清华大学")
print(s)
print(s.is_adult)
print(s.species)