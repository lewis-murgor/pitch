from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,RadioField,SelectField
from wtforms.validators import InputRequired

class CommentForm(FlaskForm):

    comment = TextAreaField('Comment',validators=[InputRequired()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):

    title = StringField('Title', validators=[InputRequired()])
    text = TextAreaField('Add pitch', validators=[InputRequired()])
    category_id = SelectField('Select Pitch Category', choices=[('1', 'Wise'), ('2', 'Pickup Lines'), ('3', 'Motivational')])
    submit = SubmitField('Submit')