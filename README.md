# visualized_laws


visualized law system.describe complexity about laws. useing graph.

# 各種ツール

## 配色ツールの使いかた

### 概要

配色ツールは、[gephi-toolkit](https://gephi.org/toolkit/) を使うためにjyhtonで書かれています。
config/config.ymlの設定を読み込んで、 `  刑事: {b: 0.8, h: 0.02, s: 1.0}` のように、配色を決定します。

指定した配色で、svg,pdfが出力されるのでそちらをみて、配色を詰めていきます。

### jythonのインストール

jythonのインストールに関しては、[こちら](http://www.jython.org/downloads.html) を参考にして下さい。[こちら](https://wiki.python.org/jython/InstallationInstructions) を参考にしてインストールしました。その際pipもインストールして下さい。

### ライブラリのインストール

```
jythonのインストールパス/pip2.7 install -r jython_requirements.txt
```

で必要なライブラリが入ります。現在は、`ruamel.yaml==0.14.11` しか利用してません。

### 実行

Makefileが実体になっており、 `make` を実行することで、gexfallにある*.gexfのsvg,pdfに変えます。
出力フォルダ先は`out` になってます。

Makefileに`JYTHON=`にJYTHONの実行パスを含めたjythonを指定して下さい。


