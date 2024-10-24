import Vue from 'vue'
import VueRouter from 'vue-router'
import {baseURL} from '@/utils/axios-api'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import('@/views/Auth.vue'),
    meta: {
      layout: 'auth', authNeed: false
    }
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('@/views/Search.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/statistic/monitoring',
    name: 'staticticmonitoring',
    component: () => import('@/views/statistic/StatisticMonitoring.vue'),
    props:{ifns:false},
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/statistic/monitoringifns',
    name: 'staticticmonitoringifns',
    component: () => import('@/views/statistic/StatisticMonitoring.vue'),
    props:{ifns:true},
    meta: {
      layout: 'default', authNeed: true
      
    }
  },
  {
    path: '/statistic/list',
    name: 'staticticlist',
    component: () => import('@/views/statistic/StatisticList.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/statistic/justification',
    name: 'staticticjustification',
    component: () => import('@/views/statistic/StatisticJustification.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/statistic/maindocs',
    name: 'fb1maindocs',
    component: () => import('@/views/statistic/FB1maindocks.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/statistic/passports',
    name: 'staticticpassports',
    component: () => import('@/views/statistic/PassportsNormalize.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/statistic/passport/add',
    name: 'staticticpassportsadd',
    component: () => import('@/views/statistic/AddPassportsNormalize.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/statistic/dynamics',
    name: 'dynamics',
    component: () => import('@/views/statistic/Dynamics.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },

  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/wizard',
    name: 'wizard',
    component: () => import('@/views/Wizardlist.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/wizard/card',
    name: 'wizardcard',
    component: () => import('@/views/Wizard.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/wizard/schema',
    name: 'wizardschema',
    component: () => import('@/views/Wizardschema.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/sandbox',
    name: 'sandbox',
    component: () => import('@/views/Sandbox.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/helper',
    name: 'helper',
    component: () => import('@/views/Helper.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/Settings.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/loadfile',
    name: 'loadfile',
    component: () => import('@/views/LoadFile.vue'),
    meta: {
      layout: 'default', authNeed: true
    }
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => window.location.href =  baseURL +'admin/',
    meta: {
      layout: 'auth', authNeed: false
    }
  },
  {
    // catch all 404 - define at the very end
    path: "*",
    component: () => import("@/views/NotFound.vue"),
    meta: {
      layout: 'auth', authNeed: false
    }
    },

// енс
    {
      path: '/ens/passports',
      name: 'enspassports',
      component: () => import('@/views/ens/ENSPassportsNormalize.vue'),
      meta: {
        layout: 'default', authNeed: true
      }
    },

    {
      path: '/ens/list',
      name: 'enslist',
      component: () => import('@/views/ens/ensList.vue'),
      meta: {
        layout: 'default', authNeed: true
      }
    },
    {
      path: '/ens/monitoring',
      name: 'ensmonitoring',
      component: () => import('@/views/ens/ensMonitoring.vue'),
      props:{ifns:false},
      meta: {
        layout: 'default', authNeed: true
      }
    },
    {
      path: '/ens/monitoringifns',
      name: 'ensmonitoringifns',
      component: () => import('@/views/ens/ensMonitoring.vue'),
      props:{ifns:true},
      meta: {
        layout: 'default', authNeed: true
        
      }
    },
    {
      path: '/ens/dashboard',
      name: 'ensdashboard',
      component: () => import('@/views/ens/ensDashboard.vue'),
      meta: {
        layout: 'default', authNeed: true
      }
    },
    {
      path: '/ens/maindocs',
      name: 'ensmaindocs',
      component: () => import('@/views/ens/ensmaindocks.vue'),
      meta: {
        layout: 'default', authNeed: true
      }
    },







]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {

  const users = localStorage.getItem('access');
  const requireAuth = to.matched.some(record => (record.meta.authNeed));

  if (users) {
    if (to.fullPath == '/auth') {
      next('/');
    } else {
      next();
    }

  } else {
    if (requireAuth) {
      next('/auth');
    } else {
      next()
    }
  }

 

});

export default router
