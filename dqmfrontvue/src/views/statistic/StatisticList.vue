<template>
    <shell-with-loading :loading="loading" style="height: 100vh;">
        <filters-bar @sendData="updateData" @clear="clearit"
        :header="'СПИСКИ'" 
        :helper="'Для поиска пустых НО/РО введите не число'">
        <template v-slot:filterslist>
           <v-col  
                class="pa-0 "
                lg="2"
                md="6"
                sm="12"
            >
                <f-multi-select
                    :field="'date_unloading'"
                    title="Даты выгрузки"
                >
                </f-multi-select>
           </v-col>
           <v-col  
                class="pa-0"
                lg="3"
                md="6"
                sm="12"
            >
                <f-multi-select
                    :field="'region__name'"
                    :title="storegetterreg.text"
                    :disabled="storegetterreg.val"
                >
                </f-multi-select>
           </v-col>
           <v-col  
                class="pa-0 "
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
           
            <v-col  
                class="pa-0 flex-row"
                lg="4"
                md="6"
                sm="12"
            >
            <f-input-search
                    :field="'ogrn'"
                    :type="'number'"
                    title="ОГРН/ОГРНИП"
                ></f-input-search>
                <f-input-search
                    :field="'inn'"
                    :type="'number'"
                    title="ИНН"
                >
                </f-input-search>
                 <f-input-search
                    :field="'fid'"
                    :type="'number'"
                    title="ФИД"
                >
                </f-input-search>
            </v-col>
         
            <v-col  
                class="pa-0 flex-row"
                lg="2"
                md="6"
                sm="12"
            >
                <f-input-search
                    :field="'nocode'"
                    title="Код НО"
                ></f-input-search>
                  <f-input-search
                    :field="'rocode'"
                    title="Код РО"
                ></f-input-search>
                    
            </v-col>
           
              
                     
        
           </template>

        </filters-bar>
        
        <div class="px-5 scroll-block">
            <div class="d-flex">
                <!-- Виды ненормализованных данных -->
                <v-tabs 
                slider-size="0"
                 height='30'
                v-model="tab">
                    <v-tab
                        v-for="(tab, index) in tabs"
                        :key="index"
                        class="tab-table"
                        active-class= "activetab"
                        @click="changeTab(index)"
                    >
                        {{ tab.text }}
                    </v-tab>
                </v-tabs>
                <div class="d-flex align-center" style="background:white; ">
                <span v-if="disableExcel" style="background:white; color:red; font-weight:bold; white-space: nowrap;">*В Excel невозможно загрузить более одной даты</span>
                </div>
                <v-icon v-if="disableExcel" color="gray" class="excel px-3"
                    >mdi-microsoft-excel</v-icon
                >
                <v-icon v-else color="#1F6E43" class="excel px-3" @click="createExcel($event.target)"
                    >mdi-microsoft-excel</v-icon
                >
                
            </div>
            <!-- Таблица -->
            <v-data-table
                dense
                :headers="headers"
                :items="datatable"
                hide-default-footer
                :custom-sort="mySort"
                :must-sort="true"
                
                sort-by="date_unloading"
                :sort-desc="true"
                :fixed-header="true"
                disable-pagination
                class="grow-table pl-1"
            >
                <template v-slot:[`item.date_unloading`]="{ item }">
                    {{ $changeFormatDate(item.date_unloading) }}
                </template>

                <template v-slot:[`item.passport__code`]="{ item }">
                    <top-right-tooltip :item="item" :textfield="'passport__code'"/>
                     <!-- <span
                           @mouseenter="hovered(item, $event.target)" 
                         @mouseleave="buttonHovering = false"
                            ref="tooltipio"
                            style="cursor:pointer"
                            >{{ item.passport__code }}</span>
                     -->
                       
                      
                     
            
                </template>

            </v-data-table>
        </div>
       
        
        <div class="d-flex justify-end align-center mt-2 mb-3 mr-3">
            <div class="d-flex justify-end align-center mx-5">Всего записей: {{formatter(datatablecount)}} </div>
            <div class="d-flex justify-end align-center select-page mr-5 mt-1">
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
         <v-snackbar
                v-model="error"
                >                
                Не найдено записей
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
const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");
import globalFuncs from '@/utils/helper'
import TopRightTooltip from "@/components/UI/TopRightTooltip"
// import TopRightTooltip from '../../components/UI/TopRightTooltip.vue';
export default {

    name: "List",
    components:{TopRightTooltip},
    data() {
        return {
           
            loading: false,
            // Тип данных (динамические фильтры)
            tabs: [
                { text: "Список НД", sort: {} },
                {
                    text: "Старые НД",
                    sort: { type_error: 1 },
                },
                { text: "Новые НД", sort: { type_error: 2 } },
                {
                    text: "ВПНД",
                    sort: { type_error: 3 },
                },
            ],
            error:false,
            tab: 0,
            dynamicfilter: {},
            disableExcel: false,
            // disableregion: false,
            // Пагинация
            page: 1,
            totalPage: 0,
            count_pages: Array.from({length: 10}, (_, i) => (i + 1) *150),
            page_size: 150,
            datatablecount:0,
            // Данные для таблицы
            nowsort: "-date_unloading",
            headers: [
                {
                    text: "Дата отчета",
                    align: "start",
                    value: "date_unloading",
                },
                { text: "Код региона", value: "region__tax_code" },
                { text: "Регион", value: "region__name" },
                {text: "Код НО", value: "nocode"},
                {text: "Код РО", value: "rocode"},
                { text: "Код паспорта", value: "passport__code" },
                { text: "ОГРН/ОГРНИП", value: "ogrn" },
                { text: "ИНН", value: "inn" },
                { text: "ФИД", value: "fid" },
                // { text: "ID ошибки", value: "id_error" },
            ],
            datatable: [],
            storegetterreg:{text:'Регион',val:false}
        };
    },
     
    methods: {
        ...mapMutations(["setFields"]),
        ...mapActions(["clear", "getFilters", "addFilter", "activefilters"]),
        
        //* Динамические методы
        formatter(intg){return globalFuncs.formatter(intg)},
        storegetterregf(){
            if(this.$store.getters.region == null){
            this.storegetterreg = {text:'Регион', val:false}}
            else{this.storegetterreg = {text:'Регион (недоступно)', val:true}}
            
        },
        clearit(){
            this.clear()
            this.updateData()
        },
       
        changeTab(index) {
            if (index == this.tab) return;
            // Изменения вида ненормализованных данных
            this.page = 1;
            this.dynamicfilter = this.tabs[index].sort;
            this.storegetterregf();
            this.updateTable();
        },

        changePage() {
            // Пролистывание данных
            this.giveDataTable();
        },

        //* Методы обновления всех данных, используя фильтры
        async updateData() {
            // Применить фильтрацию
            
            this.page = 1;
            await this.updateTable();
        },

        //* Методы таблиц
        async giveDataTable() {
            // Получить данные для таблицы
            this.loading= false
            const filters = await this.activefilters();
            
            this.disableExcel=(!('date_unloading__in' in filters) || filters.date_unloading__in.length>1)?true:false;
            
            
            const res = await this.$http.get(`/api/statistic/fb1/reporting/list/`, {
                params: {
                    filters: JSON.stringify({
                        ...filters,
                        ...this.dynamicfilter,
                    }),
                    page: this.page,
                    page_size: this.page_size,
                    sort: this.nowsort,
                },
            });
            this.loading= true
            this.datatable = res.data.results;
           
            return res.data;
        },
        async updateTable() {
            // Обновить таблицу с учетом пагинации
            this.loading= false
            const dataTable = await this.giveDataTable();
            
            this.totalPage = Math.ceil(dataTable.count / this.page_size);
            this.datatablecount=dataTable.count
            this.loading= true
        },
        async createExcel(el) {
            // Получить данные для таблицы
            
            const filters = await this.activefilters();
            this.disableExcel=(!('date_unloading__in' in filters) || filters.date_unloading__in.length>1)?true:false;
            if (!this.disableExcel){
            this.$store.commit("loadFrameTrue");
            try {
                let table =  [...this.headers];
               
                // table.splice(3,0,{text: "Код НО", value: "nocode"})
                // table.splice(4,0,{text: "Код РО", value: "rocode"})
                table.push({text: "Тип ошибки", value: "type_error"})
                
                const res = await this.$http.post(`/api/statistic/fb1/reporting/list/`, {

                    params: {
                        filters: JSON.stringify({
                            ...filters,
                            ...this.dynamicfilter,
                        }),
                        page: this.page,
                        fn_modificator: this.tabs[this.tab].text,
                        page_size: this.page_size,
                        sort: this.nowsort,
                        headers_table: table,

                    },
                }).then((res) => {
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
            } catch {
                this.$store.commit("loadFrameFalse");
               

            }     
            }
            
            
        },
        mySort(items, sortBy, sortDesc, locale) {
            // Сортировка таблицы

            const sign = sortDesc[0] ? "-" : "";
            const sort = `${sign}${sortBy[0]}`;
            if (this.nowsort != sort) {
                this.nowsort = sort;

                this.giveDataTable().then(() => {
                    return this.datatable;
                });
            }
    
            // if (['inn','-inn', 'fid','-fid','ogrn','-ogrn','passport__code','-passport__code'].includes(this.nowsort)){
            //         let isDesc = this.nowsort[0]=="-"?false:true
         
            //         this.datatable.sort((a,b)=>{
            //             if (['passport__code','-passport__code'].includes(this.nowsort)){
            //                 let one = String(a.passport__code).replace("_",".").replace(/[a-zа-яё]/gi, '')
       
            //                 let two = String(b.passport__code).replace("_",".").replace(/[a-zа-яё]/gi, '')
            //                 if (parseFloat(this.$splitter(one)) > parseFloat(this.$splitter(two))) return isDesc?1:-1;
            //                 if (parseFloat(this.$splitter(one)) <  parseFloat(this.$splitter(two))) return isDesc?-1:1;
                            
            //             }
            //         return 0
            //         })
                    
            // }

            return this.datatable;
        },
    },
    mounted() {
        globalFuncs.permissiondenied(this.$route.path)
        this.storegetterregf()
        this.setFields({
            date_unloading: {
                module: "mult",
                correct: (arr) => {   
                    let narr=[]             
                    arr.map((el) => {narr.push(this.$changeFormatDateReverse(el))})                    
                    return narr},
            },
            region__name: { module: "mult" },
            passport__code: { module: "mult" },
        });
        this.getFilters({
            listFB1: [{ name: "date_unloading", sort: "-" }],
            regions: [{ name: "region__name", sort: "", related_name: "name" }],
            passports: [
                { name: "passport__code", sort: "", related_name: "code" },
            ],
        }).then(async (data) => {
            
            if (data.region__name.length==1){
            await this.addFilter({
                key: "region__name",
                value: [this.$insertRegion(data.region__name[0])]
            });
            }



            await this.addFilter({
                key: "date_unloading",
                value: [this.$changeFormatDate(data.date_unloading)],
            });
            
            this.updateTable().then(() => {
                // this.loading = true;
                
            });
        });
    },
};
</script>

<style lang="scss" scoped>
@import "@/utils/colors.scss";

.tab-table {
    font-size: 0.6em;
    color: $gray;
}

.filtr_width{
    min-width: 220px;
}

.filtr_width_input{
    min-width: 121px;
} 
// Динамическая высота для таблицы

.scroll-block {
    display: flex;
    flex-direction: column;
    overflow-y: hidden;
    flex-grow: 3;
    height: 100%;
}

// .grow-table {
//     display: flex;
//     flex-direction: column;
//     overflow-y: hidden;

// }
.FIL_item_8 {
    flex-wrap: nowrap;
}




</style>