/*
TODO:
 - https://www.npmjs.com/package/protobufjs#using-proto-files
 - https://programmer.help/blogs/how-to-use-protobuf-in-the-front-end-vue-chapter.html
 - https://router.vuejs.org/
 - https://github.com/vuejs/vue-router/tree/dev/examples
*/
import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

import { iceworm } from './proto/bundle'
const { WebServiceStatus } = iceworm

let message = WebServiceStatus.create({ uptime: 42. })
let buffer  = WebServiceStatus.encode(message).finish()
let decoded = WebServiceStatus.decode(buffer)
console.log(decoded)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
