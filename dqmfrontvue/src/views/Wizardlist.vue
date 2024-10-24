<template>
<shell-with-loading :loading="loading" style="height: 100vh;">
    <filters-bar @clear="clear" @sendData="updateData" :header="'ИНТЕРАКТИВНЫЙ ПОМОЩНИК'">
            <template v-slot:toptext>
            <div class="mb-4 pl-1">
                <v-avatar
                color="primary"
                >
                <v-icon
            class="bigpic"
            color="white"
            
            >mdi-human-handsdown</v-icon> </v-avatar>
            <span class="ml-3 toptext">Я - ваш гид по исправлению ошибок в данных. Выберите паспорт, который вамнеобходимо нормализовать. Начнем?</span>
            </div>
            </template>
            <template v-slot:filterslist>
            <v-row class="flex-row">
               <v-col
                lg="6"
                class="pr-0"
            >
                    <f-multi-select
                    class="flex-item"
                        :field="'passport__code'"
                        title="Код паспорта"
                    ></f-multi-select>
                </v-col>
               <v-col
                lg="6"
                class="px-0"
               >
                    <f-multi-select
                    class="flex-item mr-3"
                        :field="'passport__name'"
                        title="Название паспорта"
                    ></f-multi-select>
                
               </v-col>
                    <div class="flex-item mr-3 FIL_item_9">
           
                </div>
            </v-row>
            </template>


            </filters-bar>
   
    <div class="px-3 px-5 scroll-block">
    <v-data-table
    class="pointertable grow-table pl-1"
    :headers="headers"
    :items="datatable"
    hide-default-footer
    :custom-sort="mySort"
        :fixed-header="true"
        :must-sort="true"
        sort-by="passport__code"
        :sort-desc="true"
        disable-pagination
        @dblclick:row="clickRowed"
    
   
    >

     <template v-slot:[`item.actions`]="{ item }">
         <v-tooltip
                   
                            color="primary"
                            bottom
                        >
                            <template
                                v-slot:activator="{ on, attrs }"
                            >
                                <v-icon
                                    style="cursor:pointer; font-size:1.5rem!important"
                                    v-bind="attrs"
                                    v-on="on"
                                    small
                                    class="mr-2"
                                    
                                    color="orange"
                                    @click="cardItem(item)"
                                >
                                    mdi-cards-variant
                                </v-icon>
                            </template>
                                <span>К карточкам</span>
                        </v-tooltip>
     <v-tooltip
                   
                            color="primary"
                            bottom
                        >
                            <template
                                v-slot:activator="{ on, attrs }"
                            >
                                <v-icon
                                    style="cursor:pointer; font-size:1.5rem!important"
                                    
                                    v-bind="attrs"
                                    v-on="on"
                                    small
                                    class="mr-2"
                                    
                                    color="green"
                                    @click="mapItem(item)"
                                >
                                    mdi-file-tree
                                </v-icon>
                            </template>
                                <span>К схеме</span>
                        </v-tooltip>

     
    </template>




    </v-data-table>
    </div>
</shell-with-loading>
</template>

<script>
import globalFuncs from '@/utils/helper'
import { clearAxios } from '@/utils/axios-api'
import { createNamespacedHelpers } from "vuex";
const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");
export default {
name: "Wizardlist",
data(){
    return{
        
        loading:false,
        nowsort:'-passport__code',
        datatable:[],
        headers: [
            {text: 'Код паспорта', value:'passport__code'},
            {text:"Наименование", value:'passport__name'},
            { text: 'Действия', value: 'actions', sortable: false }],
            
        namefilters: ['code', 'name'],
    }
   
},
methods:{
    ...mapMutations(["setFields"]),
    ...mapActions(["clear", "getFilters", "addFilter", "activefilters"]),
    cardItem(it){        
        localStorage.setItem("wizardswitch", JSON.stringify(0))
        this.clickRow(it)
    },
    mapItem(it){
    localStorage.setItem("wizardswitch", JSON.stringify(1))
    this.clickRow(it)
   ;
    },
    async giveDataTable(){
        // this.loading=false
        
           
        const filters = await this.activefilters();
        
        
        const res= await this.$http.get(`/api/wizard/list/`,{
                        params:{sort:this.nowsort,
                        filters: JSON.stringify({...filters})}
                    })
                                  
            this.datatable = res.data.results;                                           
            // this.loading=true                 
                                       
            ;
        },
    
    mySort(items, sortBy, sortDesc, locale) {
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
    clickRowed(value, settings){
        this.clickRow(settings.item)
    },
    clickRow(it){        
        this.$store.commit('wizardparams', {"passport__id": it.passport__id})
        localStorage.setItem("wizardinfo", JSON.stringify({"passport__id": it.passport__id}))
        this.$router.push({ path: '/wizard/card' })
    },

    async updateData() {
            
            await this.giveDataTable();
        },

},
async mounted(){
    globalFuncs.permissiondenied(this.$route.path)
     this.setFields({           
            passport__code: { module: "mult" },
            passport__name: { module: "mult" },
        });
        this.getFilters({
           
            passports: [
                { name: "passport__code", sort: "", related_name: "code" },
                { name: "passport__name", sort: "", related_name: "name" },
               
            ],
        }).then(async (data) => {
        
            })
    await this.updateData()
    this.loading=true
}

,

        }
</script>

<style lang="scss">
@import "@/utils/colors.scss";
.bigpic{
 font-size: 3rem !important;
}
.toptext{
    font-size: 1.2rem !important; 
    color: $bg-purple;
}

</style>

