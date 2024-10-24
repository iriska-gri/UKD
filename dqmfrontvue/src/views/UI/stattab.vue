<template>
    
<div class="flex-col stattab h-0 flex-grow-1">
    
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
          <!-- <v-select
          v-model="type"
          :items="types"
          label="Тип подсчета"
          @change="changecalculate"
        ></v-select> -->
     <!-- Таблица 1-->
    <v-row>
        <v-col class="flex-col colortab mt-5   mr-2">


        <v-row class="flex-grow-1 flex-col">
            <v-col class="  py-0">

                      <v-data-table
                :headers="headers"
                :items="totaldata"
                disable-pagination
                class="elevation-1  growtable"
                hide-default-footer
                :fixed-header="true"
            >
            <template
                    v-for="h in headers" 
                    v-slot:[`header.${h.value}`]="{ headers }" 
                    
                >
                    {{ h.text }}              
                    <br :key="h.value">
                    {{h.value!="region"? totaller(totaldata, h.value):''}}  
                   
                </template>
            
            
            
            </v-data-table>
       



            </v-col>
        </v-row>
     
         </v-col>
    </v-row>
     <v-row>
        <v-col class="flex-col colortab mt-5   mr-2">


        <v-row class="flex-grow-1  flex-col ">
            <v-col class=" py-0">

       


  <v-data-table
    :headers="group_headers"
    :items="grouppeddata"
    hide-default-footer
    sort-by="region"
    group-by="date"
    class="elevation-1 growtable"
    show-group-by
    :fixed-header="true"
    disable-pagination
  >
                 <template
                    v-for="h in group_headers" 
                    v-slot:[`header.${h.value}`]="{ group_headers }" 
                    
                >
                    {{ h.text }}              
                    <br :key="h.value+1">
                    {{h.value!="region"? totaller(grouppeddata, h.value):''}}  
                   
                </template>
                    <template v-slot:[`group.header`]="{items, isOpen, toggle}">
                            <th>
                            <v-icon @click="toggle"
                                >{{ isOpen ? 'mdi-minus' : 'mdi-plus' }}
                            </v-icon>
                            {{ items[0].date }}
                            </th>
                            <th>{{totaller(items,"fb1uniq")}}   </th>
                            <th>{{ totaller(items,"fb1") }}   </th>
                            <th>{{ totaller(items,"ensuniq") }}   </th>
                            <th>{{ totaller(items,"ens") }}   </th>

                        </template>
  
  
  
  
  </v-data-table>
            </v-col>
        </v-row>
     
         </v-col>
    </v-row>
      
</div>

           
</template>

<script>
import moment from 'moment';
import { createNamespacedHelpers } from "vuex";
const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");
export default {
    data(){
        return{
         date_unloading: [{},{}],
        totaldata:[],
        datatable:[],
        grouppeddata:[],
        group_headers:[
            { text: 'Регион', value: 'region',groupable: false, },
            { text: 'Дата', value: 'date' },
            { text: 'ФБ1 уникальных', value: 'fb1uniq',groupable: false, },
            { text: 'ФБ1 обращений', value: 'fb1',groupable: false, },
            { text: 'ЕНС уникальных', value: 'ensuniq',groupable: false, },
            { text: 'ЕНС обращений', value: 'ens',groupable: false, },
        ],
     headers:[
          { text: 'Регион', value: 'region' },
          { text: 'ФБ1 уникальных', value: 'fb1uniq' },
           { text: 'ФБ1 обращений', value: 'fb1' },
          { text: 'ЕНС уникальных', value: 'ensuniq' },
          { text: 'ЕНС обращений', value: 'ens' },
     ],
   
   }
    },
    computed:{
        tab(){
            
            return this.$store.getters.picindx
        }
    },
    watch:{
        tab(newval,old){
           if (newval==2){
            this.giveDataTable()
           }
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
            // const dates = [
            //   this.$changeFormatDate(data["date"][data["date"].length-1]),
            //     this.$changeFormatDate(data["date"][0]),
                
            // ];
            if(data.date.length>1){
                this.$set(this.date_unloading, 1, {$value:data.date[0], model:this.datefrom})
                this.$set(this.date_unloading, 0, {$value:data.date[data.date.length-1], model: this.dateto})
                // this.date_unloading[1] = data.date_unloading[data.date_unloading.length-1]
                this.datefrom1=data.date[0]
                this.dateto1=data.date[data.date.length-1]
            }

            
           
       
                await this.giveDataTable()

               


            
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
                        
                        this.totalcalculate()
                        this.eachcalc()
                    });
            });
        },
    totaller(arr,key){
        let res=0
        arr.forEach(e=>res+=e[key])
        return res
    },
    totalcalculate(){
        this.totaldata=[]
       
            this.datatable.forEach(el=>{
            let indexregion = this.totaldata.findIndex(e=>el.user__region__name===null? e.region=="Центральный Аппарат":e.region==el.user__region__name )
            if (indexregion>-1){
                if (el.razdel=="ФБ1"){
                    this.totaldata[indexregion].fb1+=el.counted
                    this.totaldata[indexregion].fb1uniq+=1

                 }else{
                    this.totaldata[indexregion].ens+=el.counted
                    this.totaldata[indexregion].ensuniq+=1
                 }
            }else{
                let ob = {region:el.user__region__name===null? "Центральный Аппарат":el.user__region__name, fb1uniq:0,fb1:0,ensuniq:0,ens:0}
                if (el.razdel=="ФБ1"){
                    ob.fb1+=el.counted
                    ob.fb1uniq=1
                }else{
                    ob.ens+=el.counted
                    ob.ensuniq=1
                }
                this.totaldata.push(ob)
            }

            }
        
        
        )
    },
    formatDate(value){               
        return  moment(value, 'YYYY-MM-DD').format('DD.MM.YYYY')
    },
    eachcalc(){
        this.grouppeddata=[]
         this.datatable.forEach(el=>{
            let chdate = this.formatDate(el.date)
            let indexregion = this.grouppeddata.findIndex(e=>(el.user__region__name===null? e.region=="Центральный Аппарат":e.region==el.user__region__name) && (e.date==chdate) )
             if (indexregion>-1){
                if (el.razdel=="ФБ1"){
                        this.grouppeddata[indexregion].fb1+=el.counted
                        this.grouppeddata[indexregion].fb1uniq+=1

                    }else{
                        this.grouppeddata[indexregion].ens+=el.counted
                        this.grouppeddata[indexregion].ensuniq+=1
                    }
             }else{
                let ob= {region:el.user__region__name===null? "Центральный Аппарат":el.user__region__name, fb1uniq:0,fb1:0,ensuniq:0,ens:0,date:chdate}
                if (el.razdel=="ФБ1"){
                       ob.fb1+=el.counted
                        ob.fb1uniq=1 
                    }else{
                         ob.ens+=el.counted
                         ob.ensuniq=1
                    }
                this.grouppeddata.push(ob)
             }
         }
         )
    },
     clearit(){
           
            this.clear()
            this.giveDataTable()
        },


      changecalculate(){  
        this.totalcalculate()
          
          },


    },
  

}
</script>

<style>
.h-0 {
    height: 0
}

.growtable {
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    height: 38vh;
}
</style>