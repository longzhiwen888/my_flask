# 我自己的flask项目

国际化模板
---------
* 1.收集需要翻译的信息:
    在项目根目录运行 "pybabel extract -F babel.cfg -o messages.pot ."
* 2.创建中文翻译(如果曾经创建过中文翻译，此步骤省略，否则会覆盖掉之前写好的翻译文件)：
    pybabel init -i messages.pot -d ./journey/translations -l zh_Hans_CN
* 3.代码或者模板变动后，可以在步骤1收集完信息后，直接执行此步骤，将变动更新到对应目录的messages.po文件：
   pybabel update -i messages.pot -d ./journey/translations
* 4.将上一步生成的文件翻译好，然后运行编译命令:
    pybabel compile -d ./journey/translations

注意：步骤2每种语言只执行一次就好了，第二次执行会覆盖掉之前写好的翻译，所以第二次执行要跳过步骤2直接步骤3
