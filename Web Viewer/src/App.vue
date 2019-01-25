<template>
  <div id="app">
    <div v-if="password !== 'conway'" class="password-overlay">
      <div class="password-container">
        <div class="password-form">
          <md-field>
            <label>Password toggle</label>
            <md-input v-model="password" type="password"></md-input>
          </md-field>
        </div>
      </div>
    </div>
    <template v-if="password === 'conway'">
      <div class="page-container">
        <md-app md-mode="fixed">
          <md-app-toolbar class="md-primary md-medium">
            <img class="logo" src="./assets/images/colophon-logo-white-01.svg" alt="">
            <span class="md-title logo-header">
              Colophon Foundry
            </span>
            <div class="md-toolbar-section-end nav-header">
              <li>
                <router-link :to="{ name: 'headlines' }" exact>
                  Headlines
                  <span></span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'proofer' }" exact>
                  Proofer
                  <span></span>
                </router-link>
              </li>
              <li>
                <router-link :to="{ name: 'applications' }" exact>
                  Applications
                  <span></span>
                </router-link>
              </li>
            </div>
          </md-app-toolbar>
          <md-app-drawer md-permanent="clipped">
            <md-toolbar class="md-transparent controls-header md-medium" md-elevation="0">
               <span class="md-title">Controls</span>
            </md-toolbar>
            <SliderContainer />
          </md-app-drawer>
          <md-app-content>
            <FunContainer />
          </md-app-content>
        </md-app>
      </div>
    </template>
  </div>
</template>

<script>
import FunContainer from './components/FunContainer.vue'
import SliderContainer from './components/SliderContainer.vue'
export default {
  name: 'app',
  components: {
    FunContainer,
    SliderContainer
  },
  data() {
    return {
      password: ''
    }
  }
}
</script>
