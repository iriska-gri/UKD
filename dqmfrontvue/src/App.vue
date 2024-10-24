<template>

  <component :is="layout">
    <router-view/>
     
  </component>
  
  
</template>

<script>

export default {
  name: 'App',
   

  computed: {
    layout() {
      if (this.$route.meta.layout) {
        return (this.$route.meta.layout || 'default') + '-layout'
      }
      
    }
  }
};
</script>
<style lang="scss">

@import "@/utils/colors.scss";
  .v-data-table-header th {
  // position: absolute;
  z-index: 2 !important;
}

h2 {
    color: $bg-purple;
    font-size: 1rem !important;
}

.pointer{
  cursor: pointer;
}

.activetab{
    color: $bg-maincont !important;
    background: $bg-purple;
    border-radius: 5px 5px 0px 0px;
}

.alertt{
  background-color: rgb(240, 136, 136) ;
}

.alertt:hover{
  background-color: #eee ;
}
  .select-page {
    max-width: 85px;
    

    .v-text-field--box .v-input__slot, .v-input__control .v-input__slot{
       min-height: 2.5rem !important;
     }
    //  .v-text-field--box .v-input__slot, .v-input__control .v-input__slot{
    //    max-height:15px !important;
    //  }
  }

  .v-application--is-ltr .v-menu__content .v-list-item__action:first-child {
    margin-right: 14px;
  }

  .pointertable {
      cursor: pointer;
  
  }
  
  // .v-data-table__wrapper::-webkit-scrollbar {
    // width: 0px;
    // display: none;
// }


.grow-table {
        display: flex;
        flex-direction: column;
        overflow-y: auto;
            }
            
.excel {
    cursor: pointer;
    background: white;
    font-size: 1.5rem !important;
}

.Form .v-label {
    font-size: 16px!important;
}

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
/* Track */
::-webkit-scrollbar-track {
   
    -webkit-border-radius: 6px;
    border-radius: 6px;
}
/* Handle */
::-webkit-scrollbar-thumb {
    -webkit-border-radius: 6px;
    border-radius: 6px;
    background: $bg-purple; 
  
}
::-webkit-scrollbar-thumb:window-inactive {
    background: $bg-purple; 
}








* {
    font-size: .85rem !important;
}

.v-data-table--fixed-header>.v-data-table__wrapper>table>thead>tr>th {
    border-bottom: 0!important;
    position: sticky;
    top: 0px;
    padding: 8px 8px 0 8px!important;
    text-align: end;
    z-index: 2;
    vertical-align: -webkit-baseline-middle;
}

// ------------------------------------- Стилизация флексов
.flex-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  // background: rgb(238, 235, 239);
  background:$bg-newsbg;
}

.flex-item {
  flex-grow: 1;
}

.flex-static_row {
  flex: 0 0 auto;
  display: flex  !important;
  flex-direction: row;
  flex-wrap: wrap;
}

.flex-row {
  display: flex !important;
  flex-direction: row;
  flex-wrap: wrap;
}

.flex-col {
  display: flex !important;
  flex-direction: column;
}




// ------------------------------------- Стилизация Грид

.grid-container {
  overflow-y: hidden;
  height: 100vh;
  display: grid;
}


// ------------------------------------- Стилизация Фильтров
.FIL_item {
  gap: 12px;   
}

.filtr, .filtrDuo {
    width: 30%;
    min-width: 240px;
    align-self: flex-end;
}

.filtrDuo {
  flex-wrap: nowrap;
}

.FIL_item_1, .FIL_item_2, .FIL_item_3, .FIL_item_4, .FIL_item_5, .FIL_item_6, .FIL_item_7, .FIL_item_8, .FIL_item_9 {
    width: 30%;
    min-width: 240px;
    align-self: flex-end;
    
}
// ------------------------------------- Стилизация Таблицы
    // Динамическая высота для таблицы
    .scroll-block {
        display: flex;
        flex-direction: column;
        overflow-y: hidden;
        flex-grow: 3;
        height: 100%;
        margin-top: 10px;
    }
// -------------------------------------- Стилизация Canvas

.card_Mybar_item_1 {
      width: 100%;
      height: 100%;
      justify-content: center;

}

// ---------------------------------------Высота и ширина

.h-100 {
  height: 100%;
}

.w-100 {
   width: 100%;
}



@media (max-width: 1500px) {
  .grid-container {
  overflow-y: auto;
}
}

// -------------------------------------- Для контейнеров

.bg1 {
  background: goldenrod;
}

.bg2 {
  background: rgb(66, 32, 218);
}

.bg3 {
  background: rgb(32, 218, 72);
}

.bg4 {
  background: rgb(218, 54, 32);
}

.bg5 {
  background: rgb(150, 32, 218);
}

.bg6 {
  background: rgb(32, 106, 218);
}

.bg7 {
  background: rgb(52, 226, 101);
}

.bg8 {
  background: rgb(72, 79, 92);
}

.bg9 {
  background: rgb(180, 231, 147);
}

.bg10 {
  background: rgb(240, 243, 45);
}

// -------------------------------------- Для flex Vuetify

.vh-100 {
  min-height: 100vh;
}

.text-nowrap {
    white-space: nowrap;
}


.text-center {
  text-align: center;
}

.text-bottom {
  display: grid;
    align-items: end;
    justify-content: center;
}

</style>
