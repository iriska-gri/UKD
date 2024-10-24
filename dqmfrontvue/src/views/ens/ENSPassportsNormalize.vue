<template>
    <shell-with-loading :loading="loading" style="height: 100vh;">
        <div v-show="!this.$store.getters.thisshowForm" class="main-align">
            <filters-bar
                @clear="clear"
                @sendData="updateData"
                :header="'ПАСПОРТА НОРМАЛИЗАЦИИ (ЕНС)'"
            >
                <template
                    v-slot:filterslist
                >
                
                    <v-col  
                        class="pa-0"
                        lg="2"
                        md="6"
                        sm="12"
                        
                    >
                        <fc-multi-select
                            title="Код паспорта" 
                            :items="multi.code"
                            v-model="formData.code"
                        >
                        </fc-multi-select>
                    </v-col>
                    <v-col  
                        class="pa-0"
                        md="4"
                        sm="12"
                    >
                        <fc-multi-select
                            title="Код тех. процесса"
                            :items="multi.code_name_process"
                            v-model="formData.code_name_process"
                        >
                        </fc-multi-select>
                    </v-col> 
                    <v-col  
                        class="pa-0"
                        md="3"
                        sm="12"
                    >
                        <fc-multi-select
                            title="Приоритет"
                            :items="multi.priority"
                            v-model="formData.priority">
                        </fc-multi-select>
                    </v-col>
                    <v-col  
                        class="pa-0"
                        md="3"
                        sm="12"
                    >
                        <fc-multi-select
                            title="Наименование паспорта"
                            :items="multi.name"
                            v-model="formData.name"
                        >
                        </fc-multi-select>
                    </v-col>
                    <v-col  
                        class="pa-0"
                        md="2"
                        sm="12"
                    >
                        <fc-multi-select
                            title="Режим"
                            :items="booleanMultiMode"
                            v-model="formData.mode">
                        </fc-multi-select>
                    </v-col>
                    <v-col  
                        class="pa-0"
                        md="2"
                        sm="12"
                    >
                        <fc-multi-select
                            title="Критичность"
                            :items="multi.criticality"
                            v-model="formData.criticality">
                        </fc-multi-select>
                    </v-col>
                    <v-col  
                        class="pa-0"
                        md="2"
                        sm="12"
                    >
                        <fc-multi-select
                            title="Подсистема"
                            :items="multi.sub_system"
                            v-model="formData.sub_system">
                        </fc-multi-select>
                

                    </v-col>
                        <v-col  
                            class="pa-0"
                            md="3"
                            sm="12"
                        >
                                <fc-chain-select 
                                    title="Дата включения паспорта в перечень" 
                                    :items="multi.date_of_including_of_the_initial_list"
                                    :cleaner="true"
                                    v-model="dateRange.date_of_including_of_the_initial_list"
                                >
                                </fc-chain-select>
                        </v-col>           
                <!-- <v-col  
                        class="pl-0 pr-2"
                        cols="2">
                        <fc-multi-select
                        
                            title="Код паспорта" 
                            :items="multi.code"
                            v-model="formData.code"
                        >
                        </fc-multi-select>
                
                </v-col>

                <v-col  
                        class="pl-0 pr-2"
                        cols="4">
                        <fc-multi-select
                        
                            title="Код тех. процесса"
                            :items="multi.code_name_process"
                            v-model="formData.code_name_process"
                        >
                        </fc-multi-select>
                </v-col>
                    <v-col  
                        class="pl-0 pr-2"
                        cols="3">
                        <fc-multi-select
                        class=""
                            title="Приоритет"
                            :items="multi.priority"
                            v-model="formData.priority">
                        </fc-multi-select>
                    </v-col>
                    <v-col  
                        class="pl-0 pr-2"
                        cols="3">
                        <fc-multi-select
                        
                            title="Наименование паспорта"
                            :items="multi.name"
                            v-model="formData.name"
                        >
                        </fc-multi-select>
                    
                    </v-col>
                    <v-col  
                        class="pl-0 pr-2"
                        cols="2">
                        <fc-multi-select
                        class=""
                            title="Режим"
                            :items="booleanMultiMode"
                            v-model="formData.mode">
                        </fc-multi-select>
                    </v-col>
                    <v-col  
                        class="pl-0 pr-2"
                        cols="2">
                        <fc-multi-select
                        
                            title="Критичность"
                            :items="multi.criticality"
                            v-model="formData.criticality">
                        </fc-multi-select>
                    </v-col>
                    <v-col  
                        class="pl-0 pr-2"
                        cols="2">
                        <fc-multi-select
                        class=""
                            title="Подсистема"
                            :items="multi.sub_system"
                            v-model="formData.sub_system">
                        </fc-multi-select>
                

                    </v-col>
                    <v-col  
                        class="pl-0 pr-2"
                        cols="3">
                            <fc-chain-select 
                            title="Дата включения паспорта в перечень" 
                        
                            :items="multi.date_of_including_of_the_initial_list"
                            :cleaner="true"
                            v-model="dateRange.date_of_including_of_the_initial_list"
                            ></fc-chain-select>
                    </v-col>
                         -->
                
                </template>
            </filters-bar>

            <div class="px-3 px-5 scroll-block">
                <v-data-table
                    dense
                    class="pointertable grow-table pl-1"
                    :headers="headers"
                    :items="showDataTable"
                    hide-default-footer
                    :fixed-header="true" 
                    :custom-sort="$customSortDataTable" 
                    sort-by="code"                  
                    :must-sort="true"
                    :sort-desc="true"
                    :disable-pagination="true"
                    @dblclick:row="clickRow"                    
                    
                >


                    <template v-slot:[`item.date_of_including_of_the_initial_list`]="{ item }">
                        {{ $changeFormatDate(item.date_of_including_of_the_initial_list) }}
                    </template>
                    <template v-slot:[`item.date_of_deactivate`]="{ item }">
                        {{ $changeFormatDate(item.date_of_deactivate) }}
                    </template>
                    <template v-slot:[`item.mode`]="{ item }">
                        {{ item.mode? 'Мониторинг': (item.mode == null? '': 'Нормализация') }}
                    </template>
                    <template v-slot:[`item.sub_system`]="{ item }">
                        {{ item.sub_system.join(", ") }}
                    </template>
                    <template v-slot:[`item.code_name_process`]="{ item }">
                        {{ item.code_name_process.length>50? `${item.code_name_process.slice(0, item.code_name_process.indexOf(' ', 50))}...`:item.code_name_process }}
                    </template>
                </v-data-table>
            
            </div>
            
            <div class="d-flex justify-end my-2 mr-3 ">
                <div class="d-flex justify-end align-center mx-5">Всего записей: {{filterdata.length}} </div>
                <div class="d-flex justify-end align-center select-page mr-5 ">
                    
                    <v-select
                    :items = "count_pages"
                    v-model="page_size"
                    @change="updateData"
                    dense
                    solo
                    hide-details="true"
                    
                    >

                    </v-select>
                </div>
                
                    <!-- Пагинация -->
                <v-pagination
                    v-model="page"
                    :length="totalPage"
                    :total-visible="10"
                    @input="changePage"
                ></v-pagination>
            </div>
        </div>
        <div v-if="this.$store.getters.thisshowForm">
            <form-password :updateForm="true" :fillData="rowData" :multiData="multiData" @save="save" @backMain="backMain"></form-password>
        </div>
    </shell-with-loading>
    

</template>

<script>
import { createNamespacedHelpers } from "vuex";
import FormPassword from '@/components/statistic/FormPassword.vue';
import moment from 'moment';
const { mapActions } = createNamespacedHelpers("filterslogic");
import  datepickerf  from "@/utils/datepickerf.js"
import globalFuncs from '@/utils/helper'
    export default {
        name: 'enspassports',
        components: { FormPassword },
        mixins:[datepickerf],
        data() {
            return {
                loading: false,
                // showForm: this.$store.getters.thisshowForm,
                rowData: null,
                dateRange: {
                    date_of_including_of_the_initial_list: {
                        with: '',
                        by: '',
                    }
                },
                multiData: {},
                multi: {
                    name:[],
                    code: [],
                    code_name_process: [],
                    priority: [],
                    mode: [],
                    criticality: [],
                    sub_system: [],
                    date_of_including_of_the_initial_list: [],
                },
                formData: {
                    code: [],
                    name: [],
                    code_name_process: [],
                    priority: [],
                    mode: [],
                    criticality: [],
                    sub_system: [],
                },
                group_by: "date_of_including_of_the_initial_list", 
                desc_sort: false,

                headers: [
                    { text: "Код", value: "code" },
                    { text: "Наименование паспорта", value: "name" },
                    { text: "Включен в перечень", value: "date_of_including_of_the_initial_list"},
                    { text: "Дата признания паспорта неактуальным", value: "date_of_deactivate", width:"11%" },
                    { text: "Режим", value: "mode" },
                    { text: "Приоритет", value: "priority", width:"7%"  },
                    { text: "Критичность", value: "criticality", width:"7%"  },
                    { text: "Подсистема", value: "sub_system" },
                    { text: "Код тех. процесса", value: "code_name_process" },
                ],

                datatable: [],
                filterdata: [],
                namefilters: ['code', 'name','code_name_process', 'mode', ' priority', 'date_of_including_of_the_initial_list','sub_system', 'criticality'],

                // Pagination
                page: 1,
                totalPage: 0,
                count_pages: Array.from({length: 10}, (_, i) => (i + 1) *150),
                page_size: 150,
                openindex: 0,

            }
        },
        methods: {
            ...mapActions([
                "getFiltersWithoutRecord",
            ]),
            // subsystemstr(item){                
            //     return item.map((e)=>{return e.name}).join(", ")
            // },      
            updateData() {
                this.loading=false
                const data = {};
                
                for (let [key, value] of Object.entries(this.formData)) {
                   
                    // data[key] = value;
                    if (typeof value == 'string') {
                        if (value != '') {
                            data[key] = value;
                        }
                    } else {
                        if ( value.length != 0 ) {
                        
                            data[key] = [...value];
                    //         // data[key] = value;

                            // const index = data[key].indexOf('Пустой');
                            // if (index != -1) {
                            //     data[key][index] = '';
                            }
                        }
                    // }
                    
                }
                const readyDateRange = {}
                for (let [key, period] of Object.entries(this.dateRange)) {
                    
                    if (period.with != '' || period.by != '') {

                        let startFunc = null;
                        if (period.with == '') {
                            startFunc = (val) => moment(val).isSameOrBefore(period.by);
                        } else if (period.by == '') {
                            startFunc = (val) => moment(val).isSameOrAfter(period.with);
                                
                        } else {
                            startFunc = (val) => moment(val).isBetween(period.with, period.by,null, '[]');
                        }

                        readyDateRange[key] = startFunc;
                    }
                        
                }
              
                this.filterdata = this.datatable.filter((row) => {                    
                    for (let [key, value] of Object.entries(data)) {
                        
                        
                            let a=['']
                                if (typeof row[key]==="undefined"){a=["Пустой"]}
                                else if (key=="mode")   
                                    if (row[key]==null){a=["Пустой"]}
                                    else{a=row[key]?["Мониторинг"]:["Нормализация"]}
                                else if(key=="sub_system"){
                                    a=row[key]==''?["Пустой"]:[...row[key]]
                                }
                                else{
                                    a=row[key]==''?["Пустой"]:[row[key]]
                                }
                            
                            if (value.filter(x => a.includes(x)).length==0) {                             
                                return false}
                                
                                // !value.some((e)=>a.includes(String(e)))) return false 
                                
                        // }
                    
                    }
                    
                    for (let [key, func] of Object.entries(readyDateRange)) {

                        if (row[key]) {
                            
                            if (!func(row[key])) return false;
                        } else {
                            return false;
                        }
                        
                    }
                    return true;
                })
               
                this.page = 1;
                this.totalPage = Math.ceil(this.filterdata.length/this.page_size);
                this.loading=true
            },
            changePage() {

            },
            clickRow(value, settings) {
                // let index = inputArr.findIndex(el => el.name === searchName);
                // this.rowData = this.datatable.find(i => i.code === settings.item.code)
                
                this.openindex = this.datatable.findIndex(i => i.code === settings.item.code)
                // this.openindex = settings.index + (this.page-1)*this.page_size
               
                this.rowData = this.datatable[this.openindex];
                
                this.$store.commit("thisshowForm", true);
                
            },
            save(newdata) {
                let data = Object.assign({},newdata)
                let sub_system=[]
                data.sub_system.forEach((e)=>{sub_system.push(e)})            
                data.sub_system=sub_system
                this.$http
                .post('/api/ens/passport/', {data, method: 'update'})
                .then(() => {
                    
                    for (let [key, value] of Object.entries(data)) {                       
                        // this.filterdata[this.openindex][key] = value
                        this.datatable[this.openindex][key] = value
                        // this.datatable[this.filterdata[this.openindex].id][key] = value;
                 
                    }
                    this.$store.commit("thisshowForm", false);
                    
                })
            },
            clear() {

                for (let [key, value] of Object.entries(this.formData)) {
                    // if (typeof value == 'string') {
                    //     this.formData[key] = '';
                    // } else {
                        this.formData[key] = [];
                    // }
                }

                for (let [key, value] of Object.entries(this.dateRange)) {
                    this.dateRange[key].with = "";
                    this.dateRange[key].by = "";
                }
                
            },
            backMain() {
                this.$store.commit("thisshowForm", false);
                // document.getElementById("menu-items").querySelector("[href='/statistic/passports']").closest(".v-list-group__items").removeEventListener("click", this.backMain)
            },
            converMode(arr, reverse=false)  {

                const translator = [['Мониторинг', true], ['Нормализация', false], ['Пустой', null]];
                let i1 = reverse? 1: 0;
                let i2 = reverse? 0: 1;
                
                return arr.map((el) => {
                    if (el == translator[0][i1]) return translator[0][i2];
                    if (el == translator[1][i1]) return translator[1][i2];
                    if (el == translator[2][i1]) return translator[2][i2];
                    return el;
                });
            
            },
           
            
        },
        computed: {
            showDataTable() {

                return [...this.filterdata].slice((this.page-1)*this.page_size, this.page*this.page_size);
            },
            booleanMode: {
                get() {
                    return this.converMode(this.formData.mode, true);
                },
                set(value) {
                    this.formData.mode = this.converMode(value);
                   
                }
            },
            booleanMultiMode: {
                get() {
                    return this.converMode(this.multi.mode, true);
                },
                set(value) {
                    
                    // this.formData.mode = this.converMode(value);
                }
            } 
            
        },
        
        async mounted() {
           globalFuncs.permissiondenied(this.$route.path)
            const filters = await this.getFiltersWithoutRecord({
                sub_system_ens: [{ name: "sub_system", related_name: "name", sort: "none" }],
                priority: [{ name: "priority", related_name: "name", sort: "none" }],
                criticality: [{ name: "criticality", related_name: "name", sort: "none" }],
                responsible: [{ name: "responsible", related_name: "name", sort: "none" }],
              
            })
           
            for (let [key, val] of Object.entries(filters)) {
                this.multi[key] = val;
            }
            this.multiData = filters;


            const data = await this.$http
            .get('/api/ens/passport/')
           
          
            const dictSets = {}

            let validate = (val) => {

                if (val ==  '') {
                    return 'Пустой'
                }

                if (val == null) {
                    return '';
                }
                
                return val

            }
            
            for (let field of this.namefilters) {
                dictSets[field] = new Set();
            }
            
            for (let row of data.data) {
                
                for (let [key, val] of Object.entries(dictSets)) {  
                    if (key=="mode") val.add(validate(row[key])) 
                    if (typeof row[key]=="string" ||(key=='date_of_including_of_the_initial_list' && row[key]==null)) {       
                        val.add(validate(row[key]));}
                    else if(typeof row[key]=="undefined"||row[key]==null) {
                        val.add(validate(""))                    }
                    else if (typeof row[key]=="object"){
                        for (let [x,y] of Object.entries(row[key])){
                           
                            val.add(validate(y.name))
                        }
                        
                    }
                }
                let arr=[]
                if (row['sub_system'] && row['sub_system'].length>0) row['sub_system'].forEach((e)=>{arr.push(e.name)})
                row['sub_system']=arr
            }

            for (let [key, val] of Object.entries(dictSets)) {
                
                this.multi[key] = Array.from(val);
                this.multi[key].sort((a, b) => {
                    
                    if (a == 'Пустой') return -1;
                    if (b == 'Пустой') return 1;
                    if (key=="name"){
                        if (String(a).toLowerCase().replace(/[^a-zа-яё.]/gi, '') > String(b).toLowerCase().replace(/[^a-zа-яё.]/gi, '')) return 1;
                        if (String(a).toLowerCase().replace(/[^a-zа-яё.]/gi, '') <  String(b).toLowerCase().replace(/[^a-zа-яё.]/gi, '')) return -1;
                    }
                    if (key=="code"){
                        if (Number(String(a).replace("_",".").replace(" ",".").split(".")[0]) > Number(String(b).replace("_",".").replace(" ",".").split(".")[0])) return 1;
                        if (Number(String(a).replace("_",".").replace(" ",".").split(".")[0]) <  Number(String(b).replace("_",".").replace(" ",".").split(".")[0])) return -1;
                    }
                    else{
                        if (String(a).toLowerCase() > String(b).toLowerCase()) return 1;
                        if (String(a).toLowerCase() <  String(b).toLowerCase()) return -1;
                    }
                    return 0;
                });
            }

            let indexD = this.multi['date_of_including_of_the_initial_list'].indexOf('');
            if (indexD !== -1) {
                delete this.multi['date_of_including_of_the_initial_list'].splice(indexD, 1)
            }

            this.totalPage = Math.ceil(data.data.length/this.page_size);
            this.datatable = data.data;
            this.datatable.forEach((el, index) => {
                el.id = index;
            })
            this.filterdata = data.data;
          

            this.loading = true
        }
    }
</script>

<style lang="scss" >

    .main-align {        
        display: flex;
        flex-direction: column;
        height: 100%;
    }



</style>