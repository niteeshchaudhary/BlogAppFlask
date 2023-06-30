from flask import render_template, request, redirect, url_for,session,flash
from blogging import app
from blogging.models import *
from blogging import db

with app.app_context():
    db.create_all() 
    
@app.route('/')
def login():
	return render_template('login.html')

@app.route('/blogger', methods=['POST'])
def blogger():
    if request.method == 'POST':
        name = request.form['name']
        user = User.query.filter_by(name=name).first()
        session["name"]=name
        if user:
            session['user_id'] = user.id
            return redirect(url_for('blogger_page', name=name))
        else:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(name=name).first()
            session['user_id'] = user.id
            return redirect(url_for('blogger_page', name=name))
    
    return render_template('login.html')
    

# Routes
@app.route('/blogger/<name>', methods=['GET', 'POST'])
def blogger_page(name):
    user = User.query.filter_by(name=name).first()
    blogs = Blog.query.order_by(Blog.timestamp.desc()).all()

    return render_template('blogger2.html', name=name, blogs=blogs, user=user)

@app.route('/edit-blog/<blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    blog = Blog.query.get(blog_id)

    # Check if the blog exists
    if not blog:
        flash('Blog not found', 'error')
        return redirect(url_for('blogger_page', name=session['name']))

    # Check if the current user is the author of the blog
    if blog.author.name != session['name']:
        flash('You are not authorized to edit this blog', 'error')
        return redirect(url_for('blogger_page', name=session['name']))

    # Handle the form submission for editing the blog
    if request.method == 'POST':
        # Update the blog content
        blog.content = request.form['new_content']
        db.session.commit()

        flash('Blog updated successfully', 'success')
        return redirect(url_for('blogger_page', name=session['name']))

    return render_template('edit_blog.html', blog=blog)

@app.route('/rate-blog/<int:blog_id>',methods=['POST'])
def rate_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if not blog:
        flash('Blog not found.', 'error')
        return redirect(url_for('blogger_page', name=session['name']))

    user = User.query.filter_by(name=session['name']).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('blogger_page', name=session['name']))


    if user not in blog.likes:
        blog.likes.append(user)
    else:
        blog.likes.remove(user)

    db.session.commit()
    flash('Your rating has been updated.', 'success')
    return redirect(url_for('blogger_page', name=session['name']))

@app.route('/add-blog', methods=['POST'])
def add_blog():
    content = request.form['blog_content']
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if user:
        blog = Blog(content=content, author=user)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('blogger_page', name=user.name))
    else:
        return "User not found"

@app.route('/delete-blog/<blog_id>', methods=['POST','GET'])
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)

    # Check if the blog exists
    if not blog:
        flash('Blog not found', 'error')
        return redirect(url_for('blogger_page', name=session['name']))

    # Check if the current user is the author of the blog
    if blog.author.name != session['name']:
        flash('You are not authorized to delete this blog', 'error')
        return redirect(url_for('blogger_page', name=session['name']))

    # Delete the blog from the database
    db.session.delete(blog)
    db.session.commit()

    flash('Blog deleted successfully', 'success')
    return redirect(url_for('blogger_page', name=session['name']))

@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

