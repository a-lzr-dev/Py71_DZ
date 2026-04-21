from flask import Blueprint, render_template, request, g, redirect, abort

from src.services.posts import post_service

blueprint = Blueprint('posts', __name__)


@blueprint.route("/posts")
def list_posts_view():
    if g.current_user is None:
        return redirect("/login")

    posts = post_service.get_user_posts_list(g.current_user.id)
    return render_template("posts/list.html", posts=posts)


@blueprint.route('/posts/create', methods=["GET", "POST"])
def create_new_post_view():
    if g.current_user is None:
        return redirect("/login")

    template_name = "posts/create.html"

    print("Функция create_new_post_view, метод:", request.method)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        print("title:", title)
        print("content:", content)

        if not title or not content:
            return render_template(template_name, error="Заголовок и содержимое должны быть переданы!")
        if len(title) > 80:
            return render_template(template_name, error="Длина заголовки должна быть не более 80 символов.")

        # --------------------
        post = post_service.create_new_post(title, content, g.current_user.id)

        return redirect(f"/posts/{post.id}")

    return render_template(template_name)


@blueprint.route('/posts/<int:post_id>', methods=["GET"])
def get_post_by_id_view(post_id: int):
    if g.current_user is None:
        return redirect("/login")

    post = post_service.get_post_by_id(post_id)
    if post is None:
        abort(404)

    if g.current_user.id != post.user_id:
        abort(404)

    return render_template("posts/view.html", post=post)


@blueprint.route('/posts/edit/<int:post_id>', methods=["GET", "POST"])
def edit_post_by_id_view(post_id: int):
    if g.current_user is None:
        return redirect("/login")

    post = post_service.get_post_by_id(post_id)
    if post is None:
        abort(404)

    if g.current_user.id != post.user_id:
        abort(404)

    template_name = "posts/edit.html"

    print("Функция edit_post_by_id_view, метод:", request.method)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        print("title:", title)
        print("content:", content)

        if not title or not content:
            return render_template(template_name, error="Заголовок и содержимое должны быть переданы!")
        if len(title) > 80:
            return render_template(template_name, error="Длина заголовки должна быть не более 80 символов.")

        # --------------------
        post = post_service.edit_post(post, title, content)

        return redirect(f"/posts/{post.id}")

    return render_template(template_name, post=post, post_id=post_id)

@blueprint.route('/posts/delete/<int:post_id>', methods=["GET", "POST"])
def delete_post_by_id_view(post_id: int):
    if g.current_user is None:
        return redirect("/login")

    post = post_service.get_post_by_id(post_id)
    if post is None:
        abort(404)

    if g.current_user.id != post.user_id:
        abort(404)

    template_name = "posts/delete.html"

    print("Функция delete_post_by_id_view, метод:", request.method)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        print("title:", title)
        print("content:", content)

        if not title or not content:
            return render_template(template_name, error="Заголовок и содержимое должны быть переданы!")
        if len(title) > 80:
            return render_template(template_name, error="Длина заголовки должна быть не более 80 символов.")

        # --------------------
        post_service.delete_post(post_id)

        return redirect(f"/posts")

    return render_template(template_name, post=post, post_id=post_id)
