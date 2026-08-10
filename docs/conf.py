project = 'The Plant Matrix Database'
copyright = '2026, The Plant Matrix'
author = 'The Plant Matrix'

# This ensures ReadTheDocs can build a basic structure
extensions = []
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# This variable passes authority to your main site globally
html_context = {
    "display_github": True,
    "github_user": "your-github-username",
    "github_repo": "your-repo-name",
    "github_version": "main",
    "conf_py_path": "/docs/",
}
