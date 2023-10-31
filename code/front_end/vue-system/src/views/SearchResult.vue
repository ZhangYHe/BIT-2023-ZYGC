<template>
  <!-- <div>
    <ul>
      <li v-for="author in authors" :key="author.id">{{ author.name }}</li>
    </ul>
    <ul>
      <li v-for="paper in papers" :key="paper.id">{{ paper.title }}</li>
    </ul>
  </div> -->
</template>

<script>
export default {
  data() {
    return {
      authors: [],
      papers: []
    };
  },
  mounted() {
    this.authors = this.$route.params.authors;
    this.papers = this.$route.params.papers;
  }
};
</script>
