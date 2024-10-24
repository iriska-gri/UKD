import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import components from '@/components/UI/index'
import '@babel/polyfill'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'
// Подумать, сто м этм делпть
import 'devextreme/dist/css/dx.light.css';
import '@/utils/css/dx-diagram.css';

import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import { axiosApiInstance } from '@/utils/axios-api'
import globalFuncs from '@/utils/helper'





Vue.component('default-layout', DefaultLayout)
Vue.component('auth-layout', AuthLayout)
components.forEach((component) => {
  Vue.component(component.name, component);
})

Vue.config.productionTip = false
Vue.prototype.$http = axiosApiInstance;
for (let [name, func] of Object.entries(globalFuncs)) {
  Vue.prototype[`$${name}`] = func;
}


new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')


export const bus = new Vue()