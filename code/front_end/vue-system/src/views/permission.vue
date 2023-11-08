<template>
	<div>
		<div class="button-container">
			<input v-model="userData" placeholder="User Data" />
			<button @click="UserManagement">管理用户</button>
		</div>
		<div class="button-container">
			<input v-model="dataData" placeholder="Data Data" />
			<button @click="DataManagement">管理数据</button>
		</div>
		<div class="button-container">
			<input v-model="crawlerData.name" placeholder="Name" />
			<input v-model="crawlerData.target_url" placeholder="Target URL" />
			<input v-model="crawlerData.schedule" placeholder="Schedule" />
			<input v-model="crawlerData.crawl_rules" placeholder="Crawl Rules" />
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

const username = localStorage.getItem('ms_username');
const adminToken = localStorage.getItem('ms_admintoken');

const url = 'http://127.0.0.1:5000';

export default {
	data() {
    	return {
      		is_loading: false,
      		userData: '', // 用户数据输入
      		dataData: '', // 数据数据输入
      		crawlerData: {
        		name: '',
        		target_url: '',
        		schedule: '',
        		crawl_rules: '',
      	 } // 爬虫数据输入
    };
  },
	methods: {
		async UserManagement() {
			this.is_loading = true;
			const headers = {
				Authorization: adminToken,
			};
			const data = {
				mongo_command: 'dbstats',
				userData: this.userData // 使用用户输入的数据
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
        		this.is_loading = false;
      		}
		},
		async DataManagement() {
			this.is_loading = true;
			const headers = {
				Authorization: adminToken,
			};
			const data = {
				mongo_command: 'dbstats',
				dataData: this.dataData // 使用数据输入的数据
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
        		this.is_loading = false;
      		}
		},
		async SetCrawler() {
			this.is_loading = true;
			const headers = {
				Authorization: adminToken,
			};
			const data = {
				name: this.crawlerData.name, // 使用爬虫数据输入的数据
				target_url: this.crawlerData.target_url,
				schedule: this.crawlerData.schedule,
				crawl_rules: this.crawlerData.crawl_rules
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
        		this.is_loading = false;
      		}
		},
	},
};
</script>

<style scoped>
.button-container {
  margin: 20px;
}

input, button {
  margin-right: 10px;
  margin-bottom: 10px;
}
</style>

<!-- <template>
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

const username = localStorage.getItem('ms_username');
const adminToken = localStorage.getItem('ms_admintoken');

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
</script> -->