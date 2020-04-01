from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *


# Create your views here.
def home(request,error_message=''):
    #used to make dynamic options in forms
    dept_no_list = department.objects.all().order_by('dept_no')
    scheme_no_list=scheme.objects.all()
    sub_no_list=subjects.objects.all().order_by('sub_no')

    context = {
    'scheme_no_list': scheme_no_list,
    'dept_no_list': dept_no_list,
    'sub_no_list' : sub_no_list,
    'error_message':error_message,


 }
    return render(request,'job/home.html', context)

def dept_form(request):
    if request.method=='POST':
        if department.objects.filter(dept_no=request.POST['dept_no']).exists():
            return redirect(home,error_message="Department Already Exist!!")
        Department=department()
        Department.dept_name=request.POST['dept_name']
        Department.dept_no=request.POST['dept_no']
        Department.save()
        return redirect('home')

    else:
       return redirect('home')

def student_form(request):
    if request.method=='POST':
        if student.objects.filter(enroll_no=request.POST['enroll_no']).exists():
            return redirect(home,error_message="Student Already Exist!!")

        Student=student()
        Student.fname=request.POST['fname']
        Student.lname=request.POST['lname']
        Student.enroll_no=request.POST['enroll_no']
        student_dept_no=request.POST['student_dept_no']
        Student.student_dept_no=department.objects.get(dept_no=student_dept_no)

        Student.save()
        return redirect('home')

    else:
       return redirect('home')

def scheme_form(request):

        if request.method=='POST':
            if  scheme.objects.filter(scheme_no=request.POST['scheme_no']).exists():
                return redirect(home,error_message="Scheme Already Exist!!")

            sc_no=int(request.POST['scheme_no'])
            th_cr=int(request.POST['theory_cr'])
            pr_cr=int(request.POST['practical_cr'])

            if th_cr==1 and pr_cr==1 or th_cr==2 and pr_cr==1 or th_cr==2 and pr_cr==2 or th_cr==3 and pr_cr==1 or th_cr==3 and pr_cr==2:
                Scheme= scheme.objects.create(scheme_no=sc_no, theory_cr=th_cr,practical_cr=pr_cr,max_th='50',max_mid='20',max_pr='30')

            elif th_cr==0 and pr_cr==1 or th_cr==0 and pr_cr==2 or th_cr==0 and pr_cr==3 or th_cr==0 and pr_cr==4:
                Scheme= scheme.objects.create(scheme_no=sc_no, theory_cr=th_cr,practical_cr=pr_cr,max_th='0',max_mid='20',max_pr='80')


            elif th_cr==1 and pr_cr==0 or th_cr==2 and pr_cr==0 or th_cr==3 and pr_cr==0 or th_cr==4 and pr_cr==0:
                Scheme= scheme.objects.create(scheme_no=sc_no, theory_cr=th_cr,practical_cr=pr_cr,max_th='80',max_mid='20',max_pr='0')

            elif th_cr==1 and pr_cr==2 or th_cr==1 and pr_cr==3 or th_cr==1 and pr_cr==4:
                Scheme= scheme.objects.create(scheme_no=sc_no, theory_cr=th_cr,practical_cr=pr_cr,max_th='30',max_mid='20',max_pr='50')


            else:
                return redirect(home,error_message="Enter a Valid Scheme!!")

            return redirect('home')

        else:
                return redirect('home')


def sub_form(request):
    if request.method=='POST':
        string=''
        string=str(request.POST['sub_no']) + str('/') + str(request.POST['student_scheme'])

        if subjects.objects.filter(sub_no=string).exists():
            return redirect(home,error_message="Subject Already Exist!!")


        Subject=subjects()
        Subject.sub_no=string
        Subject.sub_name=request.POST['sub_name']
        Subject.sub_stu_scheme=request.POST['student_scheme']
        sub_dept_no=request.POST['sub_dept_no']
        Subject.sub_dept_no=department.objects.get(dept_no=sub_dept_no)
        sub_scheme_no=request.POST['sub_scheme_no']
        Subject.sub_scheme_no=scheme.objects.get(scheme_no=sub_scheme_no)
        Subject.sem=request.POST['Sem']
        Subject.save()
        return redirect('home')

    else:
       return redirect('home')

def marks_form(request):
        if request.method=='POST':
            if student.objects.filter(enroll_no=request.POST['marks_enroll_no']).exists():

                        if marks.objects.filter(marks_sub_no=request.POST['marks_sub_no']).exists():
                            return redirect(home,error_message="Marks Already Uploaded!!")

                        if backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).exists() and backlog.objects.filter(back_sub_no=request.POST['marks_sub_no']).exists():

                                back_obj=backlog.objects.get(back_enroll_no=request.POST['marks_enroll_no'])
                                field_name_back_sub='back_sub_no'
                                back_log_object=backlog._meta.get_field(field_name_back_sub)
                                back_log_sub_code=back_log_object.value_from_object(back_obj)



                                marks_sub_no=request.POST['marks_sub_no']
                                sub_scheme_obj=subjects.objects.get(sub_no=marks_sub_no)

                                field_name='sub_scheme_no'
                                field_object=subjects._meta.get_field(field_name)
                                scheme_id=field_object.value_from_object(sub_scheme_obj)

                                scheme_obj=scheme.objects.get(scheme_no=scheme_id)

                                field_name_th='theory_cr'
                                field_object_th=scheme._meta.get_field(field_name_th)
                                th_cr=field_object_th.value_from_object(scheme_obj)

                                field_name_pr='practical_cr'
                                field_object_pr=scheme._meta.get_field(field_name_pr)
                                pr_cr=field_object_pr.value_from_object(scheme_obj)

                                mark_back_obj=marks.objects.filter(marks_enroll_no=request.POST['marks_enroll_no']).filter(marks_sub_no=back_log_sub_code)
                                mark_back_obj.update(th=request.POST['th'])
                                mark_back_obj.update(pr=request.POST['pr'])
                                mark_back_obj.update(mid=request.POST['mid'])


                                result=(th_cr + pr_cr) * (int(request.POST['th']) + int(request.POST['pr']) + int(request.POST['mid']))/10
                                mark_back_obj.update(current_result=result)




                                if th_cr==1 and pr_cr==1 or th_cr==2 and pr_cr==1 or th_cr==2 and pr_cr==2 or th_cr==3 and pr_cr==1 or th_cr==3 and pr_cr==2:
                                    if (int(request.POST['th']) + int(request.POST['mid']))>=28 and int(request.POST['pr'])>=12:


                                        backlog.objects.get(back_enroll_no=request.POST['marks_enroll_no']).delete()



                                if th_cr==0 and pr_cr==1 or th_cr==0 and pr_cr==2 or th_cr==0 and pr_cr==3 or th_cr==0 and pr_cr==4:
                                    if int(request.POST['pr'])>=40:


                                        backlog.objects.get(back_enroll_no=request.POST['marks_enroll_no']).delete()


                                if th_cr==1 and pr_cr==0 or th_cr==2 and pr_cr==0 or th_cr==3 and pr_cr==0 or th_cr==4 and pr_cr==0:
                                    if (int(request.POST['th']) + int(request.POST['mid']))>=40:


                                        backlog.objects.get(back_enroll_no=request.POST['marks_enroll_no']).delete()


                                if th_cr==1 and pr_cr==2 or th_cr==1 and pr_cr==3 or th_cr==1 and pr_cr==4:
                                    if (int(request.POST['th']))>=12 or int(request.POST['pr'])>=28:


                                        backlog.objects.get(back_enroll_no=request.POST['marks_enroll_no']).delete()


                                return redirect(home,error_message='BackLog subject updated for current student')




                        else:
                                Marks=marks()

                                sub_obj=subjects.objects.get(sub_no=request.POST['marks_sub_no'])
                                field_name_subject='sub_no'
                                field_object_sub=subjects._meta.get_field(field_name_subject)
                                subject_no=str(field_object_sub.value_from_object(sub_obj))

                                sub_last_ele=(subject_no[0:5])

                                sub_sare_list=subjects.objects.all().filter(sub_no__contains=sub_last_ele)



                                student_roll=request.POST['marks_enroll_no']
                                student_start_four=int(student_roll[0:4])


                                min=5
                                subject_loop_obj=subjects()

                                for subject in sub_sare_list:



                                    field_name_subject_loop='sub_no'
                                    field_object_sub_loop=subjects._meta.get_field(field_name_subject_loop)
                                    subject_no=str(field_object_sub.value_from_object(subject))
                                    sub_last_four_int=int(subject_no[-4:])



                                    if (student_start_four-sub_last_four_int)<min:
                                        min=(student_start_four-sub_last_four_int)
                                        subject_loop_obj=subject







                                field_name_sub_no='sub_no'
                                field_object_sub_no=subjects._meta.get_field(field_name_sub_no)
                                sub_id=field_object_sub_no.value_from_object(subject_loop_obj)


                                Marks.marks_sub_no=subjects.objects.get(sub_no=sub_id)
                                sub_scheme_obj=subjects.objects.get(sub_no=sub_id)

                                field_name='sub_scheme_no'
                                field_object=subjects._meta.get_field(field_name)
                                scheme_id=field_object.value_from_object(sub_scheme_obj)

                                scheme_obj=scheme.objects.get(scheme_no=scheme_id)

                                field_name_th='theory_cr'
                                field_object_th=scheme._meta.get_field(field_name_th)
                                th_cr=field_object_th.value_from_object(scheme_obj)

                                field_name_pr='practical_cr'
                                field_object_pr=scheme._meta.get_field(field_name_pr)
                                pr_cr=field_object_pr.value_from_object(scheme_obj)

                                total_cr=th_cr + pr_cr
                                Marks.current_cr=total_cr

                                marks_enroll_no=request.POST['marks_enroll_no']
                                Marks.marks_enroll_no=student.objects.get(enroll_no=marks_enroll_no)

                                if int(scheme_obj.max_th)>=int(request.POST['th']):
                                    Marks.th=request.POST['th']
                                else:
                                    return redirect(home,error_message="Insert Theory marks according to Used Scheme!!")
                                if int(scheme_obj.max_pr)>=int(request.POST['pr']):
                                    Marks.th=request.POST['pr']
                                else:
                                    return redirect(home,error_message="Insert Practical marks according to Used Scheme!!")
                                if int(scheme_obj.max_mid)>=int(request.POST['mid']):
                                    Marks.th=request.POST['mid']
                                else:
                                    return redirect(home,error_message="Insert Mid-Term marks according to Used Scheme!!")


                                result=(th_cr + pr_cr) * (int(Marks.th) + int(Marks.pr) + int(Marks.mid))/10
                                Marks.current_result=result

                                if th_cr==1 and pr_cr==1 or th_cr==2 and pr_cr==1 or th_cr==2 and pr_cr==2 or th_cr==3 and pr_cr==1 or th_cr==3 and pr_cr==2:
                                    if (int(Marks.th) + int(Marks.mid))<28 or int(Marks.pr)<12:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.save()

                                if th_cr==0 and pr_cr==1 or th_cr==0 and pr_cr==2 or th_cr==0 and pr_cr==3 or th_cr==0 and pr_cr==4:
                                    if int(Marks.pr)<40:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.save()

                                if th_cr==1 and pr_cr==0 or th_cr==2 and pr_cr==0 or th_cr==3 and pr_cr==0 or th_cr==4 and pr_cr==0:
                                    if (int(Marks.th) + int(Marks.mid))<40:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.save()

                                if th_cr==1 and pr_cr==2 or th_cr==1 and pr_cr==3 or th_cr==1 and pr_cr==4:
                                    if (int(Marks.th))<12 or int(Marks.pr)<28:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.save()

                                Marks.save()
                                return redirect('home')
            else:
                    return redirect(home,error_message="Student Does Not Exist!!")

        else:
                return render(request,'job/home.html',context)





def result_form(request):
    if request.method=='POST':
        if student.objects.filter(enroll_no=request.POST['result_enroll']).exists():

                    student_roll=str(request.POST['result_enroll'])
                    student_start_four=int(student_roll[0:4])


                    sub_list=subjects.objects.filter(sem=request.POST['Sem'])

                    sub_last_four_list=[]
                    for sub in sub_list:
                        sub_code_str=str(sub.sub_no)
                        sub_last_four_int=int(sub_code_str[-4:])
                        if sub_last_four_int not in sub_last_four_list:
                            sub_last_four_list.append(sub_last_four_int)


                    min=5
                    scheme_year=0
                    for list in sub_last_four_list:
                        if (student_start_four-list)<min:
                            min=student_start_four-list
                            scheme_year=list



                    str_scheme_year=str(scheme_year)

                    sub_count_obj=subjects.objects.filter(sub_no__contains=str_scheme_year).filter(sem=request.POST['Sem'])

                    marks_count_obj=marks.objects.filter(marks_sub_no__sub_no__contains=str_scheme_year)

                    mark_obj_list=[]
                    for mark_count in marks_count_obj:
                        field_name_mark='marks_sub_no'
                        field_object_mark=marks._meta.get_field(field_name_mark)
                        mark_sub_no=field_object_mark.value_from_object(mark_count)
                        if subjects.objects.filter(sub_no=mark_sub_no).filter(sem=request.POST['Sem']):
                            mark_obj_list.append(mark_count)


                    if len(mark_obj_list)!=len(sub_count_obj):
                        return redirect(home,error_message="Result in under progress !! Thank You")


                    student_object=student.objects.get(enroll_no=request.POST['result_enroll'])

                    field_name_roll='enroll_no'
                    field_object_result=student._meta.get_field(field_name_roll)
                    roll_no=field_object_result.value_from_object(student_object)




                    result_sem_no=request.POST['Sem']
                    sub_no_obj=subjects.objects.all().filter(sem=result_sem_no)

                    Marks=marks.objects.all().filter(marks_enroll_no=roll_no).filter(marks_sub_no__in=sub_no_obj)
                    result_sum=0
                    result_cr=0
                    result_t=0
                    crs=0
                    for mark in Marks:
                        field_name_current_result='current_result'
                        field_object_current_result=marks._meta.get_field(field_name_current_result)
                        result_t=field_object_current_result.value_from_object(mark)

                        result_sum+=result_t

                        field_name_current_cr='current_cr'
                        field_object_current_cr=marks._meta.get_field(field_name_current_cr)
                        crs=field_object_current_cr.value_from_object(mark)

                        result_cr+=crs

                    fnl_result=float(result_sum/(result_cr))
                    if result.objects.filter(result_enroll_no=request.POST['result_enroll']).exists():

                        res_obj_res=result.objects.get(result_enroll_no=request.POST['result_enroll'])
                        previous_res=float(res_obj_res.previous_grades)
                        current_res=previous_res + result_sum
                        result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(previous_grades=current_res)
                        previous_cr=int(res_obj_res.total_credits_hour)
                        current_cr_for=previous_cr + result_cr
                        result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(total_credits_hour=current_cr_for)



                    if result.objects.filter(result_enroll_no=roll_no).exists():
                        res_obj=result.objects.get(result_enroll_no=request.POST['result_enroll'])



                        if int(request.POST['Sem'])==1:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem1=fnl_result)
                                sem_1=(current_res)/(current_cr_for)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_1)

                        elif int(request.POST['Sem'])==2:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem2=fnl_result)
                                sem_2=(current_res)/(current_cr_for)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_2)

                        elif int(request.POST['Sem'])==3:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem3=fnl_result)
                                sem_3=(current_res)/(current_cr_for)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_3)
                        elif int(request.POST['Sem'])==4:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem4=fnl_result)
                                sem_4=(current_res)/(current_cr_for)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_4)
                        elif int(request.POST['Sem'])==5:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem5=fnl_result)
                                sem_5=(current_res)/(current_cr_for)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_5)
                        elif int(request.POST['Sem'])==6:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem6=fnl_result)
                                sem_6=(current_res)/(current_cr_for)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_6)
                        elif int(request.POST['Sem'])==7:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem7=fnl_result)
                                sem_7=(current_res)/(current_cr_for)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_7)
                        elif int(request.POST['Sem'])==8:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem8=fnl_result)
                                sem_8=(current_res)/(current_cr_for)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_8)


                    else:
                                final_result=result()
                                final_result.result_enroll_no=student.objects.get(enroll_no=request.POST['result_enroll'])
                                final_result.sem1=fnl_result
                                final_result.ogpa=fnl_result
                                final_result.previous_grades=result_sum
                                final_result.total_credits_hour=result_cr
                                final_result.save()

                    return redirect('home')
        else:
                        return redirect(home,error_message="Student Does Not Exist!!")

    else:
            return redirect('home')
