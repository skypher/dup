dup
===

Fast no-frills duplicate file finder.

### But there are a lot of duplicate file finders out there already!

Yes, I've tried a couple of them. Unfortunately they were much too
slow and each one had a different way to specify the details of
their behavior.

So I wrote this utility in a day, featuring sane defaults, clean code
that is easy to modify, decent speed and a very simple interface.


### Requirements

Python 3 with batteries; I run it on Python 3.3 right now.

I haven't tested dup with Python 2.


### Running dup 

In line with the UNIX philosophy of /one program per task/, dup doesn't
provide any facility for configuring which files to include in the
duplication scan.

Instead you provide it with a file that contains a list of files; the
widespread `find` utility is ideally suited to this task:

    find target_dir1 target_dir2 -type f -size +10M > files.txt

Then you can run dup on the resulting list of files:

    ./dup.py files.txt

dup will read the list into memory, get the files' sizes, sort it by that
and then look for duplicates. It will ask you interactively which clone to
delete as it finds them. Type 1 for the first file listed, 2 for the second
file, anything else to not remove any of them.


### Limitations and caveats

* Undefined but non-destructive behavior occurs with:

    * file names that include newline characters
    * directories -- use `-type f` with find to exclude them

* To keep things efficient hashing only looks at the first 1024^2 bytes of
each file. You can easily change that number in the source.

* No provisions are made for efficient interruption and resumption of the
  analysis process (save for terminal suspend/resume of course).

* Raw key input (when you're given a 1/2 choice) can leave the terminal
  in uncooked mode.

* Raw key input (when you're given a 1/2 choice) ignores Control commands
  Like C-c 


### Future

For now dup does exactly what I need. If you need it to do something else
you can pay me to adapt it.

Please consider a donation if this little program has saved your time. :)

