<template>
    <v-container
        fluid
        class="vh-100  c1 flex-col pt-0 px-1"
    >
    <!-- <v-row class="flex-grow-0 header_sait"> -->
    <!-- <v-col >
        <h1 class="pl-2 thebiggest"> ЗАЛИВКИ И СТАТИСТИКА

        </h1>
        </v-col>
    </v-row> -->
    <fills-and-statistics
    ref="tab"
    >
        <template #stat>
           <statistic/>

        </template>
        <template #stattable>
            <stattab/>
        </template>
       
     
        <template #fills>
    <v-row>
        <v-col>


        <v-row class="strokarov px-3 flex-grow-0">
            <v-col
                class="fix_h_eye flex-col"
                lg=4
                md=6
                sm=12
            >   
            <v-card class="flex-grow-1 flex-col">
                <v-row class="flex-grow-0 ma-0 oneblock">
                    <v-col class="flex-grow-0 pb-0"
                        lg=1
                        md=1
                        sm=1
                    >
                         <v-tooltip
                                    v-if="helper.length"
                                    color="primary"
                                    right
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn
                                        class="indicator "
                                            v-bind="attrs"
                                            v-on="on"
                                            fab
                                            dark
                                            
                                            :color="colorbutton"
                                        >   
                                        </v-btn>
                                    </template>
                                    <span>{{helper}}</span>
                                </v-tooltip>
                    </v-col>
                    <v-col 
                    class="pa-0"
                    lg=10
                    md=10
                    sm=10
                    >
                  
                        <h1 class="title-load py-3">Заливка</h1>
               
                    </v-col>
                </v-row>
                <v-row class="flex-grow-0 ma-0 pt-3">
                    <v-col class="pa-0">
                        <h1 class="title_tvo ">========== Если ФБ1 - лист называем ФБ1 ==========</h1>
                         <h1 class="title_tvo ">====== Если ЕНС - лист называем ЕНС ======</h1>
                    </v-col>
                </v-row>
                <v-row class="ma-0 px-15">
                    <v-col 
                    class="align-self-center flex-col pa-0"
                    >
                        <v-file-input
                            label="Загрузите файл"
                            ref="fileinput"
                            outlined
                            dense
                            v-model="fileFB1"
                            class="pt-7"
                        ></v-file-input>     
                    </v-col>

                </v-row>
                <v-row class="flex-grow-0 ma-0">
                    <v-col class="flex-col pa-0 pb-3">
                        <v-btn
                        class="submit-button  align-self-center"

                            @click="sendFB1"
                            >
                            Отправить
                        </v-btn>
                    </v-col>
                </v-row>

            </v-card>
        </v-col>
        
      
        <v-col
            class="fix_h flex-col"
            lg=4
            md=6
            sm=12
        >
        <v-card class="flex-grow-1 flex-col">
           <v-row class="flex-grow-0 ">
                <v-col>
                    <v-divider></v-divider>
                    <h1 class="title-load py-3">Удаление загрузок</h1>
                    <v-divider></v-divider>
                </v-col>
            </v-row>
               <v-row class="ma-0 px-14 mt-2">
                <v-col class="pa-0">
                    <v-select
                    :class="'pt-0'"
                                v-model="razdel"
                                label="Подраздел"
                                :items="['ФБ1', 'ЕНС']"
                                solo
                                dense
                                ></v-select>
                                </v-col>
            </v-row>
            <v-row class="flex-grow-0 ma-0 pt-3">
                <v-col class="pa-0">
                    <h1 class="title_tvo ">Дата выгрузки</h1>
                </v-col>
            </v-row>
            <v-row class="ma-0 px-14">
                <v-col class=" align-self-center flex-col pa-0">

                    <f-multi-select
                        :class="'pt-0'"
                        :field="razdel=='ФБ1'?'date_unloading':'date_unloading__ens'"
                    ></f-multi-select>  
                
                </v-col>
            </v-row>
            <v-row class="flex-grow-0 ma-0">
                <v-col class="flex-col  pa-0 pb-3">
                    <v-btn
                        class="submit-button  align-self-center"
                        color="error"
                        @click="delloadslayer"
                    >
                        Удалить
                    </v-btn>
                </v-col>
            </v-row>
           
            </v-card>
        </v-col>
       
        <v-col
            class="fix_h flex-col"
            lg=4
            md=6
            sm=12
        >
            <v-card class="flex-grow-1 flex-col">
                <v-row class="flex-grow-0 ">
                    <v-col>
                        <v-divider></v-divider>
                        <h1 class="title-load py-3">Информер</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>

                <v-row >
                    <v-col class="flex-col">
                        <v-img   
                            class="align-self-center"
                            contain         
                            style="width: 40vw; max-height:16vh; min-height:16vh"                 
                            :src= buratino()
                        ></v-img>
                    </v-col>
                </v-row>
                <v-row class="flex-grow-0 ma-0">
                    <v-col class="flex-col pa-0 pb-3">
                        <v-btn 
                            class="btninf"
                            href="/media/informer/informer.exe"
                            download         
                        >
                            Скачать
                        </v-btn>
                        
                    </v-col>
                </v-row>
            </v-card>
        </v-col>
 
        <v-col
            class="flex-grow-0 flex-col"
            lg=8
            md=12
            sm=12
        >
        <v-card class="flex-grow-1 flex-row ">
            <v-col
                        lg=6
            md=12
            sm=12
            class="py-0 right_files"
            >
                <v-row class="flex-grow-0">
                <v-col>
                    <h1 class="title-load py-2 pb-3">Загрузка динамики</h1>
                    <v-divider></v-divider>
                </v-col>
            </v-row>
            <v-row class="flex-grow-0">
                <v-col
                    class="flex-row pikkalendar pt-0 justify-center"
                >
                    <v-menu 
                        v-model="datefilter"
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
                            :title="'Выберите дату для файлов'"   
                            class="align-self-center pr-3"   
                        />
                            <v-text-field
                                :value="formatDate(date_unloading)"              
                                type="date-local"              
                                placeholder="дд.мм.гггг"
                                solo
                                @input="oninputnotFilter"
                                v-bind="attrs"
                                hide-details
                                v-on="on"
                                class="pt-0 datewitxh"
                                title="Дата для файлов"
                                
                            >
                            </v-text-field>
                        </template>
                        <v-date-picker
                            :first-day-of-week="1"
                            event-color="green lighten-1"
                            v-model="date_unloading"
                        >
                        </v-date-picker>
                    </v-menu>
                </v-col>
            </v-row>
            <v-row class="flex-grow-0 ma-0">
                <v-col id="file-drag-drop">
                    <form class="formfile" ref="fileform">
                        <span class="drop-files">Перетащите файлы сюда</span>
                    </form>
                </v-col>
            </v-row>
            <v-row class="flex-grow-0 ma-0 mb-2">
                <v-col class="pa-0">
                    <progress
                        class="my-0" max="100"
                        :value.prop="uploadPercentage"
                    >
                    </progress>
                </v-col>
            </v-row>
            <v-row class="ma-0">
                <v-col
                    class="pa-0 flex-col "            
                >

                <v-btn 
                    class="submit-button align-self-center"
                    
                    v-on:click="submitFiles()"  
                    :disabled="!files.length"   
                >
                            Отправить
                        </v-btn>


                </v-col>
                <v-alert
                    v-if="resultmessage.length"
                    class="absoluten mx-auto"
                    prominent
                    :type="typemes"
                    >
        <v-row align="center" class="px-4">
            <v-col class="grow">
            {{resultmessage}}
            </v-col>
            <v-col class="shrink">
              
            <v-btn @click="closealert">Закрыть</v-btn>
            
            </v-col>
        </v-row>
    </v-alert>
            </v-row>
            </v-col>
 
            <v-col >
                <div class="pb-3 overflow-auto kl" v-if="files.length">
                    <v-row
                        v-for="(file, key) in files"
                        :key="key"
                        class="file-listing ma-0 "
                    >
                        <v-col class="flex-grow-0 align-self-center pr-2 pa-0">
                            <img
                                class="preview"
                                v-bind:ref="'preview'+parseInt( key )"
                            /> 
                        </v-col>
                        <v-col class="align-self-center pa-0">
                        {{ file.name }}
                        </v-col>
                        <v-col class="remove-container flex-grow-0 align-self-center px-4 pa-0 ">
                            <a class="remove" v-on:click="removeFile( key )">Удалить</a>
                        </v-col>
                    </v-row>
                </div>
                
                <div class="pb-3 overflow-auto kl d-flex flex-col justify-center mx-auto" v-else>
                    
                    <h2 class="align-self-center" style="color:#AFAFAF">
                    Ожидание файлов . . .
                    </h2>
                </div>
            </v-col>
        
        </v-card>
        </v-col>
       
        <v-col
            lg=4
            md=6
            sm=12
        >
        
        </v-col>



    </v-row>
    <v-overlay :value="delloadslay">
                <v-card
                elevation="2"                
                width="40vw"                
                light
                >
                <v-card-title>ВЫ УВЕРЕНЫ ЧТО ХОТИТЕ УДАЛИТЬ ВЫГРУЗКИ?</v-card-title>
                <v-card-text>Все записи будут удалены: {{filtertext}}</v-card-text>
                <v-spacer></v-spacer>
                <v-btn class="ma-2"
                color="success"
                @click="closelay"
                
                >Отказаться</v-btn>
                
                
                <v-btn
                class="ma-2"
                color="error"
                @click="delloads"
                >Подтвердить
                </v-btn>
                </v-card>
        </v-overlay>
      
            <v-overlay :value="overlay">
                <v-card
                elevation="2"                
                width="40vw"                
                light
                >
                   <v-card-title class="justify-space-between">
                    <div class="d-flex">ЗАГРУЗКА И ОБРАБОТКА ФАЙЛА</div>
                  
    <v-tooltip v-if="helper.length"
                                         color="primary"
                                          left>
                                        <template v-slot:activator="{ on, attrs }">
        

                                       <v-btn
                                        style="height:1.3em; width:1.3em"
                                          v-bind="attrs"
                                        v-on="on"
                                        fab
                                        dark
                                        small
                                        :color="colorbutton"
                        >   
                        </v-btn>
                                    </template>
                                    <span>{{helper}}</span>
                                    </v-tooltip>


                   </v-card-title>
                    <v-card-text>
                        <span v-if="percentage<100">Загружаю файл....</span>
                        <span v-else>Файл загружен</span> <v-icon  v-if="percentage==100"
                        large
                        class="ml-2"
                        color="success"                     >
                     mdi-check-bold
                    </v-icon>
                    <v-progress-linear
                    v-model="percentage"                    
                    height="25">
                     <strong :style="percentage>=50?'color:white':''">{{ Math.ceil(percentage) }}%</strong>
                    </v-progress-linear>
                    <br>
                    <span v-show="percentage==100">Обработка файла</span>
                  
                       <v-progress-linear
                    v-model="workprogress"                    
                    height="25">
                     <strong :style="workprogress>=50?'color:white':''">{{ Math.ceil(workprogress) }}%</strong>
                    </v-progress-linear>
                   <br>
                    <div v-show="actions.opening.value">
                    <span>{{actions.opening.text}}</span> 
                        <v-icon v-if="actions.columnwork.value"
                             large
                             class="ml-2"
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else large class="ml-2" color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-show="actions.columnwork.value">                    
                        <span>{{actions.columnwork.text}}</span>
                        <v-icon v-if="actions.rowwork.value"
                            class="ml-2"
                             large
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else class="ml-2" large color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-show="actions.rowwork.value">
                    <span >{{actions.rowwork.text}}. Строка  {{actions.rowwork.value}} {{actions.totalrows.text}} {{actions.totalrows.value}}
                    </span>
                    <v-icon v-if="actions.basewrighting.value"
                             large
                             class="ml-2"
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else class="ml-2" large color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-show="actions.justific.value">
                    <span>{{actions.justific.text}} {{actions.justific.value}}</span>
                  
                    </div>
                    <div v-if="actions.error.value">
                    <span>{{actions.error.text}} {{actions.error.value}}</span>
                    <v-icon large class="ml-2" color="error"> mdi-alert</v-icon>
                    </div>
                    <div  v-show="actions.basewrighting.value">
                    <span>{{actions.basewrighting.text}}</span>
                    <v-icon v-if="actions.completedshow.value"
                             large
                             class="ml-2"
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else large class="ml-2" color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-if="actions.completedshow.value && !actions.error.value">
                    <span>{{actions.completed.text}} {{actions.completed.value}}  </span>
                    <v-icon large class="ml-2" color="success">  mdi-check-bold</v-icon>
           
                    </div>
                    <div v-else-if="actions.completedshow.value && actions.error.value" >
                    <span >Произошла ошибка. Строк загружено:{{actions.completed.value}}  </span>
                   
                    <v-icon large class="ml-2" color="error"> mdi-alert</v-icon>
                    </div>
                    <v-spacer></v-spacer>
                        
                    </v-card-text>
                       <v-card-actions>
                           <v-btn v-show="actions.completedshow.value" color="primary"  @click="overlayoffer()"
                            >Закрыть</v-btn
                        >
                            </v-card-actions>
                </v-card>
               
               
            </v-overlay>
    </v-col>
</v-row>
           
        </template>
         
        <template #statonline>
<v-row>
    <v-col>
          <v-row class="strokarov px-3 flex-grow-0">

<v-col                 
    class=" fix_h_eye flex-col"
    lg=2
    md=6
    sm=12>
                <v-card class="flex-grow-1  flex-col">
                <v-row class="flex-grow-0  ma-0">
                    <v-col class="pa-0 ">
                        <v-divider ></v-divider>
                        <h1 class="title-load title_eye py-3">На входе</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>
            <v-row class="flex-grow-0 ma-0 pt-3">
                <v-col class="pa-0 ">
                    <h1 class="title_tvo "> Сейчас онлайн на входе: {{useronline.anonymousnow.length}}<br></h1>
                </v-col>
            </v-row>
                <v-row class=" ma-0 eye">
                    <v-col class="flex-col pa-0">
                        <v-data-table
                        :fixed-header="true"
                            disable-pagination
                            :headers="anonymousheaders"
                            :items="useronline.anonymousnow"
                            dense
                            hide-default-footer
                            class="elevation-1 flex-grow-1"
                        >
                        <template v-slot:[`item.entered`]="{ item }">
                            {{datebuild(item.entered)}}
                        </template>                  
                        </v-data-table>
                    </v-col>
                </v-row>
            </v-card>
</v-col>

<v-col                
    class="fix_h_eye flex-col"
    lg=2
    md=6
    sm=12>
                 <v-card class="flex-grow-1 flex-col">
                <v-row class="flex-grow-0  ma-0">
                    <v-col class="pa-0">
                        <v-divider></v-divider>
                        <h1 class="title-load py-3">В системе <br> всего {{calcmoment(summer(total.loggednow))}}</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>
            <v-row class="flex-grow-0 ma-0 pt-3">
                <v-col class="pa-0 ">
                    <h1 class="title_tvo ">Сейчас онлайн в системе: {{useronline.loggednow.length}}<br> </h1>
                </v-col>
            </v-row>
                <v-row class=" ma-0 eye">
                    <v-col class="flex-col pa-0">
                          <v-data-table
                :headers="loggednowheaders"
                :items="useronline.loggednow"
                dense
                sort-by="sn"
                group-by="region"
                hide-default-footer
                disable-pagination
                :fixed-header="true"
                 class="elevation-1 flex-grow-1 "
                    >
                    <template v-slot:[`group.header`]="{items, isOpen, toggle}">
        <th colspan="1">
          <v-icon @click="toggle"
            >{{ isOpen ? 'mdi-minus' : 'mdi-plus' }}
          </v-icon>
          {{ items[0].region=='null'?'Нет': items[0].region }}
        </th>
        <th>{{ calcmoment(total.loggednow[items[0].region]) }}   </th>
      </template>
                    <template v-slot:[`item.entered`]="{ item }">
                    {{datebuild(item.entered)}}
                    </template>                  
                    
                    
                    
                    </v-data-table>     
                    </v-col>
                </v-row>
            </v-card>
</v-col>

<v-col
    class="fix_h_eye flex-col"
    lg=4
    md=6
    sm=12>
                   <v-card class="flex-grow-1 flex-col">
                <v-row class="flex-grow-0  ma-0">
                    <v-col class="pa-0">
                        <v-divider></v-divider>
                        <h1 class="title-load py-3">За неделю онлайн зарегистрированные провели на сайте:<br> {{calcmoment(summer(total.logged_outed))}}</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>
                <v-row class="ma-0 eye">
                    <v-col class="flex-col pa-0">
                         <v-data-table
                         disable-pagination
                :headers="outedheaders"
                :items="useronline.logged_outed"
                dense
                sort-by="sn"
                group-by="region"
                :fixed-header="true"
                hide-default-footer
                
                
                 class="elevation-1 flex-grow-1"
                    >
                     <template v-slot:[`group.header`]="{items, isOpen, toggle}">
        <th colspan="2">
          <v-icon @click="toggle"
            >{{ isOpen ? 'mdi-minus' : 'mdi-plus' }}
          </v-icon>
          {{ items[0].region=='null'?'Нет': items[0].region }}
        </th>
        <th>{{ calcmoment(total.logged_outed[items[0].region]) }}   </th>
      </template>
                    <template v-slot:[`item.entered`]="{ item }">
                    {{datebuild(item.entered)}}
                    </template>   
                    <template v-slot:[`item.outed`]="{ item }">
                    {{item.outed-item.entered}}
                    </template>                  
                    
                    
                    
                    </v-data-table>
                    </v-col>
                </v-row>
            </v-card>
</v-col>

<v-col                 
    class="fix_h_eye flex-col"
    lg=4
    md=6
    sm=12>
                   <v-card class="flex-grow-1  flex-col">
                <v-row class="flex-grow-0  ma-0">
                    <v-col class="pa-0">
                        <v-divider></v-divider>
                        <h1 class="title-load py-3 px-3">За неделю онлайн по регионам:</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>

                <v-row class=" ma-0 eye">
                    <v-col class="flex-col pa-0">
                       <v-data-table
                :headers="loggedregionhead"
                :items="loggedregiontotal"
                dense
                sort-desc
                sort-by="onsite"
                hide-default-footer
                disable-pagination
                :fixed-header="true"
                 class="elevation-1 flex-grow-1"
                    >
      
                    <template v-slot:[`item.onsite`]="{ item }">
                    {{calcmoment(item.onsite)}}
                    </template>                  
                    
                    
                    </v-data-table>
                    </v-col>
                </v-row>
            </v-card>
</v-col>

           
       
      
 
      



    </v-row>
    <v-overlay :value="delloadslay">
                <v-card
                elevation="2"                
                width="40vw"                
                light
                >
                <v-card-title>ВЫ УВЕРЕНЫ ЧТО ХОТИТЕ УДАЛИТЬ ВЫГРУЗКИ?</v-card-title>
                <v-card-text>Все записи будут удалены: {{filtertext}}</v-card-text>
                <v-spacer></v-spacer>
                <v-btn class="ma-2"
                color="success"
                @click="closelay"
                
                >Отказаться</v-btn>
                
                
                <v-btn
                class="ma-2"
                color="error"
                @click="delloads"
                >Подтвердить
                </v-btn>
                </v-card>
        </v-overlay>
      
            <v-overlay :value="overlay">
                <v-card
                elevation="2"                
                width="40vw"                
                light
                >
                   <v-card-title class="justify-space-between">
                    <div class="d-flex">ЗАГРУЗКА И ОБРАБОТКА ФАЙЛА</div>
                  
    <v-tooltip v-if="helper.length"
                                         color="primary"
                                          left>
                                        <template v-slot:activator="{ on, attrs }">
        

                                       <v-btn
                                        style="height:1.3em; width:1.3em"
                                          v-bind="attrs"
                                        v-on="on"
                                        fab
                                        dark
                                        small
                                        :color="colorbutton"
                        >   
                        </v-btn>
                                    </template>
                                    <span>{{helper}}</span>
                                    </v-tooltip>


                   </v-card-title>
                    <v-card-text>
                        <span v-if="percentage<100">Загружаю файл....</span>
                        <span v-else>Файл загружен</span> <v-icon  v-if="percentage==100"
                        large
                        class="ml-2"
                        color="success"                     >
                     mdi-check-bold
                    </v-icon>
                    <v-progress-linear
                    v-model="percentage"                    
                    height="25">
                     <strong :style="percentage>=50?'color:white':''">{{ Math.ceil(percentage) }}%</strong>
                    </v-progress-linear>
                    <br>
                    <span v-show="percentage==100">Обработка файла</span>
                  
                       <v-progress-linear
                    v-model="workprogress"                    
                    height="25">
                     <strong :style="workprogress>=50?'color:white':''">{{ Math.ceil(workprogress) }}%</strong>
                    </v-progress-linear>
                   <br>
                    <div v-show="actions.opening.value">
                    <span>{{actions.opening.text}}</span> 
                        <v-icon v-if="actions.columnwork.value"
                             large
                             class="ml-2"
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else large class="ml-2" color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-show="actions.columnwork.value">                    
                        <span>{{actions.columnwork.text}}</span>
                        <v-icon v-if="actions.rowwork.value"
                            class="ml-2"
                             large
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else class="ml-2" large color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-show="actions.rowwork.value">
                    <span >{{actions.rowwork.text}}. Строка  {{actions.rowwork.value}} {{actions.totalrows.text}} {{actions.totalrows.value}}
                    </span>
                    <v-icon v-if="actions.basewrighting.value"
                             large
                             class="ml-2"
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else class="ml-2" large color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-show="actions.justific.value">
                    <span>{{actions.justific.text}} {{actions.justific.value}}</span>
                  
                    </div>
                    <div v-if="actions.error.value">
                    <span>{{actions.error.text}} {{actions.error.value}}</span>
                    <v-icon large class="ml-2" color="error"> mdi-alert</v-icon>
                    </div>
                    <div  v-show="actions.basewrighting.value">
                    <span>{{actions.basewrighting.text}}</span>
                    <v-icon v-if="actions.completedshow.value"
                             large
                             class="ml-2"
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else large class="ml-2" color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-if="actions.completedshow.value && !actions.error.value">
                    <span>{{actions.completed.text}} {{actions.completed.value}}  </span>
                    <v-icon large class="ml-2" color="success">  mdi-check-bold</v-icon>
           
                    </div>
                    <div v-else-if="actions.completedshow.value && actions.error.value" >
                    <span >Произошла ошибка. Строк загружено:{{actions.completed.value}}  </span>
                   
                    <v-icon large class="ml-2" color="error"> mdi-alert</v-icon>
                    </div>
                    <v-spacer></v-spacer>
                        
                    </v-card-text>
                       <v-card-actions>
                           <v-btn v-show="actions.completedshow.value" color="primary"  @click="overlayoffer()"
                            >Закрыть</v-btn
                        >
                            </v-card-actions>
                </v-card>
               
               
            </v-overlay>
    </v-col>
</v-row>
           
        </template>
    </fills-and-statistics>
    <!-- <v-row class="flex-grow-0 header_sait">
    <v-col >
        <h1 class="pl-2 thebiggest"> ЗАЛИВКИ И СТАТИСТИКА

        </h1>
        </v-col>
    </v-row>

    <v-row class="strokarov px-3 flex-grow-0">

<v-col                 
    class=" fix_h_eye flex-col"
    lg=2
    md=6
    sm=12>
                <v-card class="flex-grow-1  flex-col">
                <v-row class="flex-grow-0  ma-0">
                    <v-col class="pa-0 ">
                        <v-divider ></v-divider>
                        <h1 class="title-load title_eye py-3">На входе</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>
            <v-row class="flex-grow-0 ma-0 pt-3">
                <v-col class="pa-0 ">
                    <h1 class="title_tvo "> Сейчас онлайн на входе: {{useronline.anonymousnow.length}}<br></h1>
                </v-col>
            </v-row>
                <v-row class=" ma-0 eye">
                    <v-col class="flex-col pa-0">
                        <v-data-table
                        :fixed-header="true"
                            disable-pagination
                            :headers="anonymousheaders"
                            :items="useronline.anonymousnow"
                            dense
                            hide-default-footer
                            class="elevation-1 flex-grow-1"
                        >
                        <template v-slot:[`item.entered`]="{ item }">
                            {{datebuild(item.entered)}}
                        </template>                  
                        </v-data-table>
                    </v-col>
                </v-row>
            </v-card>
</v-col>

<v-col                
    class="fix_h_eye flex-col"
    lg=2
    md=6
    sm=12>
                 <v-card class="flex-grow-1 flex-col">
                <v-row class="flex-grow-0  ma-0">
                    <v-col class="pa-0">
                        <v-divider></v-divider>
                        <h1 class="title-load py-3">В системе <br> всего {{calcmoment(summer(total.loggednow))}}</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>
            <v-row class="flex-grow-0 ma-0 pt-3">
                <v-col class="pa-0 ">
                    <h1 class="title_tvo ">Сейчас онлайн в системе: {{useronline.loggednow.length}}<br> </h1>
                </v-col>
            </v-row>
                <v-row class=" ma-0 eye">
                    <v-col class="flex-col pa-0">
                          <v-data-table
                :headers="loggednowheaders"
                :items="useronline.loggednow"
                dense
                sort-by="sn"
                group-by="region"
                hide-default-footer
                disable-pagination
                :fixed-header="true"
                 class="elevation-1 flex-grow-1 "
                    >
                    <template v-slot:[`group.header`]="{items, isOpen, toggle}">
        <th colspan="1">
          <v-icon @click="toggle"
            >{{ isOpen ? 'mdi-minus' : 'mdi-plus' }}
          </v-icon>
          {{ items[0].region=='null'?'Нет': items[0].region }}
        </th>
        <th>{{ calcmoment(total.loggednow[items[0].region]) }}   </th>
      </template>
                    <template v-slot:[`item.entered`]="{ item }">
                    {{datebuild(item.entered)}}
                    </template>                  
                    
                    
                    
                    </v-data-table>     
                    </v-col>
                </v-row>
            </v-card>
</v-col>

<v-col
    class="fix_h_eye flex-col"
    lg=4
    md=6
    sm=12>
                   <v-card class="flex-grow-1 flex-col">
                <v-row class="flex-grow-0  ma-0">
                    <v-col class="pa-0">
                        <v-divider></v-divider>
                        <h1 class="title-load py-3">За неделю онлайн зарегистрированные провели на сайте:<br> {{calcmoment(summer(total.logged_outed))}}</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>
                <v-row class="ma-0 eye">
                    <v-col class="flex-col pa-0">
                         <v-data-table
                         disable-pagination
                :headers="outedheaders"
                :items="useronline.logged_outed"
                dense
                sort-by="sn"
                group-by="region"
                :fixed-header="true"
                hide-default-footer
                
                
                 class="elevation-1 flex-grow-1"
                    >
                     <template v-slot:[`group.header`]="{items, isOpen, toggle}">
        <th colspan="2">
          <v-icon @click="toggle"
            >{{ isOpen ? 'mdi-minus' : 'mdi-plus' }}
          </v-icon>
          {{ items[0].region=='null'?'Нет': items[0].region }}
        </th>
        <th>{{ calcmoment(total.logged_outed[items[0].region]) }}   </th>
      </template>
                    <template v-slot:[`item.entered`]="{ item }">
                    {{datebuild(item.entered)}}
                    </template>   
                    <template v-slot:[`item.outed`]="{ item }">
                    {{item.outed-item.entered}}
                    </template>                  
                    
                    
                    
                    </v-data-table>
                    </v-col>
                </v-row>
            </v-card>
</v-col>

<v-col                 
    class="fix_h_eye flex-col"
    lg=4
    md=6
    sm=12>
                   <v-card class="flex-grow-1  flex-col">
                <v-row class="flex-grow-0  ma-0">
                    <v-col class="pa-0">
                        <v-divider></v-divider>
                        <h1 class="title-load py-3 px-3">За неделю онлайн по регионам:</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>

                <v-row class=" ma-0 eye">
                    <v-col class="flex-col pa-0">
                       <v-data-table
                :headers="loggedregionhead"
                :items="loggedregiontotal"
                dense
                sort-desc
                sort-by="onsite"
                hide-default-footer
                disable-pagination
                :fixed-header="true"
                 class="elevation-1 flex-grow-1"
                    >
      
                    <template v-slot:[`item.onsite`]="{ item }">
                    {{calcmoment(item.onsite)}}
                    </template>                  
                    
                    
                    </v-data-table>
                    </v-col>
                </v-row>
            </v-card>
</v-col>

            <v-col
                class="fix_h_eye flex-col"
                lg=4
                md=6
                sm=12
            >   
            <v-card class="flex-grow-1 flex-col">
                <v-row class="flex-grow-0 ma-0 oneblock">
                    <v-col class="flex-grow-0 pb-0"
                        lg=1
                        md=1
                        sm=1
                    >
                         <v-tooltip
                                    v-if="helper.length"
                                    color="primary"
                                    right
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn
                                        class="indicator "
                                            v-bind="attrs"
                                            v-on="on"
                                            fab
                                            dark
                                            
                                            :color="colorbutton"
                                        >   
                                        </v-btn>
                                    </template>
                                    <span>{{helper}}</span>
                                </v-tooltip>
                    </v-col>
                    <v-col 
                    class="pa-0"
                    lg=10
                    md=10
                    sm=10
                    >
                  
                        <h1 class="title-load py-3">Заливка</h1>
               
                    </v-col>
                </v-row>
                <v-row class="flex-grow-0 ma-0 pt-3">
                    <v-col class="pa-0">
                        <h1 class="title_tvo ">========== Если ФБ1 - лист называем ФБ1 ==========</h1>
                         <h1 class="title_tvo ">====== Если ЕНС - лист называем ЕНС ======</h1>
                    </v-col>
                </v-row>
                <v-row class="ma-0 px-15">
                    <v-col 
                    class="align-self-center flex-col pa-0"
                    >
                        <v-file-input
                            label="Загрузите файл"
                            ref="fileinput"
                            outlined
                            dense
                            v-model="fileFB1"
                            class="pt-7"
                        ></v-file-input>     
                    </v-col>

                </v-row>
                <v-row class="flex-grow-0 ma-0">
                    <v-col class="flex-col pa-0 pb-3">
                        <v-btn
                        class="submit-button  align-self-center"

                            @click="sendFB1"
                            >
                            Отправить
                        </v-btn>
                    </v-col>
                </v-row>

            </v-card>
        </v-col>
        
      
        <v-col
            class="fix_h flex-col"
            lg=4
            md=6
            sm=12
        >
        <v-card class="flex-grow-1 flex-col">
           <v-row class="flex-grow-0 ">
                <v-col>
                    <v-divider></v-divider>
                    <h1 class="title-load py-3">Удаление загрузок</h1>
                    <v-divider></v-divider>
                </v-col>
            </v-row>
               <v-row class="ma-0 px-14 mt-2">
                <v-col class="pa-0">
                    <v-select
                    :class="'pt-0'"
                                v-model="razdel"
                                label="Подраздел"
                                :items="['ФБ1', 'ЕНС']"
                                solo
                                dense
                                ></v-select>
                                </v-col>
            </v-row>
            <v-row class="flex-grow-0 ma-0 pt-3">
                <v-col class="pa-0">
                    <h1 class="title_tvo ">Дата выгрузки</h1>
                </v-col>
            </v-row>
            <v-row class="ma-0 px-14">
                <v-col class=" align-self-center flex-col pa-0">

                    <f-multi-select
                        :class="'pt-0'"
                        :field="razdel=='ФБ1'?'date_unloading':'date_unloading__ens'"
                    ></f-multi-select>  
                
                </v-col>
            </v-row>
            <v-row class="flex-grow-0 ma-0">
                <v-col class="flex-col  pa-0 pb-3">
                    <v-btn
                        class="submit-button  align-self-center"
                        color="error"
                        @click="delloadslayer"
                    >
                        Удалить
                    </v-btn>
                </v-col>
            </v-row>
           
            </v-card>
        </v-col>
       
        <v-col
            class="fix_h flex-col"
            lg=4
            md=6
            sm=12
        >
            <v-card class="flex-grow-1 flex-col">
                <v-row class="flex-grow-0 ">
                    <v-col>
                        <v-divider></v-divider>
                        <h1 class="title-load py-3">Информер</h1>
                        <v-divider></v-divider>
                    </v-col>
                </v-row>

                <v-row >
                    <v-col class="flex-col">
                        <v-img   
                            class="align-self-center"
                            contain         
                            style="width: 40vw; max-height:16vh; min-height:16vh"                 
                            :src= buratino()
                        ></v-img>
                    </v-col>
                </v-row>
                <v-row class="flex-grow-0 ma-0">
                    <v-col class="flex-col pa-0 pb-3">
                        <v-btn 
                            class="btninf"
                            href="/media/informer/informer.exe"
                            download         
                        >
                            Скачать
                        </v-btn>
                        
                    </v-col>
                </v-row>
            </v-card>
        </v-col>
 
        <v-col
            class="flex-grow-0 flex-col"
            lg=8
            md=12
            sm=12
        >
        <v-card class="flex-grow-1 flex-row ">
            <v-col
                        lg=6
            md=12
            sm=12
            class="py-0 right_files"
            >
                <v-row class="flex-grow-0">
                <v-col>
                    <h1 class="title-load py-2 pb-3">Загрузка динамики</h1>
                    <v-divider></v-divider>
                </v-col>
            </v-row>
            <v-row class="flex-grow-0">
                <v-col
                    class="flex-row pikkalendar pt-0 justify-center"
                >
                    <v-menu 
                        v-model="datefilter"
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
                            :title="'Выберите дату для файлов'"   
                            class="align-self-center pr-3"   
                        />
                            <v-text-field
                                :value="formatDate(date_unloading)"              
                                type="date-local"              
                                placeholder="дд.мм.гггг"
                                solo
                                @input="oninputnotFilter"
                                v-bind="attrs"
                                hide-details
                                v-on="on"
                                class="pt-0 datewitxh"
                                title="Дата для файлов"
                            >
                            </v-text-field>
                        </template>
                        <v-date-picker
                            :first-day-of-week="1"
                            event-color="green lighten-1"
                            v-model="date_unloading"
                        >
                        </v-date-picker>
                    </v-menu>
                </v-col>
            </v-row>
            <v-row class="flex-grow-0 ma-0">
                <v-col id="file-drag-drop">
                    <form class="formfile" ref="fileform">
                        <span class="drop-files">Перетащите файлы сюда</span>
                    </form>
                </v-col>
            </v-row>
            <v-row class="flex-grow-0 ma-0 mb-2">
                <v-col class="pa-0">
                    <progress
                        class="my-0" max="100"
                        :value.prop="uploadPercentage"
                    >
                    </progress>
                </v-col>
            </v-row>
            <v-row class="ma-0">
                <v-col
                    class="pa-0 flex-col "            
                >

                <v-btn 
                    class="submit-button align-self-center"
                    
                    v-on:click="submitFiles()"  
                    :disabled="!files.length"   
                >
                            Отправить
                        </v-btn>


                </v-col>
                <v-alert
                    v-if="resultmessage.length"
                    class="absoluten mx-auto"
                    prominent
                    :type="typemes"
                    >
        <v-row align="center" class="px-4">
            <v-col class="grow">
            {{resultmessage}}
            </v-col>
            <v-col class="shrink">
              
            <v-btn @click="closealert">Закрыть</v-btn>
            
            </v-col>
        </v-row>
    </v-alert>
            </v-row>
            </v-col>
 
            <v-col >
                <div class="pb-3 overflow-auto kl" v-if="files.length">
                    <v-row
                        v-for="(file, key) in files"
                        :key="key"
                        class="file-listing ma-0 "
                    >
                        <v-col class="flex-grow-0 align-self-center pr-2 pa-0">
                            <img
                                class="preview"
                                v-bind:ref="'preview'+parseInt( key )"
                            /> 
                        </v-col>
                        <v-col class="align-self-center pa-0">
                        {{ file.name }}
                        </v-col>
                        <v-col class="remove-container flex-grow-0 align-self-center px-4 pa-0 ">
                            <a class="remove" v-on:click="removeFile( key )">Удалить</a>
                        </v-col>
                    </v-row>
                </div>
                
                <div class="pb-3 overflow-auto kl d-flex flex-col justify-center mx-auto" v-else>
                    
                    <h2 class="align-self-center" style="color:#AFAFAF">
                    Ожидание файлов . . .
                    </h2>
                </div>
            </v-col>
        
        </v-card>
        </v-col>
       
        <v-col
            lg=4
            md=6
            sm=12
        >
        
        </v-col>



    </v-row>
    <v-overlay :value="delloadslay">
                <v-card
                elevation="2"                
                width="40vw"                
                light
                >
                <v-card-title>ВЫ УВЕРЕНЫ ЧТО ХОТИТЕ УДАЛИТЬ ВЫГРУЗКИ?</v-card-title>
                <v-card-text>Все записи будут удалены: {{filtertext}}</v-card-text>
                <v-spacer></v-spacer>
                <v-btn class="ma-2"
                color="success"
                @click="closelay"
                
                >Отказаться</v-btn>
                
                
                <v-btn
                class="ma-2"
                color="error"
                @click="delloads"
                >Подтвердить
                </v-btn>
                </v-card>
        </v-overlay>
      
            <v-overlay :value="overlay">
                <v-card
                elevation="2"                
                width="40vw"                
                light
                >
                   <v-card-title class="justify-space-between">
                    <div class="d-flex">ЗАГРУЗКА И ОБРАБОТКА ФАЙЛА</div>
                  
    <v-tooltip v-if="helper.length"
                                         color="primary"
                                          left>
                                        <template v-slot:activator="{ on, attrs }">
        

                                       <v-btn
                                        style="height:1.3em; width:1.3em"
                                          v-bind="attrs"
                                        v-on="on"
                                        fab
                                        dark
                                        small
                                        :color="colorbutton"
                        >   
                        </v-btn>
                                    </template>
                                    <span>{{helper}}</span>
                                    </v-tooltip>


                   </v-card-title>
                    <v-card-text>
                        <span v-if="percentage<100">Загружаю файл....</span>
                        <span v-else>Файл загружен</span> <v-icon  v-if="percentage==100"
                        large
                        class="ml-2"
                        color="success"                     >
                     mdi-check-bold
                    </v-icon>
                    <v-progress-linear
                    v-model="percentage"                    
                    height="25">
                     <strong :style="percentage>=50?'color:white':''">{{ Math.ceil(percentage) }}%</strong>
                    </v-progress-linear>
                    <br>
                    <span v-show="percentage==100">Обработка файла</span>
                  
                       <v-progress-linear
                    v-model="workprogress"                    
                    height="25">
                     <strong :style="workprogress>=50?'color:white':''">{{ Math.ceil(workprogress) }}%</strong>
                    </v-progress-linear>
                   <br>
                    <div v-show="actions.opening.value">
                    <span>{{actions.opening.text}}</span> 
                        <v-icon v-if="actions.columnwork.value"
                             large
                             class="ml-2"
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else large class="ml-2" color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-show="actions.columnwork.value">                    
                        <span>{{actions.columnwork.text}}</span>
                        <v-icon v-if="actions.rowwork.value"
                            class="ml-2"
                             large
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else class="ml-2" large color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-show="actions.rowwork.value">
                    <span >{{actions.rowwork.text}}. Строка  {{actions.rowwork.value}} {{actions.totalrows.text}} {{actions.totalrows.value}}
                    </span>
                    <v-icon v-if="actions.basewrighting.value"
                             large
                             class="ml-2"
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else class="ml-2" large color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-show="actions.justific.value">
                    <span>{{actions.justific.text}} {{actions.justific.value}}</span>
                  
                    </div>
                    <div v-if="actions.error.value">
                    <span>{{actions.error.text}} {{actions.error.value}}</span>
                    <v-icon large class="ml-2" color="error"> mdi-alert</v-icon>
                    </div>
                    <div  v-show="actions.basewrighting.value">
                    <span>{{actions.basewrighting.text}}</span>
                    <v-icon v-if="actions.completedshow.value"
                             large
                             class="ml-2"
                                color="success"                     >
                            mdi-check-bold
                        </v-icon>
                        <v-icon v-else large class="ml-2" color="primary">mdi-timer-sand</v-icon>
                    </div>
                    <div v-if="actions.completedshow.value && !actions.error.value">
                    <span>{{actions.completed.text}} {{actions.completed.value}}  </span>
                    <v-icon large class="ml-2" color="success">  mdi-check-bold</v-icon>
           
                    </div>
                    <div v-else-if="actions.completedshow.value && actions.error.value" >
                    <span >Произошла ошибка. Строк загружено:{{actions.completed.value}}  </span>
                   
                    <v-icon large class="ml-2" color="error"> mdi-alert</v-icon>
                    </div>
                    <v-spacer></v-spacer>
                        
                    </v-card-text>
                       <v-card-actions>
                           <v-btn v-show="actions.completedshow.value" color="primary"  @click="overlayoffer()"
                            >Закрыть</v-btn
                        >
                            </v-card-actions>
                </v-card>
               
               
            </v-overlay> -->


    </v-container>







</template>

<script>

import { createNamespacedHelpers } from "vuex";
import {baseURL, baseWS} from "@/utils/axios-api"
import DateCalSelect from '../components/UI/DateCalSelect.vue';
import  datepickerf  from "@/utils/datepickerf.js"
import moment from 'moment';
import { clearAxios } from '@/utils/axios-api'
import fillsAndStatistics from '@/views/UI/fills-and-statistics.vue';
import Statistic from './UI/statistic.vue';
import Stattab from './UI/stattab.vue';
const { mapMutations, mapActions } = createNamespacedHelpers("filterslogic");

export default {
  components: { fillsAndStatistics,
  Statistic,
    Stattab },
    name: "LoadFile",
    mixins:[datepickerf],
    data() {
        return {
           
            razdelselect:["ФБ1","ЕНС"],
            razdel:"ФБ1",
            loggedregionhead:[
                {text:"Регион",value:"region"},
                {text:"Провели",value:"onsite"}

            ],
            loggedregiontotal:[],
            total:{     anonymousnow:0,
                        anonymous_outed:0,
                        loggednow:{},
                        logged_outed:{}},
            anonymousheaders:[
                 {text:"IP",value:"ip"},
                {text:"Зашел",value:"entered"},
            ],
            anonymousoutedheaders:[
                 {text:"IP",value:"ip"},
                {text:"Зашел",value:"entered"},
                {text:"Пробыл (сек)",value:"outed"}
            ],

            outedheaders:[
                 {text:"Регион",value:"region"},
                {text:"Фамилия",value:"sn"},
                {text:"Зашел",value:"entered"},
                {text:"Пробыл (сек)",value:"outed"}
                ],
           
            useronline:{anonymousnow:[],
                        anonymous_outed:[],
                        loggednow:[],
                        logged_outed:[]},

            loggednowheaders:[
            {text:"Регион",value:"region"},
            {text:"Фамилия",value:"sn"},
            {text:"Зашел",value:"entered"},
            ],



            typemes:"success",
            resultmessage:"",
            datefilter:"",
            date_unloading:"",
             date_unloading__ens:"",
            helper: "Красный - соединения нет и заливка не пройдет. Желтый - установка соединения. Зеленый - все хорошо",
            colorbutton: 'yellow',
            actions:{justific:{text:"Согласованное исключение", value:0},
                    rowwork:{text:"Обрабатываю строки",value:0},
                    totalrows:{text:"из",value:0},
                    columnwork:{text:"Обрабатываю колонки",value:0},
                    opening:{text:"Открываю файл",value:0},
                    error:{text:"Ошибка",value:0},
                    basewrighting:{text:"Отправляю данные в базу",value:0},
                    completed:{text:"Загрузка завершена. Строк добавлено:",value:0},
                    completedshow:{value:0}

            },
            
            dynamicfilter: {},
            ws: "",
            wspy:'',
            selectDict: '',
            snackbar: false,
            textSnack: '',
            dictItems: [
                { text: "Регион", value: "regions" },
                { text: "Паспорта", value: "passports" },
            ],
            fileForDict: null,
            fileFB1: null,
            filePassport: null,
            overlay: false,
            delloadslay:false,
            filtertext:"",
            uploadtype:"",
            percentage:0,
            workprogress:0,

            dragAndDropCapable: false,
            files: [],
            uploadPercentage: 0


        };
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
        determineDragAndDropCapable(){
        var div = document.createElement('div');
        return ( ( 'draggable' in div )
                || ( 'ondragstart' in div && 'ondrop' in div ) )
                && 'FormData' in window
                && 'FileReader' in window;
      },
      getImagePreviews(){
        for( let i = 0; i < this.files.length; i++ ){
          if ( /\.(jpe?g|png|gif)$/i.test( this.files[i].name ) ) {
            let reader = new FileReader();
            reader.addEventListener("load", function(){
              this.$refs['preview'+parseInt( i )][0].src = reader.result;
            }.bind(this), false);
            reader.readAsDataURL( this.files[i] );
          } else {
            this.$nextTick(function(){
              this.$refs['preview'+parseInt( i )][0].src = baseURL+'media/uploads/grut_ais.png';
            });
          }
        }
      },
      submitFiles(){
      
        if ( (!(moment(this.date_unloading, "YYYY-MM-DD").isValid()))||(this.date_unloading.length<10)){
             this.resultmessage="Проверьте дату загрузки. Явно что-то не то"
             this.typemes="error"
        }
        else{
       
        let formData = new FormData();
        for( var i = 0; i < this.files.length; i++ ){
        
          formData.append('files[]',this.files[i]);
        }
        formData.append("date_unloading", this.date_unloading)
        this.$http.post( '/api/statistic/dynamics/list/',
          formData,
          {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: function( progressEvent ) {
              this.uploadPercentage = parseInt( Math.round( ( progressEvent.loaded * 100 ) / progressEvent.total ) );
            }.bind(this)
          }
        ).then((resp)=>{
            
          this.resultmessage=resp.data.mess;
          this.typemes="success"
        })
        .catch(function(){
          this.resultmessage="Произошла ошибка"
          this.typemes="error"
        });
        }
      },
      removeFile( key ){
        this.files.splice( key, 1 );
      },
        datebuild(it){
         
        return moment.unix(it).format("HH:mm:ss DD.MM.YYYY")
        },


        buratino(){            
            return baseURL+'media/uploads/12.png'
        },
        
        async delloads(){
            
            let filters = await this.activefilters()
         
            const res = await this.$http.post(`/api/statistic/load/`, {
                    params: {
                        filters: JSON.stringify({
                            ...filters,                          
                        }),}}).then(()=>{
                     this.getFilters({
            listFB1: [{ name: "date_unloading", sort: "-" }],
            ens:[{ name: "date_unloading__ens", sort: "-", related_name:'date_unloading' }]           
        }).then(
            
            async (data) => { }) })
                                this.closelay()
                             this.setFields({
            date_unloading: {
                module: "mult",
                correct: (arr) => {   
                    let narr=[]             
                    arr.map((el) => {narr.push(this.$changeFormatDateReverse(el))})                    
                    return narr}
            },
            date_unloading__ens:{
                module: "mult",
                 correct: (arr) => {   
                    let narr=[]             
                    arr.map((el) => {narr.push(this.$changeFormatDateReverse(el))})                    
                    return narr},
            }
            },           
        );
       
        
        
        },
        calcmoment(timestamp){
           let hours = Math.floor(timestamp / 60 / 60);
           let minutes = Math.floor(timestamp / 60) - (hours * 60);
           let seconds = timestamp % 60 ; 
           let formatted = [
                hours.toString().padStart(2, '0')+"ч",
                minutes.toString().padStart(2, '0')+"м",
                seconds.toString().padStart(2, '0')+ "с"
                ].join(' ');
	        return formatted
        },
        summer(obj){
            let s=0
            for (let val of Object.values(obj)){
                s+=val
            }
            return s
        },

        closealert(){
            if (this.resultmessage!="Проверьте дату загрузки. Явно что-то не то"){
                this.files=[]
            }
            this.resultmessage=""
            this.uploadPercentage=0
            
        },

        async closelay(){
            this.clear()
            this.filtertext=""
            this.delloadslay=false
            

        }, 
        async delloadslayer(){
            let field=this.razdel=='ФБ1'?'date_unloading__in':'date_unloading__ens__in'
            const filters = await this.activefilters()
            if ((filters[field])&&(filters[field].length>0)){
                this.delloadslay=true
                this.filtertext = filters[field].map((e)=>{return this.$changeFormatDate(e)}).join(", ")
            }
            else{this.delloadslay=false
            this.filtertext=""
            }
        },

        overlayoffer(){
            this.workprogress =0            
            this.$refs.fileinput.reset();
            for(let [key,val] of Object.entries(this.actions)){
                val.value=0
            }
              
              this.setFields({
                    date_unloading: {
                        module: "mult",
                        correct: (arr) => {   
                            let narr=[]             
                            arr.map((el) => {narr.push(this.$changeFormatDateReverse(el))})                    
                            return narr},
                        
                    }, 
                      date_unloading__ens:{
                module: "mult",
                 correct: (arr) => {   
                    let narr=[]             
                    arr.map((el) => {narr.push(this.$changeFormatDateReverse(el))})                    
                    return narr},
            }          
                });
                this.getFilters({
                    listFB1: [{ name: "date_unloading", sort: "-" }],   
                     ens:[{ name: "date_unloading__ens", sort: "-", related_name:'date_unloading' }],           
                }).then(async (data) => { })
          
            this.overlay=false
            
        },
        sendFB1() {
            this.send({attr: 'FB1', file: this.fileFB1})            
        },
        sendDict() {

            this.send({attr: this.selectDict, file: this.fileForDict})
        },
        sendPassport() {
            this.send({attr: 'passport', file: this.filePassport})
        },
        wsrecieve(data){

        },
        send(data) {

            const sdata = new FormData();

            for (let [key, val] of Object.entries(data)) {
                sdata.append(key, val);
            }
            this.overlay =true;          
           
            


                // Отправить можем только строку
            this.uploadtype = "Загружаю файл"
            this.percentage =0  
            this.closelay  ()
            let sendik= new Promise((resolve, reject) => {

                this.$http.put("/api/statistic/load/", sdata, 
        { onUploadProgress: function( progressEvent ) {        
        this.percentage = parseInt( Math.round( ( progressEvent.loaded / progressEvent.total ) * 100 ) );
      }.bind(this)}).then((res) => {     
                             
                    this.ws.send(JSON.stringify(res.data))
                    // if (res.data['msg']) {
                        
                    //     this.textSnack = res.data['msg'];
                    //     this.overlay =false;
                    //     this.snackbar= true;
                        
                    // } else {
                        
                    //     this.textSnack = 'Заливка прошла успешно';
                    //     this.overlay =false;
                    //     this.snackbar= true;
                    //     resolve(res);
                        
                    // }
                    
                    
                }).catch((error) => {
                    this.overlay =false;

                    alert(error);
                    reject(error)
                })
                
                
            })
            
        }

    },
    async mounted() {  
    moment.locale('ru') 
    this.date_unloading = moment().format("YYYY-MM-DD")
     this.dragAndDropCapable = this.determineDragAndDropCapable();
    
        const ip = await clearAxios.get("/api/contacts/ipgetter/")       
        // this.ws= new WebSocket(baseWS+`ws/spy/logged/?token=${localStorage.getItem('access')}?ip=${ip.data.ip}`)
        this.wspy= new WebSocket(baseWS+`ws/spy/watcher/?ip=${ip}`)
        // this.$store.commit("initializeStore");
       
          this.wspy.onmessage=(e) =>{
            let data = JSON.parse(e.data)
            this.useronline = data.message.data
           
            for (let [key,val] of Object.entries(this.total)){
                
                if (['logged_outed','loggednow'].includes(key)){
                    
                    this.total[key]={}
                }


            }
            for (let [key,val] of Object.entries(this.useronline)){
                if (['logged_outed','loggednow'].includes(key)){
                    
                for (let i in val){ 

                    let time = key=='loggednow'? Math.round(Date.now()/1000):val[i]['outed']
                if (val[i]['region'] in this.total[key]) 
                    {                        
                        this.total[key][val[i]['region']]+=time-val[i]['entered']
                        
                    }
                        else{  this.total[key][val[i]['region']]=time-val[i]['entered']
                        }
                }
            }
            }
            this.loggedregiontotal=[]
            for (let [key,val] of Object.entries(this.total.logged_outed)){
                this.loggedregiontotal.push({'region':key=="null"?"Нет":key,"onsite":val})
            }
            // console.log(`this.useronline`, this.useronline);
        //   console.log(this.total);
          }
          this.wspy.onopen=(e)=>{
                  
          }
        //   this.wspy.onclose=(e)=>{this.colorbutton = 'red'}



       this.ws= new WebSocket(baseWS+`ws/loader/`)
        this.$store.commit("initializeStore");
       
          this.ws.onmessage=(e) =>{
             let data = JSON.parse(e.data)
           
            for (let [key,val] of Object.entries(data)){
                this.actions[key].value=val
            }
            if(this.actions.totalrows.value && this.actions.rowwork.value){
                this.workprogress = this.actions.rowwork.value*100/this.actions.totalrows.value
            }
          
          }
          this.ws.onopen=(e)=>{this.colorbutton = 'green'           
          }
          this.ws.onclose=(e)=>{this.colorbutton = 'red'}


         this.getFilters({
            listFB1: [{ name: "date_unloading", sort: "-" }],
            ens:[{ name: "date_unloading__ens", sort: "-", related_name:'date_unloading' }],           
        }).then(async (data) => { })    




        this.setFields({
            date_unloading: {
                module: "mult",
                correct: (arr) => {   
                    let narr=[]             
                    arr.map((el) => {narr.push(this.$changeFormatDateReverse(el))})                    
                    return narr},
            },           
            date_unloading__ens:{
                module: "mult",
                 correct: (arr) => {   
                    let narr=[]             
                    arr.map((el) => {narr.push(this.$changeFormatDateReverse(el))})                    
                    return narr},
            }
        });
        
      if( this.dragAndDropCapable ){        
        ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach( function( evt ) {
          this.$refs.fileform.addEventListener(evt, function(e){
            e.preventDefault();
            e.stopPropagation();
          }.bind(this), false);
        }.bind(this));
        this.$refs.fileform.addEventListener('drop', function(e){
          for( let i = 0; i < e.dataTransfer.files.length; i++ ){
            this.files.push( e.dataTransfer.files[i] );
            this.getImagePreviews();
          }
        }.bind(this));
      }
   
            
           
    // }
    },

    beforeDestroy(){
         this.$store.commit('picindx', 0)
    }
   
};
</script>

<style lang="scss">
@import "@/utils/colors.scss";

#file-drag-drop form{
    display: block;
    height: 100px;
    width: 100%;
    background: $bg-maincont;
    margin: auto;
    margin-top: 0px;
    text-align: center;
    line-height: 100px;
    border-radius: 4px;
  }

  
  div.file-listing{
    width: 100%;
    // margin: auto;
    padding: 5px;
    border-bottom: 1px solid #ddd;
  }
  div.file-listing img{
    height: 25px;
  }

  div.remove-container a{
    color: red;
    cursor: pointer;
  }

  progress{
    width: 400px;
    margin: auto;
    display: block;
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .absoluten{
    position: absolute;
    bottom: 25px;
    margin-left: auto;
    margin-right: auto;
    left: 25%;
    right: 25%;
    text-align: center;
    z-index: 2;
  }


.fix_h {
    min-height: 300px;
}
.fix_h_eye {
     height: 400px;
   
}

.eye {
    height: 35px;
    overflow-y: auto;
}

// .title_eye {
//     min-height: 50px;
// }

.overauto {
    min-height: 100vh;
    overflow-x: auto;
}

.header_sait {
    max-height: 4.8vh;
    background: white;
    min-height: 42px;
}


.thebiggest {
    color: $bg-purple;
    font-size: 1.5rem !important;
}

.title_tvo {
    font-size: 0.85rem !important;
    color: $gray;
    text-align: center;
}

.title-load {
    font-size: 1rem !important;
    color: $bg-purple;
    text-align: center;
}



.pikkalendar 
    .v-text-field.v-text-field--solo .v-input__control {
        min-height: 30px!important;
        padding: 0;

}

.formfile 
{
    height: 85px;
    
    line-height: 90px;
}

.kl {
    height: 260px;
   
}

.strokarov {
    min-width: 450px;
}

.datewitxh {
    max-width: 12em;
}

.c1 {
background: $bg-newsbg;
}
.btninf, .submit-button{
    display: block;
    margin: auto;
    text-align: center;
    width: 200px;
    padding: 10px;
    text-transform: uppercase;
    background-color: $bg-purple!important;
    color: white!important;
    font-weight: bold;
    margin-top: 20px;
    border-radius: 8px;
  }

.btninf  {
    display: flex;
}

.oneblock {
    border-bottom: 1px solid #ddd;
}

.right_files {
border-right: 1px solid #ddd;
}
.col-sm-12 .right_files {
border-bottom: 1px solid #ddd;
    padding-bottom: 15px!important;
}

progress {
    width: 100%;
}
.indicator {



    height: 20px!important;
    width: 20px!important;

}
</style>