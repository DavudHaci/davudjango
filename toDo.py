from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/haliy/Desktop/ToDoAppFlask/todo.db'
db = SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complate = db.Column(db.Boolean)



@app.route("/")
def homePage():
    data=todo.query.all()
    #print(data[0].id)
    sifir=[]
    bir=[]
    if len(data)>0:
        for i in range(len(data)):
            if data[i].complate == 0:
                sifir += [data[i]]
            else:
                bir+=[data[i]]
        end = sifir+bir
        

       
    
        return render_template("index.html",data=end,tamamlanan=len(bir))
    else:
        return render_template("index.html")

@app.route("/add",methods=["POST"])
def addPage():
    title = request.form.get("basliq")
    newTodo=todo(title=title,complate=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("homePage"))



@app.route("/complate/<string:id>")
def complate(id):
    data = todo.query.filter_by(id=id).first()
    print(data.complate)
    data.complate = not data.complate

    db.session.commit()
    return redirect(url_for("homePage"))



@app.route("/delete/<string:id>")
def delete(id):
    data = todo.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("homePage"))



@app.route("/update/<string:id>",methods=["POST","GET"])
def update(id):
    if request.method=="GET":
        
        return render_template("update.html")
    else:
        new=request.form.get("basliq")
        data = todo.query.filter_by(id=id).first()
        data.title=new
        db.session.commit()
        return redirect(url_for("homePage"))




if __name__=="__main__":
    db.create_all()
    app.run(debug=True)