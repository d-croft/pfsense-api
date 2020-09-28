import argparse
import pathlib
import os
import subprocess

# Variables
args = None
css = """
<style>
    body {
        display: block;
        width: 90%;
        margin: 0 auto;
    }
    footer {
        display:none;
    }
    div.col-md-12 {
        margin-top: 20px;
    }

    li:before {
        content:"• ";
    }

    summary:hover {
        cursor: pointer;
        color: darkred;
    }

    details[open] summary ~ * {
      animation: open 0.3s ease-in-out;
    }

    @keyframes open {
      0% {
        opacity: 0;
      }
      100% {
        opacity: 1;
      }
    }

    details summary::-webkit-details-marker {
      display: none;
    }

    details summary {
      width: 100%;
      padding: 0.5rem 0;
      border-top: 1px solid black;
      position: relative;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      list-style: none;
    }

    details summary:before {
      content: "+ ";
      color: black;
      position: relative;
      font-size: 12px;
      line-height: 0;
      margin-top: 0.75rem;
      font-weight: 400;
      transform-origin: center;
      transition: 200ms linear;
    }

    details[open] summary:before {
      content: "- ";
      font-size: 12px;
    }

    details summary {
      outline: 0;
    }

    details p {
      font-size: 14px;
      margin: 0 0 1rem;
      padding-top: 1rem;
    }
</style>
"""

# Parses command line arguments and generates help pages
def start_argparse():
    global args
    # Custom file path type for argparse
    def fp(value_string):
        if not pathlib.Path(value_string).exists():
            raise argparse.ArgumentTypeError("No file found at %s" % value_string)
        return value_string

    parser = argparse.ArgumentParser(description="Converts Postman collection to embedded API documentation")
    parser.add_argument('--json', dest="json", type=fp, required=True, help="Path to the Postman collection JSON file")
    args = parser.parse_args()

# Runs our docgen command to convert the Postman collection to HTML and Markdown
def run_docgen():
    docgen_html = subprocess.check_output(
        ["docgen", "build", "-i", args.json, "-o", "documentation.html"],
        stderr=subprocess.STDOUT
    )
    docgen_md = subprocess.check_output(
        ["docgen", "build", "-i", args.json, "-o", "documentation.md", "-m"],
        stderr=subprocess.STDOUT
    )
    print(docgen_html.decode().replace("html", "php").replace("\n", ""))
    print(docgen_md.decode().replace("\n", ""))

# Formats the docs docgen created to add custom CSS and other content overrides
def format_docs():
    # Read the contents of the HTML document docgen created, then delete the file
    with open("documentation.html", "r") as dr:
        html_doc = dr.read()
    os.remove("documentation.html")

    # Write a new PHP script containing the HTML created by docgen, then override custom attributes and CSS
    with open("documentation.php", "w") as dw:
        html_doc = "<?php\n?>\n" + html_doc
        html_doc = html_doc + css
        html_doc = html_doc.replace("{{$hostname}}", "<?echo $_SERVER['HTTP_HOST'];?>")
        dw.write(html_doc)

# Moves the docs to their appropriate location
def move_docs():
    php_path = pathlib.Path("documentation.php").absolute()
    md_path = pathlib.Path("documentation.md").absolute()
    root_dir = pathlib.Path(__file__).absolute().parent.parent
    os.rename(md_path, root_dir.joinpath("README.md"))
    os.rename(php_path, root_dir.joinpath("pfSense-pkg-API/files/usr/local/www/api/documentation/index.php"))

# RUN TIME
start_argparse()
run_docgen()
format_docs()
move_docs()
