from class_registry import dbhandler as db
from flask import Flask

import markdown
import os

app = Flask(__name__)

@app.route("/")
def index():
    """Present some documentation"""

    db.create_tables()

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)

if __name__ == '__main__':
    app.run(debug = True)
