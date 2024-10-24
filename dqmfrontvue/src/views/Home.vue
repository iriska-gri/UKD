<template>
<v-container class="flex-col vh-100 r" fluid>
    <v-row class="headerHome flex-grow-0">
        <v-col>                
            <h1 class="thebiggest ">
                    ВЕБ-СЕРВИС УПРАВЛЕНИЕ КАЧЕСТВОМ ДАННЫХ
            </h1>
        </v-col>
        <!-- <v-col class="flex-row justify-end">
            <div class=" Home_item_1_2_1 radiused pt-1"
                    v-for="(item, i) in menuItems"
                    :key="i"
                    :style="`background: ${item.bg}`"
                >
                <router-link
                    :to="item.path"
                    class="nonehref px-3"
                >
                    {{item.name}}
                </router-link>
                </div>
        </v-col> -->
    </v-row>
<v-row >
    <v-col class="pt-0 f flex-col">
                     <v-card class="flex-grow-1">
                        <news-list
                            :content="content.news"
                            :fileiconss="fileiconss"
                            :header="'НОВОСТНАЯ ЛЕНТА'"
                        />
                    </v-card>
    </v-col>




    <v-col class="flex-col">
        <div class="flex-col flex-grow-1">
            <v-row class="flex-col flex-grow-1">
                <v-col
                class="flex-col gh"
   
                >


                     <v-card class="flex-item f1 flex-col">
                    <div class="flex-static_row Home_item_2_2_1_1"  v-if="Object.keys(linearchart).length">
                         <h2 class="pt-3 pl-3">
                            КОЛИЧЕСТВО НД ФБ1 ПО СОСТОЯНИЮ НА {{content.linear?formatDate(content.linear[content.linear.length-1].date_unloading):''}}
                        </h2>
                    </div>
                    <div class="Home_item_2_2_1_1" v-else>
                        <v-skeleton-loader
                            class="pt-3 pl-4"
                            type="heading"
                        ></v-skeleton-loader>
                    </div>
                <v-card
                
                class="flex-item flex-col mx-3 card_Home_item_2_2_1">

                    <div class="flex-item  flex-row Home_item_2_2_1_2">
                        <div class="flex-grow-0 flex-col Home_item_2_2_1_2_1" v-if="Object.keys(linearchart).length">
                            <animatednumber
                                class="superbigHome1"
                                :value='content.linear?content.linear[content.linear.length-1].countData:0'
                            />
                        </div>
                        <div class="flex-item flex-col Home_item_2_2_1_2_1" v-else>
                            <v-skeleton-loader
                                class="superbigHome"
                                type="button"
                            ></v-skeleton-loader>
                        </div>
                        <div class="flex-grow-1 flex-col px-4 Home_item_2_2_1_2_2">
                            <linear
                                class=""
                                :chartData='linearchart'
                                :chartOptions='chartLineOptions'
                                :height="calcheightchart(1.7)"
                            />
                        </div>
                    </div>
                    <div class="flex-static_row Home_item_2_2_1_3" v-if="Object.keys(linearchart).length">
                        <span class="pl-3 pb-2 my-auto boldcolored">
                            *динамика изменений количества нд с {{content.linear?formatDate(content.linear[0].date_unloading):''}} по {{content.linear?formatDate(content.linear[content.linear.length-1].date_unloading):''}}
                        </span>
                    </div>
                    <div class="Home_item_2_2_1_3" v-else>
                        <v-skeleton-loader
                            class="pl-4 pb-2"
                            type="heading"
                        ></v-skeleton-loader>
                    </div>
                </v-card>

                <div class="flex-item flex-row mt-2 pb-3 px-3 Home_item_2_2_2">
                    <div
                        class="flex-item flex-col  Home_item_2_2_2_1"
                        v-for="(n) in 3"
                        :key=n
                    >
                    <v-card class="flex-item flex-col Home_item_2_2_2_1"
                    >
                        <don
                            class=""
                           
                            :chartData='content.nd?piedata(content.nd[n-1], content):{}'
                            :chartOptions ='content.nd?pieoptions(content.nd[n-1], content):{}'
                        />
                    </v-card>
                    </div>
                </div>
                </v-card>
                </v-col>


                <v-col class="flex-col px-0">
                      <v-card class="flex-grow-0 flex-col" >
                        <div class="flex-col ma-3 flex-grow-1">
                        <v-row >
                            <v-col class="flex-grow-0 pa-0" v-if="content.totalpassports">
                                <animatednumber class="superbigHome" :value='content.totalpassports'/>
                            </v-col>
                            <v-col class="flex-grow-0 pa-0" v-else>
                                                        <v-skeleton-loader
                            class="align-self-center pa-4"
                            type="button"
                        ></v-skeleton-loader>
                            </v-col>
                            <v-col v-if="barchart" class="pa-0 pl-5 align-self-center">
                                                       <span class="bigger ">
                            Количество паспортов ФБ1 по состоянию на {{content.linear?formatDate(content.linear[content.linear.length-1].date_unloading):0}}
                        </span>
                            </v-col>
                            <v-col class="pa-0 pl-5 align-self-center" v-else>
                        <v-skeleton-loader 
                            type="card-heading"
                        ></v-skeleton-loader>
                            </v-col>
                        </v-row>
                        </div>
                    <!-- <div class="flex-item flex-col Home_item_2_4_1_1" v-if="content.totalpassports">
                        <animatednumber class="superbigHome" :value='content.totalpassports'/>
                    </div>
                    <div class="flex-item flex-col Home_item_2_4_1_1" v-else>
                        <v-skeleton-loader
                            class="superbigHome"
                            type="button"
                        ></v-skeleton-loader>
                    </div>
                    <div class="flex-item flex-col  Home_item_2_4_1_2" v-if="barchart">
                        <span class="bigger">
                            Количество паспортов по состоянию на {{content.linear?formatDate(content.linear[content.linear.length-1].date_unloading):0}}
                        </span>
                    </div>
                    <div class="flex-item flex-col pl-6 Home_item_2_4_1_2" v-else>
                        <v-skeleton-loader 
                            type="card-heading"
                        ></v-skeleton-loader>
                    </div> -->
                </v-card>
                <v-card class="flex-grow-1 f flex-col">
                    <v-row>
                        <v-col class="g">
                    <mybar
                      
                        :chartData='barchart?barchart:{}'
                        :chartOptions='chartBarOptions'
                        :height ="calcheightchart(30.5)"
                    />
                        </v-col>
                    </v-row>
              
                </v-card>
                </v-col>
            </v-row>
        </div>
    </v-col>
</v-row>
</v-container>
 
</template>

<script>

import { clearAxios } from '@/utils/axios-api'
import { bus } from "@/main";
import NewsList from '@/components/statistic/ord/NewsList.vue'
import Linear from '../components/statistic/dashboard/linear.vue';
import Mybar from '../components/statistic/dashboard/mybar.vue'
import Don from '../components/statistic/dashboard/don.vue'
import Animatednumber from '../components/UI/Animatednumber.vue'
import  chartlogic  from "@/utils/charts/chartlogic.js"
import moment from 'moment';
import jshelper from '@/utils/helper'
import glob from '@/utils/helper'


export default {
    name: "Home",
    components: {
        Animatednumber,
        NewsList,
        Linear,
        Mybar,
        Don,
    },
    mixins:[chartlogic],
    data() {
            return {
                 desserts:[],
          headers: [
          {
            text: 'ФИО',
            align: 'start',
            sortable: true,
            value: 'name',
          },
        //   { text: 'Код паспорта', value: 'code' },
          { text: 'Контактный телефон', value: 'phone' },
          
        ],       
                loading:false,
                nd:{
                    1:["Старые НД",['#41B883', '#E9E9E9']],
                    2:["Новые НД",['#754DEC', '#E9E9E9']],
                    3:["ВПНД",['#FFC100', '#E9E9E9']],
                },
                barchart:false,
                linearchart:{},
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
                            },
        // menuItems:[
        //     {name: "Справочная информация",
        //     path: "/statistic/maindocs",
        //     bg:"rgba(255,0,0,.15)"
        //     },
        //     {name: "Паспорта",
        //     path: "/statistic/passports",
        //     bg:"rgba(255,255,0,.2)"
        //     },
        //     {name:"Мониторинг",
        //     path: "/statistic/monitoring",
        //     bg:"rgba(65,184,131,.2)"
        //     },
        //     {name:  "Списки",
        //     path: "/statistic/list",
        //     bg:"rgba(175,250,255,.3)"
        //     },
          
        //     {name:  "Дашборд",
        //     path: "/dashboard",
        //     bg:"rgba(10,22,255,.1)"
        //     },
        //     ],

        chartLineOptions: {
           
           scales: {      
                xAxis: {      
                display:false,
                },
                yAxis:{
                    display:false
                }      
             },
            elements:{point:{radius: 1}},
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
            chartBarOptions: { 
                        responsive: true,
                        layout: {
                               
                                },  
                        maintainAspectRatio: false,
                        indexAxis: 'y',                     
                        plugins:{legend: {                                
                              display: false},
                                title: {
                                display: true,
                                text: 'Топ 5 паспортов по количеству ошибок на конец периода'
                              }, 
                               tooltip: {
                                callbacks: {
                                    title:function(context){
                                     
                                       return glob.passportnamed(context[0].label).map((e)=>{return e}).join("\n")

                                    },
                                            label: function(context) {
                                                let label = context.dataset.label || '';

                                                if (label) {
                                                        
                                                    label += ': ';
                                                }
                                                if (context.parsed.x !== null) {
                                                
                                                    label += ((context.parsed.x>=10000)||(context.parsed.x<=-10000))?new Intl.NumberFormat('ru-RU').format(context.parsed.x):context.parsed.x
                                                }
                                                return label;
                                            }
                                            },
                                
                    enabled: true,
                    backgroundColor: '#43425D'
                },          
                              datalabels: {
                                display:true,
                                anchor: 'end',
                                align: 'end',
                                formatter: (val) => this.formatter(val)
                                }                             
                                
                              },
                                     
                        scales:
                            {                                                         
                              y:{                                               
                                grid: {
                                    // display: false,
                                     lineWidth:0,
                                     drawBorder: false
                                    },                                      
                                                     
                                ticks:{
                                    crossAlign: "far",
                                    callback: function(value){return `${this.getLabelForValue(value).slice(0,20)}...`}
                                        }
                            },
                     
                            xAxis: {  
                                grace:"10%",                                                               
                                grid:{
                                    lineWidth:0, 
                                    drawBorder: false                                                                                                      
                                },                                
                                ticks:{                                    
                                color:"transparent" },                                                            
                            },
                           
                           
                        }
                         },
                         
                panel:'44vh',
                content: {
                news: [],
                adress:[],
                metodologs:[]
                
            }, 

                    }
            
    },
     created(){
      
    bus.$on('loadfileiconpushed', item=>{      
        //  Скачивание data - объект со всеми данными файла   
    
    clearAxios({
        url: this.$http.defaults.baseURL +"media/"+ item.file,
        method: "GET",
        responseType: "blob" // important
      }).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;        
        link.setAttribute("download", item.doc +"." + this.fileext(item.file)); //or any other extension
        document.body.appendChild(link);
        link.click();
        link.remove()
      });   
      
    })
    
  },
    async mounted(){
        moment.locale('ru')
        const data = await this.$http
            .get('/api/contacts/mainpage/')
        this.content = data.data       
        while (this.content.nd.length<3){
            this.content.nd.push({countData:0, type_error: this.content.nd.length})
        };

        this.loading=!this.loading
        this.linearchart = this.builddata4chart(this.content.linear,"date_unloading", false,false,5)
        
        
        this.barchart= this.builddata4chart(this.content.toppassports,'passport__name', 'passport__code', false)
        // this.desserts=jshelper.gettabdata(data.data.metodologs)

    },

    methods:{
    formatter(integer){
      return ((integer>=10000)||(integer<=-10000))?new Intl.NumberFormat('ru-RU').format(integer):integer
    },    
    

    fileext(filestr){
    let fileext = filestr.split(".")
    return fileext[fileext.length-1]

    },
    formatDate(value){               
        return  moment(value, 'YYYY-MM-DD').format('DD.MM.YYYY')
    },
    rounded(number){
        return +number.toFixed(2);
    },

    piedata(data,content){
        
        let datacountData= data.countData?data.countData:0
        let total=content.linear[this.content.linear.length-1].countData
        // let a=this.rounded(datacountData/total*100)
        // let dtp = [a, 100-a]
        // console.log( datacountData, total);
        return { 
            // hovers: {thisdata: datacountData, total:total},
            labels: [this.nd[data.type_error][0]  ],
            datasets: [
                {
                    backgroundColor: this.nd[data.type_error][1] ,
                    data: [datacountData, total-datacountData]
                }
            ]
      }
      
    },

    pieoptions(data, content){

        let total=this.formatter(content.linear[this.content.linear.length-1].countData)
        return  {
           plugins: {
            datalabels: {display:false, },
            legend: {display:false},
            tooltip: {
                position: 'myCustomPositioner',
                enabled: true,

                backgroundColor: '#43425D',
                callbacks: {
                    label: function(data) {
                        return `${data.formattedValue} из ${total}`
                    }
                }
            },
            
                title: {
                        display: true,
                        text: this.nd[data.type_error][0]
                        },     
             },
                responsive: true,
                maintainAspectRatio: false,
                cutout: '80%',
      }



    },
    
    },

};
</script>

<style lang="scss">
@import '@/utils/colors.scss';



.thebiggest {
    color: $bg-purple;
    font-size: 1.5rem !important;
    // font-size: 2em !important;
    // font-weight: 800;
    // color: $bg-purple ;
}

.nonehref {
    text-decoration: none;
    color: $bg-purple;
    font-size: 1.2em !important;
    font-weight: 800 !important;
}

.boldcolored {
    font-weight: bold;
    color: $bg-purple;
}
.f {
    min-height: 313px;

}

.bigger {
    color: $bg-purple;
    font-size: 1.5rem !important;
    font-weight: 700;
}

.superbigHome, .superbigHome1{
    color: $bg-purple;
    font-size: 3rem !important;
    font-weight: 800 !important;
    padding-left: 20px;

}
.g {
    max-width: 90%;
}

.superbigHome1 {
padding-left: 10px;
}

.r {
    background: #F9F9F9;
}

.headerHome {
    align-items: flex-end;
    background: white;
    min-height: 42px;
    
}

.Home_item_1_2 {
    justify-content: end;
    gap: 1px;
}

.Home_item_2_1, .Home_item_2_2, .Home_item_2_3, .Home_item_2_4 {
    min-width: 515px;
    min-height: 360px;
    height: 100%;
}




.Home_item_2_2_1_1 {
    flex-basis: 10%;

    .v-skeleton-loader__heading {
        border-radius: 12px;
        height: 24px;
        width: 41%;
    }
}


.Home_item_2_2_1_2 {
    flex-basis: 80%;
}

.Home_item_2_2_1_2_1 {
   
    justify-content: center;
        .v-skeleton-loader__button {
            border-radius: 4px;
            height: 53px;
            width: 141px;
        }

}

.Home_item_2_2_1_2_2 {
    width: 60%;
    height: 150px;
    
    .lin_items canvas {
        flex-grow: 0;
}
}

.Home_item_2_2_1_3 {
    flex-basis: 10%;
    .v-skeleton-loader__heading {
        border-radius: 12px;
        height: 24px;
        width: 46%;
}

}

.Home_item_2_2_2 {
    max-height: 49%;
    min-height: 100px;
    gap: 8px;
    flex-wrap: nowrap;
}

.Home_item_2_2_2_1 {
    width: 100%;
    flex-basis: 25%;
}

.Home_item_2_3 {
    gap: 15px;
}

.Home_item_2_3_1 {
    min-height: 40px;
        .v-skeleton-loader__heading {
            border-radius: 12px;
            height: 17px;
            width: 20%!important;
        }

}
.Home_item_2_3_2 {
    
    overflow-y: auto;

    .v-skeleton-loader__image {
        height: 95px;
        border-radius: 8px;
        width: 95%;
        margin-left: 15px;
        margin-bottom: 21px;
    }
}

.card_Home_item_2_3_2 {
    width: 100%;
    align-self: center;
    justify-content: center;
}

.Home_item_2_3_2_1 {
    align-self: center;
    width: 95%;
    height: 55%;
    gap:5px;
}
       

.Home_item_2_4 {
    gap: 8px;
}

.card_Home_item_2_4_1 {
    flex: 0 0 20%;
}

.Home_item_2_4_1_1 {
    justify-content: center;
    width: 12.5%;
    min-width: 150px;
        .v-skeleton-loader__button {
            border-radius: 4px;
            height: 53px;
            width: 141px;
        }
}
.Home_item_2_4_1_2 {
    width: 70%;
    justify-content: center;
        .v-skeleton-loader__heading {
            border-radius: 0px;
            height: 34px;
            margin-left: 0;
            width: 86%;
        }
}

.card_Home_item_2_4_2 {
  height: 50px;
}

.Home_contact, .Home_adress {
    min-height: 10%;
        min-height: 40px;
}

.Home_adress{
    gap: 18px;
    align-content: center;
}
.Home_support {
    height: 1%;
    min-height: 20px;
    .a .v-skeleton-loader__heading {
        width: 23%;
    }
}
.Home_methodolog {
    height: 65%;
    min-height: 50px;
    overflow-y: auto;
    .v-skeleton-loader__text {
        height: 98%;
    }
}
.Home_table {
    max-height: 150px;
}

.v-skeleton-loader__text {
    border-radius: 6px;
    flex: 1 0 auto;
    height: 46px;
    margin-bottom: 6px;
}

@media (max-width: 1600px) {
    .Home_item_1_2 {
        display: none !important;
    }

}

@media (max-width: 1330px) {
    .don_skelet .v-skeleton-loader__avatar {
        border-radius: 50%;
        height: 100px;
        width: 100px;
    }

    .Home_item_2_1, .Home_item_2_2, .Home_item_2_3, .Home_item_2_4 {
        min-height: 250px;
    }
    .Home_item_2_2_1_2_1, .Home_item_2_2_1_2_1 {
        width: 100%;
    }
    .Home_item_2_2 {
        min-height: 410px;
    }
    .superbigHome {
        padding-left: 0;
        align-self: center;
        font-size: 2rem !important; 
    }
    .Home_item_2_4 {
        min-height: 450px;
    }
    .Home_item_2_4_1_1 {
        min-height: 45px;
        .superbigHome {
            font-size: 3rem !important;
        }
    }

    .bigger {
        text-align: center;
    }
}

@media (max-width: 819px) {

    .Home_item_2_4_1_1 {
        .superbigHome {
            font-size: 2rem !important; 
    }
    }
     
    }

@media (max-width: 780px) {
    .Home_item_2_1, .Home_item_2_2, .Home_item_2_3, .Home_item_2_4 {
        width: 100%;
        min-width: 0;
    }

    .superbigHome {
        font-size: 2rem !important; 
    }


}
@media (max-width: 1010px) {

   .gh {
    padding: 12px!important;
}



}

@media (max-height: 582px) {
    .superbigHome {
        font-size: 2rem !important; 
    }
}

@media (max-height: 870px) {
    .don_skelet .v-skeleton-loader__avatar {
        border-radius: 50%;
        height: 100px;
        width: 100px;
    }
}
.f1 {
    min-height: 480px;
}

.gh {
    padding: 0px;
}

.wightcol {
    max-width: 50%;
}
.radiused{
    border-top-left-radius: 8px ;
    border-top-right-radius: 8px ;
    
     }


    
</style>

