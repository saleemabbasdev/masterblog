import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_posts():
    with open('posts.json', 'r') as file:
        return json.load(file)


def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    for post in load_posts():
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        # Unique id: highest existing id + 1 (1 if the list is empty)
        new_id = max((p['id'] for p in posts), default=0) + 1
        posts.append({
            'id': new_id,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content'),
        })
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    posts = [p for p in posts if p['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        posts = load_posts()
        for p in posts:
            if p['id'] == post_id:
                p['author'] = request.form.get('author')
                p['title'] = request.form.get('title')
                p['content'] = request.form.get('content')
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
