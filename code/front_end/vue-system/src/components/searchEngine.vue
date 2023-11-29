<template>
    <div id="searchEngine">
      <input type="text" id="text" v-model="query" v-on:input="change">
      <span id="img_upload"></span>
      <button v-on:click="submit" id="button">search</button>
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
  export default {
  name: 'searchEngine',
  data () {
    return {
      query: '',
      is_loading: false,
    };
  },
  methods: {
    change: function(){
      this.$emit('childChange',this.query)
    },
    submit: function(){
      
      
      if (this.query === '') {
        ElMessage.error('请输入关键词！');
      return;
      }
      //提交时出现加载动画
      this.is_loading = true;
      const params = {
        keyword: this.query,
      };
      axios.get('http://127.0.0.1:5000/search/searchres',{params})
      .then(response => {
          const matchingRecords = response.data;
          console.log("1");
          console.log(matchingRecords);
          this.is_loading = false;
          this.$router.push({
          name: 'SearchResult',
          params: {matchingRecords:JSON.stringify(matchingRecords)}
        })
      })
      .catch(error => {
        if (error.response && error.response.status === 401) {
              ElMessage.error("无搜索结果！");
            }
        else{
        ElMessage.error('搜索失败，请检查网络！');
        }
      })
        .finally(() => {
          this.is_loading = false;
        });
  }
    }
  }
  </script>
  
  <style scoped>
  #searchEngine{
    left: 25%;
    top: 60%;
    width: 50%;
    position: fixed;
    z-index: 1;
    background-color: #FFF;
  }
  #text{
    width: 80%;
    height: 41px;
    
    border-style:solid;
    border-width:1px;
    border: solid 1px #39F;
    font-size:24px;
    padding: 0px;
    margin:-1px 0 0 0px;
  }
  #img_ipload{
  background:url(https://ss1.bdstatic.com/5eN1bjq8AAUYm2zgoY3K/r/www/cache/static/protocol/https/soutu/img/camera_new_5606e8f.png) no-repeat;
  }
  #button{
    float: right;
    height:45px;
    width:20%;
    background-color:#39F;
    border-width: 1px;
    border-style: solid;
    font-size:24px;
    color:#FFF;
    margin:-2px 0 0 -5px;
    padding: 0px;
  }
  </style>
  