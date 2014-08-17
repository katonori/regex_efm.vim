" Copyright (c) 2014, katonori All rights reserved.
" 
" Redistribution and use in source and binary forms, with or without modification, are
" permitted provided that the following conditions are met:
" 
"   1. Redistributions of source code must retain the above copyright notice, this list
"      of conditions and the following disclaimer.
"   2. Redistributions in binary form must reproduce the above copyright notice, this
"      list of conditions and the following disclaimer in the documentation and/or other
"      materials provided with the distribution.
"   3. Neither the name of the katonori nor the names of its contributors may be used to
"      endorse or promote products derived from this software without specific prior
"      written permission.
" 
" THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
" EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
" OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
" SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
" INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
" TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
" BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
" CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
" ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
" DAMAGE.
if exists("g:load_regex_efm")
    finish
endif
let g:load_regex_efm = 1

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

if !exists("g:regex_efm_config")
    let g:regex_efm_config = ''
endif

let s:scriptName = expand('<sfile>:p')
let s:dirName = fnamemodify(s:scriptName, ":h") 
let s:tmpFile = tempname()

"
" define commands
"
command! -nargs=1 -complete=file REefm :call <SID>ParserErrorFromFile(<f-args>)
command! -nargs=0 -complete=file REefmC :call <SID>ParserErrorFromClipboard()
command! -nargs=1 -complete=file REefmVS 
            \ :let g:regex_efm_config = '[0-9]+>(?P<file>.+)\((?P<line>[0-9]+)(,(?P<col>[0-9]+))?\):(?P<msg>.+$)' |
            \ execute(":REefm " . <f-args>)
command! -nargs=0 -complete=file REefmVSC 
            \ :let g:regex_efm_config = '[0-9]+>(?P<file>.+)\((?P<line>[0-9]+)(,(?P<col>[0-9]+))?\):(?P<msg>.+$)' |
            \ execute(":REefmC")
command! -nargs=1 -complete=file REefmMK 
            \ :let g:regex_efm_config = "(?P<file>.+):(?P<line>[0-9]+):(?P<col>[0-9]+):(?P<msg>.+$)|make.+Entering directory [`'](?P<dir>.+)'" |
            \ execute(":REefm " . <f-args>)
command! -nargs=1 -complete=file REefmPY 
            \ :let g:regex_efm_config = '^\s*File\s+"(?P<file>.+)", line (?P<line>[0-9]+), in .+$\s+(?P<msg>.+\n\S+.+|.+$)' |
            \ execute(":REefm " . <f-args>)

"
" run parser
"
function! s:ParserErrorFromFile(logfile)
    if g:regex_efm_config[0] == ""
        echo "Error: set g:regex_efm_config correctlly"
        finish
    endif
python << EOF
# add script directory to search path
import vim, sys
sys.path.append(vim.eval("s:dirName"))
import regex_efm

def func():
    logfile = vim.eval("a:logfile")
    lines = regex_efm.ParseErrorLogFromFile(logfile, vim.eval("g:regex_efm_config"))
    fn = vim.eval("s:tmpFile")
    f = open(fn, "w")
    for l in lines:
        l = l.replace("\n", "")
        l = l.replace("\r", "")
        f.write(l + "\n")
    f.close()
    vim.command("setlocal errorformat=%f:%l:%c:%m")
    vim.command("cgetfile " + fn)
    vim.command("cwin ")
# run
func()

EOF
endfunction

"
" run parser
"
function! s:ParserErrorFromClipboard()
    if g:regex_efm_config[0] == ""
        echo "Error: set g:regex_efm_config correctlly"
        finish
    endif
python << EOF
# add script directory to search path
import vim, sys
sys.path.append(vim.eval("s:dirName"))
import regex_efm

def func():
    lines = regex_efm.ParseErrorLog(vim.eval('@*'), vim.eval("g:regex_efm_config"))
    fn = vim.eval("s:tmpFile")
    f = open(fn, "w")
    for l in lines:
        l = l.replace("\n", "")
        l = l.replace("\r", "")
        f.write(l + "\n")
    f.close()
    vim.command("setlocal errorformat=%f:%l:%c:%m")
    vim.command("cgetfile " + fn)
    vim.command("cwin ")
# run
func()

EOF
endfunction

