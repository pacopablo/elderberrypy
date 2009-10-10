function! s:LoadPythonFiles()
setlocal ff=unix
setlocal sw=4
setlocal ts=4
setlocal sts=4
setlocal expandtab
highlight WhiteSpaceEOL ctermbg=lightgreen guibg=#303050
match WhiteSpaceEOL /\s\+$/
endfunction

function! s:LoadSrcFiles()
setlocal ff=unix
highlight WhiteSpaceEOL ctermbg=lightgreen guibg=#303050
match WhiteSpaceEOL /\s\+$/
endfunction

filetype plugin on
autocmd FileType python call s:LoadPythonFiles()
autocmd FileType make,c,cpp,cmake call s:LoadSrcFiles()
