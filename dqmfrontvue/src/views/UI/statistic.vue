<template>
<div class="flex-col statistic flex-grow-1">
    <filters-bar
            @sendData="giveDataTable"
            @clear="clearit"
           
            :header="'Статистика посещений'"
        >

            <template
                v-slot:filterslist            
            >          
           
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
                  :max="datefrom1" 
                  :min="dateto1"
                  
                  event-color="green lighten-1"
                  v-model="item.$value"
                
                >
                </v-date-picker>
              </v-menu>
            </v-col>        
            
                <v-col
                    class="pa-0"
                    :lg="'3'"
                    md="6"
                    sm="12"
                >
                    <f-multi-select 
                        :field="'user__region__name'"
                        :title="'Регион'"
                                                
                    ></f-multi-select>  
                </v-col>
                <v-col>

                  
                </v-col>

                 
              
            </template>
        </filters-bar>
        <v-divider class="mt-3 fon"></v-divider>
        <v-row class="mt-0 flex-grow-0 ">
          <v-col class="py-0 ">
            <v-select
          v-model="type"
          :items="types"
          label="Тип подсчета"
          @change="changecalculate"
        ></v-select>
          </v-col>

        </v-row>
         <!-- <v-divider class="grey lighten-1"></v-divider> -->
        <v-row class="mt-0 flex-grow-0">
          <v-col class="text-center pa-0 fon">
            <span class="text-h6 text-white"> ФБ1</span>
          </v-col>
        </v-row>
          <!-- <v-divider class="grey lighten-1"></v-divider> -->
        <v-row class="mt-0 ">
          <v-col class="maxh_statistic py-0">
               <linear
              class="pt-3 pl-5"
              :chartData='linear1'
              :chartOptions='chartLineOptions'
           
              />
              
          </v-col>
        </v-row>
          <!-- <v-divider class="grey lighten-1 mt-3"></v-divider> -->
        <v-row class="mt-0 flex-grow-0">
           <v-col class="text-center pa-0 fon">
             <span class="text-h6 text-white"> ЕНС</span>
          </v-col>
        </v-row>
          <!-- <v-divider class="grey lighten-1"></v-divider> -->
        <v-row class="mt-0  ">
          <v-col class="maxh_statistic py-0">
            
                 <linear v-if="ensshow"
              class="pt-3 pl-5"
              :chartData='linear2'
              :chartOptions='chartLineOptions'
       
              /> 
          </v-col>
        </v-row>
          <!-- 
       <span> ФБ1</span>
  
       <span v-if="ensshow">ЕНС</span>
     <linear v-if="ensshow"
              class="pt-3 pl-5"
              :chartData='linear2'
              :chartOptions='chartLineOptions'
             :height="300"
              /> -->
    
            </div>
</template>

<script>
import moment from 'moment';
import { createNamespacedHelpers } from "vuex";
const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");
import Linear from '@/components/statistic/dashboard/linear.vue'
import  datepickerf  from "@/utils/datepickerf.js"

export default { 
    mixins:[datepickerf],

   components: {       
      Linear,     
         
    },
    data(){
      return {
         date_unloading: [{},{}],
        ensshow:false,
        col:{},
        datefrom1: new Date(),
        dateto1: new Date(),
         linear1: {
        labels: [],
        datasets: [
          {
            label: '',
            backgroundColor: '#f87979',
            data: []
          }
        ]
      }, linear2: {
        labels: [],
        datasets: [
          {
            label: '',
            backgroundColor: '#f87979',
            data: []
          }
        ]
      },

         chartLineOptions: {           
           scales: {      
                xAxis: {      
                display:true,
                grid:{
                    lineWidth:0, 
                    drawBorder: false}, 
                },
                
                yAxis:{
                        ticks: {
       
                    callback: function(val, index) {         
                    return Number.isInteger(val)? val : ''
                    }
                }   

                    // display:false
                }      
             },
              elements:{point:{radius: 2}},
         
                responsive: true,
              
                plugins:{ 
                     datalabels: {
                                display:false,                               
                                },                         
                                
                    legend: {display:false},
                    tooltip: {
                    enabled: true,
                    backgroundColor: '#43425D'
                },         
                },
                },
     
        types: ['Уникальные', 'Обращения к разделу', 'Суммы'],
        type: 'Уникальные',
         startdatetable: "",
            enddatetable: "",
            datatable: [],
         
      }
    },
    mounted() {    
      
        this.setFields({
            date: { module: "chain" },
            user__region__name: { module: "mult" },         
      
        });


        // this.setIncludeFilters(["date_unloading"]);

        this.getFilters({
            watcher: [{ name: "date", sort: "-" }],
            watcher_regions: [{ name: "user__region__name", sort: "", related_name: "name" }],
            
           
        }).then(async (data) => {
            
            
            this.loading = true;
           if(data.date.length>1){
                this.$set(this.date_unloading, 1, {$value:data.date[0], model:this.datefrom})
                this.$set(this.date_unloading, 0, {$value:data.date[data.date.length-1], model: this.dateto})
                // this.date_unloading[1] = data.date_unloading[data.date_unloading.length-1]
                this.datefrom1=data.date[0]
                this.dateto1=data.date[data.date.length-1]
            }

            // const dates = [
            //   this.$changeFormatDate(data["date"][data["date"].length-1]),
            //     this.$changeFormatDate(data["date"][0]),
                
            // ];
            // if (data.user__region__name.length==1){
            await this.addFilter({
                key: "user__region__name",
                value: [this.$insertRegion(data.user__region__name[data.user__region__name.length-1])]
            });
            
            data.user__region__name.forEach(e=> this.col[e[1]===null?"Центральный Аппарат":e[1]]=this.random_rgba())
            // }
           
            // await this.addDate({
            //     period: true,
            //     field: "date",
            //     value: [dates[0], dates[1]],
            // });
            // this.startdatetable = dates[0];
            //   this.enddatetable = dates[1];
                  
                  // await this.changecalculate();
                await this.giveDataTable()


                  // this.resizeTable();
                  // window.addEventListener("resize", this.resizeTable);
                  this.changedate = false;     


            
        });

        
    },
     methods: {
        ...mapMutations(["setFields", "setIncludeFilters"]),
        ...mapActions([
            "cleartypeerror",
            "clear",
            "getFilters",
            "addDate",
            "addFilter",
            "activefilters",
        ]),
         formatDate(value){               
        return  moment(value, 'YYYY-MM-DD').format('DD.MM.YYYY')
    },

        giveDataTable({table= 'datatable', load="loadTable", sort="desc_sort", group="group_by", disable=true, subFilt={}}={}) {
            // Получить данные для таблицы
            
            this.datatable = [];
            this[load] = true;
            
            return new Promise(async (resolve, reject) => {
               await this.addDate({
                period: true,
                field: "date",
                value: [ this.$changeFormatDate(this.date_unloading[0].$value),  this.$changeFormatDate(this.date_unloading[1].$value)],
                });
                let filters = await this.activefilters(
                  
                );
                // filters = this.filtercheck(filters)
                if("user__region__name" in filters && filters.includes(null) || !("user__region__name" in filters)) {
                  this.ensshow=true
                }else{
                  this.ensshow=false
                }
              
                this.$http
                    .post(`/api/watcher/`, {
                        filters: {
                            ...filters,
                            ...this.dynamicfilter,
                            ...subFilt,
                        },
                       
                        group_by: disable? this.disableRegion: !this.disableRegion,
                        sort: {
                      
                            group_by: this[group],
                            desc: this[sort],
                        },
                    })
                    .then((res) => {                     
                         
                        this[load] = false;
                        this.datatable =  res.data;
                        
                        this.changecalculate()

                    });
            });
        },

         async updateData() {
            //? В зависимости менялась ли дата, грузим данные для таблицы ил просто запускаем фильтр для нее
                console.log("ss");
                
                // this.tabsdisabled()
                // await this.giveDataTable();
                // this.changedate = false;
      
            
        },

          clearit(){
            
            this.clear()
            this.giveDataTable()
        },
        changecalculate(){  
             
          this.linear1=this.linearcalc("ФБ1")
          this.linear2=this.linearcalc("ЕНС")
         
          
          },
          random_rgba() {
              let o = Math.round
              let  r = Math.random
              let s = 255
              return 'rgb(' + o(r()*s) + ',' + o(r()*s) + ',' + o(r()*s) +')';
          },

          linearcalc(razdel){
                let labels1 = []
                let datasets1 = []
                this.chartLineOptions.plugins.legend.display=false
              if (this.type=="Суммы") {
                this.chartLineOptions.plugins.legend.display=true
                 datasets1 = [ {label:"Сумма уникальных", 
                          backgroundColor: 'rgb(148,87,235)',
                          borderColor: 'rgb(148,87,235)',
                          data:[]},
                          {label:"Сумма обращений", 
                          backgroundColor: 'rgb(204,57,123)',
                          borderColor: 'rgb(204,57,123)',
                          data:[]}
                          ]
                 
                }
              this.datatable.forEach((el)=>
              { 
                if (el.razdel==razdel){               
                let datka = el.date.split("-")  
                datka=datka.reverse().join('.')          
                let ind = labels1.findIndex(e=>e==datka)                
                

                if (this.type=="Суммы") {
                   if (ind>-1){ 
                    datasets1[0].data[ind]+=1
                    datasets1[1].data[ind]+=el.counted
                   }
                   else {
                    labels1.push(datka)
                    datasets1[0].data.push(1)
                    datasets1[1].data.push(el.counted)
                   }
                }
                else {
                    let x = datasets1.findIndex(e=>el.user__region__name===null? e.label=="Центральный Аппарат":e.label==el.user__region__name )
                
                  
                  if (ind>-1){  

                      if(x>-1){
                        datasets1[x].data[ind]+= this.type=="Уникальные"?1:el.counted
                      datasets1.forEach((e,index)=> {if(x!=index)datasets1[x].data.push(0)})
                      }else{
                          let dataarr = []
                          datasets1.forEach(pel=> dataarr.push(0))
                          dataarr[dataarr.length-1]=this.type=="Уникальные"?1:el.counted
                          datasets1.push({label:el.user__region__name===null?"Центральный Аппарат":el.user__region__name, 
                          backgroundColor: this.col[el.user__region__name===null?"Центральный Аппарат":el.user__region__name],
                          borderColor:this.col[el.user__region__name===null?"Центральный Аппарат":el.user__region__name],
                          data:dataarr})

                      }
                  }else{
                    
                      labels1.push(datka)
                      if(x>-1){
                        datasets1[x].data.push(this.type=="Уникальные"?1:el.counted)
                        datasets1.forEach((e,index)=> {if(x!=index)datasets1[x].data.push(0)})
                      }else{
                          datasets1.forEach(elm=> elm.data.push(0))

                          datasets1.push({label:el.user__region__name===null?"Центральный Аппарат":el.user__region__name,
                            backgroundColor: this.col[el.user__region__name===null?"Центральный Аппарат":el.user__region__name],
                          borderColor:this.col[el.user__region__name===null?"Центральный Аппарат":el.user__region__name],
                            data:[this.type=="Уникальные"?1:el.counted]})
                      }

                    
                  }
                  }
                 
                }

                
              

              })  
              console.log(`datasets1`, datasets1);
              return {   labels:labels1,  datasets:datasets1
                }        






          

        
     }},
     computed:{
        tab(){
            
            return this.$store.getters.picindx
        }
    },
      watch:{
        tab(newval,old){
           if (newval==1){
            this.giveDataTable()
           }
        }
    },
    beforeDestroy() {
        this.clear()
        // window.removeEventListener("resize", this.resizeTable);
    }
}
</script>

<style>

 .v-window {
    display: flex;
    flex-grow: 1;
  }


.v-window-item--active {
        flex-grow: 1!important;
    /* flex-direction: column; */
    display: flex;
  }

 .v-window__container {
    flex-grow: 1!important;
    /* flex-direction: column; */
  }
  .maxh_statistic {
    max-height: 30vh;
  }

  .fon {
    background-color: #43425d82;
  }

.text-white {
    color: rgb(255, 255, 255);
}
</style>