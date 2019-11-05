import Vue from 'vue'
import Router from 'vue-router'
import SimpleChoice  from '@/components/SimpleChoice'
import MultipleChoice from '@/components/MultipleChoice'

Vue.use(Router)
/*{
      path: '/',
      name: 'SimpleChoice',
      component: SimpleChoice
    },*/
export default new Router({
  routes: [

    {
      path: '/',
      name: 'SimpleChoice',
      component: SimpleChoice
    }
  ]
})
