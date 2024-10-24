<template>
<div class="flex-item flex-col card_Linear_item" v-if="Object.keys(chartData).length">
  <LineChartGenerator
    :chart-options="chartOptions"
    :chart-data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
 
  />
    <!-- :height="height" -->
</div>
<div class="flex-item flex-col card_Linear_item" v-else>
  <div class="lin_items">
      <v-skeleton-loader
    type="image"
    >
    </v-skeleton-loader>
  </div>

</div>
</template>

<script>
import { Line as LineChartGenerator } from 'vue-chartjs/legacy'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement,
  Filler
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement,
  Filler,
)

export default {
  name: 'LineChart',
  components: {
    LineChartGenerator
  },
  props: {
    chartId: {
      type: String,
      default: 'line-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      type: Number,
      default: 100
    },
    height: {
      type: Number,
      default: 65
    },
    cssClasses: {
      default: 'lin_items',
      type: String
    },
    styles: {
      type: Object,
      default: () => {}
    },
    plugins: {
      type: Array,
      default: () => []
    },
      chartData: {
        type: Object,
      default: () => {}
      },
    chartOptions: {
        type: Object,
      default: () => {}
      }
  },
  data() {
    return {
  
    }
  },
 
}
</script>
<style lang="scss">
@import "@/utils/colors.scss";

.card_Linear_item {
  width: 100%;
  height: 100%;
  .v-skeleton-loader {
    flex-grow: 1
  }
.v-skeleton-loader__image {
    height: 100%;
    border-radius: 0;
}
}

.lin_items {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    canvas {
      flex-grow: 1;
      max-height: 100%;
    }
}
  

</style>