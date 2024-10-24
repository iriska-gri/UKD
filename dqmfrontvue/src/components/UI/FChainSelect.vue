<template>
    <v-col class="pb-3 pt-1 px-1">
        <v-row
            class="pa-3 pl-2 flex-nowrap"
        >
            <v-col 
                lg="6"
                sm="6"
                class="pa-0 pl-1"
            >
                <layout-label
                    class="text-nowrap"
                    :title="withtitle"
                    :disabled="disabled"
                >
                    <v-row
                        class="ma-0"
                    >
                        <v-col
                            v-if="period"
                            class="pa-0   flex-grow-0 align-self-center"
                            lg="1"
                        >
                            <span
                                
                                class="prefix-select"
                                :class="disabled?'graycolor':''"
                            >
                                с 
                            </span>
                        </v-col>
                        <v-col
                            :lg="period?'11':'12'"
                            class="pa-0 pr-1"
                        >
                            <v-autocomplete
                                :items="itemswithdate"
                                v-model="withdate"
                                :clearable="cleaner"
                                :disabled="disabled"
                                dense
                                solo
                                hide-details="true"
                            >
                            </v-autocomplete>
                        </v-col>
                    </v-row> 
                </layout-label>
            </v-col>
            <v-col
                lg="6"
                sm="6"
                class="pa-0 pl-1"
            >
                <layout-label
                    :title="bytitle"
                    :disabled="disabled"
                    class="text-nowrap"
                >
                    <v-row
                        class="ma-0"
                    >
                        <v-col
                            v-if="period"
                            class="pa-0 flex-grow-0 align-self-center"
                            lg="1"
                        >
                            <span
                                class="prefix-select"
                                :class="disabled?'graycolor':''"
                            >
                                по 
                            </span>
                        </v-col>
                        <v-col
                            :lg="period?'11':'12'"
                            class="pa-0 pl-1"
                        >
                            <v-autocomplete
                                :items="itemsbydate"
                                v-model="bydate"
                                :clearable="cleaner"
                                :disabled="disabled"
                                dense
                                solo
                                hide-details="true"
                                :menu-props="{closeOnContentClick:true}"
                            >
                            </v-autocomplete>
                        </v-col>
                    </v-row>
                </layout-label>
            </v-col>
        </v-row>
    </v-col>
    <!-- <v-row>
        <v-col>
            <layout-label :title="withtitle">
                <div class="d-flex align-center">
                    <span v-if="period" class="me-2 prefix-select">с</span>
                    
                    <v-select
                        :items="itemswithdate"
                        v-model="withdate"
                        :clearable="cleaner"
                        :disabled="disabled"
                        dense
                        solo
                        hide-details="true"
                    >

                    </v-select>
                </div>
            </layout-label>
        </v-col>
        <v-col>
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
                    </v-select>
                </div>
            </layout-label>
        </v-col>
    </v-row> -->
</template>

<script>
import moment from 'moment';
export default {
    name: "f-chain-select",
    data() {
        return {
            methodBefore: '',
            methodAfter: '',
        }
    },
    props: {
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
    color: $bg-purple;
    font-family: "Roboto", Arial, Helvetica, sans-serif;
    font-weight: bold;
}

.graycolor{
    color: $gray;
}
</style>