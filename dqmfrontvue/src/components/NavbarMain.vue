<template>
    <v-navigation-drawer
        app
        id="navigator-menu"
        v-model="drawer"
        :mini-variant.sync="mini"
        stateless
        width="300"
        mini-variant-width="60"
        color="primary"
    >
        <div class="d-flex flex-column pt-3" style="height: 100%" id="menu-items">
            <h2 class="title-nav text-center pb-2 ">
                <span v-if="!mini" class=" font-gray">УПРАВЛЕНИЕ КАЧЕСТВОМ ДАННЫХ</span
                >
                <span v-else>ᅠ ᅠ </span>
            </h2>
            <v-list
            
             class="">
                <!-- mb-10 -->
                <v-list-item>
                    <v-list-item-avatar class="mr-auto">
                        <v-img
                            :src="this.$store.getters.photo"
                        ></v-img>
                    </v-list-item-avatar>
                    <v-list-item-title class="ml-4 font-white"
                        >{{ avatarName }}</v-list-item-title
                    >
                    <v-btn class="font-gray" icon @click.stop="closeMenu">
                        <v-icon>mdi-chevron-left</v-icon>
                    </v-btn>
                </v-list-item>
            </v-list>
         
            <v-list-item-group>
                <div v-for="(item, i) in menuItems" :key="i">
                    <v-list-item dense v-if="i==0||!item.sub && userpermission(item)" link :to="item.path || false">
                        <v-list-item-icon class="mr-0">
                            <v-icon x-small class="font-gray">{{ item.icon }}</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title class="font-gray">{{
                                item.title
                            }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list

                    dense
                     class="font-gray py-0" v-else-if="item.sub && userpermission_anyOf(item.sub)">
                        <v-list-group
                            
                            
                            :value="true"
                            ref="collapsibleclose"
                            class="font-gray"
                        >
                        <!-- :value="item.active" -->
                            <template v-slot:activator>
                                <v-list-item-icon class="mr-0">
                            <v-icon x-small class="font-gray">{{ item.icon }}</v-icon>
                                </v-list-item-icon>
                                <v-list-item-title class="font-gray">{{
                                    item.title
                                }}</v-list-item-title>
                            </template>

                            <div
                                v-for="(item2, i) in item.sub"
                                :key="item2.title"
                                class="ms-4"
                            >
                                <div v-if="userpermission_anyOf(item2.sub)">
                                <v-list-item
                                    class="py-0"
                                    dense
                                    v-if="!item2.sub && userpermission(item2)"
                                    link
                                    :to="item2.path || false"
                       
                                >
                                    <!-- <v-list-item-icon class="mr-0">
                                        <v-icon x-small>{{ "mdi-arrow-right" }}</v-icon>
                                    </v-list-item-icon> -->
                                    <v-list-item-title class="font-gray"
                                       
                                    >{{item2.title}}
                                    </v-list-item-title>
                                </v-list-item>

                                <v-list dense ref="level2"
                                class="py-0"
                                 v-else-if="item2.sub && userpermission_anyOf(item2.sub)">
                                    <v-list-group
                                        :value="true"
                                       ref="collapsibleclose"
                                       @click="collapselist(i, 'level2')"
                                       class="font-gray"
                                    >
                                        <template v-slot:activator >
                                            <v-list-item-title class="font-gray">{{
                                                item2.title
                                            }}</v-list-item-title>
                                        </template>
                                        <div
                                            
                                            v-for="item3 in item2.sub"
                                            :key="item3.title"
                                            class="ms-4"
                                        >
                                            <v-list-item
                                            dense
                                            class="py-0"
                                                v-if="!item3.sub && userpermission(item3)"
                                                link
                                                 @click="thisshowForm()"
                                                :to="item3.path || false"
                                            >
                                                <!-- <v-list-item-icon>
                                                    <v-icon>{{
                                                        "mdi-arrow-right"
                                                    }}</v-icon>
                                                </v-list-item-icon> -->
                                                <v-list-item-title
                                                    class="font-gray"
                                                  
                                                >{{item3.title}}</v-list-item-title>
                                            </v-list-item>
                                            <v-list
                                            class="py-0"
                                             dense v-else-if="item3.sub && userpermission_anyOf(item3.sub)">
                                                <v-list-group
                                                    :value="true"                            
                                                    ref="collapsibleclose"
                                                    class="font-gray"
                                                >
                                                    <template v-slot:activator>
                                                        <v-list-item-title class="font-gray">{{
                                                            item3.title
                                                        }}</v-list-item-title>
                                                    </template>
                                                    <div
                                                     v-for="item4 in item3.sub"                                                        
                                                        :key="item4.title"
                                                    >
                                                    <v-list-item
                                                        dense
                                                        v-if="userpermission(item4)"
                                                       
                                                        class="ps-10 py-0"
                                                        @click="thisshowForm()"
                                                        link
                                                        :to="item4.path || false"
                                                    >
                                                        <!-- <v-list-item-icon class="mr-0">
                                                            <v-icon  x-small class="font-gray">{{
                                                                "mdi-arrow-right"
                                                            }}</v-icon>
                                                        </v-list-item-icon> -->
                                                        <v-list-item-title class="font-gray"
                                                         
                                                        ><v-icon  x-small class="font-gray pr-2">{{
                                                                "mdi-arrow-right"
                                                            }}</v-icon>{{item4.title}}
                                                        
                                                        
                                                        </v-list-item-title>
                                                    </v-list-item>
                                                    </div>
                                                </v-list-group>
                                            </v-list>
                                        </div>
                                    </v-list-group>
                                </v-list>
                                </div>
                            </div>
                        </v-list-group>
                    </v-list>
                </div>
            </v-list-item-group>
            
            <div>
                <v-list dense class="py-0">
                 <v-list-item-group v-for="(item, i) in centraltools" :key="i">
                     <v-list-item
                     v-if="userpermission(item)"
                     dense
                      link :to="item.path"                                     
                     >
                        <v-list-item-icon class="mr-0">
                            <v-icon x-small class="font-gray">{{ item.icon }}</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title class="font-gray">{{
                                item.title
                            }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                 </v-list-item-group>
                 </v-list>
            </div>
            <div class="mt-auto">
                 <!-- <v-list-item-group v-for="(item, i) in menuTools" :key="i">
                     <v-list-item
                      link :to="item.path"                                     
                     >
                        <v-list-item-icon>
                            <v-icon class="font-gray">{{ item.icon }}</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title class="font-gray">{{
                                item.title
                            }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                 </v-list-item-group> -->
            </div>
             <div v-if="superuser()">
                <v-list dense class="py-0">
                 <v-list-item-group v-for="(item, i) in adminTools" :key="i">
                     <v-list-item dense v-if="item.title!='Админка'"
                      link :to="item.path"
                     >
                        <v-list-item-icon class="mr-0">
                            <v-icon x-small class="font-gray">{{ item.icon }}</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title class="font-gray">{{
                                item.title
                            }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                    <v-list-item dense v-else
                      :href="item.path"
                     >
                        <v-list-item-icon class="mr-0">
                            <v-icon x-small class="font-gray">{{ item.icon }}</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title class="font-gray">{{
                                item.title
                            }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                 </v-list-item-group>
                 </v-list>
            </div>
            <div class="mt-auto">
                <v-list dense class="py-0">
                 <v-list-item-group>
                     <v-list-item dense class="py-0"
                      @click="$logout($router)"                                     
                     >
                        <v-list-item-icon class="mr-0">
                            <v-icon x-small class="font-gray">mdi-logout</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title class="font-gray">Выход
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                 </v-list-item-group>
                 </v-list>
            </div>

        </div>
    </v-navigation-drawer>
</template>

<script>
import {baseURL} from "@/utils/axios-api"
export default {
    name: "navbar-main",
    components: {},
    data() {
        
        return {
            activem:[],            
            drawer: true,
            mini: false,
            
            menuItems: [
                { icon: "mdi-home-outline", title: "Главная", path: "/", access: true},
               
                {
                    icon: "mdi-poll",
                    title: "Статистика",
                    sub: [
                        {       
                            title: "ФБ1",
                            access: true,
                            sub: [
                                {
                                    title: "Справочная информация",
                                    path: "/statistic/maindocs",
                                },
                                {  title: "Интерактивный помощник", path: "/wizard" },
                                //                                 {
                                //     title: "Песочница",
                                //     path: "/sandbox",
                                // },
                                {
                                    title: "Паспорта нормализации",
                                    path: "/statistic/passports",
                                    // sub: [
                                    //     {
                                    //         title: "Перечень",
                                            
                                            
                                    //     },
                                        //   {
                                        //      "title": "Добавление",
                                        //      "path": "/statistic/passport/add"                                            
                                        // }
                                       
                                    // ]
                                },
                                {
                                    title: "Отчетность",
                                    sub: [
                                        {
                                            title: "Мониторинг УФНС",
                                            path: "/statistic/monitoring",
                                        },
                                        // ! Сюда потом вернуть
                                         {
                                            title: "Мониторинг ИФНС",
                                            path: "/statistic/monitoringifns",
                                        },
                                        {
                                            title: "Списки",
                                            path: "/statistic/list",
                                        },
                                        // {
                                        //     title: "Исключения",
                                        //     path: "/statistic/justification",
                                        // },
                                        {
                                            title: "Динамика",
                                            path: "/statistic/dynamics",
                                        },
                                        
                                    ],
                                },
                                { icon: "mdi-chart-line", title: "Дашборд", path: "/dashboard" },
                            ],
                        },
                         {
                            title: "ЕНС",
                            access: false,
                            sub: [
                                 {
                                    title: "Справочная информация",
                                    path: "/ens/maindocs",
                                },
                                 {
                                    title: "Паспорта ЕНС",
                                    path: "/ens/passports",
                                    },
                                  {
                                    title: "Отчетность",
                                    sub: [
                                        {
                                            title: "Мониторинг УФНС",
                                            path: "/ens/monitoring",
                                        },
                                        // ! Сюда потом вернуть
                                         {
                                            title: "Мониторинг ИФНС",
                                            path: "/ens/monitoringifns",
                                        },
                                        {
                                            title: "Списки",
                                            path: "/ens/list",
                                        },
                                        // {
                                        //     title: "Исключения",
                                        //     path: "/statistic/justification",
                                        // },
                                        // {
                                        //     title: "Динамика",
                                        //     path: "/statistic/dynamics",
                                        // },
                                        
                                    ],
                                },
                                { icon: "mdi-chart-line", title: "Дашборд", path: "/ens/dashboard" },

                                
                                
                                
                                ]}
                    ],
                },
              
            ],
            centraltools:
            [
                
               
                { icon: "mdi-web", title: "Техподдержка", path: "/helper", }
            ],
           
            // menuTools: [
            //     ,
            //     // { icon: "mdi-logout", title: "Выход", path: "/settings" },
            // ],
            adminTools: [
                { icon: "mdi-key-variant", title: "Админка", path: String(baseURL).includes("127.0.0.1")? '/admin': '/api/admin/' },
                { icon: "mdi-upload", title: "Заливки", path: "/loadfile" },
            ],

         
            disabled: false,
            admins: [
                ["Management", "people_outline"],
                ["Settings", "settings"],
            ],
  
        };
    },
    // !Выкинуть mounted после теста 50
    mounted(){
        // console.log(this.userpermission({"path":"/"}))
       
        // if((JSON.parse(localStorage.getItem('profile'))["region"]==50) || this.superuser())
        // {
        //     this.menuItems[1].sub[0].sub[3].sub.splice(1,0,{
        //                                     title: "Мониторинг ИФНС",
        //                                     path: "/statistic/monitoringifns",
        //                                 })
        //                                 }
    },
    methods: {      
        
        superuser(){
                 
          return JSON.parse(localStorage.getItem('profile'))["is_superuser"]
        },
        intersect(arr1, arr2) {
      return arr1.filter(function(n) {
        return arr2.indexOf(n) !== -1;
      });
    },
        leveling(arr, s){
            arr.forEach(e=>{s.push(e.path)
             if ("sub" in e){
                this.leveling(e.sub,s)
            }}
            )
            return s
        },

        userpermission_anyOf(sub){
            
            let s = []
            let up = []
            sub.forEach(e=>{s.push(e.path)
            if ("sub" in e){
                s=[...s,...this.leveling(e.sub,s)]
            }
            })
            
            let userpermission = JSON.parse(localStorage.getItem('profile')).permission.access
            userpermission.forEach(e=>up.push(e.link))          
            
            return this.intersect(s,up).length>0

        },

        userpermission(item){
            
            let userpermission = JSON.parse(localStorage.getItem('profile')).permission.access
           
            // console.log(userpermission.find(el=>el.link==item.path)!=undefined)
            return userpermission.find(el=>el.link==item.path)!=undefined
            // return true
        },
        
        collapselist(i, key) {
            
            this.$refs[key].forEach((el, index) => {
                if (index != i) el.$children[0].isActive = false;
            })
        },
        closeMenu() {
            let activemenu=[]
            this.$refs['collapsibleclose'].forEach((el) => {
                activemenu.push(el.isActive)
                el.isActive = false;
            })
            this.activem= activemenu;
            this.mini = !this.mini;
        },

        thisshowForm(){
            this.$store.commit("thisshowForm", false);            
            },

        
    },
    computed: {
        
        avatarName() {
            
            const last_name = this.$store.getters.last_name;
            const first_name = this.$store.getters.first_name;
            return `${last_name} ${first_name}`
        },

        ca_superuser() {
            if (this.superuser() || JSON.parse(localStorage.getItem('profile'))["region"]==null) {
                return true
               
            }           
            return false
            
        }
         
              
    },
    watch:{
        "mini": function (val) {
      		if (this.mini == false) {
                
                this.$refs['collapsibleclose'].forEach((el, index) => {
                
                el.isActive = this.activem[index];
                })

    }},
    }
    
};
</script>

<style lang="scss">
@import '@/styles/variables.sass';
$gray: #9B9B9B;
.v-list-item--dense, .v-list--dense,.v-list-item{
    min-height: 33px!important;
   
}

.v-navigation-drawer__content::-webkit-scrollbar {
  width: 0;
}

#navigator-menu {
    
    cursor: pointer;
    color: $gray;
    // overflow-y: hidden;

    .font-gray {
        color: $gray;
        font-size: .9rem !important;
        
    }


    .font-white {
        color: white;
    }

    .theme--light.v-icon {
        color: $gray;
        font-size: 1.1rem !important;
    }

    .main-link-active {
        color: white;
        background:rgba($color: #ffffff, $alpha: .1);
    }

    .v-list-item--active .font-gray {
        color: white;
        
    }

    #menu-items .v-list-item--active .v-list-item__icon i {
        color: white;
        
    }
}


#navigator-menu #menu-items {

    .title-nav {
        font-size: 1em;
        white-space: nowrap;
        // color: white
    }

    .v-list-item__icon {
        // margin-top: 3px;
        // margin-bottom: 0px;
        // margin-right: auto;
        // margin-left: 5px;
        color: $gray;
    }

    .v-list-item__title {
        margin-left: 5px;
    }


}

// #menu-items 
// #9B9B9B



</style>
