<template>
    <v-container
        class=" flex-col shell-filters"
        fluid
    >
        <v-row class="pl-2">
            <v-col>
                <h2>{{header}}</h2>
            </v-col>
            <v-col>
                <v-row >
                    <v-col
                        class="flex-row justify-end pr-1"    
                    >
                        <v-tooltip
                            v-if="helper.length"
                            color="primary"
                            bottom
                        >
                            <template
                                v-slot:activator="{ on, attrs }"
                            >
                                <v-icon 
                                    style="cursor:pointer"
                                    v-bind="attrs"
                                    v-on="on"
                                >
                                    mdi-help
                                </v-icon>
                            </template>
                                <span>{{helper}}</span>
                        </v-tooltip>
                        <v-icon
                            :class="[iconreverse? 'up': '', 'icon-down']"
                            @click="reverse"
                        >
                            mdi-chevron-up-circle-outline
                        </v-icon> 
                    </v-col>
                </v-row>
            </v-col> 
        </v-row>
        <!-- <v-row  class="pl-4 pr-3">
            <v-col> -->
                <transition
                    name="slide"
                    @afterLeave="endAnimation"
                    @afterEnter="endAnimation"
                >
                    <v-row  class="pl-4 pr-3"
                        v-if="isShow"
                    >
                        <slot name="toptext"></slot>                        
                        <slot name="filterslist"></slot>
                        <v-col
                            class="pt-0 pr-1  flex-row flex-nowrap align-end justify-end col_btn_apply_reset"
                        >
                            <v-btn
                                class="btn-filter"
                                height='30'
                                width='100'
                                @click="$emit('sendData')"
                            >
                                ПРИМЕНИТЬ
                            </v-btn>
                            <v-btn
                                height='30'
                                width='100'
                                @click="$emit('clear')"
                            >
                                СБРОСИТЬ
                            </v-btn>
                        </v-col>
                    </v-row>
                </transition>                  
            <!-- </v-col>
        </v-row> -->
    </v-container>
    <!-- <div class="shell-filters px-4  pr-0 mr-0">
        <div class="d-flex justify-space-between title-filters pt-2 pb-2 pl-1 pr-4 ">
            <h2 class="">{{header}}</h2>

            <div>
                <v-tooltip v-if="helper.length"
                                         color="primary"
                                          bottom>
                                        <template v-slot:activator="{ on, attrs }">
        

                                         <v-icon 
                                        style="cursor:pointer"
                                          v-bind="attrs"
                                        v-on="on"
                                        >mdi-help</v-icon>
                                    </template>
                                    <span>{{helper}}</span>
                                    </v-tooltip>






            <v-icon
                :class="[iconreverse? 'up': '', 'icon-down']"
                @click="reverse"
            >
                mdi-chevron-up-circle-outline
            </v-icon> 
            </div>
        </div>
        <transition
            name="slide"
            @afterLeave="endAnimation"
            @afterEnter="endAnimation"
        >

   
            <div
                class=""
                v-if="isShow"
            >
                <slot name="toptext"></slot>
                
                <v-row class=" px-4 mb-2">
                    <slot name="filterslist"></slot>
                    <v-col
                    cols=2
                    
                    class="ml-auto">
                    <div class="d-flex align-end align-content-end  mt-auto" style="height:100%">
                    <v-btn class="ml-auto btn-filter mr-1 "  height='30' @click="$emit('sendData')" >ПРИМЕНИТЬ</v-btn>
                    <v-btn class=""  height='30' @click="$emit('clear')" >СБРОСИТЬ</v-btn>
                    </div>
                </v-col>
                </v-row>
                
                
            </div>
        </transition>  
    </div> -->

</template>

<script>
    export default {
        name: 'filters-bar',
        props:{
            helper:{
                type:String,
                default:""
            },
            header:{
                type: String,
                default: 'ФИЛЬТРЫ'
            }


        },
        data() {
            return {
                iconreverse: false,
                isShow: true,
            }
        },
        methods: {
            reverse() {
                this.iconreverse = !this.iconreverse;
                this.isShow = !this.isShow;
                
                   
            },
            endAnimation() {
                this.$emit("cbArrow");
            }
        },
        beforeDestroy() {
           
            this.$store.commit('filterslogic/filtersClear');
        }
        
    }
</script>

<style lang="scss" scoped>
    @import '@/utils/colors.scss';

.col_btn_apply_reset {
    gap: 15px;
}

    .shell-filters {
        z-index: 12;
        background: white;
        font-size: 1em;
        box-shadow: 0 2px 3px $gray;

        .title-filters {
            cursor: pointer;
        }

        h2 {
            color: $bg-purple;
            font-size: 1rem !important;
        }

        .icon-down {
            color: $bg-purple;
            transition: transform ease-in .2s;
            transform: rotate(0deg);
            font-size: 1.2rem !important;
        }

        .icon-down.up {
            transform: rotate(180deg);
        }

       .btn-filter {
            background-color: $bg-purple;
            color: white;
        }
        
    }

    .slide-enter-active {
        -moz-transition-duration: 0.3s;
        -webkit-transition-duration: 0.3s;
        -o-transition-duration: 0.3s;
        transition-duration: 0.3s;
        -moz-transition-timing-function: ease-in;
        -webkit-transition-timing-function: ease-in;
        -o-transition-timing-function: ease-in;
        transition-timing-function: ease-in;
    }

    .slide-leave-active {
        -moz-transition-duration: 0.3s;
        -webkit-transition-duration: 0.3s;
        -o-transition-duration: 0.3s;
        transition-duration: 0.3s;
        -moz-transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
        -webkit-transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
        -o-transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
        transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
    }

    .slide-enter-to, .slide-leave {
        max-height: 500px;
        overflow: hidden;
    }

    .slide-enter, .slide-leave-to {
        overflow: hidden;
        max-height: 0;
    }
    
 
</style>