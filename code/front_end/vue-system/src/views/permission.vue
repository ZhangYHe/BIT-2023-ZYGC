<!-- 
<template>
	<div>
	  <h2>管理数据</h2>
	  <div class="button-container">
		<select v-model="dataData.operation_type" @change="handleOperationChange">
		  <option value="" disabled>请选择操作类型</option>
		  <option value="modify">Modify</option>
		  <option value="insert">Insert</option>
		  <option value="delete">Delete</option>
		</select>
		<input v-model="dataData.collection" placeholder="collection(example:users)" />
		<div v-if="dataData.operation_type === 'modify'">
		  <input v-model="dataData.modifyQueryObject" placeholder="QueryObject(ex:username)" />
		  <input v-model="dataData.modifyQueryValue" placeholder="QueryValue(ex:new_user)" />
		  <input v-model="dataData.modifyUpdateObject" placeholder="UpdateObject(ex:is_admin)" />
		  <input v-model="dataData.modifyUpdateValue" placeholder="UpdateValue(ex:true)" />
		</div>
		<div v-if="dataData.operation_type === 'insert'">
		  <input v-model="dataData.insertDocuments" class="input1" placeholder='Documents(example:[{"username": "new_user1", "password": "hashed_password1", "is_admin": false},{"username": "new_user2", "password": "hashed_password2", "is_admin": true}])' />
		</div>
		<div v-if="dataData.operation_type === 'delete'">
		  <input v-model="dataData.deleteObjectId" placeholder="Object ID" />
		</div>
		<button @click="DataManagement" :disabled="!isDataManagementButtonEnabled">确认修改</button>
	  </div>
  
	  <h2>管理数据</h2>
	  <div class="button-container">
		<input v-model="crawlerData.name" placeholder="Name" />
		<input v-model="crawlerData.target_url" placeholder="Target URL" />
		<input v-model="crawlerData.schedule" placeholder="Schedule" />
		<input v-model="crawlerData.crawl_rules" placeholder="Crawl Rules" />
		<div>
		  <button @click="SetCrawler" :disabled="!isSetCrawlerButtonEnabled">确认修改</button>
		</div>
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
      		dataData: {
				operation_type: '',
				collection:'',
				modifyQueryObject: '',
				modifyQueryValue: '',
				modifyUpdateObject: '',
				modifyUpdateValue:'',
				insertDocuments: '',
				deleteObjectId: '',
			}, // 数据数据输入
      		crawlerData: {
        		name: '',
        		target_url: '',
        		schedule: '',
        		crawl_rules: '',
      	 } // 爬虫数据输入
    };
  },
	methods: {
		
		handleOperationChange() {
      // Reset additional input fields when operation type changes
      
	  this.dataData.modifyQueryObject= '',
	  this.dataData.modifyQueryValue = '';
      this.dataData.modifyUpdateObject = '';
	  this.dataData.modifyUpdateValue='';
      this.dataData.insertDocuments = '';
      this.dataData.deleteObjectId = '';
    },

		async DataManagement() {
			this.is_loading = true;
			const headers = {
				Authorization: adminToken,
			};

			let data = {};
			switch (this.dataData.operation_type) {
        case 'modify':
          data = {
            mongo_command: {
              operation_type: 'modify',
              modify: {
                collection: this.dataData.collection,
                query: {
                  [this.dataData.modifyQueryObject]: this.dataData.modifyQueryValue,
				  //username: this.dataData.modifyQueryValue,
                },
                update: {
                  $set: {
                    [this.dataData.modifyUpdateObject]: this.dataData.modifyUpdateValue,
                  },
                },
              },
            },
          };
          break;
        case 'insert':
          data = {
            mongo_command: {
              operation_type: 'insert',
              insert: {
                collection: this.dataData.collection,
                documents: JSON.parse(this.dataData.insertDocuments),
              },
            },
          };
          break;
        case 'delete':
          data = {
            mongo_command: {
              operation_type: 'delete',
              delete: {
                collection: this.dataData.collection,
                object_id: this.dataData.deleteObjectId,
              },
            },
          };
          break;
        default:
          data = {
            mongo_command: 'dbstats',
          };
          // Handle other cases or provide a default value
          break;
      }
			try {
				const response = await axios.post(
					`${url}/admin/data-management/${username}`,
					data,
					{ headers }
				);
				if (response.status === 200) {
					ElMessage.success('处理成功');
				}
				else{
					ElMessage.error('处理错误，请检查网络连接');
				}
			}
			catch (error) {
				if(error.response.status === 400){
					ElMessage.error('请检查JSON格式');
				}
				else if(error.response.status === 500){
					ElMessage.error('请正确填写信息');
				}
				else{
					ElMessage.error('处理错误，请检查网络连接');
				}
				// Handle errors
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
	computed: {
    isDataManagementButtonEnabled() {
      // Check if all required fields for DataManagement are filled
      if (this.dataData.operation_type === 'modify') {
        return (
          this.dataData.collection &&
          this.dataData.modifyQueryObject &&
          this.dataData.modifyQueryValue &&
          this.dataData.modifyUpdateObject &&
          this.dataData.modifyUpdateValue
        );
      } else if (this.dataData.operation_type === 'insert') {
        return this.dataData.collection && this.dataData.insertDocuments;
      } else if (this.dataData.operation_type === 'delete') {
        return this.dataData.collection && this.dataData.deleteObjectId;
      }

      // Return false by default if the operation_type is not recognized
      return false;
    },
    isSetCrawlerButtonEnabled() {
      // Check if all required fields for SetCrawler are filled
      return (
        this.crawlerData.name &&
        this.crawlerData.target_url &&
        this.crawlerData.schedule &&
        this.crawlerData.crawl_rules
      );
    },
  },

};
</script> -->
<template>
	<div>
	  <!-- DataManagement Section -->
	  <h2>管理数据/用户</h2>
	  <div class="button-container">
		<select v-model="dataData.operationCollection" @change="handleOperationCollectionChange" class="select1">
		  <option value="" disabled>请选择操作</option>
		  <option value="userManagement">用户管理</option>
		  <option value="dataManagement">数据管理</option>
		</select>
		<select v-model="dataData.collection" class="select1">
		  <option value="" disabled>请选择表</option>
		  <option value="clean_papers" v-if="dataData.operationCollection === 'dataManagement'">clean_papers</option>
		  <option value="authors" v-if="dataData.operationCollection === 'dataManagement'">authors</option>
		  <option value="users" v-if="dataData.operationCollection === 'userManagement'">users</option>
		</select>
		<select v-model="dataData.operation_type" @change="handleOperationChange" class="select1">
		  <option value="" disabled>请选择操作类型</option>
		  <option value="modify">Modify</option>
		  <option value="insert">Insert</option>
		  <option value="delete">Delete</option>
		</select>
		<!-- <div v-if="dataData.operation_type === 'modify'" class="body1"> -->
		  <input v-model="dataData.modifyQueryObject" v-if="dataData.operation_type === 'modify'" class="input1" placeholder="请输入查询属性 (例:username)" />
		  <input v-model="dataData.modifyQueryValue" v-if="dataData.operation_type === 'modify'" class="input1" placeholder="请输入查询的值 (例:new_user)" />
		  <input v-model="dataData.modifyUpdateObject" v-if="dataData.operation_type === 'modify'" class="input1" placeholder="请输入修改属性 (例:is_admin)" />
		  <input v-model="dataData.modifyUpdateValue" v-if="dataData.operation_type === 'modify'" class="input1" placeholder="请输入修改的值 (例:true)" />
		<!-- </div> -->
		<!-- <div v-if="dataData.operation_type === 'insert'" class="body1"> -->
			
			<!-- <textarea v-model="dataData.insertDocuments" v-if="dataData.operation_type === 'insert'" class="textarea2" placeholder='请输入要插入内容的JSON格式(example:[{"username": "new_user1", "password": "hashed_password1", "is_admin": false},{"username": "new_user2", "password": "hashed_password2", "is_admin": true}])'></textarea> -->

		  <el-input v-model="dataData.insertDocuments" type="textarea" rows="4" v-if="dataData.operation_type === 'insert'" class="input2" placeholder='请输入要插入内容的JSON格式，例如：
[{"username": "new_user1", "password": "password1", "is_admin": false},
 {"username": "new_user2", "password": "password2", "is_admin": true}]' />
		
		  <!-- </div> -->
		<!-- <div v-if="dataData.operation_type === 'delete'" class="body1"> -->
		  <input v-model="dataData.deleteObjectId" v-if="dataData.operation_type === 'delete'" class="input3" placeholder="请输入要删除内容的Object ID" />
		<!-- </div> -->
		<button @click="DataManagement" :disabled="!isDataManagementButtonEnabled">确认修改</button>
	  </div>
  
	  <!-- SetCrawler Section -->
	  <h2>管理爬虫</h2>
	  <div class="button-container">
		<input v-model="crawlerData.name" class="input4" placeholder="Name" />
		<input v-model="crawlerData.target_url" class="input4" placeholder="Target URL" />
		<input v-model="crawlerData.schedule" class="input4" placeholder="Schedule" />
		<input v-model="crawlerData.crawl_rules" class="input4" placeholder="Crawl Rules" />
		<!-- <div> -->
		  <button @click="SetCrawler" :disabled="!isSetCrawlerButtonEnabled">确认修改</button>
		<!-- </div> -->
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
		dataData: {
		  operationCollection: '',
		  operation_type: '',
		  collection: '',
		  modifyQueryObject: '',
		  modifyQueryValue: '',
		  modifyUpdateObject: '',
		  modifyUpdateValue: '',
		  insertDocuments: '',
		  deleteObjectId: '',
		}, // 数据数据输入
		crawlerData: {
		  name: '',
		  target_url: '',
		  schedule: '',
		  crawl_rules: '',
		} // 爬虫数据输入
	  };
	},
	methods: {
  
	  handleOperationChange() {
		// Reset additional input fields when operation type changes
		this.dataData.modifyQueryObject = '';
		this.dataData.modifyQueryValue = '';
		this.dataData.modifyUpdateObject = '';
		this.dataData.modifyUpdateValue = '';
		this.dataData.insertDocuments = '';
		this.dataData.deleteObjectId = '';
	  },
  
	  handleOperationCollectionChange() {
		// Reset dataData properties when operation collection changes
		this.dataData.collection = '';
		this.dataData.operation_type = '';
		this.handleOperationChange(); // Reset operation-specific fields
	  },
  
	  async DataManagement() {
		this.is_loading = true;
		const headers = {
		  Authorization: adminToken,
		};
  
		let data = {};
		switch (this.dataData.operation_type) {
		  case 'modify':
			data = {
			  mongo_command: {
				operation_type: 'modify',
				modify: {
				  collection: this.dataData.collection,
				  query: {
					[this.dataData.modifyQueryObject]: this.dataData.modifyQueryValue,
				  },
				  update: {
					$set: {
					  [this.dataData.modifyUpdateObject]: this.dataData.modifyUpdateValue,
					},
				  },
				},
			  },
			};
			break;
		  case 'insert':
			data = {
			  mongo_command: {
				operation_type: 'insert',
				insert: {
				  collection: this.dataData.collection,
				  documents: JSON.parse(this.dataData.insertDocuments),
				},
			  },
			};
			break;
			//[{"username": "new_user","password": "hashed_password","is_admin": false}]
		  case 'delete':
			data = {
			  mongo_command: {
				operation_type: 'delete',
				delete: {
				  collection: this.dataData.collection,
				  object_id: this.dataData.deleteObjectId,
				},
			  },
			};
			break;
		  default:
			data = {
			  mongo_command: 'dbstats',
			};
			// Handle other cases or provide a default value
			break;
		}
		try {
		  const response = await axios.post(
			`${url}/admin/data-management/${username}`,
			data,
			{ headers }
		  );
		  if (response.status === 200) {
			ElMessage.success('处理成功');
		  } else {
			ElMessage.error('处理错误，请检查网络连接');
		  }
		} catch (error) {
		  if (error.response.status === 400) {
			ElMessage.error('请检查JSON格式');
		  } else if (error.response.status === 500) {
			ElMessage.error('请正确填写信息');
		  } else {
			ElMessage.error('处理错误，请检查网络连接');
		  }
		  // Handle errors
		} finally {
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
	computed: {
	  isDataManagementButtonEnabled() {
		// Check if all required fields for DataManagement are filled
		if (this.dataData.operation_type === 'modify') {
		  return (
			this.dataData.collection &&
			this.dataData.modifyQueryObject &&
			this.dataData.modifyQueryValue &&
			this.dataData.modifyUpdateObject &&
			this.dataData.modifyUpdateValue
		  );
		} else if (this.dataData.operation_type === 'insert') {
		  return this.dataData.collection && this.dataData.insertDocuments;
		} else if (this.dataData.operation_type === 'delete') {
		  return this.dataData.collection && this.dataData.deleteObjectId;
		}
  
		// Return false by default if the operation_type is not recognized
		return false;
	  },
	  isSetCrawlerButtonEnabled() {
		// Check if all required fields for SetCrawler are filled
		return (
		  this.crawlerData.name &&
		  this.crawlerData.target_url &&
		  this.crawlerData.schedule &&
		  this.crawlerData.crawl_rules
		);
	  },
	},
  };
  </script>


 <style>
  body {
   margin: 0;
   padding: 0;
   display: flex;
   justify-content: center;
   align-items: center;
   min-height: 100vh;
   background-color: #f4f4f4;
 } 

 .button-container {
   display: flex;
   flex-wrap: wrap;
   justify-content: space-between;
   align-items: center;
   max-width: 800px; /* Adjust the maximum width as needed */
   margin: 0 auto;
 }

 .select1 {
   width: calc(33.33% - 10px); /* Adjust the width as needed */
   margin-bottom: 10px;
   height: 30px;
   font-size: large;
   text-align: center;
 }

 .input1 {
   width: calc(50% - 10px); /* Adjust the width as needed */
   margin-bottom: 10px;
   height: 30px;
   font-size: large;
   text-align: center;
 }

 .input2 {
   width: 100%;
   margin-bottom: 15px;
   height: 100px;
   font-size: medium;
   resize: vertical;
 	 text-align: left; 
 }
 /* .textarea2 {
  width: 100%;
  margin-bottom: 10px;
  height: 80px;
  font-size: large;
  resize: vertical; 
  text-align: left; 
} */

 .input3 {
   width: 100%;
   margin-bottom: 10px;
   height: 30px;
   font-size: large;
   text-align: center;
 }

 .input4 {
   width: calc(50% - 10px); /* Adjust the width as needed */
   margin-bottom: 10px;
   height: 30px;
   font-size: large;
   height: 30px;
   font-size: large;
   text-align: center;
 }

 button {
   width: 100%;
   /* margin-left:33%; */
   padding: 10px;
   box-sizing: border-box;
   margin-bottom: 20px;
   font-size: large;
 }

 h2 {
   text-align: center;
   margin-top: 20px;
   margin-bottom: 20px;
 }

 /* Add any additional styling as needed */
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