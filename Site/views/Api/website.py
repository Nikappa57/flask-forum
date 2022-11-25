from flask import jsonify, request, url_for, abort
from flask_login import current_user

from Site import app, db
from Site.models.cmt_upvote import CmtUpvote
from Site.models.sub_upvote import SubUpvote
from Site.models.subcomment import Subcomments
from Site.models.comment import Comments


#TODO only POST

@app.route("/api/subcomment/<int:comment_id>/<int:to_user_id>" + \
    "/<string:text>/")
def create_subcomment(comment_id:int, to_user_id:int, text:str):
    new_comment = Subcomments(
        user_id=current_user.id,
        comment_id=comment_id,
        to_user_id=to_user_id,
        text=text
    )

    db.session.add(new_comment)
    db.session.commit()
    
    return ""

@app.route("/api/comment/delete/<int:comment_id>/")
def delete_comment(comment_id:int): 
    comment = Comments.query.get_or_404(comment_id)
    #TODO only admin or user
    if current_user.id != comment.user_id:
        return abort(401)

    for sc in comment.subcomments:
        for up in sc.upvote:
            db.session.delete(up)
        db.session.delete(sc)
    for up in comment.upvote:
        db.session.delete(up)

    db.session.delete(comment)
    db.session.commit()

    return ""

@app.route("/api/subcomment/delete/<int:comment_id>/")
def delete_subcomment(comment_id:int): 
    comment = Subcomments.query.get_or_404(comment_id)
    #TODO only admin or user
    if current_user.id != comment.user_id:
        return abort(401)

    for up in comment.upvote:
        db.session.delete(up)

    db.session.delete(comment)
    db.session.commit()
    
    return ""

@app.route("/api/upvote/comment/<int:comment_id>/")
def add_cmtupvote(comment_id):
    print("Creazione upvote commento")
    comment = Comments.query.get_or_404(comment_id)
    vote = comment.check_upvote(current_user.id)
    if vote:
        db.session.delete(vote)
        db.session.commit()
        return ""
    
    new_upvote = CmtUpvote(user_id=current_user.id, comment_id=comment_id)
    db.session.add(new_upvote)
    db.session.commit()
    
    return ""

@app.route("/api/upvote/subcomment/<int:comment_id>/")
def add_subupvote(comment_id):
    comment = Subcomments.query.get_or_404(comment_id)
    vote = comment.check_upvote(current_user.id)
    if vote:
        db.session.delete(vote)
        db.session.commit()
        return ""
    
    new_upvote = SubUpvote(user_id=current_user.id, comment_id=comment_id)
    db.session.add(new_upvote)
    db.session.commit()
    return ""

