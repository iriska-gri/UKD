<template>
     <shell-with-loading :loading="loading" style="height: 100vh;">
        <div class="grid-container SJ_grid">
            <div class="box_SJ_A">
            <!-- ------------------------------------------------------------------1 -->
        <filters-bar @clear="clear" @sendData="updateData">
            <div class="flex-item flex-row FIL_item">
                <div class="flex-item mr-3 FIL_item_1">
                    <f-chain-select
                        field="date_unloading"
                        :period="true"
                        withtitle="Дата отчета"
                        :same="true"
                    >
                    </f-chain-select>
                </div>
                <div class="flex-item mr-3 FIL_item_2">
                    <f-chain-select
                        field="justify__date_of_justification"
                        :period="true"
                        withtitle="Дата согласования"
                        :disabled="tab==0?true:false"
                        :cleaner="true"
                        :same="true"
                    ></f-chain-select>


                </div>
                <div class="flex-item mr-3 FIL_item_3"> 
                    <f-multi-select
                        :title="tab==0?'ФИО методолога(недоступно)':'ФИО методолога'"
                        :field="'justify__methodologist'"
                        :disabled="tab==0?true:false"
                    ></f-multi-select>
                </div>
                <div class="flex-item mr-3 FIL_item_4">
                    <f-multi-select
                        :field="'region__name'"
                        title="Регион"
                    ></f-multi-select>
                </div>
                <div class="flex-item mr-3 FIL_item_5">
                    <f-multi-select
                        :field="'passport__code'"
                        title="Код паспорта"
                    ></f-multi-select>
                </div>
                <div class="flex-item mr-3 FIL_item_6">
                    <f-multi-select
                        :title="tab==0?'Статус исправления (недоступно)':'Статус исправления'"
                        :field="'justify__fix_status'"
                        :disabled="tab==0?true:false"
                    ></f-multi-select>
                </div>
                <div class="flex-item mr-3 FIL_item_7">
                    <f-multi-select
                        :field="'justify__reason__name'"
                        :title="tab==0?'Причина исключения (недоступно)':'Причина исключения'"
                        :disabled="tab==0?true:false"
                    ></f-multi-select>
                </div>
                <div class="flex-item flex-row mr-3 FIL_item_8">
                    <div class="flex-item mr-3 FIL_item_8_1">
                    <f-input-search
                        :field="'ogrn'"
                        :type="'number'"
                        title="ОГРН/ОГРНИП"
                    ></f-input-search>
                    </div>
                    <div class="flex-item FIL_item_8_2">
                        <f-input-search
                            :field="'inn'"
                            :type="'number'"
                            title="ИНН"
                        ></f-input-search>
                    </div>
                </div>
                <div class="flex-item mr-3 FIL_item_9">
                    <f-input-search
                        :field="'fid'"
                        :type="'number'"
                        title="ФИД"
                    ></f-input-search>
                </div>


              
            </div>
          
            
        </filters-bar>
         </div>

                    <!-- ------------------------------------------------------------------1 -->
                    <!-- --------------------------------------------------------------------------- 23 -->
        <div class="box_SJ_B mx-5 mt-3 scroll-block">

            <div class="d-flex">
    
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
                    >mdi-microsoft-excel</v-icon
                >
            </div>


            
     
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
            <div v-if="datatablecount" class="d-flex justify-end align-center mx-5">Всего записей: {{datatablecount}} </div>
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
      
            <v-pagination
                v-model="page"
                :length="totalPage"
                :total-visible="10"
                @input="changePage"
            ></v-pagination>
        </div>
        </div> 
        </div>
<!-- --------------------------------------------------------------------------- 3 -->
        <v-dialog v-model="dialog" max-width="45%">
            <v-card>
                <v-card-title class="justify-center">
                    
                    <span class="headline bgpurple" style="font-weight:bolder">Детализация </span>
                   
                    
                </v-card-title>
                <hr class="lined">
                <v-card-text>
                    <v-form
                                ref="sform"
                                v-model="valid"
                                lazy-validation
                            >
                    <div class='ml-2'>
                    <h2 class="bgpurple mt-3 mb-2">Информация о НД:</h2>
                    
                    
                    <div style="color:black; font-weight:bold" class="pl-2" v-for="(value,key) in resultinfo" :key="key">{{key}} : {{value}}</div>
                      </div>  
                    <div class="align-center mt-3">
                        <div  v-if="tab==0">
                            <v-card class="pt-2"><h2 class="bgpurple pl-2">Выберите причину, по которой необходимо исключить НД из статистики:<span style="color:red">*</span></h2>
                                <div class="pl-2">
                            
                                <v-radio-group
                                v-model="reason"
                                            row
                                :rules="[value => !!value.length || 'Необходимо сделать выбор']"
                                required
                                                >
                                            
                                <v-radio v-for="(item, index) in reasons" :key="index"
                                    color="primary"
                                    
                                    :value="item"
                                    
                                > <template v-slot:label>
                                            <span class="bgpurplebold">{{item}}</span>
                                            </template>
                                
                                
                                
                                
                                </v-radio>
                                    </v-radio-group>
                            
                                </div>                        
                            
                            </v-card>
                       
                        </div>
                        
                        <div v-else class="my-3 ml-2">
                            <h2 class="bgpurple">Причина исключения, указанная регионом:  </h2>
                           <span class="bgpurplebold pl-2">{{reason}}</span>                           
                            <hr>
                        </div>
                        
                    </div>
                    

                    <h2 class="bgpurple ml-2 mt-4" v-if="tab==0">Опишите причину исключения:<span style="color:red">*</span></h2>
                    <h2 class="bgpurple ml-2 mt-4" v-else>Комментарий УФНС</h2>
                    <v-textarea v-if="tab==0" 
                    :rules="[value => !!value || 'Заполните обязательно']"
                    solo 
                    label="Введите текст..." 
                    v-model="description"
                    no-resize
                    
                    > </v-textarea>

                    <v-textarea v-else readonly solo label="Нет комментария"  :hide-details="true" no-resize v-model="description"> </v-textarea>
                    <v-card class="Jus_item_1">
                        <div class="d-flex Jus_item_1_1">
                            <h2 class="bgpurple pl-2 pb-1 pt-2" v-if="tab==0">При необходимости, прикрепите файлы:</h2>
                            <v-icon class="pr-5">mdi-paperclip</v-icon>
                        </div>
                        <v-card class="d-flex Jus">
                            <div class="d-flex Jus_item_2 my-1"
                                v-for="(item, i) in 10"
                                :key="i">
                                <div class="d-flex flex-item Jus_item_2_1" >
                                    <v-icon
                                        class="icon pl-2"
                                    >
                                        mdi-image-size-select-actual
                                    </v-icon>
                                    <v-list-item-title
                                        class="pl-2">
                                        Название картинки
                                    </v-list-item-title>
                                </div>
                                <div
                                    class="d-flex flex-item Jus_item_2_2">
                                    <v-icon
                                        class="icon pr-3"
                                    >
                                    mdi-delete
                                    </v-icon>
                                </div>

                            </div>
                
                        </v-card >
                    </v-card >
                    

                    <div class="mt-4">
                     
                     <h2 class="bgpurple ml-2" v-if="tab==1 && methodolog">Комментарий</h2>
                     <h2 class="bgpurple ml-2" v-else-if="tab==1">Комментарий методолога</h2>
                    <v-textarea v-if="tab==1 && ((methodolog && havenoreason)||superuser)" no-resize  solo label="Введите текст..!." :hide-details="true" v-model="methodologist_note"> </v-textarea>
                    <v-textarea v-else-if="tab==1 && methodolog && !havenoreason" readonly no-resize solo label="Нет комментария"  :hide-details="true" v-model="methodologist_note"> </v-textarea>
                    <v-textarea v-else-if="tab==1" readonly no-resize solo label="Нет комментария"  :hide-details="true" v-model="methodologist_note"> </v-textarea>
                    
                    
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
       
    </shell-with-loading>
</template>

<script>

import { createNamespacedHelpers } from "vuex";
import moment from "moment";
import DateCalSelect from '../../components/UI/DateCalSelect.vue';

const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");

export default {
  components: { DateCalSelect },
    name: "Justify",
   
    data() {
        return {
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
            

            // Пагинация
            page: 1,
            totalPage: 0,
            count_pages: Array.from({length: 20}, (_, i) => (i + 1) *150),
            page_size: 150,
            havenoreason: true,
            // Данные для таблицы
            nowsort: "-date_unloading",
            resultinfo:{},
            
            textrow: {
                passport__code: "Код паспорта",
                region__tax_code: "Код региона",
                date_unloading: "Дата отчета",
                fid: "ФИД",
                inn: "ИНН",
                ogrn: "ОГРН",
                justify__date_of_justification: "Дата внесения обоснования",
                justify__agreement_date: "Дата согласования",                
                justify__methodologist: "Методолог",
                
                
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
        itemRowBackground(item){    
         
            if (item.justify__fix_status=="Согласовано"){
                return 'success'
            }
            else if (item.justify__fix_status=="Не согласовано"){
                return "error"
            }
            // return item.justify__fix_status==true ?  'success':'error' 
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
                        
                        // if(this.nowsort.includes("passport__code")){
                    
                        //     if(this.nowsort[0]=="-"){
                        //         res.data.results.sort((a, b) => {
                    
                        //          if (Number(String(a.passport__code).replace("_",".").replace(" ",".").split(".")[0]) > Number(String(b.passport__code).replace("_",".").replace(" ",".").split(".")[0])) return -1;
                        //          if (Number(String(a.passport__code).replace("_",".").replace(" ",".").split(".")[0]) <  Number(String(b.passport__code).replace("_",".").replace(" ",".").split(".")[0])) return 1;
                        //             return 0;
                        //     })
                        //     }
                        //     else{
                        //     res.data.results.sort((a, b) => {
                        //          if (Number(String(a.passport__code).replace("_",".").replace(" ",".").split(".")[0]) > Number(String(b.passport__code).replace("_",".").replace(" ",".").split(".")[0])) return 1;
                        //          if (Number(String(a.passport__code).replace("_",".").replace(" ",".").split(".")[0]) <  Number(String(b.passport__code).replace("_",".").replace(" ",".").split(".")[0])) return -1;
                        //     return 0;
                        //     }
                            
                        //     )}
                        // };       
                       
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
                }).then((res)=>{
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
                    .post(`/api/statistic/fb1/reporting/justify/create/`, data)
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
            if (this.$refs.sform) this.$refs.sform.resetValidation()
            this.valid=true
            this.havenoreason=settings.item.justify__fix_status=="На согласовании"?true:false
            this.methodologist_note=settings.item.justify__methodologist_note?settings.item.justify__methodologist_note:"";
            this.description = settings.item.justify__description? settings.item.justify__description: '';
            this.reason = settings.item.justify__reason__name? settings.item.justify__reason__name: '';
            this.idlist = {id: settings.item.id, index: settings.index};
            this.dialog = true;
            this.resultinfo={}
            for (let[key,val] of Object.entries(this.textrow)){
                if ( !([null,''].includes(settings.item[key]))){

                    this.resultinfo[val]= ['date_unloading', 'justify__date_of_justification','justify__agreement_date'].includes(key)?  this.$changeFormatDate(settings.item[key]) : settings.item[key]
                }
            }
            
 




        },
        saveDialog() {
            
            
            if (this.$refs.sform.validate()) {
                this.createJustify({id: this.idlist.id, fields: {
                    reason__name: this.reason, 
                    description: this.description? this.description: ''}
                }).then((data) => {
                 
                    // this.datatable[this.idlist.index].justify__date_of_justification = data['date_of_justification'];
                    // this.datatable[this.idlist.index].justify__deadline_for_correction = data['deadline_for_correction'];
                    // this.datatable[this.idlist.index].justify__reason__name = this.reason;
                    // this.datatable[this.idlist.index].justify__description = this.description;
                    this.dialog=false
                    this.updateTable();
                })
            
            
            }
        },
       

        savemetDialog(solution){
            
            this.createJustify({id: this.idlist.id, fields: {
               methodologist_note:this.methodologist_note,
               fix_status: solution}}
                               ).then((data) => { 
                                this.datatable[this.idlist.index].justify__methodologist = data.justify__methodologist;
                                this.datatable[this.idlist.index].justify__agreement_date = data.justify__agreement_date;
                                this.datatable[this.idlist.index].justify__fix_status = this.rebuildfix(solution)
                                this.datatable[this.idlist.index].justify__methodologist = data.justify__methodologist
                                this.dialog=false
                                this.updateTable();
                               })
          
        }
        

    },

    mounted() {
        this.methodolog= JSON.parse(localStorage.getItem('profile'))["region"]?false:true
        this.superuser= JSON.parse(localStorage.getItem('profile'))["is_superuser"]
        
        this.setFields({
            date_unloading: { module: "chain" },
            justify__date_of_justification: { module: "chain" },
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
                    name: "justify__date_of_justification",
                    sort: "-",
                    related_name: "date_of_justification",
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
                // data["date_unloading"].length-1
                
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

.Jus_item_1 {
      display: flex !important;
  flex-direction: column;
    height: 150px;
}
.Jus {
    overflow-y: auto;
  overflow-x: hidden;
  
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
    font-weight: 800;
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