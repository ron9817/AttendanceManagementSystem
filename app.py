from flask import Flask, render_template, request
app=Flask(__name__)
def to_string(previous_dict):
    previous_dict_str=""
    for i in previous_dict:
        previous_dict_str+=i
        previous_dict_str+=":"
        previous_dict_str+=str(previous_dict[i])
        previous_dict_str+=";"
    previous_dict_str=previous_dict_str[:-1]
    return previous_dict_str

def to_dict(previous_dict_str):
    previous_dict={}
    temp1=[]
    for i in (previous_dict_str.split(';')):
        temp1.append(i)
    for i in temp1:
        temp2=i.split(':')
        temp3=temp2[1].split(',')
        previous_dict[temp2[0]]=[int(temp3[0][1:]),int(temp3[1][:-1])]

    return previous_dict

@app.route('/')
@app.route('/Ronak@9821')
def attendance():
    return render_template("attendace.html")

@app.route('/Ronak@9821/result',methods=['GET', 'POST'])
def attendance_result():
    if request.method=="POST":
        details=[]
        if request.form['day']=='-':

            file=open("/home/ronakseita38/mysite/r_attendance.txt","r")
            previous=file.read()
            file.close()

            previous_dict=to_dict(previous)

            result={}
            for i in previous_dict:
                if previous_dict[i][1]==0:
                    result[i]=0
                else:
                    result[i]=(previous_dict[i][0]/previous_dict[i][1])*100

            sump=0
            sumt=0
            for i in previous_dict:
                sump+=previous_dict[i][0]
                sumt+=previous_dict[i][1]
            result['Total']=(sump/sumt)*100

            #not required as you are only viewing attendance
            #previous=to_string(previous_dict)
            #file=open("/home/ronakseita38/mysite/r_attendance.txt","w")
            #file.write(previous)
            #file.close()

            return render_template("attendace_result.html",details=result)
        else:

            form=request.form

            for i in form:
                if i=="day":
                    continue
                else:
                    details.append(form[i])

            file=open("/home/ronakseita38/mysite/r_attendance.txt","r")
            previous=file.read()
            file.close()
            previous_dict=to_dict(previous)
            #return render_template("attendace_result.html",details=previous_dict)

            timetable={}
            timetable['Mon']=["CNS","ADBMS","MEP","ADSAA","INTPL","INTPL"]
            timetable['Tue']=["ADSAA","CNS","IOTL","IOTL","INTP","ADBMS"]
            timetable['Wed']=["INTP","ADBMS","MEP","BCE","ADSAA","SECURITYL","SECURITYL"]
            timetable['Thu']=["OLAPL","OLAPL","MEP","CNS","INTP","ADSAA"]
            timetable['Fri']=["CNS","MEP","INTP","BCE","ADBMS","BCEL","BCEL"]

            for i in details:
                previous_dict[i][0]+=1

            selected_day=form['day']
            for i in timetable[selected_day]:
                previous_dict[i][1]+=1

            result={}
            for i in previous_dict:
                if previous_dict[i][1]==0:
                    result[i]=0
                else:
                    result[i]=(previous_dict[i][0]/previous_dict[i][1])*100
            sump=0
            sumt=0

            for i in previous_dict:
                sump+=previous_dict[i][0]
                sumt+=previous_dict[i][1]
            result['Total']=(sump/sumt)*100
            ##save the new dict

            file=open("/home/ronakseita38/mysite/r_attendance.txt","w")
            previous=to_string(previous_dict)
            file.write(previous)
            file.close()

            return render_template("attendace_result.html",details=result)
    else:
        return render_template("ERROR")

@app.route('/Ronak@9821/proxy',methods=["GET","POST"])
def attendance_proxy():
    if request.method=="POST":
        form=request.form
        actual=form['actual']
        proxy=form['proxy']

        file=open("/home/ronakseita38/mysite/r_attendance.txt","r")
        previous=file.read()
        file.close()
        previous_dict=to_dict(previous)

        previous_dict[actual][1]-=1
        previous_dict[proxy][0]+=1
        previous_dict[proxy][1]+=1

        result={}
        for i in previous_dict:
            if previous_dict[i][1]==0:
                result[i]=0
            else:
                result[i]=(previous_dict[i][0]/previous_dict[i][1])*100

        sump=0
        sumt=0
        for i in previous_dict:
            sump+=previous_dict[i][0]
            sumt+=previous_dict[i][1]

        result['Total']=(sump/sumt)*100

        file=open("/home/ronakseita38/mysite/r_attendance.txt","w")
        previous=to_string(previous_dict)
        file.write(previous)
        file.close()

        return render_template("attendace_result.html",details=result)
    else:
        return render_template('attendance_proxy.html')


if __name__=='__main__':
	app.run(debug=True)
