/*
TODO:
 - https://www.npmjs.com/package/protobufjs#using-proto-files
 - https://programmer.help/blogs/how-to-use-protobuf-in-the-front-end-vue-chapter.html
*/
import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

// import iceworm from './proto/proto'

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
