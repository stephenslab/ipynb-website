import os
import glob
import re
import json

def get_output(cmd, show_command=False, prompt='$ '):
    import subprocess
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, shell=True).decode()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e)
    if show_command:
        return '{}{}\n{}'.format(prompt, cmd, output)
    else:
        return output.strip()

def get_commit_link(repo, cid):
    bits = os.path.split(repo)
    if "github.com" or "gitlab.com" in bits:
        return "{}/commit/{}".format(repo, cid)
    elif "bitbucket.org" in bits:
        return "{}/commits/{}".format(repo, cid)
    else:
        return repo

def get_notebook_link(repo, cid, fn):
    bits = os.path.split(repo)
    if "github.com" or "gitlab.com" in bits:
        link = "{}/blob/{}/{}".format(repo, cid, fn)
        return '<a href=\\"{}\\"><code>{}</code></a>'.format(link, fn)
    else:
        return '<code>{}</code>'.format(fn)

def get_commit_info(fn, conf):
    out = ''
    if conf['add_commit_info']:
        try:
            long_fmt = get_output('git log -n 1 --pretty=format:%H -- {}'.format(fn))
            short_fmt = get_output('git log -n 1 --pretty=format:%h -- {}'.format(fn))
            rev_string = 'by {} on {} <a href=\\"{}\\">revision {}, {}</a>'.\
                       format(get_output('git log -n 1 --format="%an" {}'.format(long_fmt)),
                              get_output('git show -s --format="%cd" --date=local {}'.format(long_fmt)),
                              get_commit_link(conf['repo'], long_fmt),
                              get_output('git rev-list --count {}'.format(long_fmt)), short_fmt)
            out = '<p><small>Exported from {} committed {} {}</small></p>'.\
                  format(get_notebook_link(conf['repo'], long_fmt, fn), rev_string,
                         '<a href=\\"{}\\">{}</a>'.\
                         format(conf['__about_commit__'], '<span class=\\"fa fa-question-circle\\"></span>')
                         if conf['__about_commit__'] else '')
        except:
            raise
            # if git related command fails, indicating it is not a git repo
            # I'll just pass ...
            pass
    return out.replace('/', '\/')

def get_nav(dirs, home_label, prefix = './'):
    out = '''
<li>
  <a href="{}index.html">{}</a>
</li>
    '''.format(prefix, home_label)
    for item in dirs:
        out += '''
<li>
  <a href="{}{}.html">{}</a>
</li>
        '''.format(prefix, item, item.capitalize())
    return out

def get_font(font):
    if font is None:
        return ''
    else:
        return 'font-family: "{}";'.format(font)

def get_sidebar(path):
    return '''
<script>
$( document ).ready(function(){
            var cfg={'threshold':{{ nb.get('metadata', {}).get('toc', {}).get('threshold', '3') }},     // depth of toc (number of levels)
             'number_sections': false,
             'toc_cell': false,          // useless here
             'toc_window_display': true, // display the toc window
             "toc_section_display": "block", // display toc contents in the window
             'sideBar':true,       // sidebar or floating window
             'navigate_menu':false       // navigation menu (only in liveNotebook -- do not change)
            }
            var st={};                  // some variables used in the script
            st.rendering_toc_cell = false;
            st.config_loaded = false;
            st.extension_initialized=false;
            st.nbcontainer_marginleft = $('#notebook-container').css('margin-left')
            st.nbcontainer_marginright = $('#notebook-container').css('margin-right')
            st.nbcontainer_width = $('#notebook-container').css('width')
            st.oldTocHeight = undefined
            st.cell_toc = undefined;
            st.toc_index=0;
            // fire the main function with these parameters
            table_of_contents(cfg, st);
            var file=%sDict[$("h1:first").attr("id")];
            $("#toc-level0 a").css("color","#126dce");
            $('a[href="#'+$("h1:first").attr("id")+'"]').hide()
            var docs=%sArray;
            var pos=%sArray.indexOf(file);
            for (var a=pos;a>=0;a--){
                  var name=docs[a]
                  $('<li><a href="'+name+'.html"><font color="#073642"><b>'+name.replace(/_/g," ")+'</b></font></a></li>').insertBefore("#toc-level0 li:eq(0)");
            }
            $('a[href="'+file+'.html'+'"]').css("color","#126dce");
            for (var a=pos+1;a<docs.length;a++){
                  var name=docs[a]
                  $(".toc #toc-level0").append('<li><a href="'+name+'.html"><font color="#073642"><b>'+name.replace(/_/g," ")+'</b></font></a></li>');
            }
            $("#toc-header").hide();
    });
</script>
''' % (path, path, path)

def get_disqus(name):
    if name is None:
        return ''
    return '''
  <div id="disqus_thread"></div>
    <script type="text/javascript">
        /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
        var disqus_shortname = '%s'; // required: replace example with your forum shortname

        /* * * DON'T EDIT BELOW THIS LINE * * */
        (function() {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();
    </script>
    <noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
    <a href="http://disqus.com" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>''' % name

def get_index_tpl(conf, dirs):
    '''Generate index template at given paths'''
    content = '''
{%%- extends 'basic.tpl' -%%}

{%%- block header -%%}
{{ super() }}

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="ipynb_website:version" content="%s" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<title>%s</title>

<script src="site_libs/jquery-1.11.3/jquery.min.js"></script>
<link href="site_libs/bootstrap-3.3.5/css/%s.min.css" rel="stylesheet" />
<script src="site_libs/bootstrap-3.3.5/js/bootstrap.min.js"></script>
<script src="site_libs/bootstrap-3.3.5/shim/html5shiv.min.js"></script>
<script src="site_libs/bootstrap-3.3.5/shim/respond.min.js"></script>
<link href="site_libs/font-awesome-4.5.0/css/font-awesome.min.css" rel="stylesheet" />

<style type="text/css">code{white-space: pre;}</style>
<link rel="stylesheet"
      href="site_libs/highlight/textmate.css"
      type="text/css" />
<script src="site_libs/highlight/highlight.js"></script>
<style type="text/css">
  div.input_prompt {display: none;}
  div.output_html {
     font-family: "PT Mono", monospace;
     font-size: 10.0pt;
     color: #353535;
     padding-bottom: 25px;
 }
  pre:not([class]) {
    background-color: white;
  }
</style>
<script type="text/javascript">
if (window.hljs && document.readyState && document.readyState === "complete") {
   window.setTimeout(function() {
      hljs.initHighlighting();
   }, 0);
}
</script>
<script>
    MathJax.Hub.Config({
        extensions: ["tex2jax.js"],
        jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {
        inlineMath: [ ['$','$'], ["\\\\(","\\\\)"] ],
        displayMath: [ ['$$','$$'] ["\\\\[","\\\\]"] ],
        processEscapes: true
        },
        "HTML-CSS": {
            preferredFont: "TeX",
            availableFonts: ["STIX","TeX"],
            styles: {
                scale: 110,
                ".MathJax_Display": {
                    "font-size": "110%%",
                }
            }
        }
    });
</script>
</head>

<body>
<style type = "text/css">
@font-face {
 font-family: 'Droid Sans';
 font-weight: normal;
 font-style: normal;
 src: local('Droid Sans'), url('fonts/droid-sans.ttf') format('truetype');
}
@font-face {
 font-family: 'Fira Code';
 font-weight: normal;
 font-style: normal;
 src: local('Fira Code'), url('fonts/firacode.otf') format('opentype');
}
@font-face {
 font-family: 'PT Mono';
 font-weight: normal;
 font-style: normal;
 src: local('PT Mono'), url('fonts/ptmono.ttf') format('truetype');
}

body {
  %s
  font-size: 160%%;
  padding-top: 66px;
  padding-bottom: 40px;
}

h1 {
  margin-top: 25px;
  margin-bottom: 30px;
}

h2 {
  margin-bottom: 25px;
}

a.anchor-link:link {
  text-decoration: none;
  padding: 0px 20px;
  visibility: hidden;
}

h1:hover .anchor-link,
h2:hover .anchor-link,
h3:hover .anchor-link,
h4:hover .anchor-link,
h5:hover .anchor-link,
h6:hover .anchor-link {
  visibility: visible;
}

.main-container {
  max-width: 940px;
  margin-left: auto;
  margin-right: auto;
}
code {
  color: inherit;
  background-color: rgba(0, 0, 0, 0.04);
}
img {
  max-width:100%%;
  height: auto;
}
.tabbed-pane {
  padding-top: 12px;
}
button.code-folding-btn:focus {
  outline: none;
}
</style>

<script>
// manage active state of menu based on current page
$(document).ready(function () {
  // active menu anchor
  href = window.location.pathname
  href = href.substr(href.lastIndexOf('/') + 1)
  if (href === "")
    href = "index.html";
  var menuAnchor = $('a[href="' + href + '"]');

  // mark it active
  menuAnchor.parent().addClass('active');

  // if it's got a parent navbar menu mark it active as well
  menuAnchor.closest('li.dropdown').addClass('active');
});
</script>

<div class="container-fluid main-container">

<!-- tabsets -->
<script src="site_libs/navigation-1.1/tabsets.js"></script>
<script>
$(document).ready(function () {
  window.buildTabsets("TOC");
});
</script>

<!-- code folding -->

<div class="navbar navbar-default  navbar-fixed-top" role="navigation">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="index.html">%s</a>
    </div>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        %s
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li>
    <a href="%s">
    %s
    </a>
    </li>
    </ul>
    </div><!--/.nav-collapse -->
  </div><!--/.container -->
</div><!--/.navbar -->

{%%- endblock header -%%}
{%% block footer %%}
<hr>
%s
<!-- To enable disqus, uncomment the section below and provide your disqus_shortname -->
%s
</div>

<script>
// add bootstrap table styles to pandoc tables
$(document).ready(function () {
  $('tr.header').parent('thead').parent('table').addClass('table table-condensed');
});
</script>

<!-- dynamically load mathjax for compatibility with self-contained -->
<script>
  (function () {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src  = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML";
    document.getElementsByTagName("head")[0].appendChild(script);
  })();
</script>
</body>
</html>
{%% endblock %%}
	''' % (conf['__version__'], conf['name'], conf['theme'], get_font(conf['font']), conf['name'],
           get_nav([x for x in dirs if not x in conf['hide_navbar']], conf['homepage_label']),
           conf['repo'], conf['source_label'], conf['footer'],
           get_disqus(conf['disqus']))
    return content

def get_notebook_tpl(conf, dirs, path):
    '''Generate notebook template at given path'''
    content = '''
{%%- extends 'basic.tpl' -%%}

{%%- block header -%%}
{{ super() }}
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="ipynb_website:version" content="%s" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<link rel="stylesheet" type="text/css" href="../css/jt.css">
%s
<link rel="stylesheet" type="text/css" href="../css/toc2.css">

<link href="../site_libs/jqueryui-1.11.4/jquery-ui.css">
<link rel="stylesheet" href="../site_libs/bootstrap-3.3.5/css/%s.min.css" rel="stylesheet" />
<link rel="stylesheet" href="../site_libs/font-awesome-4.5.0/css/font-awesome.min.css" rel="stylesheet" />
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.9.1/jquery-ui.min.js"></script>
<script src="../site_libs/bootstrap-3.3.5/js/bootstrap.min.js"></script>
<script src="../site_libs/bootstrap-3.3.5/shim/html5shiv.min.js"></script>
<script src="../site_libs/bootstrap-3.3.5/shim/respond.min.js"></script>

<link rel="stylesheet"
      href="../site_libs/highlight/textmate.css"
      type="text/css" />

<script src="../site_libs/highlight/highlight.js"></script>
<script type="text/javascript">
if (window.hljs && document.readyState && document.readyState === "complete") {
   window.setTimeout(function() {
      hljs.initHighlighting();
   }, 0);
}
</script>

<script src="../js/toc2.js"></script>
<script src="../js/docs.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS_HTML"></script>
<script>
    MathJax.Hub.Config({
        extensions: ["tex2jax.js"],
        jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {
        inlineMath: [ ['$','$'], ["\\\\(","\\\\)"] ],
        displayMath: [ ['$$','$$'], ["\\\\[","\\\\]"] ],
        processEscapes: true
        },
        "HTML-CSS": {
            preferredFont: "TeX",
            availableFonts: ["STIX","TeX"],
            styles: {
                scale: 110,
                ".MathJax_Display": {
                    "font-size": "110%%",
                }
            }
        }
    });
</script>
%s
<script>
// manage active state of menu based on current page
$(document).ready(function () {
  // active menu anchor
  href = window.location.pathname
  href = href.substr(href.lastIndexOf('/') + 1)
  if (href === "")
    href = "index.html";
  var menuAnchor = $('a[href="' + href + '"]');
  // mark it active
  menuAnchor.parent().addClass('active');
  // if it's got a parent navbar menu mark it active as well
  menuAnchor.closest('li.dropdown').addClass('active');
});
</script>
<div class="container-fluid main-container">
<!-- tabsets -->
<script src="../site_libs/navigation-1.1/tabsets.js"></script>
<script>
$(document).ready(function () {
  window.buildTabsets("TOC");
});
</script>

<title>%s</title>

<style type = "text/css">
body {
  %s
  padding-top: 66px;
  padding-bottom: 40px;
}
</style>
</head>

<body>
<div tabindex="-1" id="notebook" class="border-box-sizing">
<div class="container" id="notebook-container">

<!-- code folding -->

<div class="navbar navbar-default  navbar-fixed-top" role="navigation">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="../index.html">%s</a>
    </div>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        %s
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li>
    <a href="%s">
    %s
    </a>
    </li>
    </ul>
    </div><!--/.nav-collapse -->
  </div><!--/.container -->
</div><!--/.navbar -->
{%%- endblock header -%%}
{%% block footer %%}
<hr>
%s
</div>
</div>
</body>
</html>
{%% endblock %%}
	''' % (conf['__version__'],
           '<link rel="stylesheet" type="text/css" href="../css/%s.css">' % conf['jt_theme']
           if conf['jt_theme'] is not None else '',
           conf['theme'], get_sidebar(path) if conf['notebook_toc'] else '',
           conf['name'], get_font(conf['font']), conf['name'],
           get_nav([x for x in dirs if not x in conf['hide_navbar']], conf['homepage_label'], '../'),
           conf['repo'], conf['source_label'], conf['footer'])
    return content

def make_template(conf, dirs, outdir):
    with open('{}/index.tpl'.format(outdir), 'w') as f:
        f.write(get_index_tpl(conf, dirs).strip())
    for item in dirs:
        with open('{}/{}.tpl'.format(outdir, item), 'w') as f:
            f.write(get_notebook_tpl(conf, dirs, item).strip())

def get_notebook_toc(path, exclude):
    out = "var %sDict = {" % os.path.basename(path)
    for fn in sorted(glob.glob(os.path.join(path, "*.ipynb"))):
        if os.path.basename(fn) in ['_index.ipynb', 'index.ipynb'] or fn in exclude:
            continue
        name = os.path.basename(fn[:-6]).strip()
        with open(fn) as f:
            data = json.load(f)
        title = re.compile('(^\W+|\W+$)').sub('', data["cells"][0]["source"][0]).strip().replace(" ", "-") + "-1"
        out +='"' + title + '":"' + name + '",'
    if not out.endswith('{'):
        out = out[:-1]
    out += "}"
    return out

def get_index_toc(path):
    out = 'var {}Array = '.format(os.path.basename(path))
    # Reference index
    fr = os.path.join(path, '_index.ipynb')
    if not os.path.isfile(fr):
        return out + '[]'
    # Actual index
    fi = os.path.join(path, 'index.ipynb')
    if not os.path.isfile(fi):
        fi = fr
    # Collect HTML file names from index file
    res = []
    with open(fi) as f:
        data = json.load(f)
    for cell in data['cells']:
        for sentence in cell["source"]:
            doc = re.search('(.+?)/(.+?).html', sentence)
            if doc:
                res.append(doc.group(2))
    # Filter by reference index
    if not fi == fr:
        ref = []
        with open(fr) as f:
            data = json.load(f)
        for cell in data['cells']:
            for sentence in cell["source"]:
                doc = re.search('(.+?)/(.+?).html', sentence)
                if doc:
                    ref.append(doc.group(2))
        res = [x for x in res if x in ref]
    return out + repr(res)

def get_toc(path, exclude):
    return [get_index_toc(path) + '\n' + get_notebook_toc(path, exclude)]

def make_index_nb(path, exclude):
    sos_files = [x for x in sorted(glob.glob(os.path.join(path, "*.sos")), reverse = True) if not x in exclude]
    out = '''
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# %s"
   ]
  },''' % os.path.basename(path.capitalize())
    if len(sos_files):
        out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Notebooks"
   ]
  },'''
    for fn in sorted(glob.glob(os.path.join(path, "*.ipynb")), reverse = True):
        if os.path.basename(fn) in ['_index.ipynb', 'index.ipynb'] or fn in exclude:
            continue
        name = os.path.splitext(os.path.basename(fn))[0].replace('_', ' ')
        with open(fn) as f:
            data = json.load(f)
        title = re.compile('(^\W+|\W+$)').sub('', data["cells"][0]["source"][0]).strip()
        out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[%s](%s/%s)<br>\\n",
    "&nbsp; &nbsp; %s"
   ]
  },''' % (name, path, os.path.splitext(os.path.basename(fn))[0] + '.html', title.replace('"', "'"))
    if len(sos_files):
        out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Pipelines"
   ]
  },'''
    for fn in sos_files:
        name = os.path.splitext(os.path.basename(fn))[0].replace('_', ' ')
        out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[%s](%s/%s)"
   ]
  },''' % (name, path, os.path.splitext(os.path.basename(fn))[0] + '.pipeline.html')
    out = out.strip(',') + '''
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}'''
    return out

def make_empty_nb(name):
    return '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Welcome to %s!"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}''' % name
