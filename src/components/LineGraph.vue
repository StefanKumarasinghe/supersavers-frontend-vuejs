<template>
  <div ref="chart"></div>
</template>

<script>
import * as d3 from 'd3';

export default {
  props: ["chartData", "options"],
  mounted() {
    this.drawChart();
  },
  watch: {
    chartData() {
      this.drawChart();
    }
  },
  methods: {
    drawChart() {
      const el = this.$refs.chart;

      // Clear any existing chart
      d3.select(el).selectAll("*").remove();

      const margin = { top: 20, right: 20, bottom: 30, left: 50 };
      const width = this.options.width - margin.left - margin.right || 400;
      const height = this.options.height - margin.top - margin.bottom || 300;

      const x = d3.scaleBand()
        .range([0, width])
        .domain(this.chartData.labels)
        .padding(0.1);

      const y = d3.scaleLinear()
        .range([height, 0])
        .domain([0, d3.max(this.chartData.datasets[0].data)]);

      const svg = d3.select(el).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      this.chartData.datasets.forEach(dataset => {
        const line = d3.line()
          .x((d, i) => x(this.chartData.labels[i]) + x.bandwidth() / 2)
          .y(d => y(d));

        svg.append("path")
          .datum(dataset.data)
          .attr("fill", "none")
          .attr("stroke", dataset.borderColor)
          .attr("stroke-width", 1.5)
          .attr("d", line);
      });

      // Add the X Axis
      svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

      // Add the Y Axis
      svg.append("g")
        .call(d3.axisLeft(y));
    }
  }
};
</script>

<style scoped>
div {
  width: 500px;
  height: 400px;
}
</style>
