<template>
<shell-with-loading :loading="loading" style="height: 100vh;">
<div class="grid-container FB1_grid pa-2 bwite">
  <div class="box_D"> 
     <h2 class="pl-3 pt-1">СПРАВОЧНАЯ ИНФОРМАЦИЯ</h2>
    
   
 </div>
<div class="box_A">
 
    <v-card class="flex-col FB1_item_A_1 pb-3">
    <!-- --------------------------------------------- -->
      <div class="flex-item flex-col flex-card_DVitem_1" v-if="content.docs.attachments">
        <div class="flex-static_row DVitem_1_1">
          <div class="DVitem_1_1_1">
            <h2 class="pt-3 pl-4">ПРОСМОТР - {{maindoc.doc}}</h2>
          </div>
          <div class="flex-row DVitem_1_1_2">
            <v-icon  
              :color="maindoc.icon?maindoc.icon.color: ''" 
              v-text="maindoc.icon?maindoc.icon.icon:''"
              class="excel"
              @click.stop="loadfile(maindoc, $event.target)"             
            >
            </v-icon>
          </div>
        </div>
        <div class="DVitem_1_2" v-if="preview">
          <pdf
            v-for="i in numPages"
            :key="i"
            :src="docsrc"
            :page="i"
            >
          </pdf>
        </div>
        <div class="flex-item flex-row  DVitem_1_3" v-else>
          <h2>ДЛЯ ДАННОГО ФОРМАТА ФАЙЛА ПРЕДПРОСМОТР НЕДОСТУПЕН<br>
          РЕКОМЕНДУЕМ СКАЧАТЬ ФАЙЛ
          </h2>
        </div>
    </div>
  <!-- --------------------------------------------- -->
    <div class="flex-item flex-col skelet_DVitem" v-else>
      <div class="flex-item flex-row skelet_DVitem_0">
        <v-skeleton-loader 
          class="flex-item pl-2 pt-3 "
          type="heading"                      
        >
        </v-skeleton-loader>
        <v-skeleton-loader 
          class="flex-item pr-3 pt-3 skelet_DVitem_1"
          type="button"                      
        >
        </v-skeleton-loader>
        </div>
        <div class="skelet_DVitem_0_1 flex-col">
        <v-skeleton-loader 
            class="flex-item px-3 py-7 skelet_DVitem_1_1_1"
            type="image"                      
          >
          </v-skeleton-loader>
        </div>
  </div>
  </v-card>


 </div>
 <div class="box_B">
  <v-card class="flex-col FB1_item_B_1 pb-2">
<!-- --------------------------------------------- -->
    <div class="flex-item FB1_card_B_1" v-if="content.docs.attachments">
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
                :color="content.docs.icon?content.docs.icon.color: ''"                      
                v-text="content.docs.icon?content.docs.icon.icon:''"
                @click.stop="loadfile(content.docs, $event.target)"
              >
              </v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <div class="d-flex">
                <v-list-item-title
                  @click="tryview(content.docs)"
                  v-text="content.docs.doc">
                </v-list-item-title>
                <v-icon
                  class="icon"
                  @click.stop="loadfile(content.docs, $event.target)" 
                  >
                  mdi-cloud-download
                </v-icon>
              </div>
            </v-list-item-content>
          </v-list-item>

          <v-list-item
            v-for="(item, i) in content.docs.attachments"
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

        <div v-for="el in header" :key="el.dictkey">
           <v-subheader v-if="content.docs[el.dictkey].length">
            <h2 class="pa-2">{{el.text}}</h2>
          </v-subheader>
        
               <v-list-item
                  v-for="(item, i) in content.docs[el.dictkey]"
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
        </div>
        </v-list-item-group>
      </v-list>          
    </div>
        <div class="flex-item mb-1 flex-card_DVitem_2" v-else>
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
    </div>
    <!-- --------------------------------------------- -->
  </v-card>
 </div>
 <div class="box_C">
  <div class="flex-col FB1_item_C_1">
            <v-card class="flex-item flex-col flex-card_item_3_2">
                <faq-list  :content="content.faq"/>
            </v-card>
  </div>
 </div>
</div>
</shell-with-loading>
</template>

<script>
import { clearAxios } from '@/utils/axios-api'
import { bus } from "@/main";
import pdf from 'vue-pdf'
// import  DockView  from '@/components/statistic/ord/DockView.vue'
import NewsList from '@/components/statistic/ord/NewsList.vue'
import FaqList from '@/components/statistic/ord/FaqList.vue'
import globalFuncs from '@/utils/helper'
export default {
   name:"fb1Docs",
   components: {    
    pdf,
    NewsList,
    FaqList
 
  },
   data(){
     return {
      loading:false,
       header:[{dictkey:'additions',
                text:"Дополнительные письма"}, 
                {dictkey:'contactinfo',
                text:"Перечни сотрудников, отвечающих за нормализацию данных"}],
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
        
        
      },
      preview: false,
        
        docsrc:"",
        numPages: null,      
        selectedItem: 0,
        maindoc:{},
        mini: 40,
        maxi: 89,
      
       drawer: null,
       panel: true, 
       content: {
         news: [],
         docs: {},
         faq: [],         
       }, 
     }
   },

  // watch: {
  //   drawer(newValue) {   
  //       this.panel = !newValue
  //   },
  //    },
  methods:{
    fileext(filestr){
    let fileext = filestr.split(".")
    return fileext[fileext.length-1]

    },
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
        
          });
   
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
    this.loading=true
   
    
  },
  async mounted() { 
  globalFuncs.permissiondenied(this.$route.path)   
  const data = await this.$http
            .get('/api/statistic/fb1/reporting/docs/')  
  this.content = data.data;

  this.content.docs.icon = this.fileiconss[this.fileext(this.content.docs.file)]  
  this.maindoc = this.content.docs

  for (let val of Object.values(['attachments', 'additions','contactinfo'])){
  
    this.iconprep(this.content.docs[val])
    
  }
   
  // this.iconprep(this.content.docs.attachments)
  // this.iconprep(this.content.docs.additions) 
  // this.iconprep(this.content.docs.contactinfo) 
  
  this.handleFileload(this.content.docs.file)    
  },
 
}
</script>



<style lang="scss" >
@import '@/utils/colors.scss';

.FB1_grid {
  gap:8px;
  background: $bg-newsbg;
  overflow-y: auto;
  grid-template-rows: 0fr 1fr 1fr 1fr 1fr ;
  grid-template-columns: 1fr 1fr 1fr 1fr   1fr 1fr 1fr 1fr;
  grid-template-areas:
    "D D D D   D D D D"
    "A A A A   B B B B"
    "A A A A   B B B B"
    "A A A A   C C C C"
    "A A A A   C C C C"
    ;
}

.box_A {
  grid-area: A;
}
.box_B {
  grid-area: B;
}
.box_C {
  grid-area: C;
}
.box_D {
  grid-area: D;
}

@media (max-width: 1500px) {
.FB1_grid {
  gap: 0;
  grid-template-areas:
    "D D D D   D D D D"
    "A A A A   A A A A"
    "A A A A   A A A A"
    "B B B B   B B B B"
    "C C C C   C C C C"
    ;
}
.box_A {
  min-height: 450px;
  padding-bottom: 15px;
}
.box_B {
  min-height: 350px;
  padding-bottom: 15px;
}
.box_C {
  min-height: 350px;
}
.box_D {
  min-height: 50px;
}
}

.FB1_item_A_1, .FB1_item_B_1, .FB1_item_C_1,  .FB1_item_D_1 {
  height: 100%;
}

.FB1_item_D_1 {
  justify-content: center;
}

.FB1_h_D_1 {
  align-self: center;
  font-size: 1.4rem!important;
  .v-skeleton-loader__heading {
    width: 12%;
  }
}

.FB1_card_B_1 {
  overflow: auto;

}


.flex-card_DVitem_2 {
  overflow: auto;
  height: 10px;
}
.skelet_DVitem_0 {
  height: 4%;
}

.flex-card_DVitem_1 {
  overflow: auto;
  height: 10px;
}

.DVitem_1_1 {
   height: 35px;
   justify-content: space-between;

}

.skelet_DVitem_1 {
    text-align: -webkit-right;
}
.skelet_DVitem_0_1 {
  height: 96%;
}
.skelet_DVitem_1_1_1
{

.v-skeleton-loader__image {
    height: 100%;
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

.skelet_FBitem_2 {
 
  height: 500px;
}

.skelet_FBitem_2_1 {
  height: 56.2%;
 background: rgb(255, 255, 255);

}

.skelet_FBitem_2_1_1 {
  padding: 16px 23px 16px 15px;
  .v-skeleton-loader__heading {
    border-radius: 12px;
    height: 32px;
    width: 20%;
}
}
.skelet_FBitem_2_1_2 {
  margin: 0 9px 7px 9px;
}

.FBitem_1 {
    min-height: 43px;
    align-items: center;
    .v-skeleton-loader__heading {
        border-radius: 12px;
        height: 24px;
        width: 12%;
    }
}


.FBitem_2_1{
    height: 100%;
    gap:20px;

}


.flex-card_item_3_2 {
        height: 100%;
}



@media (max-width: 550px) {
    .FBitem_2{
        display: none;
    }
}
</style>