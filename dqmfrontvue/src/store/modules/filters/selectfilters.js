import moment from "moment";
let convertDate = (date) => {  return moment(date, 'DD.MM.YYYY').format('YYYY-MM-DD');
}
export default {
  namespaced: true,
  state: {
    // Фильтры
    date:"",
    mult_date:[],
    justify__deadline_for_correction: '',
    mult_justify__deadline_for_correction: [],
    type_error:'',
    date_unloading:"",
    mult_date_unloading:[],
    mult_date_unloading__ens:[],
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
    date_unloading(state) {
      return state.date_unloading;
    },
    justify__deadline_for_correction(state) {
      return state.justify__deadline_for_correction;
    },
    mult_justify__deadline_for_correction(state) {
      return state.mult_justify__deadline_for_correction.map((el) =>
        moment(el).format("DD.MM.YYYY")
      );
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
  
  }

   
  },
  mutations: {
    addFilter(state, { key, value }) {
   
      state[key] = value;
    }
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
       
        // rootState.filterslogic.activefilters[key] = {value:convertDate(value), postfix: '', module: 'select'};
        rootState.filterslogic.activefilters[key] = {value:value, postfix: '', module: 'select'};
      }
    },
  }
};

