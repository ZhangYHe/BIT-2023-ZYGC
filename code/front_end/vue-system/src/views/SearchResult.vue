<template>
  <div>
    <h1>Matching Records:</h1>
    <div v-for="(record, index) in matchingRecords" :key="index">
      
      <p>Title: {{ record['*title' ]}}</p>
      <p>DOI: <a :href="record['*doi' ]" target="_blank">{{ record['*doi' ] }}</a></p>
      <hr>
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
  }
};
</script>
