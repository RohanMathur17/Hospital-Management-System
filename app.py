from flask import Flask,render_template,redirect,url_for,request
from pymongo import MongoClient




app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.medicords

@app.route('/',methods=['GET','POST'])



def main():
     global task
     if request.method=='POST':
          if request.form.get('DOCTOR')=='DOCTOR':
             task = 1
             return redirect(url_for('login'))


          elif request.form.get('PATIENT')=='PATIENT':
              task = 2
              return redirect(url_for('patient'))


     elif request.method=='GET':
          return render_template('index.html')
     print('hello')




@app.route('/login',methods=['GET','POST'])
def login():
    if task == 1:
        collection = db.doctors_details
        if request.form.get('signup')=='signup':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            spec = request.form['specialization']
            username_new = request.form['username_new']
            password_new = request.form['password_new']
            temp = db.doctors_details.find()
            flag = 0
            for i in temp:
                if i['username']==username_new:
                    flag=1
                    break
            if flag ==0:
                post = {'name':name , 'email':email , 'phone':phone , 'spec':spec , 'username':username_new , 'password':password_new}
                postID = db.doctors_details.insert_one(post).inserted_id
                emp = db.doctors_details.find()
            return render_template('login.html')

        elif request.form.get('signin')=='signin':
            user = request.form['username']
            passw = request.form['password']
            acc = db.doctors_details.find_one({"username":user})
            if passw==acc["password"]:
                global user_d
                user_d = user
                global nam
                nam  = acc['name']
                global speci
                speci = acc['spec']
                global emaili
                emaili = acc['email']
                global usern
                usern = acc['username']
                return redirect(url_for('doctorhome'))
    return render_template('login.html')


@app.route('/patient',methods=['GET','POST'])
def patient():
    if task == 2:

        collection = db.patient_details
        if request.form.get('signup')=='signup':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            username_new = request.form['username_new']
            password_new = request.form['password_new']
            temp = db.patient_details.find()
            flag = 0
            for i in temp:
                if i['username']==username_new:
                    flag=1
                    break
            if flag ==0:
                post = {'name':name , 'email':email , 'phone':phone ,  'username':username_new , 'password':password_new}
                postID = db.patient_details.insert_one(post).inserted_id
                emp = db.patient_details.find()

            return render_template('login_patient.html')
        elif request.form.get('signin1')=='signin1':
            user = request.form['username']
            passw = request.form['password']
            acc = db.patient_details.find_one({"username":user})
            if passw==acc["password"]:
                global user_p
                user_p = user
                global nam
                nam  = acc['name']
                global emaili
                emaili = acc['email']
                global usern
                usern = acc['username']
                return redirect(url_for('patienthome'))


    return render_template('login_patient.html')



@app.route('/doctorhome',methods=['GET','POST'])
def doctorhome():
    global task_doc
    task_doc = 0
    data1 = db.appointment.find({"doctor":user_d})
    if request.method=='POST':
        if request.form.get('addappointment')=='addappointment':
            task_doc=1
            return redirect(url_for('addappointment'))
        if request.form.get('add_medical_data')=='add_medical_data':
            task_doc=2
            return redirect(url_for('adddata'))
        if request.form.get('see_medical_data')=='see_medical_data':
            task_doc=3
            return redirect(url_for('seedata'))
    return render_template('doctor_home.html',name1 =nam , data1 = data1)





@app.route('/patienthome',methods=['GET','POST'])
def patienthome():
    global task_pat
    task_pat = 0
    data = db.medical_history.find({"patient":user_p})
    if request.method=='POST':
        if request.form.get('records')=='records':
            task_pat = 1
            return redirect(url_for('addmedical'))
        if request.form.get('appointment')=='appointment':
            task_pat=2
            return redirect(url_for('seeappoint'))
        if request.form.get('docs')=='docs':
            task_pat=3
            return redirect(url_for('seedoc'))

    return render_template('patient_home.html' , name1 = nam , data = data)

@app.route('/addappointment',methods=['GET','POST'])
def addappointment():
    if task_doc==1:
        if request.method=='POST':
            if request.form.get('appoint')=='appoint':
                naam = request.form['naam']
                tareek = request.form['tareek']
                mahina = request.form['mahina']
                ghanta = request.form['ghanta']
                minutes = request.form['minutes']
                post = {'doctor':user_d , 'patient':naam , 'date':tareek , 'month':mahina , 'hour':ghanta , 'minutes':minutes}
                postID = db.appointment.insert_one(post).inserted_id
        return render_template('add_appointment.html')

@app.route('/adddata',methods=['GET','POST'])
def adddata():
    if task_doc==2:
        if request.method=='POST':
            if request.form.get('data')=='data':
                disease = request.form['disease']
                mont = request.form['mont']
                saal = request.form['saal']
                post = {'doctor':user_d , 'disease':disease , 'month':mont , 'year':saal}
                postID = db.disease_data.insert_one(post).inserted_id
        return render_template('add_data.html')

@app.route('/seedata',methods=['GET','POST'])
def seedata():
    data2 = db.disease_data.find()
    if task_doc==3:
        return render_template('see_data.html' , data2 = data2)

@app.route('/addmedical',methods = ['GET','POST'])
def addmedical():
    if task_pat==1:
        if request.method=='POST':
            if request.form.get('data')=='data':
                disease = request.form['disease']
                mont = request.form['mont']
                saal = request.form['saal']
                post = {'patient':user_p , 'disease':disease , 'month':mont , 'year':saal}
                postID = db.medical_history.insert_one(post).inserted_id
        return render_template('add_data.html')
    return render_template('add_medicalHistory.html')

@app.route('/seeappoint',methods = ['GET','POST'])
def seeappoint():
    if task_pat==2:
        data3 = db.appointment.find({"patient":user_p})
        return render_template('see_appoint_pat.html',data3 = data3)
@app.route('/seedoc',methods = ['GET','POST'])
def seedoc():
    if task_pat==3:
        data4 = db.treats.find({"patient":user_p})
        if request.method=='POST':
            if request.form.get('adddoc')=='adddoc':
                doc = request.form['doname']
                post = {'doc':doc , 'patient':user_p}
                postID = db.treats.insert_one(post).inserted_id
            return render_template('seedoc.html',data4 = data4)
        return render_template('seedoc.html',data4 = data4)
if __name__=='__main__':
    task = 0
    app.run(debug=True)
