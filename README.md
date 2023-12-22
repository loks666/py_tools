# py_tools
### 分享自己写的一些小工具

---
### backup[备份数据到百度云]
<pre>
└─backup  
        backup_by_BaiDuYun.py  ====>    备份halo博客，mysql，redis上传到百度云
        requirements.txt       ====>    依赖文件
</pre>
### 前置工作
<pre>
需要在你的win或者mac下安装bypy(百度云python客户端)，需要你有python环境
pip install bypy
bypy list
</pre>
执行`bypy list`之后会给你一个链接，点击链接，在浏览器打开，复制那个代码，粘贴进命令行当中，回车确认  
然后会在你的用户目录生成一个.bypy的文件夹，里面是你的登录信息，一般一个月过期一次  
如果你想要在服务器使用，则把.bypy上传到你服务器的用户路径  
`windows =====>  C:\Users\用户\{用户名}\.bypy`  
`linux =======>  cd ~  (一般情况下波浪线就是用户目录，等价于/root)`
### 然后修改代码里的地址和端口号，运行如下代码
<pre>
cd backup
pip install -r requirements.txt
python backup_by_BaiDuYun.py
</pre>