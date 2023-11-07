<template>
	<div>
		<div>
			<button @click="UserManagement">管理用户</button>
		</div>
		<div>
			<button @click="DataManagement">管理数据</button>
		</div>
		<div>
			<button @click="SetCrawler">设置爬虫</button>
		</div>
		<div>
			<transition name="fade">
				<loading v-if="is_loading"></loading>
			</transition>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import Loading from "../components/Loading.vue"
import { ElMessage } from 'element-plus';

const username = localStorage.getItem('ms_username'); // 替换为你的用户名
const adminToken = localStorage.getItem('ms_admintoken');; // 替换为你的管理员令牌

const url = 'http://127.0.0.1:5000';

export default {
	data() {
    	return {
      		is_loading: false, // 初始化 is_loading 为 false
    	};
  	},
	methods: {
		async UserManagement() {
			this.is_loading = true;
			// const url = `http://127.0.0.1:5000/admin/user-management/${username}`;
			const headers = {
				Authorization: adminToken,
			};
			const data = {
				mongo_command: 'dbstats',
			};

			try {
				const response = await axios.post(`${url}/admin/user-management/${username}`, data, { headers });
				if (response.status === 200) {
					ElMessage.success('处理成功');
				}
				else {
					ElMessage.error('未知错误');
				}
			}
			catch (error) {
				if (error.response && error.response.status === 400) {
					ElMessage.error('JSON格式错误');
				}
				else if(error.response && error.response.status === 401) {
					ElMessage.error('无权限');
				}
				else {
					ElMessage.error('请检查网络连接！');
				}
			}
			finally {
        		this.is_loading = false; // 无论请求成功或失败，都设置为 false
      		}
		},
		async DataManagement() {
			this.is_loading = true;
			// const username = 'wyz'; // 替换为你的用户名
			// const adminToken = 'da1bf34c4b998981979423329e1efd163881a59d36953faaf917dfe2db25adee'; // 替换为你的管理员令牌
			//const url = `http://127.0.0.1:5000/admin/data-management/${username}`;
			const headers = {
				Authorization: adminToken,
			};
			const data = {
				mongo_command: 'dbstats',
			};

			try {
				const response = await axios.post(`${url}/admin/data-management/${username}`, data, { headers });
				if (response.status === 200) {
					ElMessage.success('处理成功');
				}
				else {
					ElMessage.error('未知错误');
				}
			}
			catch (error) {
				if (error.response && error.response.status === 400) {
					ElMessage.error('JSON格式错误');
				}
				else if(error.response && error.response.status === 401) {
					ElMessage.error('无权限');
				}
				else {
					ElMessage.error('请检查网络连接！');
				}
			}
			finally {
        		this.is_loading = false; // 无论请求成功或失败，都设置为 false
      		}
		},
		async SetCrawler() {
			this.is_loading = true;
			// const username = 'wyz'; // 替换为你的用户名
			// const adminToken = 'da1bf34c4b998981979423329e1efd163881a59d36953faaf917dfe2db25adee'; // 替换为你的管理员令牌
			//const url = `http://127.0.0.1:5000/admin/data-management/${username}`;
			const headers = {
				Authorization: adminToken,
			};
			const data = {
				"name":"test",
				"target_url":"www.baidu.com",
				"schedule":"0 0 * * *",
				"crawl_rules":"tags"
			};

			try {
				const response = await axios.post(`${url}/admin/set-crawler/${username}`, data, { headers });
				if (response.status === 200) {
					ElMessage.success('处理成功! '+' Task ID: '+ response.data.task_id);
				}
				else {
					ElMessage.error('未知错误');
				}
			}
			catch (error) {
				if (error.response && error.response.status === 400) {
					ElMessage.error('JSON格式错误');
				}
				else if(error.response && error.response.status === 401) {
					ElMessage.error('无权限');
				}
				else {
					ElMessage.error('请检查网络连接！');
				}
			}
			finally {
        		this.is_loading = false; // 无论请求成功或失败，都设置为 false
      		}
		},
	},
};
</script>
<!--   
<script setup lang="ts" name="permission">
import { ref } from 'vue';
import { ElTree } from 'element-plus';
import { usePermissStore } from '../store/permiss';

const role = ref<string>('admin');

interface Tree {
	id: string;
	label: string;
	children?: Tree[];
}

const data: Tree[] = [
	{
		id: '1',
		label: '系统首页'
	},
	{
		id: '2',
		label: '基础表格',
		children: [
			{
				id: '15',
				label: '编辑'
			},
			{
				id: '16',
				label: '删除'
			}
		]
	},
	{
		id: '3',
		label: 'tab选项卡'
	},
	{
		id: '4',
		label: '表单相关',
		children: [
			{
				id: '5',
				label: '基本表单'
			},
			{
				id: '6',
				label: '文件上传'
			},
			{
				id: '7',
				label: '三级菜单',
				children: [
					{
						id: '8',
						label: '富文本编辑器'
					},
					{
						id: '9',
						label: 'markdown编辑器'
					}
				]
			}
		]
	},
	{
		id: '10',
		label: '自定义图标'
	},
	{
		id: '11',
		label: 'schart图表'
	},

	{
		id: '13',
		label: '权限管理'
	},
	{
		id: '14',
		label: '支持作者'
	}
];

const permiss = usePermissStore();

// 获取当前权限
const checkedKeys = ref<string[]>([]);
const getPremission = () => {
	// 请求接口返回权限
	checkedKeys.value = permiss.defaultList[role.value];
};
getPremission();

// 保存权限
const tree = ref<InstanceType<typeof ElTree>>();
const onSubmit = () => {
	// 获取选中的权限
	console.log(tree.value!.getCheckedKeys(false));
};

const handleChange = (val: string[]) => {
	tree.value!.setCheckedKeys(permiss.defaultList[role.value]);
};
</script>

<style scoped>
.tree-wrapper {
	max-width: 500px;
}
.label {
	font-size: 14px;
}
</style> -->
