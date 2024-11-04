# 环境准备

```
sudo pip3 install django

pip3 install pymysql

pip3 install mutagen

pip3 install xattr

```

## 安装数据库 

```
brew install mysql 
```

## 同步数据库数据 

## 启动数据库 

```
brew service start mysql
```

# 启动项目 

```
python3 manager.py runserver 127.0.0.1:5566
```

# 验证启动成功 

1. 访问：127.0.0.1:5566/test 

2. 页面显示 Hello World 

# 验证基本传参 

1. 访问：127.0.0.1:5566/test2 

# 验证参数传递和JSON返回值 

1. 访问：127.0.0.1:5566/test3?msg=hello


# 验证参数传递

1. 访问：127.0.0.1:5566/test4/fty/123 
