import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import ru from 'vuetify/lib/locale/ru';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    options: {
      customProperties: true,

    },
    themes: {
      light: {
        primary: '#43425D',
        secondary: '#424242',
        accent: '#82B1FF',
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FFC107'
      },
      dark: {
        primary: '#43425D',
        secondary: '#424242',
        accent: '#FF4081',
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FB8C00',
      },
    },
  },
    lang: {
      locales: { ru },
      current: 'ru',
    },
  icons: {
    iconfont: 'mdi',
  },
});
