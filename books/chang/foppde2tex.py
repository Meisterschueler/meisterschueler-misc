# coding: utf-8

import re

inputname = "foppde_mod.html"
outputname = "foppde.tex"

foppde = open(inputname).read()
s = foppde

s = re.sub("&auml;", "ä", s)
s = re.sub("&ouml;", "ö", s)
s = re.sub("&uuml;", "ü", s)
s = re.sub("&Auml;", "Ä", s)
s = re.sub("&Ouml;", "Ö", s)
s = re.sub("&Uuml;", "Ü", s)
s = re.sub("&agrave;", "à", s)
s = re.sub("&eacute;", "é", s)
s = re.sub("&egrave;", "è", s)
s = re.sub("&szlig;", "ß", s)
s = re.sub("&quot;", "\"", s)
s = re.sub("&minus;", "\\-", s)
s = re.sub("&lt;", "\\lt", s)
s = re.sub("&asymp;", "\\approx", s)
s = re.sub("&copy;", "\\copyright", s)
s = re.sub("&reg;", "\\textregistered", s)
s = re.sub("\\%", "\\\\%", s)

#GLIEDERUNG
s = re.sub("(<a name=\")(.+)(\"></a>[\n\r\s]+)"
    "(<h2><u>Kapitel [0-9]+\: )(.+)(</u></h2>)",
    lambda m: "\\part{%s}\\hypertarget{%s}{}" % (m.group(5), m.group(2)), s)

s = re.sub("(<a name=\")(.+)(\"></a>[\n\r\s]+)"
    "(<h2><u>)(.+)(</u></h2>)",
    lambda m: "\\section*{%s}\\hypertarget{%s}{}" % (m.group(5), m.group(2)), s)


s = re.sub("(<a name=\")(.+)(\"></a>[\n\r\s]+)(<h2><br>[IVX]+\. )(.+)(</h2>)",
    lambda m: "\\chapter{%s}\\hypertarget{%s}{}" % (m.group(5), m.group(2)), s)

s = re.sub("(<h2><br>[IVX]+\. )(.+)(</h2>)",
    lambda m: "\\chapter{%s}" % m.group(2), s)


s = re.sub("(<a name=\")(.+)(\"></a>[\n\r\s]+)"
    "(<h3><br>[0-9]+\. )(.+?)(\\s*</h3>)",
    lambda m: "\\section{%s}\\hypertarget{%s}{}" % (m.group(5), m.group(2)), s)

s = re.sub("(<h3><br>[0-9]+\. )(.+)(</h3>)",
    lambda m: "\\section{%s}" % m.group(2), s)


s = re.sub("(<a name=\")(.+)(\"></a>[\n\r\s]+)"
    "(<h3><br>[0-9]+[a-z]+\. )(.+)(</h3>)",
    lambda m: "\\subsection{%s}\\hypertarget{%s}{}"
    % (m.group(5), m.group(2)), s)

s = re.sub("(<h3><br>[0-9]+[a-z]+\. )(.+)(</h3>)",
    lambda m: "\\subsection{%s}" % m.group(2), s)


s = re.sub("(<a name=\")(.+)(\"></a>\r\n\r\n)(<h4><br>)(.+)(</h4>)",
    lambda m: "\\subsubsection{%s}\\hypertarget{%s}{}"
    % (m.group(5), m.group(2)), s)

#FUSSNOTEN
p = re.compile("(\s*<i><font color=\"navy\">\\s*\[)(.+?)(\]</font></i>)",
    re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "\\footnote{%s}" % m.group(2), s)


#ZULETZT GEÄNDERT
#<p><b><i><font color="green" size="-1"><br>[zuletzt ge&auml;ndert 09.08.2009; <a href="./Originale/book_090306.pdf">englisches Original vom 06.03.2009</a> (2 MB)]</font></i></b>
#</p>
p = re.compile("(<p><b><i><font color=\"green\" size=\"\-1\"><br>\[)"
    "(.+?)(; <a href.+?</font></i></b>\\s*?</p>)")
s = re.sub(p, lambda m: "%% %s" % m.group(2), s)

#FETT, KURSIV, UNTERSTRICHEN
p = re.compile("(<b>\\s*)(.+?)(\\s*</b>)", re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "\\textbf{%s}" % m.group(2), s)

p = re.compile("(<i>\\s*)(.+?)(\\s*</i>)", re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "\\textit{%s}" % m.group(2), s)

s = re.sub("(<u>\\s*)(.+?)(\\s*</u>)",
    lambda m: "\\underline{%s}" % m.group(2), s)


p = re.compile("(<p>)(.+?)(</p>)", re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "%s" % m.group(2), s)


#LINKS
# <a href="#c1iii6hand">Hand-Ged?chtnis</a>
p = re.compile("(<a href=\"#)(.+?)(\">\\s*)(.+?)(\\s*</a>)",
    re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "\\hyperlink{%s}{%s}" % (m.group(2), m.group(4)), s)

# <a href="./Originale/book_090306.pdf">englisches Original vom 06.03.2009</a>
p = re.compile("(<a href=\")(.+?)(\">)(.+?)(\\s*</a>)",
    re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "\\hyperref[%s]{%s}" % (m.group(2), m.group(4)), s)

p = re.compile("(<a name=\")(.+?)(\"></a>)", re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "\\hypertarget{%s}{}" % m.group(2), s)


#LISTEN
p = re.compile("(<ul>)(.+?)(</ul>)", re.MULTILINE | re.DOTALL)
s = re.sub(p,
    lambda m: "\\begin{itemize} "
    "%s \\end{itemize}" % m.group(2), s)

p = re.compile("(<ol>)(.+?)(</ol>)", re.MULTILINE | re.DOTALL)
s = re.sub(p,
    lambda m: "\\begin{enumerate} "
    "%s \\end{enumerate}" % m.group(2), s)

p = re.compile("(<ol type=\"1\">)(.+?)(</ol>)", re.MULTILINE | re.DOTALL)
s = re.sub(p,
    lambda m: "\\begin{enumerate}[label={\\arabic*.}] "
    "%s \\end{enumerate}" % m.group(2), s)

p = re.compile("(<ol type=\"a\">)(.+?)(</ol>)", re.MULTILINE | re.DOTALL)
s = re.sub(p,
    lambda m: "\\begin{enumerate}[label={\\alph*.}] "
    "%s \\end{enumerate}" % m.group(2), s)

p = re.compile("(<ol type=\"i\">)(.+?)(</ol>)", re.MULTILINE | re.DOTALL)
s = re.sub(p,
    lambda m: "\\begin{enumerate}[label={\\roman*.}] "
    "%s \\end{enumerate}" % m.group(2), s)

p = re.compile("(<li>)(.+?)(</li>)", re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "\\item %s" % m.group(2), s)


#TABELLEN
s = re.sub("<tr>[\n\r\s]*?<td>", "", s)
s = re.sub("</td>[\n\r\s]*?<td>", " & ", s)
s = re.sub("</td>[\n\r\s]*?</tr>", " \\\\ ", s)


#AUFRÄUMEN
p = re.compile("(<font.*?>)(.+?)(</font>)", re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "%s" % m.group(2), s)

s = re.sub("\\$", "\\\\$", s)
s = re.sub("\\#", "\\\\#", s)
s = re.sub("&nbsp;", " ", s)
s = re.sub("<hr>", "", s)


#ZITATE
p = re.compile("(\\\"\\s*)(.+?)(\\s*\\\")", re.MULTILINE | re.DOTALL)
s = re.sub(p, lambda m: "\\enquote{%s}" % m.group(2), s)

#KOMMENTARE (AUSSER HTML)
p = re.compile("(<!-- )(.+?)( -->)")
for (sbegin, comment, send) in re.findall(p, s):
    if ".html" not in comment:
        s = re.sub("<!-- " + comment + " -->", "%: " + comment, s)

#RAW OUTPUT
fobj_out = open(outputname, "w")
fobj_out.write(s)
fobj_out.close()

#SPLIT AB HTML-KOMMENTAR
p = re.compile("(<!-- )(.+?)(\\.html -->)",
    re.MULTILINE | re.DOTALL)

occ = list()
for m in p.finditer(s):
    occ.append(m.start())

occ.reverse()

for part_i in occ:
    part = s[part_i:]
    s = s[:part_i]

    p = re.compile("(<!-- )(.+?)(\\.html -->)(.*)",
        re.MULTILINE | re.DOTALL)

    for (sstart, name, send, content) in re.findall(p, part):
        content = "% File: " + name + content
        part_out = open(name + ".tex", "w")
        part_out.write(content)
        part_out.close()
