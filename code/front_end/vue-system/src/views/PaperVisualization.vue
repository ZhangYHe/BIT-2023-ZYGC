<template>
    <div>
      <!-- <h1>debug</h1> -->
      <div class="chart-container">
        <canvas id="chart"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
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
          datasets: []
        },
        paperId: null
      };
    },
    mounted() {
      this.paperId = this.$route.params.paper_id;
  
      axios.get(`http://127.0.0.1:5000/visualization/paper/${this.paperId}`)
        .then(response => {
          const data = response.data;
          this.drawChart(data);
        })
        .catch(error => {
          console.error("Error fetching data:", error);
        });
    },
    methods: {
      drawChart(data) {
        const labels = ["0-1990", "1990-1995", "1995-2000", "2000-2005", "2005-2010", "2010-2015", "2015-2019", "2020-2024"];
        const datasets = [];
  
        for (const item of data) {
          if (item.author_id) {
            datasets.push({
              label: item.name,
              data: item.paper_count,
            });
          }
        }
  
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
            maintainAspectRatio: false, // 允许图表自动缩放
            responsive: true, // 使图表响应窗口大小变化
            plugins: {
              title: {
                display: true,
                text: '本文作者发表论文数量趋势',
              },
            },
            // 纵轴的最小值为 0，最大值为 100，每个刻度之间的距离为 10
            // scales: {
            // y: {
            //   min: 0,
            //   max: 100,
            //   ticks: {
            //     stepSize: 10
            //   }
            // }
            // }
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
    /* width: 100%; //设置容器宽度，根据需要调整 */
    width: 1500px; /* 设置容器宽度 */
    height: 500px; /* 设置容器高度 */
    margin: 0 auto;
  }
  </style>
  