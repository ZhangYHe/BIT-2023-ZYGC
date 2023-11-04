<template>
  <div class="author-details">
    <h2>{{ author.name }}</h2>
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
    
    <button v-if="author.name">
      <router-link :to="`/visualization/author/${author['_id']}`">Go to author Visualization</router-link>
    </button>

    
    <!-- 可根据返回的 JSON 数据中的其他字段添加更多信息 -->

  </div>
  <div>
      <transition name="fade">
        <loading v-if="is_loading"></loading>
      </transition>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
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
    };
  },
  mounted() {
    this.getAuthorDetails();
  },
  methods: {
    getAuthorDetails() {
      const authorId = this.$route.params.author_id;
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
</style>

<!-- <template>
    <div class="author-details">
      <h2>{{ author['name'] }}</h2>

    </div>

  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { ElMessage } from 'element-plus';
  import axios from 'axios';
  
  export default {
    data() {
      return {
        author: {
            // "_id": "",
            // "affiliation": "",
            // "dblp_key": "",
            // "first_name": "",
            // "last_name": "",
            
            '_id':'',
            'name': '',

            // "name_index": "",
            // "orcid": "",
            // "other_affiliation": [],
            // "other_names": [],
            // "profiles": [],
        },
      };
    },
    mounted() {
      this.getAuthorDetails();
    },
    methods: {
      getAuthoretails() {
        const authorId = this.$route.params.author_id;
        const url = `http://127.0.0.1:5000/information/authors/651288cfeb11a940d8e47976`;
        axios.get(url)
          .then((response) => {
            //ElMessage.success(authorId);
            this.author = response.data;
          })
          .catch((error) => {
            //ElMessage.success('失败');
            console.error('Failed to fetch author details:', error);
          });
      },
      // formatAuthors() {
      //   return 0;
      // },
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
  
  /* h2 {
    font-size: 24px;
  }
  
  p {
    margin: 10px 0;
  }
  
  .abstract {
    white-space: pre-line;
  } */
  </style>
   -->