<template>
  <div>
    <h1>User Collections</h1>
    <h2 v-if="!is_loading">Favorite Authors:</h2>
    <ul class="author-list">
      <router-link :to="`/information/authors/${author['_id']}`" v-for="author in authors" :key="author.id">
        <div class="author-item">
          <span>{{ author['name'] }}</span>
          <button class="cancel-button" @click.prevent="sendRequest_author" v-bind:data-id="author['_id']">取消收藏</button>
        </div>  
      </router-link>
      <div v-if="!authors.length&&!is_loading" class="empty-message">暂时还没有作者收藏记录~</div>
    </ul>
    <h2 v-if="!is_loading">Favorite Papers:</h2>
    <ul class="paper-list">
      <router-link :to="`/information/papers/${paper['_id']}`" v-for="paper in papers" :key="paper.id">
        <div class="paper-item">
          <span>{{ paper['*title'] }}</span>
          <button class="cancel-button" @click.prevent="sendRequest_paper" v-bind:data-id="paper['_id']">取消收藏</button>
        </div>
      </router-link>
      <div v-if="!papers.length&&!is_loading" class="empty-message">暂时还没有文献收藏记录~</div>
    </ul>
    <div>
      <transition name="fade">
        <loading v-if="is_loading"></loading>
      </transition>
    </div>
  </div>
</template>

<style>
.author-list,
.paper-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.author-item,
.paper-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 5px;
}

.cancel-button {
  border: none;
  background-color: transparent;
  color: #3498db;
  cursor: pointer;
}

.cancel-button:hover {
  text-decoration: underline;
}
.empty-message {
    margin-top: 10px;
    font-style: italic;
    color: gray;
  }
</style>

  
<script>
import Loading from "../components/Loading.vue";
import {ElMessage} from "element-plus";
import axios from  'axios';
  export default {
    data() {
      return {
        authors: [],
        papers: [],
        is_loading: false,  
      };
    },
    mounted() {
      
      const userId = localStorage.getItem('ms_userid');
      const url = this.backendurl;
      this.is_loading = true;
      // 发起 GET 请求获取收藏信息
      axios.get(url+`/collection/collections/${userId}`)
        .then(response => {
          this.is_loading = false;
          const collectiondata = response.data;
          console.log(collectiondata);
          this.authors = response.data.authors;
          this.papers = response.data.papers;
          console.log(this.authors);
          console.log(this.papers);
          //ElMessage.success('成功');
        })
        .catch(error => {
          this.is_loading = false;
          console.log(error);
          ElMessage.error('获取收藏失败，请检查网络连接！');
        })
        .finally(() => {
          // 无论请求成功还是失败，都将 is_loading 设置为 false
          this.is_loading = false;
        });
    },
    methods:{
      sendRequest_author(event){
        const id = event.target.getAttribute('data-id');
        const params = {
          userId : localStorage.getItem('ms_userid'),
          collection_id : id,
        }
        console.log(params)
        axios.get(`http://127.0.0.1:5000/collection/user/delete_collection`,{params})
          .then(response => {
            // 请求成功处理逻辑
            console.log(response.data);
            ElMessage.success(response.data);
            location.reload();
          })
          .catch(error => {
            // 请求失败处理逻辑
            console.error(error);
            ElMessage.error(error);
          });
      },
      sendRequest_paper(event){
        const id = event.target.getAttribute('data-id');
        const params = {
          userId : localStorage.getItem('ms_userid'),
          collection_id : id,
        }
        console.log(params)
        axios.get(`http://127.0.0.1:5000/collection/user/delete_collection`,{params})
          .then(response => {
            // 请求成功处理逻辑
            console.log(response.data);
            ElMessage.success(response.data);
            location.reload();
          })
          .catch(error => {
            // 请求失败处理逻辑
            console.error(error);
            ElMessage.error(error);
          });
      }
    }
  };
  </script>
  