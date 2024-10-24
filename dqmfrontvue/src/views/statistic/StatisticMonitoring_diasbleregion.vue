<template>
    <shell-with-loading :loading="loading" style="height: 100vh;">
        <filters-bar @sendData="updateData" @clear="clear" :helper="ifns?'Для поиска пустых НО/РО введите не число':''">
            <template v-slot:filterslist>
            <div class="flex-item flex-row FIL_item"> 
                <div class=" pa-0  col-4 mr-3 ">            
                    <f-chain-select
                        class="flex-item  FIL_item_1_IFNS"
                        field="date_unloading"
                        :period="false"
                        withtitle="Дата выгрузки"
                        bytitle="Дата выгрузки для сравнения"
                        :watcher="watcher"
                    ></f-chain-select>               
                </div>   
                        <f-multi-select v-if="!ifns"
                            class="flex-item mr-3 FIL_item_2_IFNS col-4  pa-0"
                            
                            :field="'passport__code'"
                            :title="disableRegion ?'Код паспорта':'Код паспорта (недоступно)'"
                           

                        ></f-multi-select> 
                         <!-- :disabled="!disableRegion" -->
                        <f-multi-select v-else
                            class="flex-item mr-3 FIL_item_2_IFNS col-4  pa-0"
                            
                            :field="'passport__code'"
                            :title="'Код паспорта'"                           

                        ></f-multi-select> 




                    <f-multi-select v-if="!ifns"
                        class="flex-item FIL_item_3_IFNS  pa-0" 
                        :field="'region__name'"
                        :title="!disableRegion?'Регион':'Регион (недоступно)'"
                        
                    ></f-multi-select>  
                    <!-- :disabled="disableRegion" -->
                    <f-multi-select v-else-if="methodolog() & ifns"                     
                                    class="flex-item FIL_item_3_IFNS  pa-0"
                                        :field="'region__name'"
                                        :title="'Регион'"
                                        
                                    ></f-multi-select>  
                
                    <!-- <div class=" pt-3  pl-3" v-if="ifns">                                -->
                                    <f-select  v-if="ifns"
                                    :title="'Тип НД'"
                                    :field="'type_error'"
                                    :class="methodolog()?'col-4':''"
                                    class="flex-item   pa-0 mr-3"
                                    :cleaner="true"
                                    >
                                        
                                    </f-select>

                                     
                         <!-- :disabled="disableRegion" -->
                                    <!-- :type="'number'" -->
                                    <div class="flex-row filtrDuo col-4 pa-0 FIL_item_1"  v-if="ifns">
                                        <f-input-search
                                            
                                            class="flex-item  mr-3  pa-0 "
                                            :field="'nocode'"
                                            
                                            :title="'Код НО'"
                                            
                                        ></f-input-search>
                                   <!-- :disabled="disableRegion" -->
                                   
                                        <f-input-search
                                            class="flex-item  pa-0 pl-2"
                                            :field="'rocode'"
                                            
                                            :title="'Код РО'"
                                            
                                        ></f-input-search>
                                    <!-- :disabled="disableRegion" -->
                                    
                                    </div>   
                                    <!-- <div class="flex-item mr-3 FIL_item_1"> -->
           
                <!-- </div>   -->

                                        
                    <!-- </div> -->
                
            </div>

            </template>

        </filters-bar>
        <div class="px-5 scroll-block pb-3 ">
            <div class="d-flex" style="width: 100%;">
                <!-- Виды ненормализованных данных -->
                <v-tabs v-model="tab" @change="changeTab"
                slider-size="0"
                height='30'>
                
                    <v-tab
                        v-for="(tab, index) in tabs"
                        
                        :key="index"
                        :disabled='tab.disabled'
                        class="tab-table"
                        active-class= "activetab"
                        
                    >
                        {{ tab.text }}
                    </v-tab>
                </v-tabs>
                <v-icon color="#1F6E43" class="excel px-3" @click="createExcel($event.target)"
                    >mdi-microsoft-excel</v-icon
                >
            </div>
            <!-- Таблица -->
            <v-data-table
                dense
                :headers="headers"
                :items="filterTable"
                hide-default-footer
                :must-sort="true"
                :sort-by.sync="group_by"
                :sort-desc.sync="desc_sort"
                :disable-pagination="true"
                :fixed-header="true"
                :loading="loadTable"
                :custom-sort="$customSortDataTable"
                loading-text="Загрузка... Пожалуйста, подождите"
                @dblclick:row="clickRow"
                class="pointertable grow-table pl-1"
            >
                <template
                    v-for="h in headers" 
                    v-slot:[`header.${h.value}`]="{ headers }" 
                    
                >
                    {{ h.text }}{{ h.value == "countData" ? startdatetable =="Первоначальная"?"Первоначальную дату":startdatetable : "" }}{{ h.value == "countCompare" ? enddatetable =="Первоначальная"?"Первоначальную дату": enddatetable : "" }}{{ h.middletext? h.middletext :""}}                   
                    <br :key="h.value">
                    {{ h.value == "countData" ? headercountData:'' }}  
                    {{ h.value == "countCompare" ? headerCompare:''}}
                    {{ h.value == "growth" ? growth:''}}
                    {{ h.value == "percentage" ? String(headerperc.toFixed(2)).split(".")[1]=="00"?headerperc:headerperc.toFixed(2):''}}
                    
                   
                    {{ h.aftertext?h.aftertext:""}}
                </template>
                <template v-slot:[`item.percentage`]="{ item }">
                
                        <span>{{item.percentage}}</span>

                    <v-icon
                        v-if="+item.percentage > 0"
                        class="icon-arrow-mon plus"
                        >mdi-arrow-up-bold</v-icon
                    >
                    <v-icon v-if="+item.percentage < 0" class="icon-arrow-mon"
                        >mdi-arrow-down-bold</v-icon
                    >
                
                    
                </template>
            </v-data-table>
        </div>
        <v-dialog
        transition="dialog-top-transition"
        style="overflow-y: hidden;"
        max-width="80%"
        
        v-model="dialogInverseTable"
      >
        <template v-slot:default="dialog">
            <v-card>
                <v-card-title class="primary--text">
                    <span>{{ headSubModal }}</span>
                    <v-spacer></v-spacer>
                 <v-icon color="#1F6E43" class="excel px-3" @click="createsubExcel($event.target)"
                    >mdi-microsoft-excel</v-icon
                >
                    <v-btn icon @click="dialog.value = false"><v-icon  class="primary--text">mdi-close</v-icon> </v-btn>
                </v-card-title>
                <v-card-text class="pa-3" style="background: rgb(238, 235, 239);" width="100vw">
            
                    <v-data-table
                        :headers="headersSub"
                        :items="dataSubtable"
                        hide-default-footer
                        :must-sort="true"
                        :sort-by.sync="group_bySub"
                        :sort-desc.sync="desc_sortSub"
                        :disable-pagination="true"
                        :fixed-header="true"
                        :loading="loadSubTable"
                        :custom-sort="$customSortDataTable"
                        
                        
                        loading-text="Загрузка... Пожалуйста, подождите"
                        style="max-height: 75vh;width: 100%; overflow-y: hidden; display: flex;" 
                         
                        
                    >

                    <!--:custom-sort="$customSortDataTable" -->
                        <template
                            v-for="h in headersSub" 
                            v-slot:[`header.${h.value}`]="{ headersSub }"

                        >
                    {{ h.text }}{{ h.value == "countData" ? startdatetable =="Первоначальная"?"Первоначальную дату":startdatetable : "" }}{{ h.value == "countCompare" ? enddatetable =="Первоначальная"?"Первоначальную дату": enddatetable : "" }}{{ h.middletext? h.middletext :""}}                   
                     <br :key="h.value">
                    {{ h.value == "countData" ? headercountDataSub:'' }}  
                    {{ h.value == "countCompare" ? headerCompareSub:''}}
                    {{ h.value == "percentage" ? String(headerpercSub.toFixed(2)).split(".")[1]=="00"?headerpercSub:headerpercSub.toFixed(2):''}}
                    {{ h.value == "growth" ? growthSub:''}}
                    {{ h.aftertext?h.aftertext:""}}
                        </template>
                        <template v-slot:[`item.percentage`]="{ item }">
                        
                                <span>{{item.percentage}}</span>

                            <v-icon
                                v-if="+item.percentage > 0"
                                class="icon-arrow-mon plus"
                                >mdi-arrow-up-bold</v-icon
                            >
                            <v-icon v-if="+item.percentage < 0" class="icon-arrow-mon"
                                >mdi-arrow-down-bold</v-icon
                            >
                        
                            
                        </template>
                    </v-data-table>
           
                </v-card-text>
            </v-card>
    
            <!-- <v-toolbar
              color="primary"
              :max-height="'75vh'"
              style="overflow-y:hidden;"
              dark
                >
                <v-toolbar-title class="mr-auto">{{ headSubModal }}</v-toolbar-title>
                    <v-btn
                icon
                dark
                @click="dialog.value = false"
            ><v-icon>mdi-close</v-icon> </v-btn>
            </v-toolbar> -->
            
        </template>
      </v-dialog>
      <v-snackbar
                v-model="error"
                >                
                {{errortext}}
                <template v-slot:action="{ attrs }">
                    <v-btn
                    color="pink"
                    text
                    v-bind="attrs"
                    @click="error = false"
                    >
                    Закрыть
                    </v-btn>
                </template>
                </v-snackbar>
    </shell-with-loading>

    
</template>

<script>
import { createNamespacedHelpers } from "vuex";
import FSelect from '../../components/UI/FSelect.vue';
const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");


function createHeader(typeR, ifns) {
    let headers = [];

    if (typeR) {
        headers.push(
            { text: "Код паспорта", 
            value: "passport__code",
            width: "9%" },
            { text: "Паспорт", value: "passport__name" }
        );
    } else if (ifns) {
        headers.push(
            
             { text: "Код региона", value: "region__tax_code" },
            { text: "Регион", value: "region__name" },
            {text:"Код НО",value:'nocode'},
            {text:'Код РО',value:'rocode'},
            
        );
    }
    else if (!(ifns)){
        headers.push( 
            { text: "Код региона", value: "region__tax_code" },
            { text: "Регион", value: "region__name" },)
    }
    

    headers.push(
        {
            text: "Кол-во НД на ",
            value: "countData",
            middletext: ": ",
            aftertext: "шт."
        },
        {
            text: "Кол-во НД на ",
            value: "countCompare",
            middletext: ": ",
            aftertext: "шт."
        },
        { text: "Прирост", 
            value: "growth",
            middletext: ": ",
            aftertext: "шт."
        },
        { text: "Прирост (%)", 
        middletext: ": ",
        value: "percentage" }
    );

    return headers;
}

export default {
  components: { FSelect },
    name: "MonitoringIFNS",
    props:{
        ifns:{type:Boolean,
        default: false}
    },
    data() {
        
        return {
            error:false,
            // ifns: window.location.pathname=='/statistic/monitoringifns'?true:false,
            errortext:'',
            loading: false,
            changedate: false,
            dialogInverseTable: false,
            // disableduser: this.$store.getters.region==null ?false : true,
            //* Таблица
            loadTable: false,
            datatable: [],
            group_by: "region__tax_code", // Сортировка
            desc_sort: true,
            loadSubTable: false,
            dataSubtable: [],
            group_bySub: "passport__name",
            desc_sortSub: true,
            headSubModal: "",
            headerperc:0,
            headerpercSub:0,
            headerCompare: 0,
            headercountData:0,
            headerCompareSub: 0,
            headercountDataSub:0,
            growth:0,
            growthSub:0,

            // Служебные, для определения типа фильтрации (По регионам или по паспортам)
            disableRegion: false,
            subfilter:{},
            interpritateDisableRegion: {
                true: ["passport__code", "passport__code"],
                false:  ["region__name", "region__tax_code"],
            },
            filts: [],
            includeField: "",
            startdatetable: "",
            enddatetable: "",
            // heightTable: 0,

            //* Тип данных (динамические фильтры)
            tab: 0,
            tabs: []
                // {
                //     text:  window.location.pathname=='/statistic/monitoringifns'?"Динамика в разрезе НО":"Динамика в разрезе регионов",
                //     sort: {},
                //     disableRegion: false,
                // },
                // {
                //     text: "Динамика в разрезе паспортов",
                //     sort: {},
                //     disableRegion: true,
                // },
                // {
                //     text: "Мониторинг старых НД",
                //     sort: { type_error: 1 },
                //     disableRegion: false,
                // },
                // {
                //     text: "Мониторинг новых НД",
                //     sort: { type_error: 2 },
                //     disableRegion: false,
                // },
                // {
                //     text: "Мониторинг ВПНД",
                //     sort: { type_error: 3 },
                //     disableRegion: false,
                // },
        // ]
            ,
            dynamicfilter: {},
        };
    },
    watch:{
        ifns: function (val) {
            this.tabs[0].text= val?"Динамика в разрезе НО":"Динамика в разрезе регионов"
            this.tab= 0
            this.group_by= this.ifns?'nocode':"region__tax_code",
            this.interpritateDisableRegion['false']= this.ifns? ['nocode','nocode']:["region__name", "region__tax_code"],
            this.disableRegion= false
            this.tabs= this.tabser(val)


            this.clear()
            this.giveDataTable();
        }
    },
    methods: {
        ...mapMutations(["setFields", "setIncludeFilters"]),
        ...mapActions([
            "clear",
            "getFilters",
            "addDate",
            "addFilter",
            "activefilters",
        ]),
        tabser(val){
            let t =  [{
                    text:  window.location.pathname=='/statistic/monitoringifns'?"Динамика в разрезе НО":"Динамика в разрезе регионов",
                    sort: {},
                    disableRegion: false,
                    disabled:false
                },
                {
                    text: "Динамика в разрезе паспортов",
                    sort: {},
                    disableRegion: true,
                    disabled:false
                }]
            if (val)  {
                return t }
            else{
                return       [...t,... [{
                    text: "Мониторинг старых НД",
                    sort: { type_error: 1 },
                    disableRegion: false,
                    disabled:true
                },
                {
                    text: "Мониторинг новых НД",
                    sort: { type_error: 2 },
                    disableRegion: false,
                    disabled:true
                },
                {
                    text: "Мониторинг ВПНД",
                    sort: { type_error: 3 },
                    disableRegion: false,
                    disabled:true
                }]]
            }
        },
        tabsdisabled(){

            const dates =
                    this.$store.getters["filterslogic/chain/dateuploading"];
                this.startdatetable = dates[0];
                this.enddatetable = dates[1];
                 if (this.changedate && this.tabs.length>2) {
                    for (let i=2;i<this.tabs.length; i++){
                  
                        this.tabs[i].disabled=  dates.includes('Первоначальная')?true:false                        
                    } 
                 if(dates.includes('Первоначальная')) {
                    this.tab=0
                    this.changeTab(0)             }
                }
                

           
        },


        async updateData() {
            //? В зависимости менялась ли дата, грузим данные для таблицы ил просто запускаем фильтр для нее
           
                
                this.tabsdisabled()
                await this.giveDataTable();
                this.changedate = false;
            // } else {
                
            //     this.includeField =
            //     this.interpritateDisableRegion[this.disableRegion][0];
          
                
            //     const givenFilt = this.ifns?this.$store.getters[`filterslogic/input/${this.includeField}`]:this.$store.getters[`filterslogic/mult/${this.includeField}`];
            //     this.filts =
            //     this.includeField == 'region__name'? givenFilt.map((el) => el.replace(/\d\d\.\s/, '')):givenFilt;
        
            // }

            
        },
        async changeTab(index) {
            // Изменение динамических фильтров
           
            if (this.disableRegion != this.tabs[index].disableRegion) {
                this.disableRegion = this.tabs[index].disableRegion;
                this.group_by =
                    this.interpritateDisableRegion[this.disableRegion][1];
                this.group_bySub =
                    this.interpritateDisableRegion[!this.disableRegion][1];
                this.clear();
                this.filts = [];
            }
            
            
            this.dynamicfilter = this.tabs[index].sort;
            this.giveDataTable();
        },
        desc_sortf(){
            this.desc_sort=!this.desc_sort
            return this.desc_sort
        },
        // filtercheck(filters){
        //         if ('type_error__in' in filters){
        //          for (let index = 0; index < filters.type_error__in.length; index++) {
        //             filters.type_error__in[index]=['',"Старая","Новая","ВПНД"].indexOf(filters.type_error__in[index])
        //                           }                   
        //         }
        //         return filters},
        giveDataTable({table= 'datatable', load="loadTable", sort="desc_sort", group="group_by", disable=true, subFilt={}}={}) {
            // Получить данные для таблицы
            
            this[table] = [];
            this[load] = true;
            return new Promise(async (resolve, reject) => {
                let filters = await this.activefilters(
                  
                );
                // filters = this.filtercheck(filters)               
                this.$http
                    .post(`/api/statistic/fb1/reporting/monitoring/`, {
                        filters: {
                            ...filters,
                            ...this.dynamicfilter,
                            ...subFilt,
                        },
                        ifns:this.ifns,
                        group_by: disable? this.disableRegion: !this.disableRegion,
                        sort: {
                            group_by: this[group],
                            desc: this[sort],
                        },
                    })
                    .then((res) => {
                        // this.datatable[this.idlist.index].justify__fix_status = this.rebuildfix(solution)
                        
                        this[load] = false;
                        this[table] = res.data;
                        if (load== 'loadSubTable'){                            
                            this.headerCompareSub = 0
                            this.headercountDataSub=0 
                            this.growthSub=0
                            res.data.map((e)=>{
                            this.headerCompareSub += e.countCompare
                            this.headercountDataSub += e.countData
                            this.growthSub+=e.growth
            })
                        this.headerpercSub = this.headercountDataSub==0? 100:((this.headerCompareSub*100/this.headercountDataSub).toFixed(2) -100)
                        }
                        resolve(res.data);
                    });
            });
        },
        methodolog(){
            return JSON.parse(localStorage.getItem('profile'))['region']==null
        },
        async createExcel(el) {
            this.$store.commit("loadFrameTrue");
            let filters = await this.activefilters(
            //     [
            //     "region__name",
            //     "passport__code",
            // ]
            );
            // filters = this.filtercheck(filters) 




            this.$http
                .post(`/api/statistic/fb1/reporting/monitoring/`, {
                    filters: {
                        ...filters,
                        ...this.dynamicfilter,
                        
                    },
                    group_by: this.disableRegion,
                    sort: {
                        group_by: this.group_by,
                        desc: this.desc_sort,
                    },
                    ifns:this.ifns,
                    excel: true,
                    fn_modificator: this.tabs[this.tab].text,
                    
                    headers_table: this.headers.map((el) => {
                        const o = { ...el };                        
                        if (o.value == "countData")
                            o.text = `${o.text}${this.startdatetable=="Первоначальная"?"Первоначальную дату":this.startdatetable}`;
                        if (o.value == "countCompare")
                            o.text = `${o.text}${this.enddatetable=="Первоначальная"?"Первоначальную дату":this.enddatetable}`;
                        return o;
                    }),
                })
                .then((res) => {
                    el.blur()
                    this.$store.commit("loadFrameFalse");
                    if ('name' in res.data){
                    window.location.href =
                        this.$http.defaults.baseURL +  res.data.name;
                    }else{
                        this.errortext = res.data.error
                        this.error=true
                    }
                    
                })
                .catch(() => {
                    this.$store.commit("loadFrameFalse");
                });

                
        },
        async createsubExcel(el) {
            this.$store.commit("loadFrameTrue");
            const filters = await this.activefilters(
            //     [
            //     "region__name",
            //     "passport__code",
            // ]
            );
            // filters = this.filtercheck(filters) 

            let disable=false
            this.$http
                .post(`/api/statistic/fb1/reporting/monitoring/`, {

                    filters: {
                        ...filters,
                        ...this.dynamicfilter,
                        ...this.subfilter,
                    },
                    group_by: disable? this.disableRegion: !this.disableRegion,
                    sort: {
                        
                        group_by: this.group_bySub,
                        desc: this.desc_sortSub,
                    },
                    ifns:this.ifns,
                    excel: true,
                    fn_modificator: this.tabs[this.tab].text,
                    
                    headers_table: this.headersSub.map((el) => {
                        const o = { ...el };                        
                        if (o.value == "countData")
                            o.text = `${o.text}${this.startdatetable=="Первоначальная"?"Первоначальную дату":this.startdatetable}`;
                        if (o.value == "countCompare")
                            o.text = `${o.text}${this.enddatetable=="Первоначальная"?"Первоначальную дату":this.enddatetable}`;
                        return o;
                    }),
                })
                .then((res) => {
                    el.blur()
                    this.$store.commit("loadFrameFalse");
                    if ('name' in res.data){
                    window.location.href =
                        this.$http.defaults.baseURL +  res.data.name;
                    }else{
                        this.errortext = res.data.error
                        this.error=true
                    }
                    
                })
                .catch(() => {
                    this.$store.commit("loadFrameFalse");
                });

        },

        watcher() {
            this.changedate = true;
        },
        // resizeTable() {
        //     const scrollBlock = this.$refs.scrollBlock;
        //     this.heightTable = scrollBlock.offsetHeight - scrollBlock.firstElementChild.offsetHeight-20;
        // },
        async clickRow(e, row) {

            this.headSubModal = this.disableRegion? `${row.item['passport__code']}. ${row.item['passport__name']}` : this.ifns?`${row.item['nocode']}`:`${row.item['region__tax_code']}. ${row.item['region__name']}`;
            let subFilt = this.disableRegion? {'passport__code': row.item['passport__code']}:this.ifns?{'nocode':row.item['nocode'],'rocode':row.item['rocode'], 'region__tax_code': row.item['region__tax_code']}: {'region__tax_code': row.item['region__tax_code']};
            this.subfilter = subFilt
            this.dialogInverseTable = true;
       
            this.giveDataTable({
                table: 'dataSubtable',
                load: 'loadSubTable',
                sort: 'desc_sortSub',
                group: 'group_bySub',
                disable: false,
                subFilt
            })
        },
        
    },
 
    computed: {
        headers() {
            // Установка хэдера таблицы в зависимости от группировки по регионам или паспортам
            return createHeader(this.disableRegion, this.ifns);
            
        },

        headersSub() {
            return createHeader(!this.disableRegion,this.ifns);
        }, 

        filterTable() {
            //? Фильтрация для таблицы и подсчет в шапку
            this.headerCompare = 0
            this.headercountData=0
            this.growth=0
            this.headerperc =0
            let a =  [...this.datatable]
        
            // if (this.filts && this.filts.length != 0) {
           
            //     if ( ['nocode', 'rocode'].includes(this.includeField)){
                   
            //          a= a.filter((value) =>
            //           {
         
            //         this.filts.includes(value[this.includeField])})
            //     }
                
            //     }else{
            //             a= a.filter((value) =>
            //         this.filts.includes(value[this.includeField])
            //     );
            //     }
            
            
            a.map((e)=>{
                this.headerCompare += e.countCompare
                this.headercountData += e.countData
                this.growth += e.growth
            })
            this.headerperc =this.headercountData==0?100: (this.headerCompare*100/this.headercountData).toFixed(2) -100
            return a
        },
       
        
    },
    

    mounted() {
        
        this.group_by= this.ifns?'nocode':"region__tax_code",
        this.interpritateDisableRegion['false']= this.ifns? ['nocode','nocode']:["region__name", "region__tax_code"],
        this.tabs=this.tabser(this.ifns)
        this.setFields({
            date_unloading: { module: "chain" },
            region__name: { module: "mult" },
            passport__code: { module: "mult" },
            type_error:{module:"select"}
      
        });

        this.setIncludeFilters(["date_unloading"]);

        this.getFilters({
            listFB1: [{ name: "date_unloading", sort: "-" }],
            regions: [{ name: "region__name", sort: "", related_name: "name" }],
            passports: [
                { name: "passport__code", sort: "", related_name: "code" },
            ],
           
        }).then(async (data) => {
            
            
            this.loading = true;
            const dates = [
                this.$changeFormatDate(data["date_unloading"][data["date_unloading"].length-1]),
                this.$changeFormatDate(data["date_unloading"][0]),
            ];
            if (data.region__name.length==1){
            await this.addFilter({
                key: "region__name",
                value: [this.$insertRegion(data.region__name[0])]
            });
            }
            // "1 - Старая , 2 - Новая, 3 - ВПНД"
            
            // await this.addFilter({
            //     key: "type_error",
            //     value: 0
            // })
            await this.addDate({
                period: false,
                field: "date_unloading",
                value: [dates[0], dates[1]],
            });

            this.startdatetable = dates[0];
            this.enddatetable = dates[1];
            
            await this.giveDataTable();




            // this.resizeTable();
            // window.addEventListener("resize", this.resizeTable);
            this.changedate = false;
            
        });
        
    },
   
    beforeDestroy() {
        // window.removeEventListener("resize", this.resizeTable);
    }
    
};
</script>

<style lang="scss">
@import "@/utils/colors.scss";
.FIL_item_1 {
    width: 30%;
    min-width: 240px;
    align-self: flex-end;
    
}

.FIL_item_1_per {
    width: 40%;
    min-width: 420px;
}
.FIL_item_2_per, .FIL_item_3_per {
    width: 20%;
    min-width: 150px;
    align-self: flex-end;
    
}
.v-data-table__wrapper{
    width: 100%;
}

.tab-table {
    font-size: 0.6em;
    color: $gray;
}



.icon-arrow-mon.v-icon {
    font-size: 14px;
    color: #1dc9b7;
}

.icon-arrow-mon.v-icon.plus {
    color: #fd397a;
    margin-bottom: 2px;
}
//  --- Если регион
// .FIL_item_1_IFNS {
//     width: 20%;
//     min-width: 420px;
// }

// .FIL_item_2_IFNS {
//     width: 15%;
//     min-width: 220px;
// }

// .FIL_item_3_IFNS {
//     width: 15%;
//     min-width: 220px;

    
// }

// .FIL_item_4_IFNS {
//     width: 25%;
//     min-width: 150px;
// flex-wrap: nowrap;
    
// }

</style>