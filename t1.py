from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from form import NewsForm

app = Flask(__name__,static_folder='templates',static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/test?charset=utf8'
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "a random string"
db = SQLAlchemy(app)


class News(db.Model):
    __tablename__='news'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    data = db.Column(db.String(120), unique=True)
    is_valid = db.Column(db.Integer)
    def __repr__(self):
        return '<News %r>'%self.id

@app.route('/')
def index():
    '''新闻首页''' 
    news_list=News.query.filter_by(is_valid=1)
    return render_template('index.html',news_list=news_list)

@app.route('/cat/<name>')
def cat(name):
    '''新闻类别'''
    '''查询类别为name的数据'''
    news_list=News.query.filter(News.type==name)
    return render_template('cat.html',name=name,news_list=news_list)

@app.route('/detail/<int:pk>/')
def detail(pk):
    '''新闻详情信息'''
    new_obj=News.query.get(pk)
    return render_template('detail.html',new_obj=new_obj)

@app.route('/admin/')
@app.route('/admin/<int:page>')
def admin(page=None):
    '''新闻管理首页'''
    #如果没传就使page为1
    if page is None:
        page=1
    news_list = News.query.filter_by(is_valid=1).paginate(page,per_page=3)
    return render_template('admin/index.html',news_list=news_list)

@app.route('/admin/add/',methods=('GET','POST'))
def add():
    '''新闻新增界面'''
    form = NewsForm()
    if form.validate_on_submit():
        new_obj = News(
            type=form.type.data,
            data=form.data.data,
            is_valid=1,
        )
        db.session.add(new_obj)
        db.session.commit()

        #文字提示
        return redirect(url_for('admin'))
    return render_template('admin/add.html',form=form)


@app.route('/admin/update/<int:pk>/',methods=('GET','POST'))
def update(pk):
    '''新闻修改'''
    new_obj = News.query.get(pk)
    if not new_obj:
        return render_template(url_for('admin'))
    form = NewsForm(obj=new_obj)
    if form.validate_on_submit():
        new_obj.type=form.type.data
        new_obj.data=form.data.data

        db.session.add(new_obj)
        db.session.commit()
        #成功后跳转到admin
        return redirect(url_for('admin'))
    return render_template('admin/update.html',form=form)

@app.route('/admin/delete/<int:pk>/',methods=('GET','POST'))
def delete(pk):
    '''新闻修改'''
    new_obj = News.query.get(pk)
    if not new_obj:
        return "no"
    new_obj.is_valid=0
    db.session.add(new_obj)
    db.session.commit()
    return "yes"

if __name__ == '__main__':
    app.run(debug=True)