<template>
    <form ref="form_passport">
        <div class="main-bg px-4 pb-3">
            <!-- Основное определение паспорта -->
            <v-card>
                <v-card-text>
                    <div class="d-flex align-center mb-3">
                        <div>
                            <h2 class="title-passport">ПАСПОРТ</h2>
                        </div>
                        <!-- Код -->
                        <div>
                            <input
                                type="text"
                                name="code"
                                :disabled="!superuser"
                                :class="[
                                    { shown: showForm||updateForm},
                                    'input-normal ml-2',
                                ]"
                                style="width: 7rem"
                                v-model="formData.code"
                            />
                        </div>
                        <!-- Имя -->
                        <div style="width: 100%">
                            <input
                                type="text"
                                name="name"
                                :disabled="!superuser"
                                v-model="formData.name"
                                :class="[
                                    { shown: showForm },
                                    superuser?'input-normal ml-2':'',
                                ]"
                                style="width: 50%"
                            />
                        </div>
                        <div v-if="updateForm">
                            <v-icon @click="backMain">mdi-close</v-icon>
                        </div>
                    </div>
                    <!-- Описание -->
                    <div class="d-flex flex-column mb-2">
                        <label for="description1">Описание:</label>
                        <input
                            type="text"
                            id="description1"
                            name="description"
                            v-model="formData.description"
                            :disabled="!superuser"
                            :class="[{ shown: showForm }, 
                              superuser?'input-normal':''
                            ]"
                        />
                    </div>
                    <!-- Код и наименование технологического процесса -->
                    <div class="d-flex flex-column">
                        <label for="description2"
                            >Код и наименование технологического
                            процесса:</label
                        >
                        <input
                            name="code_name_process"
                            v-model="formData.code_name_process"
                            type="text"
                            id="description2"
                            :disabled="!superuser"
                            :class="[{ shown: showForm }, superuser?'input-normal':'']"
                        />
                    </div>
                </v-card-text>
            </v-card>
            <!-- Описание ненормализованных данных -->
            <v-card class="mt-3">
                <v-card-title class="title-block bg-card justify-center">
                    <div>Описание ненормализованных данных</div>
                </v-card-title>
                <v-card-text class="bg-card">
                    <v-container>
                        <v-row>
                            <v-col cols="6"><strong>Наименование показателя</strong></v-col>
                            <v-col cols="6"><strong>Значение показателя</strong></v-col>
                        </v-row>
                        <!-- Ответственный за мониторинг и нормализацию данных -->
                        <v-row class="align-center">
                            <v-col cols="6"
                                >Ответственный за мониторинг и нормализацию
                                данных</v-col
                            >
                            <v-col cols="6">
                                <v-select
                                    name="responsible"
                                    v-model="formData.responsible"
                                    :items="multiData.responsible"
                                    dense
                                    :disabled="!superuser"
                                    :hide-details="true"
                                    class="custom"
                                ></v-select>
                            </v-col>
                        </v-row>
                        <!-- Подсистема АИС "Налог-3" или другое ПО -->
                        <v-row class="align-center">
                            <v-col cols="6"
                                >Подсистема АИС "Налог-3" или другое ПО</v-col
                            >
                            <v-col cols="6">
                                <!-- <fc-multi-select 
                                :items="multiData.sub_system" 
                                v-model="formData.sub_system"
                                attach
                                chips
                                >                               
                                </fc-multi-select> -->


                                <v-select
                                
                                 v-model="formData.sub_system"
                                :items="multiData.sub_system"
                                attach   
                                class="custom mh26"       
                                :disabled="!superuser"
                                multiple
                            ></v-select>

<!-- 


                                <v-select
                                    :items="multiData.sub_system"
                                    dense
                                    name="sub_system"
                                    v-model="formData.sub_system"
                                    :hide-details="true"
                                    class="custom"
                                ></v-select> -->
                            </v-col>
                        </v-row>
                        <!-- Критичность -->
                        <v-row class="align-center">
                            <v-col cols="6">Критичность</v-col>
                            <v-col cols="6">
                                <v-select
                                    :items="multiData.criticality"
                                    dense
                                    :disabled="!superuser"
                                    name="criticality"
                                    v-model="formData.criticality"
                                    :hide-details="true"
                                    class="custom"
                                ></v-select>
                            </v-col>
                        </v-row>
                        <!-- Приоритет -->
                        <v-row class="align-center">
                            <v-col cols="6">Приоритет</v-col>
                            <v-col cols="6">
                                <v-select
                                    name="priority"
                                    v-model="formData.priority"
                                    :items="multiData.priority"
                                    dense
                                    :disabled="!superuser"
                                    :hide-details="true"
                                    class="custom"
                                ></v-select>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
            </v-card>
            <!-- Анализ ненормализованных данных -->
            <v-card class="mt-3">
                <v-card-title class="title-block justify-center bg-card">
                    <div>Анализ ненормализованных данных</div>
                </v-card-title>
                <v-card-text class="bg-card">
                    <v-container>
                        <v-row>
                            <v-col cols="6"><strong>Наименование показателя</strong></v-col>
                            <v-col cols="6"><strong>Значение показателя</strong></v-col>
                        </v-row>
                        <!-- Причина возникновения ненормализованных данных -->
                        <v-row>
                            <v-col cols="6"
                                >Причина возникновения ненормализованных
                                данных</v-col
                            >
                            <v-col cols="6">
                                <v-textarea
                                    name="reason_occurrence"
                                    outlined
                                    :readonly="!superuser"
                                    dense
                                    v-model="formData.reason_occurrence"
                                >
                                </v-textarea>
                            </v-col>
                        </v-row>
                        <!-- Способ выявления ненормализованных данных -->
                        <v-row>
                            <v-col cols="6"
                                >Способ выявления ненормализованных данных</v-col
                            >
                            <v-col cols="6">
                                <v-textarea
                                    name="detection_method"
                                    outlined
                                    :readonly="!superuser"
                                    dense
                                    v-model="formData.detection_method"
                                >
                                </v-textarea>
                            </v-col>
                        </v-row>
                        <!-- Вероятность возникновения новых ненормализованных данных -->
                        <v-row class="align-center">
                            <v-col cols="6"
                                >Вероятность возникновения новых ненормализованных данных</v-col
                            >
                            <v-col cols="6">
                                <v-select
                                    :items="['Да', 'Нет']"
                                    name="probability_of_occurrence"
                                    v-model="correctBoolean"
                                    dense
                                    :disabled="!superuser"
                                    class="custom"
                                    :hide-details="true"
                                    style="width: 6em"
                                ></v-select>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
            </v-card>
            <!-- Оценка масштаба ненормализованных данных в АИС "Налог-3" -->
            <v-card class="mt-3">
                <v-card-title class="title-block justify-center bg-card">
                    <div>
                        Оценка масштаба ненормализованных данных в АИС "Налог-3"
                    </div>
                </v-card-title>
                <v-card-text class="bg-card">
                    <v-container>
                        <v-row>
                            <v-col cols="6"><strong>Наименование показателя</strong></v-col>
                            <v-col cols="6"><strong>Значение показателя</strong></v-col>
                        </v-row>
                        <!-- Срок создания алгоритма отбора ненормализованных данных -->
                        <v-row>
                            <v-col cols="6"
                                >Срок создания алгоритма отбора ненормализованных данных</v-col
                            >
                            <v-col cols="6">
                                 <v-menu
                                    v-model="menu1"
                                    :disabled="!superuser"
                                    :close-on-content-click="false"
                                    :nudge-right="40"
                                    transition="scale-transition"
                                    offset-y
                                    min-width="auto"
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-text-field
                                            :value="formatDate(formData.algorithm_creation_period)"
                                            append-icon="mdi-calendar"
                                            dense
                                            class="custom"
                                            :disabled="!superuser"
                                            @focus="datakey='algorithm_creation_period'"
                                            @input="oninputs"                                            
                                            type="date-local"              
                                            placeholder="дд.мм.гггг"
                                            style="width: 10rem"
                                            :hide-details="true"
                                            v-bind="attrs"
                                            v-on="on"
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker
                                        v-model="formData.algorithm_creation_period"
                                        :disabled="!superuser"
                                        
                                        @input="menu1 = false"
                                    ></v-date-picker>
                                </v-menu>
                            </v-col>
                        </v-row>
                        <!-- Срок согласования отбора ненормализованных данных -->
                        <v-row>
                            <v-col cols="6"
                                >Срок согласования отбора ненормализованных данных</v-col
                            >
                            <v-col cols="6">
                                <v-menu
                                    v-model="menu2"
                                    :disabled="!superuser"
                                    :close-on-content-click="false"
                                    :nudge-right="40"
                                    transition="scale-transition"
                                    offset-y
                                    min-width="auto"
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-text-field
                                            :value="formatDate(formData.selection_aproval_period)"
                                            :disabled="!superuser"
                                            append-icon="mdi-calendar"
                                            dense
                                            @focus="datakey='selection_aproval_period'"
                                            @input="oninputs"
                                            class="custom"
                                            type="date-local"              
                                            placeholder="дд.мм.гггг"
                                            style="width: 10rem"
                                            :hide-details="true"
                                            v-bind="attrs"
                                            v-on="on"
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker
                                        v-model="formData.selection_aproval_period"
                                        :disabled="!superuser"
                                        @input="menu2 = false"
                                    ></v-date-picker>
                                </v-menu>
                            </v-col>
                        </v-row>
                        <!-- Дата формирования первоначального перечня ненормализованных данных -->
                        <v-row>
                            <v-col cols="6"
                                >Дата формирования первоначального перечня ненормализованных данных</v-col
                            >
                            <v-col cols="6">
                                <v-menu
                                    v-model="menu3"
                                    :disabled="!superuser"
                                    :close-on-content-click="false"
                                    :nudge-right="40"
                                    transition="scale-transition"
                                    offset-y
                                    min-width="auto"
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-text-field
                                            :value="formatDate(formData.date_of_formation_of_the_initial_list)"
                                            append-icon="mdi-calendar"
                                            :disabled="!superuser"
                                            dense
                                            @input="oninputs"
                                            class="custom"
                                            @focus="datakey='date_of_formation_of_the_initial_list'"
                                            type="date-local"              
                                            placeholder="дд.мм.гггг"
                                            style="width: 10rem"
                                            :hide-details="true"
                                            v-bind="attrs"
                                            v-on="on"
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker
                                        v-model="formData.date_of_formation_of_the_initial_list"
                                        :disabled="!superuser"
                                        :first-day-of-week="1"
                                        @input="menu3 = false"
                                    ></v-date-picker>
                                </v-menu>
                            </v-col>
                        </v-row>
                        <!-- Количество ненормализованных данных в первоначально сформированном перечне -->
                        <v-row>
                            <v-col cols="6"
                                >Количество ненормализованных данных в первоначально сформированном перечне</v-col
                            >
                            <v-col cols="6">
                                <input
                                    type="text"
                                    :disabled="!superuser"
                                    
                                    :class="[
                                        { shown: showForm },
                                        superuser?'input-normal':'',
                                    ]"
                                    style="width: 10rem"
                                    name="count_into_the_initial_list"
                                    v-model="
                                        formData.count_into_the_initial_list
                                    "
                                />
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
            </v-card>
            <!-- Алгоритм нормализации данных -->
            <v-card class="mt-3">
                <v-card-title class="title-block justify-center bg-card">
                    <div>Алгоритм нормализации данных</div>
                </v-card-title>
                <v-card-text class="bg-card">
                    <v-container>
                        <v-row>
                            <v-col cols="6"><strong>Наименование показателя</strong></v-col>
                            <v-col cols="6"><strong>Значение показателя</strong></v-col>
                        </v-row>
                        <!-- Описание алгоритма нормализации данных -->
                        <v-row>
                            <v-col cols="6"
                                >Описание алгоритма нормализации данных</v-col
                            >
                            <v-col cols="6">
                                <v-textarea
                                    outlined
                                    dense
                                    :readonly="!superuser"
                                    name="description_algorithm"
                                    v-model="formData.description_algorithm"
                                >
                                </v-textarea>
                            </v-col>
                        </v-row>
                        <!-- Необходимость получения дополнительных сведений из внешних источников -->
                        <v-row>
                            <v-col cols="6"
                                >Необходимость получения дополнительных сведений из внешних источников</v-col
                            >
                            <v-col cols="6">
                                <v-textarea
                                    :readonly="!superuser"
                                    outlined
                                    dense
                                    name="external_sources"
                                    v-model="formData.external_sources"
                                >
                                </v-textarea>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
            </v-card>
            <!-- Мероприятия по предотвращению новых ненормализованных данных -->
            <v-card class="mt-3">
                <v-card-title class="title-block justify-center bg-card">
                    <div>
                        Мероприятия по предотвращению новых ненормализованных данных
                    </div>
                </v-card-title>
                <v-card-text class="bg-card">
                    <v-container>
                        <v-row>
                            <v-col cols="6"><strong>Наименование показателя</strong></v-col>
                            <v-col cols="6"><strong>Значение показателя</strong></v-col>
                        </v-row>
                        <!-- Причины возникновения новых ненормализованных данных -->
                        <v-row>
                            <v-col cols="6"
                                >Причины возникновения новых ненормализованных данных</v-col
                            >
                            <v-col cols="6">
                                <input
                                    type="text"
                                    :class="[
                                        { shown: showForm },
                                        superuser?'input-normal':'',
                                    ]"
                                    :disabled="!superuser"
                                    style="width: 100%"
                                    name="reason_occurrence_new"
                                    v-model="formData.reason_occurrence_new"
                                />
                            </v-col>
                        </v-row>
                        <!-- Меры по исключению причин возникновения новых ненормализованных данных -->
                        <v-row>
                            <v-col cols="6"
                                >Меры по исключению причин возникновения новых ненормализованных данных</v-col
                            >
                            <v-col cols="6">
                                <input
                                :disabled="!superuser"
                                    type="text"
                                    :class="[
                                        { shown: showForm },
                                        superuser?'input-normal':'',
                                    ]"
                                    style="width: 100%"
                                    name="measures_to_eliminate_causes"
                                    v-model="
                                        formData.measures_to_eliminate_causes
                                    "
                                />
                            </v-col>
                        </v-row>
                        <!-- Номера заявок в СУТ -->
                        <v-row>
                            <v-col cols="6">Номера заявок в СУТ</v-col>
                            <v-col cols="6">
                                <input
                                    type="text"
                                    :class="[
                                        { shown: showForm },
                                        superuser?'input-normal':'',
                                    ]"
                                    :disabled="!superuser"
                                    style="width: 100%"
                                    name="application_numbers"
                                    v-model="formData.application_numbers"
                                />
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
            </v-card>

            <div class="d-flex align-center mt-2" v-if="superuser">
                <v-btn @click.prevent="submitPForm">Сохранить</v-btn>
                <div>
                    <v-file-input class="mt-n2" hide-input v-model="excel_file" @change="fillForm"
                        >Залить из Excel</v-file-input
                    >
                </div>
                
                
            </div>
        </div>
    </form>
</template>

<script>
import readXlsxFile from "read-excel-file";
import { DictPassport } from "@/utils/dicts";
import  datepickerf  from "@/utils/datepickerf.js"
import moment from "moment";
export default {
    name: "form-password",
    mixins:[datepickerf],
    props: {
        updateForm: {
            type: Boolean,
            default: false,
        },
        fillData: {
            type: Object,
        },
        multiData: {
            type: Object,
            default: () => ({}),
        }
    },
    data() {
        return {
            superuser: false,
            showForm: false,
            menu1: false,
            menu2: false,
            menu3: false,
            excel_file: null,
            responsible: [],
            sub_system: [],
            criticality: [],
            priority: [],
            datakey:null,
            formData: {
                code: "",
                name: "",
                description: "",
                code_name_process: "",
                responsible: "",
                sub_system: "",
                criticality: "",
                priority: "",
                reason_occurrence: "",
                detection_method: "",
                probability_of_occurrence: "",
                algorithm_creation_period: "",
                selection_aproval_period: "",
                date_of_formation_of_the_initial_list: "",
                count_into_the_initial_list: "",
                description_algorithm: "",
                external_sources: "",
                reason_occurrence_new: "",
                measures_to_eliminate_causes: "",
                application_numbers: "",
            },
        };
    },
    methods: {
        async fillForm() {

            this.clearFields();
            const passport = await readXlsxFile(this.excel_file);
            let skipKey = this.updateForm? '1.1.': '';

            for (let [key, , value] of passport) {
                
                if (!key || key == skipKey) continue;

                if (/^\d\./.test(key) && value != null) {
                    const nowValue = DictPassport.getValue(key, value, true);
                    if (nowValue) {
                        this.formData[nowValue.key] = nowValue.value;
                    }
                }
            }

            for (let key of ["responsible", "sub_system", "criticality", "priority"]) {
               
                if ( this[key].indexOf(this.formData[key]) == -1 ) {
                    this.formData[key] = "";
                }
            }

         
        },
        clearFields() {

            let keys = Object.keys(this.formData);
            if (this.updateForm) keys = keys.slice(1, -1);
            
            keys.forEach((key) => {
                this.formData[key] = '';
            })
        },
        oninputs(val){
            
            try{
            let str=this.formatDateRev(val)
            const newdate=moment(str)
            // =newdate.format("YYYY-MM-DD")
            if (newdate.isValid()){
              this.formData[this.datakey]=str
            }            
            }catch{ 
                     
            }
            
          },

        dateFormatted(key) {
            
            const date = this.formData[key];

            if (!date) return null;
            const [year, month, day] = date.split("-");
            return `${day}.${month}.${year}`;
           
        },

        submitPForm() {

            const data = Object.assign(this.formData);
                        
            if (this.formData.probability_of_occurrence == "") {
                delete data['probability_of_occurrence']
            }
            
            this.$emit('save', data);
        },
        backMain() {
            this.$emit('backMain');
        }
    },
    computed: {

        ...(function() {
            const formatingDateFields = ['algorithm_creation_period', 'selection_aproval_period', 'date_of_formation_of_the_initial_list'];
            return formatingDateFields.reduce((acc, val, index) => {

                acc[`dateFormatted${index+1}`] = {
                    set(value) {
                        this.formData[val] = value;
                    },
                    get() {
                        return this.dateFormatted(val)
                    }
                }

                return acc;
            }, {});
        })(),

        correctBoolean: {
            set(value) {
                this.formData.probability_of_occurrence = value == "Да" ? true : false;
            },
            get() {

                if (typeof this.formData.probability_of_occurrence == "string") {
                    return "";
                } 

                return this.formData.probability_of_occurrence? "Да": "Нет";
                
            },
        },
    },
    mounted() {
        this.superuser = JSON.parse(localStorage.getItem('profile'))["is_superuser"]
    
        if (this.fillData) {
            for (let [key, val] of Object.entries(this.fillData)) {
                this.formData[key] = val;
            }
        };
        
    }, 
    //  watch: {
    //     datefrom (val) {
    //         this.dateFormatted = this.formatDate(this.datefrom)
    //     },
    //     dateFormatted(val) {
    //         this.update();
    //     }
    // },
    
};
</script>

<style lang="scss">


// #eeebef
.main-bg {
    background-color: #eeebef;
    height: 100%;
}

.bg-card {
    background-color: #f5f6fa;
}

.title-block {
    color: #666666;
}

.custom.v-text-field > .v-input__control > .v-input__slot:before {
    border-style: none;
}
.custom.v-text-field > .v-input__control > .v-input__slot:after {
    border-style: none;
}

.custom.v-text-field.v-input--dense .v-input__append-inner {
    margin-top: 2px;
}

.custom {
    border: 1px solid black;
    border-radius: 0.3rem;
    padding: 0.1rem 0.5rem;
}
.mh26{
    max-height: 2.5rem;
}

.input-normal {
    border: 1px solid black;
    border-radius: 0.3rem;
    padding: 0.1rem 0.2rem;
}

label {
    pointer-events: none;
}

.v-text-field.v-text-field--solo .v-input__control {
    min-height: 10px;
}

.input-normal.shown {
    border: none;
    pointer-events: none;
    padding: 0;
}

.input-normal:focus {
    outline: none;
    box-shadow: 0 0 0 1px black;
}


</style>