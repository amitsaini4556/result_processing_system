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
        if 'stu_dtod' in request.POST:
            result_obj=result()
            result_obj.result_enroll_no=student.objects.get(enroll_no=request.POST['enroll_no'])
            result_obj.sem1=1
            result_obj.sem2=1
            result_obj.save()
            student.objects.filter(enroll_no=request.POST['enroll_no']).update(d2d="Yes")


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



                        if backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).filter(status__contains='Back').exists() :

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

                                result1=(th_cr + pr_cr) * (int(request.POST['th']) + int(request.POST['pr']) + int(request.POST['mid']))/10
                                mark_back_obj.update(current_result=result1)

                                if th_cr==1 and pr_cr==1 or th_cr==2 and pr_cr==1 or th_cr==2 and pr_cr==2 or th_cr==3 and pr_cr==1 or th_cr==3 and pr_cr==2:
                                    if (int(request.POST['th']) + int(request.POST['mid']))>=28 and int(request.POST['pr'])>=12:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Clear')

                                    if (int(request.POST['th']) + int(request.POST['mid']))>=28 and int(request.POST['pr'])<12:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Practical')


                                    if (int(request.POST['th']) + int(request.POST['mid']))<28 and int(request.POST['pr'])>=12:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Theory')

                                if th_cr==0 and pr_cr==1 or th_cr==0 and pr_cr==2 or th_cr==0 and pr_cr==3 or th_cr==0 and pr_cr==4:
                                    if int(request.POST['pr'])>=40:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Clear')
                                    if int(request.POST['pr'])<40:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Practical')


                                if th_cr==1 and pr_cr==0 or th_cr==2 and pr_cr==0 or th_cr==3 and pr_cr==0 or th_cr==4 and pr_cr==0:
                                    if (int(request.POST['th']) + int(request.POST['mid']))>=40:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Clear')
                                    if (int(request.POST['th']) + int(request.POST['mid']))<40:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Theory')

                                if th_cr==1 and pr_cr==2 or th_cr==1 and pr_cr==3 or th_cr==1 and pr_cr==4:
                                    if (int(request.POST['th']))>=12 or int(request.POST['pr'])>=28:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Clear')

                                    if (int(request.POST['th']))>=12 or int(request.POST['pr'])<28:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Practical')

                                    if (int(request.POST['th']))<12 or int(request.POST['pr'])>=28:

                                        backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).filter(back_sub_no=request.POST['marks_sub_no']).update(status='Back in Theory')

                                back_result(request.POST['marks_enroll_no'])
                                sub_sem=subjects.objects.get(sub_no=request.POST['marks_sub_no'])
                                from .models import result
                                result_check=result.objects.get(result_enroll_no=request.POST['marks_enroll_no'])
                                if str(result_check.result_status)=='Year Back':
                                    count=0
                                    count=int(request.POST['count'])+1
                                    back=backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).get(back_sub_no=request.POST['marks_sub_no'])
                                    if back.status=='Clear':
                                        count-=1
                                    subject,sem_id=no_marks(request.POST['marks_enroll_no'])
                                    if len(subject)==count:
                                        result.objects.filter(result_enroll_no=request.POST['marks_enroll_no']).update(result_status='Next Sem')
                                        return redirect('home')
                                    enroll=request.POST['marks_enroll_no']
                                    return render(request,'job/marks_detail.html',{'subject':subject,'enroll':enroll,'count':count})

                                if int(sub_sem.sem)%2==0:
                                    count=0
                                    count=int(request.POST['count'])+1
                                    back=backlog.objects.filter(back_enroll_no=request.POST['marks_enroll_no']).get(back_sub_no=request.POST['marks_sub_no'])
                                    if back.status=='Clear':
                                        count-=1
                                    subject,sem_id=no_marks(request.POST['marks_enroll_no'])
                                    if len(subject)==count:
                                                from .models import result
                                                result_obj=result.objects.get(result_enroll_no=request.POST['marks_enroll_no'])
                                                results_float=float(result_obj.ogpa)
                                                print(int(sub_sem.sem))
                                                if int(sub_sem.sem)==2 and results_float>=4.00:
                                                    result.objects.filter(result_enroll_no=request.POST['marks_enroll_no']).update(result_status='None')
                                                    print('hello 1')
                                                elif int(sub_sem.sem)==4 and results_float>=4.50:
                                                    result.objects.filter(result_enroll_no=request.POST['marks_enroll_no']).update(result_status='None')
                                                    print('hello 2')
                                                elif int(sub_sem.sem)==6 and results_float>=4.75:
                                                    print('hello 3')
                                                    result.objects.filter(result_enroll_no=request.POST['marks_enroll_no']).update(result_status='None')
                                                else:
                                                    print('hello 4')
                                                    result.objects.filter(result_enroll_no=request.POST['marks_enroll_no']).update(result_status='Year Back')
                                                messages.error(request,'BackLog subject updated for current student')
                                                return redirect(home,error_message='BackLog subject updated for current student')
                                    else:
                                        enroll=request.POST['marks_enroll_no']
                                        return render(request,'job/marks_detail.html',{'subject':subject,'enroll':enroll,'count':count})

                                messages.error(request,'BackLog subject updated for current student')



                        else:
                                if marks.objects.filter(marks_sub_no=request.POST['marks_sub_no']).filter(marks_enroll_no=request.POST['marks_enroll_no']).exists():
                                    messages.error(request,'Marks Already Uploaded!!')
                                    return redirect(home,error_message="Marks Already Uploaded!!")

                                Marks=marks()

                                sub_obj=subjects.objects.get(sub_no=request.POST['marks_sub_no'])
                                field_name_subject='sub_no'
                                field_object_sub=subjects._meta.get_field(field_name_subject)
                                subject_no=str(field_object_sub.value_from_object(sub_obj))

                                sub_last_ele=(subject_no[0:7])
                                print(sub_last_ele)
                                student_obj=student.objects.get(enroll_no=request.POST['marks_enroll_no'])
                                sub_sare_list=subjects.objects.all().filter(sub_no__contains=sub_last_ele).filter(sub_dept_no=student_obj.student_dept_no)

                                student_roll=request.POST['marks_enroll_no']
                                print(str(student_obj.d2d))
                                if str(student_obj.d2d)=='Yes':
                                    student_start_four=int(student_roll[0:4])-1
                                    print(student_start_four)
                                else:
                                    student_start_four=int(student_roll[0:4])
                                    print(student_start_four)
                                    print('else')


                                min=5
                                subject_loop_obj=subjects()

                                for subject in sub_sare_list:

                                    field_name_subject_loop='sub_no'
                                    field_object_sub_loop=subjects._meta.get_field(field_name_subject_loop)
                                    subject_no=str(field_object_sub.value_from_object(subject))
                                    sub_last_four_int=int(subject_no[-6:-2])

                                    if (student_start_four-sub_last_four_int)<min and (student_start_four-sub_last_four_int)>=0:
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
                                        back.status='Back in both Theory & Practical'
                                        back.save()
                                    if (int(request.POST['th']) + int(request.POST['mid']))<28 and int(request.POST['pr'])>12:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='Back in Theory'
                                        back.save()
                                    if (int(request.POST['th']) + int(request.POST['mid']))>28 and int(request.POST['pr'])<12:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='Back in Practical'
                                        back.save()

                                if th_cr==0 and pr_cr==1 or th_cr==0 and pr_cr==2 or th_cr==0 and pr_cr==3 or th_cr==0 and pr_cr==4:
                                    if int(request.POST['pr'])<40:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='Back in Practical'
                                        back.save()

                                if th_cr==1 and pr_cr==0 or th_cr==2 and pr_cr==0 or th_cr==3 and pr_cr==0 or th_cr==4 and pr_cr==0:
                                    if (int(request.POST['th']) + int(request.POST['mid']))<40:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='Back in Theory'
                                        back.save()

                                if th_cr==1 and pr_cr==2 or th_cr==1 and pr_cr==3 or th_cr==1 and pr_cr==4:
                                    if (int(request.POST['th']))<12 and int(request.POST['pr'])<28:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='Back in both Theory & Practical'
                                        back.save()
                                    if (int(request.POST['th']))<12 and int(request.POST['pr'])>28:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='Back in Theory'
                                        back.save()
                                    if (int(request.POST['th']))>12 and int(request.POST['pr'])<28:
                                        back=backlog()
                                        enroll=request.POST['marks_enroll_no']
                                        back.back_enroll_no=student.objects.get(enroll_no=enroll)
                                        back.back_sub_no=subjects.objects.get(sub_no=sub_id)
                                        back.status='Back in Practical'
                                        back.save()

                                Marks.save()

                        subject1,sem_id=no_marks(request.POST['marks_enroll_no'])
                        mark_subject=marks.objects.filter(marks_enroll_no=request.POST['marks_enroll_no']).order_by('marks_sub_no')
                        mark_update_list=[]
                        count1=0
                        count2=0
                        for mark in mark_subject:
                            field_name='marks_sub_no'
                            field_object=marks._meta.get_field(field_name)
                            mark_sub=str(field_object.value_from_object(mark))
                            if mark_sub[-8] in ['a' , 'b' , 'c' , 'd' , 'e' ]:
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

                            return render(request,'job/marks_detail.html',{'subject':subject,'enroll':enroll,'count':0})
                        else:
                            return redirect('home')


            else:
                    # return redirect(home,error_message="Student Does Not Exist!!")
                    messages.error(request,'Student Does Not Exist!!')
                    messages.error(request,'Student Does Not Exist!!')

        else:
                return render(request,'job/home.html',context)








def result_form(request):
    if request.method=='POST':
        if student.objects.filter(enroll_no=request.POST['result_enroll']).exists():
                if result.objects.filter(result_enroll_no=request.POST['result_enroll']).exists():
                    result_obj=result.objects.get(result_enroll_no=request.POST['result_enroll'])
                    if request.POST['Sem']=='1':
                        if result_obj.sem1!=0:
                            mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total=marksheet(request.POST['result_enroll'],request.POST['Sem'])
                            zip_list=zip(mark_list,sub_name,th_cr,pr_cr,th_mark,pr_mark,mid_mark,total,total_mark,current_res)

                            context={
                            'zip_list':zip_list,
                            'stu_fname':stu_fname,
                            'stu_lname':stu_lname,
                            'stu_enroll':stu_enroll,
                            'year':year,
                            'semaster':semaster,
                            'sgpa':sgpa,
                            'ogpa':ogpa,
                            'grades':grades,
                            'crs':crs,
                            'previous_points':previous_points,
                            'previous_cr':previous_cr,
                            'sum_cr_current':sum_cr_current,
                            'sum_points_current':sum_points_current,
                            'dept_name':dept_name,
                            'back_zip_list':back_zip_list
                            }

                            return render(request,'job/marksheet.html',context)
                    elif request.POST['Sem']=='2':
                        if result_obj.sem2!=0:
                            mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total=marksheet(request.POST['result_enroll'],request.POST['Sem'])
                            zip_list=zip(mark_list,sub_name,th_cr,pr_cr,th_mark,pr_mark,mid_mark,total,total_mark,current_res)

                            context={
                            'zip_list':zip_list,
                            'stu_fname':stu_fname,
                            'stu_lname':stu_lname,
                            'stu_enroll':stu_enroll,
                            'year':year,
                            'semaster':semaster,
                            'sgpa':sgpa,
                            'ogpa':ogpa,
                            'grades':grades,
                            'crs':crs,
                            'previous_points':previous_points,
                            'previous_cr':previous_cr,
                            'sum_cr_current':sum_cr_current,
                            'sum_points_current':sum_points_current,
                            'dept_name':dept_name,
                            'back_zip_list':back_zip_list
                            }

                            return render(request,'job/marksheet.html',context)
                    elif request.POST['Sem']=='3':
                        if result_obj.sem3!=0:
                            mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total=marksheet(request.POST['result_enroll'],request.POST['Sem'])
                            zip_list=zip(mark_list,sub_name,th_cr,pr_cr,th_mark,pr_mark,mid_mark,total,total_mark,current_res)

                            context={
                            'zip_list':zip_list,
                            'stu_fname':stu_fname,
                            'stu_lname':stu_lname,
                            'stu_enroll':stu_enroll,
                            'year':year,
                            'semaster':semaster,
                            'sgpa':sgpa,
                            'ogpa':ogpa,
                            'grades':grades,
                            'crs':crs,
                            'previous_points':previous_points,
                            'previous_cr':previous_cr,
                            'sum_cr_current':sum_cr_current,
                            'sum_points_current':sum_points_current,
                            'dept_name':dept_name,
                            'back_zip_list':back_zip_list
                            }

                            return render(request,'job/marksheet.html',context)
                    elif request.POST['Sem']=='4':
                        if result_obj.sem4!=0:
                            mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total=marksheet(request.POST['result_enroll'],request.POST['Sem'])
                            zip_list=zip(mark_list,sub_name,th_cr,pr_cr,th_mark,pr_mark,mid_mark,total,total_mark,current_res)

                            context={
                            'zip_list':zip_list,
                            'stu_fname':stu_fname,
                            'stu_lname':stu_lname,
                            'stu_enroll':stu_enroll,
                            'year':year,
                            'semaster':semaster,
                            'sgpa':sgpa,
                            'ogpa':ogpa,
                            'grades':grades,
                            'crs':crs,
                            'previous_points':previous_points,
                            'previous_cr':previous_cr,
                            'sum_cr_current':sum_cr_current,
                            'sum_points_current':sum_points_current,
                            'dept_name':dept_name,
                            'back_zip_list':back_zip_list
                            }

                            return render(request,'job/marksheet.html',context)
                    elif request.POST['Sem']=='5':
                        if result_obj.sem5!=0:
                            mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total=marksheet(request.POST['result_enroll'],request.POST['Sem'])
                            zip_list=zip(mark_list,sub_name,th_cr,pr_cr,th_mark,pr_mark,mid_mark,total,total_mark,current_res)

                            context={
                            'zip_list':zip_list,
                            'stu_fname':stu_fname,
                            'stu_lname':stu_lname,
                            'stu_enroll':stu_enroll,
                            'year':year,
                            'semaster':semaster,
                            'sgpa':sgpa,
                            'ogpa':ogpa,
                            'grades':grades,
                            'crs':crs,
                            'previous_points':previous_points,
                            'previous_cr':previous_cr,
                            'sum_cr_current':sum_cr_current,
                            'sum_points_current':sum_points_current,
                            'dept_name':dept_name,
                            'back_zip_list':back_zip_list
                            }

                            return render(request,'job/marksheet.html',context)
                    elif request.POST['Sem']=='6':
                        if result_obj.sem6!=0:
                            mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total=marksheet(request.POST['result_enroll'],request.POST['Sem'])
                            zip_list=zip(mark_list,sub_name,th_cr,pr_cr,th_mark,pr_mark,mid_mark,total,total_mark,current_res)

                            context={
                            'zip_list':zip_list,
                            'stu_fname':stu_fname,
                            'stu_lname':stu_lname,
                            'stu_enroll':stu_enroll,
                            'year':year,
                            'semaster':semaster,
                            'sgpa':sgpa,
                            'ogpa':ogpa,
                            'grades':grades,
                            'crs':crs,
                            'previous_points':previous_points,
                            'previous_cr':previous_cr,
                            'sum_cr_current':sum_cr_current,
                            'sum_points_current':sum_points_current,
                            'dept_name':dept_name,
                            'back_zip_list':back_zip_list
                            }

                            return render(request,'job/marksheet.html',context)
                    elif request.POST['Sem']=='7':
                        if result_obj.sem7!=0:
                            mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total=marksheet(request.POST['result_enroll'],request.POST['Sem'])
                            zip_list=zip(mark_list,sub_name,th_cr,pr_cr,th_mark,pr_mark,mid_mark,total,total_mark,current_res)

                            context={
                            'zip_list':zip_list,
                            'stu_fname':stu_fname,
                            'stu_lname':stu_lname,
                            'stu_enroll':stu_enroll,
                            'year':year,
                            'semaster':semaster,
                            'sgpa':sgpa,
                            'ogpa':ogpa,
                            'grades':grades,
                            'crs':crs,
                            'previous_points':previous_points,
                            'previous_cr':previous_cr,
                            'sum_cr_current':sum_cr_current,
                            'sum_points_current':sum_points_current,
                            'dept_name':dept_name,
                            'back_zip_list':back_zip_list
                            }

                            return render(request,'job/marksheet.html',context)
                    elif request.POST['Sem']=='8':
                        if result_obj.sem2!=8:
                            mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total=marksheet(request.POST['result_enroll'],request.POST['Sem'])
                            zip_list=zip(mark_list,sub_name,th_cr,pr_cr,th_mark,pr_mark,mid_mark,total,total_mark,current_res)

                            context={
                            'zip_list':zip_list,
                            'stu_fname':stu_fname,
                            'stu_lname':stu_lname,
                            'stu_enroll':stu_enroll,
                            'year':year,
                            'semaster':semaster,
                            'sgpa':sgpa,
                            'ogpa':ogpa,
                            'grades':grades,
                            'crs':crs,
                            'previous_points':previous_points,
                            'previous_cr':previous_cr,
                            'sum_cr_current':sum_cr_current,
                            'sum_points_current':sum_points_current,
                            'dept_name':dept_name,
                            'back_zip_list':back_zip_list
                            }

                            return render(request,'job/marksheet.html',context)





                student_roll=str(request.POST['result_enroll'])
                student_start_four=int(student_roll[0:4])
                roll_no=student.objects.get(enroll_no=student_roll)
                sub_list=subjects.objects.filter(sem=request.POST['Sem']).filter(sub_dept_no=roll_no.student_dept_no)
                sub_last_four_list=[]
                for sub in sub_list:
                    sub_code_str=str(sub.sub_no)
                    sub_last_four_int=int(sub_code_str[-6:-2])
                    if sub_last_four_int not in sub_last_four_list:
                        sub_last_four_list.append(sub_last_four_int)
                min=5
                scheme_year=0
                for list in sub_last_four_list:
                    if (student_start_four-list)<=min and (student_start_four-list)>=0:
                        min=student_start_four-list
                        scheme_year=list
                str_scheme_year=str(scheme_year)
                print(scheme_year)
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

                # if len(mark_obj_list)!=count:
                #     messages.error(request,"Result in under progress !! Thank You")
                #     return redirect(home,error_message="Result in under progress !! Thank You")


                student_object=student.objects.get(enroll_no=request.POST['result_enroll'])

                field_name_roll='enroll_no'
                field_object_result=student._meta.get_field(field_name_roll)
                roll_no=field_object_result.value_from_object(student_object)

                sub_no_obj=subjects.objects.all().filter(sub_no__contains=scheme_year).filter(sem=request.POST['Sem']).filter(sub_dept_no=(stu_dept_no_1.student_dept_no))
                print('subjects')
                print(sub_no_obj)
                try:
                    Marks=marks.objects.all().filter(marks_enroll_no=roll_no).filter(marks_sub_no__in=sub_no_obj)
                    print('marks subjects')
                    print(Marks)
                    result_sum=0
                    result_cr=0
                    result_t=0
                    crs=0
                    for mark in Marks:
                        string=str(mark.marks_sub_no)
                        if string[0:11] in ['NSS/NCC/NSO']:
                                continue
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
                                if sem_2<=4.00:
                                    result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(result_status='Year Back')

                        elif int(request.POST['Sem'])==3:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem3=fnl_result)
                                sem_3=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_3)
                        elif int(request.POST['Sem'])==4:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem4=fnl_result)
                                sem_4=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_4)
                                if sem_4<=4.50:
                                    result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(result_status='Year Back')
                        elif int(request.POST['Sem'])==5:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem5=fnl_result)
                                sem_5=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_5)
                        elif int(request.POST['Sem'])==6:
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(sem6=fnl_result)
                                sem_6=round((current_res)/(current_cr_for),2)
                                result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(ogpa=sem_6)
                                if sem_6<=4.75:
                                    result.objects.filter(result_enroll_no=request.POST['result_enroll']).update(result_status='Year Back')
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

                    mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total=marksheet(request.POST['result_enroll'],request.POST['Sem'])
                    zip_list=zip(mark_list,sub_name,th_cr,pr_cr,th_mark,pr_mark,mid_mark,total,total_mark,current_res)

                    context={
                    'zip_list':zip_list,
                    'stu_fname':stu_fname,
                    'stu_lname':stu_lname,
                    'stu_enroll':stu_enroll,
                    'year':year,
                    'semaster':semaster,
                    'sgpa':sgpa,
                    'ogpa':ogpa,
                    'grades':grades,
                    'crs':crs,
                    'previous_points':previous_points,
                    'previous_cr':previous_cr,
                    'sum_cr_current':sum_cr_current,
                    'sum_points_current':sum_points_current,
                    'dept_name':dept_name,
                    'back_zip_list':back_zip_list
                    }

                    return render(request,'job/marksheet.html',context)
                except:
                    messages.error(request,'result dont exist')
                    return redirect(home,error_message="Student Does Not Exist!!")

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
            return render(request,'job/marks_detail.html',{'subject':subject,'enroll':enroll,'count':0})
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
        if str(student_dept.d2d)=='Yes':
            stu_four=int(enroll[0:4])-1
        else:
            stu_four=int(enroll[0:4])
        if result.objects.filter(result_enroll_no=str(enroll)).exists():
                if str(results.result_status)=='Year Back' and (sem_id-1)%2==0:
                    subs=subjects.objects.filter(sem=(sem_id-2)).filter(sub_dept_no=student_dept.student_dept_no)
                    back_subs=backlog.objects.filter(back_enroll_no=enroll).filter(status__icontains='Back').filter(back_sub_no__in=subs)
                    back_final_list=[]
                    for back in back_subs:
                        if back.back_sub_no in subs:
                            field_name='back_sub_no'
                            field_object=backlog._meta.get_field(field_name)
                            back_in=str(field_object.value_from_object(back))
                            back_final_list.append(back_in)


                    return_subjects=subjects.objects.filter(sub_no__in=back_final_list)
                    return (return_subjects,(sem_id-2))
                elif str(results.result_status)=='Next Sem' and (sem_id-1)%2==0:
                        subs=subjects.objects.filter(sem=(sem_id-1)).filter(sub_dept_no=student_dept.student_dept_no)
                        back_subs=backlog.objects.filter(back_enroll_no=enroll).filter(status__icontains='Back')
                        back_final_list=[]
                        for back in back_subs:
                            if back.back_sub_no in subs:
                                field_name='back_sub_no'
                                field_object=backlog._meta.get_field(field_name)
                                back_in=str(field_object.value_from_object(back))
                                back_final_list.append(back_in)

                        return_subjects=subjects.objects.filter(sub_no__in=back_final_list)
                        return (return_subjects,(sem_id-1))
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
            if int(stu_four-sub_scheme)<min and int(stu_four-sub_scheme)>=0:
                min=stu_four-sub_scheme
                sub_scheme_year_final=sub_scheme
        subject=subjects.objects.filter(sub_dept_no=student_dept.student_dept_no).filter(sem=sem_id).filter(sub_no__contains=str(sub_scheme_year_final))
        final_query=subject
        if backlog.objects.filter(back_enroll_no=str(enroll)).exists():
            if sem_id>=3:
                for i in range(sem_id,1,-2):
                    sub=subjects.objects.filter(sub_dept_no=student_dept.student_dept_no).filter(sem=i-2).filter(sub_no__contains=str(sub_scheme_year_final)).order_by('sub_no')
                    back_sub=backlog.objects.filter(back_enroll_no=str(enroll)).filter(back_sub_no__in=sub).filter(status__contains='Back')

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



def marksheet(enroll='',sem_id=''):
                    stu=student.objects.get(enroll_no=enroll)
                    field_name_dept='student_dept_no'
                    field_object_dept=student._meta.get_field(field_name_dept)
                    dept_no=str(field_object_dept.value_from_object(stu))
                    dept=department.objects.get(dept_no=dept_no)
                    dept_name=dept.dept_name
                    subj=subjects.objects.filter(sem=sem_id).filter(sub_dept_no=stu.student_dept_no)
                    mark_obj=marks.objects.filter(marks_sub_no__in=subj).filter(marks_enroll_no=enroll)
                    mark_list=[]
                    th_mark=[]
                    pr_mark=[]
                    mid_mark=[]
                    th_cr=[]
                    pr_cr=[]
                    total_mark=[]
                    sub_name=[]
                    current_res=[]
                    total=[]
                    sum_cr_current=0
                    sum_points=0.0
                    sum_points_current=0.0
                    for mark in mark_obj:
                        field_name='marks_sub_no'
                        field_object=marks._meta.get_field(field_name)
                        obj=str(field_object.value_from_object(mark))
                        sub=subjects.objects.get(sub_no=obj)
                        sub_name.append(str(sub.sub_name))
                        if obj[-8] in ['a','b','c','d','e','i','j','k','l','m','n','o'] and obj[-9] in ['P','C','E']:
                            mark_list.append(obj[0:6])
                        elif obj[-8] in ['a','b','c','d','e','i','j','k','l','m','n','o'] and obj[2] not in ['1'] :
                            mark_list.append(obj[0:6])
                        elif obj[-8] in ['P','C','E']:
                            mark_list.append(obj[0:6])
                        else:
                            mark_list.append(obj[0:5])
                        th_mark.append(mark.th)
                        pr_mark.append(mark.pr)
                        mid_mark.append(mark.mid)

                        total.append((int(mark.th)+int(mark.pr)+int(mark.mid)))
                        total_mark.append(float((int(mark.th)+int(mark.pr)+int(mark.mid)))/10)
                        current_res.append(mark.current_result)
                        sub1=subjects.objects.get(sub_no=obj)
                        field_name='sub_scheme_no'
                        field_object=subjects._meta.get_field(field_name)
                        sub_scheme_no_marksheet=field_object.value_from_object(sub1)

                        scheme_obj=scheme.objects.get(scheme_no=sub_scheme_no_marksheet)
                        th_cr.append(scheme_obj.theory_cr)
                        pr_cr.append(scheme_obj.practical_cr)

                        string=str(mark.marks_sub_no)
                        if string[0:11] in ['NSS/NCC/NSO']:
                                    continue
                        sum_cr_current+=int(scheme_obj.theory_cr)+int(scheme_obj.practical_cr)
                        sum_points+=(mark.current_result)

                    sum_points_current=round(sum_points,2)
                    sgpa=0.0
                    ogpa=0.0
                    year=''
                    semaster=''
                    grades=0.0
                    crs=0
                    result_obj=result.objects.get(result_enroll_no=enroll)

                    if sem_id=='1':
                        sgpa=result_obj.sem1
                        year='First'
                        semaster='First'
                    elif sem_id=='2':
                        sgpa=result_obj.sem2
                        year='First'
                        semaster='Second'
                    elif sem_id=='3':
                        sgpa=result_obj.sem3
                        year='Second'
                        semaster='First'
                    elif sem_id=='4':
                        sgpa=result_obj.sem4
                        year='Second'
                        semaster='Second'
                    elif sem_id=='5':
                        sgpa=result_obj.sem5
                        year='Third'
                        semaster='First'
                    elif sem_id=='6':
                        sgpa=result_obj.sem6
                        year='Third'
                        semaster='Second'
                    elif sem_id=='7':
                        sgpa=result_obj.sem7
                        year='Final'
                        semaster='First'
                    elif sem_id=='8':
                        sgpa=result_obj.sem8
                        year='Final'
                        semaster='Second'

                    stu_enroll=str(stu.enroll_no)
                    stu_fname=str(stu.fname)
                    stu_lname=str(stu.lname)

                    results=0.0
                    cr=0
                    previous_points=0.0
                    previous_cr=0
                    id=int(sem_id)+1
                    for i in range(1,id,1):

                        ogpa_sub=subjects.objects.filter(sem=i).filter(sub_dept_no=stu.student_dept_no)

                        ogpa_marks=marks.objects.filter(marks_sub_no__in=ogpa_sub).filter(marks_enroll_no=enroll)

                        for mark in ogpa_marks:
                            string=str(mark.marks_sub_no)
                            if string[0:11] in ['NSS/NCC/NSO']:
                                        continue
                            results+=float(mark.current_result)
                            cr+=int(mark.current_cr)

                        if i!=int(sem_id):
                            previous_points=round(results,2)
                            previous_cr=cr

                    ogpa=round(float(results/cr),2)
                    grades=round(results,2)
                    crs=cr


                    back_zip_list=[]
                    if backlog.objects.filter(back_enroll_no=enroll).exists():
                        back_obj=backlog.objects.filter(back_enroll_no=enroll)
                        print(back_obj)
                        back_sub_list=[]
                        back_sub_name=[]
                        back_th_cr=[]
                        back_pr_cr=[]
                        back_th_mark=[]
                        back_pr_mark=[]
                        back_mid_mark=[]
                        back_total_mark=[]
                        back_grades=[]
                        back_current_res=[]
                        back_total=[]


                        for i in range(int(sem_id),1,-2):
                            subs=subjects.objects.filter(sem=i-2)
                            for back in back_obj:
                              if back.back_sub_no in subs:
                                print(i)
                                print(i-2)
                                print(back.back_sub_no)
                                field_name_back='back_sub_no'
                                field_object_back=backlog._meta.get_field(field_name_back)
                                back_sub_no=field_object_back.value_from_object(back)
                                print(back_sub_no)
                                try:
                                    back_sub=subjects.objects.filter(sem=i-2).get(sub_no=back_sub_no)
                                    sub=str(back_sub.sub_no)
                                    status=str(back.status)
                                    string=status[0:4]

                                    if int(sem_id)-(i-2) in [4,6] and backlog.objects.filter(back_enroll_no=enroll).filter(back_sub_no=back_sub_no).filter(status__contains='Back'):
                                            if sub[-8] in ['a','b','c','d','e','i','j','k','l','m','n','o'] and sub[-9] in ['P','C','E']:
                                                back_sub_list.append(sub[0:6])
                                            elif sub[-8] in ['a','b','c','d','e','i','j','k','l','m','n','o'] and sub[2] not in ['1'] :
                                                back_sub_list.append(sub[0:6])
                                            elif sub[-8] in ['P','C','E']:
                                                back_sub_list.append(sub[0:6])
                                            else:
                                                back_sub_list.append(sub[0:5])


                                            back_sub_name.append(str(back_sub.sub_name))
                                    if int(sem_id)-(i-2) in [2]:
                                            if sub[-8] in ['a','b','c','d','e','i','j','k','l','m','n','o'] and sub[-9] in ['P','C','E']:
                                                back_sub_list.append(sub[0:6])
                                            elif sub[-8] in ['a','b','c','d','e','i','j','k','l','m','n','o'] and sub[2] not in ['1'] :
                                                back_sub_list.append(sub[0:6])
                                            elif sub[-8] in ['P','C','E']:
                                                back_sub_list.append(sub[0:6])
                                            else:
                                                back_sub_list.append(sub[0:5])


                                            back_sub_name.append(str(back_sub.sub_name))

                                    field_name='sub_scheme_no'
                                    field_object=subjects._meta.get_field(field_name)
                                    scheme_no=field_object.value_from_object(back_sub)

                                    scheme_obj=scheme.objects.get(scheme_no=scheme_no)
                                    back_th_cr.append(scheme_obj.theory_cr)
                                    back_pr_cr.append(scheme_obj.practical_cr)

                                    mark=marks.objects.filter(marks_enroll_no=enroll).get(marks_sub_no=back.back_sub_no)
                                    back_th_mark.append(mark.th)
                                    back_pr_mark.append(mark.pr)
                                    back_mid_mark.append(mark.mid)
                                    back_total.append(int(mark.th)+int(mark.pr)+int(mark.mid))
                                    back_grades.append(float(int(mark.th)+int(mark.pr)+int(mark.mid))/10)
                                    back_current_res.append(mark.current_result)
                                    back_zip_list=zip(back_sub_list,back_sub_name,back_th_cr,back_pr_cr,back_th_mark,back_pr_mark,back_mid_mark,back_total,back_grades,back_current_res)

                                except:
                                    pass


                    return(mark_list,th_mark,pr_mark,mid_mark,th_cr,pr_cr,sgpa,ogpa,year,semaster,stu_enroll,stu_fname,stu_lname,grades,crs,previous_points,previous_cr,total_mark,sub_name,current_res,sum_cr_current,sum_points_current,dept_name,back_zip_list,total)
