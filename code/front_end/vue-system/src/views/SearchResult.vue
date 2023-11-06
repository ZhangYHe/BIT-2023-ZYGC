<template>
  <div>
    <h1>Matching Records:</h1>
    <div v-for="(record, index) in matchingRecords" :key="index">
      <div>
        <router-link :to="`/information/papers/${record['_id']}`">Title: {{ record['*title' ]}}</router-link>
      </div>
      <p>DOI: <a :href="record['*doi' ]" target="_blank">{{ record['*doi' ] }}</a></p>
      <hr>
    </div>
  </div>
  <div>
    <button>
      <router-link :to="`/search/search_visualization`"> Go to Search Result Visualization</router-link>
    </button>
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
  }
};
</script>
