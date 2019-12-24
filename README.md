# nv
Evaluate numbers from a string on the command line.
--------------------------------------------------------

Python shell utility for numerical processing in bash
-----------------------------------------------------


INSTALL:
--------

   `python nv.py install

    or

    cp -v nv.py $HOME/bin/

    chmod -v 0755 ~/bin/nv.py

    ln -s ~/bin/nv.py ~/bin/nv
`


try:
----

 `nv 1 2 3 4 5 6 7 8 9 10`

should print out

55
--


nv test
-------

runs a bash script with nv

If so, you are good to go!


**usage:**

`nv <key>|expression  arg arg arg ...
           prog  | nv <keyword>`


    if receiving data from a pipe,
        nv evaluates numbers created by other programs.
    
        nv accepts one keyword and a list of numbers,
        or a string mathematical expression
        similar to
             "2 * pi * sin( sqrt(1/2) )"
    
              -- note the quotes or the shell will
                  interpret the * as a file glob and
                 the parens as syntax errors.
    
        If no keywords are given nv expects a list of numbers and will return the sum
    
        nv is designed for shells that do no do floating point by default (sh, bash)
        so they output integers. If you want floating point there are
    
        [fadd, fdiv, favg] which convert all arguments to floats first.
    
        preload option:  nv preload  runs python and this script and
                         exits so that it is quick to respond upon
                         subsequent calls in the script.
    
    
    
        note -- To see all available functions, type "nv help functions".
                To see some examples, type "nv help examples".



    [cmdline]
    
    nv 5 6 7 8 9               nv max  13 45 6 7 8 22 31 41 7
    ==>                        ==>
       35                        45
    ------------               ------------------------------
     
    nv pow 11 12               nv "sin(pi/4) * 4"
    ==>                        ==>
    3.13842837672e+12         2.82842712475
    ----------------          -------------------
    
    -------------------------------------------------------
     
    echo "5 7 9 2 3" | nv          echo "5 7 9 2 3" | nv mul
    ==>                            ==>
       26                              1890
    ---------------------          -------------------------
     
    echo "5 7 9 2 3" | nv fdiv     echo "sin(pi/4)" | nv
    ==>                            ==>
    0.0132275132275               0.707106781187

    --------------------------     ----------------------

    #!/bin/bash
    radius=3
    area=$(nv "pi * ${radius}**2")
    echo "area = ${area}"
 
    circ=$(nv "2 * pi * ${radius}")
    echo "circ = $circ"
 
    a=$(nv round ${area}) # bash only likes strings and ints
    c=$(nv round ${circ})
 
    echo "a = $a"
    echo "c = $c"
    let "x = $a * $c"  # let can do some arithmetic
    echo "x = $x"
 
    ==>
       area = 28.2743338823
       circ = 18.8495559215
       a = 28
       c = 19
       x = 532

---------------------------------------------------------------------

    echo "2 4 8 16 32 35" | nv log10       echo "2 4 8 16 32 35" | nv log2
    ==>                                    ==>
     0.301029995664                         1
     0.602059991328                         2
     0.903089986992                         3
     1.20411998266                          4
     1.50514997832                          5
     1.54406804435                          5.12928301694
`
    ---------------                         --------------------------------



