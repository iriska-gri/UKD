<template>
  <v-card  
    class="d-flex flex-item align-center justify-center"  
    elevation="4"
    :style="stiled(countdata.gradient)"
  >
<div>
<div class="d-flex justify-center"><animatednumber class="superbig" :value='countdata.count'/></div>
<div class="d-flex justify-center text-center textstyle mx-2">{{countdata.text}}</div>
</div>
  </v-card>
</template>

<script>
import Animatednumber from '@/components/UI/Animatednumber.vue'
import  card  from "@/utils/charts/card.js"
export default {
    name:"QuadroCard",
    mixins:[card],
    components:{Animatednumber},
    props:{        
        countdata:{type:Object},        
    },
    methods:{
        
    }
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