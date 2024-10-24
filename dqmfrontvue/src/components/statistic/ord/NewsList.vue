<template>
    <div class="flex-item flex-col NLitem" v-if="content.length>0">
      <div class="NLitem_1">
        <h2 class="pt-3 pl-3">{{header}}</h2>
      </div>
      <div class="flex-item flex-col NLitem_2 px-3">
          <div class="flex-col NLitem_2_1"
            v-for="(item, i) in content"
            :key="i"
            >
           <v-card
                class="mcont my-1 "
                elevation="3"
              >
            <div class="flex-static_row NLitem_2_1_1"> 
              
              <div class="flex-item NLitem_2_1_1_1 d-flex">
                
                <div v-if="(new Date()- new Date(item.datenews))/(1000 * 60 * 60 * 24)<8"><v-icon
                class="pl-2 minitext2"
                color="green"
                >mdi-comment-text-outline</v-icon>
                </div>
                <div v-if="item.urgency"><v-icon
                class="pl-1 minitext2"
                color="red"
                
                >mdi-alarm</v-icon>
                </div>
                <div><span class="minitext pl-2">{{UTCDate(item.datenews)}}</span></div>
                
              </div>
              
              <div class="flex-item NLitem_2_1_1_2" v-if="item.news_files.length">
                <span class="minitext"><strong class="minitext">Файлов прикреплено: </strong>{{item.news_files.length}}</span>
              </div>
              
              <div class="flex-item NLitem_2_1_1_2" v-else>
              </div>

              <div class="flex-item NLitem_2_1_1_3">
                        <v-carousel 
                          show-arrows-on-hover
                          hide-delimiters
                          :show-arrows="item.news_files.length>1?true:false" 
                          height="100%">
                            <template 
                              v-slot:prev="{ on, attrs }"
                            >
                              <v-btn 
                              color="green"
                              v-bind="attrs"
                              v-on="on"
                              x-small
                              icon
                              >
                                <v-icon>mdi-arrow-left-bold</v-icon>
                              </v-btn>
                            </template>
                          <template
                            v-slot:next="{ on, attrs }"
                          >
                            <v-btn
                              color="blue"
                              v-bind="attrs"
                              v-on="on"
                              x-small
                              icon
                            >
                        
                              <v-icon>mdi-arrow-right-bold</v-icon>
                            </v-btn>
                          </template>
                          <v-carousel-item
                            v-for="it in item.news_files"
                            :key="it.doc"
                          >
                              <v-sheet 
                                height="100%"
                              >
                                <v-row
                                  class="fill-height pointer"
                                  align="center"
                                  justify="center"
                                  @click="pushfile(it)">
                                    <div class="flex-row flex-item px-2 NLitem_div_icon_0">
                                      <div class="flex-item NLitem_div_icon_1">
                                        <v-icon
                                 
                                          :color= "fileiconss[fileext(it.file)]?fileiconss[fileext(it.file)].color : 'black'"
                                          :class="it.doc.length<4? 'icon flex-item': 'icon flex-item'"
                                          @click.stop = "download(it, $event.target)"
                                        >
                                          {{fileiconss[fileext(it.file)]?fileiconss[fileext(it.file)].icon: 'mdi-file'}}
                                        </v-icon>
                                      </div>
                                      
                                      <div
                                    class="flex-item NLitem_div_icon_2"
                                      align="center" 
                                      >
                                        {{ it.doc }}
                                      </div>
                                    </div>
                                </v-row>
                              </v-sheet>
                          </v-carousel-item>
                        </v-carousel>

              </div>
             
            </div>
             
            <div class="flex-item NLitem_2_1_2">  
              <!-- <strong class="minitext">Описание:</strong> -->
             
                         
                <div class="card-text rounded-lg px-3 pt-3 pb-2 news" v-html="replsrc(item.newstext)">
                </div>
             
            </div>
             </v-card>
          </div>
          
      </div>
      
    </div>

    <div class="flex-item flex-col NLitem" v-else>


      <div class="NLitem_1">
        
          <v-skeleton-loader  class="px-3 py-4"
            type="heading"                      
          >
          </v-skeleton-loader>
       
      </div>
      <div class="flex-item flex-col NLitem_2">
          <div class="flex-col NLitem_2_1"
            v-for="(item, i) in 3"
            :key="i"
          >
            <div class="flex-static_row NLitem_2_1_1 px-3"> 
              <div class="flex-item NLitem_2_1_1_1">
                <v-skeleton-loader
                  type="table-cell"                      
                >
                </v-skeleton-loader>                
              </div>
              <div class="flex-item NLitem_2_1_1_2">
                <v-skeleton-loader
                  type="table-cell"                      
                >
                </v-skeleton-loader>                 
              </div>
              <div class="flex-item NLitem_2_1_1_3 skelet">
                <v-skeleton-loader
                  type="table-cell"                      
                >
                </v-skeleton-loader> 
              </div>
            </div>
            <div class="flex-item NLitem_2_1_2 px-3 pb-7">  
              <v-skeleton-loader
                type="table-cell, image"                      
              >
              </v-skeleton-loader> 
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
  props: ['content','fileiconss','panel','header'],

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
          
          return itemcode.replaceAll('px', 'px !important;').replaceAll('" src="/','" src="'+ this.$http.defaults.baseURL).replaceAll("<p>","<p class='mb-1'>")
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
      linker(){
          
          return this.$http.defaults.baseURL + "media/"
      },
     
  }
}

</script>


<style lang="scss" >
@import '@/utils/colors.scss';

.myM {
      margin: 6px!important;
}

.myMt {
    margin: 2px 0px 0px 25px!important;
}

.NLitem {
    height: 97%;
}

.NLitem_1 {
    flex-basis: 30px;

        .v-skeleton-loader__heading {
          border-radius: 12px;
          height: 17px;
          width: 20%!important;
        }
}

.NLitem_2 {
    height: 39px;
    overflow-y: auto;

}



.NLitem_2_1 {
  margin-bottom: 1px;

      .skelet {
        width: 11%;
      }
}
.NLitem_2_1_1 {
  flex-basis: 25px;
  border-bottom: 1px solid #00000038;
}

.NLitem_2_1_2 {
  height: 80%;


    .v-skeleton-loader__image {
        height: 150px;
        border-radius: 8px;
        width: 99%;
    }
}


.NLitem_2_1_1_1, .NLitem_2_1_1_2, .NLitem_2_1_1_3 {
  width: 25%;
  align-self: self-end;

  .v-skeleton-loader__table-cell {
    width: 175px;
  }
}

.NLitem_2_1_1_2 {
  text-align: -webkit-center;
}

.NLitem_2_1_1_3 {

  height: 100%;
  .row {
          margin: 0px 30px 0 30px;
  }
.v-window__next, .v-window__prev {

    top: calc(40% - 8px)!important;
    background: none;

}
}

.NLitem_2_4 {
  width: 100%;
}

.NLitem_div_icon_0 {
  height: 100%;
}
.NLitem_div_icon_1 {
  width: 10%;
  align-self: flex-end;
  
    padding-bottom: 2px;
}

.NLitem_div_icon_2 {
  font-size:  0.8rem!important;
  overflow-y: auto;
  height: 1.3rem;
  width: 90%;
  align-self: flex-end;
}

.NLitem_div_icon_2::-webkit-scrollbar {width:0px;}

@media (max-width: 880px){
.NLitem_2_1_1 {
  flex-direction: column;
}

.NLitem_2_1_1_1, .NLitem_2_1_1_2, .NLitem_2_1_1_3{
  width: 100%;
  flex: 1 0 auto;
  align-self: center;
}
  .NLitem_2_1_1_2 {
      text-align: inherit;
}
}

  h2 {
      color: $bg-purple;
      font-size: 1rem !important;
  }

  .mcont{
    background-color: $bg-newsbg;
}

  .minitext{
    font-size: 0.7rem !important;
}
  .minitext2{
    font-size: 1rem !important;
}


  .icon {
  font-size: 1.2rem !important;
}


</style>