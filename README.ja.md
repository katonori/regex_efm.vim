regex\_efm.vim
==========
このプラグインはvimのerrorformatを正規表現で設定するためのものです。
私のように正規表現なら理解できるが、vimのerrorformatの文法をよく知らない
という方々のためのものです。

使い方
==========
変数 "g:regex\_efm\_config" にpythonの正規表現でerrorformatを設定し、
下記の通りコマンドを実行します。

        :REefmMake

        もしくは 

        :REefm file.log

そうするとファイルがパースされ、その結果検出されたエラー箇所がロードされ
quickfixバッファーが開かれます。

正規表現の文法
----------
errorformatの指定にはpythonの正規表現で使用できる文法が指定できます。
が、vim plugin に対していくつかの情報を正規表現経由で渡す必要があります。
vim pluginに正規表現のどの箇所がどのような情報なのかは、正規表現のグループの
名前を設定することによって指定します。グループ名"file", "line", "msg"はマッチした
グループがファイル名、行番号、エラーメッセージであることを指定します。
さらに、unix makeのようにカレントディレクトリを変更しながら処理するプログラムの
ログを処理する場合には"dir"も指定する必要があります。これはそのマッチしたグループ
がカレントディレクトリであることを指定します。
下記はunix makeでgccを実行したときのログを処理するための設定例です。


        let g:regex\_efm\_config = "(?P<file>.+):(?P<line>[0-9]+):(?P<msg>.+$)|make.+Entering directory [`'](?P<dir>.+)'"


コマンド
==========

* REefmMake
    * :makeを実行し、その結果をg:regex\_efm\_config の内容にしたがって処理し、
      、エラーが検出されたらquickfixウィンドウを開きます。
* REefm file.log
    * g:regex\_efm\_config の内容にしたがいログファイルを処理し、エラーが検出
      されたらquickfixウィンドウを開きます。
* REefmC
    * 入力がクリップボードから得られること以外はREefmと同じです。

いくつかの設定での実行をプリセットとしてコマンド定義してあります。

* REefmVS 
    * 下記の通り g:regex\_efm\_config を設定し、REefm を実行します。
      これは Visual Studio C++ のエラーログを処理するための設定です。

                '[0-9]+>(?P<file>.+)\((?P<line>[0-9]+)(,[0-9]+)?\):(?P<msg>.+$)' 
* REefmVSC 
    * 下記の通り g:regex\_efm\_config を設定し、REefmC を実行します。
      これは Visual Studio C++ のエラーログを処理するための設定です。

                '[0-9]+>(?P<file>.+)\((?P<line>[0-9]+)(,[0-9]+)?\):(?P<msg>.+$)'
* REefmMK 
    * 下記の通り g:regex\_efm\_config を設定し、REefm を実行します。
      これは unix make で gcc を実行した場合のエラーログを処理するための設定です。
      
                "(?P<file>.+):(?P<line>[0-9]+):(?P<msg>.+$)|make.+Entering directory [`'](?P<dir>.+)'"
* REefmPY 
    * 下記の通り g:regex\_efm\_config を設定し、REefm を実行します。
      これはpythonスクリプトのエラーログを処理するための設定です。
      
                '^\s*File\s+"(?P<file>.+)", line (?P<line>[0-9]+), in .+$\s+(?P<msg>.+\n\S+.+|.+$)'

