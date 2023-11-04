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
    //提交时出现加载动画
    this.is_loading = true;
    if (this.query === '') {
      ElMessage.error('Keyword is required');
    return;
    }
    
    //location.reload() 
    const params = {
      keyword: this.query,
    };
    //ElMessage.error(this.query);
    axios.get('http://127.0.0.1:5000/search/searchres',{
      params
})
  
  .then(response => {
      // 处理响应数据
      // const keywords = response.data.keyword;
      //ElMessage.success("matchingRecords");
      const matchingRecords = response.data;
      // const authors = response.data.authors;
      // const papers = response.data.papers;
      console.log("1");
      console.log(matchingRecords);
      //后端处理完成，将is_loading改为false
      this.is_loading = false;
      this.$router.push({
      name: 'SearchResult',
      params: {matchingRecords:JSON.stringify(matchingRecords)}
    })
  })
    .catch(error => {
    })
    .finally(() => {
      // 无论请求成功还是失败，都将 is_loading 设置为 false
      this.is_loading = false;
    });
}
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#searchEngine{
  left: 25%;
  top: 40%;
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
