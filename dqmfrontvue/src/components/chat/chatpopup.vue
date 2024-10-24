<template>

 <div>
    <div class="my-3 ml-3"><h2>НОВОСТНАЯ ЛЕНТА</h2></div>
    <div class="d-flex flex-column scroller"
    :class="panel?'mini':'maxi'">
      <div
          v-for="(item, i) in content"
            :key="i"       
            class="pa-0 ml-2 mr-1 noborder" 
          >
                <div>
                <!-- <v-avatar
                size="15"
                >
                <v-img 
                  :src="linker + item.author__photo">
                </v-img>
                
                </v-avatar> -->
                <div class="d-flex justify-space-between">
                  <div>
                <span class="px-1 minitext"><strong class="minitext">Автор: </strong>{{item.author__last_name}} {{item.author__first_name[0]}}. {{item.author__middle_name[0]}}.</span>
                <br>
                <span class="px-1 minitext"><strong class="minitext">Дата добавления: </strong>{{UTCDate(item.datenews)}}</span>    
                  </div> 
                  <div
                  v-if="item.news_files.length"
                   class="d-flex align-end"><span class="px-1 minitext"><strong class="minitext">Файлов прикреплено: </strong>{{item.news_files.length}}</span> </div>
                  

                  <div style="width:45%; height:2.5rem"
                  v-if="item.news_files.length">
                   
                    <!-- show-arrows-on-hover  -->
                      <v-carousel 
                        show-arrows-on-hover
                        hide-delimiters
                        class="pt-2"
                        :show-arrows="item.news_files.length>1?true:false"
                                 
                        height="2.5rem">
                        <template 
                       
                        v-slot:prev="{ on, attrs }">
                          <v-btn 
                          
                          color="green"
                          v-bind="attrs" v-on="on"
                          x-small
                          icon >
                            
                            <v-icon
                          
                           
                        >mdi-arrow-left-bold</v-icon></v-btn>
                          
                            </template>
                        <template v-slot:next="{ on, attrs }"
                        >
                      <v-btn
                        
                          x-small
                          :ripple="false"
                            icon
                            depressed              
                       color="blue" v-bind="attrs" v-on="on"
                      >
                        <v-icon 
                        >mdi-arrow-right-bold</v-icon>
                      </v-btn>
                      </template>
                        <v-carousel-item v-for="it in item.news_files" :key="it.doc"
                        >
                            <v-sheet  height="100%">
                            <v-row class="fill-height pointer" align="center" justify="center"
                             @click="pushfile(it)">
                     <div class="d-flex"
                    >
                       <div>
                              <v-icon
                              :color= "fileiconss[fileext(it.file)]?fileiconss[fileext(it.file)].color : 'black'"
                              class="mx-3 pt-2 icon"
                              @click.stop = "download(it, $event.target)"
                              
                           >
                              {{fileiconss[fileext(it.file)]?fileiconss[fileext(it.file)].icon: 'mdi-file'}}
                          </v-icon>
                                    </div>
                                    <div  class="mx-3 pt-2" align="center" justify="center">
                                      {{ it.doc }}
                                    </div>
                     </div>
                    </v-row>
                  </v-sheet>
                </v-carousel-item>

                          
                        </v-carousel>
                      <!-- :src="item.src" -->
   

        </div>
  
      </div>
      <hr class="my-1">

      <strong class="minitext">Описание:</strong>
      <v-card
        class="mcont"
        elevation="1"
      ><p class="card-text rounded-lg px-2 pt-2" v-html="replsrc(item.newstext)" /></v-card>
      
     
      </div>
      </div>
    </div>
   
  </div>
    

</template>

<script>
import * as moment from "moment";
import { bus } from "@/main";
export default {
  name: "news-list",
  props: ['content','fileiconss','panel'],

  data(){
      return{
        newcontent:[],
      }
  } ,
 
  methods: {
       UTCDate(date) {           
            return moment(date, "YYYY-MM-DD").format("LL");
        },
        replsrc(itemcode){
          return itemcode.replaceAll('" src="/','" src="'+ this.$http.defaults.baseURL)
        },
    fileext(filestr){
  let fileext = filestr.split(".")
  return fileext[fileext.length-1]

  },
    
    
    iconprep(arr){
    arr.forEach((el) => {
    let ic=this.fileext(el.file)
    el.icon = ic in this.fileiconss? this.fileiconss[ic]: {icon: 'mdi-file', color: "black"}
      }); 
  },

  pushfile(file){
    bus.$emit('pushfile', file)
  },
   download(file, el){
    bus.$emit('loadfileiconpushed', file)
    el.blur()
  }

  },
   mounted() {
      moment.locale('ru')
      
     
   
  }, 
  computed:{
     
  }
}

</script>


<style lang="scss" scoped>
@import '@/utils/colors.scss';



</style>