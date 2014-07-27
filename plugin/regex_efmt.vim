if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

if exists("g:load_regex_efmt")
    finish
endif
let g:load_regex_efmt = 1

if !exists("g:regex_efmt_config")
    let g:regex_efmt_config = ['', [1, 2, 3], '']
endif

let s:scriptName = expand('<sfile>:p')
let s:dirName = fnamemodify(s:scriptName, ":h") 
let s:tmpFile0 = tempname()

"
" define commands
"
command! -nargs=1 -complete=file REefmt :call <SID>ParserError(<f-args>)
command! -nargs=1 -complete=file REefmtVS 
            \ :let g:regex_efmt_config = ['1>(.+)\(([0-9]+)\):(.+$)', [1, 2, 3], ''] |
            \ execute(":REefmt " . <f-args>)
command! -nargs=1 -complete=file REefmtMK 
            \ :let g:regex_efmt_config = ["(.+):([0-9]+):(.+$)", [1, 2, 3], "make: Entering directory '(.+)'"] |
            \ execute(":REefmt " . <f-args>)

"
" run parser
"
function! s:ParserError(logfile)
    if g:regex_efmt_config[0] == ""
        echo "Error: set g:regex_efmt_config correctlly"
        finish
    endif
python << EOF
# add script directory to search path
import vim, sys
sys.path.append(vim.eval("s:dirName"))
import regex_efmt

def func():
    logfile = vim.eval("a:logfile")
    lines = regex_efmt.ParseErrorLog(logfile,
    vim.eval("g:regex_efmt_config[0]"),
    vim.eval("g:regex_efmt_config[1]"),
    vim.eval("g:regex_efmt_config[2]"))
    fn = vim.eval("s:tmpFile0")
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

