# Column Converter

Automated conversion of units in columns of a latex table.  
\# Processing strings in Python

# Usage

```
./preproc.sh table.tex  # Note: this is in-place op.
./cols-convert.py --fields=3,6 table.tex
```

`preproc.sh` aligns the table, mends broken with newline chars rows
(if there are more than one \n, it is not going to work;
change the regex pattern for this case). It is better to backup `table.tex`
before calling the script.

`cols-convert.py` changes the units according to the rule
(function `converter` defined in the file). Columns for the conversion
are specified via `--fields` option and use 1-based numbering.

(`table.tex` is given in the repo as an example of the target table.)
