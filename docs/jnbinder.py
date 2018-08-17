import os
import glob
import re
import json
import subprocess
import collections
from hashlib import sha1
from dateutil.parser import parse
from bs4 import BeautifulSoup

def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False

def get_output(cmd, show_command=False, prompt='$ '):
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, shell=True).decode()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e)
    if show_command:
        return '{}{}\n{}'.format(prompt, cmd, output)
    else:
        return output.strip()

def short_repr(obj, noneAsNA=False, n1=25, n2=12):
    '''Return a short representation of obj for clarity.'''
    if obj is None:
        return 'unspecified' if noneAsNA else 'None'
    elif isinstance(obj, str) and len(obj) > (n1+n2):
        return repr('{} ... {}').format(obj[:(n1-2)].replace('\n', '\\n'), obj[-n2:].replace('\n', '\\n').lstrip())
    elif isinstance(obj, (str, int, float, bool)) or (isinstance(obj, collections.Sequence) \
        and len(obj) <= 2) or len(str(obj)) < (n1+n2):
        return repr(obj)
    elif isinstance(obj, collections.Sequence): # should be a list or tuple
        return f'[{short_repr(obj[0])}, ...] ({len(obj)} items)'
    elif isinstance(obj, dict):
        if obj:
            first_key = list(obj.keys())[0]
            return f'{{{first_key!r}:{short_repr(obj[first_key])!r}, ...}} ({len(obj)} items)'
        else:
            return '{}'
    else:
        return f'{repr(obj)[:n1]} ...'

def compare_versions(v1, v2):
    # This will split both the versions by '.'
    arr1 = v1.split(".")
    arr2 = v2.split(".")
    # Initializer for the version arrays
    i = 0
    # We have taken into consideration that both the
    # versions will contains equal number of delimiters
    while(i < len(arr1)):
        # Version 2 is greater than version 1
        if int(arr2[i]) > int(arr1[i]):
            return -1
        # Version 1 is greater than version 2
        if int(arr1[i]) > int(arr2[i]):
            return 1
        # We can't conclude till now
        i += 1
    # Both the versions are equal
    return 0

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
                              get_output('git log --oneline {} | wc -l'.format(fn)), short_fmt)
            out = '<p><small>Exported from {} committed {} {}</small></p>'.\
                  format(get_notebook_link(conf['repo'], long_fmt, fn), rev_string,
                         '<a href=\\"{}\\">{}</a>'.\
                         format(conf['__about_commit__'], '<span class=\\"fa fa-question-circle\\"></span>')
                         if conf['__about_commit__'] else '')
        except:
            # if git related command fails, indicating it is not a git repo
            # I'll just pass ...
            pass
    return out.replace('/', '\/')

def get_nav(dirs, home_label, prefix = './'):
    if home_label:
        out = '''
<li>
  <a href="{}index.html">{}</a>
</li>
        '''.format(prefix, home_label)
    else:
        out = ''
    for item in dirs:
        out += '''
<li>
  <a href="{}{}{}">{}</a>
</li>
        '''.format(prefix, item,
                   '/index.html' if os.path.isfile(f'{item}/{item}.ipynb') or os.path.isfile(f'{item}/{item}.Rmd') else '.html',
                   ' '.join([x.capitalize() if x.upper() != x else x for x in item.split('_')]))
    return out

def get_right_nav(repo, source_label):
    if source_label:
        return '''
<ul class="nav navbar-nav navbar-right">
<li>
   <a href="%s"> %s </a>
</li>
</ul>
        ''' % (repo, source_label)
    else:
        return ''

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
            var docs_map=%sArrayMap;
            var pos=%sArray.indexOf(file);
            for (var a=pos;a>=0;a--){
                  $('<li><a href="'+docs[a]+'.html"><font color="#073642"><b>'+docs_map[docs[a]].replace(/_/g," ")+'</b></font></a></li>').insertBefore("#toc-level0 li:eq(0)");
            }
            $('a[href="'+file+'.html'+'"]').css("color","#126dce");
            for (var a=pos+1;a<docs.length;a++){
                  $(".toc #toc-level0").append('<li><a href="'+docs[a]+'.html"><font color="#073642"><b>'+docs_map[docs[a]].replace(/_/g," ")+'</b></font></a></li>');
            }
            // $("#toc-header").hide(); // comment out because it prevents search bar from displaying
    });
</script>
''' % (path, path, path, path)

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
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.9.1/jquery-ui.min.js"></script>
<link href="site_libs/bootstrap-3.3.5/css/%s.min.css" rel="stylesheet" />
<script src="site_libs/bootstrap-3.3.5/js/bootstrap.min.js"></script>
<script src="site_libs/bootstrap-3.3.5/shim/html5shiv.min.js"></script>
<script src="site_libs/bootstrap-3.3.5/shim/respond.min.js"></script>
<link href="site_libs/font-awesome-4.5.0/css/font-awesome.min.css" rel="stylesheet" />

<style type="text/css">code{white-space: pre;}</style>
<link rel="stylesheet"
      href="site_libs/highlightjs/%s.min.css"
      type="text/css" />

<script src="site_libs/highlightjs/highlight.%s.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
<script type="text/javascript">
if (window.hljs && document.readyState && document.readyState === "complete") {
   window.setTimeout(function() {
      hljs.initHighlighting();
   }, 0);
}
</script>
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
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML"></script>
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
            availableFonts: ["TeX"],
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

h1, h2, h3, h4, h5, h6 {
  margin-top: 20px;
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
  visibility: hidden;
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
    %s
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
    script.src  = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML";
    document.getElementsByTagName("head")[0].appendChild(script);
  })();
</script>
</body>
</html>
{%% endblock %%}
	''' % (conf['__version__'], conf['name'], conf['theme'],
           'null', conf['auto_highlight'][0],
           get_font(conf['font']), conf['name'],
           get_nav([x for x in dirs if not x in conf['hide_navbar']], conf['homepage_label']),
           get_right_nav(conf['repo'], conf['source_label']), conf['footer'],
           get_disqus(conf['disqus']))
    return content

def get_sos_tpl(option):
    if option == "header":
        return '''
{%- if nb['metadata'].get('sos',{}).get('kernels',none) is not none -%}

<style type="text/css">

table {
   padding: 0;
   border-collapse: collapse; }
thead {
    border-bottom-width: 1px;
    border-bottom-color: rgb(0,0,0);
    border-bottom-style: solid;
}
table tr {
   border: none;
   background-color: white;
   margin: 0;
   padding: 0; }
table tr:nth-child(2n) {
   background-color: #f8f8f8; }
table tr th {
   font-weight: bold;
   border: none;
   margin: 0;
   padding: 6px 13px; }
table tr td {
   border: none;
   margin: 0;
   padding: 6px 13px; }
table tr th :first-child, table tr td :first-child {
   margin-top: 0; }
table tr th :last-child, table tr td :last-child {
   margin-bottom: 0; }

.dataframe_container { max-height: 400px }
.dataframe_input {
    border: 1px solid #ddd;
    margin-bottom: 5px;
}

.rendered_html table {
  border: none;
}

.sos_hint {
  color: rgba(0,0,0,.4);
  font-family: monospace;
  display: none;
}

.output_stderr {
    display: none;
}
/*
 div.input {
     display: none;
 }
*/
.hidden_content {
    display: none;
}

.input_prompt {
    display: none;
}

.output_area .prompt {
    display: none;
}

.output_prompt {
    display: none;
}

#nextsteps {
   color: blue;
}

.scatterplot_by_rowname div.xAxis div.tickLabel {
    transform: translateY(15px) translateX(15px) rotate(45deg);
    -ms-transform: translateY(15px) translateX(15px) rotate(45deg);
    -moz-transform: translateY(15px) translateX(15px) rotate(45deg);
    -webkit-transform: translateY(15px) translateX(15px) rotate(45deg);
    -o-transform: translateY(15px) translateX(15px) rotate(45deg);
    /*rotation-point:50% 50%;*/
    /*rotation:270deg;*/
}

div.cell {
    padding: 0pt;
    border-width: 0pt;
}
.sos_dataframe td, .sos_dataframe th, .sos_dataframe tr {
    white-space: nowrap;
    border: none;
}

.sos_dataframe tr:hover {
    background-color: #e6f2ff;
}

.display_control_panel  {
    position: inherit;
    z-index: 1000;
}

.display_checkboxes {
    margin-top: 5pt;
}

{%- if nb['metadata'].get('sos',{}).get('kernels',none) is not none -%}

{% for item in nb['metadata'].get('sos',{}).get('kernels',{}) %}

{%- if item[2] -%}
.lan_{{item[0]}} .input_prompt { background-color: {{item[3]}} !important }

{%- else -%}
.lan_{{item[0]}} {}

{%- endif -%}

{% endfor %}

{%- endif -%}
</style>

<script>

function filterDataFrame(id) {
    var input = document.getElementById("search_" + id);
    var filter = input.value.toUpperCase();
    var table = document.getElementById("dataframe_" + id);
    var tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (var i = 1; i < tr.length; i++) {
        for (var j = 0; j < tr[i].cells.length; ++j) {
            var matched = false;
            if (tr[i].cells[j].innerHTML.toUpperCase().indexOf(filter) != -1) {
                tr[i].style.display = "";
                matched = true
                break;
            }
            if (!matched)
                tr[i].style.display = "none";
        }
    }
}

function sortDataFrame(id, n, dtype) {
    var table = document.getElementById("dataframe_" + id);

    var tb = table.tBodies[0]; // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
    var tr = Array.prototype.slice.call(tb.rows, 0); // put rows into array

    if (dtype === 'numeric') {
        var fn = function(a, b) { 
            return parseFloat(a.cells[n].textContent) <= parseFloat(b.cells[n].textContent) ? -1 : 1;
        }
    } else {
        var fn = function(a, b) {
            var c = a.cells[n].textContent.trim().localeCompare(b.cells[n].textContent.trim()); 
            return c > 0 ? 1 : (c < 0 ? -1 : 0) }
    }
    var isSorted = function(array, fn) {
        if (array.length < 2)
            return 1;
        var direction = fn(array[0], array[1]); 
        for (var i = 1; i < array.length - 1; ++i) {
            var d = fn(array[i], array[i+1]);
            if (d == 0)
                continue;
            else if (direction == 0)
                direction = d;
            else if (direction != d)
                return 0;
            }
        return direction;
    }

    var sorted = isSorted(tr, fn);

    if (sorted == 1 || sorted == -1) {
        // if sorted already, reverse it
        for(var i = tr.length - 1; i >= 0; --i)
            tb.appendChild(tr[i]); // append each row in order
    } else {
        tr = tr.sort(fn);
        for(var i = 0; i < tr.length; ++i)
            tb.appendChild(tr[i]); // append each row in order
    }
}

function toggle_source() {
    var btn = document.getElementById("show_cells");
    if (btn.checked) {
        $('div.input').css('display', 'flex');
        $('.hidden_content').show();
        // this somehow does not work.
        $('div.cell').css('padding', '0pt').css('border-width', '0pt');
    } else {
        $('div.input').hide();
        $('.hidden_content').hide();
        $('div.cell').css('padding', '0pt').css('border-width', '0pt');
    }
}

function toggle_prompt() {
    var btn = document.getElementById("show_prompt");
    if (btn.checked) {
        $('.output_prompt').show();
        $('.input_prompt').show();
        $('.output_area .prompt').show();
    } else {
        $('.output_prompt').hide();
        $('.input_prompt').hide();
        $('.output_area .prompt').hide();
    }
}

function toggle_messages() {
    var btn = document.getElementById("show_messages");
    if (btn.checked) {
        $('.sos_hint').show();
        $('.output_stderr').show();
    } else {
        $('.output_stderr').hide();
        $('.sos_hint').hide();
    }
}

</script>

{%- endif -%}
    '''
    elif option == "panel":
        return '''
<div class='display_control_panel'>
        <div class="display_checkboxes">
        Show:
            &nbsp;
            <input type="checkbox" id="show_cells" name="show_cells" onclick="toggle_source()">
            <label for="show_cells">All cells</label>
            &nbsp;
            <input type="checkbox" id="show_prompt" name="show_prompt" onclick="toggle_prompt()">
            <label for="show_prompt">Prompt</label>
            &nbsp;
            <input type="checkbox" id="show_messages" name="show_messages" onclick="toggle_messages()">
            <label for="show_messages">Messages</label>
    </div>
</div>
    '''
    elif option == "body":
        return '''
{%- block input -%}

    {%- if 'scratch' in cell.metadata.tags -%}
	{%- elif 'report_cell' in cell.metadata.tags -%}
        {{ super() }}
    {%- else -%}
        <div class="hidden_content">
        {{ super() }}
        </div>
   {%- endif -%}
{%- endblock input -%}

{% block output %}
    {%- if 'report_output' in cell.metadata.tags -%}
        {{ super() }}
    {%- elif 'report_cell' in cell.metadata.tags -%}
        {{ super() }}
    {%- elif 'scratch' in cell.metadata.tags -%}
    {%- else -%}
        <div class="hidden_content">
        {{ super() }}
        </div>
   {%- endif -%}
{% endblock output %}

{% block markdowncell %}
    {%- if 'hide_output' in cell.metadata.tags -%}
		<div class="hidden_content">
        {{ super() }}
		</div>
    {%- elif 'scratch' in cell.metadata.tags -%}
    {%- else -%}
        {{ super() }}
   {%- endif -%}
{%- endblock markdowncell -%}


{% block codecell %}

{%- if cell['metadata'].get('kernel',none) is not none -%}
    <div class="rendered lan_{{cell['metadata'].get('kernel', none)}}">
    {{ super() }}
    </div>
{%- else -%}
    {{ super() }}
{%- endif -%}

{%- endblock codecell %}
        '''
    else:
        return ''

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
      href="../site_libs/highlightjs/%s.min.css"
      type="text/css" />

<script src="../site_libs/highlightjs/highlight.%s.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
<script type="text/javascript">
if (window.hljs && document.readyState && document.readyState === "complete") {
   window.setTimeout(function() {
      hljs.initHighlighting();
   }, 0);
}
</script>

<script src="../js/doc_toc.js"></script>
<script src="../js/docs.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML"></script>
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
            availableFonts: ["TeX"],
            styles: {
                scale: 110,
                ".MathJax_Display": {
                    "font-size": "110%%",
                }
            }
        }
    });
</script>
<script>
function filterDataFrame(id) {
    var input = document.getElementById("search_" + id);
    var filter = input.value.toUpperCase();
    var table = document.getElementById("dataframe_" + id);
    var tr = table.getElementsByTagName("tr");
    // Loop through all table rows, and hide those who don't match the search query
    for (var i = 1; i < tr.length; i++) {
        for (var j = 0; j < tr[i].cells.length; ++j) {
            var matched = false;
            if (tr[i].cells[j].innerHTML.toUpperCase().indexOf(filter) != -1) {
                tr[i].style.display = "";
                matched = true
                break;
            }
            if (!matched)
                tr[i].style.display = "none";
        }
    }
}
function sortDataFrame(id, n, dtype) {
    var table = document.getElementById("dataframe_" + id);
    var tb = table.tBodies[0]; // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
    var tr = Array.prototype.slice.call(tb.rows, 0); // put rows into array
    if (dtype === 'numeric') {
        var fn = function(a, b) { 
            return parseFloat(a.cells[n].textContent) <= parseFloat(b.cells[n].textContent) ? -1 : 1;
        }
    } else {
        var fn = function(a, b) {
            var c = a.cells[n].textContent.trim().localeCompare(b.cells[n].textContent.trim()); 
            return c > 0 ? 1 : (c < 0 ? -1 : 0) }
    }
    var isSorted = function(array, fn) {
        if (array.length < 2)
            return 1;
        var direction = fn(array[0], array[1]); 
        for (var i = 1; i < array.length - 1; ++i) {
            var d = fn(array[i], array[i+1]);
            if (d == 0)
                continue;
            else if (direction == 0)
                direction = d;
            else if (direction != d)
                return 0;
            }
        return direction;
    }
    var sorted = isSorted(tr, fn);
    if (sorted == 1 || sorted == -1) {
        // if sorted already, reverse it
        for(var i = tr.length - 1; i >= 0; --i)
            tb.appendChild(tr[i]); // append each row in order
    } else {
        tr = tr.sort(fn);
        for(var i = 0; i < tr.length; ++i)
            tb.appendChild(tr[i]); // append each row in order
    }
}
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

%s

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
        %s
      </div><!--/.nav-collapse -->
  </div><!--/.container -->
</div><!--/.navbar -->
%s
{%%- endblock header -%%}
%s
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
           conf['theme'], conf['auto_highlight'][1], conf['auto_highlight'][0],
           get_sidebar(path) if conf['notebook_toc'] else '',
           get_sos_tpl('header' if conf['report_style'] is True else ''),
           conf['name'], get_font(conf['font']), conf['name'],
           get_nav([x for x in dirs if not x in conf['hide_navbar']], conf['homepage_label'], '../'),
           get_right_nav(conf['repo'], conf['source_label']),
           get_sos_tpl('panel' if conf['report_style'] is True else ''),
           get_sos_tpl('body' if conf['report_style'] is True else ''),
           conf['footer'])
    return content

def update_gitignore():
    flag = True
    if os.path.isfile('.gitignore'):
      lines = [x.strip() for x in open('.gitignore').readlines()]
      if '**/.sos' in lines:
        flag = False
    if flag:
      with open('.gitignore', 'a') as f:
        f.write('\n**/.sos\n**/.ipynb_checkpoints\n**/__pycache__')

def make_template(conf, dirs, outdir):
    with open('{}/index.tpl'.format(outdir), 'w') as f:
        f.write(get_index_tpl(conf, dirs).strip())
    for item in dirs:
        with open('{}/{}.tpl'.format(outdir, item), 'w') as f:
            f.write(get_notebook_tpl(conf, dirs, item).strip())

def get_notebook_toc(path, exclude):
    map1 = dict()
    map2 = dict()
    for fn in sorted(glob.glob(os.path.join(path, "*.ipynb"))):
        if os.path.basename(fn) in ['_index.ipynb', 'index.ipynb'] or fn in exclude:
            continue
        name = os.path.basename(fn[:-6]).strip()
        with open(fn) as f:
            data = json.load(f)
        try:
            idx = 0
            while True:
                title = data["cells"][0]["source"][idx].strip()
                if title:
                    break
                idx += 1
        except IndexError:
            title = name
            continue
        # FIXME: this regex is to be continuously updated based on observed TOC generated
        map2[name] = short_repr(title.replace('`','').strip('#').strip())[1:-1]
        title = re.sub('[^0-9a-zA-Z-:&!?@.,()+]+', '-', title).strip('-') + "-1"
        map1[title] = name
    out = f"var {os.path.basename(path)}Dict = {str(map1)}\n"
    out += f"var {os.path.basename(path)}ArrayMap = {str(map2)}"
    return out

def get_index_toc(path):
    out = f'var {os.path.basename(path)}Array = '
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
            doc = re.search('^.*\/(.+?).html', sentence)
            if doc:
                res.append(doc.group(1))
    # Filter by reference index
    if not fi == fr:
        ref = []
        with open(fr) as f:
            data = json.load(f)
        for cell in data['cells']:
            for sentence in cell["source"]:
                doc = re.search('^.*\/(.+?).html', sentence)
                if doc:
                    ref.append(doc.group(1))
        res = [x for x in res if x in ref]
    return out + repr(res)

def get_toc(path, exclude):
    return [get_index_toc(path) + '\n' + get_notebook_toc(path, exclude)]

def make_index_nb(path, exclude, long_description = False, reverse_alphabet = False):
    sos_files = [x for x in sorted(glob.glob(os.path.join(path, "*.sos")), reverse = reverse_alphabet) if not x in exclude]
    out = '''
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# %s"
   ]
  },''' % os.path.basename(path).replace('_', ' ').capitalize()
    if len(sos_files):
        out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Notebooks"
   ]
  },'''
    date_section = None
    add_date_section = False
    for fn in sorted(glob.glob(os.path.join(path, "*.ipynb")), reverse = reverse_alphabet):
        if os.path.basename(fn) in ['_index.ipynb', 'index.ipynb'] or fn in exclude:
            continue
        name = os.path.splitext(os.path.basename(fn))[0].replace('_', ' ')
        tmp = "{}/{}".format(name[:4], name[4:6])
        if is_date(tmp) and date_section != tmp:
            date_section = tmp
            add_date_section = True
        with open(fn) as f:
            data = json.load(f)
        try:
            source = [x.strip() for x in data["cells"][0]["source"] if x.strip()]
            if long_description and source[0].startswith('#') and len(source) >= 2 and not source[1].startswith('#'):
                title = source[0].lstrip('#').strip()
                description = source[1].lstrip('#').strip()
            else:
                title = name.strip()
                description = source[0].lstrip('#').strip()
        except IndexError:
            continue
        if add_date_section:
            add_date_section = False
            out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### %s\\n"
   ]
  },''' % date_section
        html_link = (os.path.splitext(os.path.basename(fn))[0] + '.html') if os.path.splitext(os.path.basename(fn))[0] != os.path.basename(os.path.dirname(fn)) else 'index.html'
        if title != description:
            out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[**%s**](%s/%s)<br>\\n",
    %s
   ]
  },''' % (title, path, html_link, json.dumps("&nbsp; &nbsp;" + description))
        else:
            out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[**%s**](%s/%s)<br>"
   ]
  },''' % (title, path, html_link)
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
    return out.strip()

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

def protect_page(page, page_tpl, password, write):
    # page: docs/{name}
    page_dir, page_file = os.path.split(page)
    page_file = '/'.join(page.split('/')[1:])
    secret = page_dir + '/' + sha1((password + page_file).encode()).hexdigest() + '.html'
    if write:
        content = open(page).readlines()
        content.insert(5, '<meta name="robots" content="noindex">\n')
        with open(secret, 'w') as f:
            f.write(''.join(content))
        content = open(page_tpl).readlines()
        with open(page, 'w') as f:
            f.write(''.join(content).replace("TPL_PLACEHOLDER", page_file))
    secret = os.path.basename(secret)
    return secret, f'docs/{secret.rsplit(".", 1)[0]}_{os.path.basename(page_dir)}.sha1'

def get_sha1_files(index_files, notebook_files, passwords, write = False):
    # Inputs are list of files [(input, output), ...]
    password = [None if passwords is None or (os.path.dirname(fn[0]) not in passwords and fn[0] not in passwords) else (passwords[os.path.dirname(fn[0]) if (os.path.dirname(fn[0]) in passwords and not fn[0] in passwords) else fn[0]]) for fn in index_files] + [None if passwords is None or fn[0] not in passwords else passwords[fn[0]] for fn in notebook_files]
    res = [protect_page(fn[1], 'docs/site_libs/jnbinder_password.html', p, write)[1]
           for fn, p in zip(index_files + notebook_files, password) if p]
    return res

def parse_html(url, html):
    '''
    A simple script to create tipue content by searching for documentation
    files under given folders.

    Copyright (C) 2016 Bo Peng (bpeng@mdanderson.org) under GNU General Public License
    '''
    with open(html, 'rb') as content:
        soup = BeautifulSoup(content, "html.parser", from_encoding='utf-8')
        #
        # try to get the title of the page from h1, h2, or title, and
        # uses filename if none of them exists.
        #
        title = soup.find('h1')
        if title is None:
            title = soup.find('h2')
        if title is None:
            title = soup.find('title')
        if title is None:
            title = os.path.basename(html).rsplit('.')[0]
        else:
            title = title.get_text()
        maintitle = soup.find('h1')
        if maintitle is None:
            maintitle = soup.find('h2')
        if maintitle is None:
            maintitle = soup.find('title')
        if maintitle is None:
            maintitle = os.path.basename(html).rsplit('.')[0]
        else:
            maintitle = maintitle.get_text()

        # remove special characters which might mess up js file
        title = re.sub(r'[¶^a-zA-Z0-9_\.\-]', ' ', title)
        #
        # sear
        all_text = []
        for header in soup.find_all(re.compile('^h[1-6]$')):
            # remove special character
            part = re.sub(r'[^a-zA-Z0-9_\-=\'".,\\]', ' ', header.get_text()).replace('"', "'").strip() + "\n"
            part = re.sub(r'\s+', ' ', part)
            ids = [x for x in header.findAll('a') if x.get('id')]
            if ids:
                tag = '#' + ids[0].get('id')
            else:
                hrefs = header.findAll('a', {'class': 'anchor-link'})
                if hrefs:
                    tag = hrefs[0].get('href')
                else:
                    tag = ''
            part = '{{"mainTitle": "{}", "title": "{}", "text": "{}", "tags": "", "mainUrl": "{}", "url": "{}"}}'.format(
                    re.sub('¶', '', maintitle), re.sub('¶', '', header.get_text()), part, url, url + tag)
            all_text.append(part)
    return all_text

def generate_tipue_content(html_files, base_url, docs_dir):
    # input is a list of html files and their url
    n = len(docs_dir)
    text = [parse_html(url, html) for (url, html) in [(os.path.join(base_url, item[len(docs_dir):]), item) for item in html_files]]
    # write the output to file.
    with open(os.path.join(docs_dir, 'site_libs/tipuesearch', 'tipuesearch_content.js'), 'w') as out:
        out.write('''\
var tipuesearch = {{"pages": [
{}
]}};
'''.format(',\n'.join(sum(text, []))))
