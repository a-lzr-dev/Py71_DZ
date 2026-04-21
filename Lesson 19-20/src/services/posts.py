from src.db import db
from src.models import Post


class PostService:

    @staticmethod
    def get_user_posts_list(user_id: int) -> list[Post]:
        posts = Post.query.filter_by(user_id=user_id).all()
        return posts

    @staticmethod
    def get_post_by_id(id_: int) -> Post | None:
        post = Post.query.get(id_)
        return post

    @staticmethod
    def create_new_post(title: str, content: str, user_id: int) -> Post:
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def edit_post(post: Post, title: str, content: str) -> Post:
        post.title = title
        post.content = content
        db.session.commit()
        return post

    @staticmethod
    def delete_post(id_: int) -> Post | None:
        post = Post.query.get(id_)
        if post is None:
            return None
        db.session.delete(post)
        db.session.commit()
        return post


post_service = PostService()
