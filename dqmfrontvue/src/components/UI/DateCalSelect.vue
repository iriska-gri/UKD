<template>
    <v-row>
        <v-col>
            <layout-label :title="withtitle">
                <div class="d-flex align-center">
                    <span v-if="period" class="me-2 prefix-select">с</span>
                    <v-menu 
          
          v-model="date_unloading.model"
          :close-on-content-click="false"
          
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="auto"
        >
          <template v-slot:activator="{on, attrs }">
            <!-- v-model="item.$value" -->
            <v-text-field
              :value="formatDate(date_unloading.value)"              
              type="date-local"
              :label="date_unloading.label"
              @focus="datekey=i"
              @input="oninput"
              v-bind="attrs"
              v-on="on"
              
              class="custom"
            ></v-text-field>
          </template>
          <!-- readonly -->
          <!-- @click:clear="date = null" -->
            <!-- :min="datefrom1" 
            :max="dateto1"
            :events="eventarr" -->
          <v-date-picker
          :first-day-of-week="1"
          
            
            event-color="green lighten-1"
            v-model="date_unloading.value"
           
            
          ></v-date-picker>
           <!-- @input="i==1? datefrom = false:dateto=false" -->
        </v-menu>
                    <!-- <v-select
                        :items="itemswithdate"
                        v-model="withdate"
                        :clearable="cleaner"
                        :disabled="disabled"
                        dense
                        solo
                        hide-details="true"
                    >
                     
                    </v-select> -->
                </div>
            </layout-label>
        </v-col>
        <!-- <v-col>
            <layout-label :title="bytitle">
                <div class="d-flex align-center">
                    <span v-if="period" class="me-2 prefix-select">по</span>
                    <v-select
                        :items="itemsbydate"
                        v-model="bydate"
                        :clearable="cleaner"
                        :disabled="disabled"
                        dense
                        solo
                        hide-details="true"
                        :menu-props="{closeOnContentClick:true}"
                    >
                     <template v-if="cleaner" v-slot:prepend-item>
                            <v-list-item ripple @click="cleans('bydate')">
                                <v-list-item-content>
                                    <v-list-item-title>Очистить</v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>
                        </template> 
                    </v-select>
                </div>
            </layout-label>
        </v-col> -->
        <!-- mdi-checkbox-marked mdi-checkbox-blank-outline-->
    </v-row>
</template>

<script>
import moment from 'moment';
export default {
    name: "date-cal-select",
    data() {
        return {
            methodBefore: '',
            methodAfter: '',
        }
    },
    props: {
        date_unloading:{
            type:Array,
            default:()=> {return []}
            
        },
        period: {
            type: Boolean,
            default: false,
        },
        clean: {
            type: Boolean,
            default: false,
        },
        cleaner: {
            type: Boolean,
            default: false,
        },
        withtitle: {
            type: String,
            default: '⁣'
        },
        bytitle: {
            type: String,
            default: '⁣'
        },
        field: {
            type: String
        },
        watcher: {
            type: Function,
            default: null,
        },
        same: {
            type: Boolean,
            default: false,
        },
        disabled:{
            type: Boolean,
            default: false
        }
    },
    
    methods: {
        // UTCDate(date) {
        //     return moment(date, "DD.MM.YYYY");
        // },
        // sortDateSelect( date, method ) {
        //     let arr = this.$store.getters[`filterslogic/chain/mult_${this.field}`];
        //     if (arr.length == 1 || arr.length == 0) return arr;
        //     if (!date) {
        //         // SameOr
        //         arr = method == this.methodBefore? arr.slice(1, arr.length): arr.slice(0, arr.length-1);
        //         return arr;
        //     }
        //     return [...arr].filter((value) => 
        //         this.UTCDate(value)[method](this.UTCDate(date))
        //     );
        // },
        cleans(type) {

            this[type] = '';
            // this.bydate = '';
        }
    },
    computed: {
        itemswithdate() {
            return this.$store.getters[`filterslogic/chain/mult_${this.field}`];
            // return this.sortDateSelect(this.bydate, this.methodBefore);
        },
        itemsbydate() {
            // SameOr
            return this.$store.getters[`filterslogic/chain/mult_${this.field}`];
            // return this.sortDateSelect(this.withdate, this.methodAfter);
        },
        withdate: {
            get() {
                return this.$store.getters[`filterslogic/chain/with_${this.field}`]
            },
            set(value) {
                this.$store.dispatch('filterslogic/chain/addDate', {key: `with_${this.field}`, value, period: this.period, field: this.field, type: 'with'})
            }
        },
        bydate: {
            get() {
                return this.$store.getters[`filterslogic/chain/by_${this.field}`]
            },
            set(value) {
                this.$store.dispatch('filterslogic/chain/addDate', {key: `by_${this.field}`, value, period: this.period, field: this.field, type: 'by'})
            }
        }

    },
    created() {
        let same = this.same? 'SameOr': '';
        this.methodBefore = `is${same}Before`;
        this.methodAfter = `is${same}After`;
    },
    beforeDestroy() {
        this.$store.dispatch('filterslogic/chain/clearDate', this.field)
        
    },
    watch: {
        withdate() {
            if (this.watcher) {
                this.watcher()
            }
        },
        bydate() {
            if (this.watcher) {
                this.watcher()
            }
        }
    }
    
};
</script>

<style lang="scss" scoped>
@import "@/utils/colors.scss";
.prefix-select {
    color: $gray;
    font-family: "Roboto", Arial, Helvetica, sans-serif;
    font-weight: bold;
}
</style>