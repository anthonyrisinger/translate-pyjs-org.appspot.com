import os
import sys
import cgi
from logging import info
from cStringIO import StringIO

from google.appengine.ext.webapp.util import run_wsgi_app

pyjspth = os.path.realpath(os.path.dirname(__file__))
sys.path[0:0] = [os.path.join(pyjspth, 'pyjs/src')]
sys.path.append(os.path.join(pyjspth, 'pgen'))

import pyjs
import pyjs.translator_proto


pyjs.pyjspth = pyjspth
pyjs.path += [os.path.join(pyjspth, 'library')]
extext = (r'''<span class="http">POST / HTTP/1.1</span>
<span class="hdr">User-Agent:</span> curl/7.25.0 (x86_64-unknown-linux-gnu) libcurl/7.25.0 OpenSSL/1.0.1 zlib/1.2.6 libssh2/1.4.0
<span class="hdr">Host:</span> translate-pyjs-org.appspot.com
<span class="hdr">Accept:</span> */*
<span class="hdr">Content-Length:</span> 303
<span class="hdr">Content-Type:</span> multipart/form-data; boundary=----------------------------985ccc6f96af

----------------------------985ccc6f96af
Content-Disposition: form-data; name="t"; filename="Hello.py"
Content-Type: application/octet-stream

<span class="kn">import</span> <span class="nn">module</span>

<span class="k">def</span> <span class="nf">hello</span><span class="p">(</span><span class="n">there</span><span class="p">):</span>
    <span class="k">return</span> <span class="s">&#39;hi&#39;</span><span class="p">,</span> <span class="n">there</span>

<span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">&#39;__main__&#39;</span><span class="p">:</span>
    <span class="k">print</span> <span class="n">hello</span><span class="p">(</span><span class="s">&#39;me&#39;</span><span class="p">)</span>

----------------------------985ccc6f96af
''',
r'''<span class="http">HTTP/1.1 200 OK</span>
<span class="hdr">Content-Type:</span> text/javascript
<span class="hdr">Vary:</span> Accept-Encoding
<span class="hdr">Date:</span> Tue, 03 Apr 2012 11:17:00 GMT
<span class="hdr">Server:</span> Google Frontend
<span class="hdr">Cache-Control:</span> private
<span class="hdr">Transfer-Encoding:</span> chunked

<span class="cm">/* start module: Hello */</span>
<span class="nx">$pyjs</span><span class="p">.</span><span class="nx">loaded_modules</span><span class="p">[</span><span class="s1">&#39;Hello&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="kd">function</span> <span class="p">(</span><span class="nx">__mod_name__</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">if</span><span class="p">(</span><span class="nx">$pyjs</span><span class="p">.</span><span class="nx">loaded_modules</span><span class="p">[</span><span class="s1">&#39;Hello&#39;</span><span class="p">].</span><span class="nx">__was_initialized__</span><span class="p">)</span> <span class="k">return</span> <span class="nx">$pyjs</span><span class="p">.</span><span class="nx">loaded_modules</span><span class="p">[</span><span class="s1">&#39;Hello&#39;</span><span class="p">];</span>
    <span class="kd">var</span> <span class="nx">$m</span> <span class="o">=</span> <span class="nx">$pyjs</span><span class="p">.</span><span class="nx">loaded_modules</span><span class="p">[</span><span class="s2">&quot;Hello&quot;</span><span class="p">];</span>
    <span class="nx">$m</span><span class="p">.</span><span class="nx">__repr__</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span> <span class="k">return</span> <span class="s2">&quot;&lt;module: Hello&gt;&quot;</span><span class="p">;</span> <span class="p">};</span>
    <span class="nx">$m</span><span class="p">.</span><span class="nx">__was_initialized__</span> <span class="o">=</span> <span class="kc">true</span><span class="p">;</span>
    <span class="k">if</span> <span class="p">((</span><span class="nx">__mod_name__</span> <span class="o">===</span> <span class="kc">null</span><span class="p">)</span> <span class="o">||</span> <span class="p">(</span><span class="k">typeof</span> <span class="nx">__mod_name__</span> <span class="o">==</span> <span class="s1">&#39;undefined&#39;</span><span class="p">))</span> <span class="nx">__mod_name__</span> <span class="o">=</span> <span class="s1">&#39;Hello&#39;</span><span class="p">;</span>
    <span class="nx">$m</span><span class="p">.</span><span class="nx">__name__</span> <span class="o">=</span> <span class="nx">__mod_name__</span><span class="p">;</span>


    <span class="nx">$m</span><span class="p">[</span><span class="s1">&#39;module&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nx">$p</span><span class="p">[</span><span class="s1">&#39;___import___&#39;</span><span class="p">](</span><span class="s1">&#39;module&#39;</span><span class="p">,</span> <span class="kc">null</span><span class="p">);</span>
    <span class="nx">$m</span><span class="p">[</span><span class="s1">&#39;hello&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">there</span><span class="p">)</span> <span class="p">{</span>

        <span class="k">return</span> <span class="nx">$p</span><span class="p">[</span><span class="s1">&#39;tuple&#39;</span><span class="p">]([</span><span class="s1">&#39;hi&#39;</span><span class="p">,</span> <span class="nx">there</span><span class="p">]);</span>
    <span class="p">};</span>
    <span class="nx">$m</span><span class="p">[</span><span class="s1">&#39;hello&#39;</span><span class="p">].</span><span class="nx">__name__</span> <span class="o">=</span> <span class="s1">&#39;hello&#39;</span><span class="p">;</span>

    <span class="nx">$m</span><span class="p">[</span><span class="s1">&#39;hello&#39;</span><span class="p">].</span><span class="nx">__bind_type__</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
    <span class="nx">$m</span><span class="p">[</span><span class="s1">&#39;hello&#39;</span><span class="p">].</span><span class="nx">__args__</span> <span class="o">=</span> <span class="p">[</span><span class="kc">null</span><span class="p">,</span><span class="kc">null</span><span class="p">,[</span><span class="s1">&#39;there&#39;</span><span class="p">]];</span>
    <span class="k">if</span> <span class="p">(</span><span class="nx">$p</span><span class="p">[</span><span class="s1">&#39;bool&#39;</span><span class="p">](</span><span class="nx">$p</span><span class="p">[</span><span class="s1">&#39;op_eq&#39;</span><span class="p">]((</span><span class="k">typeof</span> <span class="nx">__name__</span> <span class="o">==</span> <span class="s2">&quot;undefined&quot;</span><span class="o">?</span><span class="nx">$m</span><span class="p">.</span><span class="nx">__name__</span><span class="o">:</span><span class="nx">__name__</span><span class="p">),</span> <span class="s1">&#39;__main__&#39;</span><span class="p">)))</span> <span class="p">{</span>
        <span class="nx">$p</span><span class="p">[</span><span class="s1">&#39;printFunc&#39;</span><span class="p">]([</span><span class="nx">$m</span><span class="p">[</span><span class="s1">&#39;hello&#39;</span><span class="p">](</span><span class="s1">&#39;me&#39;</span><span class="p">)],</span> <span class="mi">1</span><span class="p">);</span>
    <span class="p">}</span>
    <span class="k">return</span> <span class="k">this</span><span class="p">;</span>
<span class="p">};</span> <span class="cm">/* end Hello */</span>


<span class="cm">/* end module: Hello */</span>


<span class="cm">/*</span>
<span class="cm">PYJS_DEPS: [&#39;module&#39;]</span>
<span class="cm">*/</span>
''',
)
ex = r'''
<!doctype html>
<html>
<head>
<style>

.hll { background-color: #404040 }
.c { color: #999999; font-style: italic } /* Comment */
.err { color: #a61717; background-color: #e3d2d2 } /* Error */
.g { color: #d0d0d0 } /* Generic */
.k { color: #6ab825; font-weight: bold } /* Keyword */
.l { color: #d0d0d0 } /* Literal */
.n { color: #d0d0d0 } /* Name */
.o { color: #d0d0d0 } /* Operator */
.x { color: #d0d0d0 } /* Other */
.p { color: #d0d0d0 } /* Punctuation */
.cm { color: #999999; font-style: italic } /* Comment.Multiline */
.cp { color: #cd2828; font-weight: bold } /* Comment.Preproc */
.c1 { color: #999999; font-style: italic } /* Comment.Single */
.cs { color: #e50808; font-weight: bold; background-color: #520000 } /* Comment.Special */
.gd { color: #d22323 } /* Generic.Deleted */
.ge { color: #d0d0d0; font-style: italic } /* Generic.Emph */
.gr { color: #d22323 } /* Generic.Error */
.gh { color: #ffffff; font-weight: bold } /* Generic.Heading */
.gi { color: #589819 } /* Generic.Inserted */
.go { color: #cccccc } /* Generic.Output */
.gp { color: #aaaaaa } /* Generic.Prompt */
.gs { color: #d0d0d0; font-weight: bold } /* Generic.Strong */
.gu { color: #ffffff; text-decoration: underline } /* Generic.Subheading */
.gt { color: #d22323 } /* Generic.Traceback */
.kc { color: #6ab825; font-weight: bold } /* Keyword.Constant */
.kd { color: #6ab825; font-weight: bold } /* Keyword.Declaration */
.kn { color: #6ab825; font-weight: bold } /* Keyword.Namespace */
.kp { color: #6ab825 } /* Keyword.Pseudo */
.kr { color: #6ab825; font-weight: bold } /* Keyword.Reserved */
.kt { color: #6ab825; font-weight: bold } /* Keyword.Type */
.ld { color: #d0d0d0 } /* Literal.Date */
.m { color: #3677a9 } /* Literal.Number */
.s { color: #ed9d13 } /* Literal.String */
.na { color: #bbbbbb } /* Name.Attribute */
.nb { color: #24909d } /* Name.Builtin */
.nc { color: #447fcf; text-decoration: underline } /* Name.Class */
.no { color: #40ffff } /* Name.Constant */
.nd { color: #ffa500 } /* Name.Decorator */
.ni { color: #d0d0d0 } /* Name.Entity */
.ne { color: #bbbbbb } /* Name.Exception */
.nf { color: #447fcf } /* Name.Function */
.nl { color: #d0d0d0 } /* Name.Label */
.nn { color: #447fcf; text-decoration: underline } /* Name.Namespace */
.nx { color: #d0d0d0 } /* Name.Other */
.py { color: #d0d0d0 } /* Name.Property */
.nt { color: #6ab825; font-weight: bold } /* Name.Tag */
.nv { color: #40ffff } /* Name.Variable */
.ow { color: #6ab825; font-weight: bold } /* Operator.Word */
.w { color: #666666 } /* Text.Whitespace */
.mf { color: #3677a9 } /* Literal.Number.Float */
.mh { color: #3677a9 } /* Literal.Number.Hex */
.mi { color: #3677a9 } /* Literal.Number.Integer */
.mo { color: #3677a9 } /* Literal.Number.Oct */
.sb { color: #ed9d13 } /* Literal.String.Backtick */
.sc { color: #ed9d13 } /* Literal.String.Char */
.sd { color: #ed9d13 } /* Literal.String.Doc */
.s2 { color: #ed9d13 } /* Literal.String.Double */
.se { color: #ed9d13 } /* Literal.String.Escape */
.sh { color: #ed9d13 } /* Literal.String.Heredoc */
.si { color: #ed9d13 } /* Literal.String.Interpol */
.sx { color: #ffa500 } /* Literal.String.Other */
.sr { color: #ed9d13 } /* Literal.String.Regex */
.s1 { color: #ed9d13 } /* Literal.String.Single */
.ss { color: #ed9d13 } /* Literal.String.Symbol */
.bp { color: #24909d } /* Name.Builtin.Pseudo */
.vc { color: #40ffff } /* Name.Variable.Class */
.vg { color: #40ffff } /* Name.Variable.Global */
.vi { color: #40ffff } /* Name.Variable.Instance */
.il { color: #3677a9 } /* Literal.Number.Integer.Long */

body {
    background-color: #181818;
    color: #999;
    font-family: sans;
    text-shadow:-1px -1px 1px #020202;
}
header{
    line-height: 2em;
    vertical-align: middle;
    margin: 2.8em 0;
}
.http {color: #909090;}
.hdr {color: #606060;}
div#title {
    float: right;
    margin: 0 1em;
    text-align: right;
}
h5#desc {
    margin: 0 1em;
}
h1#loc {
    margin: 0 1em;
    text-shadow:-1px -1px 1px blue;
}
.demand {
    text-decoration: none;
}
#req, #res, h4, form {
    padding: 1em;
    font-family: monospace;
    background-color: #202020;
    border: 0.1em solid #101010;
    border-radius: 1em;
    text-shadow:-1px -1px 1px #101010;
}
#req, #res {
    line-height: 1.25em;
    color: #404040;
    white-space: pre;
}
form {
    float: left;
    padding: 0;
    overflow: hidden;
}
form div {
    margin: -0.125em;
}
input {
    line-height: 1em;
    background-color: #232323;
    color: #f0f0f0;
    border: 1px solid transparent;
}
h3 {
    clear: both;
    margin: 1.8em 1em;
}
footer#who {
    margin-top: 0.125em;
    line-height: 3em;
    vertical-align: center;
    text-align: center;
}
</style>
</head>
<body>
<header>
<div id="title">
<h1 id="loc" class="m">pyjs on<span class="demand nn">DEMAND</span></h1>
<h5 id="desc" class="">python to javascript translator</h5>
</div>
<form action="" method="post" enctype="multipart/form-data">
<div><button type="submit">Translate!</button><input name="t" type="file"></div>
</form>
&nbsp;</header>
<h3>post python file(s!) multipart/form-data, using [multiple] `t` keys, eg ...</h3>
<h4 class="s"># curl -i -F 't=@Hello.py' http://translate-pyjs-org.appspot.com/</h4>
<h3>request ...</h3>
<div id="req">%s</div>
<h3>response ...</h3>
<div id="res">%s</div>
<footer id="who">&copy; 2012 C Anthony Risinger</footer>
</body>
</html>
''' % extext


def application(environ, start_response):
    parameters = cgi.parse_qs(environ.get('QUERY_STRING', ''))
    post = environ.copy()
    post.pop('QUERY_STRING', None)
    post = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=post,
    )
    if 't' not in post:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ex
    t = post['t']
    o = StringIO()
    if not hasattr(t, 'append'):
        t = [t]
    for s in (t if hasattr(t, 'append') else [t]):
        pyjs.translator_proto.translate([s], o)
    o.seek(0)
    start_response('200 OK', [('Content-Type', 'text/javascript')])
    return o


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
