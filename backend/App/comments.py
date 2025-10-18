# backend/app/comments.py
from flask import Blueprint, request, jsonify, current_app # type: ignore
from . import db
from .models import Comment
from sqlalchemy.exc import SQLAlchemyError # type: ignore

comments_bp = Blueprint('comments', __name__)

def _bad_request(msg):
    return jsonify({"error": msg}), 400

@comments_bp.route('/', methods=['POST'])
def create_comment():
    data = request.get_json() or {}
    task_id = data.get('task_id')
    text = data.get('text')
    author = data.get('author')

    if not task_id:
        return _bad_request("task_id is required")
    if not text or not isinstance(text, str) or not text.strip():
        return _bad_request("text is required and must be non-empty")

    comment = Comment(task_id=task_id, text=text.strip(), author=author)
    try:
        db.session.add(comment)
        db.session.commit()
    except SQLAlchemyError as e:
        current_app.logger.exception("DB error creating comment")
        db.session.rollback()
        return jsonify({"error": "db_error"}), 500

    return jsonify(comment.to_dict()), 201

@comments_bp.route('/task/<int:task_id>', methods=['GET'])
def get_comments_for_task(task_id):
    comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.asc()).all()
    return jsonify([c.to_dict() for c in comments]), 200

@comments_bp.route('/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "not_found"}), 404

    data = request.get_json() or {}
    text = data.get('text')
    author = data.get('author')

    if text is not None:
        if not isinstance(text, str) or not text.strip():
            return _bad_request("text must be a non-empty string")
        comment.text = text.strip()
    if author is not None:
        comment.author = author

    try:
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("DB error updating comment")
        db.session.rollback()
        return jsonify({"error": "db_error"}), 500

    return jsonify(comment.to_dict()), 200

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "not_found"}), 404
    try:
        db.session.delete(comment)
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("DB error deleting comment")
        db.session.rollback()
        return jsonify({"error": "db_error"}), 500
    return '', 204
