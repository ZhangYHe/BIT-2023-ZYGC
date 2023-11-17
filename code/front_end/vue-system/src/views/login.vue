<template>
	<div class="login-wrap">
		<div class="ms-headbar"></div>
		<div class="ms-login">
			<div class="ms-title">领域知识调研搜索平台</div>
			<el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content">
				<el-form-item prop="username">
					<el-input v-model="param.username" placeholder="username">
						<template #prepend>
							<el-button :icon="User"></el-button>
						</template>
					</el-input>
				</el-form-item>
				<el-form-item prop="password">
					<el-input
						type="password"
						placeholder="password"
						v-model="param.password"
						@keyup.enter="submitForm(login)"
					>
						<template #prepend>
							<el-button :icon="Lock"></el-button>
						</template>
					</el-input>
				</el-form-item>
				
				<div class="login-btn">
					<el-button type="primary" @click="submitForm(login)">登录</el-button>
				</div>
				<div class="register-btn">
        			<el-button type="primary" @click="goToRegistrationPage()">没有账号？点此注册</el-button>
        		</div>
			</el-form>
		</div>
		<!-- <div>
			<transition name="fade">
				<loading v-if="is_loading"></loading>
			</transition>
		</div> -->
	</div>
	<div>
      <transition name="fade">
        <loading v-if="is_loading"></loading>
      </transition>
    </div>
	<!--<register v-if="isRegistrationPageVisible" @goToLoginPage="goToLoginPage" />-->
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useTagsStore } from '../store/tags';
import { usePermissStore } from '../store/permiss';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { Lock, User } from '@element-plus/icons-vue';
import Loading from "../components/Loading.vue"
import axios from 'axios';
interface LoginInfo {
	username: string;
	password: string;
}

const router = useRouter();
//const isRegistrationPageVisible = ref(false);
const param = reactive<LoginInfo>({
	username: '',
	password: ''
});

const rules: FormRules = {
	username: [
		{
			required: true,
			message: '请输入用户名',
			trigger: 'blur'
		}
	],
	password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
};
const url = 'http://127.0.0.1:5000';
const permiss = usePermissStore();
const login = ref<FormInstance>();
const is_loading = ref(false);
//const register = ref<FormInstance>();
//const is_loading = true;
const goToRegistrationPage = () => {
	//
	router.push('/register');
	//router.push('/dashboard');
	//ElMessage.error('注册');
	//location.reload()
  	//isRegistrationPageVisible.value = true;
};
// const goToLoginPage = () => {
//   isRegistrationPageVisible.value = false;
// };

const submitForm = (formEl: FormInstance | undefined) => {
	if (!formEl) return;
	is_loading.value = true;
	formEl.validate((valid: boolean) => {

		if (valid) {
		// 构建要发送的数据对象
		const requestData = {
			username: param.username,
			password: param.password,
		};
		// 发送POST请求
		axios
			.post(url+'/auth/login', requestData)
			.then((response) => {
			// 请求成功时的处理
				console.log('POST请求成功', response.data);
				ElMessage.success('登录成功');
				//ElMessage.success(response.data.email);
				const now = new Date();
				
				// ElMessage.success(now.getFullYear().toString());
				//ElMessage.success(now.toLocaleDateString()+" "+now.toLocaleTimeString());
				// ElMessage.success(now.getDate().toString());
				localStorage.setItem('time', now.toLocaleDateString()+" "+now.toLocaleTimeString());
				localStorage.setItem('ms_username', param.username);
				localStorage.setItem('ms_userid',response.data.user_id);
				localStorage.setItem('ms_intro',response.data.intro);
				localStorage.setItem('ms_email',response.data.email);
				if(response.data.admin_token){
					localStorage.setItem('ms_admintoken',response.data.admin_token);
				}
				else{
					localStorage.setItem('ms_admintoken','');
				}
				const admin_token = localStorage.getItem('ms_admintoken');
				const keys = permiss.defaultList[admin_token !== '' ? 'admin' : 'user'];
				//const keys = permiss.defaultList[param.username == 'admin' ? 'admin' : 'user'];
				permiss.handleSet(keys);
				localStorage.setItem('ms_keys', JSON.stringify(keys));
				//router.push('/register');
			//登陆成功，跳转到主页面
				router.push('/dashboard');
			})
			.catch((error) => {
			// 请求失败时的处理
				console.error('POST请求失败', error);
				if(error.response && error.response.status===401)
					ElMessage.error('登录失败，请检查用户名和密码！');
				else{
					ElMessage.error('登录失败，请检查网络连接！');
				}
			})
			.finally(() => {
          		is_loading.value = false; // 请求完成后设置为 false，隐藏 Loading 动画
        	});
		}
		else {
			ElMessage.error('请输入用户名和密码');
		}
	});
};

const tags = useTagsStore();
tags.clearTags();
</script>


<style scoped>
.login-wrap {
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
	width: 80%;
	height: 36px;
	margin-bottom: 10px;
}
.register-btn {
	text-align: center;
}
.register-btn button {
	width: 80%;
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
</style>
