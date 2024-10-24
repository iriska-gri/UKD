<template>
  <div class="flex-item flex-col mb-3 mt-1 FLitem" v-if="content.length>0">
    <div class="flex-static-row mb-3 FLitem_1">
      <h2 class="pt-3 pl-4">ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ</h2>
    </div>
    <div class="flex-item px-4  FLitem_2">
      <v-expansion-panels
        elevation-0
        class="flex-item" >
        <v-expansion-panel
          class="FBmcont noborder"
          v-for="(item,i) in content"
          :key="i"
        >
          <v-expansion-panel-header 
          class="px-2 py-2 maincont tobottom FBmcont"     
          @click= showdet(i)
          >
            <div class="fullh pt-1">
              <strong class="">
                {{item.order}}. {{item.question}}
              </strong>
            </div>
            <template
              v-slot:actions        
            >
              <div class="d-flex align-end">
                <div class="supersmall">
                  {{showdetails[i]?"Скрыть подробности":'Показать подробности'}}
                </div>
                <v-icon>
                  mdi-chevron-down
                </v-icon>
              </div>
            </template>
            
            </v-expansion-panel-header>
            <v-expansion-panel-content 
              class="FBmcont px-1" 
            >
            <!-- <hr> -->
              <div v-html="replsrc(item.answer)"></div>
              <v-row v-for="(x, indx) in item.files" :key="indx">
                <v-col class="pt-0 pr-1 flex-col flex-grow-0 ">
                <v-icon 
                
                  class="icon pr-1"   
                  @click.stop="loadfile(x)"
                    :color="iconing(x.file, 'color')"
                  
            
                
                >
                  {{iconing(x.file, 'icon')}} 
              
                </v-icon>
                  </v-col>
                <v-col class="flex-grow-0 pt-0 pl-1">
  <span @click.stop="loadfile(x)" class="pointer ">{{x.doc}}</span>
                </v-col>
            
              
        

              </v-row>
         
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
    </div>
   
  </div>

     <div class="flex-item flex-col mb-3 FLitem" v-else>
      <v-skeleton-loader
        class="px-4 py-4"
        type="heading, button, button, button, button, button, button, button, button, button, button"                      
      >
      </v-skeleton-loader>
      </div>

</template>

<script>
import * as moment from "moment";
import { clearAxios } from '@/utils/axios-api'

export default {
  name: "news-list",
  props: ['content','panel'],

  data(){
      return{
        showdetails:[],
        fileiconss:{
        pdf: {icon:"mdi-file-pdf", color: "red"},
        txt: {icon: 'mdi-file-document', color: "black"},
        xls: {icon: 'mdi-microsoft-excel', color: "#1F6E43"},
        xlsx: {icon: 'mdi-microsoft-excel', color: "#1F6E43"},
        doc: {icon: 'mdi-microsoft-word', color: "#313EE7"},
        docx: {icon: 'mdi-microsoft-word', color: "#313EE7"},  
        jpg: {icon: 'mdi-image', color: "#17A745"},
        jpeg: {icon: 'mdi-image', color: "#17A745"},
        png: {icon: 'mdi-image', color: "#17A745"},
        bmp:  {icon: 'mdi-image', color: "#17A745"},
        any:{icon:"mdi-file", color:"gray"}
        
        
      },
      }
  } ,
  mounted() {
      moment.locale('ru')
      this.showdetails = this.content.length?Array(this.content.length-1).fill(0):[]

  }, 
  methods: {
    iconing(file, key) {
     let fex = this.fileext(file)
      if (!(fex in this.fileiconss)){
        fex="any"
      }
      return this.fileiconss[fex][key]
   
      
    },

      fileext(filestr){
  let fileext = filestr.split(".")
  return fileext[fileext.length-1]

  },

    loadfile(file){ 
    this.loading=false
         
      clearAxios({
          url: this.$http.defaults.baseURL +"media/"+ file.file,
          method: "GET",
          responseType: "blob" // important
        }).then(response => {
        

          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;        
          link.setAttribute("download", file.doc +"." + this.fileext(file.file)); //or any other extension
          document.body.appendChild(link);
          link.click();
          link.remove()
         
          this.loading=true
        
          })
    },
       showdet(indx){       
         
         if(this.showdetails[indx]!=1){ 
           this.showdetails.fill(0)
           this.showdetails[indx]=1}
          else{
            this.showdetails.fill(0)
          }

       },
       UTCDate(date) {
           
            return moment(date, "YYYY-MM-DD").format("LL");
        },
        replsrc(itemcode){
          return itemcode.replaceAll('" src="/','" src="'+ this.$http.defaults.baseURL).replaceAll('px', 'px !important;')
      },
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

.FLitem {
    // height: 50px;
    overflow: auto;
    // background: #00a7fa;
    // width: calc(100% - 17px);
    .v-skeleton-loader__heading {
      border-radius: 12px;
      height: 18px;
      width: 28%;
      margin-bottom: 15px;
      
  }


  .v-skeleton-loader__button {
    border-radius: 4px;
    height: 33px;
    width: 99%;
  }
}

// .FLitem_1 {
    // height: 40px;
//     background: red;
// }


h2 {
    color: $bg-purple;
    font-size: 1rem !important;
    }
hr {
  border: none;
  color:  $bg-newsbg;
  background-color:  $bg-newsbg;
  height: 2px;
}

.FBmcont { 
    background-color: $bg-newsbg; 
    border-radius: 5px;  
    .v-expansion-panel-content__wrap{
      padding: 8px;
    }
}

.FBmcont.v-expansion-panel-header--active {
  background-color: $bg-white!important
}

.minitext {
  font-size: 0.7rem !important;
}
.supersmall {
  font-size: 0.65rem !important;
}

.scroller {
    overflow-y:scroll;
}
.noborder {
  border-width:10px !important;
}

.fullh{
  height: 100% !important;
  }
 
.tobottom{
    min-height: 2em !important;
    display: flex !important;
    align-items: flex-end !important;
}

.bg1 {
  background: red;
}

</style>