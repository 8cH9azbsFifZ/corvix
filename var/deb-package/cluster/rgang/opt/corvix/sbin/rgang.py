#!/usr/bin/env python
#   This file (rgang.py) was created by Ron Rechenmacher <ron@fnal.gov> on
#   Apr 13, 2001. "TERMS AND CONDITIONS" governing this file are in the README
#   or COPYING file. If you do not have such a file, one can be obtained by
#   contacting Ron or Fermi Lab in Batavia IL, 60510, phone: 630-840-3000.
#   $RCSfile: rgang.py,v $ $Revision: 1.112 $ $Date: 2005/05/04 17:25:34 $

import os.path                          # basename
import sys                              # argv
import re                               # findall
import string                           # split
import time                             # time

DFLT_RSH='rsh'
DFLT_RCP='rcp'
DFLT_RSHTO='150.0'                      # float seconds  (basically, let the user decide)
DFLT_RCPTO='3600.0'                     # float seconds (big files?) (basically, let the user decide)

VERSION='2.7 cvs: $Revision: 1.112 $$Date: 2005/05/04 17:25:34 $'
APP = os.path.basename( sys.argv[0] )
USAGE=\
"%s: run cmds on hosts\n"%(APP,)+\
"Usage: %s [options] <nodespec> [cmd]\n"%(APP,)+\
"       %s [options] -<c|C> <nodespec> 'srcfile' 'dstdfile'\n"%(APP,)+\
"       %s [--skip <nodespec>] --list [<nodespec>]\n"%(APP,)+\
"       %s -d\n"%(APP,)+\
"  nodespec can be a \"farmlet\", \"expandable node list\", or \"-\".\n"+\
"  when nodespec is \"-\", nodes are read from stdin (1 per line)\n"+\
"  until a line containing a single \".\" is encountered\n"+\
"  The nodespec is evaluated in the following order:\n"+\
"      is it the stdin (\"-\")\n"+\
"      it it a file in \"farmlets\" directory\n"+\
"      it it a file in current working directory\n"+\
"      assume \"expandable node list\"\n"+\
"Examples: %s -c root@qcd01{01-4} .profile .\n"%(APP,)+\
"          %s all ls\n"%(APP,)+\
"          %s all \"echo 'hi  there'\"\n"%(APP,)+\
"          %s qcd01{01-4} '%s qcd01{01-4} \"echo hi\"'\n"%(APP,APP)+\
"          %s -l root qcd0{1-2}{04-10} \"echo 'hi  there'\"\n"%(APP,)+\
"          %s --skip node0{b-d} --list \"node{04-0x44,4f-0x55}\"\n"%(APP,)+\
" to test a large # of nodes:\n"+\
"          %s 'qcd{,,,}{01-8}{01-10}' echo hi\n"%(APP,)+\
"Note: when using node expansion, don't forget to quote the expression to\n"+\
"      stop shell expansion (as bash would do with the \"{,}\" syntax in\n"+\
"      above example)"
# For the following, the definitions are:
#       'desc'   Short description; printed out along with "USAGE"
#       'init'   The initialized value, i.e. when option is not specified;
#                usually string, but can be other if accompanied by specific
#                processing (default='')
#       'alias'  a list of aliases (i.e. short form?)
#       'arg'    the type of option argument:
#                an integer 
#                  0 => option does not take an argument (default)
#                  1 => option does take an argument
#                  2 => option takes an optional argument where if it is
#                       multiple leter (long [--] form) option there must
#                       be an '=<value>', else if it is a single letter,
#                       the arg will follow 
#       'opt'    for optional argument type options (arg=2), the
#                value of the option when specified without an argument
OPTSPEC={ 'd':{'desc':"List farmlet names"},
          's':{'desc':"Skip current (local) node"},
          'c':{'desc':"Copy input output"},
          'C':{'desc':"Copy and skip current (local) node. Equiv to -sc"},
          'p':{'desc':"Same as rcp -p (only applicable if -c/C)"},
          'l':{'desc':"Same as rsh -l (only applicable if not -c/C)",'arg':1},
          'x':{'desc':"Same as rsh/rcp -x (turns on encryption)"},
          'X':{'desc':"Same as rsh/rcp -X (turns off encryption)"},
          'f':{'desc':"Same as rsh -f (cause  nonforwardable credentials to be forwarded)"},
          'F':{'desc':"Same as rsh/rcp -F (cause  forwardable credentials to be forwarded)"},
          'N':{'desc':"Same as rsh/rcp -N (prevent credentials from being forwarded)"},
          'n':{'desc':"-n or -n0: no header, -n1 or -nn: node=, -n2: ---, -n3: --- and cmd",
               'arg':2,'init':'','opt':'0'},
          'list'    :{'desc':"list farmlets (there contents)"},
          'farmlets':{'desc':"override farmlets dir /opt/corvix/etc/rgang",
                      'arg':1,'init':'/opt/corvix/etc/rgang'},
          'serial'  :{'desc':"do not fork all commands before reading output"},
          'skip'    :{'desc':'skip this specific list of nodes','arg':1},
          'rsh'     :{'desc':'override default rsh','arg':1,'init':DFLT_RSH},
          'rcp'     :{'desc':'override default rcp','arg':1,'init':DFLT_RCP},
          'nway'    :{'desc':'number of branches for each node of the tree OR if --serial, # of groups (def=200)',
                      'arg':1,'init':200},
          'combine' :{'desc':"spawn commands with stderr dupped onto stdout"},
          'do-local':{'desc':"do 1st node in current (local) environment; do not rsh"},
          'tlvlmsk' :{'desc':"debugging; set hex debug mask i.e. 0xf, \"1<<9\"",'arg':2,'opt':1,'init':'0'},
          'pty'     :{'desc':"use pseudo term -- good for when ssh wants passwd"},
          'rshto'   :{'desc':"change the default timeout value %s (float seconds) for non-copy"%DFLT_RSHTO,
                      'arg':1,'init':DFLT_RSHTO},
          'rcpto'   :{'desc':"change the default timeout value %s (float seconds) for the copy"%DFLT_RCPTO,
                      'arg':1,'init':DFLT_RCPTO},
          'err-file':{'desc':"file to write timedout/error nodes to (could be used for retry)",
                      'arg':1},
          'verbose' :{'desc':"verbose",'alias':['v']},
          'pyret'   :{'desc':"don't output to stdout/err (used when rgang is imported in other .py scripts)"},
          'pyprint' :{'desc':"implies pyret but *final* result is printed"},
          'pypickle':{'desc':"implies pyret but *final* result is pickled and printed (preceeded by 8 length characters)"},
          'path'    :{'desc':"prepend to path when rsh rgang",'arg':1,'init':os.path.abspath(os.path.dirname(sys.argv[0]))},
          'app'     :{'desc':"change application name from default \"%s\" (use when call from script)"%(APP,),'arg':1,'init':APP},
          'input-to-all-branches' :{'desc':"send input to all branches, not just currently processed"},
          'adjust-copy-args':{'desc':"internal - applicable for \"-c\" (copy-mode)"},
          'mach_idx_offset' :{'desc':"internal - used to determine \"root\" machine",'arg':1},
          }


def getopts( optspec, argv, usage_in, app, version='' ):
    import os                           # environ
    import string                       # replace, split
    import sys                          # exit
    import re                           # sub
    optspec.update( {'help'   :{'alias':['h','?'],'desc':'print usage/help'}} )
    optspec.update( {'version':{'alias':['V'],'desc':'print cvs version/date'}} )
    opt_map={}                          # handles aliases
    opt={}                              # local master options dictionary
    long_opts = []; env_opts = []
    for op in optspec.keys():
        default = {'desc':'', 'init':'', 'alias':[], 'arg':0, 'opt':''}
        default.update( optspec[op] ); optspec[op].update( default )
        opt_map[op] = op; dashes='-'
        if len(op) > 1: long_opts.append(op); dashes='--'
        for alias in optspec[op]['alias']:
            opt_map[alias] = op
            if len(alias) > 1: long_opts.append(alias)
        env=string.upper(re.sub('[.-]','_',app)+'_'+string.replace(op,'-','_'))
        if env in os.environ.keys():
            if optspec[op]['arg']:
                  ee=os.environ[env]
                  opt[op]=ee;  env_opts.append(dashes+op+'='+ee)
            else: opt[op]='1'; env_opts.append(dashes+op)
        else:     opt[op]=optspec[op]['init']
    usage_out = usage_in+"\n\
Note: all options can be specified via environment variables of the form\n\
      %s_<OPTION> where option is all uppercase\n\
Options:\n"%(string.upper(re.sub('[.-]','_',app)),)
    xx=optspec.keys(); xx.sort()
    for op in xx:
        dash=''
        for op_ in [op]+optspec[op]['alias']:
            if len(op_) == 1: dash=dash+',-'+op_
            else:             dash=dash+',--'+op_
            if len(op_) == 1 and optspec[op]['arg'] == 1: dash=dash+'<val>'
            elif                 optspec[op]['arg'] == 1: dash=dash+'<=val>' 
            if len(op_) == 1 and optspec[op]['arg'] == 2: dash=dash+'[val]'
            elif                 optspec[op]['arg'] == 2: dash=dash+'[=val]' 
        usage_out = usage_out + '  %-20s %s\n'%(dash[1:],optspec[op]['desc'])
    long_space_separated = ' '+string.join(long_opts)
    opts=[] # to remember all args passwd
    while argv and argv[0][0] == '-' and len(argv[0]) > 1:
        op = argv[0][1:]; opts.append(argv.pop(0))      # save all opts
        long_flg = 0    # SHORT FORM is default
        if op[0] == '-':
            long_flg = 1    # LONG FORM
            op = op[1:]
            # check for '=' and prepare possible op_arg. (adding the '=' is a
            op,op_arg = string.split( op+'=', '=', 1 ) #trick, it gets removed)
            op_grp = [op]
        else: op_grp = map( lambda x:x, op )  # convert string to list
        while op_grp:
            op_ = op_grp.pop(0)
            if long_flg and not op_ in long_opts:
                possibles = re.findall(" "+op_+"[^ ]*",long_space_separated)
                if   len(possibles) == 1: op_ = possibles[0][1:]
                elif len(possibles) > 1:
                    pp = string.join(possibles,'')
                    sys.stderr.write('ambiguous "long" option: %s\ncould be:%s\n'%(op_,pp))
                    sys.exit(1)
                else: sys.stderr.write('%s: unknown "long" option: %s\n'%(APP,op_)); sys.exit(1)
            elif not long_flg and not op_ in opt_map.keys():#OK, no short list.
                sys.stderr.write('unknown option: %s\n'%(op_,)); sys.exit(1)
            op_ = opt_map[op_] # unalias
            if   optspec[op_]['arg'] == 0: ### NO OPTION ARG
                if long_flg and op_arg:
                    sys.stderr.write('option %s does not take an argument\n'%(op_,))
                    sys.exit(1)
                opt[op_] = '1'
            elif optspec[op_]['arg'] == 1: ### OPTION ARG
                if long_flg and op_arg:
                    opt[op_] = op_arg[:-1] # strip off added '='
                elif not long_flg and op_grp:
                    opt[op_] = string.join(op_grp,''); op_grp = []
                elif not argv:
                    sys.stderr.write('option %s requires and argument\n'%(op_,)); sys.exit(1)
                else: opt[op_]=argv[0]; opts.append(argv.pop(0))# save all opts
            elif long_flg and op_arg:            ### OPTIONAL OPTION ARG
                opt[op_] = op_arg[:-1] # strip off added '='
            elif not long_flg and op_grp:
                opt[op_] = string.join(op_grp,''); op_grp = []
            else: opt[op_] = optspec[op_]['opt']
    if opt['version']:
        if version == '':
            try: version = VERSION  # incase VERSION is not set (this is generic code) -
            except: pass            # version will just remain ''
        print 'version:',version; sys.exit( 0 )
    if opt['help']: print usage_out; sys.exit( 0 )
    return env_opts+opts,argv,opt,usage_out
    #getopts


# this needs g_opt['tlvlmsk']
def TRACE( lvl, fmt_s, *args ):
    import socket
    # how is g_opt working w/o "global" declaration? - must default if read
    fd = sys.stderr.fileno() # default
    if g_opt['tlvlmsk'] & (1<<lvl): # and g_opt['mach_idx_offset']=='':
        fo = open( "%s.%s.trc"%(g_thisnode.hostnames_l[0],os.getpid()), "a+" )
        fd = fo.fileno()
        os.write( fd, '%.2f:%s:%s:%d:%s\n'%(time.time(),socket.gethostname(),g_thisnode.mach_idx,lvl,fmt_s%args) )
        fo.close()
    # TRACE

###############################################################################
# General Regular Expression class that allows for:
#    xx = Re( re )
#    ...
#    if xx.search( line ):
#        yy = xx.match_obj.group( x )
#

class Re:
    import re
    def __init__( self, reg_ex=None,flags=0 ):
        if reg_ex: self.compiled = self.re.compile(reg_ex,flags)
        self.match_obj=None
    def search(self,arg1,string=None):
        if string: self.match_obj = self.re.search(arg1, string)
        else:      self.match_obj = self.compiled.search( arg1 )
        return self.match_obj
    # Re

re_numeric = Re( r"([0-9a-f]+)-((0x{0,1}){0,1}[0-9a-f]+)" )     # the "r" prefix --> use Python's raw string notation
re_1alpha  = Re( r"([a-zA-Z])-([a-zA-Z])" )                     # the "r" prefix --> use Python's raw string notation

# the connect str will be the first thing that is *supposed to be* printed out.
CONNECT_MAGIC = "__rg_connect__"
re_connect  = Re( r"(.*)%s"%(CONNECT_MAGIC,) ) # the "r" prefix --> use Python's raw string notation

STATUS_MAGIC = "__rg_sts__:"  # Can I manipulate this so it is TRACE-able? --> note ("") appended in spawn_cmd
#re_status = Re( r"(.*)%s([0-9]+)$"%(STATUS_MAGIC,),re.MULTILINE ) # the "r" prefix --> use Python's raw string notation
# I'll assume that with the echo of the STATUS_MAGIC that ends with newline as
# defined in spawn_cmd, the re search does not need to be multiline (actually,
# I recall there may be a problem with MULTILINE
re_status  = Re( r"(.*)%s([0-9]+)"%(STATUS_MAGIC,) ) # the "r" prefix --> use Python's raw string notation

re_pickle = Re( r"PICKLE:([0-9a-f]{8}):" )

re_mach_id = Re( r"(.*[^\\]|^)\$(RGANG_MACH_ID|{RGANG_MACH_ID})([^a-zA-Z_].*|$)" ) # for rcp

re_mach = Re( r"^[^#\S]*([^#\s]+)" )


def findall_expands( ss ):
    result = []; result_idx = 0; brace_lvl = 0
    for cc in ss:
        if   cc == '{':
            brace_lvl = brace_lvl + 1
            if brace_lvl == 1: result.append('')
        if brace_lvl > 0: result[result_idx] = result[result_idx] + cc
        if   cc == '}':
            brace_lvl = brace_lvl - 1
            if brace_lvl == 0: result_idx = result_idx + 1
    if brace_lvl != 0: result.pop()
    return result
    # findall_expands


def numeric_expand( ss_l ):
    ret = []
    for sss in ss_l:
        # single alpha check 1st so {a-f} is not mistaken for
        # integer (not hex) numeric expand
        if re_1alpha.search( sss ):
            start = re_1alpha.match_obj.group(1)
            end   = re_1alpha.match_obj.group(2)
            end   = chr(ord(end)+1)
            while start != end:
                ret.append( start )
                start = chr(ord(start)+1)
        elif re_numeric.search( sss ):
            start = re_numeric.match_obj.group(1)
            end   = re_numeric.match_obj.group(2)
            bb    = re_numeric.match_obj.group(3)
            if   bb == None:
                for num in range(int(start),eval(end)+1):
                    ret.append( '%0*d'%(len(start),num) )
            elif bb == '0':
                for num in range(eval('0%s'%(start,)),eval(end)+1):
                    ret.append( '%0*o'%(len(start),num) )
            elif bb == '0x':
                for num in range(eval('0x%s'%(start,)),eval(end)+1):
                    ret.append( '%0*x'%(len(start),num) )
        else: ret.append( sss )
    TRACE( 17, 'numeric_expand returning %s', ret )
    return ret
    # numeric_expand

def expand( ss ):
    import string
    import re
    TRACE( 18, 'expand(%s)', ss )
    ssIn = ss
    try:
        placeholder_idx = 0
        expands = findall_expands( ss )
        if not expands: return string.split(ss,',')
        exp_result = []
        for exp in expands:
            ss = string.replace( ss, exp, '<%d>'%(placeholder_idx,),1 )
            placeholder_idx = placeholder_idx + 1
        placeholder_idx = 0
        for sss in string.split(ss,','):
            TRACE( 19, 'expand sss=%s of ss=%s', sss, ss )
            place_holders = re.findall( '<[0-9]+>', sss )
            for idx in range(len(place_holders)):
                p_holder = '<%d>'%(placeholder_idx+idx,)
                expanding = expand( expands[placeholder_idx+idx][1:-1] ) #Recursive call
                expanding = numeric_expand( expanding )
                result = []
                for ssss in string.split(sss, ','):
                    holder_idx = string.find(ssss,p_holder)
                    if holder_idx != -1:
                        pre = ssss[:holder_idx]
                        post= ssss[holder_idx+len(p_holder):]
                        for expanded in expanding:
                            result.append( pre+expanded+post )
                sss = string.join(result,',')
            exp_result = exp_result + string.split(sss,',')
            placeholder_idx = placeholder_idx + len(place_holders)
    except:  # any
        exc, value, tb = sys.exc_info()
        sys.stderr.write('Error expanding node list "%s": %s: %s\n'%(ssIn,exc,value) )
        sys.stderr.write('Prehaps an invalid decimal/octal/hex digit\n' )
        sys.stderr.write('remember: in the \'{seq1-seq2}\' syntax, seq2\n' )
        sys.stderr.write('can begin with \'0x\' to force hex or \'0\' to\n' )
        sys.stderr.write('force octal\n' )
        if g_opt['tlvlmsk']:
            for ln in traceback.format_exception( exc, value, tb ):
                sys.stderr.write(ln)
        sys.exit(1)

    return exp_result
    # expand, numeric_expand, findall_expands


def build_quoted_str( args ):
    import string                       # join
    quoted_args=[]
    for arg in args:
        if repr(arg)[0] == "'": quoted_args.append( "'%s'"%(arg,) )
        else:                   quoted_args.append( '"%s"'%(arg,) )
    return string.join( quoted_args )
    # build_quoted_str

def build_sh_single_quoted_str( i_str ):
    o_str = re.sub("'","<<0>>",i_str,0)
    o_str = re.sub("<<0>>",'\'"\'"\'',o_str,0)
    o_str = "'%s'"%(o_str,)
    return (o_str)
    # build_sh_single_quoted_str

def build_sh_doubly_single_quoted_str( i_str ):
    o_str = re.sub("'","<<0>>",i_str,0)
    o_str = re.sub("<<0>>",'\'"\'"\'',o_str,0)
    return (o_str)
    # build_sh_doubly_single_quoted_str

# this routine needs:
# g_opt={'tlvlmsk':0,'pty':''}
g_num_spawns = 0
def spawn( cmd, args, combine_stdout_stderr=0 ):
    import os                           # fork, pipe
    import pty                          # fork
    import string                       # split
    global g_num_spawns                 # keep track for total life of process
    
    g_num_spawns = g_num_spawns + 1
    cmd_list = string.split(cmd)    # support cmd='cmd -opt'

    # for stdin/out/err for new child. Note: (read,write)=os.pipe()
    if g_opt['pty']: pipe0 = [0,0]    ; pipe1 = [1,1];     pipe2 = os.pipe()
    else:            pipe0 = os.pipe(); pipe1 = os.pipe(); pipe2 = os.pipe()
    
    if g_opt['pty']: pid,fd = pty.fork()
    else:            pid    =  os.fork()
    
    if pid == 0:
        #child
        # combining stdout and stderr helps (when simply printing output)
        # get the output in the same order
        if combine_stdout_stderr: os.dup2( pipe1[1], 2 ); os.close( pipe2[1] )#; TRACE( 20, "child close %d", pipe2[1]) # close either way as we
        else:                     os.dup2( pipe2[1], 2 ); os.close( pipe2[1] )#; TRACE( 20, "child close %d", pipe2[1])  # are done with it.
        if g_opt['pty']:
            pass                        # all done for use in pyt.fork() (except our combining above)
        else:
            os.close( pipe0[1] )#; TRACE( 20, "child close %d", pipe0[1] )
            os.close( pipe1[0] )#; TRACE( 20, "child close %d", pipe1[0] )
            os.close( pipe2[0] )#; TRACE( 20, "child close %d", pipe2[0] )
            os.dup2( pipe0[0], 0 ); os.close( pipe0[0] )#; TRACE( 20, "child close %d", pipe0[0] )
            os.dup2( pipe1[1], 1 ); os.close( pipe1[1] )#; TRACE( 20, "child close %d", pipe1[1] )
        for ii in range(3,750):  # if default nway=200, and there are 3 fd's per process...
            try: os.close(ii)#; TRACE( 20, "child successfully closed %d", ii )
            except: pass
                        
        os.execvp( cmd_list[0], cmd_list+args )
        # bye-bye python
        pass
    #parent
    TRACE( 20, 'spawn: pid=%d p0=%s p1=%s p2=%s execvp( %s, %s )', pid, pipe0, pipe1, pipe2, cmd_list[0], cmd_list+args )
    if g_opt['pty']:
        pipe0[1] = fd               # stdin  (fd is read/write and only valid in parent; pty takes care of child stdin )
        pipe1[0] = fd               # stdout (fd is read/write and only valid in parent; pty takes care of child stdout )
        os.close( pipe2[1] )        # parent doesn't need to write to child's stderr (pty does not take care of stderr)
    else:
        os.close( pipe0[0] )        # parent doesn't need to read from child's stdin
        os.close( pipe1[1] )        # parent doesn't need to write to child's stdout
        os.close( pipe2[1] )        # parent doesn't need to write to child's stderr
    child_stdin  = pipe0[1]
    child_stdout = pipe1[0]
    if combine_stdout_stderr: child_stderr = None
    else:                     child_stderr = pipe2[0]
    return pid,child_stdin,child_stdout,child_stderr
    # spawn


# node_info == g_internal_info[x]
def spawn_cmd( node_info, mach_idx, opts, args, branch_nodes, do_local ):
    import os.path                      # basename, isdir
    import os                           # environ
    global g_mach_idx_offset            # declaration necessary because I'm setting it
    global g_connects_expected          # declaration necessary because I'm setting it
    TRACE( 21, 'spawn_cmd args=%s', args )
    if   g_opt['c']:
        # rgang COPY mode
        dest = args[-1]
        # do special $RGANG_MACH_ID processing
        # 3 cases: 1 for \"initiator\" node (adjust-copy-args='')
        #          2 for non-initiator node (adjust-copy-args='1' and '2')
        if g_opt['adjust-copy-args']:
            g_opt['adjust-copy-args'] = ''  # do this once, not for each branch
            sour = args[-1]
            if re_mach_id.search(sour): sour = '%s%d%s'%(re_mach_id.match_obj.group(1),g_mach_idx_offset,re_mach_id.match_obj.group(3))
            for ii in range(len(args[:-1])):
                if os.path.isdir(dest):
                    if sour[-1] == '/': args[ii] = sour+os.path.basename(args[ii])
                    else:               args[ii] = sour+'/'+os.path.basename(args[ii])
                else:
                    # THERE SHOULD BE JUST ONE
                    args[ii] = sour
            g_mach_idx_offset = g_mach_idx_offset + 1 # TRICKY - correct effects dest node processing and rgang --mach_idx_offset
        if re_mach_id.search(dest): dest = '%s%d%s'%(re_mach_id.match_obj.group(1),g_mach_idx_offset+mach_idx,re_mach_id.match_obj.group(3))

        if node_info['stage'] == None:
            # RECALL: rcp is always first; when there are multiple nodes
            # per branch, rgang uses a 2 step process - 1st/always rcp, then
            # 2nd, rsh the rgang (if it were one node, we could just rsh, but
            # for the stake of simplicity, when just use/rely on rgang).
            sp_args = args[:-1]+['%s:%s'%(node_info['ret_info']['name'],dest)]
            if g_opt['p']: sp_args = ['-p']+sp_args
            if g_opt['x']: sp_args = ['-x']+sp_args
            if g_opt['X']: sp_args = ['-X']+sp_args
            if g_opt['F']: sp_args = ['-F']+sp_args
            if g_opt['N']: sp_args = ['-N']+sp_args
            sp_info = spawn( g_opt['rcp'], sp_args, g_opt['combine'] )
            node_info['stage'] = 'rcp'
            timeout_add( node_info['gbl_branch_idx'], float(g_opt['rcpto']) )
        else:
            # assume stage is rgang; it would be stage==rcp (with additional
            # node(s))
            sp_args = []
            if g_opt['l']: sp_args = sp_args + ['-l',g_opt['l']]
            if g_opt['x']: sp_args = sp_args + ['-x']
            if g_opt['X']: sp_args = sp_args + ['-X']
            if g_opt['f']: sp_args = sp_args + ['-f']
            if g_opt['F']: sp_args = sp_args + ['-F']
            if g_opt['N']: sp_args = sp_args + ['-N']
            sp_args = sp_args + [node_info['ret_info']['name']]
            q_user_arg_s     = build_quoted_str( args )
            sp_args = sp_args + ['/bin/sh','-c']
            # HERE'S THE 1ST PLACE WHERE I NEED TO ADD CONNECT_MAGIC
            sh_cmd_s = "'"  # I want only sh to interpret things
            sh_cmd_s = sh_cmd_s+'echo %s;'%(CONNECT_MAGIC,)
            g_connects_expected = g_connects_expected + 1
            sh_cmd_s = sh_cmd_s+'PATH=%s:$PATH;'%(g_opt['path'],)  # see option init
            sh_cmd_s = sh_cmd_s+'RGANG_MACH_ID=%d;export RGANG_MACH_ID;'%(mach_idx+g_mach_idx_offset,)
            sh_cmd_s = sh_cmd_s+'if [ -r $HOME/.rgangrc ];then . $HOME/.rgangrc;fi;' # stdout from .rgangrc should be OK; I search for PICKLE:
            sh_cmd_s = sh_cmd_s+'%s '%(g_opt['app'],)
            sh_cmd_s = sh_cmd_s+'--pypickle --mach_idx_offset=%d --adjust-copy-args '%(g_mach_idx_offset+mach_idx,)
            for rgang_opt in opts:
                if string.find(rgang_opt,'--mach_idx_offset') == 0: continue
                if string.find(rgang_opt,'--pypickle')        == 0: continue
                if string.find(rgang_opt,'--adjust-copy-args')== 0: continue
                # use build_quoted_str to preserve, i.e., --rsh="rsh -F" (which is
                # equiv to "--rsh=rsh -F")
                sh_cmd_s = sh_cmd_s+build_sh_doubly_single_quoted_str(build_quoted_str([rgang_opt]))+' '

            sh_cmd_s = sh_cmd_s+'- %s'%(build_sh_doubly_single_quoted_str(q_user_arg_s),)

            sh_cmd_s = sh_cmd_s+"'"  # end the sh cmd string

            TRACE( 22, 'spawn_cmd rcp rgang sh_cmd_ss=>%s<', sh_cmd_s )

            sp_args = sp_args + [sh_cmd_s]
            sp_info = spawn( g_opt['rsh'], sp_args, 0 )  # never combine stderr/out of rsh rgang
            for machine in branch_nodes:
                os.write( sp_info[1], machine )
                os.write( sp_info[1], '\n' )
            os.write( sp_info[1], '.\n' )
                #sp_info[1].write( machine )
                #sp_info[1].write( '\n' )
            #sp_info[1].write( '.\n' ); sp_info[1].flush()
            node_info['stage'] = 'rgang'
            timeout_add( node_info['gbl_branch_idx'], float(g_opt['rshto']) )
    elif len(branch_nodes) == 1 and do_local and g_thisnode.is_me(branch_nodes[0]): # local, no need to rsh to ourselves
        sh_cmd_s = ''
        sh_cmd_s = sh_cmd_s+'RGANG_MACH_ID=%d;export RGANG_MACH_ID;'%(mach_idx+g_mach_idx_offset,)
        # RGANG_INITIATOR, RGANG_PARENT, and RGANG_PARENT_ID should already be set
        sh_cmd_s = sh_cmd_s+'if [ -r $HOME/.rgangrc ];then . $HOME/.rgangrc;fi;'
        sh_cmd_s = sh_cmd_s+string.join(args)
        TRACE( 22, 'spawn_cmd local sh_cmd_ss=>%s<', sh_cmd_s )
        sp_args = ['-c',sh_cmd_s]
        sp_info = spawn( '/bin/sh', sp_args, g_opt['combine'] )
        node_info['stage'] = 'local'
    elif len(branch_nodes) == 1: # rsh
        sp_args = []
        if g_opt['l']: sp_args = sp_args + ['-l',g_opt['l']]
        if g_opt['x']: sp_args = sp_args + ['-x']
        if g_opt['X']: sp_args = sp_args + ['-X']
        if g_opt['f']: sp_args = sp_args + ['-f']
        if g_opt['F']: sp_args = sp_args + ['-F']
        if g_opt['N']: sp_args = sp_args + ['-N']
        sp_args = sp_args + [node_info['ret_info']['name']]
        q_user_arg_s     = build_quoted_str( args )
        sp_args = sp_args + ['/bin/sh','-c'] # NOTE: I cannot use 'exec','sh'... b/c
        # of "&& echo..." appended below. And "&& echo..." needs to be appended
        # after sh -c 'cmd' (as opposed to to the end of cmd) b/c usr cmd
        # might end w/ "&"
        # HERE'S THE 2ND PLACE WHERE I NEED TO ADD CONNECT_MAGIC
        sh_cmd_s = "'"  # I want only sh to interpret things
        sh_cmd_s = sh_cmd_s+'echo %s;'%(CONNECT_MAGIC,)
        g_connects_expected = g_connects_expected + 1
        sh_cmd_s = sh_cmd_s+'RGANG_MACH_ID=%d;export RGANG_MACH_ID;'%(mach_idx+g_mach_idx_offset,)
        sh_cmd_s = sh_cmd_s+'RGANG_INITIATOR=%s;export RGANG_INITIATOR;'%(os.environ['RGANG_INITIATOR'],)
        sh_cmd_s = sh_cmd_s+'RGANG_PARENT=%s;export RGANG_PARENT;'%(g_thisnode.hostnames_l[0],)
        sh_cmd_s = sh_cmd_s+'RGANG_PARENT_ID=%s;export RGANG_PARENT_ID;'%(g_thisnode.mach_idx,)
        sh_cmd_s = sh_cmd_s+'if [ -r $HOME/.rgangrc ];then . $HOME/.rgangrc;fi;'

        sh_cmd_s = sh_cmd_s+build_sh_doubly_single_quoted_str(string.join(args,' '))

        sh_cmd_s = sh_cmd_s+"'"  # end the sh cmd string

        TRACE( 22, 'spawn_cmd rsh sh_cmd_s=>%s<', sh_cmd_s )

        sp_args = sp_args + [sh_cmd_s]
        sp_args = sp_args+[' && echo %s""0 || echo %s""1'%(STATUS_MAGIC,STATUS_MAGIC)]

        sp_info = spawn( g_opt['rsh'], sp_args, g_opt['combine'] )
        node_info['stage'] = 'rsh'
        timeout_add( node_info['gbl_branch_idx'], float(g_opt['rshto']) )
    elif len(branch_nodes) >= 1: # rsh rgang  (not user command!)
        # need rsh <rsh_opts>... <node> <sh_cmd>
        #                 sh_cmd is appended/quoted_str of "sh -c 'python_n_rgangapp_path_var_set;rgang_app '"
        #                                                  ['"]quoted_rgang_opts['"]
        #                                                  "' - '"
        #                                                  ['"]quoted_user_args['"]
        sp_args = []
        if g_opt['l']: sp_args = sp_args + ['-l',g_opt['l']]
        if g_opt['x']: sp_args = sp_args + ['-x']
        if g_opt['X']: sp_args = sp_args + ['-X']
        if g_opt['f']: sp_args = sp_args + ['-f']
        if g_opt['F']: sp_args = sp_args + ['-F']
        if g_opt['N']: sp_args = sp_args + ['-N']
        sp_args = sp_args + [node_info['ret_info']['name']]
        q_user_arg_s     = build_quoted_str( args )
        sp_args = sp_args + ['/bin/sh','-c']
        # HERE'S THE 3RD PLACE WHERE I NEED TO ADD CONNECT_MAGIC
        sh_cmd_s = "'"  # I want only sh to interpret things
        sh_cmd_s = sh_cmd_s+'echo %s;'%(CONNECT_MAGIC,)
        g_connects_expected = g_connects_expected + 1
        sh_cmd_s = sh_cmd_s+'PATH=%s:$PATH;'%(g_opt['path'],)  # see option init
        sh_cmd_s = sh_cmd_s+'RGANG_MACH_ID=%d;export RGANG_MACH_ID;'%(mach_idx+g_mach_idx_offset,)
        sh_cmd_s = sh_cmd_s+'RGANG_INITIATOR=%s;export RGANG_INITIATOR;'%(os.environ['RGANG_INITIATOR'],)
        sh_cmd_s = sh_cmd_s+'RGANG_PARENT=%s;export RGANG_PARENT;'%(g_thisnode.hostnames_l[0],)
        sh_cmd_s = sh_cmd_s+'RGANG_PARENT_ID=%s;export RGANG_PARENT_ID;'%(g_thisnode.mach_idx,)
        sh_cmd_s = sh_cmd_s+'if [ -r $HOME/.rgangrc ];then . $HOME/.rgangrc;fi;' # stdout from .rgangrc should be OK; I search for PICKLE:
        sh_cmd_s = sh_cmd_s+'%s '%(g_opt['app'],)
        sh_cmd_s = sh_cmd_s+'--pypickle --mach_idx_offset=%d '%(g_mach_idx_offset+mach_idx,)
        for rgang_opt in opts:
            if string.find(rgang_opt,'--mach_idx_offset') == 0: continue
            if string.find(rgang_opt,'--pypickle')        == 0: continue
            # use build_quoted_str to preserve, i.e., --rsh="rsh -F" (which is
            # equiv to "--rsh=rsh -F")
            sh_cmd_s = sh_cmd_s+build_sh_doubly_single_quoted_str(build_quoted_str([rgang_opt]))+' '

        sh_cmd_s = sh_cmd_s+'- '    # "-" is the nodespec

        for arg_s in args:
            sh_cmd_s = sh_cmd_s+build_sh_doubly_single_quoted_str( build_sh_single_quoted_str(arg_s) ) + ' '

        sh_cmd_s = sh_cmd_s+"'"  # end the sh cmd string

        TRACE( 22, 'spawn_cmd rang sh_cmd_s=>%s<', sh_cmd_s )

        sp_args = sp_args + [sh_cmd_s]
        sp_info = spawn( g_opt['rsh'], sp_args, 0 )  # never combine stderr/out of rsh rgang
        TRACE( 23, 'spawn_cmd sending nodes: %s', branch_nodes )
        for machine in branch_nodes:
            os.write( sp_info[1], machine )
            os.write( sp_info[1], '\n' )
        os.write( sp_info[1], '.\n' )
        node_info['stage'] = 'rgang'
        timeout_add( node_info['gbl_branch_idx'], float(g_opt['rshto']) )
    else:                        # program error
        raise 'Program Error', 'unexpected branch_nodes list len=%s'%(len(branch_nodes),)
    return sp_info   #pid,child_stdin,child_stdout,child_stderr
    # spawn_cmd, spawn


class NodeInfo:
    import socket                       # gethostname()
    def __init__( self ):
        import socket
        import string                   # split
        import os
        xx = socket.gethostbyaddr( socket.gethostname() )
        self.hostnames_l = [xx[0]]
        self.alias_l     = xx[1]
        self.ip_l        = xx[2]
        ss = string.split(xx[0],".")
        if len(ss) == 1: self.shortnames_l = self.hostnames_l
        else:            self.shortnames_l = [ss[0]]
        try: # must "try" because this aint going to work under every os
            # get a list of inet address for all interfaces and aliases
            os_fo = os.popen( "ifconfig 2>/dev/null | grep 'inet addr:' | sed -e 's/.*addr://' -e 's/ .*//'" )
            for inet_addr in os_fo.readlines():
                xx = socket.gethostbyaddr(inet_addr[:-1])
                self.hostnames_l = self.hostnames_l + [xx[0]]
                self.alias_l     = self.alias_l     + xx[1]
                self.ip_l        = self.ip_l        + xx[2]
                ss = string.split(xx[0],".")
                if len(ss) == 1: self.shortnames_l = self.shortnames_l + self.hostnames_l
                else:            self.shortnames_l = self.shortnames_l + [ss[0]]
            os_fo.close()
        except: pass
        self.mach_idx = '?'  # rgang specific
    def is_me( self, node ):
        import string                   # find
        # NOTE: I feel that using gethostbyaddr, which potentially
        # contacts the names server, is not the right choice.
        if string.find(node,".") == -1:
            if    node in self.shortnames_l \
               or node in self.alias_l \
               or node in self.ip_l: return 1
            else:                    return 0
        else:
            if    node in self.hostnames_l \
               or node in self.alias_l \
               or node in self.ip_l: return 1
            else:                    return 0
    # NodeInfo


def get_nway_indexes( nway, nth, list_length, minus_idx0=0 ):
    if minus_idx0: minus_idx0=1; list_length = list_length - 1
    split_num = float(list_length) / nway
    start     = int( ((nth)*split_num)+0.5 ) + minus_idx0
    end       = int( ((nth+1)*split_num)+0.5 ) + minus_idx0
    TRACE( 23, 'get_nway_indexes(nway=%s,nth=%s,list_length=%s,minus_idx0=%s)=(start=%s,end=%s)',
           nway, nth, list_length, minus_idx0, start, end )
    return start,end
    # get_nway_indexes

def determ( index, list_length, nway, minus_idx0=0 ):
    if minus_idx0: minus_idx0=1; list_length = list_length - 1
    # get starting point
    split_num = float(list_length) / nway
    nth = int((index-minus_idx0)/split_num)
    # now see if it's right
    if (index-minus_idx0) >= int( ((nth+1)*split_num)+0.5 ): nth = nth + 1
    idx_in_nth = (index-minus_idx0) - int( ((nth)*split_num)+0.5 )
    return nth,idx_in_nth
    # determ, get_nway_indexes


def header( machine, args ):
    if   g_opt['n'] == '1': os.write( sys.stdout.fileno(), "%s= "%(machine,) )
    elif g_opt['n'] == '2' or g_opt['n'] == '3':   print "\n\
- - - - - - - - - - - - - - %s - - - - - - - - - - - - - -"%(machine,)
    if g_opt['c'] and g_opt['n']=='3':
        sp_args = args[:-1]+['%s:%s'%(machine,args[-1])]
        print '%s %s'%(g_opt['rcp'],string.join(sp_args))
    elif not g_opt['c'] and g_opt['n']=='3':
        print '%s %s %s'%(g_opt['rsh'],machine,build_quoted_str(args))
    sys.stdout.flush()
    # header


# returns string,status where:
#    status=0 == line
#    status=1 == tmo
#    status=2 == eof
def try_line( fd ):
    import select
    sts = 0
    try:
        #final_s = s = fd.read( 1 )
        #final_s = s = os.read(fd.fileno(), 1 )
        final_s = s = os.read(fd, 1 )
    except:   # any error - THIS CAN MESS UP ^C (main()'s except KeyboardInterrupt...)
        return '',2
        #TRACE( 0, 'try_line 1st read - fd=%d', fd )
        #sys.exit( 1 ) 
        #exc, value, tb = sys.exc_info()
        #raise exc, value
    try:
        TRACE( 24, 'try_line looking for line' )
        while s != '\n' and s != '':
            rr,ww,ee = select.select([fd],[],[],0.9)
            #rr,ww,ee = select.select([fd.fileno()],[],[],1)
            if not rr: sts=1;break
            #s = fd.read( 1 )
            #s = os.read(fd.fileno(), 1 )
            s = os.read( fd, 1 )
            final_s = final_s + s
        if s == '': sts=2
    except:   # ??????
        sys.stderr.write( 'while... fd=%s\n'%(fd,) )
        #sys.exit( 1 )
        exc, value, tb = sys.exc_info()
        raise exc, value
    TRACE( 25, 'try_line returning %s', (final_s,sts) )
    return final_s,sts
    # try_line


def get_output( sel_l, fo2node, wait ):
    import select
    import os
    global g_num_connects               # because I'm modifying it

    mach_idx=-1; s='' # init for TRACE below
    chk_exit=0; final_s=''; fd=None; sh_exit_status=None
    while 1: # debugging (EAAGAIN; see below)
        #if sys.stdin in sel_l: TRACE( 26, 'get_output select checking stdin' )
        #TRACE( 26, 'get_output sel_l=%s wait=%s', sel_l, wait )

        ready = select.select( sel_l, [], sel_l, wait )

        #TRACE( 27, 'get_output ready is %s', ready )
        if not ready[0]:
            # timeout (or error, but assume timeout; I'm not processing errors)
            if ready[2]: raise 'Program Error', 'select error'
            break

        fd = ready[0][0]
        mach_idx = fo2node[fd]['mach_idx']

        #if   fo2node[fd]['std'] == sys.stdout.fileno():
        #    TRACE( 27, 'get_output select processing for mach_idx=%d stdout', mach_idx )
        #elif fo2node[fd]['std'] == sys.stdin.fileno():
        #    TRACE( 27, 'get_output select processing for mach_idx=%d stderr', mach_idx )
        #else:
        #    TRACE( 27, 'get_output select processing for mach_idx=%d main stdin', mach_idx )
        # NOTE: When in pty mode, the input is NOT echoed locally and
        #       currently it will take time to check for the STATUS_MAGIC
        #       before echoing the typed characters.
        try:
            # ['stage'] should be (see spawn_cmd) one of:
            #  copy-mode:
            #       'rcp'
            #       'rgang'    need "connect"
            #  cmd-mode:
            #       'local'
            #       'rsh'      need "connect" ,then "status"
            #       'rgang'    need "connect"
            if    fo2node[fd]['std'] == sys.stdout.fileno() \
               and ( g_internal_info[mach_idx]['stage'] == 'rsh' \
                     or (g_internal_info[mach_idx]['stage'] == 'rgang' \
                         and g_internal_info[mach_idx]['connected'] == 0 )):
                s,sts = try_line( fd )
            else:
                # Could also be main stdin
                final_s = os.read( fd, 8192 )
                if not final_s: chk_exit = 1
                return chk_exit, final_s, fd, mach_idx, sh_exit_status
        except IOError, detail:
            if detail.errno == 11: sys.stderr.write( "EAGAIN\n" ); continue
            else: raise IOError, detail
        #TRACE( 31, "get_output mach_idx=%d: ['stage']=%s connect=%s s=>%s<"
        #       , mach_idx, g_internal_info[mach_idx]['stage'], g_internal_info[mach_idx]['connected'], s )

        if s:
            if    fo2node[fd]['std'] == sys.stdout.fileno():
                if ( g_internal_info[mach_idx]['stage'] == 'rsh' \
                      or g_internal_info[mach_idx]['stage'] == 'rgang') \
                         and g_internal_info[mach_idx]['connected'] == 0:
                    # Look for the STATUS_MAGIC or CONNECT_MAGIC.
                    # NOTE! THERE IS THE SMALL POSSIBILITY THAT THIS PROCESSING
                    # WILL FAIL B/C THE OF A DELAY IN THE TRANSMISSION OF THE
                    # STATUS LINE (GREATER THAN THE TIMEOUT IN THE TRY_LINE
                    # FUNCTION ABOVE)
                    if re_connect.search( s ):
                        TRACE( 29, 'get_output mach_idx=%d: yes connect magic', mach_idx )
                        final_s = re_connect.match_obj.group(1)
                        g_internal_info[mach_idx]['connected'] = 1
                        g_num_connects = g_num_connects + 1
                        timeout_cancel( g_internal_info[mach_idx]['gbl_branch_idx'] )
                    else:
                        final_s = s
                elif g_internal_info[mach_idx]['stage'] == 'rsh': # and connected
                    if re_status.search( s ):
                        TRACE( 29, 'get_output mach_idx=%d: yes status magic', mach_idx )
                        final_s = re_status.match_obj.group(1)
                        sh_exit_status = int(re_status.match_obj.group(2))
                    else:
                        final_s = s
                else: # either rcp, local or (rgang and connected)
                    final_s = s
            else:
                final_s = s
            break
        else:
            chk_exit = 1
        break
    #TRACE( 31, 'get_output mach_idx=%d fd=%s chk_exit=%s sh_exit_status=%s returning (s=%s) >%s<',
    #       mach_idx,fd,chk_exit,sh_exit_status,s,final_s )
    return chk_exit, final_s, fd, mach_idx, sh_exit_status
    # get_output


def do_output( mach_idx, processing_idx ):
    if     mach_idx == processing_idx \
       and not g_opt['pyret'] \
       and g_internal_info[mach_idx]['stage'] != 'rgang':
          return 1
    else: return 0
    # do output


def info_update( mach_idx, fo2node_map, sp_info, select_l ):
    # recall: sp_info=[pid,child_stdin,child_stdout,child_stderr]
    g_internal_info[mach_idx]['sp_info'] = sp_info
    if 1:
        fo2node_map[sp_info[1]] = {'mach_idx':mach_idx,'std':None}
        fo2node_map[sp_info[2]] = {'mach_idx':mach_idx,'std':sys.stdout.fileno()}
        select_l.insert( 0, sp_info[2] )  # order matters; do not "append" after select_l[0] (main stdin)
    if sp_info[3]:
        fo2node_map[sp_info[3]] = {'mach_idx':mach_idx,'std':sys.stderr.fileno()}
        select_l.insert( 0, sp_info[3] )  # order matters; do not "append" after select_l[0] (main stdin)
    # info_update


def info_clear( fd, fo2node_map, select_l ):
    TRACE( 2, "info_clear clearing fd=%s", fd )
    select_l.remove( fd )
    del( fo2node_map[fd] )
    os.close( fd )
    # info_clear

# this routine requires:
# g_timeout_l=[];g_opt={'c':1}
def timeout_add( gbl_br_idx, timeout_period ): # timeout_period is either float(g_opt['rshto'] or float(g_opt['rcpto']
    import time
    # b/c rcp time can be different, I need to search-add (list needs to be ordered)
    #
    expire_tm = time.time()+timeout_period
    if not g_opt['c']:          g_timeout_l.append( {'timeout_expires':expire_tm,'gbl_branch_idx':gbl_br_idx} )
    elif len(g_timeout_l) == 0: g_timeout_l.append( {'timeout_expires':expire_tm,'gbl_branch_idx':gbl_br_idx} )
    else: # copy mode, mix of rsh and rcp
        low_idx=0; high_idx=len(g_timeout_l)-1  # gaurd against len=0 above
        mid_idx = low_idx + (high_idx - low_idx)/2
        while mid_idx!=high_idx:
            if expire_tm < g_timeout_l[mid_idx]['timeout_expires']: high_idx = mid_idx
            else:                                                   low_idx = mid_idx+1 # no need to look at mid again
            mid_idx = low_idx + (high_idx - low_idx)/2
        if expire_tm < g_timeout_l[mid_idx]['timeout_expires']: new_idx = mid_idx
        else:                                                   new_idx = mid_idx+1
        g_timeout_l.insert( new_idx, {'timeout_expires':expire_tm,'gbl_branch_idx':gbl_br_idx} )
        pass
    pass
    # timeout_add

# currently OK if not found
def timeout_cancel( gbl_br_idx ):
    found = 0
    for idx in range(len(g_timeout_l)):
        if g_timeout_l[idx]['gbl_branch_idx'] == gbl_br_idx: found=1; g_timeout_l.pop(idx); break
    TRACE( 31, "timeout_cancel branch_idx=%d found=%d", gbl_br_idx, found )
    # timeout_cancel


# This handles 1 timeout - the 1st one!
def timeout_connect_process():
    import select                       # select
    branch_idx = g_timeout_l[0]['gbl_branch_idx']
    mach_idx = g_branch_info_l[branch_idx]['active_head']
    connected = g_internal_info[mach_idx]['connected']
    # recall: sp_info=[pid,child_stdin,child_stdout,child_stderr]
    pid       = g_internal_info[mach_idx]['sp_info'][0]
    g_timeout_l.pop(0)
    TRACE( 30, "timeout_connect_process branch_idx=%d connected=%d pidToKill=%d br_in=%s g_tmo_l=%s",
           branch_idx, connected, pid, g_internal_info[mach_idx]['sp_info'][1], g_timeout_l )

    # append ?something? to stderr
    ret_info = g_internal_info[mach_idx]['ret_info']
    ret_info['stderr'] = ret_info['stderr']+'rgang timeout expired\n'

    # do kill and kill check here
    for sig in (1,2,15,3,9):  # 1=HUP, 2=INT(i.e.^C), 15=TERM(default "kill"), 3=QUIT(i.e.^\), 9=KILL
        try: rpid,status = os.waitpid(pid,os.WNOHANG);status=(status>>8)  # but I probably won't use this status
        except: rpid = 0; break  # i.e. (OSError, '[Errno 10] No child processes')
        if rpid == pid:  # OK, process is out-of-there
            if g_internal_info[mach_idx]['ret_info']['rmt_sh_sts'] == None:
                TRACE( 31, "timeout_connect_process status=%d", status )
                g_internal_info[mach_idx]['ret_info']['rmt_sh_sts'] = 8
            break
        os.kill(pid,sig)
        TRACE( 31, "timeout_connect_process os.kill(%d,%d)", pid, sig )
        select.select([],[],[],0.05)     # use select to sleep sub second

    return mach_idx  # need to return "chk_exit,..." like get_output
    # timeout_connect_process


def initiator_node_status( mach_idx ):
    # FIRST DETERMINE IF I AM THE INITIATOR NODE
    if g_opt['mach_idx_offset']=='' and g_opt['err-file']!='':
        sts = g_internal_info[mach_idx]['ret_info']['rmt_sh_sts']
        if sts != 0:
            TRACE( 28, 'initiator_node_status mach_idx=%d sts=%s', mach_idx,sts )
            fo = open( g_opt['err-file'], 'a+' )
            name = g_internal_info[mach_idx]['ret_info']['name']
            fo.write( "%s # mach_idx=%d sts=%s\n"%(name,mach_idx,sts) )
            fo.close()
    # initiator_node_status


def node_list_from_file( listfile ):
    mach_l = []
    fo = open(listfile)
    TRACE( 2, "node_list_from_file fo.fileno()=%d", fo.fileno() )
    for xx in fo.readlines():
        if re_mach.search(xx): mach_l.append(re_mach.match_obj.group(1))
    fo.close()
    return mach_l

def node_list_from_spec( spec ):
    mach_l = []
    if spec == '-':
        xx,sts = try_line( sys.stdin.fileno() )
        #xx = sys.stdin.readline()
        while xx != '.\n' and xx != '':
            if re_mach.search(xx): mach_l.append(re_mach.match_obj.group(1))
            xx,sts = try_line( sys.stdin.fileno() )
            #xx = sys.stdin.readline()
    elif spec[0]=='.' and os.access(spec,os.R_OK):
        listfile = spec
        mach_l = node_list_from_file( listfile )
    elif os.access(g_opt['farmlets']+'/'+spec,os.R_OK):    # you can always specify --farmlets=.
        listfile = g_opt['farmlets']+'/'+spec
        mach_l = node_list_from_file( listfile )
    elif os.access(spec,os.R_OK):
        listfile = spec
        mach_l = node_list_from_file( listfile )
    else:
        if g_opt['verbose']: sys.stderr.write('assuming expandable node list\n')
        mach_l = expand( spec )
    return mach_l


def clean():
    #tty.setcbreak(0)
    os.system( "stty sane" )
    #print 'term reset'
    return
    # clean

def cleanup(signum,frame):
    clean()
    sys.exit( 1 )
    return
    # cleanup



g_opt={'tlvlmsk':0}                     # and init so test script importing
                                        # rgang (to test rgang.expand(),
                                        # for example) don't have to.

def rgang( opts_n_args ):
    import os                           # system
    import pickle                       # dumps
    import traceback                    # format_exception
    import pprint                       # pprint
    import signal                       # signal
    global g_opt
    global g_thisnode                   # 
    global g_timeout_l                  # 
    global g_internal_info              # 
    global g_branch_info_l              # 
    global g_mach_idx_offset            # 
    global g_num_connects               # needed for robust "input-to-all-branches" see (get_output)
    global g_connects_expected          # needed for robust "input-to-all-branches" see (spawn_cmd and below)
    # --------------------------------- # NOTE: currently, there is the
    # possibility of a hang on the write to a branch if all nodes in
    # the rgang sub tree fail and stdin is large.

    opts,args,g_opt,usage = getopts( OPTSPEC, opts_n_args, USAGE, APP )
    try: g_opt['tlvlmsk'] = int( eval(g_opt['tlvlmsk']) )  # 0x hex or normal decimal numbers OK
    except:              sys.stderr.write('invalid tlvlmsk value; must be integer/hex\n');return 1,[]
    g_thisnode = NodeInfo()  # needed before 1st TRACE
    TRACE( 3, 'rgang g_opt is %s', g_opt )

    if g_opt['d']:
        c="ls %s"%(g_opt['farmlets'],); os.system(c); return 0,[]
    elif g_opt['list'] and not args:
        if os.access(g_opt['farmlets']+'/.',os.R_OK):
            c1="for i in *;do echo FARMLET $i:; cat $i;done"
            c="sh -c 'cd %s;%s'"%(g_opt['farmlets'],c1)
            os.system(c)
        else:
            print 'farmlets directory %s not readable'%(g_opt['farmlets'],)
        return 0,[]
    if not args: print 'no args\n'+usage; return 0,[]

    mach_l = node_list_from_spec( args.pop(0) )

    if g_opt['pyprint']:  g_opt['pyret']='1'
    if g_opt['pypickle']: g_opt['pyret']='1'
    if g_opt['pypickle'] and g_opt['pyprint']: g_opt['pyprint']='' # pypickle wins
    # clean skips
    if g_opt['skip']:
        skip_l = node_list_from_spec( g_opt['skip'] )
        for sk in skip_l:
            ii = 0; mach_l_len = len( mach_l )
            while ii < mach_l_len:
                if mach_l[ii] == sk: mach_l.pop(ii); mach_l_len = mach_l_len-1
                else: ii = ii + 1
    if g_opt['s']:  # skip current (local) node
        ii = 0; mach_l_len = len( mach_l )
        while ii < mach_l_len:
            if g_thisnode.is_me(mach_l[ii]):
                mach_l.pop(ii); mach_l_len = mach_l_len - 1
            else: ii = ii + 1
    # mach_l is now set.

    if g_opt['list']:
        if not g_opt['pyret']:
            for mach in mach_l: print mach
        overall_status = 0; ret_info = mach_l # ret_info can have different formats
        if   g_opt['pyprint']:  pprint.pprint( ret_info )
        elif g_opt['pypickle']:
            dumps = pickle.dumps(ret_info)
            sys.stdout.write( 'PICKLE:%08x:'%(len(dumps),) )
            sys.stdout.write( dumps )
        return overall_status,ret_info

    TRACE( 4, 'rgang args is %s', args )
    if g_opt['C']:        g_opt['s']='1'; g_opt['c']='1'
    if g_opt['n'] == '':
        if len(mach_l) == 1: g_opt['n']='0'
        else:                g_opt['n']='1'
    elif g_opt['n'] == 'n': g_opt['n']='1'
    if len(g_opt['n'])>1 or not '0'<=g_opt['n']<='3':
        sys.stderr.write('invalid optional argument "%s" for -n option\n'%(g_opt['n'],))
        return 1,[]

    if g_opt['c'] and len(args) < 2:
        sys.stderr.write('copy mode must have at least 2 arguments\n')
        return 1,[]

    if len(args) == 0:
        sys.stderr.write('interactive not yet supported\n');    return 1,[]

    try: nway = int( g_opt['nway'] ) # int(string)=>int and int(int)=>int
    except:      sys.stderr.write('invalid nway value; must be integer >= 0\n');return 1,[]
    if nway < 0: sys.stderr.write('invalid nway value; must be integer >= 0\n');return 1,[]

    if g_opt['mach_idx_offset'] != '': # note: also used to determine initiator node
        try: g_mach_idx_offset = int( g_opt['mach_idx_offset'] ) # int(string)=>int and int(int)=>int
        except: sys.stderr.write('invalid mach_idx_offset value; must be decimal integer\n');return 1,[]
        g_thisnode.mach_idx = '%d'%(g_mach_idx_offset,) # for spawn_cmd rsh rgang
        g_opt['do-local'] = 1 # I'm assuming I've already rsh'd (rsh rgang...), so don't do rsh again
    else: # assume I'm the "initiator" node
        os.environ['RGANG_INITIATOR'] = g_thisnode.hostnames_l[0]
        # set the following now, in case we are also the root node and
        # opt['do-local']; this make spawn_cmd easier
        os.environ['RGANG_PARENT'] = ''
        os.environ['RGANG_PARENT_ID'] = ''
        g_mach_idx_offset = 0 # for branches (see spawn_cmd)
        g_thisnode.mach_idx='' # for spawn_cmd rsh rgang; init for TRACE
        for ii in range(len(mach_l)):
            if g_thisnode.is_me(mach_l[ii]): g_thisnode.mach_idx='%d'%(ii,); break # for spawn_cmd rsh rgang
        if g_opt['err-file'] != '':   # init err-file
            fo = open( g_opt['err-file'], 'w+' )
            TRACE( 2, "rgang err-file fd=%d", fo.fileno() )
            fo.close()

    if g_opt['serial']:
        if g_opt['input-to-all-branches']:
            sys.stderr.write('invalid --serial/--input-to-all-branches configuration\n');return 1,[]
        outer_nway = nway; inner_nway = 0
    else:
        outer_nway = 1;    inner_nway = nway
    mach_l_len = len( mach_l )
    if outer_nway > mach_l_len or outer_nway == 0: outer_nway = mach_l_len  # inner_nway is handled below

    
    ####### OK done with ALL the OPTIONS PROCESSING

    if g_opt['pty']:
        signal.signal(2,cleanup)
        signal.signal(15,cleanup)
        os.system("stty -echo -icanon min 1 time 0" )
        os.system("stty -inlcr -icrnl" )      # no translations
        #os.system("stty ignbrk -ixon -isig" )
        os.system("stty ignbrk -ixon" )


    ####### NOW, DO THE WORK!!!!

    stdin_bytes = 0L   # could be counting > 2G bytes
    # build/initialize the array so we can add stdin at the end
    ret_info = []; g_internal_info=[]
    for ii in range(mach_l_len):
        ret_info.append(None); g_internal_info.append(None)

    g_num_connects = 0
    g_connects_expected = 0
    select_l = []
    fo2node_map = {}
    if not g_opt['input-to-all-branches']:
        # add in (kludge in??) stdin --> index mach_l_len
        g_internal_info.append( {'gbl_branch_idx':None,
                                 'ret_info':None, # ret_info NOT NEEDED!
                                 'stage':None,'sp_info':None,'connected':1} )
        select_l.append(sys.stdin.fileno())
        fo2node_map[sys.stdin.fileno()] = {'mach_idx':mach_l_len,'std':None}
        need_stdin_after_connects = 0
    else:
        need_stdin_after_connects = 1

    branch_input_l = []
    g_branch_info_l = []
    g_timeout_l = []

    have_me = 0 # basicaly, flag to skip past idx 0 in branch processing below
    if not g_opt['c'] and not g_opt['serial'] and g_thisnode.is_me(mach_l[0]):
        have_me = 1
        ret_info[0] = {'name':mach_l[0],'stdout':'','stderr':'','rmt_sh_sts':None}
        g_branch_info_l.append( {'active_head':0,'branch_end_idx':1} )
        gbl_branch_idx = len(g_branch_info_l)-1     # len would be 1 here ==> gbl_branch_idx = 0
        g_internal_info[0] = {'gbl_branch_idx':gbl_branch_idx,
                            'ret_info':ret_info[0], # ptr
                            'stage':None,'sp_info':None,'connected':0}
        TRACE( 5, 'rgang local spawn_cmd' )
        mach_idx = 0
        sp_info = spawn_cmd( g_internal_info[mach_idx], mach_idx, opts, args, [mach_l[0]], g_opt['do-local'] )                         #1 not g_opt['c'] and g_thisnode.is_me(mach_l[0])
        info_update( 0, fo2node_map, sp_info, select_l )
        branch_input_l.append( sp_info[1] )
        # no timeout

    overall_status = 0
    START = 0; END = 1
    processing_idx = 0
    # outer loops result when --serial is specified. It is processed in
    # conjunction with the --nway option to specify the number of outer loops.
    # (nway==0 means all nodes so just specifying --serial with --nway=0 gives
    # "completely serial" operation. --serial with --nway=2 with 400 nodes
    # would do 2 set of 200_parallel_spawns This can be demonstrated via:
    #   rgang.py --serial --nway=2 "192.168.1.136{,,,,,}" 'sleep 8;date'
    for outer_group_idx in range(outer_nway):
        grp_idxs = get_nway_indexes( outer_nway, outer_group_idx, mach_l_len, have_me)

        # START EACH BRANCH
        #    need to get:
        #      - list for select for get output_line and 
        #      - map of select fo to node
        group_len = grp_idxs[END] - grp_idxs[START]
        if inner_nway > group_len or inner_nway == 0: inner_nway = group_len

        for inner_branch_idx in range(inner_nway):
            branch_idxs = get_nway_indexes( inner_nway, inner_branch_idx, group_len)
            branch_len = branch_idxs[END] - branch_idxs[START]
            mach_idx = grp_idxs[START] + branch_idxs[START]
            branch_end_idx = mach_idx + branch_len
            g_branch_info_l.append( {'active_head':mach_idx,'branch_end_idx':branch_end_idx} )
            gbl_branch_idx = len(g_branch_info_l)-1
            for ii in range(branch_len):
                ret_info[mach_idx+ii] = {'name':mach_l[mach_idx+ii],
                                         'stdout':'','stderr':'','rmt_sh_sts':None}
                g_internal_info[mach_idx+ii] = {'gbl_branch_idx':gbl_branch_idx,
                                              'ret_info':ret_info[mach_idx+ii], # ptr
                                              'stage':None,'sp_info':None,'connected':0}
            branch_nodes = mach_l[mach_idx:branch_end_idx]
            sp_info = spawn_cmd( g_internal_info[mach_idx], mach_idx, opts, args, branch_nodes, 0 )                     #2 for inner_branch_idx in ...
            TRACE( 6, 'rgang after initial spawn_cmd gbl_branch_idx=%d branch_len=%d sp_info=%s', gbl_branch_idx, branch_len, sp_info )
            info_update( mach_idx, fo2node_map, sp_info, select_l )
            branch_input_l.append( sp_info[1] )

        # NOW DO THE PROCESSING
        #
        if not g_opt['pyret']: header( mach_l[processing_idx], args )
        while processing_idx < grp_idxs[END]:

            if need_stdin_after_connects and g_num_connects == g_connects_expected:
                #time.sleep(30)
                g_internal_info.append( {'gbl_branch_idx':None,
                                         'ret_info':None, # ret_info NOT NEEDED!
                                         'stage':None,'sp_info':None,'connected':1} )
                select_l.insert(0,sys.stdin.fileno())
                fo2node_map[sys.stdin.fileno()] = {'mach_idx':mach_l_len,'std':None}
                need_stdin_after_connects = 0
                

            if g_timeout_l:
                # 3 cases:
                # 1) "connect" timeout period expires while waiting at select
                # 2) "connect" timeout period expires while processing for some
                #    node
                # 3) "connect" timeout period never expires as all nodes
                #    "connect" promptly
                timeout_wait = g_timeout_l[0]['timeout_expires'] - time.time()
                if timeout_wait < 0: timeout_wait = 0
            else: timeout_wait = None

            # DO THE SELECT TO (potentially) GET SOME DATA
            #        chk_exit indicate that select indicated a file, but the
            #                 read of the file returned 0 bytes (ss=''); the
            #                 process associated with the particular file/node
            #                 probably exited.
            #                 If check_exit==1 then the following should be true:
            #                     ss==''
            #                     fo!=None
            #                     sh_exit_stat==None
            #              ss is the output data returned unless there is a
            #                    timeout
            #              fo is the file/node to process, unless timeout
            #    sh_exit_stat is set if command exit_status (STATUS_MAGIC) was
            #                 received/indicated.
            # When a timeout occurs, the return values will be (as initialize
            # in get_output):
            #     chk_exit=0;ss='';fo=None;sh_exit_stat=None
            #TRACE( 7, 'rgang before get_output wait=%s select_l=%s need_stdin=%d g_num_connects=%d',
            #       timeout_wait, select_l, need_stdin_after_connects, g_num_connects )
            chk_exit,ss,fo,mach_idx,sh_exit_stat = get_output( select_l, fo2node_map, timeout_wait )

            if fo == None:
                # timeout
                # should be able to do the processing here and not continue, but return
                # chk_exit=1 and mach_idx

                #move processing from above and do it here to properly continue and finish processing after killing process
                # DO CONNECT TIMEOUT PROCESSING NOW
                # IN THE CASE of an rgang node timing out, A NEW TIMEOUT
                # PERIOD WOULD BE INITIATED
                # WHAT HAPPENS IF IT CHANGES THE processing _idx???
                mach_idx = timeout_connect_process()
                chk_exit,ss,sh_exit_stat = 1,'',None
            else:
                # no timeout
                if mach_idx == mach_l_len:  # SPECIAL STDIN FLAG
                    #TRACE( 8, 'rgang stdin processing_idx=%d', processing_idx )
                    if len(ss):
                        #stdin_bytes = stdin_bytes + len(ss)
                        if g_opt['input-to-all-branches'] or g_opt['pyret'] :
                            #TRACE( 9, "rgang branch_input_l=%s", branch_input_l )
                            for br_sdtin in branch_input_l:
                                bytes_written = os.write( br_sdtin, ss )
                                while bytes_written < len(ss):
                                    bytes_this_write = os.write( br_sdtin, ss[bytes_written:] )
                                    bytes_written = bytes_written + bytes_this_write
                        else:
                            os.write( g_internal_info[processing_idx]['sp_info'][1], ss )
                    else:
                        info_clear( sys.stdin.fileno(), fo2node_map, select_l )
                        #TRACE( 9, "rgang closing everyone's stdin after %d bytes l=%s", stdin_bytes, branch_input_l )
                        for br_stdin in branch_input_l:
                            os.close( br_stdin )
                            mi = fo2node_map[br_stdin]['mach_idx']
                            del( fo2node_map[br_stdin] )
                            #pid = g_internal_info[mi]['sp_info'][0]
                            #os.kill(pid,1)
                            #os.kill(pid,13)
                        # this should cause (via chain reaction) the remote
                        # cmd's to exit; the branch_input_l will be cleaned
                        # up when they do; as our stdin is no longer in the
                        # select_l, this whole "SPECIAL STDIN" code should
                        # not get executed again.
                    continue  # after STDIN PROCESSING
                if sh_exit_stat != None: ret_info[mach_idx]['rmt_sh_sts'] = sh_exit_stat # OK if we overwrite timeout kill status

                # PROCESS THE DATA
                if do_output( mach_idx, processing_idx ):
                    os.write( fo2node_map[fo]['std'], ss )
                elif fo2node_map[fo]['std'] == sys.stdout.fileno():
                    ret_info[mach_idx]['stdout'] = ret_info[mach_idx]['stdout'] + ss
                else:
                    ret_info[mach_idx]['stderr'] = ret_info[mach_idx]['stderr'] + ss



            # CHECK FOR BRANCH/GROUP STATUS
            #
            if chk_exit:
                TRACE( 8, 'rgang chk_exit mach_idx=%d processing_idx=%d sp_info=%s',
                       mach_idx, processing_idx, g_internal_info[mach_idx]['sp_info'] )

                if do_output( mach_idx, processing_idx ):
                    # print any previously store stdout/err
                    os.write( sys.stdout.fileno(), ret_info[mach_idx]['stdout'] )
                    os.write( sys.stderr.fileno(), ret_info[mach_idx]['stderr'] )

                # cleanup_output_status
                # if the fd that trigger us was stdOUT, then we need to check stdERR
                pid = g_internal_info[mach_idx]['sp_info'][0]
                if g_internal_info[mach_idx]['sp_info'][3] \
                   and ( ( fo != None and fo2node_map[fo]['std'] == sys.stdout.fileno() ) \
                         or fo == None ):
                    TRACE( 2, 'rgang CHECKing stdERR fo=%s pid=%d mach_idx=%d', fo, pid, mach_idx )
                    chk = 0; fo2 = g_internal_info[mach_idx]['sp_info'][3] # init this as fo may be None (i.e. tmo)
                    while not chk and fo2 != None:
                        chk,ss,fo2,mi,dont_used = get_output( [g_internal_info[mach_idx]['sp_info'][3]], # 3 is stdERR
                                                                fo2node_map, 0 )
                        if do_output( mach_idx, processing_idx ):
                            os.write( sys.stderr.fileno(), ss )
                        else:
                            ret_info[mach_idx]['stderr'] = ret_info[mach_idx]['stderr'] + ss
                # if the fd that trigger us was stdERR, then we need to check stdOUT
                if g_internal_info[mach_idx]['sp_info'][2] \
                   and ( ( fo != None and fo2node_map[fo]['std'] == sys.stderr.fileno() ) \
                         or fo == None ):
                    TRACE( 2, 'rgang CHECKing stdOUT fo=%s pid=%d mach_idx=%d', fo, pid, mach_idx )
                    # There quite possibly could be 2 iteration through
                    # this while. If the main get_output (above) had stderr
                    # in the select list first AND the shell is really fast AND
                    # there is little to no output, then the CONNECT machanism
                    # may not have happened and then the 1st loop here will
                    # cause the a '' value to be returned for ss; chk will be 0
                    # however.
                    chk = 0; fo2 = g_internal_info[mach_idx]['sp_info'][2] # init this as fo may be None (i.e. tmo)
                    while not chk and fo2 != None:
                        chk,ss,fo2,mi,sh_exit_stat = get_output( [g_internal_info[mach_idx]['sp_info'][2]],  # 2 is stdout
                                                                fo2node_map, 0 )
                        if sh_exit_stat != None:
                            ret_info[mach_idx]['rmt_sh_sts'] = sh_exit_stat # OK if we overwrite timeout kill status
                        if do_output( mach_idx, processing_idx ):
                            os.write( sys.stdout.fileno(), ss )
                        else:
                            ret_info[mach_idx]['stdout'] = ret_info[mach_idx]['stdout'] + ss
                            pass
                        pass
                    pass
                # done with output from process
                # remove sub-process's output and input fds from
                # the select list, fo2node_map, branch_input_l
                for ffo in g_internal_info[mach_idx]['sp_info'][2:]:
                    if ffo: info_clear( ffo, fo2node_map, select_l )
                branch_input_l.remove( g_internal_info[mach_idx]['sp_info'][1] )
                if g_internal_info[mach_idx]['sp_info'][1] in fo2node_map.keys():
                    del( fo2node_map[g_internal_info[mach_idx]['sp_info'][1]] )
                gbl_branch_idx = g_internal_info[mach_idx]['gbl_branch_idx']
                timeout_cancel( gbl_branch_idx )

                try:
                    opid,status = os.waitpid( pid, 0 )
                    if opid != pid: raise 'Program Error', 'process did not exit'
                    TRACE( 2, 'rgang waitpid got status for pid=%d mach_idx=%d gbl_branch_idx=%d status=%s',
                           pid, mach_idx, gbl_branch_idx, status )
                    status = (status>>8)
                except:       # i.e. (OSError, '[Errno 10] No child processes')
                    # must have been killed in timeout_connect_process
                    status = g_internal_info[mach_idx]['ret_info']['rmt_sh_sts']
                    TRACE( 2, 'rgang waitpid NO status for pid=%d mach_idx=%d gbl_branch_idx=%d using status=%s',
                           pid, mach_idx, gbl_branch_idx, status )

                # g_internal_info[x].keys = ('stage','connected','sp_info','gbl_branch_idx','ret_info')
                # g_internal_info[x]['ret_info'].keys = 
                if g_internal_info[mach_idx]['stage'] == 'rgang':
                    g_internal_info[mach_idx]['stage'] = 'done'  # SEE "ACTIVE OUTPUT PROCESSING" BELOW
                    # EEEEEEEE THIS HAS RCP OUTPUT AND RGANG RET!
                    # BUT WAIT, NORMALLY THERE IS NO RCP STDOUT (maybe stderr
                    #stdout should be in form: llllllll:pickle
                    if g_internal_info[mach_idx]['connected'] == 0:
                        g_connects_expected = g_connects_expected - 1 # if it's not connected now, it never will be
                    ss = ret_info[mach_idx]['stdout']
                    TRACE( 11, 'rgang looking for PICKLE in (rmt_sh_sts=%s) >%s<',
                           ret_info[mach_idx]['rmt_sh_sts'], ss )
                    pickle_idx = string.find( ss, "PICKLE:" )
                    if pickle_idx != -1:
                        try:
                            pre =  ss[:pickle_idx]
                            pickle_idx = pickle_idx+len("PICKLE:")
                            length = string.atoi( ss[pickle_idx:pickle_idx+8],16 )
                            loads = pickle.loads( ss[pickle_idx+9:pickle_idx+9+length] )
                            post = ss[pickle_idx+9+length:]
                            if g_opt['c']: offset = 1
                            else:        offset = 0;stderr_sav=ret_info[mach_idx]['stderr']
                            for ii in range(len(loads)):
                                ret_info[mach_idx+offset+ii].update( loads[ii] )
                                overall_status = overall_status | ret_info[mach_idx+offset+ii]['rmt_sh_sts']
                                TRACE( 28, 'rgang calling initiator_node_status #1 mach_idx=%d', mach_idx+offset+ii )
                                initiator_node_status( mach_idx+offset+ii )
                            # NOTE??? for "copy", previous stdout??? may already be printed b/c of rcp stage
                            if g_opt['c']: ret_info[mach_idx]['stdout'] = pre + post
                            else:
                                ret_info[mach_idx]['stdout'] = pre + ret_info[mach_idx]['stdout'] + post
                                ret_info[mach_idx]['stderr'] = stderr_sav + ret_info[mach_idx]['stderr']
                        except:
                            sys.stderr.write('EEEEE-pickle exception mach_idx=%s g_opt[c]=%s ii=%s\n'%(mach_idx,g_opt['c'],ii))
                            sys.stderr.write( 'EEEEEEEEE - ss[pickle_idx:pickle_idx+9+length=%d]=>%s<\n'%(length,ss[pickle_idx:pickle_idx+9+length]) )
                            pickle_idx = -1
                            exc, value, tb = sys.exc_info()
                            for ln in traceback.format_exception( exc, value, tb ):
                                sys.stderr.write(ln)
                    if pickle_idx == -1:  # status must be bad
                        if g_opt['c']:
                            ret_info[mach_idx]['stderr'] = ret_info[mach_idx]['stderr'] + '%s: warning: "rcp" %s failed\n'%(APP,APP)
                        else:
                            if ret_info[mach_idx]['rmt_sh_sts'] == None:
                                ret_info[mach_idx]['rmt_sh_sts'] = 2
                                TRACE( 12, 'rgang #1 rmt_sh_sts=2' ) # rsh failure or shell abort (i.e. syntax error)
                            ret_info[mach_idx]['rmt_sh_sts'] = ret_info[mach_idx]['rmt_sh_sts'] | status
                            overall_status = overall_status | ret_info[mach_idx]['rmt_sh_sts']
                            TRACE( 28, 'rgang calling initiator_node_status #2 mach_idx=%d', mach_idx )
                            initiator_node_status( mach_idx )
                        gbl_branch_idx = g_internal_info[mach_idx]['gbl_branch_idx']
                        branch_end_idx = g_branch_info_l[gbl_branch_idx]['branch_end_idx']
                        branch_nodes = mach_l[mach_idx+1:branch_end_idx]
                        if branch_nodes:
                            TRACE( 13, 'rgang spawn_cmd branch_node is %s', branch_nodes )
                            g_branch_info_l[gbl_branch_idx]['active_head'] = mach_idx+1
                            #timeout_cancel( gbl_branch_idx ) # cancel 1st timeout for this gbl_branch_idx
                            sp_info = spawn_cmd( g_internal_info[mach_idx+1], mach_idx+1, opts, args, branch_nodes, 0 ) #3 after bad rgang
                            info_update( mach_idx+1, fo2node_map, sp_info, select_l )
                            branch_input_l.append( sp_info[1] )
                    if mach_idx == processing_idx and not g_opt['pyret']:
                        os.write( sys.stdout.fileno(), ret_info[processing_idx]['stdout'])
                        os.write( sys.stderr.fileno(), ret_info[processing_idx]['stderr'])
                elif g_internal_info[mach_idx]['stage'] == 'rcp':
                    # STRIP OFF NODE HERE
                    if ret_info[mach_idx]['rmt_sh_sts'] != None: sys.stderr.write('1EEEEEEEEEE\n')
                    ret_info[mach_idx]['rmt_sh_sts'] = status
                    overall_status = overall_status | ret_info[mach_idx]['rmt_sh_sts']
                    TRACE( 28, 'rgang calling initiator_node_status #3 mach_idx=%d', mach_idx )
                    initiator_node_status( mach_idx )
                    gbl_branch_idx = g_internal_info[mach_idx]['gbl_branch_idx']
                    branch_end_idx = g_branch_info_l[gbl_branch_idx]['branch_end_idx']
                    branch_nodes = mach_l[mach_idx+1:branch_end_idx]
                    if status == 0 and branch_nodes:
                        TRACE( 14, 'rgang rcp spawn_cmd branch_nodes is %s', branch_nodes )
                        #timeout_cancel( gbl_branch_idx )
                        sp_info = spawn_cmd( g_internal_info[mach_idx], mach_idx, opts, args, branch_nodes, 0 )         #4 the rgang after good rcp
                        info_update( mach_idx, fo2node_map, sp_info, select_l )
                        branch_input_l.append( sp_info[1] )
                        g_branch_info_l[gbl_branch_idx]['active_head'] = mach_idx
                    elif status != 0 and branch_nodes:
                        # start rcp stage on next node
                        TRACE( 15, 'rgang rcp spawn_cmd branch_nodes is %s', branch_nodes )
                        #timeout_cancel( gbl_branch_idx )
                        sp_info = spawn_cmd( g_internal_info[mach_idx+1], mach_idx+1, opts, args, branch_nodes, 0 )     #5 bad rcp, next node rcp
                        info_update( mach_idx+1, fo2node_map, sp_info, select_l )
                        branch_input_l.append( sp_info[1] )
                        g_branch_info_l[gbl_branch_idx]['active_head'] = mach_idx+1
                    else:
                        # DONE WITH BRANCH
                        pass
                    pass
                elif g_internal_info[mach_idx]['stage'] == 'rsh':  # no further branch processing
                    if g_internal_info[mach_idx]['connected'] == 0:
                        g_connects_expected = g_connects_expected - 1 # if it's not connected now, it never will be
                    if ret_info[mach_idx]['rmt_sh_sts'] == None:
                        ret_info[mach_idx]['rmt_sh_sts'] = 4
                        TRACE( 16, 'rgang #2 rmt_sh_sts=4' ) # shell abort (i.e. syntax error)
                    ret_info[mach_idx]['rmt_sh_sts'] = ret_info[mach_idx]['rmt_sh_sts'] | status
                    overall_status = overall_status | ret_info[mach_idx]['rmt_sh_sts']
                    TRACE( 28, 'rgang calling initiator_node_status #4 mach_idx=%d', mach_idx )
                    initiator_node_status( mach_idx )
                else:  # local - no further branch processing
                    if ret_info[mach_idx]['rmt_sh_sts'] != None: sys.stderr.write('4EEEEEEEEEE\n')
                    ret_info[mach_idx]['rmt_sh_sts'] = status
                    overall_status = overall_status | ret_info[mach_idx]['rmt_sh_sts']
                    TRACE( 28, 'rgang calling initiator_node_status #5 mach_idx=%d', mach_idx )
                    initiator_node_status( mach_idx )

                # ACTIVE OUTPUT PROCESSING
                if mach_idx == processing_idx:
                    if g_internal_info[processing_idx]['stage'] == 'rgang': continue  # continue if "inprogress" rgang
                    processing_idx = processing_idx + 1
                    while processing_idx < grp_idxs[END]:
                        if not g_opt['pyret']: header( mach_l[processing_idx], args )
                        if g_internal_info[processing_idx]['stage'] == 'rgang': break
                        if ret_info[processing_idx]['rmt_sh_sts'] == None:
                            if not g_opt['pyret']:
                                # print-n-flush and clear stdout/err
                                os.write( sys.stdout.fileno(),ret_info[processing_idx]['stdout'])
                                ret_info[processing_idx]['stdout'] = ''
                                os.write( sys.stderr.fileno(),ret_info[processing_idx]['stderr'])
                                ret_info[processing_idx]['stderr'] = ''
                            break
                        if not g_opt['pyret']:
                            os.write( sys.stdout.fileno(),ret_info[processing_idx]['stdout'])
                            os.write( sys.stderr.fileno(),ret_info[processing_idx]['stderr'])
                        processing_idx = processing_idx + 1
                        pass
                    pass
                pass # end of "if chk_exit" processing

            pass # while processing_idx < grp_idxs[END]:

    if g_opt['pty']: clean()
    if not g_opt['pyret'] and g_opt['n']=='2': print
    if   g_opt['pyprint']:  pprint.pprint( ret_info )
    elif g_opt['pypickle']:
        dumps = pickle.dumps(ret_info)
        sys.stdout.write( 'PICKLE:%08x:'%(len(dumps),) )
        sys.stdout.write( dumps )
    return overall_status,ret_info
    # rgang


###############################################################################

def main():
    import sys                          # argv, exit
    import select                       # select
    if 1:                               # switch to 0 to debug
        try: total_stat,ret_list = rgang( sys.argv[1:] )
        except KeyboardInterrupt, detail:
            for mach_idx in range(len(g_internal_info)):
                # There is a case, for example: rgang <node> 'sleep 5 &'
                # where rgang will receive the "remote shell status", but because
                # stdout/err were not closed (i.e.:rgang <node> 'sleep 5 >&- 2>&- &' ), the
                # remote shell will hang until the backgrounded process completes.
                # In this case I will have a 'rmt_sh_sts' (it will NOT == None);
                # so I should NOT do 'rmt_sh_sts' checking.
                #if g_internal_info[mach_idx]['ret_info'] != None \
                #   and g_internal_info[mach_idx]['ret_info']['rmt_sh_sts'] == None \
                #   and g_internal_info[mach_idx]['sp_info'] != None:
                if g_internal_info[mach_idx]['sp_info'] != None:
                    pid = g_internal_info[mach_idx]['sp_info'][0]
                    # do kill and kill check here
                    for sig in (1,2,15,3,9):  # 1=HUP, 2=INT(i.e.^C), 15=TERM(default "kill"), 3=QUIT(i.e.^\), 9=KILL
                        try: rpid,status = os.waitpid(pid,os.WNOHANG);status=(status>>8)  # but I probably won't use this status
                        except: rpid = 0; break  # i.e. (OSError, '[Errno 10] No child processes')
                        if rpid == pid:  # OK, process is out-of-there
                            if g_internal_info[mach_idx]['ret_info']['rmt_sh_sts'] == None:
                                TRACE( 30, "main KeyboardInterrupt status=%d", status )
                                g_internal_info[mach_idx]['ret_info']['rmt_sh_sts'] = 0x10
                            break
                        os.kill(pid,sig)
                        TRACE( 30, "main os.kill(%d,%d)", pid, sig )
                        select.select([],[],[],0.05)     # use select to sleep sub second

            # emulate the old shell version of rgang when rsh is "interrupted"
            sys.exit( (1<<7)+2 )
            pass
        pass
    else:
        total_stat,ret_list = rgang( sys.argv[1:] )
    sys.exit( total_stat )
    # main


# this simple "if ...main..." allows for taking advantage of *experimenting
# with* the optimization (or even just the plain) byte compiled file via:
#    python -OO -c 'import rgang;rgang.main()' -nn all 'echo hi'
# and/or a small script:
#    #!/bin/sh
#    exec python -OO -c "
#    import sys;sys.argv[0]='`basename $0`';import rgang;rgang.main()" "$@"
if __name__ == "__main__": main()
