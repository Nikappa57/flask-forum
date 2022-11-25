from flask import (abort, flash, redirect, render_template, 
    url_for, request)
from flask_login import current_user, login_required

from Site import app, db
from Site.src.loadjson import loadjson
from Site.decorator.forum import check_priority
from Site.models.permission import Permission
from Site.models.users import Users
from Site.models.section import Section
from Site.models.category import Category
from Site.models.threads import Threads
from Site.models.comment import Comments
from Site.models.subcomment import Subcomments
from Site.views.Forum.src import changePosition
from Site.views.Forum.src.messages import Error, Success
from Site.views.Forum.src.saveFile import saveFile
from Site.views.Forum.src.forms import (ThreadForm, CommentsForm, 
    SectionForm, CategoryForm, SubCommentsForm)


### HOMEPAGE ###
@app.route("/forum/")
def forumHomepage():
    categories = Category.query.order_by('position').all()
    
    return render_template("Forum/homepage.html", categories=categories)


### CATEGORY ###
@app.route("/forum/category/create", methods=["GET", "POST"])
@login_required
@check_priority('create category')
def forumCategoryCreate():
    form = CategoryForm()

    if form.validate_on_submit():
        position = int(form.position.data)
        if Category.query.all():
            real_last_position = Category.query.order_by(
                'position').all()[-1].position + 1
            if position > real_last_position:
                position = real_last_position
            changePosition.category(position)

        new_category = Category(
            name=form.name.data,
            position=position)

        db.session.add(new_category)
        db.session.commit()

        return redirect(url_for('forumHomepage'))
    elif request.method == "GET":
        form.position.data = Category.query.order_by('position').all()[-1].position + 1 \
            if Category.query.all() else 1

    return render_template('Forum/create_category.html', form=form)


@app.route("/forum/category/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
@check_priority('edit category')
def forumCategoryEdit(category_id:int):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)

    if form.validate_on_submit():
        position = int(form.position.data)
        real_last_position = Category.query.order_by(
            'position').all()[-1].position + 1
        if position > real_last_position:
            position = real_last_position
        if position != category.position:
            
            changePosition.category(position, category.position)

        category.name = form.name.data
        category.position = position

        db.session.commit()
        
        return redirect(url_for('forumHomepage'))
    elif request.method == "GET":
        form.name.data = category.name
        form.position.data = category.position

    return render_template('Forum/create_category.html', form=form)


@app.route("/forum/category/<int:category_id>/delete")
@login_required
@check_priority('delete category')
def forumCategoryDelete(category_id:int):
    category = Category.query.get_or_404(category_id)
    
    last_position = Category.query.order_by('position').all()[-1].position
    for p in range(category.position + 1, last_position + 1):
        c = Category.query.filter_by(position=p).first()
        c.position -= 1

    for section in category.sections:
        for thread in section.threads:
            db.session.delete(thread)
        db.session.delete(section)
    db.session.delete(category)
    db.session.commit()
    
    return redirect(url_for('forumHomepage'))


### SECTION ###
@app.route("/forum/<string:section_slug>")
def forumSection(section_slug:str):
    page_number = request.args.get('page', 1, type=int)

    section = Section.query.filter_by(
        slug=section_slug).first_or_404()
    threads = Threads.query.filter_by(
        section_id=section.id, pinned=False).paginate(
            page_number, 6, True)
    print(threads)
    pinned_threads = Threads.query.filter_by(
        section_id=section.id, pinned=True).all()
    
    next_page = url_for('forumSection', section_slug=section_slug,
        page=threads.next_num) if threads.has_next else None
    
    prew_prev = url_for('forumSection', section_slug=section_slug, 
        page=threads.has_prev) if threads.has_prev else None
    
    page = {
        'current': page_number, 
        'next': next_page, 
        'prev': prew_prev
    }

    return render_template("Forum/section.html", threads=threads, 
        pinned_threads=pinned_threads, section=section,
        page=loadjson(page))


@app.route("/forum/category/<int:category_id>/create", methods=["GET", "POST"])
@login_required
@check_priority('create section')
def forumSectionCreate(category_id:int):
    form = SectionForm()

    if form.validate_on_submit():
        position = int(form.position.data)
        if Section.query.filter_by(category_id=category_id).all():
            real_last_position = Section.query.filter_by(
                category_id=category_id).order_by('position'
                    ).all()[-1].position + 1
            if position > real_last_position:
                position = real_last_position
            changePosition.section(position, category_id)

        new_section = Section(
            name=form.name.data,
            position=position,
            desc=form.desc.data,
            priority_required=form.priority_required.data,
            priority_required_create=form.priority_require_to_create.data,
            category_id=category_id)

        new_section.title_sluggifier()
        db.session.add(new_section)
        db.session.commit()

        return redirect(url_for('forumHomepage'))
    elif request.method == "GET":
        form.position.data = Section.query.filter_by(
            category_id=category_id).order_by('position')[-1].position + 1 \
                if Section.query.filter_by(category_id=category_id).all() else 1
        form.priority_required.data = 0
        form.priority_require_to_create.data = 0

    return render_template('Forum/create_section.html', form=form)


@app.route("/forum/<string:section_slug>/edit", methods=["GET", "POST"])
@login_required
@check_priority('edit section')
def forumSectionEdit(section_slug:str):
    form = SectionForm()
    section = Section.query.filter_by(
        slug=section_slug).first_or_404()
    
    if form.validate_on_submit():
        position = int(form.position.data)
        real_last_position = Section.query.filter_by(
            category_id=section.category_id).order_by('position'
            ).all()[-1].position + 1
        if position > real_last_position:
            position = real_last_position
        if position != section.position:
            changePosition.section(position, section.category_id, 
                section.position)

        section.name = form.name.data
        section.position = position
        section.priority_required = form.priority_required.data
        section.priority_required_create = form.priority_require_to_create.data

        db.session.commit()
        
        return redirect(url_for('forumHomepage'))
    elif request.method == "GET":
        form.name.data = section.name
        form.desc.data = section.desc
        form.position.data = section.position
        form.priority_required.data = section.priority_required
        form.priority_require_to_create.data = section.priority_required_create

    return render_template('Forum/create_section.html', form=form)


@app.route("/forum/<string:section_slug>/delete")
@login_required
@check_priority('delete section')
def forumSectionDelete(section_slug:str):
    section = Section.query.filter_by(
        slug=section_slug).first_or_404()

    last_position = Section.query.filter_by(category_id=section.category_id
        ).order_by('position').all()[-1].position
    for p in range(section.position + 1, last_position + 1):
        t = Section.query.filter_by(
            category_id=section.category_id, position=p).first()
        t.position -= 1

    for thread in section.threads:
        db.session.delete(thread)
    
    db.session.delete(section)
    db.session.commit()
    
    return redirect(url_for('forumHomepage'))


### THREAD ###
@app.route("/forum/thread/<string:thread_slug>/", methods=["GET", "POST"])
def forumThread(thread_slug:str):
    thread = Threads.query.filter_by(slug=thread_slug).first_or_404()
    user = Users.query.get_or_404(thread.user_id)
    form_comment = CommentsForm()
    form_subcomment = SubCommentsForm()

    if current_user.is_authenticated:
        thread.add_view(user_id=current_user.id)

    if form_comment.validate_on_submit() and not thread.closed:
        new_comment = Comments(
            text=form_comment.text.data,
            user_id=current_user.id,
            thread_id=thread.id
        )

        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('forumThread', thread_slug=thread.slug))
    
    elif form_subcomment.validate_on_submit() and not thread.closed:
        new_subcomment = Subcomments(
            text=form_subcomment.text.data,
            user_id=current_user.id,
            to_user_id=form_subcomment.to_user_id.data,
            comment_id=form_subcomment.comment_id.data
        )

        db.session.add(new_subcomment)
        db.session.commit()
        return redirect(url_for('forumThread', thread_slug=thread.slug))
        
    return render_template("Forum/thread.html", thread=thread, 
        comments=thread.comments, form_comment=form_comment, 
            form_subcomment=form_subcomment, user=user, Users=Users)


@app.route("/forum/thread/<string:section_slug>/create", methods=["GET", "POST"])
@login_required
def forumCreateThread(section_slug:str):
    form = ThreadForm()
    section = Section.query.filter_by(slug=section_slug).first_or_404()

    if form.validate_on_submit():
        new_thread = Threads(
            text=form.text.data,
            title=form.title.data,
            user_id=current_user.id,
            section_id=section.id)
        
        if current_user.check_perm('pin thrad'):
            new_thread.pinned = form.pinned.data

        new_thread.title_sluggifier()

        if form.img.data:
            try:
                img = saveFile(form.img.data)
                
            except Exception:
                db.session.add(new_thread)
                db.session.commit()
                flash(Error.img_error, Error.name)
                return redirect(url_for(forumEditThread, 
                    thread_slug=new_thread.slug))
            else:
                new_thread.img = img

        db.session.add(new_thread)
        db.session.commit()

        return redirect(url_for('forumThread', thread_slug=new_thread.slug))
    return render_template("Forum/create_thread.html", form=form, section_id=section.id)


@app.route("/forum/thread/<string:thread_slug>/edit", methods=["GET", "POST"])
@login_required
def forumEditThread(thread_slug:str):
    form = ThreadForm()
    thread = Threads.query.filter_by(slug=thread_slug).first_or_404()

    if thread.user_id != current_user.id:
        return abort(404)

    if form.validate_on_submit():
        thread.text = form.text.data
        thread.title = form.title.data
        #TODO Only admin
        thread.pinned = form.pinned.data
        
        if form.img.data:
            try:
                img = saveFile(form.img.data)
                
            except Exception:
                db.session.commit()
                flash(Error.img_error, Error.name)
                return redirect(url_for(forumEditThread, 
                    thread_slug=thread.slug))
            else:
                thread.img = img

        db.session.commit()

        return redirect(url_for('forumThread', thread_slug=thread.slug))
    elif request.method == "GET":
        form.title.data = thread.title
        form.text.data = thread.text

        #TODO Only admin
        form.pinned.data = thread.pinned

    return render_template("Forum/create_thread.html", form=form)


@app.route("/forum/thread/<int:thread_id>/delete")
@login_required
def forumDeleteThread(thread_id:int):
    thread = Threads.query.get_or_404(thread_id)
    section_id = thread.section_id

    if thread.user_id == current_user.id or \
            current_user.check_perm('delete thread'):
        db.session.delete(thread)
        db.session.commit()
    
    return redirect(url_for('forumSection', section_id=section_id))


@app.route("/forum/thread/<int:thread_id>/close")
@login_required
def forumCloseThread(thread_id:int):
    thread = Threads.query.get_or_404(thread_id)

    if thread.user_id == current_user.id or \
            current_user.check_perm('delete thread'):
        thread.closed = True
        db.session.commit()
    
    return redirect(url_for('forumThread', thread_slug=thread.slug))


@app.route("/forum/thread/<int:thread_id>/open")
@login_required
@check_priority('open thread')
def forumOpenThread(thread_id:int):
    thread = Threads.query.get_or_404(thread_id)

    thread.closed = False
    db.session.commit()

    return redirect(url_for('forumThread', thread_slug=thread.slug))
