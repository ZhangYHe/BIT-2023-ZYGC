<!-- <template>
    <div>
      <h1>Search Result</h1>
  
      <ul>
        <li v-for="(record, index) in matchingRecords" :key="index">
          <div>
            <h3>{{ record.title }}</h3>
            <p>{{ record.description }}</p>
          </div>
          <hr />
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      matchingRecords: {
        type: Array,
        required: true,
      },
    },
  };
  </script>
   -->

   <template>
    <div>
      <h1>Search Result</h1>
      <p>Keywords: {{ test }}</p>
    </div>
  </template>
  
  <script>
  export default {

    props: {
      test: {
        type: String,
        required: true,
      },
    },
  };
  
  </script>
  