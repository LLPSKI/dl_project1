import author
from flask import Flask, render_template, request

# author_name = 'Ya-qin Zhang'
app = Flask(__name__)
authors: list[author.Author] = None

@app.route('/')
def root():
    return render_template('root.html')

@app.route('/submit', methods=['POST'])
def handle_submit():
    print("Get submit!")
    author_name = request.form['author_name']  # 获取用户输入
    global authors
    authors = author.search_author(author_name)
    print("OK!")
    if authors:
        return render_template('author_found.html', a=authors)
    else:
        return render_template('author_nofound.html', a=author_name)

@app.route('/track', methods=['POST'])
def track_click():
    print("Get track!")
    author_name = request.form.get('author_name')
    global authors
    for author in authors:
        if author.name == author_name:
            print('Here')
            author.load_pages()
            return render_template('author_info.html', a=author.pages, b=author_name)
    return render_template('author_nofound.html', a=author_name)

if __name__ == '__main__':
    app.run()

