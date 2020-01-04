#!/usr/bin/env python3
# nval


from __future__ import print_function
from math import *

import os, sys, signal, socket, time

if (sys.version_info < (3, 0)):
    import thread
else:
    import _thread

""" nv
evaluate numbers from a string on the command line.

INSTALL:
    python nv.py install
  or
    cp -v nv.py $HOME/bin/
    chmod -v 0755 ~/bin/nv.py
    ln -s ~/bin/nv.py ~/bin/nv

try


 nv 1 2 3 4 5 6 7 8 9 10

should print out
55

 nv test
runs a bash script with nv

If so, you are good to go!

"""


# install defaults
__install_location__ =  "".join((os.getenv('HOME'), "/bin"))

__install_mode__  = (0o0775) # new octal notation

__no_exec_mode__  = (0o664)


# meta info
__author__      = ("Chris Reid")

__category__    = ("numeric processing")

__copyright__   = ("Copyright: 2018-2020")

__country__     = ("United States of America")

__credits__     = ("Python Software Foundation", "Free Software Foundation" )

__email__       = ("spikeysnack@gmail.com")

__file__        = ( "nval" , "nv" )

__license__     = ( """Free for all non-commercial purposes.
                       Modifications allowed but original attribution must be included.
                       see (http://creativecommons.org/licenses/by-nc/4.0/) """)

__maintainer__  = ("Chris Reid")

__modification_date__ = ("4 Jan 2020")

__version__     = ("1.6")

__status__      = ("working")


_all__ = ( "num", "n_eval", "printf" , "eprint", "is_close", "check_update",
           "help", "version", "test", "examples", "install", "reinstall",
           "safe_functons", "funcs_available" )



# debug vars
_debug    = False   # for debugging (not implemented)
_function = None    #                ''
_cmdline  = None    #                ''


# program functions
def version():

    """ print out some version info """

    vs = ( "nval  version ", __version__ ,  __modification_date__  )
    _version_string = '\t'.join(vs)


    cc = ( __copyright__ ,  __country__ )
    _copy_country = '\t'.join(cc)

    astr = ( "Author:", __maintainer__ , "email:",  __email__ )
    _auth_string = '\t'.join(astr)

    ver = ( _version_string, _copy_country, _auth_string )
    ver = '\n'.join(ver)

    print( ver )

def printf(format, *args):
    """ ersatz printf function """
    sys.stdout.write(format % args)

def eprint(*args, **kwargs):
    """ print to stderr """
    print(*args, file=sys.stderr, **kwargs)


def install():
    """ install in users path """
    from os.path import expanduser

    import py_compile

    source  = "nv.py"

    dest    = os.path.join( __install_location__, source )
    destlnk = os.path.join( __install_location__, "nv" )


    if not os.path.exists( dest ):

            try:

                with open(source, 'r') as src, open(dest, 'w') as dst: dst.write(src.read())

                os.chmod(dest, __install_mode__ )

                py_compile.compile(dest)

                os.symlink(dest , destlnk )

                if os.path.exists( destlnk):

                    print( "nv installed in user bin directory\n")

            except IOError as ioerr:
                eprint("nv install failure: " , str(ioerr) )
                sys.exit(1)

    else:
        eprint("nv already installed")


def reinstall():
    """ reinstall in users path """

    from os.path import expanduser

    import py_compile

    source  = "nv.py"

    old     = "".join ( (source ,".old" ) )

    oldname  = os.path.join( __install_location__, old  )
    dest     = os.path.join( __install_location__, source )
    destlnk  = os.path.join( __install_location__, "nv" )


    if not os.path.exists( dest ):
       install()
       return

    else:
            try:

                from filecmp  import cmp

                if cmp( source, dest):
                    print("nv is up to date.")
                    return
                else:
                    print("updating file")

                if os.path.islink(destlnk):
                    os.unlink(destlnk)

                os.rename(dest , oldname  )

                os.chmod(oldname, __no_exec_mode__ ) # remove executable bit

                with open(source, 'r') as src, open(dest, 'w') as dst: dst.write(src.read())

                os.chmod(dest, __install_mode__ )

                py_compile.compile(dest)

                os.symlink(dest , destlnk )

                if os.path.exists( destlnk):

                    print( "nv reinstalled in user bin directory\n")


            except IOError as ioerr:
                eprint("nv install failure: " , str(ioerr) )
                sys.exit(1)

def check_update():
    """ check if git has newer version """
    import subprocess

    cmd = ("/usr/bin/git", "fetch" )

    OK  = ("Already up-to-date.")
    Available = ("Update is avaliable")

    try:
        result =  subprocess.check_output( cmd , universal_newlines=True, stderr=subprocess.STDOUT, shell=False )

        if result:

            print(result)

            print(Available)

            input = raw_input("Merge update now  y/n? [n]") or "n"

            if 'y' in input.lower():
                upcmd = ("git", "merge", "origin")
                update_result =  subprocess.check_output( cmd , universal_newlines=True, stderr=subprocess.STDOUT, shell=False )
                print(update_result)

        else:

            print("status = " ,  OK )





    except subprocess.CalledProcessError as cpe:

        eprint( str(cpe) )





def test():
    """ a bash script heredoc """

    testfile = "/tmp/nvtest"

    bash_script = '''
    #!/bin/bash

    # test nv in a bash script 

    echo "running bash ${0}"   
    pi=$(nv pi)
    echo "pi = ${pi}"

    radius=2
    echo "radius = ${radius}"

    # area of circle
    area=$(nv "pi * ${radius}**2") 

    echo "area = ${area}" 

    #circumference of circle
    circ=$(nv "2 * pi * ${radius}")
    echo "circumference = ${circ}"


    # round to integers for bash
    a=$(nv round ${area})

    c=$(nv round ${circ})

    echo "area = ${a}"
    echo "circumference = ${c}"
    let  "x = a * c"
    echo "x = ${x}"


    # end
    '''
    print(bash_script)

    cmd = " ".join ( ("/bin/bash", testfile) )

    try:

        fd = open(testfile , "w")

        fd.write(bash_script)

        fd.close()

        os.system(cmd)

        os.remove(testfile)

    except IOError as ioerr:
        sys.stderr.write("test failed to execute:\t " + ioerr)




# try to return a number from a string

def num(s):
    """ convert string to int or float
        could be binary or hex as well
        if neither raise
    """

    try:
        if  isinstance(s, str ):

            if s.startswith("0x"):
                s = int(s, 16)
            elif s.startswith("0o"):
                s = int(s, 8)
            elif s.startswith("0b"):
                s = int(s, 2)

        return int(s)

    except ValueError:

        try:

            return float(s)

        except ValueError:  # not an int or float -- (what?)
            raise


def isclose(f, g, tol=0.00004):
    """ round if close within tolerance """
    r6 = round(g, 5)

    if  fabs(f - r6) < tol:
        return r6
    else:
        return f



# we do not want arbitrary code executing

def safe_functions():
    """ allow only these functions in eval """


    # make a tuple of safe function strings
    safe_list = ('bin', 'bool', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees',
                 'e', 'exp', 'fabs', 'fexp', 'floor', 'fmod', 'frexp', 'hex', 'hypot', 
                 'ldexp', 'log','log2', 'log10', 'modf', 'oct', 'pi', 'pow', 'radians',  
                 'sin', 'sinh', 'sqrt', 'tan', 'tanh',
                 'trunc', 'abs', 'int','float', 'max','min', 'round', 'sum', 'range' )

    # make a tuple of safe functions
    safe_funcs = ( bin, bool, acos, asin, atan, atan2, ceil, cos, cosh, degrees,
                   e, exp, fabs, pow, floor, fmod,  frexp, hex, hypot, 
                   ldexp, log, log2, log10, modf, oct, pi, pow, radians,  
                   sin, sinh, sqrt, tan, tanh,
                   trunc, abs, int,float, max, min, round, sum, range )

 

    # combine them into a dispatch table
    safe_dict =  dict( list(zip(safe_list, safe_funcs)) )


    return safe_dict


#yes this is global
safe_dict = safe_functions()

# tuple of local functions
localfuncs = ('area', 'avg', 'count', 'div', 'exp2', 'expe', 
              'favg', 'fdiv', 'fexploge', 'file append', 'file prepend', 'file read', 'file write', 
              'fpow', 'frames', 'frand', 'hms', 
              'logn', 'md5', 'mult', 'rand', 'repeat', 'rev', 'rsort', 
              'runtimes', 'seconds', 'sha1', 'sha25', 'sort', 'sub', 'timecode')


# what functions can nv perform?
def funcs_available():
    """ print a list of available math functions
        (see safe_functions above)            """
    

    count = 0
    for k in sorted(safe_dict.keys() ):
        count +=1
        if safe_dict[k]:
#            print( k , end=' ')
            print( "{: >10}".format(k) , end='\t')

        if (count % 8) == 0:
            printf("\n")

    printf("\n")

    count=0
    for f in sorted(localfuncs):
        count +=1
        print( "{: >10}".format(f) , end='\t')
        if (count % 8) == 0:
            printf("\n")
    printf("\n")


# take in expressions and evaluate them -- restricted
def n_eval( l ):
    """ eval math expression -- restricted eval """

    # print("l = " , l)

    _function = "n_eval" + ": " +  str(l)

    if _debug : print( (_function))

    try:
        #restrict eval to safe functions ( no file R/W or code exec )
        nres = eval( l , {"__builtins__":None}, safe_dict )

        return nres

    except:
        return None


# help message
def help( s="" ):
    """ print out a usage message """

    h1 = '''
    usage: nv <key>|expression  arg arg arg ...
           prog  | nv <keyword>


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

'''

    if s == "functions":
        funcs_available()
    elif s == "examples":
        examples()
    else:
        print (h1)


# print examples
def examples():

    """ print out some examples  'nv help examples' """

    examples1 = '''

    [cmdline]

    nv 5 6 7 8 9               nv max  13 45 6 7 8 22 31 41 7
    ==>                        ==>
       35                        45
   -------------               ------------------------------

    nv pow 11 12               nv "sin(pi/4) * 4"
    ==>                        ==>
       3.13842837672e+12         2.82842712475
    --------------------       -----------------

    -------------------------------------------------------

    echo "5 7 9 2 3" | nv          echo "5 7 9 2 3" | nv mul
    ==>                            ==>
      26                              1890
    ---------------------          -------------------------

    echo "5 7 9 2 3" | nv fdiv     echo "sin(pi/4)" | nv
    ==>                            ==>
      0.0132275132275               0.707106781187

    '''

    examples2 = '''
   ----------------------------------------------------------------------

    [#!/bin/bash]
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

   ----------------------------------------------------------------------

   echo "2 4 8 16 32 35" | nv log10       echo "2 4 8 16 32 35" | nv log2
   ==>                                    ==>
     0.301029995664                         1
     0.602059991328                         2
     0.903089986992                         3
     1.20411998266                          4
     1.50514997832                          5
     1.54406804435                          5.12928301694

   --------------------------------      --------------------------------

    '''

    print(examples1)

    os.system('read -p "Press enter to continue..." K ')
    print()
    print(examples2)



# main function
if __name__ == "__main__":


    a = []
    n = []

    first  = None
    ispipe = False
    cmd    = None
    index  = 0

    if not sys.stdin.isatty():
        ispipe = True

    # there is a command to nv
    if len(sys.argv) > 1:

        _cmdline = list(sys.argv) 
        _function = "__main__"

        first = sys.argv[1]

        # check for help arg
        if first in  {"help",  "-h", "--h", "--help" } :
            if len(sys.argv) > 2:
                help(sys.argv[2])
            else:
                help()
            exit(0)

        if first in { "-v", "--version" , "version" }:
            version()

        if first in { "-t", "--test", "test" }:
            test()

        if first == "install":
            install()

        if first == "reinstall":
            reinstall()

        if first == "check_update":
            check_update()


       # check if we need to not read stdin for bash loops
        if first  == "-n" :
            realstdin = sys.stdin
            f = open(os.devnull, 'r')
            sys.stdin = f
            first = sys.argv[2]
            sys.argv = sys.argv[2:]
           # print( "argv ", repr(sys.argv) )


        # is argv[1] a number
        try:
            # an int
            i = int(first)
            first = None
            index = 1
        except ValueError:
            try:
                #a float
                i = float(first)
                first = None
                index = 1
            except ValueError:
                index = 2
    else:
        if not ispipe:
            sys.exit(0)


    # use pipe
    if ispipe:
        datastream = sys.stdin
        ss = "\n"

    # use argv args
    else:
        datastream = sys.argv[index:]
        ss = " "

        try:
            for x in datastream:
                try:
                    n = num(x) # int or float

                    a.append(n)

                except ValueError as verr: # must be a string then.
                    a.append(x)

        except Exception as e:
            sys.stderr.write("nv:" + str(x) + " " + str(e) )


    # no args, no pipe, no output.
    if not first and not datastream:
        sys.exit(0)


    # now here is a piece.
    # programs can pipe in numbers
    # on one line or multiple lines
    # it could be an expression as well

    if ispipe:
        # print ("ispipe")
        try:
            # convert to list of numbers
            for line in datastream:
                for x in line.split():
                    n = num(x)
                    if n:
                        a.append(n)


        except:
            # try evaluation as an expression
            try:
                res = n_eval(line)

                if res:
                    printf("%s\n" , res)

            except Exception as e:
                sys.stderr.write("nv: " + e )

            sys.exit(0)


    #####################################################
    # here we have a long series of numeric functions
    # if elif elif elif seems like a bad way to do this
    # but it allows local users to add their own functions
    # to the series easily and without side effects
    # and avoids making functions out of each tiny function
    # I suppose lambdas could be more 'pythonic' but this
    # is for use in bash scripts so I went with the
    # imperative paradigm. I imagine a tree-based
    # selection process might be more effficient
    # if and when this list grows to greater than 128
    # functions.


    # default
    if not first: first = "add"

    # function selection
    if first == "add" or first == "+":
        print( sum(i for i in a), end = ss )

    # add (floating point)
    elif first == "fadd":
        b = []
        try:
            for f in a:
                b.append(float(f))

            y = b[0]

            for x in b[1:]:
                y = y + x

            print( y, end=ss )

        except ValueError as ve:
            sys.stderr.write( ("ValueError:\t" + str(ve)) )


    # possibly to get the process preloaded in memory
    # so it is faster to run in the script
    elif first in {"load" , "preload", "start", "pass"}:
        pass

    # multiply
    elif first == "*" or first == "mul":
        y = 1
        for x in a:
            y = y * x
        print( y, end=ss )

    # divide (integer)
    elif first == "div":
        y = a[0]
        try:
            for x in a[1:]:
                y = y / x
            print( y, end=ss )
        except ZeroDivisionError:
            sys.stderr.write("ZeroDivisionError")

    # divide (floating point)
    elif first == "fdiv":
        b = []
        for f in a:
            b.append(float(f))
        try:
            y = b[0]
            for x in b[1:]:
                y = y / x
            print( y, end=ss )
        except ZeroDivisionError:
            sys.stderr.write("ZeroDivisionError")

    # max of list 
    elif first == "max":
        print( max(a), end=ss )

    # min of list 
    elif first == "min":
        print( min(a), end=ss )

    # round to integer
    elif first == "round":
        for r in a:
            print( int(round(r)), end=ss )

    # subtract args
    elif first == "sub":
        if len(a) >1:
            y = a[0]
            for x in a[1:]:
                y = y - x
        print(y, end=ss)

    # sort numerically
    elif first == "sort":
        for x in sorted(a):
            print(x, end=ss)

    # reverse sort
    elif first == "rsort":
        for x in sorted(a, reverse=True):
            print(x, end=ss)

    # reverse args
    elif first == "rev":
        a.reverse()
        for x in a:
            print(x, end=ss)

    # average (integer)
    elif first == "avg":
        avg = int(sum(a) / len(a))
        print(avg, end=ss)

    # average (floatng point)
    elif first == "favg":
        b = []
        for f in a:
            b.append(float(f))
        favg = sum(b) / float(len(b))
        print(favg, end=ss)

    # exponentiation (integer)
    elif first == "pow":
        n = a[0]
        for x in a[1:]:
            p = pow( n, x)
            print(int(p), end=ss)

    # exponentiation (floating point)
    elif first == "fpow":
        n = a[0]
        for x in a[1:]:
            p = pow( n, x)
            print(p, end=ss)

    # exponentiation (floating point)
    elif first == "exp":
        for x in a:
            p = int(pow( 10, x) )
            print(p, end=ss)
    # exponentiation (floating point)
    elif first == "fexp":
        for x in a:
            p = pow( 10, x)
            print(p, end=ss)

    # exponentiation (floating point)
    elif first == "exp2":
        for x in a:
            p = int(pow(2, x ))
            print(p, end=ss)

    # exponentiation (floating point)
    elif first == "expe":
        for x in a:
            p = exp(x)
            print(p, end=ss)


    # natural logarithm
    elif first in { "log", "loge" }:
        n = a[0]
        for x in a:
            p = log( x )
            print(p, end=ss)

    # base 10 logarithm
    elif first  == "log10":
        n = a[0]
        for x in a:
            p = log10( x )
            if p.is_integer():
                p = int(p)
            print(p, end=ss)

    # base 2 logarithm
    elif first == "log2":
        n = a[0]
        for x in a:
            p = log( x, 2 )
            if p.is_integer():
                p = int(p)
            print(p, end=ss)

    # base 2 logarithm
    elif first == "logn" :

        n = int( a[0] )

        for x in a[1:]:
            p = log( x, n  )

            if p.is_integer():
                p = int(p)
            print(p, end=ss)


    # generate a range of integers
    # 1 to n (1 arg)
    # n to m (2 args)
    # n to m step s (3 args)
    elif first == "range":
        if a:
            r = a[0]
            if len(a) == 1:
                for i in range(r):
                    print(i)
            elif len(a) == 2:
                s = a[1]
                for i in range( r, s  ):
                    print( i )
            elif len(a) >= 3:
                s = a[1]
                t = a[2]
                for i in range( r, s, t ):
                    print( i )

    # convert base10 to hexadecimal
    elif first == "hex":
        for x in a:
            if int(x):
                s = '{0:X}'.format(x)
                print(s, end=ss)

    # convert base10 to base2
    elif first == "bin":
        for x in a:
            if int(x):
                s ='{0:b}'.format(x)
                print(s, end=ss)

    # convert base10 to base8
    elif first == "oct":
        for x in a:
            if int(x):
                s = '{0:o}'.format(x)
                print(s, end=ss)

    # convert seconds to h:m:s
    elif first == "hms":
        for x in a:
            n = int(x)

            h = int(x / 3600)

            m = int((x/60) - (h*60))

            s = int(x - (h*3600) - (m*60) )

            out = "" + str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
            print(out, end=ss)


    # convert seconds to frames
    elif first == "frames":
        for x in a:
            fx = float(x)
            n = int(x)

            h = int(x / 3600)

            m = int((x/60) - (h*60))

            s = int(x - (h*3600) - (m*60) )

            remainder = fx - float(n)

            one_frame = 1.0 / 75.0

            frames = int( round( remainder / one_frame + 0.08)  )

            H = str(h).zfill(2)
            M = str(m).zfill(2)
            S = str(s).zfill(2)
            F = str(frames).zfill(2)

            out = ":".join( H, M, S, F ) 

            print(out, end=ss)


    # convert h:m:s to seconds
    elif first == "seconds":
        for x in a:
            h,m,s = x.split(':')
            sec = (int(h) *3600) + (int(m)*60) + int(s)
            print(sec,end=' ')


    # convert h:m:s or h:m:s:f to seconds
    elif first == "timecode":
        for x in a:
            f = None
#            print(x)
            l = x.split(':')

            if len(l) == 3:
                h,m,s = l

            if len(l) == 4:
                h,m,s,f = l

            sec = (int(h) *3600) + (int(m)*60) + int(s)

            if f:
                one_frame = 1.0 / 75.0
                frames = float(f) * one_frame
                fsec = float(sec) + frames

                print(round(fsec,6) ,end=' ')
            else:
                print(sec, end=' ')

    # multiply pairs of HxW
    elif first == "area":
        xl = a[::2]
        yl = a[1::2]
        area = [ (x*y) for x,y in zip(xl, yl)]
        print(*area)

    # radians to degrees
    elif first == "degrees":

        for r in a:

            d = degrees(r)

            d =  isclose( d, round(d,5) , 0.00004)
            print(d )

    # degrees to radians
    elif first == "radians":
        for x in a:
            print( radians(x) )

    # got pi ?
    elif first == "pi":
        print( pi )

    # got tau ?
    elif first == "tau":
        print( 2.0 *pi )

    # hash functions
    elif first == "md5":
        import hashlib
        md = hashlib.md5()
        for x in a:
            s = str(x).strip( '\"' )
            md.update(s.encode('utf-8'))
            print(md.hexdigest(), end = ' ')

    elif first == "sha1":
        import hashlib
        sha = hashlib.sha1()
        for x in a:
           s = str(x).strip('\"')
           sha.update(s.encode('utf-8'))
           print(sha.hexdigest(), end= ' ')

    elif first == "sha256":
        import hashlib
        sha = hashlib.sha256()
        for x in a:
            s = str(x).strip('\"')
            sha.update(s.encode('utf-8'))
            print(sha.hexdigest(), end= ' ')

    elif first == "count":

        """ return count of a string in a list"""

        x = str( a[0] )
        f = a[1]

        if os.path.isfile( f ):

            lines = []
            words = []

            print( a[1] + " is a file" )

            try:
                input = open(f, 'r')

                lines = input.readlines()

                input.close()

                for line in lines:

                    l  = line.split()

                    for w in l:
                        words.append(w)

                print( (words.count(x)) )

            except IOError as e:

                print( "I/O error({0}): {1}".format(e.errno, e.strerror) )


        else:
            y = a[1:]

            z = [a for b in y for a in b.split() ]

            print ( z.count(x) )


    elif first == "rand":
        import random

        random.seed()

        if not a:
            print( random.randint(0, 0xffffffff) )
        else:

            if len(a) == 1:

                cnt = a[0]

                while cnt > 0:
                    print( (random.randint(0, 0xffffffff) ) )
                    cnt -= 1

            elif len(a) == 2:

                x,y = ( min(a[0],a[1]), max(a[0], a[1] ) )

                print( random.randint(x, y) )


            elif len(a) >= 3:

                x,y = ( min(a[0],a[1]), max(a[0], a[1] ) )

                cnt = int(a[2])

                while cnt > 0:
                    print( random.randint( x, y ) )
                    cnt -= 1


    elif first == "frand":

        import random

        random.seed()

        if not a:
            print( random.random() )
        else:
            if len(a) == 1:

                cnt = int(a[0])

                while cnt > 0:
                    print( (random.random()) )
                    cnt -= 1

            elif len(a) == 2:

                x,y = ( min(a[0],a[1]), max(a[0], a[1] ) )

                print( random.uniform(x, y) )


            elif len(a) >= 3:

                x,y = ( min(a[0],a[1]), max(a[0], a[1] ) )

                cnt = int(a[2])

                while cnt > 0:
                    print( random.uniform( x, y ) )
                    cnt -= 1


    elif first == "sqrt":
        r = []

        for n in a:
            x = sqrt(n)
            r.append(x)

        for x in r:
            print(x, end=' ')


# file is a multi arg command
    elif first == "file":
        if a[0] == "read":
            lines = []
            allines = []
            for f in a[1:]:
                if os.path.isfile(f):
                    try:
                        input = open(f, 'r')
                        lines = input.readlines()
                        allines.append(lines)
                        input.close()
                    except IOError as e:
                        print( "I/O error({0}): {1}".format(e.errno, e.strerror) )

                    for line in lines:
                        print(line, end='')

        elif a[0] == "write":
            f=  a[1]
            str = ' '.join(a[2:])
            str += '\n'
            if os.path.isfile(f):
                try:
                    output = open(f, 'w')
                    output.write(str)
                    output.close()
                except IOError as e:
                    print ("I/O error({0}): {1}".format(e.errno, e.strerror))

        elif a[0] == "append":
            f=  a[1]
            str = ' '.join( a[2:] )
            str+= '\n'

            if os.path.isfile(f):
                try:
                    output = open(f, 'a+')
                    output.write(str)
                    output.close()

                except IOError as e:
                    output.close()
                    print ("I/O error({0}): {1}".format(e.errno, e.strerror))

        elif a[0] == "prepend":
            infile=  a[1]
            str =  ' '.join(a[2:])
            str += '\n'

            if os.path.isfile(infile):
                try:
                    f = open(infile, "r+")

                    s = f.read();

                    f.seek(0);

                    full = "".join (( str, s, "\n"))

                    f.write(full )

                    f.close()

                except IOError as e:
                    print ("I/O error({0}): {1}".format(e.errno, e.strerror))

        elif a[0] == "run":
            f  = a[1]
            if os.path.isfile(f):
                command = ' '.join(a[1:])
                os.system(command)

    elif first in {"repeat", "runtimes" }:

        n = int(a[0])

        n = min( n, 1000)

        if len(a) == 1:
            eprint( ("usage: nv repeat ", str(n) , " \"command arg1 arg2 ..\" \n") )
            sys.exit(1)

        f  = a[1]

        if len(a) >=2:

            cmd = f.split()

            f = cmd[0]

            args = cmd[1:]


        args = " ".join(args)

#        print(f)
#        print ( repr(args) )
#        print (n)

        if  os.path.isfile(f):

            import subprocess
            try:

                while n > 0 :

                    result =  subprocess.check_call( [ f, args ] , universal_newlines=True, stderr=subprocess.STDOUT, shell=False )

                    n -= 1

            except subprocess.CalledProcessError as cpe:

                eprint( str(cpe) )


        else:

            from subprocess import Popen, PIPE, STDOUT

            try:

                shell_command = [ f,  args ]

                shell_command =  f + " " +  args

                while n > 0 :

                    event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

                    n -= 1

                    output = event.communicate()


                    print( output[0].decode('ascii') )
#                print("output " , repr(output) )

            except subprocess.CalledProcessError as cpe:
                eprint(  str(cpe) )

    # else:
    #     for f in a[1:]:
    #         if os.path.isfile(f):
    #             print( f , end=' ')






    #elif PUT YOUR KEYWORD HERE



    ######################################################

    else: # default no command -- use expression see below


        if not first:
            cmd = " ".join(sys.argv[1:])
        else:
            cmd = first

    if cmd:
        try:
            res  =  n_eval(cmd)

            if isinstance( res, bool ):  # actual boolean type
                print(repr(res))
            elif res:                    # not None
                printf("%s\n" , res)

        except SyntaxError:
            sys.stderr.write("nv: syntax error: " + cmd )

    if not ispipe:
        print()

else:
    pass



# "int( sin( sqrt(1/2))**2 + cos(sqrt(1/2))**2 )"

# Mathematical functions

# Trigonometric functions
# sin(x, /[, out, where, casting, order, ...])		        Trigonometric sine, element-wise.
# cos(x, /[, out, where, casting, order, ...])		        Cosine element-wise.
# tan(x, /[, out, where, casting, order, ...])		        Compute tangent element-wise.
# arcsin(x, /[, out, where, casting, order, ...])		Inverse sine, element-wise.
# arccos(x, /[, out, where, casting, order, ...])		Trigonometric inverse cosine, element-wise.
# arctan(x, /[, out, where, casting, order, ...])		Trigonometric inverse tangent, element-wise.
# hypot(x1, x2, /[, out, where, casting, ...])                  Given the "legs" of a right triangle, return its hypotenuse.
# arctan2(x1, x2, /[, out, where, casting, ...])		Element-wise arc tangent of x1/x2 choosing the quadrant correctly.
# degrees(x, /[, out, where, casting, order, ...])		Convert angles from radians to degrees.
# radians(x, /[, out, where, casting, order, ...])		Convert angles from degrees to radians.
# unwrap(p[, discont, axis])                                    Unwrap by changing deltas between values to 2*pi complement.
# deg2rad(x, /[, out, where, casting, order, ...])		Convert angles from degrees to radians.
# rad2deg(x, /[, out, where, casting, order, ...])		Convert angles from radians to degrees.

# Hyperbolic functions
# sinh(x, /[, out, where, casting, order, ...])		        Hyperbolic sine, element-wise.
# cosh(x, /[, out, where, casting, order, ...])		        Hyperbolic cosine, element-wise.
# tanh(x, /[, out, where, casting, order, ...])		        Compute hyperbolic tangent element-wise.
# arcsinh(x, /[, out, where, casting, order, ...])		Inverse hyperbolic sine element-wise.
# arccosh(x, /[, out, where, casting, order, ...])		Inverse hyperbolic cosine, element-wise.
# arctanh(x, /[, out, where, casting, order, ...])		Inverse hyperbolic tangent element-wise.

# Rounding
# around(a[, decimals, out])                                    Evenly round to the given number of decimals.
# round_(a[, decimals, out])                                    Round an array to the given number of decimals.
# rint(x, /[, out, where, casting, order, ...])                 Round elements of the array to the nearest integer.
# fix(x[, out])                                                 Round to nearest integer towards zero.
# floor(x, /[, out, where, casting, order, ...])		Return the floor of the input, element-wise.
# ceil(x, /[, out, where, casting, order, ...])  		Return the ceiling of the input, element-wise.
# trunc(x, /[, out, where, casting, order, ...])		Return the truncated value of the input, element-wise.

# Sums, products, differences
# prod(a[, axis, dtype, out, keepdims])		  	        Return the product of array elements over a given axis.
# sum(a[, axis, dtype, out, keepdims])				Sum of array elements over a given axis.
# nanprod(a[, axis, dtype, out, keepdims])			Return the product of array elements over a given axis treating Not a Numbers (NaNs) as ones.
# nansum(a[, axis, dtype, out, keepdims])			Return the sum of array elements over a given axis treating Not a Numbers (NaNs) as zero.
# cumprod(a[, axis, dtype, out])				Return the cumulative product of elements along a given axis.
# cumsum(a[, axis, dtype, out])				        Return the cumulative sum of the elements along a given axis.
# nancumprod(a[, axis, dtype, out])				Return the cumulative product of array elements over a given axis treating Not a Numbers (NaNs) as one.
# nancumsum(a[, axis, dtype, out])				Return the cumulative sum of array elements over a given axis treating Not a Numbers (NaNs) as zero.
# diff(a[, n, axis])                                            Calculate the n-th discrete difference along given axis.
# ediff1d(ary[, to_end, to_begin])				The differences between consecutive elements of an array.
# gradient(f, *varargs, **kwargs)				Return the gradient of an N-dimensional array.
# cross(a, b[, axisa, axisb, axisc, axis])			Return the cross product of two (arrays of) vectors.
# trapz(y[, x, dx, axis])       				Integrate along the given axis using the composite trapezoidal rule.

# Exponents and logarithms
# exp(x, /[, out, where, casting, order, ...])			Calculate the exponential of all elements in the input array.
# expm1(x, /[, out, where, casting, order, ...])		Calculate exp(x) - 1 for all elements in the array.
# exp2(x, /[, out, where, casting, order, ...])			Calculate 2**p for all p in the input array.
# log(x, /[, out, where, casting, order, ...])			Natural logarithm, element-wise.
# log10(x, /[, out, where, casting, order, ...])		Return the base 10 logarithm of the input array, element-wise.
# log2(x, /[, out, where, casting, order, ...])			Base-2 logarithm of x.
# log1p(x, /[, out, where, casting, order, ...])		Return the natural logarithm of one plus the input array, element-wise.
# logaddexp(x1, x2, /[, out, where, casting, ...])		Logarithm of the sum of exponentiations of the inputs.
# logaddexp2(x1, x2, /[, out, where, casting, ...])		Logarithm of the sum of exponentiations of the inputs in base-2.

# Other special functions
# i0(x)								Modified Bessel function of the first kind, order 0.
# sinc(x)							Return the sinc function.

# Floating point routines
# signbit(x, /[, out, where, casting, order, ...])		Returns element-wise True where signbit is set (less than zero).
# copysign(x1, x2, /[, out, where, casting, ...])		Change the sign of x1 to that of x2, element-wise.
# frexp(x[, out1, out2], / [[, out, where, ...])		Decompose the elements of x into mantissa and twos exponent.
# ldexp(x1, x2, /[, out, where, casting, ...])			Returns x1 * 2**x2, element-wise.
# nextafter(x1, x2, /[, out, where, casting, ...])		Return the next floating-point value after x1 towards x2, element-wise.
# spacing(x, /[, out, where, casting, order, ...])		Return the distance between x and the nearest adjacent number.

# Arithmetic operations
#       add(x1, x2, /[, out, where, casting, order, ...])	Add arguments element-wise.
#       reciprocal(x, /[, out, where, casting, ...])		Return the reciprocal of the argument, element-wise.
#       negative(x, /[, out, where, casting, order, ...])	Numerical negative, element-wise.
#       multiply(x1, x2, /[, out, where, casting, ...])		Multiply arguments element-wise.
#       divide(x1, x2, /[, out, where, casting, ...])		Divide arguments element-wise.
#       power(x1, x2, /[, out, where, casting, ...])		First array elements raised to powers from second array, element-wise.
#       subtract(x1, x2, /[, out, where, casting, ...])		Subtract arguments, element-wise.
#       true_divide(x1, x2, /[, out, where, ...])		Returns a true division of the inputs, element-wise.
#       floor_divide(x1, x2, /[, out, where, ...])		Return the largest integer smaller or equal to the division of the inputs.
#       float_power(x1, x2, /[, out, where, ...])		First array elements raised to powers from second array, element-wise.
#       fmod(x1, x2, /[, out, where, casting, ...])		Return the element-wise remainder of division.
#       mod(x1, x2, /[, out, where, casting, order, ...])	Return element-wise remainder of division.
#       modf(x[, out1, out2], / [[, out, where, ...])		Return the fractional and integral parts of an array, element-wise.
#            remainder(x1, x2, /[, out, where, casting, ...])	Return element-wise remainder of division.
#            divmod(x1, x2[, out1, out2], / [[, out, ...])	Return element-wise quotient and remainder simultaneously.

# Handling complex numbers
# angle(z[, deg])						Return the angle of the complex argument.
# real(val)                                                     Return the real part of the complex argument.
# imag(val)							Return the imaginary part of the complex argument.
# conj(x, /[, out, where, casting, order, ...])			Return the complex conjugate, element-wise.

# Miscellaneous
#  convolve(a, v[, mode])Returns the discrete, linear convolution of two one-dimensional sequences.
#  clip(a, a_min, a_max[, out])Clip (limit) the values in an array.
#  sqrt(x, /[, out, where, casting, order, ...])		Return the positive square-root of an array, element-wise.
#  cbrt(x, /[, out, where, casting, order, ...])		Return the cube-root of an array, element-wise.
#  square(x, /[, out, where, casting, order, ...])		Return the element-wise square of the input.
#  absolute(x, /[, out, where, casting, order, ...])		Calculate the absolute value element-wise.
#  fabs(x, /[, out, where, casting, order, ...])		Compute the absolute values element-wise.
#  sign(x, /[, out, where, casting, order, ...])		Returns an element-wise indication of the sign of a number.
#  heaviside(x1, x2, /[, out, where, casting, ...])		Compute the Heaviside step function.
#  maximum(x1, x2, /[, out, where, casting, ...])		Element-wise maximum of array elements.
#  minimum(x1, x2, /[, out, where, casting, ...])		Element-wise minimum of array elements.
#  fmax(x1, x2, /[, out, where, casting, ...])                  Elemennt-wise maximum of array elements.
#  fmin(x1, x2, /[, out, where, casting, ...])                  Element-wise minimum of array elements.
#  nan_to_num(x[, copy]) n                                      Replace nan with zero and inf with finite numbers.
#  real_if_close(a[, tol])					If complex input returns a real array if complex parts are close to zero.
#  interp(x, xp, fp[, left, right, period])			One-dimensional linear interpolation.
#

# The most commonly used maths functions are:

# cos, sin, tan - the trigonometric functions.
# acos, asin, atan - the inverse trigonometric functions.
# cosh, sinh, tanh - the hyperbolic functions.
# exp - the exponential function (for example, exp(10) has value e10).
# log, log10 - the logarithmic functions to base e and base 10 respectively.
# pow - raise to a power (so pow(a,b) is ab).
# sqrt - square root.
# ceil, floor - round a number up or down (for example, ceil(2.4) = 3 and floor(9.8) = 9).
# fabs - compute the absolute value (for example, fabs(-3.4) = 3.4).

# Local Variables:
# mode: python
# End:



