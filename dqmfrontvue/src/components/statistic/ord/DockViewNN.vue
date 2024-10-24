<template>
<div class="flex-item flex-row DVitem" v-if="content.attachments">
  <div class="flex-item flex-col DVitem_1">
    <v-card class="flex-item flex-col mb-1 flex-card_DVitem_1">
      <div class="flex-static_row DVitem_1_1">
        <div class="DVitem_1_1_1">
          <h2 class="pt-3 pl-4">ПРОСМОТР - {{maindoc.doc}}</h2>
        </div>
        <div class="flex-row DVitem_1_1_2">
          <v-icon  
            :color="maindoc.icon?maindoc.icon.color: ''" 
            v-text="maindoc.icon?maindoc.icon.icon:''"
            class="excel"
            @click="loadfile(maindoc, $event.target)"             
          >
          </v-icon>
        </div>
      </div>
      <div class="DVitem_1_2" v-if="preview">
        <pdf
          v-for="i in numPages"
          :key="i"
          :src="docsrc"
          :page="i">
        </pdf>
      </div>
      <div class="flex-item flex-row  DVitem_1_3" v-else>
        <h2>ДЛЯ ДАННОГО ФОРМАТА ФАЙЛА ПРЕДПРОСМОТР НЕДОСТУПЕН</h2>
      </div>
    </v-card>
  </div>
  <div class="flex-item flex-col DVitem_2">
    <v-card class="flex-item mb-1 flex-card_DVitem_2">
      <v-list
        class="pt-0"
        dense
      >
        <v-subheader>
          <h2 class="px-2">Распоряжение и Приложения</h2>
        </v-subheader>
        <v-list-item-group
          v-model="selectedItem"       
        >
          <v-list-item>
            <v-list-item-icon>
              <v-icon 
                class="icon"   
                :color="content.icon?content.icon.color: ''"                      
                v-text="content.icon?content.icon.icon:''"
                @click="loadfile(content, $event.target)"
              >
              </v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <div class="d-flex">
                <v-list-item-title
                  @click="tryview(content)"
                  v-text="content.doc">
                </v-list-item-title>
                <v-icon
                  class="icon"
                  @click.stop="loadfile(content, $event.target)" 
                  >
                  mdi-cloud-download
                </v-icon>
              </div>
            </v-list-item-content>
          </v-list-item>

          <v-list-item
            v-for="(item, i) in content.attachments"
            class="py-0"
            :key="i"
            @click="tryview(item)"
          >
            <v-list-item-icon>
              <v-icon
                v-text="item.icon?item.icon.icon:''"
                class="icon"
                :color="item.icon?item.icon.color: ''"  
                @click.stop="loadfile(item, $event.target)"
              >
              </v-icon>
            </v-list-item-icon>
            <v-list-item-content 
              class="py-0"
            >
              <div class="d-flex">
                <v-list-item-title            
                  v-text="item.doc"
                >
                </v-list-item-title>
                <v-icon
                  class="icon"
                  @click.stop="loadfile(item, $event.target)" 
                  >
                  mdi-cloud-download
                </v-icon>
              </div>
            </v-list-item-content>
          </v-list-item>

          <v-subheader>
            <h2 class="pa-2">ДОПОЛНИТЕЛЬНЫЕ ПИСЬМА</h2>
          </v-subheader>

          <v-list-item
            v-for="(item, i) in content.additions"
            :key="i+500"
            @click="tryview(item)"          
          >
            <v-list-item-icon>
              <v-icon
                v-text="item.icon?item.icon.icon:''"
                :color="item.icon?item.icon.color: ''"  
                class="icon"
                @click.stop="loadfile(item, $event.target)"    
              >
              </v-icon>
            </v-list-item-icon>
            <v-list-item-content >
              <div class="d-flex">
                <v-list-item-title      
                  v-text="item.doc"
                >
                </v-list-item-title>
                <v-icon
                  class="icon"
                  @click.stop="loadfile(item, $event.target)" 
                >
                  mdi-cloud-download
                </v-icon>
              </div>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>          
    </v-card>
  </div>
</div>
  <div class="flex-item flex-row DVitem" v-else> 
    <div class="flex-item flex-col DVitem_1">
    <v-card class="flex-item flex-col mb-1 flex-card_DVitem_1">
      <div class="flex-static_row DVitem_1_1">
        <!-- <div class="flex-item skelet_DVitem_1_1_1">1</div>
        <div class="flex-item skelet_DVitem_1_1_2">2</div> -->
      
        <v-skeleton-loader 
          class="flex-item pt-3 pl-4 "
          type="heading"                      
        >
        </v-skeleton-loader>
        <v-skeleton-loader 
          class="pt-3 pr-4"
          type="button"                      
        >
        </v-skeleton-loader>
    
 
      </div>
        <v-skeleton-loader 
          class="px-3 py-7 skelet_DVitem_1_1_1"
          type="image"                      
        >
        </v-skeleton-loader>

    </v-card>
  </div>
  <div class="flex-item flex-col DVitem_2">
    <v-card class="flex-item mb-1 flex-card_DVitem_2">
             <v-skeleton-loader 
          class="flex-item pt-3 pl-4 "
          type="heading, list-item-avatar, list-item-avatar,list-item-avatar,list-item-avatar"                      
        >
         </v-skeleton-loader>
                      <v-skeleton-loader 
          class="flex-item pt-4 pl-4 "
          type="heading, list-item-avatar, list-item-avatar,list-item-avatar,list-item-avatar"                      
        >
         </v-skeleton-loader>
    </v-card>
  </div>
  
  </div>
</template>
<script>
import pdf from 'vue-pdf'

import { bus } from "@/main";
export default {
  name: "dock-view",
  components: {
    pdf
  },
  props: ['content','fileiconss'],
  data(){
    return {      
      preview: false,
      maindoc:{},
      docsrc:"",
      numPages: null,      
      selectedItem: 0,
       
    }

  },
  
   methods:{
    handleFileload(data){
      // Ссылка для файла data = путь к файлу
    let srctfile = this.$http.defaults.baseURL +"media/"+ data
    if (this.maindoc.icon.icon=="mdi-file-pdf"){ 
    this.preview = true  
    this.docsrc = pdf.createLoadingTask(srctfile)
    this.docsrc.promise.then(pdf => {
			this.numPages = pdf.numPages;      
		});}
  
    else{
      this.preview=false
      this.docsrc = srctfile
       
    } 
    
    
  },
  tryview(item){         
      this.maindoc =  item;      
      this.handleFileload(item.file)    

  },

  fileext(filestr){
  let fileext = filestr.split(".")
  return fileext[fileext.length-1]

  },

  loadfile(file,el){ 
    bus.$emit('loadfileiconpushed', file)
    el.blur()
    },

  iconprep(arr){
    arr.forEach((el) => {
    let ic=this.fileext(el.file)
    el.icon = ic in this.fileiconss? this.fileiconss[ic]: {icon: 'mdi-file', color: "black"}
  }); 
  }
   },
  created(){
    bus.$on('pushfile', data=>{      
      data.icon = this.fileiconss[this.fileext(data.file)] 
         
      this.selecteditem = -1  
      this.tryview(data)
      
      
    })


  },
  
  mounted() {  
  
  this.content.icon = this.fileiconss[this.fileext(this.content.file)]  
  this.maindoc = this.content 

  this.iconprep(this.content.attachments)
  this.iconprep(this.content.additions) 
 
  
  this.handleFileload(this.content.file)  
   
  }

}


</script>


<style lang="scss">
@import '@/utils/colors.scss';

.DVitem{
    gap: 20px;
    align-self: center;
    width: 99.2%;
} 

.DVitem_1{
    width: 49%;
} 

.flex-card_DVitem_1 {
  overflow: auto;
  height: 10px;
}

.DVitem_1_1 {
   height: 35px;
   justify-content: space-between;

}

.skelet_DVitem_1_1_1 {
.v-skeleton-loader__image {
    height: 350px;
    border-radius: 0;
}
}



.DVitem_1_1_1 {
  width: 90%;
}
.DVitem_1_1_2 {
  justify-content: center;
  width: 10%;
}

.DVitem_1_2 {
  background: #eeebef;
}

.DVitem_1_3 {
  overflow-y: auto;
  background: #eeebef;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  h2 {
    text-align: center;
  }
}
.flex-card_DVitem_2 {
  overflow: auto;
  height: 10px;
}

.DVitem_2 {
  width: 49%;
  .v-skeleton-loader__heading {
    border-radius: 12px;
    height: 24px;
    width: 45%;
    margin: 0px 0 13px 0;
}
} 

.overhidden {
  overflow: hidden;
  height:46.3vh;
}

h2 {
  color: $bg-purple ;
  font-size: 1rem !important;
  }

.icon {
  font-size: 1.5rem !important;
}

</style>