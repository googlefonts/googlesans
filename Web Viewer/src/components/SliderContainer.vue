<template>
  <div>
    <div class="slider-container md-body-1">
      <p class="md-not-subheader">Select Typeface</p>
      <div>
        <md-button
          @click="changeTypefaceSelected('Google Sans Text')"
          class="md-raised typeface-select"
          :class="{'md-primary': typefaceSelected === 'Google Sans Text', '': typefaceSelected !== 'Google Sans Text'}"
          :md-ripple="false">
          Google Text
        </md-button>
        <md-button
          @click="changeTypefaceSelected('Google Sans')"
          class="md-raised typeface-select"
          :class="{'md-primary': typefaceSelected === 'Google Sans', '': typefaceSelected !== 'Google Sans'}"
          :md-ripple="false">
          Google Sans
        </md-button>
        <md-button
          @click="changeTypefaceSelected('Roboto')"
          class="md-raised typeface-select"
          :class="{'md-primary': typefaceSelected === 'Roboto', '': typefaceSelected !== 'Roboto'}"
          :md-ripple="false">
          Roboto
        </md-button>
      </div>
    </div>
      <md-divider v-show="typefaceSelected === 'Google Sans Text'" />
    <div v-show="typefaceSelected === 'Google Sans Text'" class="slider-container md-body-1">
      <p class="md-not-subheader">Adjust Variables</p>
      <p class="slider-title md-body-2">
        Weight
      </p>
      <vueSlider
        v-model="weight"
        @input="radioClear"
        :min="300"
        :max="400"
        class="g-1">
      </vueSlider>

      <p class="slider-title md-body-2">
        Spacing
      </p>
      <vueSlider
        v-model="spacing"
        @input="radioClear"
        :min="100"
        :max="200"
        class="o-1">
      </vueSlider>

      <p class="slider-title md-body-2">
        Character Width
      </p>
      <vueSlider
        v-model="characterWidth"
        @input="radioClear"
        :min="0"
        :max="100"
        class="o-2">
      </vueSlider>

      <p class="slider-title md-body-2">
        Ascender Height
      </p>
      <vueSlider
        v-model="ascenderHeight"
        @input="radioClear"
        :min="0"
        :max="100"
        class="g-2">
      </vueSlider>

      <p class="slider-title md-body-2">
        Counter Aperture
      </p>
      <vueSlider
        v-model="counterAperture"
        @input="radioClear"
        :min="0"
        :max="100"
        class="l">
      </vueSlider>
    </div>
      <md-divider v-show="typefaceSelected === 'Google Sans Text'" />
    <div v-show="typefaceSelected === 'Google Sans Text'" class="slider-container md-body-1">
      <p class="md-not-subheader">Toggle Extremes</p>
      <div class="md-radio-item">
        <md-radio v-model="radio" @change="radioChange(400, 100, 100, 100, 100)" :class="{'md-checked': weight === 400 && spacing === 100 && characterWidth === 100 && ascenderHeight === 100 && counterAperture === 100}" value="option-1a">
          Option 1A
        </md-radio>
        <md-avatar class="inline-tooltip md-avatar-icon md-primary md-small">
          <md-icon>help</md-icon>
          <md-tooltip md-direction="right">Spacing and weight as per Google Sans, all other changes pushed to the maximum</md-tooltip>
        </md-avatar>
      </div>
      <div class="md-radio-item">
        <md-radio v-model="radio" @change="radioChange(300, 100, 100, 100, 100)" :class="{'md-checked': weight === 300 && spacing === 100 && characterWidth === 100 && ascenderHeight === 100 && counterAperture === 100}" value="option-1b">
          Option 1B
        </md-radio>
        <md-avatar class="inline-tooltip md-avatar-icon md-primary md-small">
          <md-icon>help</md-icon>
          <md-tooltip md-direction="right">Spacing as per Google Sans, all other changes pushed to the maximum</md-tooltip>
        </md-avatar>
      </div>
      <div class="md-radio-item">
        <md-radio v-model="radio" @change="radioChange(400, 200, 100, 100, 100)" :class="{'md-checked': weight === 400 && spacing === 200 && characterWidth === 100 && ascenderHeight === 100 && counterAperture === 100}" value="option-2a">
          Option 2A
        </md-radio>
        <md-avatar class="inline-tooltip md-avatar-icon md-primary md-small">
          <md-icon>help</md-icon>
          <md-tooltip md-direction="right">Weight as per Google Sans, all other changes pushed to the maximum</md-tooltip>
        </md-avatar>
      </div>
      <div class="md-radio-item">
        <md-radio v-model="radio" @change="radioChange(300, 200, 100, 100, 100)" :class="{'md-checked': weight === 300 && spacing === 200 && characterWidth === 100 && ascenderHeight === 100 && counterAperture === 100}" value="option-2b">
          Option 2B
        </md-radio>
        <md-avatar class="inline-tooltip md-avatar-icon md-primary md-small">
          <md-icon>help</md-icon>
          <md-tooltip md-direction="right">All changes pushed to the maximum</md-tooltip>
        </md-avatar>
      </div>
    </div>
    <md-divider v-show="typefaceSelected === 'Google Sans Text'" />
    <div v-show="typefaceSelected === 'Google Sans Text'" class="slider-container md-body-1">
      <p class="md-not-subheader">Colophon Recommends</p>
      <div class="md-radio-item">
        <md-radio v-model="radio" @change="radioChange(400, 150, 70, 80, 70)" :class="{'md-checked': weight === 400 && spacing === 150 && characterWidth === 70 && ascenderHeight === 80 && counterAperture === 70}" value="option-1a">
          Option 3A
        </md-radio>
        <md-avatar class="inline-tooltip md-avatar-icon md-primary md-small">
          <md-icon>help</md-icon>
          <md-tooltip md-direction="right">Optical adjustments set to moderate values</md-tooltip>
        </md-avatar>
      </div>
      <div class="md-radio-item">
        <md-radio v-model="radio" @change="radioChange(350, 150, 70, 80, 70)" :class="{'md-checked': weight === 350 && spacing === 150 && characterWidth === 70 && ascenderHeight === 80 && counterAperture === 70}" value="option-1b">
          Option 3B
        </md-radio>
        <md-avatar class="inline-tooltip md-avatar-icon md-primary md-small">
          <md-icon>help</md-icon>
          <md-tooltip md-direction="right">As 3A, but incrementally lighter</md-tooltip>
        </md-avatar>
      </div>
      <div class="md-radio-item">
        <md-radio v-model="radio" @change="radioChange(380, 150, 70, 80, 70)" :class="{'md-checked': weight === 380 && spacing === 150 && characterWidth === 70 && ascenderHeight === 80 && counterAperture === 70}" value="option-2a">
          Option 4A
        </md-radio>
        <md-avatar class="inline-tooltip md-avatar-icon md-primary md-small">
          <md-icon>help</md-icon>
          <md-tooltip md-direction="right">As 3B but incrementally bolder</md-tooltip>
        </md-avatar>
      </div>
      <div class="md-radio-item">
        <md-radio v-model="radio" @change="radioChange(380, 185, 70, 85, 100)" :class="{'md-checked': weight === 380 && spacing === 185 && characterWidth === 70 && ascenderHeight === 85 && counterAperture === 100}" value="option-2b">
          Option 4B
        </md-radio>
        <md-avatar class="inline-tooltip md-avatar-icon md-primary md-small">
          <md-icon>help</md-icon>
          <md-tooltip md-direction="right">Amplified values set to personal preference</md-tooltip>
        </md-avatar>
      </div>
    </div>
    <!-- <md-divider />
    <div class="slider-container md-body-1">
      <p class="md-not-subheader">Toggle Font Smoothing</p>
      <div>
        <md-button
          @click="fontSmoothingActive = !fontSmoothingActive"
          class="md-raised typeface-select"
          :class="{'md-primary': !fontSmoothingActive, 'md-accent': fontSmoothingActive}"
          :md-ripple="false">
          <template v-if="!fontSmoothingActive">Enable Font Smoothing</template>
          <template v-if="fontSmoothingActive">Disable Font Smoothing</template>
        </md-button>
      </div>
    </div> -->
    <md-divider class="last-divider" />
  <!-- <div v-show="typefaceSelected === 'Google Sans Text'" class="slider-container md-body-1">
    <md-radio v-model="radio" @change="radioChange(300, 100, 0, 0, 0)" :class="{'md-checked': weight === 300 && spacing === 100 && characterWidth === 0 && ascenderHeight === 0 && counterAperture === 0}" value="option-1a">Option 1A</md-radio>
    <md-radio v-model="radio" @change="radioChange(300, 200, 0, 0, 0)" :class="{'md-checked': weight === 300 && spacing === 200 && characterWidth === 0 && ascenderHeight === 0 && counterAperture === 0}" value="option-1b">Option 1B</md-radio>
    <md-radio v-model="radio" @change="radioChange(350, 100, 0, 0, 0)" :class="{'md-checked': weight === 350 && spacing === 100 && characterWidth === 0 && ascenderHeight === 0 && counterAperture === 0}" value="option-2a">Option 2A</md-radio>
    <md-radio v-model="radio" @change="radioChange(350, 200, 0, 0, 0)" :class="{'md-checked': weight === 350 && spacing === 200 && characterWidth === 0 && ascenderHeight === 0 && counterAperture === 0}" value="option-2b">Option 2B</md-radio>
    <br>
    <p>
      Option 1A: the most extreme, with all stylistic changes dialled to the maximum.
    </p>
    <br>
    <p>
      Option 1B: same as Option 1A, but with the maximum spacing applied.
    </p>
    <br>
    <p>
      Option 2A: slightly lighter than Google Sans Regular, with all stylistic changes dialled to the maximum.
    </p>
    <br>
    <p>
      Option 2B: same as Option 2A, but with the maximum spacing applied.
    </p>
  </div> -->
  </div>
</template>

<script>
import vueSlider from 'vue-slider-component'
export default {
  name: 'SliderContainer',
  components: {
    vueSlider
  },
  data() {
    return {
      radio: 'unset'
    }
  },
  computed: {
    computedRadio() {
      return this.radio
    },
    weight: {
      get() {
        return this.$store.state.weight
      },
      set(payload) {
        return this.$store.commit('setWeight', payload)
      }
    },
    spacing: {
      get() {
        return this.$store.state.spacing
      },
      set(payload) {
        return this.$store.commit('setSpacing', payload)
      }
    },
    characterWidth: {
      get() {
        return this.$store.state.characterWidth
      },
      set(payload) {
        return this.$store.commit('setCharacterWidth', payload)
      }
    },
    ascenderHeight: {
      get() {
        return this.$store.state.ascenderHeight
      },
      set(payload) {
        return this.$store.commit('setAscenderHeight', payload)
      }
    },
    counterAperture: {
      get() {
        return this.$store.state.counterAperture
      },
      set(payload) {
        return this.$store.commit('setCounterAperture', payload)
      }
    },
    typefaceSelected() {
      return this.$store.state.typefaceSelected
    }
  },
  methods: {
    radioChange(weight, spacing, characterWidth, ascenderHeight, counterAperture) {
      this.weight = weight
      this.spacing = spacing
      this.characterWidth = characterWidth
      this.ascenderHeight = ascenderHeight
      this.counterAperture = counterAperture
    },
    radioClear() {
      this.radio = ''
    },
    changeTypefaceSelected(payload) {
      this.$store.commit('setTypefaceSelected', payload)
    }
  }
}
</script>

<style lang="scss" scoped>

  .md-radio-item {
    display: flex;
    height: 2.5em;
    align-items: center;
  }

  .inline-tooltip {
    right: 0;
    margin-right: 0 !important;
  }

  .md-not-subheader {
    display: flex;
    align-items: center;
    flex-flow: row wrap;
    font-size: 14px;
    font-weight: 500;
    color: var(--md-theme-default-primary);
    padding-bottom: 1em;
  }

  .last-divider {
    margin-bottom: 4em;
  }

</style>
