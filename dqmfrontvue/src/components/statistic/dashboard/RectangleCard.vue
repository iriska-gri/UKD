<template>
  <v-card
  
  elevation="4"
    :style="stiled(['#203A63','#5325D0'])"
    class="d-flex flex-item flex-column justify-space-between"
  >
<div class="d-flex flex-row justify-space-around">
<div class="mt-2"  v-for="(item, index) in way" :key="index">  
    <!-- <div> -->
        <v-icon class="superbig d-flex justify-center"
        large
        color="#E87289"
        >{{countdata[item].icon}}</v-icon>
        <div class="d-flex justify-center"><animatednumber class="superbig" :value='countdata[item].count'/></div>
        <div class="d-flex justify-center text-center textstyle mx-2">{{countdata[item].text}}</div>
    <!-- </div> -->
</div>
</div>
    <div ><span class="textstyle pl-2 pt-auto">*На дату выгрузки {{loclisator(max_date)}}</span>
    </div>
    </v-card>

</template>

<script>
import * as moment from "moment";
import Animatednumber from '@/components/UI/Animatednumber.vue'
import  card  from "@/utils/charts/card.js"
export default {
name:"RectangleCard",
    components:{Animatednumber},
    mixins:[card],
    props:{ 
        way:{type:Array},       
        countdata:{type:Object},
        max_date:{type:String}        
    },
    methods:{
        loclisator(date){
            moment.locale('ru')
        return moment(date).format('LL')
     }
    },
    mounted() {
     
      
     
   
  }, 
    
}
</script>
<style lang="scss" scoped>
@import '@/utils/colors.scss';
.superbig{
    color: $bg-white ;
      font-size: 3rem !important;
      font-weight: 800 !important;
}
.textstyle{
    color: $bg-white ;
}

</style>