latexindent "$1" | sed -r 's; {2,}; ;g' | perl -0pe 's;(?<=\\hline)((?!\s*\\hline)\s*\S.*)\n((?!\s*\\hline)\s*\S.*\n?\s*)(?=\\hline);$1$2;g' > /tmp/tmp.tmp
latexindent /tmp/tmp.tmp | sed -r 's; {2,}; ;g' > "$1"
