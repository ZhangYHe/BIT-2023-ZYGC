<template>
  <div id="searchEngine">
  <input type="text" id="text" v-model="query" v-on:input="change">
  <span id="img_upload"></span>
  <button v-on:click="submit" id="button">search</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
name: 'searchEngine',
data () {
  return {
    query: '',
  };
},
methods: {
  change: function(){
    this.$emit('childChange',this.query)
  },
  submit: function(){

    if (this.query === '') {
      ElMessage.error('Keyword is required');
    return;
    }
    
    //location.reload() 
    const params = {
      keyword: this.query,
    };
    ElMessage.error(this.query);
    axios.get('http://127.0.0.1:5000/search/searchres',{
      params: {
        keyword: this.query,
      },
})
  
  .then(response => {
      // 处理响应数据
      // const keywords = response.data.keyword;
      // const matchingRecords = response.data.keyword; //response.data.matching_records;
      //ElMessage.success(matchingRecords);
      const authors = response.data.authors;
      const papers = response.data.papers;

      ElMessage.success(authors);
      ElMessage.success(papers);

      this.$router.push({
      name: 'SearchResult',
      params: {authors,papers}
    })
  })
    .catch(error => {
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
  width: 40%;
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
  width:10%;
  background-color:#39F;
  border-width: 1px;
  border-style: solid;
  font-size:24px;
  color:#FFF;
  margin:-2px 0 0 -5px;
  padding: 0px;
}
</style>
