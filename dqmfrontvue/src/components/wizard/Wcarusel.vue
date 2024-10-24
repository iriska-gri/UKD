<template>
<div class="flex-item flex-col carusel">
    <!-- <span class="flex-item">Рисунок {{images[picindx].name}}</span> -->

    <v-carousel
        v-model="picindx"
        height="100%"
        hide-delimiters                     
        :value="picindx"
        
        class="flex-item flex-col"
        :show-arrows="images.length>1?true:false"
    >
        <v-carousel-item
            v-for="(item, i) in images"
            :key="i"
        >
            <v-sheet
                height="100%"
            >
                <v-row
                    class="row_carusel_img"
                    align="center"
                    justify="center"
                >
                    <v-col
                        class="flex-col"
                    >
                        <v-img
                            :src="item.path"
                            :alt="item.name"
                            contain 
                            height="35vh"
                            class="flex-item"
                            @click="dialogshow(true)"
                        >
                        </v-img>
                    </v-col>    
                </v-row>
            </v-sheet>
        </v-carousel-item>
    </v-carousel>

    <v-dialog
        transition="dialog-top-transition"
        style="overflow-y: hidden;"
        max-width="80%"        
        v-model="dialog"
    >   
        <template v-slot:default="">
            <v-card>
                <v-card-title class="primary--text">
                    <span> {{images[picindx].name}} </span>
                    <!-- value -->
                    <v-spacer></v-spacer>
                    <v-btn icon @click="dialogshow(false)"><v-icon  class="primary--text">mdi-close</v-icon> </v-btn>
                </v-card-title>
                <v-card-text class="pa-3" style="background: rgb(238, 235, 239);" width="100vw">   
                    <v-carousel
                        v-model="picindx"
                        height="80vh"
                        :show-arrows="images.length>1?true:false" 
                        class="flex-col"                       
                    >
                        <v-carousel-item
                            v-for="(item, i) in images"
                            :key="i"                            
                        >
                            <v-sheet                            
                                height="100%"
                                class="flex-item"
                            >
                                <v-row                                
                                    align="center"
                                    justify="center"
                                >
                                    <v-col
                                        class="flex-col "
                                    >
                                    <!-- height="78vh" -->
                                        <v-img
                                            :src="item.path"
                                            :alt="item.name"
                                            contain
                                            
                                            class="flex-item img_carusel"                                        
                                        >
                                        </v-img>
                                    </v-col>
                                </v-row>
                            </v-sheet>
                        </v-carousel-item>         
                    </v-carousel>
                </v-card-text>
            </v-card>
        </template>
    </v-dialog>
</div>
</template>

<script>
export default {
name: "w-carusel",

props:{
    images:{
        type: Array,
         default() {
            return []}
    },
    // dialog:{
    //     type: Boolean,
    //     default: false
    // }
    // picindx:{
    //     type: Number,
    //     default:0
    //         }
},
data(){
    return{
    // dialog: false,
    
    
    
    }
},
methods:{
dialogshow(val){
    this.dialog = val
    
}
},
mounted(){
// console.log(this.picindx);
},

computed: {
    dialog:{
        get: function(){return this.$store.getters.wizarddialog},
        set:function(val){this.$store.commit('wizarddialog', val)}
    },
    picindx:{
    get:function(){return this.$store.getters.picindx},
    set:function(val){this.$store.commit('picindx', val)}          
    }
    
        
  },
  
// watch:{
//     picindx:function (){
       
//         this.$emit('changepick', this.images[this.picindx].name)
//     },
    // dialog: function(){
    //     this.$store.commit('wizarddialogCh', this.dialog)
    // }


}

</script>

<style>

.carusel .v-responsive__content {
    width: 100%!important;
}


.img_carusel {
    height: 80vh;
  
}
</style>