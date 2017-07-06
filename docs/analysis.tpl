{%- extends 'full.tpl' -%}

{%- block header -%}
{{ super() }}

 <link rel="stylesheet" href="https://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.9.1/jquery-ui.min.js"></script>

<style>  /* defined here in case the main.css below cannot be loaded */
.lev1 {margin-left: 80px}
.lev2 {margin-left: 100px}
.lev3 {margin-left: 120px}
.lev4 {margin-left: 140px}
.lev5 {margin-left: 160px}
.lev6 {margin-left: 180px}
</style>

<link rel="stylesheet" type="text/css" href="../css/jt.css">
<link rel="stylesheet" type="text/css" href="../css/toc2.css">

<script src="../js/toc2.js"></script>
<script src="../js/docs.js"></script>

<script>
    MathJax.Hub.Config({
        extensions: ["tex2jax.js"],
        jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {
        inlineMath: [ ['$','$'], ["\(","\)"] ],
        displayMath: [ ['$$','$$'], ["\[","\]"] ],
        processEscapes: true
        },
        "HTML-CSS": {
            preferredFont: "TeX",
            availableFonts: ["STIX","TeX"],
            styles: {
                scale: 110,
                ".MathJax_Display": {
                    "font-size": "110%",
                }
            }
        }
    });
</script>

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

            var file=analysisDict[$("h1:first").attr("id")];
            $("#toc-level0 a").css("color","#126dce");
            $('a[href="#'+$("h1:first").attr("id")+'"]').hide()
            var docs=analysisArray;
            var pos=analysisArray.indexOf(file);

            for (var a=pos;a>=0;a--){
                  var name=docs[a]
                  $('<li><a href="'+name+'.html">'+name.replace(/_/g," ")+'</a></li>').insertBefore("#toc-level0 li:eq(0)");
            }
            $('a[href="'+file+'.html'+'"]').css("color","#126dce");


            $('<li id="indexHome"><a href="../analysis.html"><b>Analysis Home<b></a></li>').insertBefore("#toc-level0 li:eq(0)");
            for (var a=pos+1;a<docs.length;a++){
                  var name=docs[a]
                  $(".toc #toc-level0").append('<li><a href="'+name+'.html">'+name.replace(/_/g," ")+'</a></li>');
            }
            $("#toc-header").hide();
    });
</script>

{%- endblock header -%}