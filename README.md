# bconv

## Description 

There are various ways to represent Braille symbols (also called Braille cells) in print and in electronic form. This utility makes it easy to convert between them.

These are the representations which bconv supports:

1. *Braille ASCII* (or more formally *The North American Braille ASCII Code*, also known as *SimBraille*) e.g.:

       HELLO

1. *Unicode Braille* e.g.:

       ⠓⠑⠇⠇⠕
(if you see nothing like Braille just above, then your browser doesn't use a Unicode font that includes Braille Patterns)

1.  *Dots Braille* e.g.:

        p125p15p123p123p135
        (125)(15)(123)(123)(135)
        ...

1.  *Pseudo Braille* e.g.:

        o o  o .  o o   
        o .  . o  o o   
        o .  . .  . .

As an example suppose that you have the Braille ASCII text `HELLO WORLD` and you want to convert it to Unicode Braille. What you need to run is this:

    # bconv -fa -tu 'HELLO WORLD'
    ⠓⠑⠇⠇⠕⠀⠺⠕⠗⠇⠙

or this:

    # echo 'HELLO WORLD' | bconv -fa -tu
    ⠓⠑⠇⠇⠕⠀⠺⠕⠗⠇⠙

You can start using bconv right away. Just note that `-f` stands for translate **f**rom and `-t` for translate **t**o. After the `-f` and `-t` you should add one character to specify the representation (valid characters are a,d,p and u for **A**SCII, **D**ot, **P**seudo or **U**nicode Braille respectively). Finally note that you can have Pseudo Braille only as the output of the conversion. All others may appear either as input or as output. Run bconv without any parameters to get a more detailed help on usage

Please note that **this is not a Braille translator**. It can’t convert plain text to Braille or vice versa. Use tools like liblouis for this job. If this sentence and the HELLO WORLD example above seems contradictory to you it's OK;  you just need to cover a bit more ground to grasp Braille.

More info in this blog post: https://ndemou.wordpress.com/2012/12/28/bconv-convert-between-braille-representations/

## Installation

The code was tested under Linux with python 3. 

To run it save both bconv and pybraille.py somewhere in your path and make bconv executable (`chmod u+x /path/to/saved/files/bconv`)
