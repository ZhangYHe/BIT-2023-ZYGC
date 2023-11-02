<template>
    <div>
      <h1>User Collections</h1>
      <h2>Favorite Authors:</h2>
      <ul>
        <li v-for="author in favoriteAuthors" :key="author.id">{{ author.name }}</li>
      </ul>
      <h2>Favorite Documents:</h2>
      <ul>
        <li v-for="document in favoriteDocuments" :key="document.id">{{ document.title }}</li>
      </ul>
    </div>
  </template>
  
<script>
import Loading from "../components/Loading.vue";
import {ElMessage} from "element-plus";
import axios from  'axios';
  export default {
    data() {
      return {
        favoriteAuthors: [],
        favoriteDocuments: [],
      };
    },
    mounted() {
      //const userId = '<user_id>'; // 替换为实际的 user_id
      const userId = localStorage.getItem('ms_userid');
      const url = this.backendurl;
      // 发起 GET 请求获取收藏信息
      axios.get(url+`/collection/collections/${userId}`)
        .then(response => {
          this.favoriteAuthors = response.data.favoriteAuthors;
          this.favoriteDocuments = response.data.favoriteDocuments;
          console.log(this.favoriteAuthors);
          console.log(this.favoriteDocuments);
        })
        .catch(error => {
          console.log(error);
        });
    },
  };
  </script>
  