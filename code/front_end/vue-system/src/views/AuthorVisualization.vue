<template>
  <div>
    <div class="chart-container">
      <canvas id="chart"></canvas>
    </div>
    <div>
      <transition name="fade">
        <loading v-if="is_loading"></loading>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from 'element-plus';
import Loading from "../components/Loading.vue"
import Chart from 'chart.js/auto';

export default {
  data() {
    return {
      options: {
        type: 'line',
        title: {
          display: true,
          text: '作者论文数量趋势',
        },
        bgColor: '#fbfbfb',
        labels: [],
        datasets: [],
      },
      authorId: null,
      is_loading: false,
    };
  },
  mounted() {
    this.authorId = this.$route.params.author_id;
    this.is_loading=true;
    axios.get(`http://127.0.0.1:5000/visualization/author/${this.authorId}`)
      .then(response => {
        this.is_loading=false;
        const data = response.data;
        this.drawChart(data);
      })
      .catch(error => {
        this.is_loading=false;
        ElMessage.error('请求失败，请检查网络连接！');
        console.error("Error fetching data:", error);
      })
      .finally(() => {
        this.is_loading = false;
      });;
  },
  methods: {
    drawChart(data) {
      const labels = ["0-1990", "1990-1995", "1995-2000", "2000-2005", "2005-2010", "2010-2015", "2015-2019", "2020-2024"];
      const datasets = [];

      datasets.push({
        label: data.name,
        data: data.paper_count,
      });

      const ctx = document.getElementById('chart');
      if (ctx.chart) {
        ctx.chart.destroy();
      }

      const chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: datasets,
        },
        options: {
          maintainAspectRatio: false,
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: '作者发表论文数量趋势',
            },
          },
          scales: {
            y: {
              min: 0,
              max: Math.max(...data.paper_count) + 1,
              ticks: {
                stepSize: 10,
              },
            },
          },
        },
      });
    },
  },
};
</script>

<style>
#chart {
  max-width: 100%;
  max-height: 100%;
  margin: 0 auto;
}

.chart-container {
  width: 90%; 
  height: 500px;
  margin: 0 auto;
}
</style>
