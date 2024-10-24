import moment from "moment";
export default {
  namespaced: true,
  state: {
    // Фильтры
    date:'',
    mult_date:[],
    date_unloading__ens:[],
    date_unloading: [],
    mult_date_unloading: [],
    mult_date_unloading__ens:[],
    region__name: [],
    mult_region__name: [],
    user__region__name: [],
    mult_user__region__name: [],
    region__tax_code: [],
    mult_region__tax_code: [],
    passport__code: [],
    passport__name:[],
    mult_passport__name:[],
    mult_passport__code: [],
    justify__reason__name: [],
    mult_justify__reason__name: [],
    justify__fix_status: [],
    mult_justify__fix_status: [],
    mult_justify__methodologist:[],
    justify__methodologist:[],
    type_error:[],
    mult_type_error:[1,2,3]
  },

  getters: {
    date(state) {      
      return state.date;
    },
    mult_date(state) {      
      return state.mult_date;
    },
    
 
    // Геттеры фильтров
    date_unloading__ens(state) {      
      return state.date_unloading__ens;
    },
    mult_date_unloading__ens(state) {     
      if (['/loadfile'].includes(String(window.location.pathname))){
        return state.mult_date_unloading__ens.map((el) =>{
          
          if (el=="1900-01-01") return 'Первоначальная'        
          return moment(el).format("DD.MM.YYYY")}
        );
      }
   
     },

    date_unloading(state) {
      
      return state.date_unloading;
    },
    mult_date_unloading(state) {     
      if (['/statistic/monitoring','/statistic/monitoringifns','/loadfile','/statistic/list', '/ens/monitoring','/ens/monitoringifns','/ens/list'].includes(String(window.location.pathname))){
        return state.mult_date_unloading.map((el) =>{
          
          if (el=="1900-01-01") return 'Первоначальная'        
          return moment(el).format("DD.MM.YYYY")}
        );
      }
      else{ 
         console.log("dsggsdrdrg");
        let a= state.mult_date_unloading.filter(element => element != '1900-01-01')   
        return a.map((el) =>{     
          return moment(el).format("DD.MM.YYYY")}
        );
     }
      // return state.mult_date_unloading.filter(element => element != "1900-01-01").map((el) =>
      //   moment(el).format("DD.MM.YYYY")
      // );
    },
    type_error(state){
      return state.type_error
    },
    mult_type_error(state){     
      return state.mult_type_error
      .map((el)=>      
      {        
        if (el==1){
         
          return "Старые НД"}
        else if (el==2) {return 'Новые НД' }
        else {return 'ВПНД'}
    })
    },
    passport__name(state) {
    
      return state.passport__name;
    },
    mult_passport__name(state) {
   
      return state.mult_passport__name
    },
    region__name(state) {
    
      return state.region__name;
      },

      user__region__name(state) {
    
        return state.user__region__name;
      },
      mult_user__region__name(state) {
   
        return state.mult_user__region__name.map((el) => el.join('. '));
      },


    mult_region__name(state) {
   
      return state.mult_region__name.map((el) => el.join('. '));
    },
    region__tax_code(state) {
      return state.region__tax_code;
    },
    mult_region__tax_code(state) {
      return state.mult_region__tax_code;
    },
    passport__code(state) {
      return state.passport__code;
    },
    mult_passport__code(state) {
      return state.mult_passport__code;
    },
    justify__reason__name(state) {
      return state.justify__reason__name;
    },
    mult_justify__reason__name(state) {
      return state.mult_justify__reason__name;
    },
    justify__fix_status(state) {    
      
      return state.justify__fix_status;
    },
    mult_justify__fix_status(state) {
     
      return state.mult_justify__fix_status.map((el) => {
        if (el==null){return "На согласовании"}
        else if (el==true) {return 'Согласовано' }
        else {return 'Не согласовано'}
        })},
    justify__methodologist(state) {
      return state.justify__methodologist;
    },
    mult_justify__methodologist(state) {
      return state.mult_justify__methodologist;
    },
  },
  mutations: {
    addFilter(state, { key, value }) {
      
      state[key] = value;
    
    },
  
  },
  actions: {
    addFilter({state, commit, rootState}, { key, value }) {
      // Добавляет фильтр в хранилище

      commit('addFilter', {key, value})
    
      if (key.slice(0, 4) != "mult") {
        if (value.length == 0) {
          
          delete rootState.filterslogic.activefilters[key];
          return;
        }
      
        rootState.filterslogic.activefilters[key] = {value, postfix: '__in', module: 'mult'};
        
      }
      // rootState.filterslogic.activefilters[key] = {value, postfix: '__in', module: 'mult'};
      
    },
  }
};