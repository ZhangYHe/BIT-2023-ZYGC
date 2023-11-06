<template>
    <div>
      <!-- 柱形图容器 -->
      <div class="chart-container">
        <canvas id="bar-chart"></canvas>
      </div>
      <!-- 折线图容器 -->
      <div class="chart-container">
        <canvas id="line-chart"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import Chart from 'chart.js/auto';
  
  export default {
    data() {
      return {
        barChartData: {  // 柱形图数据
          labels: [],  // 横坐标标签
          datasets: [
            {
              label: '',
              data: [],
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
            },
          ],
        },
        lineChartData: { // 折线图数据
          labels: [],  // 横坐标标签
          datasets: [
            {
              label: '',
              data: [],
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1,
              fill: false,
            },
          ],
        },
      };
    },
    mounted() {
      axios.get(`http://127.0.0.1:5000/search/search_visualization`)
        .then(response => {
          const data = response.data;
          console.log("Received data from the server:", data);
          
          // 设置柱形图数据
          this.barChartData.labels = Object.keys(data);
          this.barChartData.datasets[0].data = Object.values(data);
          this.drawBarChart();
          
          // 设置折线图数据（仅使用authornum前面的数据）
          const authornumData = Object.values(data).slice(0, 8);
          this.lineChartData.labels = Object.keys(data).slice(0, 8);
          this.lineChartData.datasets[0].data = authornumData;
          this.drawLineChart();
        })
        .catch(error => {
          console.error("Error fetching data:", error);
        });
    },
    methods: {
      drawBarChart() {
        const ctx = document.getElementById('bar-chart');
        if (ctx.chart) {
          ctx.chart.destroy();
        }
  
        const chart = new Chart(ctx, {
          type: 'bar',
          data: this.barChartData,
          options: {
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
              title: {
                display: true,
                text: '搜索结果总览',
              },
            },
          },
        });
      },
      drawLineChart() {
        const ctx = document.getElementById('line-chart');
        if (ctx.chart) {
          ctx.chart.destroy();
        }
  
        const chart = new Chart(ctx, {
          type: 'line',
          data: this.lineChartData,
          options: {
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
              title: {
                display: true,
                text: '搜索到论文发表年份分布',
              },
            },
          },
        });
      },
    },
  };
  </script>
  
  <style>
  .chart-container {
    width: 100%;
    height: 500px;
    margin: 0 auto;
  }
  </style>
  