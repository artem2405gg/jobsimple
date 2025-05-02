from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
db = SQLAlchemy(app)

class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    employment = db.Column(db.String(50))

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vacancies')
def vacancies():
    search = request.args.get('search', '')
    type_filter = request.args.get('type', '')
    query = Vacancy.query
    if search:
        query = query.filter(Vacancy.title.contains(search) | Vacancy.city.contains(search))
    if type_filter:
        query = query.filter(Vacancy.employment == type_filter)
    return render_template('vacancies.html', vacancies=query.all())

@app.route('/vacancy/<int:vacancy_id>/apply', methods=['POST'])
def apply(vacancy_id):
    name = request.form['name']
    phone = request.form['phone']
    response = Response(name=name, phone=phone, vacancy_id=vacancy_id)
    db.session.add(response)
    db.session.commit()
    return redirect('/vacancies')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        city = request.form['city']
        salary = request.form['salary']
        employment = request.form['employment']
        v = Vacancy(title=title, city=city, salary=salary, employment=employment)
        db.session.add(v)
        db.session.commit()
        return redirect('/admin')
    return render_template('admin.html', vacancies=Vacancy.query.all())

@app.route('/vacancy/<int:vacancy_id>/delete')
def delete_vacancy(vacancy_id):
    v = Vacancy.query.get(vacancy_id)
    db.session.delete(v)
    db.session.commit()
    return redirect('/admin')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)