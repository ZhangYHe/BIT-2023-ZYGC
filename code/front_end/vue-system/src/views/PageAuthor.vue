<template>
  <div class="author-details">
    <h2>{{ author.name }}</h2>
    <div class="button-container">
      <button @click="sendRequest" v-if="already_login&&author.name" class="favorite-button">
        <img src="src/assets/img/star.png" alt="Favorite" class="star-icon">
      </button>
    </div>
    <p v-if="author.affiliation">Affiliation: {{ author.affiliation }}</p>
    <p v-if="author.first_name">First Name: {{ author.first_name }}</p>
    <p v-if="author.last_name">Last Name: {{ author.last_name }}</p>
    <p v-if="author.dblp_key">DBLP Key: {{ author.dblp_key }}</p>
    <p v-if="author.orcid">ORCID: {{ author.orcid }}</p>
    <h3 v-if="author.publication_periods[0]">
      paper list:
    </h3>  
      <p v-for="(publication,index) in author.publication_periods" :key="index">
        <p v-for="paper in publication.paper_info">
          <router-link :to="`/information/papers/${paper.paper_id}`">
             {{ paper.paper_title }}
          </router-link>
        </p>
      </p>
    
    <button v-if="author.name&&author.publication_periods[0]" class="button1">
      <router-link :to="`/visualization/author/${author['_id']}`">Go to author Visualization</router-link>
    </button>

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
      author: {
        name: '',
        affiliation: '',
        first_name: '',
        last_name: '',
        dblp_key: '',
        orcid: '',
        publication_periods:[],
      },
      is_loading:false,
      already_login:false,
    };
  },
  mounted() {
    this.getAuthorDetails();
  },
  methods: {
    getAuthorDetails() {
      const authorId = this.$route.params.author_id;
      this.already_login=localStorage.getItem('ms_admintoken')==null?false:true;
      const url = `http://127.0.0.1:5000/information/authors/${authorId}`;
      this.is_loading=true;
      axios
        .get(url)
        .then((response) => {
          this.is_loading=false;
          // ElMessage.success(authorId);
          this.author = response.data;
        })
        .catch((error) => {
          this.is_loading=false;
          // ElMessage.success('失败');
          ElMessage.error('请求失败，请检查网络连接！');
          console.error('Failed to fetch author details:', error);
        })
        .finally(() => {
          // 无论请求成功还是失败，都将 is_loading 设置为 false
          this.is_loading = false;
        });
      
    },
    sendRequest() {
      const authorId = this.$route.params.author_id;
      const params = {
          userId : localStorage.getItem('ms_userid'),
          collection_id : authorId,
        };
        axios.get(`http://127.0.0.1:5000/collection/user/collect`,{params})
        .then(response => {
          // 请求成功处理逻辑
          console.log(response.data);
          ElMessage.success("已收藏");
        })
        .catch(error => {
          // 请求失败处理逻辑
          console.error(error);
          if (error.response && error.response.status === 401) {
              // 显示收藏文献已存在的提示
              ElMessage.error("该作者已收藏");
            }
            else{
              ElMessage.error("收藏失败，请检查网络");
            }
        });
    }
  },
};
</script>

<style scoped>

 .author-details {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f8f8;
  border: 1px solid #ccc;
  border-radius: 5px;
}

h2 {
  font-size: 24px;
  margin: 10px 10px;
}

h3 {
  font-size: 18px;
  margin: 10px 20px;
}

p {
  margin: 10px 20px;
}
.button-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0px;
}

.favorite-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  margin-right: 5%;
}
.star-icon {
  width: 30px;
  height: 30px;
}
.button1 {
  background-color: #00aeffd0;
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}

</style>

