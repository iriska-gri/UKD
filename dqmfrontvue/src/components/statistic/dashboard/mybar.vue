<template>
 <!--  -->
<div class="flex-item flex-col card_Mybar_item_1" v-if="Object.keys(chartData).length">
 <Bar 
    :chart-options="chartOptions"
    :chart-data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
    :height="height"
  />
</div>

<div class="card_Mybar_item_1" v-else>
    <v-skeleton-loader
      type="chip, table-heading, table-heading, table-heading, table-heading, table-heading"                      
  >
  </v-skeleton-loader>
</div>
</template>

<script>
// import { Bar } from 'vue-chartjs'
import { Bar } from 'vue-chartjs/legacy'

import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import ChartJsPluginDataLabels from 'chartjs-plugin-datalabels'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ChartJsPluginDataLabels)

export default {
  name: 'BarChart',
  components: { Bar },
  props: {
    chartId: {
      type: String,
      default: 'bar-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      type: Number,
      default: 800,
    },
    height: {
      type: Number,
      default: 50,
    },
    cssClasses: {
      default: 'mybar-items',
      type: String
    },
    styles: {
      type: Object,
      default: () => {}
    },
    plugins: {
      type: Object,
      default: () => {}
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
  }
}
</script>




<style lang="scss">
.card_Mybar_item_1 {
      padding: 10px 5px 0 17px;
      width: 100%;
      height: 100%;

.v-skeleton-loader {

    height: 100%;
}

  .v-skeleton-loader__bone {

    height: 17%;
}

    .v-skeleton-loader__chip {
      width: 44%;
      height: 17px;
      margin: 12px 0 12px 28%;
}
    .v-skeleton-loader__text {
      border-radius: 0px;
      flex: 1 0 auto;
      height: 37px;
      margin-bottom: 12px;
      max-width: 83%;
      margin-right: 10px;
      margin-left: 29px;
}
.v-skeleton-loader__heading {
    border-radius: 12px;
    height: 17px;
    width: 60%;
}

.v-skeleton-loader__table-heading {

    padding: 3px;
}

  .mybar-items{

    width: 100%;
    height: 100%;

  }
  
}
</style>