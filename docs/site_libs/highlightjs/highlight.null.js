! function(e) {
    var n = "object" == typeof window && window || "object" == typeof self && self;
    "undefined" != typeof exports ? e(exports) : n && (n.hljs = e({}), "function" == typeof define && define.amd && define([], function() {
        return n.hljs
    }))
}(function(e) {
    function n(e) {
        return e.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    }

    function t(e) {
        return e.nodeName.toLowerCase()
    }

    function r(e, n) {
        var t = e && e.exec(n);
        return t && 0 === t.index
    }

    function a(e) {
        return m.test(e)
    }

    function c(e) {
        var n, t = {},
            r = Array.prototype.slice.call(arguments, 1);
        for (n in e) t[n] = e[n];
        return r.forEach(function(e) {
            for (n in e) t[n] = e[n]
        }), t
    }

    function i(e) {
        var n = [];
        return function e(r, a) {
            for (var c = r.firstChild; c; c = c.nextSibling) 3 === c.nodeType ? a += c.nodeValue.length : 1 === c.nodeType && (n.push({
                event: "start",
                offset: a,
                node: c
            }), a = e(c, a), t(c).match(/br|hr|img|input/) || n.push({
                event: "stop",
                offset: a,
                node: c
            }));
            return a
        }(e, 0), n
    }

    function o(e) {
        function n(e) {
            return e && e.source || e
        }

        function t(t, r) {
            return new RegExp(n(t), "m" + (e.cI ? "i" : "") + (r ? "g" : ""))
        }! function r(a, i) {
            if (!a.compiled) {
                if (a.compiled = !0, a.k = a.k || a.bK, a.k) {
                    var o = {},
                        u = function(n, t) {
                            e.cI && (t = t.toLowerCase()), t.split(" ").forEach(function(e) {
                                var t = e.split("|");
                                o[t[0]] = [n, t[1] ? Number(t[1]) : 1]
                            })
                        };
                    "string" == typeof a.k ? u("keyword", a.k) : d(a.k).forEach(function(e) {
                        u(e, a.k[e])
                    }), a.k = o
                }
                a.lR = t(a.l || /\w+/, !0), i && (a.bK && (a.b = "\\b(" + a.bK.split(" ").join("|") + ")\\b"), a.b || (a.b = /\B|\b/), a.bR = t(a.b), a.e || a.eW || (a.e = /\B|\b/), a.e && (a.eR = t(a.e)), a.tE = n(a.e) || "", a.eW && i.tE && (a.tE += (a.e ? "|" : "") + i.tE)), a.i && (a.iR = t(a.i)), null == a.r && (a.r = 1), a.c || (a.c = []), a.c = Array.prototype.concat.apply([], a.c.map(function(e) {
                    return (n = "self" === e ? a : e).v && !n.cached_variants && (n.cached_variants = n.v.map(function(e) {
                        return c(n, {
                            v: null
                        }, e)
                    })), n.cached_variants || n.eW && [c(n)] || [n];
                    var n
                })), a.c.forEach(function(e) {
                    r(e, a)
                }), a.starts && r(a.starts, i);
                var s = a.c.map(function(e) {
                    return e.bK ? "\\.?(" + e.b + ")\\.?" : e.b
                }).concat([a.tE, a.i]).map(n).filter(Boolean);
                a.t = s.length ? t(s.join("|"), !0) : {
                    exec: function() {
                        return null
                    }
                }
            }
        }(e)
    }

    function u(e, t, a, c) {
        function i(e, n, t, r) {
            var a = '<span class="' + (r ? "" : R.classPrefix);
            return (a += e + '">') + n + (t ? "" : w)
        }

        function l() {
            N += null != v.sL ? function() {
                var e = "string" == typeof v.sL;
                if (e && !h[v.sL]) return n(E);
                var t = e ? u(v.sL, E, !0, m[v.sL]) : s(E, v.sL.length ? v.sL : void 0);
                return v.r > 0 && (x += t.r), e && (m[v.sL] = t.top), i(t.language, t.value, !1, !0)
            }() : function() {
                var e, t, r, a, c, o, u;
                if (!v.k) return n(E);
                for (a = "", t = 0, v.lR.lastIndex = 0, r = v.lR.exec(E); r;) a += n(E.substring(t, r.index)), c = v, o = r, u = p.cI ? o[0].toLowerCase() : o[0], (e = c.k.hasOwnProperty(u) && c.k[u]) ? (x += e[1], a += i(e[0], n(r[0]))) : a += n(r[0]), t = v.lR.lastIndex, r = v.lR.exec(E);
                return a + n(E.substr(t))
            }(), E = ""
        }

        function f(e) {
            N += e.cN ? i(e.cN, "", !0) : "", v = Object.create(e, {
                parent: {
                    value: v
                }
            })
        }

        function b(e, n) {
            if (E += e, null == n) return l(), 0;
            var t = function(e, n) {
                var t, a;
                for (t = 0, a = n.c.length; a > t; t++)
                    if (r(n.c[t].bR, e)) return n.c[t]
            }(n, v);
            if (t) return t.skip ? E += n : (t.eB && (E += n), l(), t.rB || t.eB || (E = n)), f(t), t.rB ? 0 : n.length;
            var c, i = function e(n, t) {
                if (r(n.eR, t)) {
                    for (; n.endsParent && n.parent;) n = n.parent;
                    return n
                }
                return n.eW ? e(n.parent, t) : void 0
            }(v, n);
            if (i) {
                var o = v;
                o.skip ? E += n : (o.rE || o.eE || (E += n), l(), o.eE && (E = n));
                do {
                    v.cN && (N += w), v.skip || (x += v.r), v = v.parent
                } while (v !== i.parent);
                return i.starts && f(i.starts), o.rE ? 0 : n.length
            }
            if (c = n, !a && r(v.iR, c)) throw new Error('Illegal lexeme "' + n + '" for mode "' + (v.cN || "<unnamed>") + '"');
            return E += n, n.length || 1
        }
        var p = g(e);
        if (!p) throw new Error('Unknown language: "' + e + '"');
        o(p);
        var d, v = c || p,
            m = {},
            N = "";
        for (d = v; d !== p; d = d.parent) d.cN && (N = i(d.cN, "", !0) + N);
        var E = "",
            x = 0;
        try {
            for (var y, B, L = 0; v.t.lastIndex = L, y = v.t.exec(t);) B = b(t.substring(L, y.index), y[0]), L = y.index + B;
            for (b(t.substr(L)), d = v; d.parent; d = d.parent) d.cN && (N += w);
            return {
                r: x,
                value: N,
                language: e,
                top: v
            }
        } catch (e) {
            if (e.message && -1 !== e.message.indexOf("Illegal")) return {
                r: 0,
                value: n(t)
            };
            throw e
        }
    }

    function s(e, t) {
        t = t || R.languages || d(h);
        var r = {
                r: 0,
                value: n(e)
            },
            a = r;
        return t.filter(g).forEach(function(n) {
            var t = u(n, e, !1);
            t.language = n, t.r > a.r && (a = t), t.r > r.r && (a = r, r = t)
        }), a.language && (r.second_best = a), r
    }

    function l(e) {
        return R.tabReplace || R.useBR ? e.replace(E, function(e, n) {
            return R.useBR && "\n" === e ? "<br>" : R.tabReplace ? n.replace(/\t/g, R.tabReplace) : ""
        }) : e
    }

    function f(e) {
        var r, c, o, f, b, d, h, m, E, w, x = function(e) {
            var n, t, r, c, i = e.className + " ";
            if (i += e.parentNode ? e.parentNode.className : "", t = N.exec(i)) return g(t[1]) ? t[1] : "no-highlight";
            for (n = 0, r = (i = i.split(/\s+/)).length; r > n; n++)
                if (a(c = i[n]) || g(c)) return c
        }(e);
        a(x) || (R.useBR ? (r = document.createElementNS("http://www.w3.org/1999/xhtml", "div")).innerHTML = e.innerHTML.replace(/\n/g, "").replace(/<br[ \/]*>/g, "\n") : r = e, b = r.textContent, o = x ? u(x, b, !0) : s(b), (c = i(r)).length && ((f = document.createElementNS("http://www.w3.org/1999/xhtml", "div")).innerHTML = o.value, o.value = function(e, r, a) {
            function c() {
                return e.length && r.length ? e[0].offset !== r[0].offset ? e[0].offset < r[0].offset ? e : r : "start" === r[0].event ? e : r : e.length ? e : r
            }

            function i(e) {
                l += "<" + t(e) + p.map.call(e.attributes, function(e) {
                    return " " + e.nodeName + '="' + n(e.value).replace('"', "&quot;") + '"'
                }).join("") + ">"
            }

            function o(e) {
                l += "</" + t(e) + ">"
            }

            function u(e) {
                ("start" === e.event ? i : o)(e.node)
            }
            for (var s = 0, l = "", f = []; e.length || r.length;) {
                var b = c();
                if (l += n(a.substring(s, b[0].offset)), s = b[0].offset, b === e) {
                    f.reverse().forEach(o);
                    do {
                        u(b.splice(0, 1)[0]), b = c()
                    } while (b === e && b.length && b[0].offset === s);
                    f.reverse().forEach(i)
                } else "start" === b[0].event ? f.push(b[0].node) : f.pop(), u(b.splice(0, 1)[0])
            }
            return l + n(a.substr(s))
        }(c, i(f), b)), o.value = l(o.value), e.innerHTML = o.value, e.className = (d = e.className, h = x, m = o.language, E = h ? v[h] : m, w = [d.trim()], d.match(/\bhljs\b/) || w.push("hljs"), -1 === d.indexOf(E) && w.push(E), w.join(" ").trim()), e.result = {
            language: o.language,
            re: o.r
        }, o.second_best && (e.second_best = {
            language: o.second_best.language,
            re: o.second_best.r
        }))
    }

    function b() {
        if (!b.called) {
            b.called = !0;
            var e = document.querySelectorAll("pre code");
            p.forEach.call(e, f)
        }
    }

    function g(e) {
        return e = (e || "").toLowerCase(), h[e] || h[v[e]]
    }
    var p = [],
        d = Object.keys,
        h = {},
        v = {},
        m = /^(no-?highlight|plain|text)$/i,
        N = /\blang(?:uage)?-([\w-]+)\b/i,
        E = /((^(<[^>]+>|\t|)+|(?:\n)))/gm,
        w = "</span>",
        R = {
            classPrefix: "hljs-",
            tabReplace: null,
            useBR: !1,
            languages: void 0
        };
    return e.highlight = u, e.highlightAuto = s, e.fixMarkup = l, e.highlightBlock = f, e.configure = function(e) {
        R = c(R, e)
    }, e.initHighlighting = b, e.initHighlightingOnLoad = function() {
        addEventListener("DOMContentLoaded", b, !1), addEventListener("load", b, !1)
    }, e.registerLanguage = function(n, t) {
        var r = h[n] = t(e);
        r.aliases && r.aliases.forEach(function(e) {
            v[e] = n
        })
    }, e.listLanguages = function() {
        return d(h)
    }, e.getLanguage = g, e.inherit = c, e.IR = "[a-zA-Z]\\w*", e.UIR = "[a-zA-Z_]\\w*", e.NR = "\\b\\d+(\\.\\d+)?", e.CNR = "(-?)(\\b0[xX][a-fA-F0-9]+|(\\b\\d+(\\.\\d*)?|\\.\\d+)([eE][-+]?\\d+)?)", e.BNR = "\\b(0b[01]+)", e.RSR = "!|!=|!==|%|%=|&|&&|&=|\\*|\\*=|\\+|\\+=|,|-|-=|/=|/|:|;|<<|<<=|<=|<|===|==|=|>>>=|>>=|>=|>>>|>>|>|\\?|\\[|\\{|\\(|\\^|\\^=|\\||\\|=|\\|\\||~", e.BE = {
        b: "\\\\[\\s\\S]",
        r: 0
    }, e.ASM = {
        cN: "string",
        b: "'",
        e: "'",
        i: "\\n",
        c: [e.BE]
    }, e.QSM = {
        cN: "string",
        b: '"',
        e: '"',
        i: "\\n",
        c: [e.BE]
    }, e.PWM = {
        b: /\b(a|an|the|are|I'm|isn't|don't|doesn't|won't|but|just|should|pretty|simply|enough|gonna|going|wtf|so|such|will|you|your|they|like|more)\b/
    }, e.C = function(n, t, r) {
        var a = e.inherit({
            cN: "comment",
            b: n,
            e: t,
            c: []
        }, r || {});
        return a.c.push(e.PWM), a.c.push({
            cN: "doctag",
            b: "(?:TODO|FIXME|NOTE|BUG|XXX):",
            r: 0
        }), a
    }, e.CLCM = e.C("//", "$"), e.CBCM = e.C("/\\*", "\\*/"), e.HCM = e.C("#", "$"), e.NM = {
        cN: "number",
        b: e.NR,
        r: 0
    }, e.CNM = {
        cN: "number",
        b: e.CNR,
        r: 0
    }, e.BNM = {
        cN: "number",
        b: e.BNR,
        r: 0
    }, e.CSSNM = {
        cN: "number",
        b: e.NR + "(%|em|ex|ch|rem|vw|vh|vmin|vmax|cm|mm|in|pt|pc|px|deg|grad|rad|turn|s|ms|Hz|kHz|dpi|dpcm|dppx)?",
        r: 0
    }, e.RM = {
        cN: "regexp",
        b: /\//,
        e: /\/[gimuy]*/,
        i: /\n/,
        c: [e.BE, {
            b: /\[/,
            e: /\]/,
            r: 0,
            c: [e.BE]
        }]
    }, e.TM = {
        cN: "title",
        b: e.IR,
        r: 0
    }, e.UTM = {
        cN: "title",
        b: e.UIR,
        r: 0
    }, e.METHOD_GUARD = {
        b: "\\.\\s*" + e.UIR,
        r: 0
    }, e
});
