from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages


# Create your views here.
def home(request,error_message=''):
    #used to make dynamic options in forms
    dept_no_list = department.objects.all()
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
            #messages.add_message(request, messages.INFO, '')
            messages.error(request, 'Department Already Exist!!')
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
            messages.error(request,'Student Already Exist!!')
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
                messages.error(request,'Scheme Already Exixt!!')
                return redirect(home,error_message="Scheme Already Exist!!")

            sc_no=int(request.POST['scheme_no'])
            th_cr=int(request.POST['theory_cr'])
            pr_cr=int(request.POST['practical_cr'])

            if th_cr==1 and pr_cr==1 or th_cr==2 and pr_cr==1 or th_cr==2 and pr_cr==2 or th_cr==3 and pr_cr==1 or th_cr==3 and pr_cr==2:
                Scheme= scheme.objects.create(scheme_no=sc_no, theory_cr=th_cr,practical_cr=pr_cr,max_th='50',max_mid='20',max_pr='30',min_th='28',min_pr='12')

            elif th_cr==0 and pr_cr==1 or th_cr==0 and pr_cr==2 or th_cr==0 and pr_cr==3 or th_cr==0 and pr_cr==4:
                Scheme= scheme.objects.create(scheme_no=sc_no, theory_cr=th_cr,practical_cr=pr_cr,max_th='0',max_mid='20',max_pr='80',min_th='0',min_pr='40')


            elif th_cr==1 and pr_cr==0 or th_cr==2 and pr_cr==0 or th_cr==3 and pr_cr==0 or th_cr==4 and pr_cr==0:
                Scheme= scheme.objects.create(scheme_no=sc_no, theory_cr=th_cr,practical_cr=pr_cr,max_th='80',max_mid='20',max_pr='0',min_th='40',min_pr='0')

            elif th_cr==1 and pr_cr==2 or th_cr==1 and pr_cr==3 or th_cr==1 and pr_cr==4:
                Scheme= scheme.objects.create(scheme_no=sc_no, theory_cr=th_cr,practical_cr=pr_cr,max_th='30',max_mid='20',max_pr='50',min_th='12',min_pr='28')


            else:
                messages.error(request,'Enter a Valid Scheme')
                return redirect(home,error_message="Enter a Valid Scheme!!")

            return redirect('home')

        else:
                return redirect('home')


def sub_form(request):
    if request.method=='POST':
        string=''
        dept_no_obj=department.objects.get(dept_no=request.POST['sub_dept_no'])
        field_name_dept='dept_no'
        field_object_dept=department._meta.get_field(field_name_dept)
        dept_no=field_object_dept.value_from_object(dept_no_obj)
        string=str(request.POST['sub_no']) +str('') + str('/') + str(request.POST['student_scheme']) + str('/') + str(dept_no)

        if subjects.objects.filter(sub_no=string).filter(sub_dept_no=request.POST['sub_dept_no']).exists():
            messages.error(request,'Subject Already Exixt!!')
            return redirect(home,error_message="Subject Already Exist!!")

        else:
            Subject=subjects()

            Subject.sub_no=string
            Subject.sub_name=request.POST['sub_name']
            Subject.sub_stu_scheme=request.POST['student_scheme']
            sub_dept_no=request.POST['sub_dept_no']
            Subject.sub_dept_no=department.objects.get(dept_no=sub_dept_no)


            Subject.sub_scheme_no=scheme.objects.get(scheme_no=request.POST['sub_scheme_no'])
            Subject.sem=request.POST['Sem']

            Subject.save()
        return redirect('home')

    else:
       return redirect('home')

def marks_form(request):
        if request.method=='POST':
            if student.objects.filter(enroll_no=request.POST['marks_enroll_no']).exists():



                        if backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).exists() and backlog.objects.filter(back_sub_no=request.POST['marks_sub_no']).exists():

                                back_obj_enroll=backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no'])
                                back_obj=back_obj_enroll.get(back_sub_no__exact=request.POST['marks_sub_no'])
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

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).delete()

                                    if (int(request.POST['th']) + int(request.POST['mid']))>=28 and int(request.POST['pr'])<12:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Practical')

                                    if (int(request.POST['th']) + int(request.POST['mid']))<28 and int(request.POST['pr'])>=12:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Theory')

                                if th_cr==0 and pr_cr==1 or th_cr==0 and pr_cr==2 or th_cr==0 and pr_cr==3 or th_cr==0 and pr_cr==4:
                                    if int(request.POST['pr'])>=40:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).delete()
                                    if int(request.POST['pr'])<40:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Practical')


                                if th_cr==1 and pr_cr==0 or th_cr==2 and pr_cr==0 or th_cr==3 and pr_cr==0 or th_cr==4 and pr_cr==0:
                                    if (int(request.POST['th']) + int(request.POST['mid']))>=40:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).delete()
                                    if (int(request.POST['th']) + int(request.POST['mid']))<40:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Theory')

                                if th_cr==1 and pr_cr==2 or th_cr==1 and pr_cr==3 or th_cr==1 and pr_cr==4:
                                    if (int(request.POST['th']))>=12 or int(request.POST['pr'])>=28:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).delete()

                                    if (int(request.POST['th']))>=12 or int(request.POST['pr'])<28:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Practical')

                                    if (int(request.POST['th']))<12 or int(request.POST['pr'])>=28:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Theory')

                                back_result(request.POST['marks_enroll_no'])
                                messages.error(request,'BackLog subject updated for current student')
                                # return redirect(home,error_message='BackLog subject updated for current student')


                        else:
                                if marks.objects.filter(marks_sub_no=request.POST['marks_sub_no']).filter(marks_enroll_no=request.POST['marks_enroll_no']).exists():
                                    messages.error(request,'Marks Already Uploaded!!')
                                    return redirect(home,error_message="Marks Already Uploaded!!")

                                Marks=marks()

                                sub_obj=subjects.objects.get(sub_no=request.POST['marks_sub_no'])
                                field_name_subject='sub_no'
                                field_object_sub=subjects._meta.get_field(field_name_subject)
                                subject_no=str(field_object_sub.value_from_object(sub_obj))

                                sub_last_ele=(subject_no[0:6])

                                sub_sare_list=subjects.objects.all().filter(sub_no__contains=sub_last_ele)

                                student_roll=request.POST['marks_enroll_no']
                                student_start_four=int(student_roll[0:4])

                                min=5
                                subject_loop_obj=subjects()

                                for subject in sub_sare_list:

                                    field_name_subject_loop='sub_no'
                                    field_object_sub_loop=subjects._meta.get_field(field_name_subject_loop)
                                    subject_no=str(field_object_sub.value_from_object(subject))
                                    sub_last_four_int=int(subject_no[-6:-2])

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
                                    messages.error(request,"Insert Theory marks according to Used Scheme!!")
                                    return redirect(home,error_message="Insert Theory marks according to Used Scheme!!")
                                if int(scheme_obj.max_pr)>=int(request.POST['pr']):
                                    Marks.pr=request.POST['pr']
                                else:
                                    messages.error(request,"Insert Practical marks according to Used Scheme!!")
                                    return redirect(home,error_message="Insert Practical marks according to Used Scheme!!")
                                if int(scheme_obj.max_mid)>=int(request.POST['mid']):
                                    Marks.mid=request.POST['mid']
                                else:
                                    messages.error(request,"Insert Mid-Term marks according to Used Scheme!!")
                                    return redirect(home,error_message="Insert Mid-Term marks according to Used Scheme!!")


                                result=(th_cr + pr_cr) * (int(request.POST['th']) + int(request.POST['pr']) + int(request.POST['mid']))/10
                                Marks.current_result=result

                                if th_cr==1 and pr_cr==1 or th_cr==2 and pr_cr==1 or th_cr==2 and pr_cr==2 or th_cr==3 and pr_cr==1 or th_cr==3 and pr_cr==2:
                                    if (int(request.POST['th']) + int(request.POST['mid']))<28 and int(request.POST['pr'])<12:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='back in both Theory & Practical'
                                        back.save()
                                    if (int(request.POST['th']) + int(request.POST['mid']))<28 and int(request.POST['pr'])>12:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='back in Theory'
                                        back.save()
                                    if (int(request.POST['th']) + int(request.POST['mid']))>28 and int(request.POST['pr'])<12:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='back in Practical'
                                        back.save()

                                if th_cr==0 and pr_cr==1 or th_cr==0 and pr_cr==2 or th_cr==0 and pr_cr==3 or th_cr==0 and pr_cr==4:
                                    if int(request.POST['pr'])<40:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='back in Practical'
                                        back.save()

                                if th_cr==1 and pr_cr==0 or th_cr==2 and pr_cr==0 or th_cr==3 and pr_cr==0 or th_cr==4 and pr_cr==0:
                                    if (int(request.POST['th']) + int(request.POST['mid']))<40:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='back in Theory'
                                        back.save()

                                if th_cr==1 and pr_cr==2 or th_cr==1 and pr_cr==3 or th_cr==1 and pr_cr==4:
                                    if (int(request.POST['th']))<12 and int(request.POST['pr'])<28:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='back in both Theory & Practical'
                                        back.save()
                                    if (int(request.POST['th']))<12 and int(request.POST['pr'])>28:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='back in Theory'
                                        back.save()
                                    if (int(request.POST['th']))>12 and int(request.POST['pr'])<28:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='back in Practical'
                                        back.save()

                                Marks.save()

                        subject1,sem_id=no_marks(request.POST['marks_enroll_no'])
                        mark_subject=marks.objects.filter(marks_enroll_no=request.POST['marks_enroll_no']).order_by('marks_sub_no')
                        mark_update_list=[]
                        for mark in mark_subject:
                            field_name='marks_sub_no'
                            field_object=marks._meta.get_field(field_name)
                            mark_sub=str(field_object.value_from_object(mark))
                            if mark_sub[-8] in ['a' , 'b' , 'c' , 'd' , 'e'] :
                                str2=mark_sub[0:5]
                                subs=subjects.objects.filter(sub_no__contains=str2)
                                for sub in subs:
                                    mark_update_list.append(sub.sub_no)

                            else:
                                mark_update_list.append(mark_sub)
                        subject2=[]
                        for sub in subject1:
                            if str(sub.sub_no) not in mark_update_list:
                                subject2.append(sub.sub_no)
                        enroll=request.POST['marks_enroll_no']
                        student_dept=student.objects.get(enroll_no=enroll)
                        subject=subjects.objects.filter(sub_no__in=subject2)
                        final_query=subject
                        if backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).exists():
                            if sem_id>=3:
                                for i in range(sem_id,1,-2):
                                    sub=subjects.objects.filter(sub_dept_no=student_dept.student_dept_no).filter(sem=i-2).order_by('sub_no')
                                    back_sub=backlog.objects.filter(back_enroll_no=str(enroll)).filter(back_sub_no__in=sub)
                                    back_sub_list=[]
                                    for back in back_sub:
                                        field_name='back_sub_no'
                                        field_object=backlog._meta.get_field(field_name)
                                        back_in=str(field_object.value_from_object(back))
                                        back_sub_list.append(back_in)
                                    join_obj=subjects.objects.filter(sub_no__in=back_sub_list).filter(sem=i-2).filter(sub_dept_no=student_dept.student_dept_no).order_by('sub_no')
                                    final_query=final_query | join_obj

                        if len(subject)!=0:

                            return render(request,'job/marks_detail.html',{'subject':subject,'enroll':enroll})
                        else:
                            return redirect('home')


            else:
                    # return redirect(home,error_message="Student Does Not Exist!!")
                    messages.error(request,'student not')

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
                        sub_last_four_int=int(sub_code_str[-6:-2])
                        if sub_last_four_int not in sub_last_four_list:
                            sub_last_four_list.append(sub_last_four_int)
                    min=5
                    scheme_year=0
                    for list in sub_last_four_list:
                        if (student_start_four-list)<min:
                            min=student_start_four-list
                            scheme_year=list
                    str_scheme_year=str(scheme_year)
                    stu_dept_no_1=student.objects.get(enroll_no=request.POST['result_enroll'])
                    sub_count_obj=subjects.objects.filter(sub_no__contains=str_scheme_year).filter(sem=request.POST['Sem']).filter(sub_dept_no=(stu_dept_no_1.student_dept_no))
                    count=0
                    count_str=[]
                    for sub in sub_count_obj:
                        str1=str(sub.sub_no)
                        if str1[-8] in ['a' , 'b' , 'c' , 'd' , 'e'] :
                            str2=str1[0:5]
                            if str2 not in count_str:
                                count_str.append(str2)
                                count+=1
                        else:
                            count+=1
                    marks_count_obj=marks.objects.filter(marks_sub_no__sub_no__contains=str_scheme_year).filter(marks_sub_no__in=sub_count_obj).filter(marks_enroll_no=request.POST['result_enroll'])

                    mark_obj_list=[]
                    for mark_count in marks_count_obj:
                        field_name_mark='marks_sub_no'
                        field_object_mark=marks._meta.get_field(field_name_mark)
                        mark_sub_no=field_object_mark.value_from_object(mark_count)
                        if subjects.objects.filter(sub_no=mark_sub_no).filter(sem=request.POST['Sem']).filter(sub_dept_no=(stu_dept_no_1.student_dept_no)):
                            mark_obj_list.append(mark_count)

                    if len(mark_obj_list)!=count:
                        messages.error(request,"Result in under progress !! Thank You")
                        return redirect(home,error_message="Result in under progress !! Thank You")


                    student_object=student.objects.get(enroll_no=request.POST['result_enroll'])

                    field_name_roll='enroll_no'
                    field_object_result=student._meta.get_field(field_name_roll)
                    roll_no=field_object_result.value_from_object(student_object)

                    sub_no_obj=subjects.objects.all().filter(sub_no__contains=scheme_year).filter(sem=request.POST['Sem']).filter(sub_dept_no=(stu_dept_no_1.student_dept_no))

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

                    fnl_result=round(float(result_sum/(result_cr)),2)

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
                                sem_1=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_1)

                        elif int(request.POST['Sem'])==2:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem2=fnl_result)
                                sem_2=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_2)

                        elif int(request.POST['Sem'])==3:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem3=fnl_result)
                                sem_3=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_3)
                        elif int(request.POST['Sem'])==4:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem4=fnl_result)
                                sem_4=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_4)
                        elif int(request.POST['Sem'])==5:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem5=fnl_result)
                                sem_5=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_5)
                        elif int(request.POST['Sem'])==6:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem6=fnl_result)
                                sem_6=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_6)
                        elif int(request.POST['Sem'])==7:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem7=fnl_result)
                                sem_7=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_7)
                        elif int(request.POST['Sem'])==8:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem8=fnl_result)
                                sem_8=round((current_res)/(current_cr_for),2)
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

                        messages.error(request,'Student Doed Not Exist')
                        return redirect(home,error_message="Student Does Not Exist!!")

    else:
            return redirect('home')




def verify_enroll(request):
    if request.method=='POST':
        if student.objects.filter(enroll_no=request.POST['marks_enroll_no']).exists():
            subject,sem_id=no_marks(request.POST['marks_enroll_no'])
            enroll=request.POST['marks_enroll_no']
            return render(request,'job/marks_detail.html',{'subject':subject,'enroll':enroll})
        else:
            messages.error(request,'Student Does Not Exist.')
            return redirect(home,error_message="Student Does Not Exist!!")
    return render(request,'job/verify_enroll.html')


def no_marks(enroll=''):
        student_dept=student.objects.get(enroll_no=enroll)
        if result.objects.filter(result_enroll_no=str(enroll)).exists():
            results=result.objects.get(result_enroll_no=str(enroll))
            sem_id=0
            if results.sem1==0:
                sem_id=1
            elif results.sem2==0:
                sem_id=2
            elif results.sem3==0:
                sem_id=3
            elif results.sem4==0:
                sem_id=4
            elif results.sem5==0:
                sem_id=5
            elif results.sem6==0:
                sem_id=6
            elif results.sem7==0:
                sem_id=7
            elif results.sem8==0:
                sem_id=8
        else:
            sem_id=1
        stu_four=int(enroll[0:4])
        subject1=subjects.objects.filter(sub_dept_no=student_dept.student_dept_no).filter(sem=sem_id).order_by('sub_no')
        sub_scheme_year=[]
        for sub in subject1:
            field_name='sub_no'
            field_object=subjects._meta.get_field(field_name)
            four=str(field_object.value_from_object(sub))
            four_digit=int(four[-6:-2])
            if four_digit not in sub_scheme_year:
                sub_scheme_year.append(four_digit)
        min=5
        sub_scheme_year_final=0
        for sub_scheme in sub_scheme_year:
            if int(stu_four-sub_scheme)<min:
                min=stu_four-sub_scheme
                sub_scheme_year_final=sub_scheme
        subject=subjects.objects.filter(sub_dept_no=student_dept.student_dept_no).filter(sem=sem_id).filter(sub_no__contains=str(sub_scheme_year_final))
        final_query=subject
        if backlog.objects.filter(back_enroll_no=str(enroll)).exists():
            if sem_id>=3:
                for i in range(sem_id,1,-2):
                    sub=subjects.objects.filter(sub_dept_no=student_dept.student_dept_no).filter(sem=i-2).order_by('sub_no')
                    back_sub=backlog.objects.filter(back_enroll_no=str(enroll)).filter(back_sub_no__in=sub)

                    back_sub_list=[]
                    for back in back_sub:
                        field_name='back_sub_no'
                        field_object=backlog._meta.get_field(field_name)
                        back_in=str(field_object.value_from_object(back))
                        back_sub_list.append(back_in)
                    join_obj=subjects.objects.filter(sub_no__in=back_sub_list).filter(sem=i-2).filter(sub_dept_no=student_dept.student_dept_no).order_by('sub_no')
                    final_query=final_query | join_obj
        return (final_query,sem_id)







def back_result(enroll=''):
    result_obj=result.objects.get(result_enroll_no=enroll)
    student_obj=student.objects.get(enroll_no=enroll)
    sem_id=0
    if result_obj.sem1==0:
        sem_id=1
    elif result_obj.sem2==0:
        sem_id=2
    elif result_obj.sem3==0:
        sem_id=3
    elif result_obj.sem4==0:
        sem_id=4
    elif result_obj.sem5==0:
        sem_id=5
    elif result_obj.sem6==0:
        sem_id=6
    elif result_obj.sem7==0:
        sem_id=7
    elif result_obj.sem8==0:
        sem_id=8
    for i in range(1,sem_id,1):
        subject_obj=subjects.objects.filter(sub_dept_no=student_obj.student_dept_no).filter(sem=i).order_by('sub_no')
        marks_obj=marks.objects.filter(marks_sub_no__in=subject_obj).filter(marks_enroll_no=enroll)
        results=0.0
        crs=0
        for mark in marks_obj:
            results+=float(mark.current_result)
            crs+=int(mark.current_cr)
        current_res=round(float(results/(crs)),2)
        if result_obj.sem1!=0:
                if i==1:
                    result.objects.filter(result_enroll_no=enroll).update(sem1=current_res)
                    result.objects.filter(result_enroll_no=enroll).update(previous_grades=results)
                    result.objects.filter(result_enroll_no=enroll).update(total_credits_hour=crs )
                    result.objects.filter(result_enroll_no=enroll).update(ogpa=current_res)
        if result_obj.sem2!=0:
                if i==2:
                    result_update=result.objects.get(result_enroll_no=enroll)
                    result.objects.filter(result_enroll_no=enroll).update(sem2=current_res)
                    result.objects.filter(result_enroll_no=enroll).update(previous_grades=(results + float(result_update.previous_grades)))
                    result.objects.filter(result_enroll_no=enroll).update(total_credits_hour=(crs + int(result_update.total_credits_hour)))
                    result_ogpa=result.objects.get(result_enroll_no=enroll)
                    sem_2=round(float(result_ogpa.previous_grades)/int((result_ogpa.total_credits_hour)),2)
                    result.objects.filter(result_enroll_no=enroll).update(ogpa=sem_2)
        if result_obj.sem3!=0:
                if i==3:
                    result_update=result.objects.get(result_enroll_no=enroll)
                    result.objects.filter(result_enroll_no=enroll).update(sem3=current_res)
                    result.objects.filter(result_enroll_no=enroll).update(previous_grades=(results + float(result_update.previous_grades)))
                    result.objects.filter(result_enroll_no=enroll).update(total_credits_hour=(crs + int(result_update.total_credits_hour)))
                    result_ogpa=result.objects.get(result_enroll_no=enroll)
                    sem_3=round(float(result_ogpa.previous_grades)/int((result_ogpa.total_credits_hour)),2)
                    result.objects.filter(result_enroll_no=enroll).update(ogpa=sem_3)
        if result_obj.sem4!=0:
                if i==4:
                    result_update=result.objects.get(result_enroll_no=enroll)
                    result.objects.filter(result_enroll_no=enroll).update(sem4=current_res)
                    result.objects.filter(result_enroll_no=enroll).update(previous_grades=(results + float(result_update.previous_grades)))
                    result.objects.filter(result_enroll_no=enroll).update(total_credits_hour=(crs + int(result_update.total_credits_hour)))
                    result_ogpa=result.objects.get(result_enroll_no=enroll)
                    sem_4=round(float(result_ogpa.previous_grades)/int((result_ogpa.total_credits_hour)),2)
                    result.objects.filter(result_enroll_no=enroll).update(ogpa=sem_4)
        if result_obj.sem5!=0:
                if i==5:
                    result_update=result.objects.get(result_enroll_no=enroll)
                    result.objects.filter(result_enroll_no=enroll).update(sem5=current_res)
                    result.objects.filter(result_enroll_no=enroll).update(previous_grades=(results + float(result_update.previous_grades)))
                    result.objects.filter(result_enroll_no=enroll).update(total_credits_hour=(crs + int(result_update.total_credits_hour)))
                    result_ogpa=result.objects.get(result_enroll_no=enroll)
                    sem_5=round(float(result_ogpa.previous_grades)/int((result_ogpa.total_credits_hour)),2)
                    result.objects.filter(result_enroll_no=enroll).update(ogpa=sem_5)
        if result_obj.sem6!=0:
                if i==6:
                    result_update=result.objects.get(result_enroll_no=enroll)
                    result.objects.filter(result_enroll_no=enroll).update(sem6=current_res)
                    result.objects.filter(result_enroll_no=enroll).update(previous_grades=(results + float(result_update.previous_grades)))
                    result.objects.filter(result_enroll_no=enroll).update(total_credits_hour=(crs + int(result_update.total_credits_hour)))
                    result_ogpa=result.objects.get(result_enroll_no=enroll)
                    sem_6=round(float(result_ogpa.previous_grades)/int((result_ogpa.total_credits_hour)),2)
                    result.objects.filter(result_enroll_no=enroll).update(ogpa=sem_6)
        if result_obj.sem7!=0:
                if i==7:
                    result_update=result.objects.get(result_enroll_no=enroll)
                    result.objects.filter(result_enroll_no=enroll).update(sem7=current_res)
                    result.objects.filter(result_enroll_no=enroll).update(previous_grades=(results + float(result_update.previous_grades)))
                    result.objects.filter(result_enroll_no=enroll).update(total_credits_hour=(crs + int(result_update.total_credits_hour)))
                    result_ogpa=result.objects.get(result_enroll_no=enroll)
                    sem_7=round(float(result_ogpa.previous_grades)/int((result_ogpa.total_credits_hour)),2)
                    result.objects.filter(result_enroll_no=enroll).update(ogpa=sem_7)
        if result_obj.sem8!=0:
                if i==8:
                    result_update=result.objects.get(result_enroll_no=enroll)
                    result.objects.filter(result_enroll_no=enroll).update(sem8=current_res)
                    result.objects.filter(result_enroll_no=enroll).update(previous_grades=(results + float(result_update.previous_grades)))
                    result.objects.filter(result_enroll_no=enroll).update(total_credits_hour=(crs + int(result_update.total_credits_hour)))
                    result_ogpa=result.objects.get(result_enroll_no=enroll)
                    sem_8=round(float(result_ogpa.previous_grades)/int((result_ogpa.total_credits_hour)),2)
                    result.objects.filter(result_enroll_no=enroll).update(ogpa=sem_8)
