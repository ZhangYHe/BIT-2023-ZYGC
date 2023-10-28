# BIT-2023-ZYGC

#### 1.介绍
BIT 2023 卓越工程综合训练 小组作业

#### 2.软件架构
软件架构说明


#### 3.安装教程

##### 3.1 Database Config

- MongoDB
- MondoDB: Compass
- Username: admin
- Password: 12345678
- Database: Scholar
- Roles: readWrite
- 公网uri
  ```
  mongodb://admin:202309@64.176.214.218:27017/?authMechanism=DEFAULT
  ```

##### 3.2 vue config

1.  Project setup
    ```
    cd .\code\front_end\vue-system\
    npm install
    ```

2.  Compiles and hot-reloads for development
    ```
    npm run dev
    ```
3.  Compiles and minifies for production
    ```
    npm run build
    ```
4.  Lints and fixes files
    ```
    npm run lint
    ```

##### 3.3 backend config

1.  Project setup
    ```
    cd .\code\back_end\
    conda create -n scrapy_env python=3.8
    conda activate scrapy_env
    pip install -r requirements.txt
    ```

2.  
    ```
    python python app.py
    ```

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


