#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU Lesser General Public License, version 3.
# See the file http://www.gnu.org/copyleft/lgpl.txt

# version 0.9 Copyright Nick Demou ndemou@enlogic.gr 2012

'''
Convenience functions for dealing with braille text

Mostly functions to convert between various types of braille represantations:
  Unicode Braille  "⠇⠁⠃"
  Braille ASCII    "LAB"
  Dots notation(s) "p123 p1 p12" or "(123)(1)(12)" etc

Also support for printing pseudo braille like this:
   >>> print_psebr(unibr_2_psebr('⠃⠗⠁⠊⠇⠇⠑'))
   o .  o .  o .  . o  o .  o .  o .
   o .  o o  . .  o .  o .  o .  . o
   . .  o .  . .  . .  o .  o .  . .

IMPORTANT SHORTHANDS USED IN THIS MODULE
========================================
ascbr = Braille ASCII   -- e.g. " LAB" (North American/ΜΙΤ Braille ASCII Code)
unibr = Unicode Braille -- e.g. "⠀⠇⠁⠃"
dotbr = dots Braille    -- e.g. "p0p123p1p12", or "(0)(1,2,3)(1)(1,2)" or "0,123,1,12"*
psebr = pseudo Braille**-- e.g.:
       . .  o .  o .  o .
       . .  o .  . .  o .
       . .  o .  . .  . .    
*: this code also supports many other dots-braille schemes that you may come up 
by compining a prefix, a delimiter and a suffix (all of them optional)
e.g. this fancy dot-style: "<1-2-3>" has prefix='<', delimiter='-' and suffix='>' 

**: see notes about pseudo braille representation in class PsudoBraille

UNDERSTANDING THE CODE
======================
To understand the code you'll often need the following graphic as a reference:

The 8 dot's of a braille cell
-----------------------------

To the left of the dot its numerical order (1,2,3...8 )
Inside the dot its hex value (1,2,4,8,0x10,...,0x80)
        __      __
     1 / 1\  4 / 8\
       \__/    \__/
       
        __      __
     2 / 2\  5 /10\
       \__/    \__/
       
        __      __
     3 / 4\  6 /20\
       \__/    \__/
       
        __      __
     7 /40\  8 /80\
       \__/    \__/

Example:
Take the character with unibr ⠕
  Its dotbr is p135 (the numbers at the left of the dots)
  Its unicode position is 0x2800+1+4+0x10 (add the numbers inside plus 0x2800)

'''

ON_CONV_ERR_RAISE = 1
ON_CONV_ERR_PASS = 2
ON_CONV_ERR_REPLACE = 3

# overide them if you want:
on_conv_err = ON_CONV_ERR_PASS # see above for allowed valuesy
on_conv_err_replace_char = '?'

# unibr to ascbr translation (based on wikipedia and BrailleUtils)
_BrailleAscii__ascii =    " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
_BrailleAscii__unicode = u"⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿"

########################################################################
class PseudoBraille(str):
    """Just a unicode braille string with the __str__ method
overided in order to print it as a pseudo-braille ascii text
(it also has the print_8dot_brl property)

Use it like this:
   >>> pb = PseudoBraille(u'⠕⠓'.encode('utf-8')) #<----note the encoding
   >>> pb.print_8dot_brl = False
   >>> print pb
   o .  o .
   . o  o o
   o .  . .
"""
    print_8dot_brl = True # set it to false to print 6dot pseudo braille
    def __str__(self):
        line=['','','','']
        for c in self.decode('utf-8'):
            o = ord(c)-0x2800 
            if o>=0 and o<=0xff:
                line[0] += ('o' if (o & 0x01)<>0 else '.') + ' ' + ('o' if (o & 0x08)<>0 else '.') + '  '
                line[1] += ('o' if (o & 0x02)<>0 else '.') + ' ' + ('o' if (o & 0x10)<>0 else '.') + '  '
                line[2] += ('o' if (o & 0x04)<>0 else '.') + ' ' + ('o' if (o & 0x20)<>0 else '.') + '  '
                line[3] += ('o' if (o & 0x40)<>0 else '.') + ' ' + ('o' if (o & 0x80)<>0 else '.') + '  '
            else:
                if on_conv_err == ON_CONV_ERR_RAISE:
                    raise ValueError,'Non unicode braille PseudoBraille string %s' % self
                else:
                    line[0] += 'INV  '
                    line[1] += 'ALI  '
                    line[2] += 'D!!  '
                    line[3] += 'CHR  '
        line[0] = line[0][:-2] # strip the last two spaces
        line[1] = line[1][:-2]
        line[2] = line[2][:-2]
        line[3] = line[3][:-2]
        if self.print_8dot_brl: 
            return '%s\n%s\n%s\n%s\n' % (line[0],line[1],line[2],line[3])
        else:
            return '%s\n%s\n%s\n' % (line[0],line[1],line[2])
    
    
########################################################################

def test_braille_ascii():
    '''unit testing -- some sanity tests'''
    for i in range(0,64):
        asc = _BrailleAscii__ascii[i]
        uni = _BrailleAscii__unicode[i]
        assert unibr_2_ascbr(uni) == asc
        assert ascbr_2_unibr(asc) == uni
        
def unibr_2_ascbr(unibr, liberal_input = True):
    '''convert unibr(⠗) to ascbr(R)

liberal_input True means
a) treat lower case letters as upper case
b) pass invalid chars to output untranslated'''
    if len(unibr)<>1:
        return ''.join([unibr_2_ascbr(e) for e in unibr])
    try:
        out = _BrailleAscii__ascii[ord(unibr)-0x2800]
    except:
        if on_conv_err == ON_CONV_ERR_RAISE:
            raise ValueError,'unibr_2_ascbr failed to convert %s' % unibr
        elif on_conv_err == ON_CONV_ERR_PASS:
            out = unibr
        else: 
            out = on_conv_err_replace_char
    return out

def unibr_2_dotbr(unibr, prefix = 'p', delimiter = '', suffix = ''):
    '''convert unibr(⠗) to dotbr (eg p1235)
    
    Setting prefix to '(' delimiter to ',' and suffix to ')' will return another
    style of dotbr: "(1,2,3,5)". You can customize them as you wish.
    '''
    if len(unibr)<>1:
        return ''.join([unibr_2_dotbr(e) for e in unibr])

    o = ord(unibr)-0x2800     
    if o>=0 and o<=0xff:
        dots = prefix
        if (o & 0x01)<>0: dots += '1' + delimiter
        if (o & 0x02)<>0: dots += '2' + delimiter
        if (o & 0x04)<>0: dots += '3' + delimiter
        if (o & 0x08)<>0: dots += '4' + delimiter
        if (o & 0x10)<>0: dots += '5' + delimiter
        if (o & 0x20)<>0: dots += '6' + delimiter
        if (o & 0x40)<>0: dots += '7' + delimiter
        if (o & 0x80)<>0: dots += '8' + delimiter
        if dots == prefix: dots = prefix + '0'
        dots = dots.rstrip(delimiter) + suffix
    else:
        if on_conv_err == ON_CONV_ERR_RAISE:
            raise ValueError,'unibr_2_dotbr got non unicode braille char %s' % unibr
        elif on_conv_err == ON_CONV_ERR_PASS:
            dots = unibr
        else: 
            dots = on_conv_err_replace_char
    return dots
    
def unibr_2_psebr(unibr):
    '''convert unibr(⠗) to list of psebr's '''
    return PseudoBraille(unibr.encode('utf-8'))
        
def ascbr_2_dotbr(ascbr):
    return unibr_2_dotbr(ascbr_2_unibr(ascbr))
    
def ascbr_2_psebr(ascbr):
    return unibr_2_psebr(ascbr_2_unibr(ascbr))

def ascbr_2_unibr(ascbr, liberal_input = True):
    '''convert ascbr(R) to unibr(⠗)'''
    if len(ascbr)<>1:
        return ''.join([ascbr_2_unibr(e) for e in ascbr])
    try:
        out = unichr(0x2800 + _BrailleAscii__ascii.index(ascbr))
    except:
        if on_conv_err == ON_CONV_ERR_RAISE:
            raise ValueError,'ascbr_2_unibr failed to convert %s' % ascbr
        elif on_conv_err == ON_CONV_ERR_PASS:
            out = ascbr
        else: 
            out = on_conv_err_replace_char
    return out

def dotbr_2_ascbr(dotbr, cell_delimiter='p', valid_chars='012345678,p() '):
    return unibr_2_ascbr(dotbr_2_unibr(dotbr, cell_delimiter='p', valid_chars='012345678,p() '))

def dotbr_2_psebr(dotbr, cell_delimiter='p', valid_chars='012345678,p() '):
    return unibr_2_psebr(dotbr_2_unibr(dotbr, cell_delimiter='p', valid_chars='012345678,p() '))

def dotbr_2_unibr(dotbr, cell_delimiter='p', valid_chars='012345678,p() '):
    '''convert dotbr(eg p1235) to unibr (⠗)
    
    If dotbr contains a single cell then you can ignore the cell_delimiter
    If dotbr contains two or more cells you MUST specify the cell_delimiter:
       cell delimiter will be 'p' for dotbr like 'p123p1'
       cell delimiter will be ',' for dotbr like '123,1' 
       cell delimiter will be either '(' or ')' for dotbr like '(123)(1)' or '(1,2,3)(1)'
    
    Every characters of dotbr must be within valid_chars
    
    Note that the code for this function is quite liberal in what it accepts
    E.g. passing "3120" will return the same output as passing "p123"
    '''
    dotbr=dotbr.strip()
    if dotbr=='': return ''
    if cell_delimiter in dotbr:
        if len(dotbr.split(cell_delimiter))>2:
            return ''.join([dotbr_2_unibr(e) for e in dotbr.split(cell_delimiter) if e<>''])

    for c in dotbr:
        if not c in valid_chars:
            if on_conv_err == ON_CONV_ERR_RAISE:
                raise ValueError,'dotbr_2_unibr found invalid char %s' % c
            elif on_conv_err == ON_CONV_ERR_PASS:
                return dotbr
            else: 
                return on_conv_err_replace_char
        
    o = 0
    if ('1' in dotbr): o +=  0x01
    if ('2' in dotbr): o +=  0x02
    if ('3' in dotbr): o +=  0x04
    if ('4' in dotbr): o +=  0x08
    if ('5' in dotbr): o +=  0x10
    if ('6' in dotbr): o +=  0x20
    if ('7' in dotbr): o +=  0x40
    if ('8' in dotbr): o +=  0x80
    return unichr( 0x2800 + o )

def strip_dots78(unibr):
    '''strips dots 7,8 from all cells of unibr'''
    if len(unibr)<>1:
        return ''.join([strip_dots78(e) for e in unibr])
    return unichr(ord(unibr) & 0x283f)

def is_six_dot(unibr):
    '''returns True if there are no dots 7/8 in input'''
    if len(unibr)<>1:
        return min([is_six_dot(e) for e in unibr])
    return ((ord(unibr) & 0xC0) == 0)

if __name__ == "__main__":
    test_braille_ascii()
    
    for o in range(0,256):
        unibr = unichr(0x2800 + o)
        #print o, hex(0x2800 + o), unichr(0x28ff)+ unibr, unibr_2_dotbr(unibr), dotbr_2_unibr(unibr_2_dotbr(unibr))
        print u"%c%s %s %s" % (0x28ff,unibr, unibr_2_dotbr(unibr, '(',',',')'), is_six_dot(unibr))
        print unibr_2_psebr(unibr)
        print 
        assert dotbr_2_unibr(unibr_2_dotbr(unibr)) == unibr
    
    for o in range(0,256):
        if o % 8 == 0: print 
        unibr = unichr(0x2800 + o)
        print '%9s=%s' % (unibr_2_dotbr(unibr), unibr),
    print
        
    ascbr_table = '''
ABCDEFGHIJ
KLMNOPQRST
UVXYZ&=(!)
*<%?:$]\[W
1234567890
/+#>'-
@^_".;, 
'''
    for line in [i for i in ascbr_table.split('\n') if i.strip()<>'']:
        for ascbr in line:
            print '%s%s ' % (ascbr, ascbr_2_unibr(ascbr)),
        print
    
    for line in [i for i in ascbr_table.split('\n') if i.strip()<>'']:
        print unibr_2_psebr(ascbr_2_unibr(line))
        print
     
    pass        

    ascbr = 'ABCDEFGHIJ'
    unibr = ascbr_2_unibr(ascbr)
    dotbr = unibr_2_dotbr(unibr)
    print ascbr 
    print unibr
    print dotbr
    print dotbr_2_unibr(dotbr)
    assert dotbr_2_unibr(dotbr) == unibr
    pb8 = unibr_2_psebr(unibr)
    pb6 = unibr_2_psebr(unibr)
    pb6.print_8dot_brl = False
    print 'printing 8dots psudo braille'
    print pb8
    print 'printing 6dots psudo braille'
    print pb6
    print u'⠙⠬⠛', '6dot braille' if is_six_dot(u'⠙⠬⠛') else '8dot braille'
    print u'⠙⠬⢹', '6dot braille' if is_six_dot(u'⠙⠬⢹') else '8dot braille'
    print strip_dots78(u'⠙⠬⢹'), '6dot braille' if is_six_dot(strip_dots78(u'⠙⠬⢹')) else '8dot braille'
