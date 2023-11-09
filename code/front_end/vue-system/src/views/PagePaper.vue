<template>
    <div class="paper-details">
      <h2>{{ paper['*title'] }}</h2>
      <p>Authors: 
        <span v-for="(author, index) in paper['*authors']" :key="index">
          <router-link :to="`/information/authors/${author.id}`">
            {{ author['name'] }}{{ index < paper['*authors'].length - 1 ? ', ' : '' }}
          </router-link>
        </span>
      </p>
      
      <p>Abstract:</p>
      <p class="abstract">{{ paper['*abstract'] }}</p>
      <p>Publication Date: {{ paper['*date'] }} {{ paper['*year'] }}</p>
      <p>DOI: <a :href="paper['*doi']" target="_blank">{{ paper['*doi'] }}</a></p>
      <p>Venue: {{ paper['*venue'] }}</p>
      <p>PDF: <a :href="paper['*pdf']" target="_blank">Download PDF</a></p>
      <button>
        <router-link :to="`/visualization/paper/${paper['_id']}`">Go to Paper Visualization</router-link>
      </button>
      <p><button @click="sendRequest">收藏</button></p>
      <div>
        <transition name="fade">
          <loading v-if="is_loading"></loading>
        </transition>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { ElMessage } from 'element-plus';
  import Loading from "../components/Loading.vue"
  import axios from 'axios';
  
  export default {
    data() {
      return {
        paper: {
          '*title': '',
          '*authors': [],
          '*abstract': '',
          '*date': '',
          '*doi': '',
          '*venue': '',
          '*year': '',
          '*pdf': '',
          '_id':'',
        },
        is_loading:true,
      };
    },
    mounted() {
      // this.is_loading = true;
      this.getPaperDetails();
    },
    methods: {
      getPaperDetails() {
        const paperId = this.$route.params.paper_id;
        const url = `http://127.0.0.1:5000/information/papers/${paperId}`;
        axios.get(url)
          .then((response) => {
            //ElMessage.success(paperId);
            // this.is_loading = false;
            this.paper = response.data;
          })
          .catch((error) => {
            //ElMessage.success('失败');
            // this.is_loading = false;
            ElMessage.error('请求失败，请检查网络连接！');
            console.error('Failed to fetch paper details:', error);
          })
          .finally(() => {
            // 无论请求成功还是失败，都将 is_loading 设置为 false
            this.is_loading = false;
          });
      },
      sendRequest() {
        const paperId = this.$route.params.paper_id;
        const params = {
          userId : localStorage.getItem('ms_userid'),
          collection_id : paperId,
        };
        console.log(params);
        axios.get(`http://127.0.0.1:5000/collection/user/collect`,{params})
          .then(response => {
            // 请求成功处理逻辑
            console.log(response.data);
          })
          .catch(error => {
            // 请求失败处理逻辑
            console.error(error);
            if (error.response && error.response.status === 401) {
              // 显示收藏文献已存在的提示
              ElMessage.error("该文献已收藏");
            }
            
          });
      }
    },
  };
  </script>
  
  <style scoped>
  .paper-details {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f8f8f8;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  h2 {
    font-size: 24px;
  }
  
  p {
    margin: 10px 0;
  }
  
  .abstract {
    white-space: pre-line;
  }
  </style>
  