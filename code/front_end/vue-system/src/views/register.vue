<template>
    <div class="registration-wrap">
      <div class="ms-headbar"></div>
      <div class="ms-login">
        <div class="ms-title">注册账号</div>
        <!-- 注册表单 -->
        <el-form :model="registerParam" :rules="registrationRules" ref="register" label-width="0px" class="ms-content">
          <el-form-item prop="username">
            
            <el-input v-model="registerParam.username" placeholder="用户名">
            </el-input>
          </el-form-item>
          <el-form-item prop="email">
            <el-input v-model="registerParam.email" placeholder="邮箱">
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            
            <el-input
              type="password"
              placeholder="密码"
              v-model="registerParam.password"
            >
            </el-input>
          </el-form-item>
          <el-form-item prop="confirmPassword">
            
            <el-input
              type="password"
              placeholder="确认密码"
              v-model="registerParam.confirmPassword"
            >
            </el-input>
            <el-form-item prop="confirmPassword">
              <span v-show="registerParam.password !== registerParam.confirmPassword" class="password-mismatch">密码不匹配</span>
            </el-form-item>
          </el-form-item>
          <div class="register-btn">
            <el-button type="primary" @click="submitForm('register')">确认注册</el-button>
          </div>
        </el-form>
        <div>
          <transition name="fade">
            <loading v-if="is_loading"></loading>
          </transition>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive } from 'vue';
  import { ElMessage } from 'element-plus';
  import { Lock, User } from '@element-plus/icons-vue';
  import { useRouter } from 'vue-router';
  import { usePermissStore } from '../store/permiss';
  import type { FormInstance, FormRules } from 'element-plus';
  import axios from 'axios';
  
  interface RegistrationInfo {
    username: string;
    email: string;
    password: string;
    confirmPassword: string;
  }
  
  const router = useRouter();
  const registerParam = reactive<RegistrationInfo>({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  
  const is_loading = ref(false);
  const registrationRules: FormRules = {
    username: [
      {
        required: true,
        message: '请输入用户名',
        trigger: 'blur'
      }
    ],
    email: [
      {
        required: true,
        message: '请输入邮箱',
        trigger: 'blur'
      },
      {
        type: 'email',
        message: '请输入有效的邮箱地址',
        trigger: 'blur'
      }
    ],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
    confirmPassword: [
      {
        required: true,
        message: '请确认密码',
        trigger: 'blur'
      },
      {
        validator: (rule, value) => {
          if (value !== registerParam.password) {
            return '密码不匹配';
          }
          return true;
        },
        trigger: 'blur'
      }
    ]
  };
  
  const permiss = usePermissStore();
  
  const register = ref<FormInstance>();
  
  const url = 'http://127.0.0.1:5000';
  
  const submitForm = (formType: 'register') => {
    const formEl = register.value;
    
    if (!formEl) return;
    
    formEl.validate((valid: boolean) => {
      if (valid) {
        is_loading.value=true;
        const requestData = {
          username: registerParam.username,
          email: registerParam.email,
          password: registerParam.password,
          confirmPassword: registerParam.confirmPassword
        };
        axios
          .post(url + '/auth/register', requestData)
          .then((response) => {
            console.log('POST请求成功', response.data);
            ElMessage.success('注册成功，请登录');
            router.push('/login');
          })
          .catch((error) => {
            if(error.response.status===400){
            console.error('POST请求失败', error);
            ElMessage.error('注册失败，用户名已存在');
            }
            else{
              ElMessage.error('请检查网络连接！');
            }
          })
          .finally(() =>{
            is_loading.value=false;
          });
      }
      else {
        ElMessage.error('请检查表单输入');
      }
    });
  };
  const goToLoginPage = () => {
    router.push('/login');
  };
  </script>
  


<style scoped>
.registration-wrap {
	position: relative;
	width: 100%;
	height: 100%;
	background-image: url(../assets/img/login-bg.jpg);
	background-size: 100%;
}
.ms-title {
	width: 100%;
	line-height: 50px;
	text-align: center;
	font-size: 20px;
	color: #fff;
	border-bottom: 1px solid #ddd;
}
.ms-login {
	position: absolute;
	left: 50%;
	top: 50%;
	width: 350px;
	margin: -190px 0 0 -175px;
	border-radius: 5px;
	background: rgba(255, 255, 255, 0.3);
	overflow: hidden;
}
.ms-content {
	padding: 30px 30px;
}
.login-btn {
	text-align: center;
}
.login-btn button {
	width: 100%;
	height: 36px;
	margin-bottom: 10px;
}
.register-btn {
	text-align: center;
}
.register-btn button {
	width: 100%;
	height: 36px;
	margin-bottom: 10px;
}
.login-tips {
	font-size: 12px;
	line-height: 30px;
	color: #fff;
}
.headbar-btn-user{
	width:60px;
	height:36px;
	text-align: center;
	position: absolute;
	left: 50%;
	top: 50%;
	color: #fff;
}

.ms-headbar{
	width: 100%;
	height : 40px;
}

.password-mismatch {
  color: red;
  font-size: 12px;
}
</style>