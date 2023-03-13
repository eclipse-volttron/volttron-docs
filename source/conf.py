# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import os
import subprocess

# from mock import Mock as MagicMock

#
# class Mock(MagicMock):
#     @classmethod
#     def __getattr__(cls, name):
#             return Mock()

#
# autodoc_mock_imports = ['loadshape', 'numpy', 'sympy', 'xlrd', 'stomp', 'oadr2', 'pyodbc', 'lxml', 'pytest',
#                         'pint', 'pandas', 'suds', 'paho', 'pymongo', 'bson', 'subprocess32', 'heaters', 'meters',
#                         'hvac', 'blinds', 'vehicles']

# -- Project information -----------------------------------------------------


project = 'VOLTTRON'
copyright = '2022, The VOLTTRON Community'
author = 'The VOLTTRON Community'

# The short X.Y version
version = '8.2'
# The full version, including alpha/beta/rc tags
release = '8.2'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    # https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
    'sphinx.ext.autosectionlabel',
    # http://www.sphinx-doc.org/en/master/usage/extensions/todo.html
    'sphinx.ext.todo',
    'm2r2'
]

# prefix sections with the document so that we can cross link
# sections from different pages.
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 5

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ['.rst', '.md']

# The top-level toctree document.
main_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ["custom.css"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'VOLTTRONdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (main_doc, 'VOLTTRON.tex', 'VOLTTRON Documentation',
     'The VOLTTRON Community', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (main_doc, 'volttron', 'VOLTTRON Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (main_doc, 'VOLTTRON', 'VOLTTRON Documentation',
     author, 'VOLTTRON', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/3.6': None,
                       'volttron-ansible': ('https://volttron.readthedocs.io/projects/volttron-ansible/en/main/',
                                            None)}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Custom code generation ----------------------------------------------


# Custom event handlers for Volttron #
def setup(app):
    """
    Registers callback method on sphinx events. callback method used to
    dynamically generate api-docs rst files which are then converted to html
    by readthedocs
    :param app:
    """
    # app.connect('builder-inited', generate_apidoc)
    app.connect('builder-inited', generate_volttron_docs)

    # app.connect('build-finished', clean_api_rst)
    app.connect('build-finished', clean_volttron_docs_rst)


script_dir = os.path.dirname(os.path.realpath(__file__))
vdocs_root = os.path.join(script_dir, "volttron-docs")
vdocs_source_abs_path = os.path.join(vdocs_root, "docs/source")
vagent_readme = os.path.join(script_dir, "volttron-api")


def generate_volttron_docs(app):
    import shutil
    global script_dir, vdocs_root, vdocs_source_subdir, vdocs_source_abs_path, vagent_readme
    volttron_version = "releases/8.2"
    volttron_repo = "https://github.com/volttron/volttron"

    subprocess.check_call(["git", "clone", "--no-checkout", volttron_repo, vdocs_root], cwd=script_dir)
    subprocess.check_call(["git", "sparse-checkout", "set", "--no-cone", "docs/source/*", "docs/requirements.txt",
                           '!conf.py', '!api_doc_config.yml', '!apidocs-templates'], cwd=vdocs_root)
    subprocess.check_call(["git", "checkout", volttron_version], cwd=vdocs_root)
    # mv everything from volttron/docs/source directory into this repo's source directory(i.e. dir of this conf.py)
    shutil.copytree(vdocs_source_abs_path, script_dir, dirs_exist_ok=True)

    # Grab readme files for core agents
    os.mkdir(vagent_readme)
    subprocess.check_call(["git", "clone", "--no-checkout", volttron_repo, "volttron-api"], cwd=script_dir)
    subprocess.check_call(["git", "sparse-checkout", "set", "--no-cone",
                           "services/core/**/README.md",
                           "services/ops/**/README.md"], cwd=vagent_readme)
    subprocess.check_call(["git", "checkout", volttron_version], cwd=vagent_readme)

    # Remove unwanted agents
    core_dir = os.path.join(vagent_readme, "services/core")
    shutil.rmtree(os.path.join(core_dir, "DNP3Agent"), ignore_errors=True)
    shutil.rmtree(os.path.join(core_dir, "MarketServiceAgent"), ignore_errors=True)
    shutil.rmtree(os.path.join(core_dir, "OpenEISHistorian"), ignore_errors=True)
    shutil.rmtree(os.path.join(core_dir, "ObixHistoryPublish"), ignore_errors=True)
    shutil.rmtree(os.path.join(core_dir, "IEEE2030_5Agent"), ignore_errors=True)

    # update index.rst to point to README.md instead of generated api-docs
    index_rst = os.path.join(script_dir, 'index.rst')
    with open(index_rst, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('volttron-api/ops/*/modules', 'volttron-api/services/ops/**/README')
    filedata = filedata.replace('volttron-api/services/*/modules', 'volttron-api/services/core/**/README')

    # Write the file out again
    with open(index_rst, 'w') as file:
        file.write(filedata)


def clean_volttron_docs_rst(app, exception):
    """
    Deletes folder containing all auto generated .rst files at the end of
    sphinx build immaterial of the exit state of sphinx build.
    :param app:
    :param exception:
    """
    global vdocs_root, vdocs_source_abs_path, script_dir, vagent_readme
    import shutil
    copied_files = os.listdir(vdocs_source_abs_path)
    for f in copied_files:
        print(f"Cleanup: Removing file copied into {script_dir} {f}")
        # remove everything that was copied from volttron docs/source to this scripts parent's dir
        file_path = os.path.join(script_dir, f)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)

    if os.path.exists(vdocs_root):
        print("Cleanup: Removing volttron docs clone directory {}".format(vdocs_root))
        shutil.rmtree(vdocs_root)

    if os.path.exists(vagent_readme):
        print("Cleanup: Removing volttron api clone directory {}".format(vagent_readme))
        shutil.rmtree(vagent_readme)

# apidocs_base_dir = os.path.abspath(script_dir + "/volttron-api")
# volttron_root = os.path.abspath(os.path.join(script_dir, "../.."))
#
#
# def generate_apidoc(app):
#     """
#     Generates apidocs for modules under volttron/platform
#     and volttron/services/core
#     :param app:
#     :return:
#     """
#
#     print("\n##In run_apidocs##\n")
#     clean_api_rst(app, None)
#     global script_dir, apidocs_base_dir
#
#     os.makedirs(apidocs_base_dir, 0o755)
#     config = _read_config(filename = os.path.join(script_dir, "api_doc_config.yml"))
#     # generate api-docs for each api docs directory
#     for docs_subdir in config.keys():
#         docs_subdir_path = os.path.join(apidocs_base_dir, docs_subdir)
#         agent_dirs = glob(os.path.join(volttron_root, config[docs_subdir]["path"], "*/"))
#         file_excludes = []
#         if config[docs_subdir].get("file_excludes"):
#             for exclude_pattern in config[docs_subdir].get("file_excludes", []):
#                 file_excludes.append(os.path.join(volttron_root, config[docs_subdir]["path"], exclude_pattern))
#         print("after file excludes. calling apidoc")
#         agent_excludes = \
#             config[docs_subdir].get("agent_excludes") if config[docs_subdir].get("agent_excludes", []) else []
#         run_apidoc(docs_subdir_path, agent_dirs, agent_excludes, file_excludes)
#         print("COMPLETED RUNNING API DOC")
#
#
# def run_apidoc(docs_dir, agent_dirs, agent_excludes, exclude_pattern):
#     """
#     Runs sphinx-apidoc on all subdirectories under the given directory.
#     commnad runs with --force and exclude any setup.py file in the subdirectory
#     :param docs_dir: The base directory into with .rst files are generated.
#     :param agent_dirs: directory to search for packages to document
#     :param agent_excludes: agent directories to be skipped
#     :param exclude_pattern: file name patterns to be excluded. This passed on to sphinx-apidoc command for exclude
#     """
#     print(f"In run apidoc params {docs_dir}, {agent_dirs}, {agent_excludes}, {exclude_pattern}")
#     for agent_src_dir in agent_dirs:
#         agent_src_dir = os.path.abspath(agent_src_dir)
#         agent_src_dir = agent_src_dir[:-1] if agent_src_dir.endswith("/") else agent_src_dir
#         name = os.path.basename(agent_src_dir)
#         agent_doc_dir = os.path.join(docs_dir, name)
#         if name not in agent_excludes:
#             sys.path.insert(0, agent_src_dir)
#             cmd = ["sphinx-apidoc", '-e', '-a', '-M', '-d 4',
#                    '-t', os.path.join(script_dir, 'apidocs-templates'),
#                    '--force', '-o', agent_doc_dir, agent_src_dir,
#                    os.path.join(agent_src_dir, "setup.py"), os.path.join(agent_src_dir, "conftest.py")
#                    ]
#
#             cmd.extend(exclude_pattern)
#             subprocess.check_call(cmd)
#             grab_agent_readme(agent_src_dir, agent_doc_dir)
#
#
# def grab_agent_readme(agent_src_dir, agent_doc_dir):
#     src = os.path.join(agent_src_dir, "README.md")
#     dst = os.path.join(agent_doc_dir, "README.md")
#     os.symlink(src, dst)
#     with open(os.path.join(agent_doc_dir, "modules.rst"), "a") as f:
#         f.write("   Agent README <README>")
#
#
# def clean_api_rst(app, exception):
#     """
#     Deletes folder containing all auto generated .rst files at the end of
#     sphinx build immaterial of the exit state of sphinx build.
#     :param app:
#     :param exception:
#     """
#     global apidocs_base_dir
#     import shutil
#     if os.path.exists(apidocs_base_dir):
#         print("Cleanup: Removing apidocs directory {}".format(apidocs_base_dir))
#         shutil.rmtree(apidocs_base_dir)
