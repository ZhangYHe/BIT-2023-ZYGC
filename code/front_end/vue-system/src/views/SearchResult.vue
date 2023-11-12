<template>
  <div class="container">
    <h1 class="title">Authors:</h1>
    <div class="record" v-for="(record, index) in matchingRecords" :key="index">
      <div v-if="isAuthor(record)">
        <p>
          Author: <router-link :to="`/information/authors/${record['_id']}`">{{ record['name'] }}</router-link>
        </p>
      </div>
      <div v-else> 
        Title: <router-link class="link" :to="`/information/papers/${record['_id']}`">{{ record['*title' ]}}</router-link>
      
      <!-- <p>DOI: <a class="link" :href="record['*doi' ]" target="_blank">{{ record['*doi' ] }}</a></p> -->
      <p>
        Authors: <span v-for="(author, index) in record['*authors']"><router-link :to="`/information/authors/${author.id}`">
          {{ author['name'] }}{{ index !== record['*authors'].length - 1 ? ', ' : '' }}</router-link>
        </span>
      </p>
    </div>
      <hr>
    </div>
    <div>
      <button class="button">
        <router-link class="link" :to="`/search/search_visualization`"> Go to Search Result Visualization</router-link>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      matchingRecords:[],
    };
  },
  created() {
    console.log("2");
    //console.log(JSON.parse(this.$route.params.matchingRecords));
    const matching_Records = JSON.parse(this.$route.params.matchingRecords);
    this.matchingRecords = matching_Records;
    console.log(this.matchingRecords);
  },
  methods: {
    isAuthor(record) {
      return record.hasOwnProperty('name'); // 检查记录是否是作者
    },
  },
};
</script>

<style scoped>
.container {
  width: 80%;
  margin: auto;
}

.title {
  font-size: 2em;
  color: #333;
  margin-bottom: 1em;
}

.record {
  border: 1px solid #ccc;
  padding: 1em;
  margin-bottom: 1em;
}

.link {
  color: #007BFF;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.button {
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

.button:hover {
  background-color: #0084ffd0;
}
</style>