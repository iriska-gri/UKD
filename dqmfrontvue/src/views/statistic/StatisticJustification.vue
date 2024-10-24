<template>
     <shell-with-loading :loading="loading" style="height: 100vh;">

           <!-- ------------------------------------------------------------------1 -->
            <filters-bar
                @clear="clearit"
                @sendData="updateData"
                :header="'ИСКЛЮЧЕНИЯ'"
                >
                <template v-slot:filterslist>
                
                    <v-col  
                        class="pa-0"
                        lg="3"
                        md="6"
                        sm="12"
                    >
                        <f-chain-select
                            field="date_unloading"
                            :period="true"
                            withtitle="Дата отчета"
                            :same="true"
                        >
                        </f-chain-select>   
                    </v-col>
                    <v-col  
                        class="pa-0"
                        lg="3"
                        md="6"
                        sm="12"
                    >          
                        <f-chain-select
                            field="justify__agreement_date"
                            :period="true"
                            :withtitle="tab==0?'Дата согласования(недоступно)':'Дата согласования'"
                            :disabled="tab==0?true:false"
                            :cleaner="true"
                            :same="true"
                        ></f-chain-select>
                    </v-col>
                    <v-col  
                        class="pa-0"
                        lg="2"
                        md="6"
                        sm="12"
                    >  
                        <f-multi-select
                            :title="tab==0?'ФИО методолога(недоступно)':'ФИО методолога'"
                            :field="'justify__methodologist'"
                            :disabled="tab==0?true:false"
                        ></f-multi-select>
                    </v-col>
                    <v-col  
                        class="pa-0 "
                        lg="4"
                        md="6"
                        sm="12"
                    >  
                        <f-multi-select
                            :field="'region__name'"
                            title="Регион"
                        ></f-multi-select>
                    </v-col>
                    <v-col  
                            class="pa-0"
                            lg="3"
                            md="6"
                            sm="12"
                        >  
                        <f-multi-select
                            :field="'passport__code'"
                            :helpfield="'passport__name'"
                            title="Код паспорта"
                        ></f-multi-select>
                    </v-col>
                    <v-col  
                            class="pa-0"
                            lg="2"
                            md="6"
                            sm="12"
                        >  
                        <f-multi-select
                            :title="tab==0?'Статус исправления (недоступно)':'Статус исправления'"
                            :field="'justify__fix_status'"
                            :disabled="tab==0?true:false"
                        ></f-multi-select>
                    </v-col>
                    <v-col  
                            class="pa-0"
                            lg="2"
                            md="6"
                            sm="12"
                        >  
                        <f-multi-select
                            :field="'justify__reason__name'"
                            :title="tab==0?'Причина исключения (недоступно)':'Причина исключения'"
                            :disabled="tab==0?true:false"
                        ></f-multi-select>
                    </v-col>
                    <v-col  
                            class="pa-0"
                            lg="1"
                            md="6"
                            sm="12"
                        >  
                            <f-input-search
                                :field="'ogrn'"
                                :type="'number'"
                                title="ОГРН/ОГРНИП"
                            ></f-input-search>                        
                    </v-col>
                    <v-col  
                            class="pa-0"
                            lg="1"
                            md="6"
                            sm="12"
                        >  
                            <f-input-search
                                :field="'inn'"
                                :type="'number'"
                                title="ИНН"
                            ></f-input-search>
                    </v-col>
                    <v-col  
                            class="pa-0"
                            lg="1"
                            md="6"
                            sm="12"
                        >  
                        <f-input-search
                            :field="'fid'"
                            :type="'number'"
                            title="ФИД"
                        ></f-input-search>
                    </v-col>
           
                </template>
            </filters-bar>
       

                   <!-- ------------------------------------------------------------------1 -->
                    <!-- --------------------------------------------------------------------------- 2 -->
        <div class="box_SJ_B mx-5 mt-3 scroll-block">
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
                
                <v-icon color="#1F6E43" class="excel px-3" @click="createExcel($event.target)"
                    >mdi-microsoft-excel
                </v-icon>
            </div>

            <!-- Таблица -->
            <v-data-table
                dense
                class="pointertable grow-table pl-1"
                :headers="headers[tab]"
                :items="datatable"
                hide-default-footer
                :custom-sort="mySort"
                :fixed-header="true"
                :must-sort="true"
                sort-by="date_unloading"
                :sort-desc="true"
                :item-class="itemRowBackground"
                @dblclick:row="clickRow"
                disable-pagination
            >
                <template v-slot:[`item.passport__code`]="{ item }">
                       <top-right-tooltip :item="item" :textfield="'passport__code'"/>
                     
               
                </template>
                <template v-slot:[`item.region__tax_code`]="{ item }">
                       <top-right-tooltip :item="item" :textfield="'region__tax_code'" :helptext="'region__name'"/>
                     
               
                </template>

                <template v-slot:[`item.date_unloading`]="{ item }">
                    {{ $changeFormatDate(item.date_unloading) }}
                </template>
                <template v-slot:[`item.justify__agreement_date`]="{ item }">
                    {{ item.justify__agreement_date? $changeFormatDate(item.justify__agreement_date): '' }}
                </template>
            </v-data-table>
        </div>
 <!-- --------------------------------------------------------------------------- 2 -->       
<!-- --------------------------------------------------------------------------- 3 -->
    <div class="box_SJ_C mt-3">        
        <div class="d-flex justify-end mt-2 mb-3 mr-3">
            <div v-if="datatablecount" class="d-flex justify-end align-center mx-5">Всего записей: {{formatter(datatablecount)}} </div>
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
    </div> 
      
        <!-- --------------------------------------------------------------------------- 3 -->
        <v-dialog 
            v-model="dialog"
             max-width="65%">
            <v-card>
                <v-card-title class="justify-center">
                    <span class="headline bgpurple" style="font-weight:bolder">Детализация </span>
                </v-card-title>
                <hr class="lined">
                <v-card-text class="pb-1">
                    <v-form
                        ref="sform"
                        v-model="valid"
                        lazy-validation
                    >
                    <v-card >
                        <div class='ml-2'>
                            <h2 class="bgpurple mt-3 mb-2">Информация о НД:</h2>
                        </div> 
                        <v-data-table
                            dense
                        :headers="tablesubhead"
                        id="infotab"
                        :items="resultinfo"
                        
                        item-key="Код паспорта"
                        
                        hide-default-footer
                        >
                        <template v-slot:[`item.passport__code`]="{ item }">
                      <top-right-tooltip :item="item" :textfield="'passport__code'"/>
               
                </template>
                <template v-slot:[`item.region__tax_code`]="{ item }">
                       <top-right-tooltip :item="item" :textfield="'region__tax_code'" :helptext="'region__name'"/>
                     
               
                </template>


                        </v-data-table>
                    </v-card>
                        <div v-if="tab==1" class="ml-2">
                                <h2 class="bgpurple  pb-1 pt-2">
                                    Файлы({{justify__justifiles__length?justify__justifiles__length:0}}):
                                </h2> 
                        </div> 
                        <div class="flex-row Jus_0"  v-if="tab==1">

                            <v-card class="flex-item d-flex Jus pb-2 " v-for="(el,index) in justify__justifiles" :key="index">
                            <v-list 
                               
                                
                                dense                                                  
                            >
                                <div class="flex-item flex-col">
                                    <v-subheader class="pt-1"><strong>{{authors[index]}}</strong></v-subheader>
                                    <v-list-item-group
                                        class='flex-item pt-1'
                                        v-model="justify__justifiles[index]"
                                    >
                                        <v-list-item
                                            v-for="v in el"
                                            :key="v.path"
                                        >
                                            <v-icon
                                                :color='v.path.split(".")[v.path.split(".").length-1] in fileiconss?fileiconss[v.path.split(".")[v.path.split(".").length-1]].color:fileiconss.other.color'
                                                class="icon pl-2"
                                                @click.stop="loadfile(v.path)" 
                                            >
                                                {{v.path.split(".")[v.path.split(".").length-1] in fileiconss?fileiconss[v.path.split(".")[v.path.split(".").length-1]].icon:fileiconss.other.icon}}
                                            </v-icon>
                                            <v-list-item-content>
                                                <div class="d-flex"
                                                    @click.stop="loadfile(v.path)">
                                                    <v-list-item-title
                                                        class="pl-2">
                                                        {{v.path.split("/")[v.path.split("/").length-1]}}
                                                    </v-list-item-title>
                                                    <v-icon
                                                    class="icon"
                                                    
                                                    >
                                                        mdi-cloud-download
                                                    </v-icon>
                                                </div>
                                            </v-list-item-content>
                                        </v-list-item>   
                                    </v-list-item-group>
                                </div>
                            </v-list>
                            </v-card > 
                        </div>
                        <div class="align-center mt-2">
                            <div v-if="tab==0">
                                <v-card class="pt-2">
                                    <h2 class="bgpurple pl-2">Выберите причину, по которой необходимо исключить НД из статистики:<span style="color:red">*</span></h2>
                                    <div class="pl-2">
                                        <v-radio-group
                                            v-model="reason"
                                                        row
                                            :rules="[value => !!value.length || 'Необходимо сделать выбор']"
                                            required
                                            class="my-0"
                                        >          
                                            <v-radio
                                           
                                                v-for="(item, index) in reasons"
                                                :key="index"
                                                color="primary"
                                                :value="item"
                                            >
                                                <template v-slot:label  class="mb-0">
                                                    <span class="bgpurplebold">{{item}}</span>
                                                </template>
                                            </v-radio>
                                        </v-radio-group>
                                    </div>                        
                                </v-card>
                                <!-- <h2 class="bgpurple" v-else>Причина исключения, указанная регионом:  </h2> -->
                            </div>
                            
                            <div v-else class="my-3 ml-2">
                                <h2 class="bgpurple">Причина исключения, указанная регионом:  </h2>
                                <span class="bgpurplebold pl-2">{{reason}}</span>                           
                                <hr>
                            </div>
                            
                        </div>
                        <h2 class="bgpurple ml-2 mt-2" v-if="tab==0">Опишите причину исключения:<span style="color:red">*</span></h2>
                        <h2 class="bgpurple ml-2 mt-2" v-else>Комментарий УФНС</h2>
                        <v-textarea
                            v-if="tab==0" 
                            :rules="[value => !!value || 'Заполните обязательно']"
                            solo 
                            rows=10
                            label="Введите текст..." 
                            v-model="description"
                            no-resize
                        >
                        </v-textarea>
                        <v-textarea v-else readonly solo label="Нет комментария" rows=6  :hide-details="true" no-resize v-model="description"> </v-textarea>
                        <div class="mt-0">
                            <h2 class="bgpurple ml-2" v-if="tab==1 && methodolog">Комментарий</h2>
                            <h2 class="bgpurple ml-2" v-else-if="tab==1">Комментарий методолога ЦА</h2>
                            <v-textarea v-if="tab==1 && ((methodolog && havenoreason)||superuser)" rows=6 no-resize  solo label="Введите текст..." :hide-details="true" v-model="methodologist_note"> </v-textarea>
                            <v-textarea v-else-if="tab==1 && methodolog && !havenoreason" readonly rows=6 no-resize solo label="Нет комментария"  :hide-details="true" v-model="methodologist_note"> </v-textarea>
                            <v-textarea v-else-if="tab==1" readonly no-resize solo label="Нет комментария" rows=6  :hide-details="true" v-model="methodologist_note"></v-textarea>
                        </div>

                        <div v-if="(tab==0 && (!methodolog||superuser))||(tab==1 && methodolog)">
                            <h2 class="bgpurple ml-2">Приложите файлы</h2>
                           
                        <multi-input :filesglob="files" :dubfilesglob="dubfiles" :clear="!dialog"  @adfto='adfto'/>
                        </div>
                    </v-form>  
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn v-if="tab==0"  depressed color="success"  @click="saveDialog"
                        >Сохранить</v-btn
                    >
                    <v-btn v-if="tab==1 && ((methodolog && havenoreason) || superuser)" color="success"  @click="savemetDialog(true)"
                        >Согласовать исключение</v-btn
                    >
                    <v-btn v-if="tab==1 && ((methodolog && havenoreason) || superuser)" color="error"  @click="savemetDialog(false)"
                        >Отказать в исключении</v-btn
                    >
                    <v-btn color="primary"  @click="dialog=false"
                        >Закрыть</v-btn
                    >
                </v-card-actions>
            </v-card>
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
import moment from "moment";
import DateCalSelect from '../../components/UI/DateCalSelect.vue';
import { clearAxios } from '@/utils/axios-api'
import MultiInput from '../../components/UI/MultiInput'
import TopRightTooltip from "@/components/UI/TopRightTooltip"
import globalFuncs from '@/utils/helper'
const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");

export default {
  components: {DateCalSelect, MultiInput, TopRightTooltip},
    name: "Justify",
   
    data() {
        return {
            error:false,  
            errortext:"",          
            authors:['От УФНС', 'От методолога'],
            valid: true,
            superuser:false,
            methodolog:false,
            row: null,
            loading: false,
            dialog: false,
            datatablecount:0,
             // Тип данных (динамические фильтры)
            tabs: [
                 {text: "Обоснования для исключения",   sort: true,},
                { text: "Перечень исключений", sort: false },
               
            ],
            tab: 0,
            dynamicfilter: {'justify__reason__name__isnull': true,
                            'justify__fix_status__isnull': true,},

            // Модалка
            methodologist_note:'',
            description: '',
            reason: '',
            reasons: [],
            idlist: {},
            files:[],
            dubfiles:new Set(),
            justify__justifiles__length:0,
            // Пагинация
            page: 1,
            totalPage: 0,
            count_pages: Array.from({length: 20}, (_, i) => (i + 1) *150),
            page_size: 150,
            havenoreason: true,
            justify__justifiles:[[],[]],
            addingfile:[],
            // Данные для таблицы
            nowsort: "-date_unloading",
            resultinfo:[],
            tablesubhead:[],

            textrow: {
                passport__code: "Код паспорта",
                region__tax_code: "Код региона",
                region__name: "регион",
                date_unloading: "Дата отчета",
                fid: "ФИД",
                inn: "ИНН",
                ogrn: "ОГРН",
                justify__date_of_justification: "Дата внесения обоснования",
                justify__agreement_date: "Дата согласования",                
                justify__methodologist: "Методолог",
                justify__fix_status:"Статус",
                passport__name:"Паспорт"

                
                
            },

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
                            other:{icon: 'mdi-file', color: "black"},
                            },


            headers: [
                [
                { text: "Дата отчета",  align: "start",  value: "date_unloading", },
                { text: "Код паспорта", value: "passport__code" },
                
                { text: "Код региона", value: "region__tax_code" },

                // {
                //     text: "Дата внесения обоснования",
                //     value: "justify__date_of_justification",
                // },
                { text: "ОГРН/ОГРНИП", value: "ogrn" },
                { text: "ИНН", value: "inn" },
                { text: "ФИД", value: "fid" },
                // {
                //     text: "Причина исключения",
                //     value: "justify__reason__name",
                // },
                // {
                //     text: "Крайний срок исправления",
                //     value: "justify__deadline_for_correction",
                // },
                // { text: "Статус исправления", value: "justify__fix_status" },
            ],[
                 
                { text: "Дата отчета",  align: "start",  value: "date_unloading", },
                { text: "Код паспорта", value: "passport__code" },
                
                { text: "Код региона", value: "region__tax_code" },

                // {
                //     text: "Дата внесения обоснования",
                //     value: "justify__date_of_justification",
                // },
                { text: "ОГРН/ОГРНИП", value: "ogrn" },
                { text: "ИНН", value: "inn" },
                { text: "ФИД", value: "fid" },
                {
                    text: "Причина исключения",
                    value: "justify__reason__name",
                },
                { text: "Статус согласования", value: "justify__fix_status" },
                {
                    text: "Дата согласования",
                    value: "justify__agreement_date",
                },
                {text: "ФИО методолога", value: 'justify__methodologist'}

            ]],
            datatable: [],
        };
    },
    methods: {
        ...mapMutations(["setFields", "setIncludeFilters"]),
        ...mapActions([
            "clear",
            "clearpart",
            "getFilters",
            "addDate",
            "addFilter",
            "activefilters",
        ]),
        clearit(){
            this.clear()
            this.updateTable()
        },
        formatter(intg){return globalFuncs.formatter(intg)},
        itemRowBackground(item){    
         
            if (item.justify__fix_status=="Согласовано"){
                return 'success'
            }
            else if (item.justify__fix_status=="Не согласовано"){
                return "error"
            }
          
        },
        adfto(data){
          
            this.files=data[0]
            this.dubfiles=data[1]
            
        },
 
        updateData() {
            // Применить фильтрацию
            this.page = 1;
            this.updateTable();
        },

        //* Методы таблиц
        giveDataTable() {
            // Получить данные для таблицы
            this.loading=false
            return new Promise(async (resolve, reject) => {
                const filters = await this.activefilters();
          
                this.$http
                    .get(`/api/statistic/fb1/reporting/justify/`, {
                        params: {
                            filters: JSON.stringify({
                                ...filters,
                                ...this.dynamicfilter,
                            }),
                            
                            page: this.page,
                            page_size: this.page_size,
                            sort: this.nowsort,
                        },
                    })
                    .then((res) => {                           
                       
                        this.datatable = res.data.results;
                        
                        if (this.tab==1){
                            for(let i=0;i<this.datatable.length; i++){
                                this.datatable[i].justify__fix_status=this.rebuildfix(this.datatable[i].justify__fix_status)
                               
                            }
                        }
                        this.loading=true
                        resolve(res.data);
                        
                    });
            });
        },

        async createExcel(el) {
            const filters = await this.activefilters();   
                     
            this.$store.commit("loadFrameTrue");
            try {
                const res = await this.$http
                .post(`/api/statistic/fb1/reporting/justify/`, {
                    params: {
                        filters: JSON.stringify({
                            ...filters,
                            ...this.dynamicfilter,
                        }),  
                        datatablecount:0,  
                        fn_modificator: this.tabs[this.tab].text,             
                        page: this.page,
                        page_size: this.page_size,
                        sort: this.nowsort,
                        headers_table: this.headers[this.tab],
                        
                    },
                })
               
                if ('error' in res.data){                    
                    this.errortext = res.data.error
                    this.error=true
                }
                else{
                this.disableExcel=''
                window.location.href = this.$http.defaults.baseURL + res.data.name;
                }
                el.blur()
                this.$store.commit("loadFrameFalse");
            } catch {
                this.$store.commit("loadFrameFalse");
            }
            
        },
        rebuildfix(fix){
            if (fix!=null){
                fix=fix?"Согласовано":"Не согласовано"
            }
            else{
                fix="На согласовании"
            }
            return fix
                                },
        updateTable() {
            // Обновить таблицу с учетом пагинации
            
            return new Promise((resolve, reject) => {
                this.giveDataTable().then((dataTable) => {
                    
                    this.totalPage = Math.ceil(dataTable.count / this.page_size);
                    this.datatablecount = dataTable.count
                    resolve("ok");
                });
            });
        },

        createJustify(data) {
            return new Promise((resolve, reject) => {
                this.$http
                    .put(`/api/statistic/fb1/reporting/justify/create/`, data,
                    // {headers: {
                    //         "Content-Type": "multipart/form-data"
                    //     }},
                                        
                    
                    )
                    .then((res) => {
                        resolve(res.data);
                        
                    });
            });
        },
       

        changePage() {
            this.giveDataTable();
        },
        changeTab(index) {
            if(index == this.tab) return;
            // // Изменения вида ненормализованных данных
           
            this.page = 1;
            this.dynamicfilter = this.tabs[index].sort? {'justify__reason__name__isnull': true,
                                                          'justify__fix_status__isnull': true, }: {'justify__reason__name__isnull': false};
            
            // --------------
            // this.$refs.sform.resetValidation()
            // this.valid=true

            this.clear();
            // this.clear()
            this.updateTable();
        },
        changeFormatDate(date) {
            // Изменения формата даннызх
            return moment(date, "YYYY-MM-DD").format("DD.MM.YYYY");
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

            return this.datatable;
        },
        clickRow(value, settings) {
            this.justify__justifiles__length=0
            if (this.$refs.sform) this.$refs.sform.resetValidation()
            this.valid=true
            this.havenoreason=settings.item.justify__fix_status=="На согласовании"?true:false
            this.methodologist_note=settings.item.justify__methodologist_note?settings.item.justify__methodologist_note:"";
            this.description = settings.item.justify__description? settings.item.justify__description: '';
            this.reason = settings.item.justify__reason__name? settings.item.justify__reason__name: '';
            this.idlist = {id: settings.item.id, index: settings.index};
            this.justisort(settings.item.justify__justifiles.length?settings.item.justify__justifiles:{} )
            this.dialog = true;
            this.resultinfo=[]
            this.tablesubhead=[]
            let res={}
            for (let[key,val] of Object.entries(this.textrow)){
                
                if ( !([null,''].includes(settings.item[key]))){

                    res[key]= ['date_unloading', 'justify__date_of_justification','justify__agreement_date','justify__justifiles'].includes(key)?  this.$changeFormatDate(settings.item[key]) : settings.item[key]
                }
            }

            for (let [key,val] of Object.entries(res))
            
                {
                    if (!(["passport__name","region__name"].includes(key))){
                    this.tablesubhead.push({text:this.textrow[key], 
                                                        sortable: false,
                                                        value: key})
                    }
                }
                
            this.resultinfo.push(res)
          
         

        },
        justisort(data){
            
            this.justify__justifiles = [[],[]]
            let key=""
            this.justify__justifiles__length=data.length
            for (let i=0;i<data.length;i++){
                key=data[i].author?1:0              
                this.justify__justifiles[key].push(data[i])                
                }
            
        },
        preparedatatosave(field){                        
            if (this.$refs.sform.validate()) {
              
                const sdata = new FormData();
                const dat ={id: this.idlist.id, fields: JSON.stringify(field),
                    }
                for (let [key, val] of Object.entries(dat)) {
                sdata.append(key, val);
                 }

                if (this.files.length>0) {                    
                    for (let el of this.files){
                        
                        sdata.append('file',el)                    
                    }
                }
            return sdata
            }
       
        },


        saveDialog(field) {     


                this.createJustify(this.preparedatatosave({
                    reason__name: this.reason, 
                    description: this.description? this.description: '',
                    })
                ).then((data) => {                  
                  
                    this.dialog=false
                    this.files=[]
                    this.dubfiles=new Set()
                    this.updateTable();
                })
            
            
            
        },
       

        savemetDialog(solution){
            
            this.createJustify(this.preparedatatosave( {
               methodologist_note:this.methodologist_note,
               fix_status: solution})
                               ).then((data) => { 
                                this.datatable[this.idlist.index].justify__methodologist = data.justify__methodologist;
                                this.datatable[this.idlist.index].justify__agreement_date = data.justify__agreement_date;
                                this.datatable[this.idlist.index].justify__fix_status = this.rebuildfix(solution)
                                this.datatable[this.idlist.index].justify__methodologist = data.justify__methodologist
                                this.dialog=false
                                this.files=[]
                                this.dubfiles=new Set()
                                this.updateTable();
                               })
          
        },
        loadfile(file){
        this.loading=true
        clearAxios({
        url: this.$http.defaults.baseURL +"media/"+ file,
        method: "GET",
        responseType: "blob" // important
      }).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        let filearr    = file.split("/")
        link.setAttribute("download", filearr[filearr.length-1])        
       
        document.body.appendChild(link);
        link.click();
        link.remove()
        this.loading=false
      });    
        }
        

    },

    mounted() {
        globalFuncs.permissiondenied(this.$route.path)
        this.methodolog= JSON.parse(localStorage.getItem('profile'))["region"]?false:true
        this.superuser= JSON.parse(localStorage.getItem('profile'))["is_superuser"]
        
        this.setFields({
            date_unloading: { module: "chain" },
            justify__agreement_date: { module: "chain" },
            justify__methodologist: { module: "mult" },
            // justify__deadline_for_correction: { module: "select" },
            region__name: { module: "mult" },
            passport__code: { module: "mult"},
            justify__reason__name: { module: "mult" },
            justify__fix_status: { module: "mult" },
        });

        this.setIncludeFilters(["date_unloading"]);

        // {
        //     name: "justify__reason__name",
        //     sort: "",
        //     related_name: "reason__name",
        // },

        this.getFilters({
            listFB1: [{ name: "date_unloading", sort: "-" }],
            reason: [{ name: "justify__reason__name", sort: "pk", related_name: "name"}],
            justify: [
                {
                    name: "justify__agreement_date",
                    sort: "-",
                    related_name: "agreement_date",
                },
                
                {
                    name: "justify__fix_status",
                    sort: "",
                    related_name: "fix_status",
                },
                {
                    name: "justify__methodologist",
                    sort: "-",
                    related_name: "methodologist",
                }
            ],
            regions: [{ name: "region__name", sort: "", related_name: "name" }],
            passports: [
                { name: "passport__code", sort: "", related_name: "code" },
               
            ],
        }).then(async (data) => {
         
            const dates = [
                               
                this.$changeFormatDate(data["date_unloading"][data["date_unloading"].length-1]),
                this.$changeFormatDate(data["date_unloading"][0]),
            ];
            await this.addDate({
                period: true,
                field: "date_unloading",
                value: [dates[0], dates[1]],
            });

            this.startdatetable = dates[0];
            this.enddatetable = dates[1];
            await this.updateTable();
            
            this.reasons = this.$store.getters['filterslogic/mult/mult_justify__reason__name'];

            this.loading = true;
        });
    },
};
</script>

<style lang="scss" scoped>
@import "@/utils/colors.scss";
.row_just {
    gap: 15px;

}
 
.filtr_width_input{
    min-width: 121px;
} 
 
.filtr_width{
    min-width: 242px;
}

.filtr_width_chain {
    min-width: 390px;
}

.Jus_0 {
    gap:1rem;
}
.grid-container {
  overflow-y: hidden;
  height: 100vh;
  display: grid;
}
.SJ_grid {

  
  grid-template-rows: 0fr 1fr 0fr;
  grid-template-columns: 1fr 1fr 1fr 1fr   1fr 1fr 1fr 1fr;
  grid-template-areas:
    "A A A A   A A A A"
    "B B B B   B B B B"
    "C C C C   C C C C"
    ;
}

.box_SJ_A {
  grid-area: A;

}
.box_SJ_B {
  grid-area: B;
overflow-x: hidden;


}
.box_SJ_C {
  grid-area: C;
}

.v-list--dense .v-list-item, .v-list-item--dense {
    min-height: 1.5rem;
}
.v-list--dense .v-list-item .v-list-item__content, .v-list-item--dense .v-list-item__content {
    padding: 0px 0;
}
.v-list {
    display: block;
    padding: 0px 0;
    }
.v-list--dense .v-subheader {
    font-size: .75rem;
    height: 27px;
    padding: 0 8px;
}
.v-list--dense .v-list-item, .v-list-item--dense {
    min-height: 20px;
}
.Jus_item_1 {
      display: flex !important;
  flex-direction: column;
    height: 150px;
}
.Jus {
    height: 100px;
    overflow-y: auto;
    overflow-x: hidden;
    max-width: 50%;
    flex-direction: column;
}

.Jus_item_2 {

     flex-direction: row;
    justify-content: space-between;
   
  
}

.Jus_item_1_1 {
    justify-content: space-between;
    height: 40px;
    
    flex-direction: row;
}
.Jus_item_2_1 {
    width: 90%;
   
}
.Jus_item_2_2 {
    width: 10px;
    justify-content: flex-end;
}

.flex-item {
  flex-grow: 1;
}

.flex-col {
  display: flex !important;
  flex-direction: column;
}
.flex-static_row {
  flex: 0 0 auto;
  display: flex  !important;
  flex-direction: row;
  flex-wrap: wrap;
}

h2{
    font-size: 1rem !important
}
.prefix-select {
    color: $gray;
    font-family: "Roboto", Arial, Helvetica, sans-serif;
    font-weight: bold;
}

.tab-table {
    font-size: 0.6em;
    color: $gray;
}



// Динамическая высота для таблицы
.scroll-block {
    display: flex;
    flex-direction: column;
    overflow-y: hidden;
    flex-grow: 3;
    height: 100%;
}

.bgpurple{
    color: $bg-purple;
}
.bold{
    font-weight: 800;
}
.bgpurplebold{
    font-weight: 700;
    color: black;
    font-size: 1.1rem !important
}
hr {
    border-top:1px dashed $bg-purple;
   
}

.lined{
    border-top:1px solid $gray;
}
// .grow-table {
//     display: flex;
//     flex-direction: column;
//     overflow-y: hidden;

// }


</style>
<style lang="scss">
#infotab{

 tbody {
     tr:hover {
        background-color: transparent !important;
     }
   }  }
</style>