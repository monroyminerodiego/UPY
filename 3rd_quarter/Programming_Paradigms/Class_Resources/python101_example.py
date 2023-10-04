# 1. Class - Define a class called Person
class Person:
    # 2. Instance - Initialize an instance of the class with attributes
    def __init__(self, name, age):
        self.name = name
        self.age = age
 
    # 3. Object - Create two objects (persons) from the class
    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
 
# 4. Message - Sending a message to the object
person1 = Person("José", 23)
person1.greet()  # Calls the greet method on person1
 
person2 = Person("Fabiana", 23)
person2.greet()  # Calls the greet method on person2
 
# 5. Inheritance - Create a subclass that inherits from Person
class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
        self.courses = []
 
    def study(self, subject):
        print(f"{self.name} is studying {subject}.")
 
    # 7. Abstraction - Encapsulate the concept of enrolling in a course
    def enroll(self, course):
        self.courses.append(course)
        print(f"{self.name} has enrolled in the course: {course}")
 
# 6. Polymorphism - Using polymorphism to call greet method on different objects
def introduce(person):
    person.greet()
 
student = Student("Mariana", 22, "S12345")
introduce(person1)  # Polymorphism with a Person object
introduce(student)   # Polymorphism with a Student object
 
# 8. Encapsulation - Accessing attributes through methods, encapsulating data
student.enroll("Mathematics")
student.enroll("Computer Science")
student.enroll("Programming Paradigms")
 
# Accessing the encapsulated course list
print(f"{student.name}'s enrolled courses: {student.courses}")