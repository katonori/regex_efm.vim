if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

if exists("g:load_regex_efm")
    finish
endif
let g:load_regex_efm = 1

if !exists("g:regex_efm_config")
    let g:regex_efm_config = ['', [1, 2, 3], '']
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
            \ :let g:regex_efm_config = ['[0-9]+>(.+)\(([0-9]+)(,[0-9]+)?\):(.+$)', [1, 2, 4], ''] |
            \ execute(":REefm " . <f-args>)
command! -nargs=0 -complete=file REefmVSC 
            \ :let g:regex_efm_config = ['[0-9]+>(.+)\(([0-9]+)(,[0-9]+)?\):(.+$)', [1, 2, 4], ''] |
            \ execute(":REefmC")
command! -nargs=1 -complete=file REefmMK 
            \ :let g:regex_efm_config = ["(.+):([0-9]+):(.+$)", [1, 2, 3], "make.+Entering directory [`'](.+)'"] |
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
    lines = regex_efm.ParseErrorLogFromFile(logfile,
        vim.eval("g:regex_efm_config[0]"),
        vim.eval("g:regex_efm_config[1]"),
        vim.eval("g:regex_efm_config[2]"))
    fn = vim.eval("s:tmpFile")
    f = open(fn, "w")
    for l in lines:
        l = l.replace("\n", "")
        l = l.replace("\r", "")
        f.write(l + "\n")
    f.close()
    vim.command("setlocal errorformat=%f:%l:%m")
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
    lines = regex_efm.ParseErrorLog(vim.eval('@*').split("\n"),
        vim.eval("g:regex_efm_config[0]"),
        vim.eval("g:regex_efm_config[1]"),
        vim.eval("g:regex_efm_config[2]"))
    fn = vim.eval("s:tmpFile")
    f = open(fn, "w")
    for l in lines:
        l = l.replace("\n", "")
        l = l.replace("\r", "")
        f.write(l + "\n")
    f.close()
    vim.command("setlocal errorformat=%f:%l:%m")
    vim.command("cgetfile " + fn)
    vim.command("cwin ")
# run
func()

EOF
endfunction

