<template>
	<div>
		<el-row :gutter="20">
			<el-col :span="12">
				<el-card shadow="hover">
					<template #header>
						<div class="clearfix">
							<span>基础信息</span>
						</div>
					</template>
					<div class="info">
						<div class="info-image" @click="showDialog">
							<el-avatar :size="100" :src="avatarImg" />
							<span class="info-edit">
								<i class="el-icon-lx-camerafill"></i>
							</span>
						</div>
						<div class="info-name">{{ name }}</div>
						<div class="info-desc">{{form.desc}}</div>
					</div>
				</el-card>
			</el-col>
			<el-col :span="12">
				<el-card shadow="hover">
					<template #header>
						<div class="clearfix">
							<span>账户编辑</span>
						</div>
					</template>
					<el-form label-width="90px">
						<el-form-item label="用户名："> {{ name }} </el-form-item>
						<el-form-item label="旧密码：" v-if="form.new">
							<el-input type="password" v-model="form.old"></el-input>
						</el-form-item>
						<el-form-item label="修改密码：">
							<el-input type="password" v-model="form.new"></el-input>
						</el-form-item>
						
						<el-form-item label="个人邮箱：">
							<el-input v-model="form.email"></el-input>
						</el-form-item>
						<el-form-item label="个人简介：">
							<el-input v-model="form.desc"></el-input>
						</el-form-item>
						<el-form-item>
							<el-button type="primary" @click="onSubmit">保存</el-button>
						</el-form-item>
					</el-form>
				</el-card>
			</el-col>
		</el-row>
		<el-dialog title="裁剪图片" v-model="dialogVisible" width="600px">
			<vue-cropper
				ref="cropper"
				:src="imgSrc"
				:ready="cropImage"
				:zoom="cropImage"
				:cropmove="cropImage"
				style="width: 100%; height: 400px"
			></vue-cropper>

			<template #footer>
				<span class="dialog-footer">
					<el-button class="crop-demo-btn" type="primary"
						>选择图片
						<input class="crop-input" type="file" name="image" accept="image/*" @change="setImage" />
					</el-button>
					<el-button type="primary" @click="saveAvatar">上传并保存</el-button>
				</span>
			</template>
		</el-dialog>
		<div>
		<transition name="fade">
		  <loading v-if="is_loading"></loading>
		</transition>
	  </div>
	</div>
</template>

<script setup lang="ts" name="user">
import { reactive, ref } from 'vue';
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';
import axios from 'axios'; 
import avatar from '../assets/img/img.jpg';
import { ElMessage } from 'element-plus';
import Loading from "../components/Loading.vue"

const name = localStorage.getItem('ms_username');
const email1 = localStorage.getItem('ms_email');
const intro = localStorage.getItem('ms_intro');
const form = reactive({
	old: '',
	new: '',
	email:email1,
	desc: intro
});

const is_loading = ref(false);
//const onSubmit = () => {};
const onSubmit = async () => {
  is_loading.value = true;

  try {
    const response = await axios.post('http://127.0.0.1:5000/auth/password', {
		username: name,
		password: form.old,
		newpassword: form.new,
		email: form.email,
		intro: form.desc
    });

    if (response.status === 200) {
		const message = response.data.message;
		if (message === 'Password changed successfully') {
			ElMessage.success("密码修改成功！");
			
		}
		else {
			ElMessage.success("信息修改成功！");
		}
		localStorage.setItem('ms_intro',(form.desc===null)?'':form.desc.toString());
		localStorage.setItem('ms_email',(form.email===null)?'':form.email.toString());
    }
  } catch (error) {
    handleErrorResponse(error);
  } finally {
    is_loading.value = false;
  }
};

const handleErrorResponse = (error:unknown) => {
  if ((error as any).response) {
    const status = (error as any).response.status;
    const data = (error as any).response.data;

    if (status === 401) {
      ElMessage.error("密码错误，请检查旧密码！");
    }
	else if (status === 400) {
      ElMessage.error("若需要修改密码，请输入旧密码！");
    }
	else if (status === 402) {
      ElMessage.error("用户未登录，请登录！");
    }
	else {
      ElMessage.error(`请求失败：${status} - ${data.message}`);
    }
  } else if ((error as any).request) {
    ElMessage.error("未收到响应，请检查网络连接！");
  } else {
    ElMessage.error("未知错误，请检查网络连接！");
  }
};

const avatarImg = ref(avatar);
const imgSrc = ref('');
const cropImg = ref('');
const dialogVisible = ref(false);
const cropper: any = ref();
const showDialog = () => {
	dialogVisible.value = true;
	imgSrc.value = avatarImg.value;
};

const setImage = (e: any) => {
	const file = e.target.files[0];
	if (!file.type.includes('image/')) {
		return;
	}
	const reader = new FileReader();
	reader.onload = (event: any) => {
		dialogVisible.value = true;
		imgSrc.value = event.target.result;
		cropper.value && cropper.value.replace(event.target.result);
	};
	reader.readAsDataURL(file);
};

const cropImage = () => {
	cropImg.value = cropper.value.getCroppedCanvas().toDataURL();
};

const saveAvatar = () => {
	avatarImg.value = cropImg.value;
	dialogVisible.value = false;
};
</script>

<style scoped>
.info {
	text-align: center;
	padding: 35px 0;
}
.info-image {
	position: relative;
	margin: auto;
	width: 100px;
	height: 100px;
	background: #f8f8f8;
	border: 1px solid #eee;
	border-radius: 50px;
	overflow: hidden;
}

.info-edit {
	display: flex;
	justify-content: center;
	align-items: center;
	position: absolute;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	opacity: 0;
	transition: opacity 0.3s ease;
}
.info-edit i {
	color: #eee;
	font-size: 25px;
}
.info-image:hover .info-edit {
	opacity: 1;
}
.info-name {
	margin: 15px 0 10px;
	font-size: 24px;
	font-weight: 500;
	color: #262626;
}
.crop-demo-btn {
	position: relative;
}
.crop-input {
	position: absolute;
	width: 100px;
	height: 40px;
	left: 0;
	top: 0;
	opacity: 0;
	cursor: pointer;
}
</style>
