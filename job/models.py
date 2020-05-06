from django.db import models

# Create your models here.
class department(models.Model):
    dept_no=models.IntegerField(primary_key=True)
    dept_name=models.TextField(max_length=50)

    def __str__(self):
        return str(self.dept_name) +" ( " + str(self.dept_no)+ " )"


class student(models.Model):
    enroll_no=models.TextField(primary_key=True,max_length=20)
    student_dept_no=models.ForeignKey(department,on_delete=models.CASCADE)
    fname=models.TextField(max_length=50)
    lname=models.TextField(max_length=50)
    d2d=models.TextField(max_length=10,default='No')


    def __str__(self):
        return str(self.fname) +" " + str(self.lname)+ " ( "+str(self.enroll_no)+" )" + str(" ") + str(self.d2d)







class scheme(models.Model):
    scheme_no=models.IntegerField(primary_key=True)
    theory_cr=models.IntegerField()
    practical_cr=models.IntegerField()
    max_th=models.IntegerField()
    max_pr=models.IntegerField()
    max_mid=models.IntegerField()
    min_th=models.IntegerField()
    min_pr=models.IntegerField()




    def __str__(self):
        return str(self.theory_cr) + " + " + str(self.practical_cr) + " ( " + str(self.scheme_no) + " ) "







class subjects(models.Model):
    sub_no=models.TextField(primary_key=True,max_length=20)
    sub_name=models.TextField(max_length=50,default="name")
    sub_dept_no=models.ForeignKey(department,on_delete=models.CASCADE)
    sub_scheme_no=models.ForeignKey(scheme,on_delete=models.CASCADE)
    sem=models.IntegerField()
    sub_stu_scheme=models.IntegerField()



    def __str__(self):
        return str(self.sub_name) +" ( " + str(self.sub_no)+ " )" +str(self.sub_dept_no)

    class Meta:
        constraints=[
        models.UniqueConstraint(fields=['sub_no','sub_dept_no','sem'],name='unique_subject')
        ]
        ordering=['sub_dept_no','sem','sub_no']
        # unique_together = (('sub_no', 'sub_dept_no','sem'),)




class marks(models.Model):
    marks_enroll_no=models.ForeignKey(student,on_delete=models.CASCADE)
    marks_sub_no=models.ForeignKey(subjects,on_delete=models.CASCADE)
    th=models.IntegerField()
    pr=models.IntegerField()
    mid=models.IntegerField()
    current_result=models.FloatField()
    current_cr=models.IntegerField(default=0)



    def __str__(self):
        return str(self.marks_enroll_no) +" ( " + str(self.marks_sub_no)+ " )"
    class Meta:
        unique_together = (('marks_enroll_no', 'marks_sub_no'),)

class backlog(models.Model):
    back_enroll_no=models.ForeignKey(student,on_delete=models.CASCADE)
    back_sub_no=models.ForeignKey(subjects,on_delete=models.PROTECT)
    status=models.TextField(max_length=30)






    def __str__(self):
        return str(self.back_enroll_no) +" ( " + str(self.back_sub_no)+ " ) " + str(self.status)
    class Meta:
        unique_together = (('back_enroll_no', 'back_sub_no'),)

class result(models.Model):
    result_enroll_no=models.ForeignKey(student,on_delete=models.CASCADE)
    sem1=models.FloatField(default=0)
    sem2=models.FloatField(default=0)
    sem3=models.FloatField(default=0)
    sem4=models.FloatField(default=0)
    sem5=models.FloatField(default=0)
    sem6=models.FloatField(default=0)
    sem7=models.FloatField(default=0)
    sem8=models.FloatField(default=0)
    ogpa=models.FloatField(default=0)
    previous_grades=models.FloatField(default=0)
    total_credits_hour=models.IntegerField(default=0)
    result_status=models.TextField(max_length=30,default='None')

    def __str__(self):
        return  str(self.result_enroll_no) + " Sem1 = " + str(self.sem1) + " Sem2 = " + str(self.sem2) + " Sem3 = " + str(self.sem3) + " Sem4 = " + str(self.sem4) + " Sem5 = " + str(self.sem5) + " Sem6 = " + str(self.sem6) + " Sem7 = " + str(self.sem7) + " Sem8 = " + str(self.sem8) + " OGPA = " + str(self.ogpa) +" Result Status = " +str(self.result_status)
