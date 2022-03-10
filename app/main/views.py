from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch,Comment,UpVote
from .forms import CommentForm,UpdateProfile,PitchForm
from .. import db,photos

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Pitch Point'
    pitches= Pitch.get_pitches() 
    return render_template('index.html', title = title,pitches = pitches)

@main.route('/wise/pitches/')
def wise():
    '''
    View wise page function that returns the wise pitches page and its data
    '''

    pitches= Pitch.get_pitches()
    title = 'Wise Pitches'

    return render_template('wise.html', title = title, pitches= pitches )

@main.route('/pickup_lines/pitches/')
def pickup_lines():
    '''
    View pickup lines page function that returns the pickup lines page and its data
    '''

    pitches= Pitch.get_pitches()
    title = 'Pick Up Lines'

    return render_template('pickup_lines.html', title = title, pitches= pitches )

@main.route('/motivation/pitches/')
def motivation():
    '''
    View motivation page function that returns the motivational pitches page and its data
    '''

    pitches= Pitch.get_pitches()
    title = 'Motivational Pitches'

    return render_template('motivation.html', title = title, pitches= pitches )

@main.route('/pitch/<int:id>')
def pitch(id):
    '''
    View pitch page function that returns the pitch details page and its data
    '''
    pitch = Pitch.query.get(id)
    title = f'{pitch.title}'
    comments = Comment.query.filter_by(pitch_id = id).all()
    return render_template('pitch.html',title = title,pitch = pitch,comments = comments)

@main.route('/pitch/new/', methods = ['GET','POST'])
@login_required
def new_pitch():
    '''
    Function that creates new pitches
    '''
    form = PitchForm()

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        category_id = form.category_id.data
        new_pitch= Pitch(title = title, text = text, category_id= category_id, user = current_user)

        new_pitch.save_pitch()
        return redirect(url_for('.index'))
    title = 'Add Pitch'
    return render_template('new_pitch.html',title = title, pitch_form = form)


@main.route('/pitch/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    pitch = Pitch.query.get(id)

    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(pitch_id=pitch.id,comment = comment, user = current_user)
        new_comment.save_comment()
        return redirect(url_for('.pitch',id = pitch.id ))

    title = f'{pitch.title} comment'
    return render_template('new_comment.html',title = title, comment_form=form, pitch = pitch)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))