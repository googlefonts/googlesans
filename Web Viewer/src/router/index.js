import Vue from 'vue'
import Router from 'vue-router'
import Applications from '@/components/Applications.vue'
import Headlines from '@/components/Headlines.vue'
import Proofer from '@/components/Proofer.vue'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '', component: Headlines, name: 'headlines', props: true },
    { path: '/proofer', component: Proofer, name: 'proofer', props: true },
    { path: '/applications', component: Applications, name: 'applications', props: true },
    { path: '*', redirect: { name: 'headlines' } }
  ],
  mode: 'history'
})
