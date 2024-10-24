<template>
    <v-col class="pb-3 pt-1 px-1">
    <layout-label
        :title="title"
        class="text-nowrap"
    >
    <!-- <v-row>
    <v-col>
    <span class="prefix-select flex-grow-0">с</span>
                <v-select
                :items="itemswithdate"
                v-model="withdate"
                dense
                solo
                :clearable="cleaner"
                hide-details="true"
            >
            </v-select>
            </v-col>
    </v-row> 
     -->
    <v-row class="ma-0">
        <v-col
            class="flex-grow-0 pa-0 pr-2 align-self-center"
        >
            <span class="prefix-select">с</span>
        </v-col>
        <v-col
            class="pa-0"
        >
            <v-autocomplete
                :items="itemswithdate"
                v-model="withdate"
                dense
                solo
                :clearable="cleaner"
                hide-details="true"
            >
            </v-autocomplete>
        </v-col>
        <v-col
            class="flex-grow-0 pa-0 px-2 align-self-center"
        >
            <span class="prefix-select ">по</span>
        </v-col>
        <v-col
            class="pa-0"
        >
            <v-select
                :items="itemsbydate"
                v-model="bydate"
                dense
                solo
                :clearable="cleaner"
                hide-details="true"
            >
            </v-select>
        </v-col>
    </v-row>
    
    </layout-label>
   </v-col>
</template>

<script>
import moment from "moment";
export default {
    name: "fc-chain-select",
    data() {
        return {
            nowVal: {
                with: '',
                by: '',
            }
        };
    },
    props: {
        cleaner: {
            type: Boolean,
            default: false,
        },
        title: {
            type: String,
            default: "⁣",
        },
        items: {
            type: Array
        },
        value: [String, Object],
    },

    methods: {
        UTCDate(date) {
            return moment(date, "DD.MM.YYYY");
        },
        sortDateSelect(date, method = "isSameOrBefore") {
            let arr = [...this.getterItems];
        
            if (arr.length == 1 || arr.length == 0) return arr;
            if (!date) {
                arr =
                    method == "isSameOrBefore"
                        ? arr.slice(0, arr.length - 1)
                        : arr.slice(1, arr.length);
                return arr;
            }
            return [...arr].filter((value) => {
                return this.UTCDate(value)[method](this.UTCDate(date))
            });
        },
        // clean() {
        //     this.withdate = "";
        //     this.bydate = "";
        // },
    },
    computed: {
        getterItems() {
            return this.items.map((el) => {
                let [year, month, day] = el.split('-');
                return `${day}.${month}.${year}`;
            })
        },
        itemswithdate() {
            return this.sortDateSelect(this.bydate);
        },
        itemsbydate() {
            return this.sortDateSelect(this.withdate, "isSameOrAfter");
        },
        withdate: {
            get() {
                return this.nowVal.with? this.$changeFormatDate(this.nowVal.with): '';
            },
            set(value) {
                this.nowVal.with = this.$changeFormatDateReverse(value);
                this.$emit('input', this.nowVal);
            },
        },
        bydate: {
            get() {
                return this.nowVal.with? this.$changeFormatDate(this.nowVal.by): '';
            },
            set(value) {
                this.nowVal.by = this.$changeFormatDateReverse(value);
                this.$emit('input', this.nowVal);
            },
        },
    },
};
</script>

<style lang="scss" scoped>
@import "@/utils/colors.scss";
.prefix-select {
    color: $bg-purple;
    font-family: "Roboto", Arial, Helvetica, sans-serif;
    font-weight: bold;
}

</style>