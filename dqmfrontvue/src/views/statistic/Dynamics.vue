<template>
 <shell-with-loading :loading="loading" style="height: 100vh;">
<v-container fluid class="vh-100 flex-col bg5">
  <v-row class="flex-grow-0">
    <v-col class="pa-0">
      <filters-bar
        @sendData="updateData"
        @clear="clearit"
        :header="`ДИНАМИКА`"
      >
        <template v-slot:filterslist>
          <v-col  
            class="flex-grow-0 pl-1 pb-5 align-self-center namedynamik"
          >
            <h4 class="h4dyn">Статистический отчет по состоянию на:</h4>
          </v-col>
         <f-datepicker :field="'date_unloading'" :events="eventarr"/>
        </template>
      </filters-bar>
    </v-col>
  </v-row>
  <!-- Контент -->
  <v-row>
    <v-col class="flex-col colordyn">
      <v-card
        class="flex-grow-1 flex-col vcard"  
      >
        <div class="flex-col ma-3 flex-grow-1">
          <v-row v-if="content">
            <v-col>
               <v-timeline
                  dense
                >
                <v-timeline-item
                  v-for="(value,key) in content"
                  :key="key"
                  small
                >
                  <v-row class="pt-1" >
                   
                    <v-col
                      class="pl-0 namedynamik align-self-center col_month flex-grow-0"
                    >
                      <strong class="month">{{key}}</strong>
                    </v-col>
                    <v-col
                      class="pl-0 pt-1"
                    >
                      <v-expansion-panels
                        focusable
                        class="py-2"
                      >
                        <v-expansion-panel  
                          v-for="(val,k) in value"
                          :key="k"
                         
                        >     
                          <v-expansion-panel-header>      
                            Динамика по состоянию на: {{k}}
                          </v-expansion-panel-header>
                          <v-expansion-panel-content 
                            class="dynamic_expansion"
                          >
                            <v-list
                              dense
                            >
                              <v-list-item
                                v-for="(item,index) in val"
                                @click.stop="loadfile(item, $event.target)"
                                :key="index"
                                class="minlistdin"
                               
                              >
                                <v-list-item-icon
                                class="smallerdin"
                                >
                                  <v-icon
                                  
                                    class="excel2"
                                    :color="iconprep(item.file).color"
                                  >
                                    {{iconprep(item.file).icon}}
                                  </v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                  <v-list-item-title
                                    v-text="item.name"
                                  >
                                  </v-list-item-title>
                                </v-list-item-content>
                              </v-list-item>
                            </v-list>
                          </v-expansion-panel-content>
                        </v-expansion-panel>
                      </v-expansion-panels>
                    </v-col>
                  </v-row>
                </v-timeline-item>
              </v-timeline>
            </v-col>
          </v-row>
                            <v-row v-else>
                             
                             <div class="d-flex flex-col justify-center mx-auto "><h2 style="color:#AFAFAF">Отсутствуют данные</h2> </div>
                   
                  </v-row>
        </div>
      </v-card>
    </v-col>
  </v-row>
</v-container>
 </shell-with-loading>
</template>

<script>
import { clearAxios } from '@/utils/axios-api'
import moment from 'moment';
import  datepickerf  from "@/utils/datepickerf.js"
import { createNamespacedHelpers } from "vuex";
import FDatepicker from '../../components/UI/FDatepicker.vue';
import globalFuncs from '@/utils/helper'
const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");

export default {
  components: { FDatepicker },
    name:"dynamics",
    mixins:[datepickerf],
   
    data(){
        return{
            loading: true,
            datefrom:"",
            dateto:"",
            datefilter:"",
            eventarr:[],
            content:{},
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
                          bmp:  {icon: 'mdi-image', color: "#17A745"}
      },

        }
    },
    methods:{
        ...mapMutations(["setFields"]),
        ...mapActions(["clear", "getFilters", "addFilter", "activefilters"]),
        fileext(filestr){
            let fileext = filestr.split(".")
                 return fileext[fileext.length-1]
                 },

        iconprep(el){

            let ic=this.fileext(el)
            
            return ic in this.fileiconss? this.fileiconss[ic]: {icon: 'mdi-file', color: "black"}
             
            
    },
    clearit(){
      this.clear()
      this.updateData()
    },
    loadfile(item,el){
        this.loading=false
        clearAxios({
        url: item.file,
        method: "GET",
        responseType: "blob"
      }).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;        
        link.setAttribute("download", item.name +"." + this.fileext(item.file)); //or any other extension
        document.body.appendChild(link);
        link.click();
        
        link.remove()
        el.blur()
        this.loading=true
      });
        
        el.blur()
        
    },
        updateData(){
        
        return new Promise(async (resolve, reject) => {
          
        const filters = await this.activefilters();
        
         this.$http
                    .get('/api/statistic/dynamics/list/', {
                        params: {
                            filters: JSON.stringify({
                                ...filters,
                                
                            }),
                        },
                    })
                    .then((res) => { 
                     
                      if (res.data.results.length>0){    
                        this.content = this.groupper(res.data.results)}
                        else{
                          this.content=false
                        }
                      
                      })        
        })
        },
    groupper(data){
        let grouppedob={}
        data.forEach(el => {
            let date = moment(el.date_unloading,'YYYY-MM-DD')
            let daymonth = date.format("DD MMMM")
            let key = `${this.capitalizeFirstLetter(date.format("MMMM"))}  ${date.format("Y")}`;           
            if (!(key in grouppedob)) grouppedob[key]={}            
            if(!(daymonth in grouppedob[key])) grouppedob[key][daymonth]=[]
            grouppedob[key][daymonth].push(el)           
        });
        return grouppedob 
    },
    capitalizeFirstLetter(string) {
    return string[0].toUpperCase() + string.slice(1);
}


    },
    
    mounted(){
      globalFuncs.permissiondenied(this.$route.path)
        moment.locale('ru')
        this.setFields({
            date_unloading: {
                module: "select",
              
            },
           
        });
         
        this.getFilters({
            dynamicdate: [{ name: "date_unloading", sort: "-" }],
            
        }).then(async (data) => {
          
            if(data.date_unloading.length>1){         
        
                this.eventarr=data.date_unloading
                
             }
             else if(data.date_unloading.length==1){
              this.eventarr=[data.date_unloading[0],data.date_unloading[0]]
             }
            this.updateData()     
           
        });
    }
}
</script>

<style lang="scss">
    @import '@/utils/colors.scss';
  .minlistdin {
  min-height: 25px !important;
}
.smallerdin{
  height: 16px !important;
}
.excel2 {
    cursor: pointer;
    background: white;
    font-size: 1.2rem !important;
}

.namedynamik {
  white-space: nowrap;
}    

.h4dyn {
  color: $bg-purple;
}

.month {
    background: $bg-maincont;
    padding: 4px 14px;
    border-radius: 20px;
}

.col_month {
  min-width: 7vw;
}

.colordyn {
  background: $bg-newsbg;
}

.position {
  text-align: end;
}

.vcard {
  height: 50px;
  overflow: auto;
}

.dynamic_expansion {
  .v-expansion-panel-content__wrap {
    padding: 0 5px 0px;
  }
}


</style>