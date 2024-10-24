<template>
    <div class="grid-container">
      <div class="box_Dash_O">
        <v-card class="flex-staic-row  mb-2 DB_card_item_1">
          <filters-bar 
            @clear="clear"
            @sendData="updateData"
            :header="'ДАШБОРД'"
          >
          <template v-slot:filterslist>
            <v-col
              class="pa-0 px-1 align-self-center pb-2"
              lg="2"
              md="6"
              sm="12"
              v-for="(item, i) in date_unloading"
              :key="i"
            >
              <v-menu 
                v-model="item.model"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template
                    v-slot:activator="{on, attrs}"
                    class=" ma-0 align-self-start "
                >
                  <layout-label
                      :title="i==0?'Выберите дату с:':'Выберите дату по:'"      
                  />
                    <v-text-field
                        dense
                        solo
                        :value="formatDate(item.$value)"              
                        type="date-local"              
                        placeholder="дд.мм.гггг"
                        @focus="datekey=i"
                        @input="oninput"
                        v-bind="attrs"
                        hide-details
                        v-on="on"
                        class="pt-0"
                        title="Код паспорта"
                      >
                    </v-text-field>
                </template>
                <v-date-picker
                  :first-day-of-week="1"
                  :min="datefrom1" 
                  :max="dateto1"
                  :events="eventarr"
                  event-color="green lighten-1"
                  v-model="item.$value"
                  @input="i==1?
                  datefrom = false
                  :dateto=false"  
                >
                </v-date-picker>
              </v-menu>
            </v-col>
            <v-col
              class="pa-0 align-self-end"
              lg="3"
              md="6"
              sm="12"
            >
              <f-multi-select
                :field="'region__name'"
                title="Регион"
              >
              </f-multi-select>
            </v-col>  
            <v-col
              class="pa-0 align-self-end"
              lg="3"
              md="6"
              sm="12"
            >
              <f-multi-select
                :field="'passport__code'"
                title="Код паспорта"
              >
              </f-multi-select>
            </v-col> 
        
            <!-- <div class="flex-item pr-4 DB_item_2">
              <f-multi-select
                :field="'region__name'"
                title="Регион"
              >
              </f-multi-select>
            </div>
            <div class="flex-item pr-4 DB_item_3">
              <f-multi-select
                  :field="'passport__code'"
                  title="Код паспорта"
              >
              </f-multi-select>
            </div> -->
          </template>
          </filters-bar>
        </v-card>   
      </div>
      <div class="box_Dash_A">
        <div class="flex-row h-100">
          <div
            ref = "Dash_A_ref_1"
            class="flex-item h-100 DB_item_1_1">
              <linear
              class="pt-3 pl-5"
              :chartData='linear1'
              :chartOptions='chartLineOptions'
             
              />
              <!--  :height="calcheightchart(8.3)" -->
          </div>
          <div class="flex-item h-100 DB_item_1_2">
            <linear
              class="pt-3 pl-5"
              :chartData='linear2'
              :chartOptions='chartLineOptions'
              
            />
          </div>
        </div>
      </div>
      <div class="box_Dash_B mx-4">
        <div class="flex-row pt-2 h-100 w-100">
          <rectangle-card
            class="halfh"
            :countdata="helptextmaxdate"
            :way='wayhelp'
            :max_date="content.max_date"
          /> 
        </div>
      </div>
        <div class="box_Dash_C"></div>
        <div class="box_Dash_D h-100 mx-4">
          <div class="flex-col h-100 w-100">
              <div class="flex-col DB_item_4_1">
                <quadro-card
                  class="halfh"
                  :countdata="totalobject.countDataNewVPND"
                />
              </div>
              <div class="flex-col  DB_item_4_2">
                <quadro-card
                  class="halfh"
                  :countdata="totalobject.corrected"
                />
              </div>
              <div class="flex-col DB_item_4_3">
                <quadro-card
                  class="halfh"
                  :countdata="totalobject.countDataVPND"
                />
              </div>
          </div>
        </div>
        <div class="box_Dash_E">
          <div class="h-100 flex-row pl-3">
            <div class="flex-item h-100 DB_item_5_1">
              <mybar
                class="px-3"
                :chartData='barchart[1]'
                :chartOptions='chartBarOptions2'
                :height ="calcheightchart(42)"
              />
            </div>
            <div class="flex-item h-100 DB_item_5_2">
              <mybar
                class="px-3"
                :chartData='barchart[0]'
                :chartOptions='chartBarOptions'
                :height ="calcheightchart(42)"
              />
            </div>
          </div>
        </div>
    </div>

</template>


<script>
//  help_text="1 - Старая , 2 - Новая, 3 - ВПНД"
import { createNamespacedHelpers } from "vuex";
const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");
import moment from "moment";
import QuadroCard from '@/components/statistic/dashboard/QuadroCard.vue'
import RectangleCard from '@/components/statistic/dashboard/RectangleCard.vue'
import Mybar from '@/components/statistic/dashboard/mybar.vue'
import Don from '@/components/statistic/dashboard/don.vue'
import Linear from '@/components/statistic/dashboard/linear.vue'
import  chartlogic  from "@/utils/charts/chartlogic.js"
import { bus } from "@/main";
import  datepickerf  from "@/utils/datepickerf.js"
import globalFuncs from '@/utils/helper'
export default {
   name: "dashboard",
    components: {        
        Mybar,
        Don,
        Linear,
        QuadroCard,
        RectangleCard,
         
    },
  mixins:[chartlogic,datepickerf],
    data() {return {
      datekey:0,
      barchart: [{},{}],
      open: false,
      date: null,
      linear1: {},
      linear2: {},
      chartLineOptions: {           
           scales: {      
                xAxis: {      
                display:true,
                grid:{
                    lineWidth:0, 
                    drawBorder: false}, 
                },
                yAxis:{
                    display:false
                }      
             },
              elements:{point:{radius: 2}},
            // elements:{point:{radius: true}},
                responsive: true,
                // maintainAspectRatio: false,
                plugins:{ 
                     datalabels: {
                                display:false,                               
                                },                         
                                
                    legend: {display:true},
                    tooltip: {
                    enabled: true,
                    backgroundColor: '#43425D'
                },         
                },
                },
      date_unloading: [{},{}],
      dateFormatted: null,
      datefrom: false,
      dateto: false,
      datefrom1: "",
      dateto1: "",
      eventarr:[],
      label:"",
      content:{},
      barscharts:[],
      pre_data_linearchart1: {countDataVPND: {label:'ВПНД', fill:true, borderColor: 'rgb(79, 129, 189)',backgroundColor:'rgba(79, 129, 189, 0.5)',tension: 0.1, data:[]},
                              countDataNew: {label:'Новые НД', fill:true, borderColor: 'rgb(246, 220,224)',backgroundColor:'rgba(246, 220,224,0.7)',tension: 0.1, data:[]}, 
                              countDataOld: {label:'Старые НД', fill:true, borderColor: 'rgba(196, 152, 210,255)',backgroundColor: 'rgba(196, 152, 210,0.5)',tension: 0.1, data:[]},
                },
      pre_data_linearchart2: {
                              countDataNewVPND: {label:'Новые НД+ВПНД', fill:true, borderColor: 'rgb(246, 220,224)',backgroundColor:'rgba(246, 220,224,0.7)',tension: 0.1, data:[]}, 
                              corrected: {label:'Исправлено НД', fill:false, borderColor: 'rgba(19, 212, 194,255)', backgroundColor:'rgba(19, 212, 194,255)', tension: 0.1, data:[]},
                },

      totalobject:{ corrected: {text:"Всего исправлено ошибок за выбранный период", gradient:["#19D3C1", "#148579"], count:0},
                      countDataNew:{text:"Всего новых ошибок за выбранный период", gradient:["#FB708A", "#DD6EB7", "#8264CE"], count:0},
                      countDataNewVPND:{text:"Всего новых + ВПНД за выбранный период", gradient:["#FB708A", "#DD6EB7", "#8264CE"], count:0},
                      countDataVPND:{text:"Всего вновь появившихся ошибок за выбранный период", gradient:["#FD9467", "#C7385B"] , count:0}}
    ,
      wayhelp:['countDataNew','countDataOld','countDataVPND'],
      helptextmaxdate: {countDataOld:{text:"Старые НД", icon:"mdi-pill", count:0},
                        countDataNew:{text:"Новые НД", icon:"mdi-debug-step-into", count:0},
                        countDataVPND:{text:"ВПНД", icon:"mdi-alert-outline",count:0}, 
      },
      chartOptions: { responsive: true,                
                     
                      plugins:[{legend: {
                                display: false}},
                                {title: {
                                display: true,
                                text: 'Топ 10 паспортов по количеству ошибок на конец периода'
                              }},                          
                                                           
                              ],
                    
                         },      
      chartBarOptions: this.chartBarOpt('ТОП-10 паспортов по количеству ошибок на конец периода','passport__code'),
      chartBarOptions2: this.chartBarOpt('ТОП-10 регионов по количеству ошибок на конец периода', 'region__name')
    }

},
created(){
  bus.$on('addFilBar',data=>{

  
  // let tp = 
  // let a={ tp : {value: data.val},}
 
  this.addFilter({
                key: data.type,
                value: [data.val]
            });
            
            this.updateData()
            }

  )
  
},

async mounted() { 
globalFuncs.permissiondenied(this.$route.path)



this.setFields({    region__name: { module: "mult" },
                    passport__code: { module: "mult"},
                    date_unloading: { module: "chain", 
                    correct: (arr) => {   
                    let narr=[]             
                    arr.map((el) => {narr.push(this.$changeFormatDate(el))})                    
                   
                    return narr},
            },},)
  this.getFilters({
     ens: [{ name: "date_unloading", sort: "" }],
     regions: [{ name: "region__name", sort: "", related_name: "name" }],
     ensPass: [{ name: "passport__code", sort: "", related_name: "code" },],
     
  }).then(async (data) => {
    
    if(data.date_unloading.length>1){    
      
      this.$set(this.date_unloading, 0, {$value:data.date_unloading[0], model:this.datefrom})
      this.$set(this.date_unloading, 1, {$value:data.date_unloading[data.date_unloading.length-1], model: this.dateto})
      // this.date_unloading[1] = data.date_unloading[data.date_unloading.length-1]
      this.datefrom1=data.date_unloading[0]
      this.dateto1=data.date_unloading[data.date_unloading.length-1]
      this.eventarr=data.date_unloading
      this.updateData()
    }

      })

   
  // this.canvascalc()
  // this.calcheightchart(8.3)
},


methods:{
  
  ...mapMutations(["setFields", "setIncludeFilters"]),
  ...mapActions([
            "clear",            
            "getFilters",
            "addDate",
            "addFilter",
            "activefilters",
        ]),
 
  calctopbanner(data){
    for (let key of Object.keys(this.helptextmaxdate)){      
                  
              this.helptextmaxdate[key].count=data[data.length-1][key]  
                       
  }
 
  },
 
    
  calctotaldata(data){
    
    for (let i=0;i<data.length;i++){
          for (let key of Object.keys(this.totalobject)){
            if(i==0){
              this.totalobject[key].count=0
              continue
            }
           
            this.totalobject[key].count += Number(data[i][key])}
    }

  },

  


  compareandadd(one,two){
    for (let [key,val] of Object.entries(two)){
      one[key]=val
    }  
    return one
  },
  
  update() {
     
      this.$value = this.dateFormatted;
      this.$emit('change', this.dateFormatted);
        },
 
  
  
  updateData(){   
   
         return new Promise(async (resolve, reject) => {
                await this.addDate({
                period: true,
                field: "date_unloading",
                value: [ this.$changeFormatDate(this.date_unloading[0].$value),  this.$changeFormatDate(this.date_unloading[1].$value)],
                });
                const filters = await this.activefilters();
                
                this.$http
                    .get('/api/ens/dashboard/', {
                        params: {
                            filters: JSON.stringify({
                                ...filters,
                                
                            }),
                            
                         
                        },
                    })
                    .then((res) => {  
                     
                       this.content=res.data   
            
                       
                       this.barchart= [this.builddata4chart(this.content.toppassportserrors,'passport__name', 'passport__code', false,0,this.colorbarchart(this.content.toppassportserrors, "passport__code", filters,['#D2627B','#EB2A54'])),
                                      this.builddata4chart(this.content.topregionserrors,'region__name', 'region__tax_code', false,0,this.colorbarchart(this.content.topregionserrors, "region__name", filters))
                       ]
                   
                        this.calctopbanner(this.content.totalerrorperiod)
                        this.calctotaldata(this.content.totalerrorperiod)
                        
                        this.summer(this.content.totalerrorperiod,['countDataNew',"countDataVPND"],'countDataNewVPND' )
                        
                        this.totalobject.countDataNewVPND.count=this.totalobject.countDataVPND.count+this.totalobject.countDataNew.count
                        this.linear1=this.data4liinearchart(this.content.totalerrorperiod,this.pre_data_linearchart1,"date_unloading")
                        this.linear2=this.data4liinearchart(this.content.totalerrorperiod,this.pre_data_linearchart2,"date_unloading")
                        resolve(res.data);
                        
                    });
            });

    
  },
  
  summer(data,keys,newkey){
    for (let i=0;i<data.length;i++){
      data[i][newkey]=0
      for (let n of keys){
        data[i][newkey]+=Number(data[i][n])
      }
    }
  },
  // async updateDashboard(){
  //   // обновление дб
  //   const filters = this.getfilters()
  // }

},
 watch: {
        datefrom (val) {
            this.dateFormatted = this.formatDate(this.datefrom)
        },
        dateFormatted(val) {
            this.update();
        }
    },
  beforeDestroy () {
    bus.$off('addFilBar', false)
 },
}
</script>

<style lang="scss" scoped>
@import "@/utils/colors.scss";

.grid-container {
  grid-template-rows: 0fr 1fr 1.2fr 1fr 1fr ;
  grid-template-columns: 2fr 2fr 2fr 2fr   2fr 1fr 0.1fr 2fr   1fr 1fr 1fr 1fr;
  grid-template-areas:
    "O O O O   O O O O   O O O O"
    "A A A A   A A A B   B B B B"
    "A A A A   A A A C   C D D D"
    "E E E E   E E E E   E D D D"
    "E E E E   E E E E   E D D D"
    ;
    overflow-x: hidden;
}

.box_Dash_O {
  grid-area: O;
  min-width: 390px;
}

.box_Dash_A {
  grid-area: A;

}
.box_Dash_B {
  grid-area: B;
}

.box_Dash_C {
  grid-area: C;
}

.box_Dash_D {
  grid-area: D;
  min-height: 350px;
}

.box_Dash_E {
  grid-area: E;
  min-height: 250px;
}

.DB_card_item_1 .Fil_item_2 {
  flex-wrap: wrap;
}

.DB_card_item_1 .Fil_item_3 {
  margin-top: 0!important;
}

.DB_item_1_1, .DB_item_1_2, .DB_item_5_1, .DB_item_5_2 {
  width: 250px;
}

.DB_item_4_1, .DB_item_4_2, .DB_item_4_3 {
  min-height: 31.5%;
  padding-top: 20px;
}

.DB_item_1, .DB_item_2,.DB_item_3 {
  min-width: 300px;
  width: 10%;
}

@media (max-width: 1500px) {
  .grid-container {
    display: grid;
    grid-template-areas:
      "O O O O   O O O O   O O O O"
      "B B B B   B B B B   B B B B"
      "D D D D   D D D D   D D D D"
      "A A A A   A A A A   A A A A"
      "E E E E   E E E E   E E E E"    
      ;
  }

  .box_Dash_C {
    display: none;
  }

  .grid-container {
    overflow-y: auto;
  }
}
.grid-container::-webkit-scrollbar {width:0px;}
@media (max-width: 1660px) {
  .DB_item_3 {
    padding-bottom: 20px;
  }
}

@media (max-width: 1041px) {
  .DB_item_3 {
    padding-top: 20px;
  }
}

@media (max-width: 920px) {
  .box_Dash_A, .box_Dash_E {
    height: 50%;
  }
  .DB_item_1_1, .DB_item_1_2, .DB_item_5_1, .DB_item_5_2 {
    width: 100%;
    padding: 0 20px 0 0px;
  }
}

@media (max-height: 890px) {
  .grid-container {
    overflow-y: auto;
  }
}

.DB_item_1, .DB_item_2,.DB_item_3 {
  min-width: 300px;
  width: 10%;
}
</style>