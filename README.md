# PyCharCounter

PyCharCounter is a small Python 3 script that counts the occurrence of every character in its input and outputs a CSV table.

Nonprinting characters are escaped using a C-style escape (e.g. `\n`) wherever possible. If there is no well-defined C-style escape, then they are escaped as `\UXXXXXXXX`.

Commas are not explicitly escaped and are instead handled by the CSV dialect. Python's default CSV dialect (`excel`) adds quotes around delimiters. (See the usage example below).

The exact behavior of how nonprinting characters are escaped is unstable until I receive more feedback from the wider community.


## Usage Example

Command:

```
$ charcounter -i input.txt -o output.txt
```

Input file:

```
Hello, world!
```

Output file:

```
H,1
e,1
l,3
o,2
",",1
 ,1
w,1
r,1
d,1
!,1
\n,1
```


## Configuration

The output can be configured with the `--output-delimiter` and `--output-dialect` options. (If TSV output is desired, use `--output-delimiter '\t'`)

