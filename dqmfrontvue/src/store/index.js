import Vue from "vue";
import Vuex from "vuex";
import main from "@/store/modules/main";
import addpassport from "@/store/modules/addpassport";
import filterslogic from "@/store/modules/filters/filterslogic";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    main,
    filterslogic,
    addpassport,
  },
});
