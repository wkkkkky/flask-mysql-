from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class NewsForm(Form):
    '''新闻表单'''
    type = StringField('新闻类型',validators=[DataRequired("请输入类型")],
        description="请输入类型",
        render_kw={"required":"required","class":"form-control"})
    data = StringField('新闻内容',validators=[DataRequired("请输入内容")],
        description="请输入内容",
        render_kw={"required":"required","class":"form-control"})
    submit = SubmitField('提交')