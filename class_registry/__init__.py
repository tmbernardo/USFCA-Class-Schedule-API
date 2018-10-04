from class_registry import dbhandler as db
from flask import Flask

import markdown
import os
import sys
import time

app = Flask(__name__)


@app.before_first_request
def _run_on_start():
    for _ in range(60):
        try:
            db.create_tables()
            return
        except Exception as e:
            time.sleep(1)
            continue
    print('TIMEOUT: could not connect to database after 1 minute', file=sys.stderr)

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


if __name__ == "__main__":
    app.run(debug = True)
