<template>
  <div class="don-items-1" v-if="Object.keys(chartData).length">
    <Pie
    :chart-options="chartOptions?chartOptions:{}"
    :chart-data="chartData?chartData:{}"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :width="width"
    :height="height"
    :css-classes="cssClasses"
    :styles="styles"
    class=""
    />
    <!-- <v-tooltip
      
      top
      color="primary"
    >
      <template
        v-slot:activator="{ on, attrs }"
      > -->
        <div
          class="donval ma-auto"
          :style="{color: chartData.datasets? chartData.datasets[0].backgroundColor[0]:'black'}"
          
        ><p class = "anima">
          <animatednumber
            class = "anima" 
            :value='chartData.datasets? Number(rounded(chartData.datasets[0].data[0]/(chartData.datasets[0].data[1]+chartData.datasets[0].data[0])*100)):0'
            :fixed = 2>
          </animatednumber>%</p>
        </div> 
      <!-- </template> -->
      <!-- <span 
        class="pointed zind"        
      >{{chartData.hovers? formatter(chartData.hovers.thisdata):0 }} из {{chartData.hovers? formatter(chartData.hovers.total):0}}
      </span> -->
    <!-- </v-tooltip> -->
    
  </div>
  
  <div v-else class ="don_skelet">
    <v-skeleton-loader
    type="heading, avatar"
    >
    </v-skeleton-loader>
  </div>

</template>

<script>

import { Pie } from 'vue-chartjs/legacy'

import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale} from 'chart.js'
import Animatednumber from '@/components/UI/Animatednumber.vue'
import ChartJsPluginDataLabels from 'chartjs-plugin-datalabels'
ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, ChartJsPluginDataLabels)
Tooltip.positioners.myCustomPositioner= function(items) {
  const pos = Tooltip.positioners.average(items);

  // Happens when nothing is found
  if (pos === false) {
    return false;
  }

  const chart = this.chart;
 
  return {
    x: pos.x,
    y: chart.chartArea.height*0.5,
    xAlign: 'center',
  
  };
};
export default {
  name: 'PieChart',
  components: {
    Pie,
    Animatednumber
  },
  props: {
    
    chartId: {
      type: String,
      default: 'pie-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      type: Number,
      default: 0
    },
    height: {
      type: Number,
      default: 0
    },
    cssClasses: {
      default: 'canvas-items-1',
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
    },
    hovers:{
      type: Object,
      default:()=>{}
    }

  },
  data() {
    return {
      show: false,
    
    }
  },

  methods:{
         formatter(integer){
      return ((integer>=10000)||(integer<=-10000))?new Intl.NumberFormat('ru-RU').format(integer):integer
    },    
     rounded(number){
        return +number.toFixed(2);
    },
    },

 
}
</script>
<style lang="scss">
// .zind{
//   position:relative;
//   z-index:1;
// }


.don_skelet {
      align-self: center;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-grow: 1;
  .v-skeleton-loader__avatar {
    border-radius: 50%;
    height: 160px;
    width: 160px;
}
.v-skeleton-loader__heading {
    margin-left: 25%;
    margin-top: 17px;
    margin-bottom: 4px;
    border-radius: 12px;
    height: 15px;
    width: 50%;
}
}

.don-items-1 {
  display: flex;
  flex-direction: row;
  flex-grow: 1;
  justify-content: center;
  align-items: center;
}

.canvas-items-1 {

  display: flex;
  flex-grow: 1;
  height: 90%;
  width: 100%;
  justify-content: center;
  align-items: center;


    canvas {
    // background: red;
    min-height: 180px !important;
    width: 20% !important;
    flex-grow: 1;
    padding-bottom: 2px;
    position: relative;
    z-index: 1;
  }

}



.donval{
    position:absolute;
    margin-left: auto;
margin-right: auto;
left: 0;
right: 0;
top:50%;
text-align: center;
    width: 50%;
  
    }
.pointed{
  cursor: pointer !important;
}

.anima {
  font-size: 1.8rem !important;
}

@media (max-width:750px) {
  .anima {
    font-size: 1.5rem !important;
}
}
@media (max-width:586px) {
.donval {
    top: 53%;
}
.anima {
    font-size: 1.0rem !important;
}
}

@media (max-height: 870px) {
  .canvas-items-1 {



    canvas {

    min-height: 160px !important;

  }
}
}

</style>  