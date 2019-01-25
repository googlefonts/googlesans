import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    weight: 400,
    spacing: 100,
    characterWidth: 0,
    ascenderHeight: 0,
    counterAperture: 0,
    typefaceSelected: "Google Sans Text"
  },
  getters: {
    weight: state => state.weight,
    spacing: state => state.spacing,
    characterWidth: state => state.characterWidth,
    ascenderHeight: state => state.ascenderHeight,
    counterAperture: state => state.counterAperture,
    typefaceSelected: state => state.typefaceSelected,
    typefaceStyle: state => "font-family: '" + state.typefaceSelected + "', 'Google Sans';",
    variables: state => "font-variation-settings: 'wght' " + state.weight + ", 'ital' " + state.spacing + ", 'CUS2' " + state.characterWidth + ", 'CUS3' " + state.ascenderHeight + ", 'CUS4' " + state.counterAperture + ", 'opsz' " + 170 + "; transition: font-variation-settings 0.5s;",
  },
  mutations: {
    setWeight(state, payload) {
      state.weight = payload
    },
    setSpacing(state, payload) {
      state.spacing = payload
    },
    setCharacterWidth(state, payload) {
      state.characterWidth = payload
    },
    setAscenderHeight(state, payload) {
      state.ascenderHeight = payload
    },
    setCounterAperture(state, payload) {
      state.counterAperture = payload
    },
    setTypefaceSelected(state, payload) {
      state.typefaceSelected = payload
    }
  }
})
