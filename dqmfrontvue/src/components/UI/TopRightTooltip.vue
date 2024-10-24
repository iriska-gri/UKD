<template>
<div>
    <span
      @mouseenter="hovered(item, $event.target)" 
                         @mouseleave="buttonHovering = false"
                            ref="tooltipio"
                            style="cursor:pointer"
    >{{item[textfield]}}</span>
   <v-tooltip
                    right
                     v-model="showToolTip"
                     :position-x="toolleft"
                     :position-y="tooltop"
          >
             <div  v-for="(i,index) in $passportnamed(`${item[textfield]}: ${item[helptext]}`)" :key="index">
                        <span>{{ i }}</span>
                         </div>
          </v-tooltip>
        </div>
</template>

<script>
import globalFuncs from '@/utils/helper'
export default {
    name:"top-right-tooltip",
    props:{
        item: {
            type:Object,
            default:{}
        },
        textfield:{type:String,
               default:"passport__code"             
                            },
        helptext:{type:String,
               default:"passport__name"             
                            },
    },

    data(){
      return{      
        showToolTip: false,
            buttonHovering:false,
            toolleft:0,
            tooltop:0,}
            
    },
    methods:{
         hovered(item,target){                
               
                this.toolleft = target.getBoundingClientRect().left + target.getBoundingClientRect().width/2
                this.tooltop = target.getBoundingClientRect().top - target.getBoundingClientRect().height*2
                // console.log(left,top);
                this.buttonHovering = true;
        },
    },
    watch: {
        buttonHovering (newVal) {
         this.showToolTip = newVal
        },
     },

}
</script>

<style>

</style>