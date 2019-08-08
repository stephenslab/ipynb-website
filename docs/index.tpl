{%- extends 'basic.tpl' -%}

{%- block header -%}
{{ super() }}

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="ipynb_website:version" content="0.9.7" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<title>Divvy data exploration project</title>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.9.1/jquery-ui.min.js"></script>
<link href="site_libs/bootstrap-3.3.5/css/readable.min.css" rel="stylesheet" />
<script src="site_libs/bootstrap-3.3.5/js/bootstrap.min.js"></script>
<script src="site_libs/bootstrap-3.3.5/shim/html5shiv.min.js"></script>
<script src="site_libs/bootstrap-3.3.5/shim/respond.min.js"></script>
<link href="site_libs/font-awesome-4.5.0/css/font-awesome.min.css" rel="stylesheet" />

<style type="text/css">code{white-space: pre;}</style>
<link rel="stylesheet"
      href="site_libs/highlightjs/null.min.css"
      type="text/css" />

<script src="site_libs/highlightjs/highlight.pack.js"></script>
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
        inlineMath: [ ['$','$'], ["\\(","\\)"] ],
        displayMath: [ ['$$','$$'] ["\\[","\\]"] ],
        processEscapes: true
        },
        "HTML-CSS": {
            preferredFont: "TeX",
            availableFonts: ["TeX"],
            styles: {
                scale: 110,
                ".MathJax_Display": {
                    "font-size": "110%",
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
  
  font-size: 160%;
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
  max-width:100%;
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
      <a class="navbar-brand" href="index.html">Divvy data exploration project</a>
    </div>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        
<li>
  <a href="./index.html">Overview</a>
</li>
        
<li>
  <a href="./setup.html">Setup</a>
</li>
        
<li>
  <a href="./license.html">License</a>
</li>
        
<li>
  <a href="./notes.html">Notes</a>
</li>
        
<li>
  <a href="./protected.html">Protected</a>
</li>
        
      </ul>
    
<ul class="nav navbar-nav navbar-right">
<li>
   <a href="http://github.com/stephenslab/ipynb-website"> source </a>
</li>
</ul>
        
    </div><!--/.nav-collapse -->
  </div><!--/.container -->
</div><!--/.navbar -->

{%- endblock header -%}
{% block footer %}
<hr>
&copy; 2017 Peter Carbonetto &amp; Gao Wang
<!-- To enable disqus, uncomment the section below and provide your disqus_shortname -->

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
{% endblock %}